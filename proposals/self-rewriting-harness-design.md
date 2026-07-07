# Self-rewriting / self-evolving harness — design + how crazy we can get (Fable, 2026-06-16)

Jeff's spark (from the HarnessX signal): a harness that edits its *own* prompt — and tunes it to the
task it's about to do. Built a working prototype today (`self-rewriting-harness.py`). Here's the design,
the wild version, and the experiments — because *who says how long the prompt has to be?*

## The premise (corrected + sharpened)
Fable and Opus are **different models** (different weights), not one model with two prompts — so capability
genuinely differs. But the weights are the one thing we can't touch, so **the harness + prompt + tools +
routing is ~all the leverage we can actually pull.** HarnessX proved the payoff: evolve the harness and
*weak models jump, strong models barely move.* Translation for us: **the self-rewriting harness is how a
cheap local model punches above its weight** — exactly the Badass Fable lane.

## Two layers of "self-rewriting"
1. **Task-adaptive (built today).** Before doing the work, a cheap pre-pass writes a short task-specific
   addendum to the soul ("for THIS code task: read first, small diffs, add a test"), then runs with
   soul+addendum. Keep-mostly-same or rewrite is bounded by the base soul. Per-task, per-run, free.
2. **Trace-evolving (HarnessX-style, next).** Log every run's (task, soul-variant, output, score). A
   scoring pass proposes soul edits; only ship an edit if it **beats the current soul on held-out tasks**.
   That's the safe self-improvement loop — the harness improving its own scaffolding, gated by evals.
   Ties directly to our Researcher Layer + the self-improve loop already running.

## How crazy we can get (open ideas)
- **Per-cell harnesses.** Each cell = its own soul + length + tools + backend. A **trading harness**
  (strict JSON, Kelly/risk rules, hard brakes, no prose), a **research harness** (verbose, show-work,
  self-critique), a **draft harness** (terse, voice-matched). The cell template is the soul; swap freely.
- **Prompt-length as a knob, not a dogma.** "Short prompt = cheaper" is only true on *paid* lanes. On the
  *free local* lane, length is free — so a long, rich soul (full reasoning scaffolds, worked examples,
  self-checks) can make a 4B model far better with zero token cost. We should A/B short vs full vs long.
- **Soul tournaments.** Generate N soul variants (short/long, different emphases), run them on a fixed
  task set, score, keep the winner per task-type. Evolutionary prompt search — cheap because local.
- **Task-class routing of souls.** Classify the task → load the soul that historically won that class.
  The harness picks its own personality per job.
- **Self-authored tools/hooks.** Further out: the harness proposes a new skill/hook when it keeps hitting
  the same friction — gated, human-approved, HarnessX for the tool layer not just the prompt.

## Experiments to run (this is the fun part)
1. **Adapt on/off:** same task set, `BF_ADAPT=1` vs `=0`. Does task-tuning help? Score outputs.
2. **Length sweep:** `BF_SOUL_LEN=short|full|long` on the free lane. Find where longer stops helping.
3. **Per-cell:** build the trading soul + research soul, run domain tasks, compare to the generic soul.
4. **Trace-evolve:** after enough traces, run a scoring pass; propose one soul edit; verify it beats
   baseline on held-out tasks before shipping. (Researcher Layer owns this.)
All cheap — they run on the free local model. Brakes + a held-out eval set keep it honest (never ship a
"self-improvement" that didn't beat the incumbent on unseen tasks).

## What you can put into Grok Imagine vs NotebookLM (your question)
- **Grok Imagine = images/video from a PROMPT (+ an optional reference IMAGE for style continuity).** It
  does *not* read a research paper or documents. So to make harness visuals: extract the concepts → write
  image prompts → feed prompt + a style-reference image (e.g. our orb keyframe) so every render matches.
  That reference-image-for-style-continuity is exactly how we keep the look consistent across a set.
- **NotebookLM = documents IN → narrated audio/explainer OUT.** *This* is where the research paper goes:
  upload `claude-harness-paper.md` (+ the editable-parts map) → it makes the narrated overview. 
- So: **paper → NotebookLM (audio); concepts+style-image → Grok Imagine (visuals).** Pair them.

## Status
Prototype `self-rewriting-harness.py` runs on the free local model. Next: the length sweep + the trading
soul, then wire the trace-evolve scoring into the Researcher Layer. The harness visuals (so you can *see*
where to edit) are in production — clean map done, cyberpunk incoming from grok.
