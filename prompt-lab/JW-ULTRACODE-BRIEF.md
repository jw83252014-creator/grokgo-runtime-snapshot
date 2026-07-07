# JW (Fable-JW) — ultracode work brief

You are running on the **jw83252014** Claude Pro account (fresh quota — null is capped until ~1:20pm PT).
Full Fable config: distilled soul prompt + skip-permissions. Work autonomously, ultracode the list.

## Hard guardrails (do not cross)
- **Draft only.** No public posting, no X/social actions, no spend, no account changes, no logins.
- No live mitmproxy / token capture. No mass-follow / automated engagement.
- Save every deliverable to **disk** (paths below) and reference the path — don't leave work only in chat.
- Terse progress notes for Jeff: did this / found / next.

## Primary list — `~/grokgo/prompt-lab/FABLE-TASKS.md` (work top to bottom)
1. Review the Grok Go router/mining code (`~/grokgo/dispatch.py, brakes.py, bus.py, mining_pipeline.py,
   load_anchors.py, review_queue.py`, `routing.yaml`, `directives/`). Note strengths + concrete improvements.
2. Check Polymarket/Kalshi research (`~/agent-comms/workers/scripts/kalshi-monitor.py`,
   `~/agent-comms/workers/projects/frankenstein-poly/`, `~/.openclaw/workspace/polymarket-bot/`).
   Summarize what it does + one concrete improvement.
3. Before/after on prompt work: `prompts/reference/CLAUDE-FABLE-5-pliny.md` vs
   `prompts/fable5-distilled-for-claude-code.md`; the leaked-prompt repo is `CL4R1T4S/` (Opus 4.7 at
   `CL4R1T4S/ANTHROPIC/Claude-Opus-4.7.txt`).
4. **Draft a lean Codex prompt + a lean Grok prompt** for our agent lanes (distill useful patterns from the
   *leaked system prompts* in `CL4R1T4S/OPENAI/Codex.md` and `CL4R1T4S/XAI/` — transparency material, NOT
   jailbreaks). Save to `prompts/codex-distilled.md` and `prompts/grok-distilled.md`.
5. Read shared brain: `~/grokgo-context/SHARED.md`, `~/grokgo/prompt-lab/FABLE-ONBOARDING.md`.

## Secondary — pull READ-ONLY / DRAFT-ONLY items from `~/agent-comms/tasks.md` as bandwidth allows
Good candidates (skip anything tagged `jeff`/needs-approval/needs-login):
- Daily GitHub progress review design (repo-review script: branch, dirty state, divergence, next action).
- Mining Engine daily research loop design (inputs, source notes, digest format).
- Defensive-security hardening note (owned systems only; produce one hardening note).
Leave a one-line note in this file under "## Log" for each item you touch.

## Log
(append terse entries here as you go)
