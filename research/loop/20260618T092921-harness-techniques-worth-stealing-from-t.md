# research.loop receipt — 2026-06-18T09:29:21Z

target: harness techniques worth stealing from the open agent ecosystem

I have read the directive, the proposal queue, and the last three receipts in `research/loop/`. I have also checked `routing.yaml` and the trace RAG index to confirm the current state of our local harness and research backlog.

I have reviewed the existing receipts regarding local models (Qwen, Llama, Phi), Fable-trace usage (RAG retrieval quality), and distilled datasets. The last cycle covered "Cheaper/faster local inference (MLX tricks, quantization, speculative decoding)." The next available target in our rotation is **Harness techniques worth stealing from the open agent ecosystem**.

I have performed a self-critique: *What is the weakest part of this plan?* The risk is assuming "open agent ecosystem" implies a single, monolithic standard. In reality, it is a fragmented landscape of tooling (LangChain, LlamaIndex, CrewAI, AutoGen, etc.) with varying degrees of integration into MLX and local inference. I must be careful not to conflate "agent frameworks" with "local inference engines." The "stealable" techniques are likely architectural patterns (e.g., tool-use loops, state management) rather than library imports. I will verify which patterns are actually portable to MLX or have clear equivalents in our current `src/` structure.

I have not found a definitive, single "best" technique in the wild that applies universally to our specific MLX-based Fable harness without further context or a specific agent framework example. The landscape is too dynamic and our local constraints (M4 Mac Mini, MLX backend) are specific enough that a blanket recommendation is risky.

I will mark the findings as `UNCERTAIN` regarding a universal "stealable" technique, noting that the answer likely depends on which specific agent framework we are emulating or extending. I will propose a concrete, low-risk candidate: auditing our current tool registry against the most popular open-agent patterns to identify gaps.

Here is the findings receipt.

```markdown
target: harness techniques worth stealing from the open agent ecosystem
found: 
- The "open agent ecosystem" is fragmented; there is no single standard technique that applies universally to MLX-based local harnesses. Major contenders (LangChain, LlamaIndex, CrewAI, AutoGen) prioritize different abstractions (graph-based vs. task-based vs. role-based).
- Local inference (MLX) typically requires explicit tool wrapping rather than native agent loops, meaning "stealing" a technique often means adapting a high-level framework pattern to a low-level MLX call stack.
- No verified, high-impact technique was found in the last 3 receipts or the immediate RAG trace that directly improves our current MLX Fable harness without significant refactoring.
- A few patterns (e.g., tool-use loops, state persistence) are common, but their implementation in MLX often incurs latency or complexity trade-offs not present in cloud-based agents.
candidate: Audit our current `src/` tool registry against the top 3 open-agent frameworks (LangChain, CrewAI, AutoGen) to identify which architectural patterns (e.g., tool-calling schemas, state management) are missing or misaligned, then draft a "local-agent-patterns.md" proposal for Jeff to review before implementation.
next: In the next cycle, review the proposed audit against the specific MLX constraints (e.g., MLX's lack of native tool-calling support vs. Pythonic tool wrapping) to refine the candidate into a concrete implementation plan or a "don't do this" list.
```
