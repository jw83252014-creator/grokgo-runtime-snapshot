#!/usr/bin/env python3
"""Shared task-board and Agent Bridge dispatch helper."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import pathlib
import re
import sys
import urllib.error
import urllib.request
from typing import Any


HOME = pathlib.Path.home()
DEFAULT_BOARD = HOME / "grokgo" / "TASK_BOARD.md"
DEFAULT_BACKLOG = HOME / "grokgo" / "proposals" / "master-backlog.md"
DEFAULT_API = "http://127.0.0.1:8787/api/say"
OWNER_RE = re.compile(r"owner\s+([^.;\n]+)", re.I)
DASH_OWNER_RE = re.compile(r"[—-]\s*owner\s+([^.;\n]+)", re.I)
STATUS_MAP = {"☐": "open", "◐": "in_progress", "☑": "done", "⛔": "blocked"}


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def clean_cell(value: Any) -> str:
    text = " ".join(str(value or "").split())
    return text.replace("|", "/")


def task_id(owner: str, task: str) -> str:
    digest = hashlib.sha256(f"{owner}:{task}".lower().encode("utf-8")).hexdigest()[:8]
    return f"tb-{digest}"


def lane_for(owner: str) -> str:
    low = owner.lower()
    if any(x in low for x in ("grok", "scout", "castor", "nova", "librarian")):
        return "browser-research"
    if any(x in low for x in ("vega", "creative")):
        return "creative"
    if any(x in low for x in ("altair", "security")):
        return "security"
    if any(x in low for x in ("jeff", "approval")):
        return "approval"
    if any(x in low for x in ("codex", "keystone", "fable", "hermes")):
        return "terminal-build"
    return "ops"


def parse_owner(text: str) -> str:
    matches = list(DASH_OWNER_RE.finditer(text)) or list(OWNER_RE.finditer(text))
    if not matches:
        return "unassigned"
    match = matches[-1]
    owner = match.group(1)
    owner = re.sub(r"\([^)]*$", "", owner)
    owner = re.sub(r"\([^)]*\)", "", owner)
    owner = re.split(r"[,/+]|\band\b|\bto\b", owner, maxsplit=1, flags=re.I)[0]
    return clean_cell(owner).strip("* -–—>") or "unassigned"


def parse_backlog(backlog: pathlib.Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    section = ""
    for raw in backlog.read_text(encoding="utf-8").splitlines():
        if raw.startswith("## "):
            section = clean_cell(raw.lstrip("# "))
            continue
        stripped = raw.strip()
        if not stripped.startswith("- "):
            continue
        body = stripped[2:].strip()
        status = "open"
        for mark, mapped in STATUS_MAP.items():
            if body.startswith(mark):
                status = mapped
                body = body[len(mark):].strip()
                break
        if "owner" not in body.lower():
            continue
        owner = parse_owner(body)
        task = re.sub(r"\s+—\s+owner\s+.*$", "", body, flags=re.I).strip()
        gate = "draft-only; Jeff approves public posts/spend/account changes"
        rows.append(
            {
                "id": task_id(owner, task),
                "status": status,
                "owner": owner,
                "lane": lane_for(owner),
                "source": str(backlog),
                "task": task,
                "gate": gate,
                "receipt": "pending",
                "updated": now(),
                "section": section,
            }
        )
    return rows


def board_header() -> str:
    return (
        "# Shared Task Board\n\n"
        "Single source of truth for gated lane work pulled from the master backlog.\n"
        "Rows are draft-only until Jeff approves any public post, spend, account/billing change, or irreversible action.\n\n"
        "| id | status | owner | lane | source | task | gate | receipt | updated |\n"
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
    )


def row_to_md(row: dict[str, str]) -> str:
    cells = [row.get(k, "") for k in ("id", "status", "owner", "lane", "source", "task", "gate", "receipt", "updated")]
    return "| " + " | ".join(clean_cell(c) for c in cells) + " |"


def write_board(board: pathlib.Path, rows: list[dict[str, str]]) -> None:
    board.parent.mkdir(parents=True, exist_ok=True)
    text = board_header() + "\n".join(row_to_md(row) for row in rows) + "\n"
    tmp = board.with_name(f".{board.name}.tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(board)


def append_row(board: pathlib.Path, row: dict[str, str]) -> None:
    if not board.exists():
        write_board(board, [])
    with board.open("a", encoding="utf-8") as f:
        f.write(row_to_md(row) + "\n")


def post_to_bridge(agent: str, message: str, api: str) -> dict[str, Any]:
    payload = json.dumps({"agent": agent, "message": message}).encode("utf-8")
    request = urllib.request.Request(api, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        raise RuntimeError(f"bridge post failed: {exc}") from exc


def cmd_seed(args: argparse.Namespace) -> int:
    rows = parse_backlog(args.backlog)
    write_board(args.board, rows)
    print(json.dumps({"board": str(args.board), "rows": len(rows)}, sort_keys=True))
    return 0


def cmd_add(args: argparse.Namespace) -> int:
    row = {
        "id": args.id or task_id(args.owner, args.task),
        "status": args.status,
        "owner": args.owner,
        "lane": args.lane or lane_for(args.owner),
        "source": args.source,
        "task": args.task,
        "gate": args.gate,
        "receipt": args.receipt,
        "updated": now(),
    }
    append_row(args.board, row)
    print(json.dumps({"board": str(args.board), "id": row["id"]}, sort_keys=True))
    return 0


def cmd_dispatch(args: argparse.Namespace) -> int:
    payload = {"agent": args.agent, "message": args.message}
    if not args.post:
        print(json.dumps({"dry_run": True, "api": args.api, "payload": payload}, sort_keys=True))
        return 0
    result = post_to_bridge(args.agent, args.message, args.api)
    print(json.dumps({"dry_run": False, "result": result}, sort_keys=True))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Seed task board and dispatch gated Agent Bridge tasks")
    sub = parser.add_subparsers(dest="cmd", required=True)

    seed = sub.add_parser("seed", help="seed board from master backlog owner rows")
    seed.add_argument("--backlog", type=pathlib.Path, default=DEFAULT_BACKLOG)
    seed.add_argument("--board", type=pathlib.Path, default=DEFAULT_BOARD)
    seed.set_defaults(func=cmd_seed)

    add = sub.add_parser("add", help="append one local task-board row")
    add.add_argument("--board", type=pathlib.Path, default=DEFAULT_BOARD)
    add.add_argument("--id")
    add.add_argument("--status", default="open")
    add.add_argument("--owner", required=True)
    add.add_argument("--lane")
    add.add_argument("--source", required=True)
    add.add_argument("--task", required=True)
    add.add_argument("--gate", default="draft-only; Jeff approval required for public/spend/account changes")
    add.add_argument("--receipt", default="pending")
    add.set_defaults(func=cmd_add)

    dispatch = sub.add_parser("dispatch", help="prepare or post one /api/say message")
    dispatch.add_argument("--agent", required=True)
    dispatch.add_argument("--message", required=True)
    dispatch.add_argument("--api", default=DEFAULT_API)
    dispatch.add_argument("--post", action="store_true")
    dispatch.set_defaults(func=cmd_dispatch)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
