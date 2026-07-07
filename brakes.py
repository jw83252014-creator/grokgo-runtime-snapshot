"""grokgo brakes + ledger.

Every paid call goes through check() BEFORE and log() AFTER. No exceptions.
Brakes implemented:
  1. KILLSWITCH file        -> everything stops (touch $GROKGO_ROOT/KILLSWITCH)
  2. Per-task max_turns     -> runaway task dies
  3. Loop detection         -> same (task_id, input-hash) seen twice = spinning;
                               stale hashes expire and failed calls are retryable
  4. Per-lane daily budget  -> 80% downgrades one tier, 100% halts the lane
  5. Halt-on-no-work        -> two consecutive empty outputs parks the lane
                               until a task file NEWER than the park flag arrives
Ledger: every call logged to SQLite (lane, model, tokens, est. cost, status).
"""
import hashlib
import fcntl
import json
import os
import pathlib
import re
import sqlite3
import time

ROOT = pathlib.Path(os.environ.get("GROKGO_ROOT", str(pathlib.Path.home() / "grokgo")))
DB = ROOT / "ledger.db"
KILLSWITCH = ROOT / "KILLSWITCH"
PARKED = ROOT / "parked"
RECEIPTS = ROOT / "receipts"
TIER_ORDER = ["t1", "t2", "t3", "t4"]
DEFAULT_SEEN_HASH_TTL_SECONDS = 24 * 60 * 60
DEFAULT_UNKNOWN_PRICE_PER_MTOK = [15, 75]
RECEIPT_SCHEMA_VERSION = "grokgo.action_receipt.v2"
BEHAVIOR_CLASSES = {
    "new_capability",
    "polish",
    "maintenance",
    "correction",
    "cooperation",
    "unknown",
}
_BEHAVIOR_RULES = (
    (
        "new_file",
        "new_capability",
        re.compile(r"\b(creat(e|ed|ing)|wrote|writing) (a )?(new )?(file|module|script|cell|endpoint|test)\b", re.I),
        2.0,
    ),
    (
        "new_capability",
        "new_capability",
        re.compile(r"\b(implement(ed|ing)?|built|adding support for|integrat(ed|ing)|deployed|shipped|merged)\b", re.I),
        1.5,
    ),
    (
        "external_output",
        "new_capability",
        re.compile(r"\b(publish(ed|ing)?|submitt(ed|ing)|sent (the )?(report|paper|snapshot)|artifact created)\b", re.I),
        1.2,
    ),
    (
        "refactor_only",
        "polish",
        re.compile(r"\b(refactor(ed|ing)?|clean(ed|ing)? up|tid(y|ied|ying)|reorganiz(ed|ing))\b", re.I),
        2.0,
    ),
    (
        "cosmetic",
        "polish",
        re.compile(r"\b(rename[d]?|reword(ed|ing)?|formatt(ed|ing)|whitespace|typo[s]?|docstring|minor (tweak|change|update)|polish(ed|ing)?)\b", re.I),
        1.5,
    ),
    (
        "summary_of_summary",
        "polish",
        re.compile(r"\bsummar(y|ize[d]?) of (the |my )?(previous |earlier |last )?(summary|report|notes)\b", re.I),
        2.5,
    ),
    (
        "error_detected",
        "correction",
        re.compile(r"\b(error|exception|traceback|failed|failure|bug|incorrect|wrong|mistake|root cause|retry|revert(ed|ing)?|fix(ed|ing) by)\b", re.I),
        1.5,
    ),
    (
        "handoff",
        "cooperation",
        re.compile(r"\b(hand(ed|ing)? (off|over) to|delegat(ed|ing) to|passing to|requested from|read(ing)? .* (cell|agent)'?s? output)\b", re.I),
        1.5,
    ),
    (
        "health_check",
        "maintenance",
        re.compile(r"\b(health check|heartbeat|watchdog|credit (check|balance)|usage check|sleep(ing)?|waiting for|log rotation|backup)\b", re.I),
        1.2,
    ),
)
_BEHAVIOR_TIE_ORDER = {
    "new_capability": 0,
    "correction": 1,
    "cooperation": 2,
    "polish": 3,
    "maintenance": 4,
    "unknown": 5,
}


