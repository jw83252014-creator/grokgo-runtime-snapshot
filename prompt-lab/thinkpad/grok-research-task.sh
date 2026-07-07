#!/usr/bin/env bash
# Run one headless Grok research task (requires grok auth / XAI_API_KEY).
set -euo pipefail
TASK="${1:-reddit}"
LOG=~/agent-bridge/logs/grok-research-$(date +%Y%m%d).log
mkdir -p ~/agent-bridge/logs ~/agent-bridge/outbox
GROK="${GROK:-$HOME/.local/bin/grok}"
RULES_FILE="${GROK_FABLE_RULES:-$HOME/agent-bridge/prompts/grok-fable-harness.md}"

case "$TASK" in
  reddit)
    ~/agent-bridge/scripts/reddit-scout.sh
    PROMPT="Read ~/agent-bridge/outbox/reddit-signals.md. Summarize top 3 actionable +EV or research leads for prediction markets. Under 300 words. Save summary to ~/agent-bridge/outbox/reddit-summary-$(date +%Y%m%d).md"
    ;;
  money)
    PROMPT="Research current Polymarket and Kalshi edges for solo traders June 2026. Focus on free data sources and paper trading. Output markdown to ~/agent-bridge/outbox/money-research-$(date +%Y%m%d).md"
    ;;
  x-article)
    PROMPT="Draft a 400-word X article in Jeff's voice: systems-thinking, Agent Bridge, Frankenstein Moto G watching Polymarket. Direct, not cringe. Write to ~/agent-bridge/outbox/x-article-draft-$(date +%Y%m%d).md"
    ;;
  *)
    echo "Usage: $0 {reddit|money|x-article}"
    exit 1
    ;;
esac

{
  echo "=== $(date '+%Y-%m-%dT%H:%M:%S%z') task=$TASK ==="
  if command -v "$GROK" >/dev/null 2>&1; then
    GROK_ARGS=(
      --cwd "$HOME/agent-bridge"
      --output-format plain
      --permission-mode bypassPermissions
      --always-approve
      --compaction-mode segments
      --compaction-detail balanced
      --todo-gate
    )
    if [ -f "$RULES_FILE" ]; then
      GROK_ARGS+=(--rules "$(cat "$RULES_FILE")")
    else
      echo "warning: Fable rules file not found: $RULES_FILE"
    fi
    "$GROK" -p "$PROMPT" "${GROK_ARGS[@]}" 2>&1 | tail -80
  else
    echo "grok CLI not found; ran local script only"
  fi
} >> "$LOG" 2>&1
echo "Done. Log: $LOG"
