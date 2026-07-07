# Cheaper Fable — strategy assessment (Fable, 2026-06-14)

Grok proposed: fork **OpenClaude** + inject our Fable soul + distill a local model on the HF
**fable-5-traces** + tie to a Hermes agent → a cheaper Fable. Below is a realistic assessment with a
**go/no-go + MVP**. Verified the inputs before judging (sources at bottom).

## What the inputs actually are (verified)
- **OpenClaude** (github.com/Gitlawb/openclaude): 28.8k★, TypeScript, *forked from the Claude Code
  codebase* and modified for many backends — OpenAI-compatible, Gemini, GitHub Models, Codex OAuth,
  **Ollama (local)**, Fireworks, DeepSeek/Qwen/Llama. Built-in agent routing for cost. Not Anthropic-
  affiliated. → It's a real, mature, Claude-Code-grade loop that runs against **local + free** models.
- **fable-5-traces** (glint-research): 4,665 traces, JSON, 69.8MB, **AGPL-3.0**. Provenance: "Claude
  conversation traces from an internal project, collected **before it was taken away**" (i.e. scraped/
  leaked), 953 TeichAI msgs + **CoT annotations added by the dataset creators** (so the "reasoning" is
  partly synthetic, not native Fable CoT). Tiny by training standards.
- **Official Fable-5 prompting guide** (legit techniques to fold in): goal-oriented prompting (define
  goals, not steps), **effort tiers** (High default, XHigh/Ultracode for hard), **/loop** for autonomy,
  **conciseness** (over-engineering degrades output), **markdown memory files** for cross-loop lessons,
  and "Opus-4.8 prompts ≠ Fable-5" (adapt per model).

## The three questions, answered straight

### (1) Fine-tune on the 16GB M4 mini — feasible, or is few-shot/RAG the real move?
**Full fine-tuning: no.** 16GB unified memory is shared OS+GPU. Full FT of even a 1B model (weights +
gradients + Adam states ≈ 16–20GB) doesn't fit. **QLoRA via MLX** is the only on-device training that
fits, and realistically only up to a **3B** base (4-bit 3B ≈ 1.8GB + activations + adapter grads; slow,
tiny batch/seq). 7–8B QLoRA is borderline-painful. **Inference** is fine: a 4-bit **7–8B** (Qwen2.5-7B/
Coder, Llama-3.1-8B) runs comfortably (~5GB) on the mini via MLX/Ollama.

So the realistic move is **RAG / few-shot over the traces at inference**, not training. Index the 4,665
traces, retrieve a few style-matched exemplars per call, prepend to the local model's context. If we ever
train, it's a **3B QLoRA for VOICE only** — and that brings us to the hard truth:

**A local 3–7B cannot do Fable-level WORK.** Capability lives in the weights (Opus/Fable is hundreds of
B). 4,665 mostly-synthetic-CoT traces transfer *style*, not *reasoning*. You'd get something that *sounds*
like Fable and *fails* the hard tasks Fable is for. Recommended local model: **Qwen2.5-7B-Instruct (4-bit
MLX)** for inference + RAG; **Qwen2.5-3B** if we insist on a QLoRA voice experiment.

### (2) Does OpenClaude beat what we already have (Claude Code + souls + collector + router)?
**Mostly no — it's complementary, not a replacement.** Our stack already has the strong parts: souls via
`--append-system-prompt`, the tiered router with ledger/brakes, free-brain routing, the collector. The
**one thing Claude Code can't do is run our soul against a local/arbitrary backend** — it's Anthropic-
locked. OpenClaude *can* (Ollama, DeepSeek, GitHub Models in one Claude-Code-grade loop). But our router
already dispatches to free brains at the task layer, so the overlap is large. Net: OpenClaude is worth a
**spike as an experiment lane** ("Fable soul on a local model with a real tool-loop"), **not a migration**.
Don't rip out what works.

### (3) Simplest real path to Fable-level work cheaper + risks
"Fable-level work" cheaply is, unavoidably: **route the genuinely hard calls to real Fable/Opus** (you
can't fake the capability) and push everything else to free/local. That's already grokgo's thesis. The
cheap wins that are *real*:
1. **Fold the official Fable-5 techniques into the soul** (free, immediate) → leaner, more autonomous
   frontier calls = fewer tokens/turns per hard task. Ready-to-paste block below.
2. **Offload low-stakes drafting to a local 7B** (via OpenClaude or our router) with **RAG over the
   traces for style** — not training.
3. Keep the hard calls on Fable/Opus.

**Risks (be honest):**
- **Legal/ToS:** the traces are scraped frontier-model outputs. Anthropic's ToS prohibits using outputs
  to build a competing model. AGPL-3.0 covers the *dataset packaging*, **not** permission for the
  underlying content. Training a "cheaper Fable" on them and shipping it is real exposure. Using them as
  **private few-shot style exemplars** (RAG, not redistributed, not trained-and-published) is far lower
  risk but still grey — keep it internal, never publish a model trained on them.
- **Quality:** synthetic-added CoT + "taken away" provenance = noisy; 4,665 is tiny.
- **Capability ceiling:** 3–7B ≠ Opus; voice mimic, not reasoning.
- **Maintenance:** a local train/serve pipeline on a 16GB box is heavy upkeep for low payoff.

## GO / NO-GO
- **NO-GO:** fine-tuning a local model to *replace* Fable. Infeasible at capability on 16GB + legal risk +
  tiny/noisy data. Don't.
- **GO (MVP, low-risk, cheap):**
  1. **Fold Fable-5 guide techniques into the distilled soul** (proposal below) — do first, costs nothing.
  2. **Spike OpenClaude** in a sandbox: our soul × Ollama **Qwen2.5-7B (4-bit)**; run 3 real *low-stakes*
     tasks; compare quality to free GitHub Models. Keep hard tasks on Fable.
  3. If the spike wins, add a **`local-fable` router tier** for drafting/grunt work only.
  4. **RAG (not train)** the traces: build a private index, retrieve few-shot style exemplars at
     inference. Internal use only; never publish a trained artifact.
  5. **Defer any QLoRA** until RAG proves insufficient *and* legal is cleared.
- Tie-in: the local-fable lane becomes a **Hermes agent** addressable on the bridge, behind the router.

Outcome: cheaper by making frontier calls leaner (#1) and offloading low-stakes work to local (#2–4),
**without** the legal/capability trap of cloning.

## Proposal: fold official Fable-5 techniques into the soul
Append-ready block for `~/grokgo/prompt-lab/prompts/fable5-distilled-for-claude-code.md` (apply on Jeff's
OK — keeps it a plan, not a build):
```
## Operating mode (Fable-5 guide)
- Goal-oriented: tell me the goal + constraints, not every step; I choose the path.
- Effort: default High; reserve XHigh/Ultracode for genuinely hard, multi-step work.
- Loop: for multi-step objectives, keep working until the goal is met; pause for input only at the
  decision points I flag.
- Concise: no over-engineering; over-long prompts/answers degrade quality.
- Memory: record cross-loop lessons to markdown (proposals/learnings.md) and read them back.
```

## Sources
- github.com/Gitlawb/openclaude · huggingface.co/datasets/glint-research/fable-5-traces
- Anthropic Fable-5 prompting guide (via phemex.com, thewincentral.com, alphasignalai.substack.com summaries)
