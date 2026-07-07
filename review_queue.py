#!/usr/bin/env python3
"""Review queue — the human gate, plus the verdict ledger that feeds the trust ramp.

Two handoff modes (pick via REVIEW_MODE env or --mode):
  files     write handoff markdown into $AGENT_BRIDGE_INBOX (default
            $GROKGO_ROOT/bridge_out) so Null's existing Telegram channel presents
            it. Verdicts come back via:  review_queue.py verdict <id> <v>
  telegram  push directly to a Telegram chat with Approve/Edit/Kill buttons.
            REQUIRES A SEPARATE BOT TOKEN from OpenClaw's — two consumers
            long-polling getUpdates on one token = the 409 conflicts you've
            already fought. BotFather, 2 minutes, done.
            env: TELEGRAM_REVIEW_BOT_TOKEN, TELEGRAM_CHAT_ID

Commands:
  review_queue.py push [--mode files|telegram]   send unsent pending items
  review_queue.py poll                           telegram only: collect verdicts
  review_queue.py verdict <id> <approve|edit|kill>
  review_queue.py stats                          trust-ramp readout (14-day window)

Verdict meanings: approve = posted as-is, edit = approved with edits, kill = junk.
Trust ramp (from jeff-filter-spec.md): Null-route may post unattended after 2
consecutive weeks of >=80% approve-without-edit AND <1 kill/day reaching review.
"""
import json
import os
import pathlib
import sqlite3
import sys
import time

import requests

ROOT = pathlib.Path(os.environ.get("GROKGO_ROOT", str(pathlib.Path.home() / "grokgo")))
DB = ROOT / "ledger.db"
PENDING = ROOT / "review" / "pending"
DECIDED = ROOT / "review" / "decided"
BRIDGE = pathlib.Path(os.environ.get("AGENT_BRIDGE_INBOX", str(ROOT / "bridge_out")))
OFFSET = ROOT / "review" / ".tg_offset"
VALID = ("approve", "edit", "kill")


def _db():
    con = sqlite3.connect(DB)
    con.execute("""CREATE TABLE IF NOT EXISTS verdicts(
        item_id TEXT, verdict TEXT, ts REAL)""")
    return con


def _fmt(b):
    ev = "; ".join(b.get("evidence") or [])
    return (f"MINING REVIEW  [{b.get('route')}]  total={b.get('total')}\n"
            f"id: {b['id']}\n\nDRAFT:\n{b['draft'].get('text','')}\n\n"
            f"EVIDENCE: {ev}\nSOURCE: {b.get('source','')}\n\n"
            f"verdict with: review_queue.py verdict {b['id']} approve|edit|kill")


def _tg(method, payload):
    tok = os.environ["TELEGRAM_REVIEW_BOT_TOKEN"]
    r = requests.post(f"https://api.telegram.org/bot{tok}/{method}",
                      json=payload, timeout=60)
    r.raise_for_status()
    return r.json()


def cmd_push(mode):
    PENDING.mkdir(parents=True, exist_ok=True)
    sent = 0
    for p in sorted(PENDING.glob("*.json")):
        b = json.loads(p.read_text())
        if b.get("sent_at"):
            continue
        if mode == "telegram":
            kb = {"inline_keyboard": [[
                {"text": "✅ Approve", "callback_data": f"approve:{b['id']}"},
                {"text": "✏️ Edit", "callback_data": f"edit:{b['id']}"},
                {"text": "❌ Kill", "callback_data": f"kill:{b['id']}"}]]}
            _tg("sendMessage", {"chat_id": os.environ["TELEGRAM_CHAT_ID"],
                                "text": _fmt(b), "reply_markup": kb})
        else:
            BRIDGE.mkdir(parents=True, exist_ok=True)
            (BRIDGE / f"review-{b['id']}.md").write_text(_fmt(b))
        b["sent_at"] = time.time()
        p.write_text(json.dumps(b, indent=2))
        sent += 1
    print(f"[push:{mode}] sent {sent} item(s)")


def cmd_verdict(item_id, verdict):
    if verdict not in VALID:
        sys.exit(f"verdict must be one of {VALID}")
    con = _db()
    con.execute("INSERT INTO verdicts VALUES (?,?,?)", (item_id, verdict, time.time()))
    con.execute("UPDATE mined SET disposition=? WHERE id=?",
                (f"verdict_{verdict}", item_id))
    con.execute("UPDATE items SET stage=? WHERE id=?",
                (f"verdict_{verdict}", item_id))
    con.commit()
    src = PENDING / f"{item_id}.json"
    if src.exists():
        DECIDED.mkdir(parents=True, exist_ok=True)
        os.replace(src, DECIDED / src.name)
    print(f"[verdict] {item_id} -> {verdict}")


def cmd_poll():
    """Telegram long-poll for button presses. Run under launchd/loop."""
    offset = int(OFFSET.read_text()) if OFFSET.exists() else 0
    upd = _tg("getUpdates", {"offset": offset + 1, "timeout": 50,
                             "allowed_updates": ["callback_query"]})
    for u in upd.get("result", []):
        offset = max(offset, u["update_id"])
        cq = u.get("callback_query")
        if not cq:
            continue
        verdict, _, item_id = cq.get("data", "").partition(":")
        if verdict in VALID and item_id:
            cmd_verdict(item_id, verdict)
            _tg("answerCallbackQuery",
                {"callback_query_id": cq["id"], "text": f"{verdict} recorded"})
            try:
                _tg("editMessageText",
                    {"chat_id": cq["message"]["chat"]["id"],
                     "message_id": cq["message"]["message_id"],
                     "text": cq["message"]["text"] + f"\n\n== {verdict.upper()} =="})
            except Exception:
                pass
    OFFSET.parent.mkdir(parents=True, exist_ok=True)
    OFFSET.write_text(str(offset))


def cmd_stats():
    con = _db()
    since = time.time() - 14 * 86400
    rows = con.execute(
        "SELECT verdict, COUNT(*) FROM verdicts WHERE ts>=? GROUP BY verdict",
        (since,)).fetchall()
    d = dict(rows)
    total = sum(d.values())
    if not total:
        print("[stats] no verdicts in 14-day window yet")
        return
    rate = d.get("approve", 0) / total
    junk_per_day = d.get("kill", 0) / 14.0
    print(f"[stats] 14d window  n={total}  {d}")
    print(f"  approve-without-edit rate: {rate:.0%}  (ramp needs >=80%)")
    print(f"  junk reaching review/day:  {junk_per_day:.2f}  (ramp needs <1.0)")
    ok = rate >= 0.8 and junk_per_day < 1.0
    print(f"  trust ramp: {'PASSING — hold for 2 consecutive weeks' if ok else 'not yet'}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "stats"
    if cmd == "push":
        mode = os.environ.get("REVIEW_MODE", "files")
        if "--mode" in sys.argv:
            mode = sys.argv[sys.argv.index("--mode") + 1]
        cmd_push(mode)
    elif cmd == "poll":
        cmd_poll()
    elif cmd == "verdict":
        cmd_verdict(sys.argv[2], sys.argv[3])
    else:
        cmd_stats()
