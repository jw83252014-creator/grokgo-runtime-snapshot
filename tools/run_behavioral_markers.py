#!/usr/bin/env python3
"""Run behavioral marker scoring over a JSONL log.

Default target is the Grok unified log. The marker computer writes a daily
JSONL time series under state_dir/markers and this runner can also write a
single summary JSON file for handoff/reporting.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from behavioral_markers import BehavioralMarkerComputer, LogIngestor


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LOG = Path.home() / ".grok" / "logs" / "unified.jsonl"
DEFAULT_STATE = ROOT / "researcher_state"


def _read_anchor_texts() -> list[str]:
    anchors = []
    for rel in (
        "CLAUDE.md",
        "directives/watcher.emergence.md",
        "directives/mining.score.s2.md",
        "directives/mining.adjudicate.md",
    ):
        path = ROOT / rel
        if path.exists():
            anchors.append(path.read_text(errors="replace")[:6000])
    return anchors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", default=str(DEFAULT_LOG), help="JSONL log path")
    parser.add_argument("--state-dir", default=str(DEFAULT_STATE), help="marker state directory")
    parser.add_argument("--max-entries", type=int, default=100_000)
    parser.add_argument("--incremental", action="store_true", help="read only new entries and update offset")
    parser.add_argument("--external-fitness-delta", type=float, default=0.0)
    parser.add_argument("--output", help="optional summary JSON output path")
    args = parser.parse_args()

    ingestor = LogIngestor(args.log, offset_dir=args.state_dir)
    entries = (
        ingestor.read_new(max_entries=args.max_entries)
        if args.incremental
        else ingestor.read_all(max_entries=args.max_entries)
    )
    computer = BehavioralMarkerComputer(
        state_dir=args.state_dir,
        coherence_anchor_texts=_read_anchor_texts(),
    )
    markers = computer.compute_markers(entries, external_fitness_delta=args.external_fitness_delta)
    result = {
        "log_path": str(Path(args.log).expanduser()),
        "state_dir": str(Path(args.state_dir).expanduser()),
        "mode": "incremental" if args.incremental else "read_all",
        "malformed_count": ingestor.malformed_count,
        "markers": markers,
    }
    text = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        out = Path(args.output).expanduser()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
