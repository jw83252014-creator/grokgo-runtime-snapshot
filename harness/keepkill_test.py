#!/usr/bin/env python3
"""KEEP/KILL harness for the Grok Go mining lane.

This is the gate before directive rewrites:

  1. prepare  -> write one mining.score.s2 task from anchors.yaml
  2. dispatch -> run ~/grokgo/dispatch.py normally so brakes/ledger apply
  3. report   -> compare outbox receipts to anchor labels and write a report

The harness never calls a model directly. It only creates task files and reads
dispatcher result receipts.
"""
import argparse
import json
import os
import pathlib
import time

import yaml

ROOT = pathlib.Path(os.environ.get("GROKGO_ROOT", str(pathlib.Path.home() / "grokgo")))
ANCHORS = ROOT / "anchors.yaml"
CONFIG = ROOT / "mining_config.yaml"
QUEUE = ROOT / "queue"
INBOX = ROOT / "inbox"
OUTBOX = ROOT / "outbox"
RUNS = ROOT / "harness" / "runs"
REPORTS = ROOT / "harness" / "reports"


def load_anchors(path=ANCHORS):
    data = yaml.safe_load(path.read_text())
    rows = []
    for label, key in (("KEEP", "keeps"), ("KILL", "kills")):
        for idx, item in enumerate(data.get(key, [])):
            rows.append({
                "id": f"{label.lower()}-{idx:02d}",
                "label": label,
                "expected_keep": label == "KEEP",
                "expected_score": item.get("score"),
                "why": item.get("why", ""),
                "text": " ".join(item["text"].split()),
                "embed_prior": None,
            })
    if not rows:
        raise SystemExit(f"no anchors found in {path}")
    return rows


def load_thresholds():
    data = yaml.safe_load(CONFIG.read_text())
    return data.get("thresholds", {"draft_min_total": 8, "adjudicate_min": 5})


def write_task(task, target):
    target.mkdir(parents=True, exist_ok=True)
    path = target / f"{task['id']}.task.json"
    tmp = target / f".{task['id']}.tmp"
    tmp.write_text(json.dumps(task, indent=2))
    os.replace(tmp, path)
    return path


def result_path(task_id):
    candidates = [
        OUTBOX / f"{task_id}.result.json",
        OUTBOX / "consumed" / f"{task_id}.result.json",
    ]
    for path in candidates:
        if path.exists():
            return path
    return None


def read_result(task_id):
    path = result_path(task_id)
    if not path:
        return None
    return json.loads(path.read_text())


def normalize_outputs(result):
    if not result:
        return {}
    output = result.get("output")
    if isinstance(output, dict) and "output" in output:
        output = output["output"]
    if isinstance(output, dict):
        output = [output]
    if not isinstance(output, list):
        return {}
    out = {}
    for row in output:
        if isinstance(row, dict) and row.get("id"):
            out[row["id"]] = row
    return out


def is_keep(row, thresholds):
    try:
        total = float(row.get("total") or 0)
    except (TypeError, ValueError):
        total = 0
    return row.get("route") in ("null", "jeff") and total >= thresholds["draft_min_total"]


def needs_adjudicate(row, thresholds):
    if not row:
        return False
    if is_keep(row, thresholds):
        return False
    try:
        total = float(row.get("total") or 0)
    except (TypeError, ValueError):
        total = 0
    return total >= thresholds["adjudicate_min"] or row.get("confidence") == "borderline"


def cmd_prepare(args):
    rows = load_anchors(args.anchors)
    run_id = args.run_id or time.strftime("keepkill-%Y%m%d-%H%M%S")
    task_id = f"{run_id}-s2"
    task = {
        "id": task_id,
        "type": "mining.score.s2",
        "lane": "mining",
        "turns": 0,
        "input": [
            {"id": row["id"], "text": row["text"], "embed_prior": row["embed_prior"]}
            for row in rows
        ],
    }
    target = INBOX if args.target == "inbox" else QUEUE
    path = write_task(task, target)
    RUNS.mkdir(parents=True, exist_ok=True)
    meta = {
        "run_id": run_id,
        "s2_task": task_id,
        "adjudicate_task": None,
        "target": str(path),
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "anchors": rows,
    }
    (RUNS / f"{run_id}.json").write_text(json.dumps(meta, indent=2))
    print(f"[prepared] {run_id}")
    print(f"[task] {path}")
    print("[next] rtk python3 ~/grokgo/dispatch.py --once")
    print(f"[report] rtk python3 ~/grokgo/harness/keepkill_test.py report {run_id}")


