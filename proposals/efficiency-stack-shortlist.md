# Efficiency stack — the shortlist (Fable, 2026-06-17)

We've collected a cluster of "efficient local-first" signals. They all point the same way and they're
good — so here's the consolidated shortlist + ONE test pass, instead of a file + a chase per tool.
The honest note: collecting signals ≠ shipping. Test these once, adopt the winners, keep building.

## The shortlist (retrieval + inference efficiency)
| Tool | What it does | Layer | Verdict |
|---|---|---|---|
| **grep/BM25 > vector** (arxiv 2605.15184) | literal search beats embeddings for code/exact lookup, less noise | retrieval | **Default to it** — Codex A/B running. Low effort, high payoff. |
| **LEANN** (StarTrail-org) | compressed vector retrieval — 201GB→6GB (97%), laptop, no GPU, no accuracy loss | retrieval | **Test** — this is the "if you DO need vectors, compress hard" answer. Pairs with grep-first. |
| **Headroom** (chopratejas) | compresses tool-output/context *in-flight* 60–95% before the model | context | **Cloned to spike; test** — complements rtk (shell) + LEANN (storage). |
| **llmfit** | right-sizes/quantizes local models to the hardware | inference | **Test** — picks the best local model for the 16GB mini. |
| **Niels Rogge efficient VLM** | a compute-friendly vision-language model | inference | **Eval list, not urgent** — no pressing multimodal need yet; add when Codex evals local models. |
| **Darkbloom** | decentralized inference on idle Apple Silicon, ~50% cheaper | inference | **Provider-test only** (enroll mini idle; watch payouts before renting a box). |

## The picture (how they fit, not compete)
- **Retrieval:** grep/BM25 first → LEANN (compressed vectors) only for conceptual queries the Researcher Layer routes to.
- **Context:** rtk (shell output) + Headroom (in-flight context) — stack them.
- **Inference:** llmfit picks the model; MLX local default; Darkbloom/frontier as lanes.
This *is* the "cheap by default, smart on demand" + "move forward, less waste" principle, made concrete.

## ONE test pass (Codex — fold into the grep/Headroom work already running)
1. grep/BM25 vs vector vs **LEANN** on our trace corpus → pick the retrieval default.
2. Headroom in-flight compression — measure savings + quality on a real session.
3. llmfit on the mini — best local model pick.
Write one combined report to `research/loop/efficiency-stack-results.md`. Adopt winners; skip the rest.

## The honest call
This efficiency thesis is *converged* — we don't need more tools to prove it; we need to test these once
and get back to shipping the things that move Jeff forward: the **Nous hackathon**, the **outreach
videos**, the **website**, **BidLocal**. New efficiency signals → drop them in this table, don't start a
new research thread each time.
