# GrokGo Claude Code Context

This repo is the shared runtime memory for GrokGo / the Digital Organism. Read this file first, then read `TASK_BOARD.md` before doing task work.

## Canonical Thesis

GrokGo is a layered agent organism built for long-running coherence instead of one giant model trying to do everything.

- Researcher Layer: the brain / central coordination layer. It routes work, keeps state, asks for deep reasoning only when earned, and preserves continuity.
- Tool Cells: scoped workers for research, mining, content, health, code, X radar, visuals, business ops, and other repeatable jobs.
- Conscious Layer: memory, identity, receipts, and the Jeff-facing continuity layer.
- Brakes + Ledger: every model/tool lane should be governed by killswitches, budgets, stop conditions, trace IDs, append-only receipts, and review gates.

The biological analogy matters: inspired by Michael Levin-style multi-scale agency, the organism should behave like coordinated cells under explicit boundaries, not like a brittle prompt chain.

## Jeff / Project Facts

- Jeff built Champion Fencing from the ground up as a hands-on fencing contractor. This is real operator proof: estimates, crews, customers, cash flow, mistakes, and local service work from the ground.
- Bid Local is the contractor marketplace / co-op economic layer: cleaner bids for homeowners, less lead-broker extraction, and shared upside for crews doing the work.
- GrokGo / Digital Organism is the AI-native layer that makes a bootstrapped operator team act like a funded one: specialized agents, receipts, budgets, hard stops, and persistent memory.
- Sam is a technical collaborator with Hermes Desktop and GitHub. Jade/GLM failover should be packaged so Sam can recreate it without hunting through Jeff's machine.

## Current Lanes

Use `LANE-MAP-2026-07-02.md` as the current lane map. High-level summary:

- Null: Jeff-facing coordinator and memory/routing lane. Jeff wants to talk mostly to Null, not every helper directly.
- Fable: hard reasoning and architecture. Expensive turns must be justified; `t4` tasks require `why_fable` or `why`.
- Keystone/Codex: build/execution lane. Use for code, repo edits, mechanical changes, tests, and receipts.
- Jade: cheap GLM 5.2 lane for scoring, S1 content triage, and high-volume background work.
- Morpho/Castor/Nova: Gemini-backed lanes for research and tab/CLI memory experiments.
- Vega: creative lane for visuals, video drafts, and presentation material.

## Read Order For New Claude Code Sessions

1. `CLAUDE.md` (this file)
2. `TASK_BOARD.md`
3. `LANE-MAP-2026-07-02.md`
4. `routing.yaml`
5. `brakes.py`
6. Relevant directive under `directives/`
7. Relevant proposal or receipt under `proposals/` or `receipts/`

Do not assume old chat context is complete. The repo is the shared memory.

## Runtime Shape

- `routing.yaml`: task type to tier/model routing and budgets.
- `dispatch.py`: routes tasks through directives and model tiers.
- `brakes.py`: killswitch, max turns, loop detection, per-lane spend, halt-on-no-work, ledger receipts.
- `bus.py`: inbox/outbox task movement.
- `mining_pipeline.py`: staged X/content intelligence pipeline.
- `review_queue.py`: draft/review gate before public output.
- `tools/behavioral_markers.py`: deterministic t0 marker computer for goal/polish/correction/cooperation/maintenance signals.
- `directives/`: small task-specific prompts/contracts.
- `proposals/`: architecture notes, handoffs, and non-live plans.
- `receipts/`: append-only runtime receipts. Treat as evidence, not scratch space.

## Safety Boundaries

Draft-only unless Jeff explicitly approves the exact action:

- public posts, replies, DMs, emails, or sends
- spending money or changing account/billing/subscription limits
- connecting wallets, trading, or financial actions
- deleting data, resetting repos, or irreversible account/system changes
- exposing secrets, tokens, private logs, raw account state, or private filesystem paths in public copy

Use receipts for anything meaningful. Redact secrets before quoting. Do not put raw `.claude`, browser session state, private Grok memory, ledgers, or logs into public repos.

## Fable Token Discipline

- Default to deterministic code or cheap/local lanes.
- Escalate one tier at a time unless a human or Researcher Layer explicitly routes to Fable.
- A `t4` call must state why Fable is needed and what decision it changes.
- Use clear stop conditions, budgets, and output contracts.
- If a task is just glue, parsing, formatting, moving files, or simple scoring, do not burn Fable.
- Behavioral classification stays t0/deterministic in the hot path. Use sampled t1 calibration only to audit the rules; the LLM judges the classifier, it does not become the classifier.

## Brake Configuration

- Budget windows default to UTC midnight.
- `defaults.budget_day_start_hour_utc` in `routing.yaml` can set an explicit UTC reset hour.
- `BRAKES_TZ_OFFSET_HOURS` overrides that with a fixed local-midnight offset, e.g. `-8` for UTC-8. Keep this fixed-offset and explicit for deterministic ledgers.

## Action Receipt v2

`brakes.log()` emits `schema_version: grokgo.action_receipt.v2` in every JSONL receipt. This is the instrumentation gate for behavioral-marker science: old Grok unified logs are useful as a thin baseline, but future polishing-loop claims must come from these richer receipts.

Required fields for meaningful action receipts:

- `task_type`: stable task/category label.
- `outcome`: normalized `success`, `partial`, `failure`, or a short explicit status.
- `output_summary`: concise summary of what changed or what was produced.
- `tokens`: object with `input`, `output`, and `total`.
- `new_capability_vs_polish`: deterministic behavior tag. Valid values: `new_capability`, `polish`, `maintenance`, `correction`, `cooperation`, `unknown`.
- `behavior_rule_hits`: deterministic rule names that explain the tag, or `caller_supplied` when the task provided the tag.

If a caller can tag the action honestly, pass `new_capability_vs_polish` on the task. If not, `brakes.py` self-tags from `output_summary`, artifact metadata, handoff metadata, and status. Do not use an LLM in the hot path for this classification; sampled cheap-model calibration can audit the rules later.

## Current Priority Threads

- X Radar / Mining Engine: use cheap oEmbed/text ingest first, Jade/GLM S1 scoring, then Fable only for borderline or reputation-sensitive calls.
- Public repo hygiene: keep public snapshots useful but scrub private paths, logs, account state, ledgers, and secret-shaped material.
- Shared continuity: keep canonical context in repo files so account switching and model resets do not erase state.
- Jade packaging: produce a simple reproducible Hermes/GLM failover kit for Sam.
- Health/dashboard/science notes: grow structured notes, but do not let them derail runtime safety and content/intelligence work.

## Working Style

- Read before writing.
- Prefer small, reversible edits.
- Run targeted tests.
- Commit intentionally when asked or when a stable restore point is needed.
- Report result first, then evidence.
- If blocked, ask the smallest concrete question and leave a receipt or proposal.