def _json_text(value, fallback):
    try:
        return json.dumps(value, sort_keys=True, ensure_ascii=True)
    except (TypeError, ValueError):
        return json.dumps(fallback, sort_keys=True, ensure_ascii=True)


def _compact_text(value, max_chars=700):
    if value in (None, ""):
        return ""
    if isinstance(value, str):
        text = value
    else:
        try:
            text = json.dumps(value, sort_keys=True, ensure_ascii=True)
        except (TypeError, ValueError):
            text = str(value)
    text = " ".join(text.split())
    if len(text) > max_chars:
        return text[: max_chars - 1] + "..."
    return text


def _normalize_behavior_class(value: str) -> str:
    normalized = str(value or "").strip().lower().replace("-", "_").replace(" ", "_")
    aliases = {
        "goal": "new_capability",
        "goal_directed": "new_capability",
        "new": "new_capability",
        "capability": "new_capability",
        "polishing": "polish",
        "self_correction": "correction",
        "handoff": "cooperation",
    }
    normalized = aliases.get(normalized, normalized)
    return normalized if normalized in BEHAVIOR_CLASSES else ""


def _receipt_outcome(task: dict, status: str) -> str:
    raw = str(task.get("outcome") or status or "").strip().lower()
    if not raw:
        return "unknown"
    if any(word in raw for word in ("fail", "error", "exception")):
        return "failure"
    if any(word in raw for word in ("partial", "blocked", "skipped")):
        return "partial"
    if any(word in raw for word in ("success", "ok", "done", "complete")):
        return "success"
    return raw[:80]


def _output_summary(task: dict, decision, output_ref: str) -> str:
    for key in ("output_summary", "summary", "result_summary", "outcome_summary"):
        if task.get(key):
            return _compact_text(task.get(key))
    if isinstance(decision, dict):
        for key in ("output_summary", "summary", "result", "rationale"):
            if decision.get(key):
                return _compact_text(decision.get(key))
    if task.get("artifact_created") and output_ref:
        return _compact_text(f"Artifact created: {task.get('artifact_created')}")
    return ""


def _behavior_source_text(task, status, output_summary, output_ref, tool_calls, decision):
    parts = [
        task.get("type", ""),
        task.get("title", ""),
        task.get("name", ""),
        status,
        output_summary,
        task.get("artifact_created", ""),
        _compact_text(tool_calls, 400),
        _compact_text(decision, 600),
    ]
    if output_ref:
        parts.append(pathlib.Path(str(output_ref)).name)
    return " ".join(str(part) for part in parts if part)


def _classify_behavior(task, status, output_summary, output_ref, tool_calls, decision):
    supplied = _normalize_behavior_class(
        task.get("new_capability_vs_polish") or task.get("behavior_class") or ""
    )
    if supplied:
        return supplied, ["caller_supplied"]

    text = _behavior_source_text(task, status, output_summary, output_ref, tool_calls, decision)
    scores = {name: 0.0 for name in BEHAVIOR_CLASSES}
    hits = []
    if task.get("artifact_created"):
        scores["new_capability"] += 1.0
        hits.append("artifact_created")
    if int(task.get("downstream_task_count", 0) or 0) > 0:
        scores["cooperation"] += 0.8
        hits.append("downstream_task_count")
    for name, behavior_class, pattern, weight in _BEHAVIOR_RULES:
        if pattern.search(text):
            scores[behavior_class] += weight
            hits.append(name)
    winner, score = sorted(
        scores.items(),
        key=lambda item: (-item[1], _BEHAVIOR_TIE_ORDER.get(item[0], 99)),
    )[0]
    if score <= 0:
        return "unknown", []
    return winner, hits


