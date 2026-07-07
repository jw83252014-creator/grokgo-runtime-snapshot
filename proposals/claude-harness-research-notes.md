# Claude Code Harness — research notes (altair gathers; Fable plans the paper)

Raw material for the research paper + the "banger" X post + the end-to-end chain visual.
Goal: explain, end to end, what happens from your keyboard → what's in the prompt → the wire →
the model → back; every EDITABLE part of the harness; where the Fable prompt slots in + why;
the cost tricks; with code snippets shown in-place. Glossary alongside.

## A. The end-to-end chain (what to diagram)
1. You type in the terminal (Claude Code).
2. The harness ASSEMBLES the request locally:
   - system prompt (base) + **CLAUDE.md / AGENTS.md** (project memory)
   - **appended system prompt** (this is where the Fable soul goes — see C)
   - tool definitions, permissions, conversation history, your message, dynamic sections (date, etc.)
3. Serialized to JSON (Anthropic Messages API shape).
4. Sent over **HTTPS/TLS** to api.anthropic.com with the **OAuth/API token** in the header.
   - (Inspection point: mitmproxy would sit HERE — see the Ronin checklist below. It needs a root CA
     and would see your own token; ToS/ban risk. We diagram it, we don't run it on live traffic.)
5. Anthropic servers run the **model (weights = the actual intelligence)** + server-side safety.
6. Tokens stream back over the same pipe; the harness runs tool calls locally and loops.

## B. EVERY editable part of the harness (the "what you can add" list)
- `~/.claude/settings.json` — **permissions** (allow/deny tools), **model** (`claude-opus-4-8[1m]`),
  **hooks** (PreToolUse/PostToolUse), workflows, theme. (ours has the rtk PreToolUse hook.)
- **CLAUDE.md** (global `~/.claude/CLAUDE.md` + project) — persistent instructions/memory.
- **System prompt flags:** `--system-prompt[-file]` (replace), `--append-system-prompt[-file]` (add),
  `--exclude-dynamic-system-prompt-sections` (strip the dynamic add-ons).
- **Output styles** (`~/.claude/output-styles/`) — behavior presets.
- **Hooks** — shell commands fired on tool events (our rtk token-killer is a PreToolUse Bash hook).
- **MCP servers** — external tools/data (`claude mcp`).
- **Skills** (`~/.claude/skills/<name>/SKILL.md`) — reusable procedures.
- **Subagents** — specialized sub-tasks.
- **Context controls** — compaction, `/clear`, prompt caching, `--model` per session.

## C. Where the Fable prompt slots in (+ the actual snippet)
We make a base model "act like Fable" by APPENDING a soul at the system-prompt layer (step 2), not by
changing weights. The exact command we run (from `~/grokgo/prompt-lab/cc-with-prompt.sh`):
```
claude --model claude-opus-4-8 \
       --append-system-prompt-file ~/grokgo/prompt-lab/prompts/fable5-distilled-for-claude-code.md
```
Why it works: the appended text rides in the system block the model reads first, steering tone/behavior;
the *capability* still comes from the weights. (Full Pliny Fable prompt for reference:
`~/grokgo/prompt-lab/prompts/reference/CLAUDE-FABLE-5-pliny.md`, 1585 lines → our distilled = ~30.)

## D. Cost-cutting tricks we actually use (with the % story)
- **rtk** (Rust Token Killer) — PreToolUse hook rewrites every Bash call, compresses noisy output 60-90%.
- **Prompt distillation** — 1585-line consumer prompt → ~30 lines (~98% cut) keeping the signal.
- **`/clear` when bloated** — we just reset Fable from 337k → fresh (token + speed win).
- **Free-brain routing** — GitHub Models + Gemini for sub-tasks; frontier model only for hard calls.
- **Tiered router + ledger/brakes** (grokgo) — most work never touches a paid API.
- Industry note: "pi" harness ships a <1k-token system prompt vs ~7-10k for Claude Code/Cline/OpenCode.

## E. mitmproxy / inspection (the Ronin checklist)
`~/agent-comms/research/checklists/2026-05-30-null-mitmproxy-claude-oauth-inspection.md` — the existing
write-up on a mitmproxy inspection layer + Claude OAuth routing. Use for the "what actually leaves your
computer / can you inspect it" section. Honest line: client-side flags already let you see/strip the
prompt; MITM on live traffic captures your own token + risks the account.

## F. secrets dir
`~/.secrets/*` = API keys as files outside 1Password (the pattern Jeff remembered). Relevant to the
"production-ready agent" hygiene section.

## G. Open-source context (for the paper)
**OpenCode** (165k★, MIT) = the open-source Claude Code: 75+ providers, Build/Plan subagents, custom
agents via markdown, LSP. OpenHands, Zed, Cline, **pi** (minimal, <1k-token prompt) are alternatives.
Gemini CLI retiring 2026-06-18 for a closed successor. Sources: openalternative.co, builder.io, pinggy.io.

## Null app / production-agent ideas (for the "production agent" framing)
~/agent-comms/vision/Null_App_Feature_Requests_and_Integration_Points.md ·
~/agent-bridge/docs/2026-05-26-null-app-agent-bridge-product-plan.md · ~/Desktop/NULL-App-NotebookLM-Source-Pack.md
