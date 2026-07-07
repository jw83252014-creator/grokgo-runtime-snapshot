#!/bin/bash
# Auto-backup grokgo + sibling repos to GitHub. Commits any changes and pushes.
# Run on a schedule (launchd) or call manually. Safe: only commits if there are changes.
# GitHub-backed repos only. agent-bridge is intentionally EXCLUDED: it holds tokens/secrets and
# must not be pushed to a code host without a secret scrub — it's covered by local git commits +
# the offline thinkpad backup instead.
REPOS=(
  "$HOME/grokgo"
  "$HOME/OpenGoldSDR"
  "$HOME/the-device-site"
)
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
for repo in "${REPOS[@]}"; do
  [ -d "$repo/.git" ] || continue
  cd "$repo" || continue
  [ -z "$(git status --porcelain)" ] && continue
  branch=$(git rev-parse --abbrev-ref HEAD)
  git -c user.name="Jeff Whiting" -c user.email="nullaxiom0@gmail.com" add -A
  git -c user.name="Jeff Whiting" -c user.email="nullaxiom0@gmail.com" commit -q -m "Auto-backup $TS

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
  git push -q origin "$branch" 2>/dev/null \
    && echo "[$TS] $(basename "$repo") pushed" \
    || echo "[$TS] $(basename "$repo") commit ok, push failed (offline?)"
done

# independent local mirror (a single remote is not a backup) + one-way Obsidian projection
bash "$HOME/grokgo/bin/backup-mirror.sh" >/dev/null 2>&1
python3 "$HOME/grokgo/bin/obsidian-mirror.py" >/dev/null 2>&1