def _db():
    PARKED.mkdir(parents=True, exist_ok=True)
    DB.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB, timeout=30)
    con.execute("PRAGMA journal_mode=WAL")
    con.execute("PRAGMA busy_timeout=30000")
    con.execute(
        """CREATE TABLE IF NOT EXISTS calls(
            ts REAL, lane TEXT, task_id TEXT, task_type TEXT, tier TEXT,
            model TEXT, tokens_in INT, tokens_out INT, cost_usd REAL, status TEXT)"""
    )
    cols = {row[1] for row in con.execute("PRAGMA table_info(calls)").fetchall()}
    for name, ddl in {
        "why_fable": "TEXT DEFAULT ''",
        "artifact_created": "TEXT DEFAULT ''",
        "downstream_task_count": "INT DEFAULT 0",
        "trace_id": "TEXT DEFAULT ''",
        "parent_trace_id": "TEXT DEFAULT ''",
        "duration_ms": "INT DEFAULT 0",
        "receipt_path": "TEXT DEFAULT ''",
        "input_refs_json": "TEXT DEFAULT '[]'",
        "tool_calls_json": "TEXT DEFAULT '[]'",
        "decision_json": "TEXT DEFAULT '{}'",
        "schema_version": "TEXT DEFAULT ''",
        "outcome": "TEXT DEFAULT ''",
        "output_summary": "TEXT DEFAULT ''",
        "tokens_total": "INT DEFAULT 0",
        "behavior_class": "TEXT DEFAULT ''",
        "new_capability_vs_polish": "TEXT DEFAULT ''",
        "behavior_rule_hits_json": "TEXT DEFAULT '[]'",
    }.items():
        if name not in cols:
            con.execute(f"ALTER TABLE calls ADD COLUMN {name} {ddl}")
    con.execute(
        """CREATE TABLE IF NOT EXISTS seen_hashes(
            task_id TEXT, input_hash TEXT, ts REAL,
            PRIMARY KEY (task_id, input_hash))"""
    )
    return con


def _input_hash(task: dict) -> str:
    blob = json.dumps(task.get("input"), sort_keys=True) + task.get("type", "")
    return hashlib.sha256(blob.encode()).hexdigest()[:16]


def _seen_hash_ttl(cfg: dict) -> int:
    defaults = cfg.get("defaults", {})
    return int(defaults.get("seen_hash_ttl_seconds", DEFAULT_SEEN_HASH_TTL_SECONDS))


def _prune_seen_hashes(con, cfg: dict, now: float):
    ttl = _seen_hash_ttl(cfg)
    if ttl <= 0:
        return
    con.execute("DELETE FROM seen_hashes WHERE ts < ?", (now - ttl,))


def _price_for_model(model: str, cfg: dict):
    prices_cfg = cfg.get("prices_per_mtok", {})
    prices = prices_cfg.get(model)
    if prices is not None:
        return prices, ""
    fallback = cfg.get("unknown_model_price_per_mtok")
    if fallback is None and prices_cfg:
        fallback = max(
            prices_cfg.values(),
            key=lambda pair: (float(pair[0]) + float(pair[1])),
        )
    fallback = fallback or DEFAULT_UNKNOWN_PRICE_PER_MTOK
    return fallback, f"unknown model '{model}' priced at punitive fallback {fallback}"


def _budget_day_start(now: float, cfg: dict | None = None) -> float:
    """Return the last configured budget reset boundary.

    Default is UTC midnight. Set defaults.budget_day_start_hour_utc to make the
    reset boundary explicit without changing the existing default. Set
    BRAKES_TZ_OFFSET_HOURS (for example, -8) to reset at midnight for a fixed
    local offset.
    """
    tz_offset = os.environ.get("BRAKES_TZ_OFFSET_HOURS")
    if tz_offset not in (None, ""):
        offset = float(tz_offset) * 3600
        shifted = now + offset
        return shifted - (shifted % 86400) - offset
    defaults = (cfg or {}).get("defaults", {})
    start_hour = int(defaults.get("budget_day_start_hour_utc", 0)) % 24
    offset = start_hour * 3600
    shifted = now - offset
    return shifted - (shifted % 86400) + offset


def spend_today(lane: str, cfg: dict | None = None) -> float:
    con = _db()
    day_start = _budget_day_start(time.time(), cfg)
    row = con.execute(
        "SELECT COALESCE(SUM(cost_usd),0) FROM calls WHERE lane=? AND ts>=?",
        (lane, day_start),
    ).fetchone()
    con.close()
    return float(row[0])


