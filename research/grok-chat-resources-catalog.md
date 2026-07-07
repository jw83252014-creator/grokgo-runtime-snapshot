# Grok-chat resource catalog (from Right-Agent-Telegram-Bridge.md)

*Extracted 2026-06-18 from the grok export. Deduped, grouped most-useful-first. Companion to
[github-finds-harness-notebooklm.md] (which covers the harness/NotebookLM subset).*

## 1. Multi-agent / bridge / orchestration — the app blueprint
- **right-agent** ⭐ — `github.com/onsails/right-agent` — Rust; turns **Telegram into a secure command
  center for multiple sandboxed Claude agents** (identity files, cron, isolation). The chat says "model
  it after this." → reference architecture for the phone-chat-with-agents app.
- **agentcookie** — `github.com/mvanhorn/agentcookie` — one-way syncs auth (cookies/tokens/keys) to a
  remote agent machine. Solves credential delivery for a distributed bridge.
- **Shannon** — `github.com/Kocoro-lab/Shannon` — multi-agent orchestration.
- **Hermes Agent** — `github.com/NousResearch/hermes-agent` (docs: hermes-agent.nousresearch.com) — the
  off-browser always-on agent framework already central to the org.

## 2. App / UI building (multi-agent chat app)
- **ccpocket** — `github.com/K9i-0/ccpocket` — mobile pocket client for Claude Code. Study before building.
- **browser-harness** — `github.com/browser-use/browser-harness` — better base than Tampermonkey for a
  browser-driving dashboard.
- **Termius + Tailscale** — SSH-from-phone over the private mesh (tailnet already in use). Tailscale
  Aperture CLI blog is AI-experimentation-over-tailnet.
- **Vercel** — `grok-go.vercel.app`, `aiventix.vercel.app` — existing web deploy targets.
- **Native iOS** — needs Mac + Xcode + iOS Simulator (fast on M-series). No starter repo named — scaffold fresh.

## 3. Local models / inference / token-savings
- **Headroom** — `github.com/chopratejas/headroom` — run a local model below capacity so an agent can loop.
- **llmfit** — `github.com/AlexsJones/llmfit` — quantize/prune LLMs to fit constrained Macs.
- **LEANN** — `github.com/StarTrail-org/LEANN` — storage-efficient vector index (Mining Engine memory).
- **Zvec** — `github.com/alibaba/zvec` — embedded in-process vector DB (no server).
- **GLM-5.2** — `huggingface.co/zai-org/GLM-5.2` (z.ai) — **MIT open weights ≈ Opus 4.8** on coding/agentic;
  too big for the Mini (753B MoE) → cloud-host (RunPod 8×H100, per the chat).
- **freemodel.dev** / **OpenRouter** (`openrouter.ai/api/v1`) — route the official Claude Code CLI / mining
  loop through cheaper keys. Vet ToS before trusting.
- **MLX / vLLM / Unsloth / Ollama / llama.cpp** — the local stack (local endpoints `127.0.0.1:8000/v1`).
- Free credits: NVIDIA build/startups, AWS Activate, OpenAI Startups, Google for Startups.
- **Darkbloom** — `darkbloom.dev` — distributed compute across Apple-Silicon Macs.

## 4. Harness / Claude-Code frameworks & prompts
- **OpenClaude** — `github.com/Gitlawb/openclaude` — open recreation of Claude Code (read/fork the loop).
- **OpenMythos** — `github.com/kyegomez/OpenMythos` — reconstruction of the Claude Mythos/Fable architecture.
- **CL4R1T4S** — `github.com/elder-plinius/CL4R1T4S` → `ANTHROPIC/CLAUDE-FABLE-5.md` — the pliny prompt source
  (reference-only). Official: platform.claude.com prompting-claude-fable-5.
- **fable-5-traces** — `huggingface.co/datasets/glint-research/fable-5-traces` — real agentic traces (gold
  for harness training/eval).
- **knowledge-work-plugins** — `github.com/anthropics/knowledge-work-plugins` — official role-specific plugins.
- **notebooklm-skill** — `github.com/PleasePrompto/notebooklm-skill` — Claude Skill wrapping NotebookLM.
- Skills lists: `ComposioHQ/awesome-claude-skills`, `abubakarsiddik31/claude-skills-collection`.

## 5. Security / sandboxing
- **bubblewrap** — sandboxing primitive for agent isolation (pairs with right-agent's model).
- **Technitium DNS** — `github.com/TechnitiumSoftware/DnsServer` — network-wide blocking.

## 6. Misc
- **Supertonic** — `github.com/supertone-inc/supertonic` — on-device TTS ≈ ElevenLabs (local agent voice).
- **video2x** — `github.com/k4yt3x/video2x` — ML upscaler for the content-video pipeline.
- **x-algorithm** — `github.com/xai-org/x-algorithm` — xAI's open X recommender (Aiventix angle).

**Top 4 for the app:** right-agent (architecture) · agentcookie (creds) · ccpocket (mobile client to study)
· Shannon (orchestration). **Local cheap stack:** Headroom + llmfit + GLM-5.2 + freemodel.dev/OpenRouter.
