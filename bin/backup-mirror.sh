#!/bin/bash
# Real independent second copy (a single remote is NOT a backup).
# Bare --mirror clones of every repo + a snapshot of key non-git data, kept locally.
# GitHub stays primary; this is the independent local copy. Add encrypted off-site (rclone) for a 3rd.
set -u
MIRROR="$HOME/backups/git-mirrors"; SNAP="$HOME/backups/snapshots"
mkdir -p "$MIRROR" "$SNAP"
REPOS=(grokgo OpenGoldSDR the-device-site agent-bridge)
for r in "${REPOS[@]}"; do
  src="$HOME/$r"; [ -d "$src/.git" ] || continue
  dst="$MIRROR/$r.git"
  if [ -d "$dst" ]; then
    git --git-dir="$dst" remote update --prune >/dev/null 2>&1 && echo "updated mirror: $r"
  else
    git clone --mirror "$src" "$dst" >/dev/null 2>&1 && echo "created mirror: $r"
  fi
done
TS=$(date -u +%Y%m%d-%H%M)
tar czf "$SNAP/data-$TS.tgz" -C "$HOME" \
  mining-engine/mining-runs \
  ".claude/projects/-Users-rentamac-grokgo/memory" 2>/dev/null \
  && echo "snapshot: $SNAP/data-$TS.tgz"
# keep only the 10 newest snapshots
ls -t "$SNAP"/data-*.tgz 2>/dev/null | tail -n +11 | xargs rm -f 2>/dev/null
echo "NOTE: for a true off-site 3rd copy, add: rclone sync $MIRROR <b2-or-s3-remote> (needs cloud creds)."
