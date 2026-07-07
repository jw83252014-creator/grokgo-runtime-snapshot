"""grokgo bus adapter — how existing cells talk to the loop.

Any cell integrates in ~3 lines:

    import bus
    tid = bus.submit("mining.score.s1", items, lane="mining")
    result = bus.wait(tid)          # or fire-and-forget and let `advance` handle it

Writes are atomic (tmp + os.replace) so the watcher never enqueues a
partially-written task file. Results are consumed from outbox/ and moved to
outbox/consumed/ so nothing is processed twice.
"""
import json
import os
import pathlib
import time
import uuid

ROOT = pathlib.Path(os.environ.get("GROKGO_ROOT", str(pathlib.Path.home() / "grokgo")))
INBOX, OUTBOX = ROOT / "inbox", ROOT / "outbox"
CONSUMED = OUTBOX / "consumed"


def submit(task_type, input_obj, lane="default", task_id=None, turns=0):
    task_id = task_id or f"{task_type.replace('.', '-')}-{uuid.uuid4().hex[:8]}"
    task = {"id": task_id, "type": task_type, "lane": lane,
            "turns": turns, "input": input_obj}
    INBOX.mkdir(parents=True, exist_ok=True)
    tmp = INBOX / f".{task_id}.tmp"
    tmp.write_text(json.dumps(task, indent=2))
    os.replace(tmp, INBOX / f"{task_id}.task.json")  # atomic
    return task_id


def wait(task_id, timeout=600, poll=2.0):
    deadline = time.time() + timeout
    p = OUTBOX / f"{task_id}.result.json"
    while time.time() < deadline:
        if p.exists():
            return json.loads(p.read_text())
        time.sleep(poll)
    raise TimeoutError(f"no result for {task_id} within {timeout}s")


def submit_and_wait(task_type, input_obj, lane="default", timeout=600) -> dict:
    return wait(submit(task_type, input_obj, lane), timeout=timeout)


def results(type_prefixes=None, consume=False):
    """Yield result dicts from outbox/. If consume, move them to outbox/consumed/
    so they are processed exactly once. Results not matching type_prefixes are
    left untouched for other consumers."""
    CONSUMED.mkdir(parents=True, exist_ok=True)
    for p in sorted(OUTBOX.glob("*.result.json")):
        try:
            res = json.loads(p.read_text())
        except Exception:
            continue
        t = res.get("type", "")
        if type_prefixes and not any(t.startswith(x) for x in type_prefixes):
            continue
        yield res
        if consume:
            os.replace(p, CONSUMED / p.name)
