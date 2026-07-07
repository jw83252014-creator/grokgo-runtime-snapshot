#!/usr/bin/env bash
set -euo pipefail

ROOT="${GROKGO_ROOT:-$HOME/grokgo}"
LAB="$ROOT/prompt-lab"
PROMPT_FILE="${1:-$LAB/prompts/user-fable-style.md}"
INPUT_FILE="${2:-$LAB/test-input.md}"
RESULT_DIR="$LAB/results"

mkdir -p "$RESULT_DIR"

if [[ ! -f "$PROMPT_FILE" ]]; then
  echo "Prompt file missing: $PROMPT_FILE"
  exit 1
fi

if [[ ! -f "$INPUT_FILE" ]]; then
  echo "Input file missing: $INPUT_FILE"
  exit 1
fi

stamp="$(date +%Y%m%d-%H%M%S)"
out="$RESULT_DIR/prompt-test-$stamp.md"

echo "Prompt file:"
echo "  $PROMPT_FILE"
echo
echo "Test input:"
echo "  $INPUT_FILE"
echo
echo "Result will save to:"
echo "  $out"
echo
echo "This will send the prompt file and test input to Claude through normal Claude Code."
echo "Type RUN to continue."
read -r answer

if [[ "$answer" != "RUN" ]]; then
  echo "Stopped. Nothing sent."
  exit 0
fi

{
  echo "# Prompt Test $stamp"
  echo
  echo "Prompt file: \`$PROMPT_FILE\`"
  echo "Input file: \`$INPUT_FILE\`"
  echo
  echo "## Output"
  echo
  claude -p \
    --append-system-prompt-file "$PROMPT_FILE" \
    --max-turns 1 \
    "$(cat "$INPUT_FILE")"
} | tee "$out"

echo
echo "Saved:"
echo "$out"
