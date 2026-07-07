# Fable — task list (work through these, report as you go)

Keep notes terse for Jeff (did this / found / next). Draft-only; no posting/spend/account changes.

## 1. Get familiar with the code "you" (Fable) built
The Grok Go router/mining code is exceptional and was built by an earlier Fable session. Read and
review it, note what's strong and what you'd improve:
- `~/grokgo/dispatch.py`, `brakes.py`, `bus.py`, `mining_pipeline.py`, `load_anchors.py`, `review_queue.py`
- `~/grokgo/routing.yaml`, `~/grokgo/directives/`

## 2. Check our Polymarket / Kalshi research
- `~/agent-comms/workers/scripts/kalshi-monitor.py`
- `~/agent-comms/workers/projects/frankenstein-poly/` (kalshi-state.json, kalshi-config.json)
- Memory says there's also a polymarket bot at `~/.openclaw/workspace/polymarket-bot/` — look if present.
Summarize: what the trading research currently does, and one concrete improvement.

## 3. Before/after on our prompt work
- Compare `prompts/reference/CLAUDE-FABLE-5-pliny.md` (raw consumer prompt) vs
  `prompts/fable5-distilled-for-claude-code.md` (lean version wired into you).
- The full Pliny repo is at `~/grokgo/prompt-lab/CL4R1T4S/` — including Opus 4.7
  (`CL4R1T4S/ANTHROPIC/Claude-Opus-4.7.txt`) so you can see what changed Opus→Fable.
- Codex prompt: `CL4R1T4S/OPENAI/Codex.md`. Grok: `CL4R1T4S/XAI/`.

## 4. Suggest prompts to make Codex AND Grok better
Using the same "distill the useful patterns, drop the irrelevant" approach you saw for yourself,
draft a lean Codex prompt and a lean Grok prompt tuned for our agent lanes. Save to
`~/grokgo/prompt-lab/prompts/codex-distilled.md` and `grok-distilled.md`.

## 5. Read the shared brain if you haven't
`~/grokgo-context/SHARED.md` and `~/grokgo/prompt-lab/FABLE-ONBOARDING.md`.
