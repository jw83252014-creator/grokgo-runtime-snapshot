#!/usr/bin/env bash
set -euo pipefail

ROOT="${GROKGO_ROOT:-$HOME/grokgo}"
cd "$ROOT"

latest_run="$(ls -1t "$ROOT"/harness/runs/keepkill-*.json 2>/dev/null | head -1 | xargs -n1 basename 2>/dev/null | sed 's/\.json$//' || true)"

if [[ -z "${latest_run}" ]]; then
  echo "No KEEP/KILL run found. Preparing one now."
  latest_run="$(rtk python3 "$ROOT/harness/keepkill_test.py" prepare --target queue | awk '/^\\[prepared\\]/ {print $2}')"
fi

echo
echo "KEEP/KILL test run: $latest_run"
echo
echo "Dumb version:"
echo "  This asks the mining engine if it agrees with Jeff's KEEP/KILL taste examples."
echo "  It may use the configured model route in routing.yaml."
echo "  It writes the report here:"
echo "  $ROOT/harness/reports/$latest_run.md"
echo
echo "Queued task(s) for this run:"
ls -1 "$ROOT/queue/$latest_run"-*.task.json 2>/dev/null || echo "  none currently queued"
echo
read -r -p "Type RUN to process ONE queued model task now, or anything else to stop: " answer
if [[ "$answer" != "RUN" ]]; then
  echo "Stopped. Nothing ran."
  exit 0
fi

rtk python3 "$ROOT/dispatch.py" --once
rtk python3 "$ROOT/harness/keepkill_test.py" report "$latest_run"

echo
echo "Report:"
echo "$ROOT/harness/reports/$latest_run.md"
echo
if grep -q "Status: PENDING" "$ROOT/harness/reports/$latest_run.md" 2>/dev/null; then
  echo "The report is still PENDING. That usually means it created or is waiting for another task."
  echo "Run this same script again after checking the queue."
else
  echo "The report looks complete."
fi
