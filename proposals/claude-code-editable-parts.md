# Claude Code — every editable part (what we can change)

## System prompt / personality
- `--append-system-prompt-file <f>` / `--append-system-prompt "..."` — APPENDS to the base prompt.
  This is how Fable's soul is injected (the pliny/distilled file). Can't replace the base, only add.
- `~/.claude/CLAUDE.md` (global memory) — loaded every session. We put the distilled Fable soul here →
  applies to ALL sessions incl. the desktop app's Claude Code mode.
- project `CLAUDE.md` — per-repo instructions.

## settings.json (~/.claude/settings.json)
- **hooks** — PreToolUse (this runs rtk!), PostToolUse, Stop, SubagentStop, Notification, UserPromptSubmit.
  The harness runs these, so "always do X" automations live here.
- **permissions** — allow/deny tool calls (cut prompt fatigue).
- **env** — env vars. **model**, **cleanupPeriodDays** (we set 999999 = never delete sessions).

## Capabilities
- **skills** (`~/.claude/skills/`) — reusable procedures.
- **subagents** (custom agent types) — fan-out workers.
- **MCP servers** (`~/.claude.json`) — connectors (we wired prediction-markets here).
- **slash commands**, **output styles**, **statusline**, **keybindings**.
- **/schedule** — cloud cron routines (run even when the mac is off). **/loop** — recurring local runs.

## Per-run knobs
- model (opus/sonnet/haiku), effort (low→max), permission-mode (acceptEdits/plan/etc.), --resume.

## Claude DESKTOP app — what's editable there
- ✅ Custom instructions / Personalization (Settings) — steers tone/behavior (NOT a full system prompt).
- ✅ Projects with custom instructions. ✅ Connectors (Gmail/Drive/Slack/Wolfram) via UI, not config files.
- ❌ Can't inject a raw system prompt like the CLI's --append-system-prompt.
- ✅ BUT the desktop's *Claude Code mode* reads the global ~/.claude/CLAUDE.md + settings.json — so it
  already inherits the Fable soul + rtk we wired. The CHAT side uses Anthropic's prompt + your custom instructions.