def spend_task(task_id: str) -> float:
    con = _db()
    row = con.execute(
        "SELECT COALESCE(SUM(cost_usd),0) FROM calls WHERE task_id=?",
        (task_id,),
    ).fetchone()
    con.close()
    return float(row[0])


def _budget(lane: str, cfg: dict) -> float:
    b = cfg.get("budgets_usd_daily", {})
    return float(b.get(lane, b.get("default", 1.0)))


def check(task: dict, tier: str, lane: str, cfg: dict, task_path=None):
    """Returns (allowed: bool, tier: str, reason: str). May downgrade tier."""
    if KILLSWITCH.exists():
        return False, tier, "KILLSWITCH present"

    park = PARKED / lane
    if park.exists():
        task_mtime = task_path.stat().st_mtime if task_path else time.time()
        if task_mtime > park.stat().st_mtime:
            park.unlink()  # new work arrived after parking -> wake the lane
        else:
            return False, tier, "lane parked (halt-on-no-work)"

    max_turns = int(task.get("max_turns", cfg.get("defaults", {}).get("max_turns", 5)))
    if int(task.get("turns", 0)) >= max_turns:
        return False, tier, f"max_turns ({max_turns}) reached"

    if tier == "t4" and not (task.get("why_fable") or task.get("why")):
        return False, tier, "t4 requires why_fable or why"

    reason = "ok"
    if tier != "t1":  # budget math only matters for paid tiers
        task_budget = task.get("budget_usd")
        if task_budget is not None:
            spent_task = spend_task(task.get("id", "?"))
            if spent_task >= float(task_budget):
                return False, tier, f"task budget hit (${spent_task:.2f}/${float(task_budget):.2f})"
        spent, budget = spend_today(lane, cfg), _budget(lane, cfg)
        if spent >= budget:
            return False, tier, f"daily budget hit (${spent:.2f}/${budget:.2f})"
        if spent >= 0.8 * budget and tier in TIER_ORDER:
            idx = max(TIER_ORDER.index(tier) - 1, 0)
            tier = TIER_ORDER[idx]
            reason = "80% budget -> downgraded one tier"

    con = _db()
    now = time.time()
    _prune_seen_hashes(con, cfg, now)
    h = _input_hash(task)
    try:
        con.execute(
            "INSERT INTO seen_hashes VALUES (?,?,?)",
            (task.get("id", "?"), h, now),
        )
        con.commit()
    except sqlite3.IntegrityError:
        con.close()
        return False, tier, "loop detected (same task state seen twice)"
    con.close()

    return True, tier, reason


