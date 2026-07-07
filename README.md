# GrokGo Runtime Snapshot

Public, redacted snapshot of the private `grokgo` runtime repo.

This is the version intended for Fable and other reviewers to understand how
Grok Go has actually been running without exposing local account/session state,
raw logs, SQLite ledgers, or private cache material.

## What This Shows

- `bus.py`, `dispatch.py`, `brakes.py`, `routing.yaml`, `mining_pipeline.py`:
  the core filesystem bus, dispatcher, budget brakes, tier routing, and mining
  loop.
- `directives/`: the operating genome loaded by cells and reviewer lanes.
- `TASK_BOARD.md` and `LANE-MAP-2026-07-02.md`: the current lane/task map.
- `harness/`: Keep/Kill test harness and one preserved report/run.
- `done/`, `failed/`, `outbox/`: small task/result examples showing the
  dispatch shape.
- `proposals/`: architecture, Fable harness, memory, X Radar, bridge, voice,
  and business planning documents.
- `Scientific-Research-Notes/` and `knowledge-base/`: public-facing knowledge
  base structure for science/X intelligence work.
- `prompt-lab/prompts/`: locally authored or distilled prompts used to shape
  Fable/Codex/Grok style lanes, excluding third-party/reference dumps.

## What Was Excluded

See `PRIVATE_EXCLUSIONS.md`.

Short version: raw `.claude` state, local logs, SQLite ledgers, nested repo
spikes, private Grok tab memory, account inventories, and secret-shaped files
are intentionally not included.

## How To Read This

Start here:

1. `LANE-MAP-2026-07-02.md`
2. `TASK_BOARD.md`
3. `routing.yaml`
4. `brakes.py`
5. `dispatch.py`
6. `directives/default.md`
7. `directives/fable.review.routing.md`
8. `proposals/2026-07-01-fable-5-practical-harness.md`
9. `proposals/2026-07-05-grok-chat-mining.md`
10. `proposals/fable-token-savings-master-packet-2026-07-05.md`

## Safety Boundaries

This repo is draft/read/review oriented.

No public posts, DMs, spends, account changes, trades, repo pushes, or other
irreversible actions should happen from this snapshot without Jeff explicitly
approving the exact action.

## Relationship To Other Repos

- `grok-go-organism`: polished/shareable organism package.
- `grok-go-hackathon`: hackathon submission package.
- `mining-engine`: public corpus-mining and Jeff Filter work.
- `grokgo`: private live runtime repo with logs/state.
- `grokgo-runtime-snapshot`: this public, redacted operating snapshot.
