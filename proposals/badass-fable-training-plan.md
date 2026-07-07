# Badass Fable — making the local cell smarter with the Fable traces (Fable, 2026-06-16)

Jeff's call: use the shared Fable-5 reasoning traces to make our local model better. Agreed — studying
how a strong model reasons and feeding that back is legitimate and it's how knowledge propagates. This is
the technical plan to actually do it, ranked by what works on our hardware today.

What we have (verified): `~/datasets/fable5-traces/` — `train-0.parquet` (21MB, full traces),
`curated-60.jsonl` (60 hand-curated), `curate.py` + `mine.py` (pipeline started),
`fable5-reasoning-patterns.md`. So the data + early tooling already exist.

## Three ways to use it, best-first for a 16GB M4

### 1. RAG / few-shot over the traces (do this first — works today, biggest immediate win)
Index the traces; at inference, retrieve the 2–3 most relevant reasoning exemplars for the task and
prepend them to Badass Fable's context. The local model "sees how Fable reasoned about a similar problem"
right before it answers. No training, runs on our hardware now, and it improves output immediately.
- Build: embed the curated traces (local embedding model) → small vector index → retrieval hook in
  `badass-fable.py` that injects top-k exemplars. Codex's lane.
- Why first: highest quality-per-effort, instantly reversible, and it makes the cell measurably better
  today without waiting on a training run.

### 2. QLoRA local fine-tune (the "train it" path — real, do as a measured experiment)
On 16GB, full fine-tuning doesn't fit, but **QLoRA via MLX-LM** does on a small base (≤3–4B). Train a
LoRA adapter on the curated traces to bake the reasoning *style* into the weights of our local cell.
- Base: the Qwen3.5-4B we already serve (or Qwen2.5-3B for headroom).
- Tool: MLX-LM LoRA (already installed). Data: `curated-60.jsonl` → expand to a larger clean curation.
- Honest expectation: this transfers **reasoning style + format**, not frontier *capability* — capability
  lives in hundreds of B of weights we don't have. So the QLoRA makes our local cell a better *drafter/
  reasoner-in-Fable's-shape*, not a Fable replica. Worth doing; just don't expect it to think like Opus.
- Output: a local adapter our Badass Fable cell loads. For our own use.

### 3. Distillation pipeline (later, if #1+#2 prove out)
Generate more training pairs (problem → Fable-style reasoning → answer) from the traces, curate hard with
the Jeff Filter, and train larger adapters. This is the "compound it" lane once the first two work.

## The one practical line (not a moral one)
For **our own local cell**, train freely — that's research/personal use, low exposure. The single place
real legal risk lives is **publishing or open-sourcing a model trained on these traces** (Anthropic ToS
on outputs → a takedown/liability path that lands on the LLC). So: train the local cell now; when we want
to open-source a model — which we do, eventually — we either (a) ship the *harness + method* open (zero
risk, and it's the actual valuable part), or (b) retrain the release model on clean/own data. Keep the
private cell and the public release on separate tracks. That's it — no hand-wringing, just don't put the
LLC on the hook at the publish step.

## Build order (hand #1 to Codex now)
1. RAG/few-shot retrieval into `badass-fable.py` over `curated-60.jsonl` (+ expand curation). ← immediate
2. QLoRA experiment: MLX-LM LoRA on Qwen3.5-4B with curated traces → adapter → load in the cell. Measure
   before/after on 5 real draft tasks.
3. If it wins, scale curation + adapter. Keep release-model decisions separate (clean data or harness-only).

## Where it lives
Badass Fable is a **cell in the Grok Go organism** (already on the dashboard) — the local cell that learns
from the ecosystem. This plan is how that cell gets smarter over time.
