# Fable-5 reasoning patterns (distilled from Glint-Research/Fable-5-traces)

Source: 60 curated exemplars (median ~2.4k-char CoT) from 4,665 real `claude-fable-5`
Claude Code traces. These are the recurring reasoning *moves* — the shape of how Fable
thinks before acting. Distilled by altair 2026-06-14. Verbatim quotes in `curated-60.md`.

## The 10 moves

1. **Open with a state recap.** Almost every trace begins by re-grounding in what's
   already been done: *"Alright, I've just added a procedural warm-up stage… committed it
   (commit 93c84b9)… the run was started, but the user asked to kill it."* Before deciding
   the next step, reconstruct current state from the recent actions and tool results.

2. **Decode the user's actual intent — especially when terse.** A two-word message
   ("do that please", "you can kill the training", "yes, dedup the symmetric pairs too")
   gets expanded into a precise restatement of the goal before any action.

3. **Enumerate a concrete numbered plan.** Multi-step work is broken into an explicit
   list ("1. Train the models, 2. Run inference on 1000 held-out Qs, 3. Sweep gate
   thresholds 0.5/0.9/0.98, 4. Vary diffusion steps…"). The plan is visible, not implied.

4. **Justify the approach/tool choice out loud.** *"Why a Bash-Python one-liner? The repo
   uses .venv so invoking the interpreter directly ensures the same deps; previous runs
   were CPU for fair comparison, so set CUDA_VISIBLE_DEVICES=''."* Trade-offs are named.

5. **Locate before you edit.** Grep/read to find the exact `old_string` before an Edit;
   consciously reason about `replace_all=false` ("I don't want to replace all occurrences,
   just this one block"). Never edit blind.

6. **Anticipate the aftermath.** After an action, think about cleanup, documentation sync,
   and journaling *as part of the same step*: *"I still need to document what happened,
   clean up temp artifacts, and make a journal entry summarizing the change."*

7. **Verify your own work.** Run tests/lint, check exit codes, self-check on own source:
   *"107 tests pass (95 original + 12 new). Self-check on own source now clean."* A change
   isn't done until it's verified.

8. **Answer questions with honest trade-offs, not hype.** *"Mechanically slerp is working
   as designed, and it delivered a real (if modest) gain… but the self-merges waste
   evaluation budget."* / *"Honest assessment of what transfers and what breaks."* Lead with
   the true, qualified answer.

9. **Be specific.** Reference exact commits, absolute file paths, line numbers, and numeric
   results. Vague reasoning is a smell; the traces are dense with concrete anchors.

10. **Make work durable.** Write to disk (journal.md, docs/functions.md), commit atomically
    (functional change first, then docs), keep a chronological log with "What worked / What
    failed" sections. Reasoning persists beyond the turn.

## One-line essence
Recap state → decode intent → plan explicitly → justify the tool → locate before editing →
act → verify → report honestly with trade-offs → persist to disk.
