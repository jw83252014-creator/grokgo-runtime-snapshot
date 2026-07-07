#!/usr/bin/env bash
set -euo pipefail

PRINT_ONLY=0
if [[ "${1:-}" == "--print-only" ]]; then
  PRINT_ONLY=1
  shift
fi

CMD=(
  codex exec
  --profile fable-terminal
  --cd $HOME/grokgo/codex-fable-terminal
  --add-dir $HOME/grokgo
  --add-dir $HOME/agent-comms
  --add-dir $HOME/null-command-center
  --dangerously-bypass-approvals-and-sandbox
)

if [[ "$PRINT_ONLY" == "1" ]]; then
  printf '%q ' "${CMD[@]}"
  printf '\n'
  exit 0
fi

exec "${CMD[@]}" "$@"

