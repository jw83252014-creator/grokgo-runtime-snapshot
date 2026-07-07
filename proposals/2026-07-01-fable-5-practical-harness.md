# Proposal: Fable 5 Practical Harness For Grok Go

Date: 2026-07-01
Status: ready for review

## Problem

Grok Go can waste expensive Fable turns when the message bus routes glue work, polling, summaries, or repeated context setup to Fable. Current public usage patterns around Fable 5 also suggest fallback/refusal/wall behavior can be triggered by weak context hygiene, vague prompts, long loops, and missing stop conditions.

There is a second cost leak: every lane re-learns project history when memory is trapped inside browser tabs, chat exports, or one agent's session. Conare's public docs describe a shared MCP memory layer for Claude Code, Cursor, Codex, and related agents; Grok Go should implement the same architecture locally first.

There is a third reliability leak: if agent work has no receipt, the dashboard cannot prove what happened. Every meaningful model/tool attempt needs a traceable audit row with status, cost, duration, and artifact refs.

## Decision

Make Fable 5 a `t4` architect and artifact generator, not a runtime worker.

## Implementation

1. Add a reusable Codex skill:
   - `/Users/rentamac/.codex/skills/fable-5-harness`

2. Use this routing policy:
   - `t0`: deterministic code
   - `t1`: local model
   - `t2`: cheap cloud
   - `t3`: synthesis cloud
   - `t4`: Fable 5 only for hard, expensive-to-reverse decisions

3. Require every Fable packet to include:
   - why
   - verified state
   - one hard decision
   - constraints
   - output contract
   - stop condition

4. Require every Fable result to produce downstream Codex/local tasks.

5. Record all Fable calls in the ledger with:
   - reason
   - tier
   - cost estimate
   - artifact created
   - downstream task count

6. Save durable memory records after tasks:
   - decisions
   - dead ends
   - procedures
   - preferences
   - project state
   - relations between agents, repos, services, and decisions

7. Retrieve bounded top-k memory before Fable handoffs; never dump full history.

8. Add observability receipts:
   - assign `trace_id` to every dispatched task
   - carry `parent_trace_id` for spawned/downstream tasks
   - write append-only JSONL receipts under `receipts/`
   - mirror queryable fields into SQLite
   - include duration, tier, model, status, tokens, estimated cost, `why_fable`, input refs/hash, output ref, and a redacted decision summary
   - never write secrets or raw private payloads to receipts

## First Smoke Test

Ask Fable once:

> Given current Grok Go routing, brakes, and Mining Engine state, produce a patch plan that reduces Fable usage by 80 percent without hurting hard-reasoning quality.

Then Codex implements from the patch plan without another Fable call.

After implementation, save a memory record with the decision, files patched, test result, and any superseded older rule.

The smoke test is not done until the dispatcher writes a receipt and the result JSON includes its `trace_id` and `receipt_path`.

## Source Packet

See:

- `/Users/rentamac/agent-comms/research/fable-5-harness/fable-5-practical-harness.md`
- `/Users/rentamac/agent-comms/research/fable-5-harness/fable-direct-message-current.md`
- `/Users/rentamac/agent-comms/research/fable-5-harness/fable-team-handoff-package-2026-07-01.md`
