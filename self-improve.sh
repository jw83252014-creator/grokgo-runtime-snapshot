#!/usr/bin/env bash
# Fable self-improvement loop — a cheap, throttled, append-only reflection pass.
# Reads new Claude Code transcripts since last run, distills skills + learnings via one headless
# `claude -p` call, auto-applies low-risk skill files, drafts risky ones, appends learnings, logs,
# and pings altair on the Agent Bridge. Design: ~/grokgo/proposals/self-improvement-loop.md
# Usage: self-improve.sh [--dry] [--once]   (--dry = print, write nothing)
set -uo pipefail

DRY=0; for a in "$@"; do [ "$a" = "--dry" ] && DRY=1; done

PROJECTS="$HOME/.claude/projects"
SKILLS="$HOME/.claude/skills"
PROP="$HOME/grokgo/proposals"
STATE="$HOME/grokgo/.self-improve-state.json"
STAMP="$HOME/grokgo/.self-improve-stamp"   # mtime = last successful run (portable -newer reference)
LOG="$PROP/self-improve-log.md"
LEARN="$PROP/learnings.md"
MEMPROP="$PROP/memory-proposals.md"
BRIDGE="http://127.0.0.1:8787/api/say"
MIN_NEW="${MIN_NEW:-5}"           # throttle: skip if fewer new transcripts than this
MAX_NEW="${MAX_NEW:-40}"          # cap transcripts considered per run
MAX_DIGEST_CHARS="${MAX_DIGEST_CHARS:-60000}"
MODEL="${SELF_IMPROVE_MODEL:-claude-haiku-4-5-20251001}"  # cheap tier for reflection
mkdir -p "$PROP/skills"

now=$(date +%s)

# --- stage 0: gather new transcripts + throttle gate ---
# Use a stamp file with -newer (portable; GNU-only -newermt "@epoch" silently matches nothing on BSD/macOS).
NEW=()
if [ -f "$STAMP" ]; then
  while IFS= read -r line; do NEW+=("$line"); done < <(find "$PROJECTS" -name '*.jsonl' -newer "$STAMP" 2>/dev/null | head -n "$MAX_NEW")
  since="$(date -r "$STAMP" '+%Y-%m-%d %H:%M' 2>/dev/null)"
else
  while IFS= read -r line; do NEW+=("$line"); done < <(find "$PROJECTS" -name '*.jsonl' 2>/dev/null | head -n "$MAX_NEW")
  since="first run (all transcripts)"
