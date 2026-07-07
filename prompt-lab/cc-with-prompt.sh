#!/usr/bin/env bash
# Launch a Claude Code session with a custom prompt APPENDED — opt-in, does not touch
# your normal `claude` config. This is the safe "hot rod": your default Claude Code stays
# untouched; only sessions launched through this script get the extra prompt.
#
# Usage:
#   cc-with-prompt.sh distilled   [extra claude args...]   # recommended: lean CC-tuned prompt
#   cc-with-prompt.sh full        [extra claude args...]   # the raw 1585-line Pliny Fable-5 prompt
#   cc-with-prompt.sh /path/to/any-prompt.md [args...]     # any prompt file you want
set -euo pipefail
LAB="$HOME/grokgo/prompt-lab"
case "${1:-distilled}" in
  distilled) FILE="$LAB/prompts/fable5-distilled-for-claude-code.md" ;;
  full)      FILE="$LAB/prompts/reference/CLAUDE-FABLE-5-pliny.md" ;;
  *)         FILE="$1" ;;
esac
shift || true
[ -f "$FILE" ] || { echo "prompt file not found: $FILE"; exit 1; }
# Fable 5 is currently unavailable on this account (Anthropic: "use Opus 4.8"),
# so default the engine to Opus 4.8. Override with CC_MODEL=... if Fable returns.
MODEL="${CC_MODEL:-claude-opus-4-8}"
echo "Launching Claude Code with appended prompt:"
echo "  $FILE  ($(wc -l < "$FILE") lines)  ·  model: $MODEL"
echo "Your normal 'claude' is unchanged. Ctrl-C / /exit to leave."
echo
exec claude --model "$MODEL" --append-system-prompt-file "$FILE" "$@"
