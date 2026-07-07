#!/usr/bin/env python3
"""grokgo dispatcher.

Pops *.task.json from queue/, routes by routing.yaml, enforces brakes,
calls the model (Ollama for t1, Anthropic API for t2-t4 with prompt caching
on the stable directive prefix), validates strict-JSON output, escalates
ONE tier on schema failure, logs every call to the ledger.

Usage:
  python3 dispatch.py --once             # process one task
  python3 dispatch.py --loop             # run forever; idle = sleep, never a model call
  python3 dispatch.py --once --dry-run   # full routing + brakes + ledger, no model calls

Task file shape (written by any cell/agent onto the bus):
  {"id":"t-001","type":"harvest.triage","lane":"mining","turns":0,"input":[...]}
Result lands in outbox/<id>.result.json; task file moves to done/ or failed/.
"""
import argparse
import json
import os
import pathlib
import sys
import time
import uuid

import requests
import yaml

import brakes

ROOT = pathlib.Path(os.environ.get("GROKGO_ROOT", str(pathlib.Path.home() / "grokgo")))
QUEUE, DONE, FAIL, OUTBOX = ROOT / "queue", ROOT / "done", ROOT / "failed", ROOT / "outbox"
DIRECTIVES = ROOT / "directives"
TIER_ORDER = ["t1", "t2", "t3", "t4"]
ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"
# t1 local server base URL (OpenAI-compatible). Override in routing.yaml: local.base_url
LOCAL_BASE = os.environ.get("LOCAL_BASE_URL", "http://127.0.0.1:8000/v1")


def cfg():
    return yaml.safe_load((ROOT / "routing.yaml").read_text())


def route_for(task, c):
    r = dict(c.get("defaults", {}))
    r.update(c.get("routes", {}).get(task.get("type", ""), {}))
    return r


def directive_for(task_type):
    p = DIRECTIVES / f"{task_type}.md"
    if not p.exists():
        p = DIRECTIVES / "default.md"
    return p.read_text()


def call_anthropic(model, directive, payload, max_tokens):
    body = {
        "model": model,
        "max_tokens": max_tokens,
        # Stable prefix FIRST with cache_control -> ~90% off cached input reads.
        # Volatile task payload stays in the user turn only.
        "system": [{"type": "text", "text": directive,
                    "cache_control": {"type": "ephemeral"}}],
        "messages": [{"role": "user", "content": payload}],
    }
    r = requests.post(
        ANTHROPIC_URL,
        headers={"x-api-key": os.environ["ANTHROPIC_API_KEY"],
                 "anthropic-version": "2023-06-01",
                 "content-type": "application/json"},
        json=body, timeout=180)
    r.raise_for_status()
    d = r.json()
    text = "".join(b.get("text", "") for b in d.get("content", []))
    u = d.get("usage", {})
    return text, u.get("input_tokens", 0), u.get("output_tokens", 0)


def call_local(model, directive, payload, max_tokens, base_url):
    """t1 via an OpenAI-compatible local server (rapid-mlx, mlx-openai-server,
    LM Studio, vllm-mlx, etc.). Tries OpenAI JSON mode; if the server rejects
    response_format (some local servers 400 on it), retries without it — the
    directives already mandate JSON and dispatch validates + escalates anyway.
    Returns real prompt/completion token counts (cost stays $0 for local)."""
    base = {"model": model, "max_tokens": max_tokens, "temperature": 0,
            "messages": [{"role": "system", "content": directive},
                         {"role": "user", "content": payload}]}
    url = base_url.rstrip("/") + "/chat/completions"
    import os as _os
    _hdr = {}
    _k = _os.environ.get("LOCAL_API_KEY")
    if _k:
        _hdr["Authorization"] = "Bearer " + _k
    r = requests.post(url, json={**base, "response_format": {"type": "json_object"}},
                      headers=_hdr, timeout=600)
    if r.status_code == 400:
        r = requests.post(url, json=base, headers=_hdr, timeout=600)
    r.raise_for_status()
    d = r.json()
    text = d["choices"][0]["message"]["content"]
    u = d.get("usage", {})
    return text, u.get("prompt_tokens", 0), u.get("completion_tokens", 0)


def is_empty(out):
    return out in ([], {}, None) or out == {"action": "none"}


def _compact_text(value, max_chars=700):
    if value in (None, ""):
        return ""
    if isinstance(value, str):
        text = value
    else:
        try:
            text = json.dumps(value, sort_keys=True)
        except (TypeError, ValueError):
            text = str(value)
    text = " ".join(text.split())
    if len(text) > max_chars:
        return text[: max_chars - 1] + "..."
    return text


