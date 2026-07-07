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


def _json_text(value, fallback):
    try:
        return json.dumps(value, sort_keys=True, ensure_ascii=True)
    except (TypeError, ValueError):
        return json.dumps(fallback, sort_keys=True, ensure_ascii=True)


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
    reset boundary explicit without changing the existing default.
    """
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

    RECEIPTS.mkdir(parents=True, exist_ok=True)
    receipt_path = RECEIPTS / f"calls-{time.strftime('%Y%m%d', time.gmtime(ts))}.jsonl"
    receipt = {
        "ts": ts,
        "trace_id": trace_id,
        "parent_trace_id": parent_trace_id,
        "lane": lane,
        "task_id": task.get("id", "?"),
        "task_type": task.get("type", "?"),
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
            tool_calls_json, decision_json
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (ts, lane, task.get("id", "?"), task.get("type", "?"),
         tier, model, tok_in, tok_out, cost, status,
         task.get("why_fable") or task.get("why") or "",
         task.get("artifact_created", ""),
         int(task.get("downstream_task_count", 0) or 0),
         trace_id, parent_trace_id, int(duration_ms or 0), str(receipt_path),
         input_refs_json, tool_calls_json, decision_json),
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