def log(
    lane,
    task,
    tier,
    model,
    tok_in,
    tok_out,
    status,
    cfg,
    duration_ms=0,
    output_ref="",
    tool_calls=None,
    decision=None,
    trace_id="",
    parent_trace_id="",
):
    prices, pricing_warning = _price_for_model(model, cfg)
    price_in, price_out = float(prices[0]), float(prices[1])
    cost = (tok_in / 1e6) * price_in + (tok_out / 1e6) * price_out
    ts = time.time()
    trace_id = str(trace_id or task.get("trace_id") or task.get("correlation_id") or task.get("id", "?"))
    parent_trace_id = str(parent_trace_id or task.get("parent_trace_id") or "")
    input_refs = task.get("input_refs") or task.get("source_refs") or []
    if isinstance(input_refs, str):
        input_refs = [input_refs]
    input_hash = _input_hash(task)
    tool_calls = tool_calls if tool_calls is not None else task.get("tool_calls", [])
    decision = decision if decision is not None else task.get("decision", {})
    input_refs_json = _json_text(input_refs, [])
    tool_calls_json = _json_text(tool_calls, [])
    decision_json = _json_text(decision, {})
    outcome = _receipt_outcome(task, status)
    output_summary = _output_summary(task, decision, output_ref)
    behavior_class, behavior_rule_hits = _classify_behavior(
        task, status, output_summary, output_ref, tool_calls, decision
    )
    behavior_rule_hits_json = _json_text(behavior_rule_hits, [])
    tokens_total = int(tok_in or 0) + int(tok_out or 0)

    RECEIPTS.mkdir(parents=True, exist_ok=True)
    receipt_path = RECEIPTS / f"calls-{time.strftime('%Y%m%d', time.gmtime(ts))}.jsonl"
    receipt = {
        "schema_version": RECEIPT_SCHEMA_VERSION,
        "ts": ts,
        "trace_id": trace_id,
        "parent_trace_id": parent_trace_id,
        "lane": lane,
        "task_id": task.get("id", "?"),
        "task_type": task.get("type", "?"),
        "outcome": outcome,
        "output_summary": output_summary,
        "tokens": {
            "input": int(tok_in or 0),
            "output": int(tok_out or 0),
            "total": tokens_total,
        },
        "new_capability_vs_polish": behavior_class,
        "behavior_class": behavior_class,
        "behavior_rule_hits": behavior_rule_hits,
        "tier": tier,
        "model": model,
        "status": status,
        "tokens_in": tok_in,
        "tokens_out": tok_out,
        "cost_usd": cost,
        "duration_ms": int(duration_ms or 0),
        "why_fable": task.get("why_fable") or task.get("why") or "",
        "artifact_created": task.get("artifact_created", ""),
        "downstream_task_count": int(task.get("downstream_task_count", 0) or 0),
        "input_hash": input_hash,
        "input_refs": input_refs,
        "output_ref": output_ref,
        "tool_calls": tool_calls,
        "decision": decision,
    }
    if pricing_warning:
        receipt["pricing_warning"] = pricing_warning
    with receipt_path.open("a") as f:
        f.write(_json_text(receipt, {"receipt_error": "unserializable"}) + "\n")

    con = _db()
    status_l = str(status).lower()
    if "fail" in status_l or "error" in status_l:
        con.execute(
            "DELETE FROM seen_hashes WHERE task_id=? AND input_hash=?",
            (task.get("id", "?"), input_hash),
        )
    con.execute(
        """INSERT INTO calls(
            ts, lane, task_id, task_type, tier, model, tokens_in, tokens_out,
            cost_usd, status, why_fable, artifact_created, downstream_task_count,
            trace_id, parent_trace_id, duration_ms, receipt_path, input_refs_json,
            tool_calls_json, decision_json, schema_version, outcome, output_summary,
            tokens_total, behavior_class, new_capability_vs_polish, behavior_rule_hits_json
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (ts, lane, task.get("id", "?"), task.get("type", "?"),
         tier, model, tok_in, tok_out, cost, status,
         task.get("why_fable") or task.get("why") or "",
         task.get("artifact_created", ""),
         int(task.get("downstream_task_count", 0) or 0),
         trace_id, parent_trace_id, int(duration_ms or 0), str(receipt_path),
         input_refs_json, tool_calls_json, decision_json,
         RECEIPT_SCHEMA_VERSION, outcome, output_summary, tokens_total,
         behavior_class, behavior_class, behavior_rule_hits_json),
    )
    con.commit()
    con.close()
    return cost, str(receipt_path)


def _atomic_write_text(path: pathlib.Path, text: str):
    tmp = path.with_name(f".{path.name}.{os.getpid()}.{time.time_ns()}.tmp")
    tmp.write_text(text)
    os.replace(tmp, path)


def note_work(lane: str, produced_output: bool):
    """Two consecutive empty outputs -> park the lane (woken by newer task files)."""
    PARKED.mkdir(parents=True, exist_ok=True)
    streak = PARKED / f".streak_{lane}"
    lock = PARKED / f".streak_{lane}.lock"
    with lock.open("w") as lock_file:
        fcntl.flock(lock_file, fcntl.LOCK_EX)
        try:
            if produced_output:
                streak.unlink(missing_ok=True)
                return
            try:
                n = int(streak.read_text().strip() or "0") + 1 if streak.exists() else 1
            except ValueError:
                n = 1
            _atomic_write_text(streak, str(n))
            if n >= 2:
                (PARKED / lane).touch()
                streak.unlink(missing_ok=True)
        finally:
            fcntl.flock(lock_file, fcntl.LOCK_UN)
