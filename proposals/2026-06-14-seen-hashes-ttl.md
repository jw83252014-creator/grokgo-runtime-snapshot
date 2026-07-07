# Proposal: TTL on loop-detection hashes (brakes.py)

**Status:** DRAFT — not applied. Author: Fable (system designer). Date: 2026-06-14.

## Problem
`brakes.py` blocks a task when `(task_id, input_hash)` has been seen before
(seen_hashes PRIMARY KEY → IntegrityError → "loop detected"). The table is
**never pruned**. Consequences:
- A legitimate re-submit of the same task id + same input *tomorrow* is rejected
  forever as a "loop." This contradicts the PLAIN_ENGLISH_MAP claim that "money
  stops do not poison tomorrow's retry" — true for the budget brake, false here.
- The table grows unbounded over the life of `ledger.db`.

The real intent of loop detection is "same task spinning **within a short window**,"
not "this exact state may never recur for all time."

## Fix (small, reversible)
Scope the uniqueness check to a rolling window instead of all-time.

```python
# brakes.py — replace the INSERT-or-IntegrityError block in check()
LOOP_WINDOW = int(cfg.get("loop_window_sec", 3600))  # default 1h
now = time.time()
con.execute("DELETE FROM seen_hashes WHERE ts < ?", (now - LOOP_WINDOW,))
h = _input_hash(task)
recent = con.execute(
    "SELECT 1 FROM seen_hashes WHERE task_id=? AND input_hash=? AND ts>=?",
    (task.get("id", "?"), h, now - LOOP_WINDOW)).fetchone()
if recent:
    con.close()
    return False, tier, "loop detected (same task state within window)"
con.execute("INSERT OR REPLACE INTO seen_hashes VALUES (?,?,?)",
            (task.get("id", "?"), h, now))
con.commit()
```
- `INSERT OR REPLACE` refreshes the ts so an active spin keeps tripping; the
  periodic `DELETE` keeps the table bounded and lets stale states retry.
- New optional knob `loop_window_sec` in routing.yaml (defaults 3600 if absent).

## Risk / blast radius
Low. Only changes *when* a repeat is treated as a loop. Escalation path inside
`process()` is unaffected (it never re-calls `check()` mid-escalation). Add a unit
test: submit same task twice inside window → blocked; advance clock past window →
allowed.

## Why it matters
The killswitch + budget brakes are the hard safety. This one is a *correctness*
brake that currently silently kills valid retries — the worst kind because it
looks like the system "decided" not to work.
