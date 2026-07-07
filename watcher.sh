#!/usr/bin/env bash
# grokgo watcher — deterministic, ZERO model calls, ever.
# Watches inbox/ for *.task.json, debounces write bursts, header-checks with jq,
# moves valid tasks to queue/. Malformed files get renamed, never silently dropped
# and never sent to a model to "fix".
set -euo pipefail

ROOT="${GROKGO_ROOT:-$HOME/grokgo}"
INBOX="$ROOT/inbox"; QUEUE="$ROOT/queue"
DEBOUNCE="${DEBOUNCE_SECS:-4}"
mkdir -p "$INBOX" "$QUEUE"

enqueue_ready() {
  # Only move files that have settled (mtime older than the debounce window)
  find "$INBOX" -maxdepth 1 -name '*.task.json' -type f \
       -not -newermt "-${DEBOUNCE} seconds" 2>/dev/null | while read -r f; do
    if jq -e '.type and .id' "$f" >/dev/null 2>&1; then
      mv "$f" "$QUEUE/"
    else
      mv "$f" "${f}.malformed"
    fi
  done
}

if command -v fswatch >/dev/null 2>&1; then
  # macOS (brew install fswatch) — event-driven, latency = built-in debounce
  fswatch -o --latency "$DEBOUNCE" "$INBOX" | while read -r _; do enqueue_ready; done
elif command -v inotifywait >/dev/null 2>&1; then
  # Linux (apt install inotify-tools)
  while inotifywait -qq -e close_write,moved_to "$INBOX"; do
    sleep "$DEBOUNCE"; enqueue_ready
  done
else
  # proot/Termux fallback: inotify can be flaky in proot. An mtime poll costs
  # zero tokens — polling was only ever bad because a MODEL was doing it.
  while true; do enqueue_ready; sleep 30; done
fi
