# Grok vs Grok-Fable Side-by-Side - 2026-06-16

## Summary

Codex briefed regular Grok on the new `grok-fable` ThinkPad harness, then ran matched tests on regular Grok and Grok-Fable.

Verdict: **Grok-Fable is better for Agent Bridge operations**: receipts, gates, status/changed/next discipline, and bounded next action. Regular Grok is still strong for broader explanation, but it needed more turns on non-isolated runs and drifted toward essay mode.

## Test Locations

ThinkPad artifacts:

- Regular acknowledgement: `~/agent-bridge/harness-tests/results/regular-brief.txt`
- Non-isolated regular dashboard: `~/agent-bridge/harness-tests/results/regular-dashboard.txt`
- Non-isolated Fable dashboard: `~/agent-bridge/harness-tests/results/fable-dashboard.txt`
- Non-isolated regular traces: `~/agent-bridge/harness-tests/results/regular-traces.txt`
- Non-isolated Fable traces: `~/agent-bridge/harness-tests/results/fable-traces.txt`
- Isolated regular dashboard: `~/agent-bridge/harness-tests/iso-results/regular-dashboard.txt`
- Isolated Fable dashboard: `~/agent-bridge/harness-tests/iso-results/fable-dashboard.txt`
- Isolated regular traces: `~/agent-bridge/harness-tests/iso-results/regular-traces.txt`
- Isolated Fable traces: `~/agent-bridge/harness-tests/iso-results/fable-traces.txt`
- Regular receipt: `~/agent-bridge/harness-tests/iso-regular/outbox/dashboard-next-step.md`
- Fable receipt: `~/agent-bridge/harness-tests/iso-fable/outbox/dashboard-next-step.md`

## What Happened

Regular Grok understood the harness after being briefed:

- Same underlying Grok Build CLI.
- `grok-fable` adds `--rules` from `~/agent-bridge/prompts/grok-fable-harness.md`.
- It uses `--permission-mode bypassPermissions`, `--always-approve`, segmented compaction, and `--todo-gate`.
- It preserves clean-room boundaries: no hidden prompt copying, no raw reasoning trace ingestion.

## Non-Isolated Run

Regular Grok hit `max turns reached` on both first attempts:

- Dashboard with `--max-turns 5`: timed out before receipt.
- Reasoning trace policy with `--max-turns 5`: timed out before answer.

After raising regular Grok to `--max-turns 10`, it completed both.

Grok-Fable completed the same tasks under the larger cap. However, the first Fable dashboard run noticed the regular sibling receipt, so that result was useful but not clean enough for a fair score.

## Isolated Run

The isolated prompts explicitly forbade parent/sibling/external reads.

### Dashboard Receipt

Both wrote `./outbox/dashboard-next-step.md`.

Regular Grok:

- Good technical proposal.
- Suggested `outbox/tile-contract-v0.1.json` or `.yaml`.
- Clear gates.
- Slightly more generic; less connected to harness/receipt discipline.

Grok-Fable:

- Better operational framing.
- Proposed versioned JSON Schema plus examples and README.
- Included acceptance criteria and explicit additive-only gate.
- Clearer about no UI/live adapters/network calls yet.

Winner: **Grok-Fable** for Agent Bridge work.

### Reasoning Trace Policy

Regular Grok:

- Strong, broad, technically useful.
- Mentioned eval contamination, holdout discipline, manual labels, and benchmark laundering.
- Better for a research memo.

Grok-Fable:

- More directly aligned to the harness.
- Ended with `status`, `changed`, `next`, `gates`.
- Cleaner practical rule: summaries, labels, rubrics, eval outcomes; no raw CoT.
- Better for bridge/action workflow.

Winner:

- **Regular Grok** for broad explanation.
- **Grok-Fable** for operational answer and safe next step.

## Recommendation

Use:

- `grok-fable` for Agent Bridge tasks, receipts, dashboard specs, approval-gated work, Fable/Badass Fable coordination, and anything that should land as an artifact.
- Regular Grok for open-ended ideation or broader research memos when you do not need a strict receipt/gate contract.

Next useful step: build the 20-case closure eval pack the models both recommended, with frozen prompts and rubric dimensions:

- follows scope
- writes required artifact
- has `status/changed/next/gates`
- preserves approval gates
- avoids raw reasoning trace use
- avoids false action claims
- completes within turn budget

That turns this from a vibe check into a recurring scoreboard.
