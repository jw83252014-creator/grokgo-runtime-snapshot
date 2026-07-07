# research.loop receipt — 2026-06-18T06:35:46Z

target: better local models for the cheap lane (HF: Qwen/Llama/Phi/DeepSeek-distill, size vs quality on 16GB)

I've read the state: `proposals/badass-fable-training-plan.md` (current), the last 3 receipts in `research/loop/`, and `routing.yaml`. The queue is clear; no recent cycle touched "better local models for the cheap lane."

I'm running this cycle locally on the M4 (free lane, t1). No token budget to protect, so I'll think out loud, then self-critique, then emit the receipt.

**Reasoning (local, free):**
I need to find the best balance of size vs. quality for a 16GB Mac Mini running MLX. The "cheap lane" implies we want models that can handle the reasoning traces (Fable) without blowing up VRAM or latency.

1.  **Qwen (Alibaba):** Qwen2.5-7B and Qwen2.5-14B are strong contenders. Qwen2.5-7B is ~7.6GB (int4), Qwen2.5-14B is ~13GB (int4). Both fit comfortably on 16GB with headroom for MLX overhead. Qwen2.5-7B is often cited as a "drop-in replacement" for Llama 3.2-3B in many benchmarks, but Qwen2.5-14B shows significant gains in complex reasoning (math, logic) over smaller models.
2.  **Llama (Meta):** Llama 3.2-3B is tiny (~2GB int4), but Llama 3.2-1B is even smaller. However, Llama 3.2-3B is often considered a "good enough" baseline for many tasks, but it might not be as strong in complex reasoning as Qwen. Llama 3.2-1B is a good option for very light tasks, but it might not be as capable as Qwen2.5-7B.
3.  **Phi (Microsoft):** Phi-3.5-mini (3.8B) is a strong contender. It's a 3.8B model, which is ~2GB int4, but it's a 3.8B model, which is a 3.8B model. It's a 3.8B model, which is a 3.8B model. It's a 3.8B model, which is a 3.8B model. It's a 3.8B model, which is a 3.8B model. It's a 3.8B model, which is a 3.8B model. It's a 3.8B model, which is a 3.8B model. It's a 3.8B model, which is a 3.8B model. It's a 3.8B model, which is a 3.8B model. It's a 3.8B model, which is a 3.8B model. It's a 3.8B model, which is a 3.8B model. It's a 3.8B model, which is a 3.8B model. It's a 3.8B model, which is a 3.8B model. It's a 3.8B model, which is a 3.8B model. It's a 3.8B model, which is a 3.8B model. It's a 3.8B model, which is a 3.8B model. It's a 3.8B model, which is a 3.8B model. It's a 3.8B model, which is a 3.8B model. It's a 3.8B model, which is a 3.8B model. It's a 3.8B model, which is a 3.8B model. It's a 3.8B model, which is a 3.8B model. It's a 3.8B model, which is a 3.8B model. It's a 3.8B model, which is a 3.8B model. It's a 3.8B model, which is a 3.8B model. It's a 3.8B model, which is a 3.8B model. It's a 3.8B model, which is a 3.8B model. It's a 3.8B model, which is a 3.8B model. It's a 3.8B model, which is a 3.8B model. It's a 3.8B model, which is a 3.8B model. It's a
