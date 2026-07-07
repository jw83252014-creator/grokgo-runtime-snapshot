# Fable Token Savings Master Packet - 2026-07-05

## Purpose

Consolidate the current Fable/token-savings harness work into one Git-ready reference. This packet is meant for Grok Go / Agent Bridge development, not public posting.

## Core Rule

Fable is the hard-reasoning governor, not the default worker.

Default route:

```text
t0 deterministic code -> t1 local/Jade -> t2 cheap cloud -> t3 synthesis -> t4 Fable
```

Escalate one tier at a time. Nothing jumps straight to Fable unless it is a hard architecture, safety, funding, strategy, or one-way-door decision.

## Source Signals

| Source | What It Adds |
| --- | --- |
| Nathan Tulu Fable post | reason-first prompting, strong `CLAUDE.md`, avoid visible CoT, reduce fallback/refusal |
| Surim0n Fable post | task decomposition and using Fable only for one-way-door decisions |
| Miles Deutscher Fable guide | loop engineering, memory, narrow skills, long-run stability |
| Conare / Artem Murzin | persistent memory across Claude Code, Cursor, Codex-style agents |
| pxpipe / image-token compression | dense archival context as PNG/image packets, eval before default |
| Hugging Face agent traces | useful metadata and harness shapes; clean-room only |
| Local Grok Go token proposal | rtk, prompt caching, summarize-then-act, context hygiene |

## Highest-Leverage Rules

### 1. Stable Prefix + Volatile Tail

Prompt caching only helps when the prefix stays stable. Put stable role rules, current state pointer, output schema, and hard gates before task-specific context.

### 2. Context Kernel Before Fable

Never dump raw meeting logs or whole chats into Fable.

Pipeline:

```text
raw source -> local index -> Jade/cheap clustering -> context packet -> Fable decision
```

### 3. Precision Classes

| Class | Meaning | Allowed Compression |
| --- | --- | --- |
| `exact_text` | code, IDs, numbers, citations, money, user commands | raw text only |
| `source_linked_summary` | summarized source with path/URL/hash | summary plus source ref |
| `png_background_context` | bulky stale orientation context | PNG/image packet candidate |
| `discard` | stale duplicate/noise | do not send |

### 4. pxpipe Is An Eval, Not Default

Candidate PNG/image context:

- old chat exports,
- old meeting-log slices,
- X Radar source matrices,
- repeated docs and bulk orientation material.

Never use PNG compression for code patches, exact citations, credentials, money, file paths that must be copied exactly, or punctuation-sensitive material.

### 5. Clean-Room Trace Policy

Track public trace datasets as ecosystem evidence, but do not copy hidden reasoning traces into prompts, skills, or training corpora.

Allowed:

- metadata,
- licenses,
- harness shapes,
- high-level public patterns,
- our own receipts/session summaries,
- clean open tool trajectories.

Hard no:

- raw hidden CoT,
- leaked trace payloads,
- prompt examples whose main value is hidden chain-of-thought,
- unclear provenance/license.

### 6. Token Scout Lane

Create/keep a read-only `token-scout` lane:

- watches X/GitHub/docs for token-savings/context-engineering tricks,
- writes one private digest max per day,
- top 1-3 findings only,
- no public posting,
- no repo mutation,
- Null/Fable approve memory promotion,
- Keystone implements small tasks.

## Fable Decision Needed

1. What minimum change to the Fable bridge stops budget blowups?
2. Should the bridge load current-state + selected context-kernel rows instead of full memory files?
3. What prompt prefix should remain byte-stable for caching?
4. How should pxpipe be evaluated without risking exactness loss?
5. Which pieces belong in GitHub-facing docs vs private `agent-comms` memory?

## Proposed Bridge Patch Direction

Replace huge always-loaded memory prompt with a compact stable prefix:

```text
You are Fable in Agent Bridge.
Role: hard reasoning governor. Routine work goes to Keystone/Jade/local lanes.
Read current state path: /Users/rentamac/agent-comms/state/CURRENT_STATE.md
Use retrieved context snippets only when provided.
Output: decision, tasks, stop rules, risks.
No public/account/spend actions.
```

Then pass task-specific context as a bounded packet path.

