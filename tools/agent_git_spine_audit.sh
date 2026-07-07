#!/usr/bin/env bash
set -euo pipefail

mode="${1:---check}"

safe_roots=(
  "$HOME/grokgo"
  "$HOME/grok-go-organism-share"
  "$HOME/agent-bridge"
  "$HOME/null-command-center"
  "$HOME/badass-fable"
  "$HOME/mining-engine"
  "$HOME/the-device-site"
  "$HOME/command-center"
)

runtime_roots=(
  "$HOME/agent-comms"
)

ensure_ignore() {
  local root="$1"
  local name
  name="$(basename "$root")"

  if [[ -f "$root/.gitignore" ]]; then
    return 0
  fi

  case "$name" in
    command-center)
      cat > "$root/.gitignore" <<'EOF'
.DS_Store
.env
*.env
logs/
daily-log/
downloads-watch/
capture-inbox/
inbox/
outbox/
*.log
EOF
      ;;
    *)
      cat > "$root/.gitignore" <<'EOF'
.DS_Store
.env
*.env
node_modules/
.vercel/
*.log
EOF
      ;;
  esac
}

check_root() {
  local root="$1"
  local kind="$2"

  if [[ ! -d "$root" ]]; then
    printf "missing\t%s\t%s\n" "$kind" "$root"
    return 0
  fi

  if git -C "$root" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    local branch
    branch="$(git -C "$root" branch --show-current 2>/dev/null || true)"
    printf "repo\t%s\t%s\t%s\n" "$kind" "$root" "${branch:-detached-or-none}"
    return 0
  fi

  printf "no-git\t%s\t%s\n" "$kind" "$root"

  if [[ "$mode" == "--init" && "$kind" == "safe" ]]; then
    ensure_ignore "$root"
    git -C "$root" init >/dev/null
    printf "initialized\t%s\t%s\n" "$kind" "$root"
  fi
}

for root in "${safe_roots[@]}"; do
  check_root "$root" safe
done

for root in "${runtime_roots[@]}"; do
  check_root "$root" runtime-audit-only
done

if [[ "$mode" == "--init-runtime" ]]; then
  printf "runtime-init-disabled\tmanual review required before initializing runtime roots\n"
fi
