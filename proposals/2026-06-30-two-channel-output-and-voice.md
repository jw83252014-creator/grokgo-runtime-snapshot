# Two-channel output (terminal + human) + voice — design note

## The thing Jeff noticed (and it's real)
I am ONE agent (Fable, in a Claude Code terminal). I produce TWO outputs from the same work:
1. **Dense channel** — full terminal log: commands, paths, errors, receipts. For the record + other agents + disk.
2. **Human channel** — a condensed, non-technical iMessage via `send_imsg.sh`. "did this / found / next," ADHD-tight.

It's not magic: after doing the work in the terminal, I deliberately call `send_imsg.sh` with a *rewritten*,
human version. My soul file literally says: "For Jeff: terse, dense, did this/found/next. Save the dense
version for the agents + disk." So the split is a PROMPT-level discipline, not separate software.

## How to bake it into a Hermes harness (the reusable pattern)
Formalize it as a **Narrator Adapter** every cell gets:
- Cell does work → emits a **receipt** (dense, to disk/ledger — null's schema already does this).
- A tiny `narrate(text, channel)` wrapper produces the **human** version and pushes it to the chosen channel
  (iMessage, Telegram, voice). Same content, two registers: machine-precise vs human-warm.
- This is exactly "subconscious (research/receipts) vs conscious (the face you talk to)" from the video —
  the conscious layer IS the narrator adapter. The org already lives this; we just name + reuse it.

## Claude Code harness on GitHub?
The buildable, public thing is the **Claude Agent SDK** (Anthropic) — that's the supported harness to build
Hermes-style agents on. null's clean-room rule stands: mirror PUBLIC CLI/SDK behavior + our own bridge traces,
never leaked Claude Code source. So "mix them" = run our Hermes cells on the Agent SDK + our bridge/narrator.

## Voice: Vercel vs FaceTime vs middle
- **FaceTime + TTS (Apple, local)** — mini calls your iPhone (AppleScript FaceTime audio) + speaks via `say`/better TTS.
  PRO: free, uses the Apple-ID cell we already run, stays on the mini, feels like a real call.
  CON: one-way is easy (it narrates); two-way (you talk back → speech-to-text) is hacky/finicky.
  BEST FOR: "narrate while it runs" — you listen, it talks. Buildable NOW, $0.
- **Vercel Voice Agents (AI SDK 7: useRealtime/generateSpeech/transcribe)** — cloud, realtime, true two-way.
  PRO: production-grade real conversation, low latency, clean STT+TTS.
  CON: paid + cloud (data leaves the mini), another dependency.
  BEST FOR: real back-and-forth voice chat.
- **Twilio-style call API** — robust phone calls, but paid + cloud.

## Recommendation
Phase 1 (now, free): FaceTime-audio + TTS, ONE-WAY narrator — the mini calls you and talks status while work runs.
Phase 2: add two-way via Vercel Voice Agents (or a realtime API) when you want to actually converse by voice.
Both ride the same Narrator Adapter — voice is just another channel.
