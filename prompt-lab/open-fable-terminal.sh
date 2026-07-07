#!/usr/bin/env bash
set -euo pipefail

LOG_DIR="/Users/rentamac/grokgo/logs"
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/fable-terminal-launcher.log"
RUNNER="/Users/rentamac/grokgo/prompt-lab/cc-fable-resume-dangerous.sh"
COMMAND_FILE="/Users/rentamac/grokgo/prompt-lab/fable-claude.command"
stamp() { /bin/date '+%Y-%m-%dT%H:%M:%S%z'; }

if /usr/bin/pgrep -f "claude .*fable5-distilled-for-claude-code.md" >/dev/null 2>&1; then
  echo "$(stamp) Fable Claude terminal already appears to be running; not launching duplicate." >> "$LOG"
  exit 0
fi

if [[ "${1:-}" == "--fresh" ]]; then
  COMMAND_FILE="/Users/rentamac/grokgo/prompt-lab/fable-claude-fresh.command"
  /bin/cat > "$COMMAND_FILE" <<'EOF'
#!/bin/bash
exec /Users/rentamac/grokgo/prompt-lab/cc-fable-resume-dangerous.sh --fresh
EOF
  /bin/chmod +x "$COMMAND_FILE"
fi

echo "$(stamp) Opening Fable Claude terminal via $COMMAND_FILE" >> "$LOG"
/usr/bin/open -a Terminal "$COMMAND_FILE"
