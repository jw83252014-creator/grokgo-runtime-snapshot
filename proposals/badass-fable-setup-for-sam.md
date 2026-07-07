# Badass Fable — full setup (for Sam, to run on a Claude harness)

A clean-room, local-first "Fable-style" cell: a Claude-Code-grade harness pointed at a free local model,
steered by a distilled soul, with RAG over reasoning exemplars, brakes, and tiered escalation to a
frontier model only when earned. No secrets in this doc — bring your own keys via env.

## The idea in one line
The intelligence is the weights; everything else is the harness. So you take an open Claude-Code-grade
loop, point it at a cheap/free model for the bulk, append a "soul" prompt, and only escalate to a
frontier model when a task earns it. Cheap by default, smart on demand.

## Pieces
1. **Harness:** OpenClaude (`github.com/Gitlawb/openclaude`) — a fork of the Claude Code codebase that
   speaks to any OpenAI-compatible / local backend. Build with Bun (`bun install && bun run build` →
   `dist/cli.mjs`).
2. **Local model server:** any OpenAI-compatible server. We use an MLX server on Apple Silicon
   (Qwen-class 4B, 4-bit) at `http://127.0.0.1:8000/v1`. Ollama works too
   (`http://localhost:11434/v1`).
3. **The soul:** a distilled system prompt (~30–55 lines) appended at the system layer — voice,
   reasoning rules, operating gates. Keep it short; it steers, it doesn't add capability.
4. **RAG (optional but worth it):** embed a set of reasoning exemplars locally, retrieve top-k per query,
   prepend them so the local model "sees how to reason" about similar problems. (Use your own exemplars;
   mind the licensing of any dataset you index — keep trained/published artifacts on clean data.)
5. **Control layer:** brakes (killswitch + per-lane budget + loop detection), a tiered router
   (code → local → cheap cloud → frontier, escalate one tier only on real need), receipts, human gate.

## Wire OpenClaude → local model
```bash
export CLAUDE_CODE_USE_OPENAI=1
export OPENAI_BASE_URL=http://127.0.0.1:8000/v1      # or your local server
export OPENAI_MODEL=<your-local-model-id>
export OPENAI_API_KEY=local-no-key                   # local servers ignore it
node /path/to/openclaude/bin/openclaude \
  --append-system-prompt "$(cat /path/to/your-soul.md)" \
  -p "your task"
```

## Minimal soul (starting point — adapt to your voice)
```
- Goal-oriented: give me the goal + constraints, I choose the path.
- Lead with the mechanism. Concise. No hype, no filler.
- Read state before writing. Name uncertainty; don't fabricate facts/paths/numbers.
- Cheapest capable brain first; escalate ONE tier only when a task earns it.
- Gates: no public posts, spend, account changes, or installs without the human. Redact secrets.
- The brain is the weights; this prompt is steering, not capability.
```

## Tiered routing (the cheap-by-default rule)
- **t0** deterministic code (grep/tests/parsers) — never hits a model.
- **t1** local model — drafts, triage, summaries, schema checks.
- **t2/t3** cheap cloud — medium reasoning.
- **t4** frontier (real Fable/Opus) — hard reasoning + final adjudication only.
Schema-validate every model output; on failure, escalate exactly one tier. Brakes enforce a daily budget
+ killswitch so a runaway loop can't burn money.

## Looping cell (optional)
Run it as a loop: read a directive file → do one bounded task on the local model → write a receipt →
commit to git → sleep → repeat, with a killswitch file that halts it. That's how you get a self-running
research/draft cell for ~free.

## Honest caveats
- A small local model gives you *style + cheap drafts*, not frontier capability — keep hard reasoning on
  the real model.
- Mind dataset/ToS licensing on any reasoning traces: fine for private/own use; keep published models on
  clean data.
- On 16GB Apple Silicon a 4B 4-bit runs but is slow (~2 tok/s under load) — size the model to the box.

Questions → reach Jeff. This is the same setup running in the Null Axiom organism today.
