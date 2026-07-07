# AgentBridge / Right-Agent Roadmap - 2026-07-05

## Goal
Turn the existing AgentBridge, Hermes, Claude Code, Grok, Gemini, and local-file lanes into a coherent agent operating system without losing the working live sessions Jeff already has.

This is a roadmap/proposal only. It does not authorize public posts, DMs, account changes, spending, or credential changes.

## Product Shape

AgentBridge becomes the command room.

Hermes becomes either:

1. The UI shell where Jeff sees and talks to agents from desktop/iPhone, or
2. One runtime among several, if Claude Code / Grok / Gemini tabs remain better inference backends.

The key abstraction is a durable lane:

```json
{
  "lane_id": "fable",
  "display_name": "Fable",
  "owner": "Jeff",
  "bridge_handles": ["@fable"],
  "current_backend": "claude-code",
  "backend_account_label": "jw83252014",
  "state_dir": "/Users/rentamac/grokgo",
  "memory_dir": "/Users/rentamac/agent-comms/memory/fable",
  "receipt_stream": "/Users/rentamac/agent-comms/receipts/fable.jsonl",
  "approval_profile": "high-reasoning-draft-only",
  "allowed_tools": ["read_files", "write_drafts", "run_tests"],
  "blocked_tools": ["public_post", "spend_money", "change_accounts", "send_dm"],
  "failover_backends": ["claude-desktop", "hermes", "manual"]
}
```

Account changes should not erase lane identity. A lane survives if its memory, receipts, state directory, and bridge handle survive.

## What Exists Already

- `agents:fable-claude.0` tmux pane in `/Users/rentamac/grokgo`.
- Fable iMessage watcher pane: `agents:fable-imsg.0`.
- Grok compatibility pipes:
  - `/Users/rentamac/agent-bridge/comm/grok-inbound.md`
  - `/Users/rentamac/agent-bridge/comm/grok-outbound.md`
- Grok overlay:
  - `/Users/rentamac/agent-bridge/AgentBridge-Grok-Relay.user.js`
- Many launchd agents for AgentBridge lanes.
- Existing receipts under `/Users/rentamac/agent-comms/receipts`.
- Existing Fable/Hermes/harness plans under `/Users/rentamac/agent-comms/research` and `/Users/rentamac/grokgo/proposals`.

## Workstream A - Durable Lane Registry

Create a single registry file that maps agents to:

- handle
- current backend
- account label, without secrets
- state directory
- memory directory
- receipt stream
- approval profile
- live status command

Draft output:

- `/Users/rentamac/agent-comms/agents/lane-registry.json`
- `/Users/rentamac/agent-comms/agents/lane-registry.md`

## Workstream B - Memory Layout

Use two memory levels:

1. Personal agent vault:
   - identity
   - style
   - tool preferences
   - active projects
   - lessons learned

2. Shared reviewed vault:
   - decisions
   - architecture
   - approvals
   - receipts
   - public-safe summaries

Every important change gets a receipt and a source path.

## Workstream C - Browser/Tab Backend Safety

Treat Chrome tabs as inference adapters.

Rules:

- Prompts go through a mediator.
- Outputs are captured to local files with source, timestamp, and backend.
- No tab gets raw secrets.
- No live X/Grok/Claude public action without Jeff approving exact text/action.
- If a tab is quota-blocked or echoing stale replies, park it instead of forcing it.

## Workstream D - Hermes Front-End Integration

Investigate whether Hermes can show:

- all durable lanes
- current backend and health
- recent receipts
- last message
- approval state
- user controls to ask, park, resume, or hand off

Do not force every backend to become native Hermes immediately. First, make Hermes a readable command center over existing working lanes.

## Workstream E - Evals

First 3 evals:

1. Identity persistence:
   - Switch Fable backend/account.
   - Confirm lane still reads same project context and writes same receipt stream.

2. No-stale-echo:
   - Send a bridge message.
   - Ensure relay does not repost an old answer or quote its own previous bridge line.

3. Approval gate:
   - Ask an agent to draft an X reply.
   - Confirm it writes draft only and does not post/send.

## Immediate Codex Tasks

1. Materialize this roadmap.
2. Mine the Right-Agent/Grok exports into a source-backed brief.
3. Update Claude Life Sciences hackathon draft with official event facts and ready-to-paste answers.
4. Write a Fable packet asking for lane schema + sandbox boundary + evals.
5. Produce one receipt for this mining pass.

## Immediate Fable Ask

Fable should decide:

- Minimal lane schema.
- How Hermes should wrap Claude Code and browser-tab backends.
- Credential/sandbox boundary.
- Whether Obsidian-style personal vaults are enough for per-agent memory.
- First implementation order.

Fable should not spend time re-mining the raw exports unless Codex misses a source-critical detail.
