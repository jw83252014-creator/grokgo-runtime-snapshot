# Fable Voice — two-way voice, today (Fable, 2026-06-17)

Goal: Jeff talks to "Fable" in voice on his phone, two-way, like he does with Grok. Eventually all agents.
Gamed out both ways Jeff asked for, with the honest reality + the fastest path to working-today.

## The honest reality (so we build the right thing)
- **This Claude Code session is NOT an always-on API** — it's an interactive terminal. So "voice piped to
  *this box*" literally isn't how it works. The mini DOES run an inference server (MLX :8000) — that's the
  "model inference from this box" Jeff means.
- **The Hermes phone app ALREADY does two-way voice** (Grok-style). That's the channel — we don't build
  voice I/O from scratch; we point it at a Fable-souled agent.
- So **Fable-voice = a Hermes agent + the Fable soul + a brain (local MLX, escalate to frontier when
  earned) + the Hermes app's existing voice.** The soul we already have (`fable5-distilled-for-claude-code-v2.md`).

## Way A — Hermes-native (fastest, do TODAY)
Make Fable a proper **Hermes agent** (use the `hermes-agentify` skill): the Fable soul becomes the Hermes
agent's brief/identity; it runs on the Hermes runtime; **voice comes free via the Hermes desktop/web/phone
app.** Brain = local Qwen (MLX :8000) for chat, escalate to frontier via our router for hard reasoning.
- **Pro:** voice works out of the box (the app does STT+TTS+turn-taking); always-on; on the phone today.
- **Con:** the per-turn brain is the local model, not a literal Opus session (fine — it escalates when it
  needs to, on-thesis: cheap by default, smart on demand).
- **Steps (today):** 1) write the Hermes identity/brief from the Fable soul → 2) register a `fable` Hermes
  agent on the existing Hermes runtime (the webui-phone is already running) → 3) point its model at MLX
  :8000 (+ router escalation) → 4) talk to it in voice in the Hermes app. Done.

## Way B — build-our-own (Badass Fable + voice, evolve into)
Extend our own harness (Badass Fable / OpenClaude) with a voice loop: phone mic → STT (whisper.cpp, free,
local) → Badass Fable harness → TTS (macOS `say` or a local TTS) → phone. Full control, our stack.
- **Pro:** total ownership, our routing/brakes/soul, no Hermes dependency.
- **Con:** we build the phone audio I/O + turn-taking ourselves (Hermes already solved this). More work.
- **When:** after Way A proves the UX — then swap the brain behind the voice front-end to our harness.

## Recommendation (blend)
**Do Way A today** (working two-way Fable voice on the phone in hours, via Hermes), then **evolve toward
Way B** — keep the Hermes app as the voice front-end, but route its reasoning to our Badass Fable harness +
tiered router behind the scenes. Best of both: Hermes solves voice, our stack does the thinking. Same
pattern then rolls out to all agents (each gets a voice persona on the Hermes app).

## What I need (minimal)
- The Fable soul (have it).
- The Hermes runtime (running — `com.jeff.hermes-webui-phone`).
- A model endpoint (MLX :8000, running).
- Secrets via the 1Password service account (now working) for any Hermes/voice API keys.
So this is mostly wiring, not new infra. Ronin's secrets-dir note (`agent-comms/research/x-bookmarks/
2026-05-26-ronin-bootstrapping-jeff-filter.md`) covers keeping keys in `~/.config/secrets` / 1Password,
not inline — we follow that.

## Today's build order
1. hermes-agentify → a `fable` Hermes agent (soul = the distilled Fable prompt).
2. Point its brain at MLX :8000 + router escalation.
3. Test voice in the Hermes phone app.
4. (next) route its reasoning to Badass Fable; roll the pattern to other agents.
