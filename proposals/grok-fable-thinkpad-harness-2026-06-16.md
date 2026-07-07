# Grok Fable ThinkPad Harness - 2026-06-16

## Status

Installed a clean-room Fable-style Grok Build harness on Frankenstein's ThinkPad lane.

## What Changed

- Added local source prompt: `~/grokgo/prompt-lab/prompts/grok-fable-harness.md`
- Installed ThinkPad prompt: `~/agent-bridge/prompts/grok-fable-harness.md`
- Added ThinkPad launcher: `~/agent-bridge/scripts/grok-fable`
- Added PATH shortcut: `~/.local/bin/grok-fable`
- Patched ThinkPad headless runner: `~/agent-bridge/scripts/grok-research-task.sh`
- Backed up previous runner under `~/agent-bridge/scripts/backups/`
- Opened a visible XFCE terminal titled `Grok-Fable`

## Grok Flags

The launcher uses Grok Build's supported flags:

```bash
grok --rules "$CLEAN_ROOM_FABLE_RULES" \
  --permission-mode bypassPermissions \
  --always-approve \
  --compaction-mode segments \
  --compaction-detail balanced \
  --todo-gate
```

This mirrors the Claude Fable setup conceptually, but does not copy hidden prompts or provider internals.

## Safety Boundaries

- The harness preserves Jeff approval gates for public posting, spending, account/billing changes, credential changes, trading/financial actions, destructive operations, and irreversible device changes.
- It explicitly forbids hidden prompt reproduction, auth bypass, credential capture, and raw reasoning trace ingestion.
- Reasoning traces should be used only through summaries, rubrics, labels, and evaluation outcomes.

## How To Use

On the ThinkPad:

```bash
grok-fable
```

For one-shot work:

```bash
grok-fable -p "Summarize ~/agent-bridge/outbox/reddit-signals.md and write the next action receipt."
```

For the existing task runner:

```bash
~/agent-bridge/scripts/grok-research-task.sh reddit
```

## Verification

- `bash -n` passed for the launcher and patched research runner.
- `grok-fable inspect --json` accepted the flags on Grok Build `0.2.54`.
- A visible Grok Fable terminal process is running on the ThinkPad.
