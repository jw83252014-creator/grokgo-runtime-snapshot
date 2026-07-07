#!/bin/bash
# Offline/external-drive backup of the whole operation. Plug in a drive, run this.
# Mirrors the valuable dirs to <external volume>/grokgo-backup-<date>/. Air-gapped-friendly.
set -e
DEST_BASE=""
for v in /Volumes/*; do
  [ "$v" = "/Volumes/Macintosh HD" ] && continue
  [ -d "$v" ] && [ -w "$v" ] && DEST_BASE="$v" && break
done
if [ -z "$DEST_BASE" ]; then echo "No external drive found in /Volumes. Plug one in, then re-run."; exit 1; fi
DEST="$DEST_BASE/grokgo-backup-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$DEST"
echo "Backing up to $DEST ..."
# the valuable stuff (incl. secrets — safe on an OFFLINE drive, never commit these to git)
for d in "$HOME/grokgo" "$HOME/the-device-site" "$HOME/mining-engine" "$HOME/agent-comms" \
         "$HOME/grok-go-organism-share" "$HOME/The-Device/production" "$HOME/Pictures/Grok-Go-Visuals" \
         "$HOME/.config/secrets" "$HOME/.hermes-null" "$HOME/Downloads/twitter-2026-06-17-"*.zip; do
  [ -e "$d" ] && rsync -a --exclude 'node_modules' --exclude '.git/objects' --exclude 'spikes/headroom' "$d" "$DEST/" 2>/dev/null && echo "  ✓ $(basename "$d")"
done
echo "DONE. Offline backup at: $DEST"
echo "(Unplug the drive after — that's your air-gapped copy.)"
