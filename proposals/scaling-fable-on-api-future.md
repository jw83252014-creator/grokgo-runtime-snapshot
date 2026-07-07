# Scaling the brain — Fable-on-API & parallel compute (future ideas, Jeff 2026-06-18)

Capture only — not started. The dream: stop running Grok Go off interactive chat sessions and instead
have a real frontier brain (and cheap parallel brains) running the organism continuously, day after day.

## 1. Real Fable on the API, always-on
Run the organism loop against the API directly (not a chat UI), so Fable reasons 24/7 and dispatches to
Codex/grok/Carapace. Needs: an API budget, the loop harness (we have research_loop + bridge), and brakes
(ledger + spend caps). This is the "badass Fable just running Grok Go" vision — the loop is already the
skeleton; swap its brain from local MLX to the frontier API for the reasoning cells.

## 2. How many $200 subs to wire in parallel?
Idea: buy multiple max-tier ($200/mo) subscriptions and run them as parallel lanes (more concurrent
agents / higher limits). Open question = ToS. **Action before doing this:** check whether parallel
sub usage / multi-account is allowed for each provider (don't repeat the X "platform manipulation"
lesson). Likely cleaner + cheaper at scale to move heavy parallel work to the metered API or a served
open model (below) than to stack consumer subs. Math to run: $/Mtok on API vs. $200-sub effective tokens.

## 3. GLM-5 (and other open frontier models) — connect if served
If someone is serving GLM-5 (or similar strong open models) via an OpenAI-compatible endpoint
(OpenRouter, a host, etc.), wire it as an additional cheap reasoning lane in routing.yaml (t2/t3). Cheap
capable reasoning for the bulk work, frontier Fable only for the hardest calls. Verify model IDs/pricing
via the claude-api / provider docs before wiring — don't trust memory.

## 4. Later: serve our own model on rented hardware
End state: rent GPU (e.g. an H100 box) and serve our own model (a strong open base, optionally
fine-tuned on our clean data — NEVER on leaked/pliny traces for anything served/shared). Gives us a
private, always-on, no-per-token lane we fully control. This is where Carapace (the local cheap lane)
graduates from MLX-on-the-mini to real served inference.

## Sequencing (cheapest → most committed)
metered API for reasoning → add a served open model via OpenRouter (GLM-5 etc.) → rent GPU + serve our
own. Each step lets the organism run more continuously without burning interactive chat sessions.
Related: [[fable-model-status]], [[grokgo-agent-fleet]].
