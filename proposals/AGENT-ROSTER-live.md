# Live agent roster — who's running, how to address them, what they're on (Fable, 2026-06-19)

**Key rule (this is what kept biting us):** bridge lanes only act on an **@mention IN THE MESSAGE TEXT**
(`@vega`, `@keystone`, etc.) — NOT the "agent" field. Dispatch with the @mention or nothing happens.

| Agent | Model / lane | Address as | Running? | Job / current task |
|---|---|---|---|---|
| **Fable** | Opus 4.8 (this interactive session) | (you talk to me) | ✅ | Reasoning, design, orchestration. Working with you now. |
| **vega** | Opus 4.8 — `vega_claude_cli_bridge.py` | `@vega` / `@opus` | ✅ | Hard reasoning / review / second opinions. (No file writes — read-only by design.) |
| **atlas** | Sonnet — `atlas_claude_cli_bridge.py` | `@atlas` | ✅ | Older relay/reasoning lane (cheap). |
| **keystone** | Codex gpt-5.5 xhigh — `keystone-codex-bridge` (launchd) | `@keystone` / `@codex` | ✅ consumes, ⚠️ **outputs not landing** | BUILD lane. Picked up: build-status, grok-capture, hermes-agentify, Librarian-memory, image-gen — but produced no output files. Needs `codex exec` flags debug. |
| **grok-terminal** | Grok web — `grok_terminal_bridge.py` | (grok lane) | ✅ | Grok web reasoning lane. |
| **null** | Hermes null — discord + agent bridge | (null persona) | ✅ | Null persona / Discord. |
| **frankenstein** | Phone (Moto G), Tailscale | (phone lane) | ✅ online | Always-on phone agent. NOT yet on Grok sub (your login pending). |
| **gemini castor / nova** | Gemini lanes (launchd) | (gemini) | ⚠️ CLI dead | Gemini CLI free-tier killed by Google. Browser Gemini (logged in) still works. |
| **Carapace** | local Qwen (`hermes-mlx`) | (local) | ✅ | Free local reasoning; research loop runs on it. |
| **imagine-collector** | render queue (:8799) | (queue) | ✅ | Holds image prompts for the (broken) render pipeline. |

## Librarian — direct answer
**Not fixed / not on jeff8338 yet.** The memory-build (Right-Agent grok chat → Librarian) was dispatched
to keystone, which *ran* it but landed no confirmed output. And the **X login to jeff8338 is YOUR one-time
step** (I scaffold, you log in) — not done. So Librarian is NOT live on X. Needs: (1) keystone to actually
produce the brief, (2) your one login.

## Image generation — status
DELIVERY works (Telegram + Photos, `deliver-images.sh`). GENERATION is the wall: Grok fetch hangs,
Gemini browser shows 4 images but fetch-grab fails on CORS, xAI out of credits, Gemini CLI dead, ChatGPT
not logged in (debug Chrome). Next: screenshot-grab the visible Gemini images (bypasses CORS), or $5 xAI.

## To avoid future mess
- Dispatch = `@<agent> <task>` in the message text.
- keystone outputs are unverified — don't assume a dispatched build is done until a file/result confirms it.

## Jade (GLM Cell) — added 2026-06-27, named by Fable
- **Name/brain:** GLM-5.2 via Cloudflare Workers AI (free tier, 10k neurons/day)
- **Role:** cheap-capable workhorse — research, summaries, routine code (the 80%); escalate hard 20% to Fable/Opus
- **Caller:** `~/agent-bridge/bin/ask-glm.sh "<prompt>"`
- **Governance:** routes through mitmproxy (127.0.0.1:8081 → central ledger + redaction); killswitch via `~/agent-comms/KILLSWITCH`; usage logged to `~/health-data/glm-usage.log` (run `glm-usage`)
- **Cost:** $0 (free tier). 2nd Cloudflare account would double the daily allowance.

## z.ai cell (added 2026-06-28) — 2nd free GLM source
- **Brain:** glm-4.7-flash (203K context, free) via z.ai · key in ~/.config/secrets/zai.env
- **Caller:** `~/agent-bridge/bin/ask-zai.sh` · mitmproxy-routed · killswitch · usage `~/health-data/zai-usage.log`
- **Free:** Flash models free forever + up to 3M GLM-5.2 tokens/day (eligible). Paid models (glm-4.6) need recharge — skip.
- **Note:** Flash is a reasoning model — use max_tokens >=1000 so it has room after thinking.
