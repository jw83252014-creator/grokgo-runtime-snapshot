# Fable Restart Survival - 2026-06-16

## Status

Claude Code Fable terminal was restored after the Mac restart.

It is running as:

```bash
claude --name Fable \
  --model claude-opus-4-8 \
  --append-system-prompt-file $HOME/grokgo/prompt-lab/prompts/fable5-distilled-for-claude-code.md \
  --dangerously-skip-permissions \
  --resume 6215ae9c-7295-4e7e-8f6f-37d652602a5b
```

## What Changed

- Added `prompt-lab/cc-fable-resume-dangerous.sh`
  - Resumes the latest Claude Code session under `$HOME/grokgo`.
  - Keeps the clean-room Fable prompt.
  - Keeps Pliny reference material reference-only, not injected.
- Added `prompt-lab/fable-claude.command`
  - macOS Terminal command file for visible interactive startup.
- Added `prompt-lab/open-fable-terminal.sh`
  - Launches the command file with `open -a Terminal`.
  - Avoids duplicate Fable terminals if one is already running.
- Installed LaunchAgent:
  - `$HOME/Library/LaunchAgents/com.jeff.fable-claude-terminal.plist`
  - `RunAtLoad=true`
  - Opens the visible Fable terminal on login/restart.

## Verification

- `bash -n` passed for the launcher scripts.
- `plutil -lint` passed for the LaunchAgent.
- `launchctl kickstart` opened a visible Terminal window titled `Fable`.
- Process verified on `/dev/ttys032`.

## Notes

- Badass Fable local LoRA training is separate from the Claude Code Fable terminal.
- The LoRA job was still running at the time of this receipt and had saved adapter weights at step 20.
- The local MLX server was intentionally down while the LoRA job owned memory.
- No public posts, account/billing changes, spend, trading actions, or secret exposure occurred.