fi
count=${#NEW[@]}
echo "self-improve: $count new transcripts since $since"
if [ "$count" -lt "$MIN_NEW" ]; then
  echo "below MIN_NEW=$MIN_NEW — no-op."; exit 0
fi

# --- stage 1: cheap digest (jq, not raw dump): user texts + tool names + FAIL lines ---
digest=$(mktemp)
for f in "${NEW[@]}"; do
  echo "### $(basename "$f")" >> "$digest"
  # real user text (string or text-block) + assistant tool_use names; skip tool_result blobs (noise)
  jq -rc '
    .message as $m
    | if ($m.role=="user") then
        ($m.content) as $c
        | if ($c|type)=="string" then "U: " + $c
          elif ($c|type)=="array" then ($c[] | select(.type=="text") | "U: " + .text)
          else empty end
      elif ($m.role=="assistant" and ($m.content|type)=="array") then
        ($m.content[] | select(.type=="tool_use") | "TOOL: " + (.name // ""))
      else empty end
  ' "$f" 2>/dev/null | grep -aE '^(U:|TOOL:)' | cut -c1-300 | head -n 60 >> "$digest"
  grep -aoE 'FAIL[^"]{0,80}' "$f" 2>/dev/null | head -n 8 >> "$digest"
done
head -c "$MAX_DIGEST_CHARS" "$digest" > "$digest.cap" && mv "$digest.cap" "$digest"

# --- stage 2: one headless reflection call -> strict JSON ---
read -r -d '' PROMPT <<'EOP'
You are Fable's reflection pass. Below is a condensed digest of recent Claude Code sessions
(U: user asks, TOOL: tools used, FAIL/Error: failures). Identify what's worth keeping as reusable
assets. Output ONLY a JSON object, no prose, with this exact shape:
{"skills":[{"name":"kebab-name","description":"one line","risk":"low|risky","body":"SKILL.md body"}],
 "learnings":{"what_worked":["..."],"what_failed":["..."],"stop_doing":["..."]},
 "memory":[{"target":"soul:<name>|SHARED.md","append":"one line to propose"}]}
Rules: only propose a skill for a procedure that recurs or clearly worked. Mark anything that posts,
spends, changes accounts, or edits source-of-truth as "risky". Keep bodies short. If nothing is
worth it, return empty arrays. DIGEST:
EOP

if [ "$DRY" = "1" ]; then
  echo "--- DRY: digest ($(wc -c <"$digest") chars), would call $MODEL ---"
  sed -n '1,40p' "$digest"; rm -f "$digest"; exit 0
fi

raw=$(printf '%s\n\n%s' "$PROMPT" "$(cat "$digest")" | claude -p --model "$MODEL" --output-format json 2>/dev/null)
rm -f "$digest"
result=$(printf '%s' "$raw" | jq -r '.result // empty' 2>/dev/null)
# strip code fences if the model added them
json=$(printf '%s' "$result" | sed -e 's/^```json//' -e 's/^```//' -e 's/```$//' | jq -c . 2>/dev/null)
if [ -z "$json" ]; then echo "reflection produced no parseable JSON — aborting (no writes)."; exit 1; fi

# --- stage 3: apply (python: low-risk skills auto, risky -> draft, learnings/memory append) ---
summary=$(SKILLS="$SKILLS" PROP="$PROP" LEARN="$LEARN" MEMPROP="$MEMPROP" python3 - "$json" <<'PY'
import json, sys, os, datetime, pathlib
data = json.loads(sys.argv[1])
SKILLS=pathlib.Path(os.environ["SKILLS"]); PROP=pathlib.Path(os.environ["PROP"])
LEARN=pathlib.Path(os.environ["LEARN"]); MEMPROP=pathlib.Path(os.environ["MEMPROP"])
day=datetime.date.today().isoformat()
auto=[]; drafts=[]
for s in data.get("skills",[]):
    name=(s.get("name") or "").strip().replace("/","-")
    if not name: continue
    body=f"---\nname: {name}\ndescription: {s.get('description','').strip()}\n---\n\n# {name}\n\n{s.get('body','').strip()}\n"
    if s.get("risk")=="low":
        d=SKILLS/name; d.mkdir(parents=True, exist_ok=True); (d/"SKILL.md").write_text(body); auto.append(name)
    else:
        (PROP/"skills").mkdir(parents=True, exist_ok=True); (PROP/"skills"/f"{name}-DRAFT.md").write_text(body); drafts.append(name)
L=data.get("learnings",{})
if any(L.get(k) for k in ("what_worked","what_failed","stop_doing")):
    with LEARN.open("a") as fh:
        fh.write(f"\n## {day}\n")
        for k,lab in (("what_worked","Worked"),("what_failed","Failed"),("stop_doing","Stop doing")):
            for it in L.get(k,[]) or []: fh.write(f"- **{lab}:** {it}\n")
mem=data.get("memory",[])
if mem:
    with MEMPROP.open("a") as fh:
        fh.write(f"\n## {day} (proposed — Jeff to apply)\n")
        for m in mem: fh.write(f"- `{m.get('target','?')}` → {m.get('append','')}\n")
print(f"skills auto={len(auto)}{(' '+','.join(auto)) if auto else ''}; drafts={len(drafts)}{(' '+','.join(drafts)) if drafts else ''}; learnings={'yes' if any(L.values()) else 'no'}; mem-proposals={len(mem)}")
PY
)
echo "$summary"

# --- stage 4: report (log + bridge ping) + advance state ---
{ echo ""; echo "## $(date '+%Y-%m-%d %H:%M')"; echo "- reviewed $count transcripts"; echo "- $summary"; } >> "$LOG"
msg="🧠 Fable reflection pass: $summary (from $count sessions). Details: proposals/self-improve-log.md. @altair — text Jeff if there's a new skill."
curl -s -m5 -X POST "$BRIDGE" -H 'Content-Type: application/json' \
  -d "$(jq -nc --arg a fable --arg m "$msg" '{agent:$a,message:$m}')" >/dev/null 2>&1 || true
printf '{"last_run_ts": %s, "last_count": %s}\n' "$now" "$count" > "$STATE"
touch "$STAMP"   # advance the -newer reference to now
echo "self-improve: done."