def cmd_report(args):
    meta_path = RUNS / f"{args.run_id}.json"
    if not meta_path.exists():
        raise SystemExit(f"run not found: {meta_path}")
    meta = json.loads(meta_path.read_text())
    thresholds = load_thresholds()
    s2_result = read_result(meta["s2_task"])
    if not s2_result:
        write_pending_report(meta, f"waiting for {meta['s2_task']}.result.json")
        print(f"[pending] no result yet for {meta['s2_task']}")
        return

    s2 = normalize_outputs(s2_result)
    adj = {}
    adj_task = meta.get("adjudicate_task")
    if adj_task:
        adj = normalize_outputs(read_result(adj_task))

    needing_adj = [
        row for row in meta["anchors"]
        if row["id"] in s2 and row["id"] not in adj and needs_adjudicate(s2[row["id"]], thresholds)
    ]
    if needing_adj and not adj_task and not args.no_emit_adjudicate:
        task_id = f"{args.run_id}-adjudicate"
        task = {
            "id": task_id,
            "type": "mining.adjudicate",
            "lane": "mining",
            "turns": 0,
            "input": [
                {
                    "id": row["id"],
                    "text": row["text"],
                    "evidence": s2[row["id"]].get("evidence"),
                    "facets": s2[row["id"]].get("facets"),
                    "total": s2[row["id"]].get("total"),
                }
                for row in needing_adj
            ],
        }
        path = write_task(task, QUEUE)
        meta["adjudicate_task"] = task_id
        meta_path.write_text(json.dumps(meta, indent=2))
        write_pending_report(meta, f"emitted adjudicate task {task_id}: {path}")
        print(f"[adjudicate] {path}")
        print("[next] rtk python3 ~/grokgo/dispatch.py --once")
        return

    if adj_task and not read_result(adj_task):
        write_pending_report(meta, f"waiting for {adj_task}.result.json")
        print(f"[pending] no result yet for {adj_task}")
        return

    report_path, divergences = write_final_report(meta, thresholds, s2, adj)
    print(f"[report] {report_path}")
    print(f"[divergences] {divergences}")


def total_of(row):
    if not row:
        return ""
    total = row.get("total")
    return "" if total is None else str(total)


def route_of(row):
    if not row:
        return "missing"
    return str(row.get("route", "missing"))


def write_pending_report(meta, reason):
    REPORTS.mkdir(parents=True, exist_ok=True)
    path = REPORTS / f"{meta['run_id']}.md"
    path.write_text(
        f"# KEEP/KILL Divergence Report: {meta['run_id']}\n\n"
        f"Status: PENDING\n\n"
        f"Reason: {reason}\n\n"
        f"S2 task: `{meta['s2_task']}`\n\n"
        f"Adjudicate task: `{meta.get('adjudicate_task')}`\n"
    )


def write_final_report(meta, thresholds, s2, adj):
    REPORTS.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# KEEP/KILL Divergence Report: {meta['run_id']}",
        "",
        "Status: COMPLETE",
        "",
        f"S2 task: `{meta['s2_task']}`",
        f"Adjudicate task: `{meta.get('adjudicate_task')}`",
        "",
        "| id | expected | final | s2 route/total | final route/total | directive | note |",
        "|---|---:|---:|---|---|---|---|",
    ]
    divergences = 0
    for row in meta["anchors"]:
        rid = row["id"]
        s2_row = s2.get(rid)
        final = adj.get(rid) or s2_row
        final_keep = is_keep(final or {}, thresholds)
        ok = final_keep == row["expected_keep"]
        if not ok:
            divergences += 1
        directive = "mining.adjudicate" if rid in adj else "mining.score.s2"
        expected = "KEEP" if row["expected_keep"] else "KILL"
        actual = "KEEP" if final_keep else "KILL"
        note = "ok" if ok else "DIVERGED"
        lines.append(
            f"| `{rid}` | {expected} | {actual} | "
            f"{route_of(s2_row)}/{total_of(s2_row)} | "
            f"{route_of(final)}/{total_of(final)} | {directive} | {note} |"
        )
    if divergences:
        lines.extend([
            "",
            "## Failing Directives",
            "",
            "- Start with rows marked `DIVERGED`.",
            "- If the row never reached adjudication, sharpen `mining.score.s2.md` first.",
            "- If adjudication overrode or preserved the wrong call, sharpen `mining.adjudicate.md`.",
        ])
    else:
        lines.extend([
            "",
            "## Failing Directives",
            "",
            "No anchor divergences in this run. Keep directive rewrites scoped to new failures.",
        ])
    path = REPORTS / f"{meta['run_id']}.md"
    path.write_text("\n".join(lines) + "\n")
    return path, divergences


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("prepare", help="write the mining.score.s2 anchor task")
    p.add_argument("--anchors", type=pathlib.Path, default=ANCHORS)
    p.add_argument("--run-id")
    p.add_argument("--target", choices=("queue", "inbox"), default="queue")
    p.set_defaults(func=cmd_prepare)

    r = sub.add_parser("report", help="write/update the divergence report")
    r.add_argument("run_id")
    r.add_argument("--no-emit-adjudicate", action="store_true")
    r.set_defaults(func=cmd_report)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
