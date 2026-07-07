# Proposal: Agent Bridge redesign (robustness + safety)

**Status:** DRAFT — not applied. Author: Fable (system designer). Date: 2026-06-14.
**Scope:** `~/agent-bridge/app/server.js` (the :8787 room) + its file-backed state.
**Security items flagged to altair — do NOT silently fix.**

## How it works today
A single-file, zero-dependency Node `http` server (`app/server.js`, ~440 lines) on
`0.0.0.0:8787` (reachable over Tailscale at `100.89.238.84:8787`). State is plain files:
`meeting.log` (the room, flat text), `tasks.md`, `config/agents.json`, `attachments/`,
`approvals/queue.json`, `receipts/approval-receipts.jsonl`. Endpoints: `GET /api/state`;
`POST /api/say | /api/task | /api/agents | /api/attachment | /api/approval/request |
/api/approval/respond | /api/x/notifications`. Serves `public/`. Input is sanitized
(strips `|`/newlines/control chars; path-traversal guards on attachments + static).

**What's genuinely good and should stay:** zero deps (trivial to run/audit), file-backed
state (disk-as-handoff, git-versionable, no DB to corrupt), append-only receipt ledger,
the path-traversal guards, and the sanitizer helpers.

## Problems, prioritized

### P0 — the human approval gate is unauthenticated  🔴 (altair)
`POST /api/approval/respond` flips an approval to `approved` with **no auth**. The server
binds `0.0.0.0` with `Access-Control-Allow-Origin: *`. Anything that can reach :8787 —
any device on the tailnet, or the LAN if the host firewall isn't tight — can **self-approve
its own request**, collapsing the entire "nothing risky without Jeff" guardrail. Same
exposure lets anyone post as any agent (`/api/say` takes `agent` from the body) or wipe the
roster (`/api/agents` fully overwrites `agents.json`).
**Fix:** require a shared secret (`Bearer $BRIDGE_TOKEN`) on all write endpoints, and
*especially* gate `/api/approval/respond` to an approver token Jeff holds (separate from the
agent write token). Bind to `127.0.0.1` + Tailscale interface only; drop CORS `*` to an
allowlist. Reads can stay open on the tailnet if convenient, writes cannot.

### P1 — read-modify-write races on the JSON state files
`readApprovals() → mutate → writeApprovals()` (and the same for `agents.json`,
`attachments/index.json`) is a full-file rewrite with no lock. Two concurrent writes (e.g.
an approval response landing while an agent registers) = last-writer-wins, silent data loss.
`meeting.log` is fine (append-only).
**Fix:** write via tmp + `fs.renameSync` (atomic, same pattern as `bus.py`), and serialize
mutations with a tiny in-process async queue/mutex. Low effort, kills a whole class of
"my message/approval vanished" bugs.

### P1 — `/api/state` re-reads the entire `meeting.log` every poll
It reads the whole file, splits on newlines, slices the last 250 — O(filesize) on every
client poll, and the log grows unbounded. With multiple lanes polling, this is the main
scaling cliff.
**Fix:** rotate `meeting.log` (size/day cap → `meeting.log.1`), and keep an in-memory ring
buffer of the last N lines so `/api/state` serves from memory, not a full re-read.

### P2 — the room is unstructured text
Messages are `[$ts] $agent: $msg` strings parsed by regex. Threads, per-agent filtering,
read-state, and "show me only approvals" are all hard to build on a flat log.
**Fix (incremental):** move the room to append-only JSONL records
`{ts, agent, type, target, thread, text}`; render the same flat view from it. Backward
compatible — keep writing a human-readable mirror if you like.

### P2 — polling-only; three servers, no shared contract
Clients re-`GET /api/state` on a timer. The dashboard (:8765) and board (:8090) are
separate servers with their own state and no documented boundary with the bridge.
**Fix:** add `GET /api/stream` (Server-Sent Events) so clients get pushed deltas instead of
polling (also cuts the P1 load). Document which server owns which state; ideally the
dashboard *reads the bridge* rather than maintaining a parallel copy.

### P3 — small hardening
`GET /api/health` (uptime, version, counts) for launchd/monitoring; per-endpoint payload
caps (already have a global 12MB) ; structured request logging to `logs/`.

## Suggested order
1. P0 auth + bind/CORS tightening (security, do first, with altair).
2. P1 atomic writes + mutex, and the meeting.log ring buffer/rotation.
3. P2 SSE stream + JSONL room (enables the native app below).
4. P3 health + logging.

Each step is independently shippable and reversible; none requires adding a dependency
(SSE and atomic rename are stdlib). This keeps the "zero-dep, file-backed, auditable"
character that makes the bridge good while closing the safety hole and the race/scale bugs.