def summarize_output(out, raw_text=""):
    """Create the receipt summary that behavioral markers can classify.

    This is deliberately deterministic and cheap. Rich cells should still
    return their own `output_summary`; this is the dispatch fallback when they
    do not.
    """
    if out is None:
        return "Model response failed JSON schema validation."
    if isinstance(out, dict):
        for key in (
            "output_summary",
            "summary",
            "result_summary",
            "recommendation",
            "verdict",
            "action",
            "status",
        ):
            if out.get(key) not in (None, "", [], {}):
                return _compact_text(out.get(key))
        keys = ", ".join(sorted(out.keys()))
        return f"Valid JSON output with keys: {keys}" if keys else "Valid empty JSON output."
    if isinstance(out, list):
        return f"Valid JSON list output with {len(out)} item(s)."
    return _compact_text(out if out is not None else raw_text)


def ensure_trace(task):
    trace_id = task.get("trace_id") or task.get("correlation_id") or uuid.uuid4().hex
    task["trace_id"] = str(trace_id)
    task["parent_trace_id"] = str(task.get("parent_trace_id") or "")
    return task


def process(task_path: pathlib.Path, dry=False):
    c = cfg()
    task = ensure_trace(json.loads(task_path.read_text()))
    lane = task.get("lane", "default")
    r = route_for(task, c)
    tier = r["tier"]

    if tier == "t0":
        task_path.rename(FAIL / task_path.name)
        print(f"[t0] {task['id']}: t0 types are handled by scripts, not the dispatcher")
        return

    ok, tier, reason = brakes.check(task, tier, lane, c, task_path)
    if not ok:
        task_path.rename(FAIL / task_path.name)
        print(f"[brake] {task['id']}: {reason}")
        return
    if reason != "ok":
        print(f"[brake] {task['id']}: {reason}")

    directive = directive_for(task.get("type", ""))
    payload = json.dumps(task.get("input"))
    max_tok = int(r.get("max_output_tokens", 1024))

    while True:
        model = c["models"][tier]
        started = time.time()
        if dry:
            text, tin, tout = json.dumps({"dry_run": True, "routed_tier": tier,
                                          "routed_model": model}), 0, 0
        elif tier == "t1":
            base_url = c.get("local", {}).get("base_url", LOCAL_BASE)
            text, tin, tout = call_local(model, directive, payload, max_tok, base_url)
        else:
            text, tin, tout = call_anthropic(model, directive, payload, max_tok)

        try:
            out = json.loads(text)
        except Exception:
            out = None

        status = "ok" if out is not None else "schema_fail"
        output_ref = f"outbox/{task['id']}.result.json" if out is not None else ""
        decision = {
            "output_keys": sorted(out.keys()) if isinstance(out, dict) else [],
            "empty_output": is_empty(out),
            "output_summary": summarize_output(out, text),
        }
        receipt_task = dict(task)
        receipt_task.setdefault("output_summary", decision["output_summary"])
        cost, receipt_path = brakes.log(
            lane, receipt_task, tier, model, tin, tout, status, c,
            duration_ms=int((time.time() - started) * 1000),
            output_ref=output_ref,
            decision=decision,
        )

        if out is not None:
            (OUTBOX / f"{task['id']}.result.json").write_text(
                json.dumps({"task": task["id"], "type": task.get("type"),
                            "tier": tier, "model": model, "cost_usd": round(cost, 6),
                            "trace_id": task["trace_id"],
                            "parent_trace_id": task["parent_trace_id"],
                            "receipt_path": receipt_path,
                            "output": out}, indent=2))
            task_path.rename(DONE / task_path.name)
            brakes.note_work(lane, not is_empty(out))
            print(f"[done] {task['id']} via {tier}/{model} (${cost:.4f})")
            return

        # Escalate exactly ONE tier per failure; never jump straight to t4.
        if r.get("escalate_on_fail") and tier != "t4":
            tier = TIER_ORDER[TIER_ORDER.index(tier) + 1]
            print(f"[escalate] {task['id']} schema_fail -> {tier}")
            continue
        task_path.rename(FAIL / task_path.name)
        print(f"[fail] {task['id']}: unrecoverable schema failure at {tier}")
        return


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--loop", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    for d in (QUEUE, DONE, FAIL, OUTBOX):
        d.mkdir(parents=True, exist_ok=True)

    while True:
        if brakes.KILLSWITCH.exists():
            print("[killswitch] halting")
            sys.exit(0)
        tasks = sorted(QUEUE.glob("*.task.json"))
        if tasks:
            try:
                process(tasks[0], dry=args.dry_run)
            except Exception as e:
                # one failing task must not kill the loop — park it in FAIL and continue
                print(f"[dispatch] task {tasks[0].name} failed: {e}")
                try: tasks[0].rename(FAIL / tasks[0].name)
                except Exception: pass
            if args.once:
                return
        elif args.loop:
            time.sleep(5)  # idle costs nothing — no heartbeat ever calls a model
        else:
            print("[idle] queue empty")
            return


if __name__ == "__main__":
    main()
