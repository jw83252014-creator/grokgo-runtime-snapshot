# AGENTS.md — High-Volume Parallel Merge & Deploy

> Goal: let many agents merge into `main` and deploy **back-to-back, in quick succession**,
> without the whole fleet getting **blocked for an hour**.
>
> The block is caused by **serialization**: with naive branch protection, every PR must
> rebase on the new `main`, re-run the *full* CI suite, merge, and *then* the next PR can
> start. With N agents and CI time T that is ~N×T, and any mid-chain failure rebuilds
> everything behind it. This file removes the serial chain with three moves:
>
> 1. **Worktree isolation** — agents never collide on the filesystem.
> 2. **A merge queue with speculative parallel checks** — PRs are tested against their
>    *predicted post-merge state* in parallel, not one-at-a-time. Latency collapses back
>    toward a single CI run even at 50+ PRs/day.
> 3. **A single Merge Coordinator + batched deploy** — implementation agents NEVER touch
>    `main`; one coordinator owns the lane, batches deploys, bisects failures, rolls back.

---

## 0. Rules of engagement (read first, every agent)

1. **You work in your own git worktree on your own branch.** Never in the shared checkout.
2. **You NEVER merge to `main`.** You open a PR and label it `ready-to-merge`. The Merge
   Coordinator (or the merge queue) does the landing.
3. **Keep PRs small.** Target 200–400 changed lines. Split large work into stacked PRs.
4. **When your branch is behind, rebase — never merge `main` into your branch.**
5. **If your change is evicted from a merge batch, back off and re-enqueue** (see §7).
6. **Announce intent before you start** so two agents don't pick overlapping files (§8).

---

## 1. Per-agent worktree isolation (exact commands)

Each agent gets a private working directory and branch, sharing one `.git` object store.
This kills file-level clobbering and index-lock contention.

```bash
# One-time, in the repo root:
git config --global rerere.enabled true          # remember conflict resolutions
grep -qxF '.trees/' .gitignore || echo '.trees/' >> .gitignore

# Per agent — pick a unique task slug, e.g. "backend-auth":
TASK="backend-auth"
BRANCH="agent/${TASK}"
WT=".trees/${TASK}"

git fetch origin main
git worktree add "$WT" -b "$BRANCH" origin/main
cd "$WT"
```

### Runtime isolation (worktrees isolate FILES, not ports/DBs/caches)

Worktrees do **not** isolate ports, databases, caches, or `.env`. Derive everything
deterministically from the branch so two agents never share a port or a schema:

```bash
# Deterministic per-agent port (3100–9999) and DB schema from the branch name:
export PORT=$(( 3100 + $(echo "$BRANCH" | cksum | cut -d' ' -f1) % 6899 ))
export DB_SCHEMA="agent_$(echo "$BRANCH" | tr -c 'a-zA-Z0-9' '_')"
cp ../../.env.example .env.local 2>/dev/null || true
printf 'PORT=%s\nDB_SCHEMA=%s\n' "$PORT" "$DB_SCHEMA" >> .env.local
```

For true runtime isolation (parallel e2e, side-effecting tests) run each agent's app in a
container: `docker compose -p "$DB_SCHEMA" up -d`.

### Cleanup (after the PR lands — the Coordinator does this)

```bash
git worktree remove ".trees/${TASK}" --force
git branch -D "agent/${TASK}" 2>/dev/null || true
git worktree prune
```

List/lock worktrees:

```bash
git worktree list --porcelain
git worktree lock --reason 'agent running' ".trees/${TASK}"
```

---

## 2. The merge-coordinator model (who is allowed to touch `main`)

- **Implementation agents** (most of the fleet): write code in a worktree, push a branch,
  open a PR, mark it `ready-to-merge`. **They never run `git push origin main`, never
  click merge, never bypass the queue.**
- **Merge Coordinator** (exactly ONE, a dedicated agent or the GitHub merge queue itself):
  owns the single merge lane. It enqueues ready PRs, lets the queue test the *combined*
  future state, batches the resulting deploy, bisects batch failures, and rolls back.
- `main` is **never locked**. Optimistic model: agents work freely; conflicts are detected
  only at enqueue time and resolved by rebase-and-retry (§6), not by a global lock.

This is why the fleet doesn't stall: the queue tests `main+A`, `main+A+B`, `main+A+B+C`
**in parallel**. If B fails, A still lands immediately and C is retested without B —
instead of everyone waiting behind B for an hour.

### The Coordinator must not be a new single point of failure

"Exactly ONE coordinator" reintroduces the 1-hour block by another door: if it crashes
mid-loop, nothing enqueues, nothing cleans up, and a failed smoke test never rolls back.
Mitigations (all required):

1. **The merge queue, not the agent, is the source of truth for landing.** Once a PR is
   enqueued with `--auto`, it lands on its own even if the coordinator dies. The
   coordinator only *enqueues, bisects-relabels, and cleans up* — none of which is on the
   critical path of an already-enqueued PR.
2. **Lease + takeover.** The coordinator role is a lease, not an identity. Hold it via a
   short-TTL lock so a backup can take over:
   ```bash
   # Acquire/refresh a 5-min lease (atomic create; fails if a fresh lease exists).
   LEASE=$(gh api "repos/${REPO}/issues" --jq '.[]|select(.title=="merge-coordinator-lease")|.number' | head -1)
   now=$(date +%s)
   held=$(gh issue view "$LEASE" --json body --jq '.body' 2>/dev/null | sed -n 's/^until=//p')
   if [ -z "$held" ] || [ "$now" -ge "${held:-0}" ]; then
     gh issue edit "$LEASE" --body "$(printf 'until=%s\nholder=%s' "$(( now + 300 ))" "$AGENT_ID")"
   else
     exit 0   # someone else holds a live lease; I am a standby, do nothing this tick
   fi
   ```
   Any standby agent runs the §11 loop on a timer; only the lease holder acts. If the
   holder dies, the lease expires in ≤5 min and a standby takes over — bounded, not
   open-ended.
3. **Idempotent loop.** Every step in §11 is safe to re-run: `gh pr merge --auto` on an
   already-enqueued PR is a no-op; relabeling is idempotent; cleanup tolerates
   already-deleted branches. A crash mid-loop loses nothing.

---

## 3. GitHub branch protection + merge queue (copy-paste setup)

Run once with admin rights. The merge queue is what converts serial N×T into ~1×T.

> **CRITICAL:** classic `branches/*/protection` has **no field that enables the merge
> queue**. The PUT call below sets protection only. The queue MUST be enabled separately
> via a **ruleset** (`merge_queue` rule) or the UI. If you skip that step you get branch
> protection with *no queue*, which silently re-serializes every merge — the exact block
> this file claims to remove. **Do not let the enable step fail silently** (no `|| true`).

```bash
set -euo pipefail
REPO="OWNER/REPO"   # <-- set this

# Branch protection: require status checks, reviews, no direct pushes, linear history.
gh api -X PUT "repos/${REPO}/branches/main/protection" \
  -H "Accept: application/vnd.github+json" \
  -f 'required_status_checks[strict]=false' \
  -f 'required_status_checks[checks][][context]=pr-checks' \
  -f 'enforce_admins=true' \
  -f 'required_pull_request_reviews[required_approving_review_count]=1' \
  -F 'restrictions=null' \
  -f 'allow_force_pushes=false' \
  -f 'allow_deletions=false' \
  -f 'required_linear_history=true'
```

> Note `required_status_checks[strict]=false`: do **not** require "branch up to date with
> base." Strict mode forces every PR to rebase serially before merge — exactly the block
> we are removing. The merge queue handles rebasing against the predicted state instead.

Now **actually enable the queue** with a ruleset (this is the load-bearing step; it must
not be a no-op). Save as `queue-ruleset.json` and apply:

```jsonc
// queue-ruleset.json
{
  "name": "main-merge-queue",
  "target": "branch",
  "enforcement": "active",
  "conditions": { "ref_name": { "include": ["refs/heads/main"], "exclude": [] } },
  "rules": [
    { "type": "merge_queue",
      "parameters": {
        "merge_method": "SQUASH",
        "max_entries_to_build": 5,        // speculative future-states tested in parallel
        "min_entries_to_merge": 1,
        "max_entries_to_merge": 5,        // BATCH up to 5 PRs into one CI run + one deploy
        "min_entries_to_merge_wait_minutes": 5,   // let PRs accumulate so batching happens
        "grouping_strategy": "ALLGREEN",  // only merge the prefix that is fully green
        "check_response_timeout_minutes": 60
      } }
  ]
}
```

```bash
# Apply and FAIL LOUDLY if the queue is not created. No `|| true`.
gh api -X POST "repos/${REPO}/rulesets" --input queue-ruleset.json

# Verify the queue is actually live before trusting the rest of this file:
gh api "repos/${REPO}/rulesets" --jq \
  '.[] | select(.name=="main-merge-queue") | "queue enabled: \(.enforcement)"' \
  | grep -q 'queue enabled: active' \
  || { echo "FATAL: merge queue not enabled — fix before running any agent"; exit 1; }
```

### CI workflow must listen to the queue's `merge_group` event

Without this trigger the queue can never run checks and every PR hangs.

```yaml
# .github/workflows/pr-checks.yml
name: pr-checks
on:
  pull_request:        # fast feedback on the PR itself
  merge_group:         # REQUIRED: the merge queue tests the combined future state here

concurrency:
  # Cancel stale PR runs (a re-push supersedes the old one). But NEVER cancel a
  # merge_group run: the queue treats a cancelled speculative check as a FAILURE and
  # ejects the PR, which silently re-serializes the queue. So key off the unique
  # gh-readonly-queue ref for merge_group, and only cancel for pull_request.
  group: ${{ github.workflow }}-${{ github.event_name }}-${{ github.ref }}
  cancel-in-progress: ${{ github.event_name == 'pull_request' }}

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        shard: [1, 2, 3, 4]    # test sharding: split the suite so lanes scale with depth
    steps:
      - uses: actions/checkout@v4
      # Flaky-retry HERE, before the status is reported. The merge queue auto-ejects on
      # the first failing status — there is no "retry in place" at the queue level
      # (see §7). The only place to absorb a flake without losing your speculative slot
      # is inside the job, before it reports green/red.
      - run: |
          make ci SHARD=${{ matrix.shard }} SHARDS=4 \
            || make ci SHARD=${{ matrix.shard }} SHARDS=4   # one retry to swallow flakes
```

**Keep the required check list thin and fast.** Only `pr-checks` (above) is required.
Move e2e/perf/security to a *non-required* async workflow so a slow or flaky long job can
never block the queue.

---

## 4. Pre-merge checks (the gate that decides "this is safe to land")

A PR may be enqueued by the Coordinator only when ALL are true:

1. PR has label `ready-to-merge`.
2. `pr-checks` is green on the PR.
3. PR is ≤ ~400 changed lines (or is part of a declared stack).
4. At least 1 approval (human or a designated reviewer agent).
5. No `do-not-merge` / `needs-discussion` label.

```bash
# Coordinator: enqueue every eligible PR (the queue does the combined-state test).
for n in $(gh pr list --label ready-to-merge --json number,labels,reviewDecision \
            --jq '.[] | select(.reviewDecision=="APPROVED") | .number'); do
  gh pr checks "$n" --required --watch --fail-fast >/dev/null 2>&1 \
    && gh pr merge "$n" --squash --auto \
    && echo "enqueued #$n"
done
```

`--auto` + the merge queue means the PR lands only after the *combined* future-state CI
passes. The combined test (A tested together with B) is what catches **semantic
conflicts** — two PRs each green alone but contradictory together.

---

## 5. Batching & deploy (kill the one-deploy-per-merge stall)

The second half of the 1-hour block is **one deploy per merge**. Fix: deploy the **merged
batch once**, not once per PR. Deploy is triggered by the *batch landing*, and a deploy
lock coalesces rapid releases.

```yaml
# .github/workflows/deploy.yml
name: deploy
on:
  push:
    branches: [main]

concurrency:
  group: deploy-main
  cancel-in-progress: false    # don't cancel a live deploy; queue & coalesce the next

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      # Coalesce: if more commits landed while we waited, deploy the latest tip once.
      - run: git fetch origin main && git reset --hard origin/main
      # RECORD EXACTLY WHAT WE DEPLOY. Coalescing means the deployed tip may contain
      # commits from MORE than one queue batch (a later batch landed while we waited).
      # Rollback (§10) MUST target this exact tip and its exact predecessor, not "the bad
      # batch's merge commit" — with squash + linear history there IS no enclosing merge
      # commit, and the deploy unit != the merge-batch unit. So we tag the deployed range.
      - run: |
          DEPLOYED=$(git rev-parse HEAD)
          PREV=$(git tag -l 'deployed-*' --sort=-creatordate | head -1)
          PREV_SHA=$(git rev-list -n1 "${PREV:-HEAD~1}" 2>/dev/null || echo "$(git rev-parse HEAD~1)")
          git tag "deployed-$(date -u +%Y%m%dT%H%M%SZ)" "$DEPLOYED"
          git push origin --tags
          echo "DEPLOYED_SHA=$DEPLOYED"   >> "$GITHUB_ENV"
          echo "PREV_GOOD_SHA=$PREV_SHA"  >> "$GITHUB_ENV"
      - run: make deploy
      # Post-deploy proof. On failure, roll back to the LAST tag known-good (PREV_GOOD_SHA),
      # which is what was actually serving before this exact deploy — independent of how
      # many batches coalesced into it.
      - run: make smoke-test || { echo "smoke failed; rolling back to $PREV_GOOD_SHA"; make deploy REF="$PREV_GOOD_SHA"; exit 1; }
```

With `concurrency: deploy-main`, five PRs that land in one queue batch produce **one**
deploy of the final tip — not five serial deploys. That single batched deploy is the
difference between "quick succession" and "blocked for an hour." The `deployed-*` tags
make the **deploy** the unit of rollback (which is what actually shipped), decoupled from
the **merge batch** (which is what the queue grouped) — they are not the same set.

---

## 6. Conflict-resolution protocol (when your branch is behind)

`git rerere` is on (§1), so repeated conflicts auto-resolve. On "head out of date" or a
queue eviction due to conflict:

```bash
cd ".trees/${TASK}"
# Crash recovery: a previous run may have died mid-rebase, leaving .git/rebase-merge.
# Abort any in-progress rebase before starting a fresh one, or `git rebase` will refuse.
git rebase --abort 2>/dev/null || true
git fetch origin main
git rebase origin/main || {
  # Resolve, then continue. rerere replays known resolutions automatically.
  git status --short
  # ... fix conflicts ...
  # Guard against an "empty after resolution" step (whole change absorbed upstream):
  git diff --cached --quiet && git rebase --skip || { git add -A && git rebase --continue; }
}
git push --force-with-lease     # safe: only force if remote == what you last saw
```

Then re-apply the `ready-to-merge` label to re-enqueue. **Never** resolve a conflict by
merging `main` into your branch (it pollutes history and breaks linear-history). Always
rebase. If the rebase result is deterministic, this loop is fully automatable and
eventually succeeds with no human in the loop.

---

## 7. Eviction & back-off (graceful resubmission)

A PR can be ejected from the queue (its batch failed, base conflict, or flaky check). Do
NOT hammer the queue:

```bash
# Exponential back-off, then re-enqueue once green again.
attempt=${ATTEMPT:-1}
sleep $(( (2 ** (attempt-1)) * 30 ))     # 30s, 60s, 120s, ...
cd ".trees/${TASK}" && git fetch origin main && git rebase origin/main
git push --force-with-lease
gh pr edit "$PR" --add-label ready-to-merge
```

When a batch of N fails, the queue does the bisect **for you**: on a failing combined
state it auto-ejects the offending PR and recreates the temporary branch for the PRs
*behind* it without the offender, then re-tests. You do not n-ary search by hand. What you
MUST avoid is the over-eviction bug in §11: a PR that is merely *behind* the real culprit
also shows `status:failure` for its (now-stale) speculative branch — **do not** mark those
`do-not-merge`. Only the PR the queue actually removed is the culprit; the rest are
re-tested and land. Distinguish them: a true culprit is *dequeued* (no longer in
`gh api repos/$REPO/merge-queue/...`), whereas a collateral failure is still enqueued.

**Flaky checks:** the merge queue ejects on the **first** failing status — there is no
"retry in this position" knob. So flake-retry must happen **inside the CI job before it
reports status** (see the double `make ci` in §3). If a PR was ejected anyway, re-enqueue
via the back-off above; do not assume the queue will retry it for you.

---

## 8. Agent communication protocol (claim work, signal ready)

> **Do NOT put the claim board in a file on `main`.** §2 forbids implementation agents
> from pushing to `main`, and branch protection blocks it anyway — so a file board would
> force every CLAIM through the merge queue (5-min wait + CI just to claim a task) and two
> agents claiming at once would branch from the same `main` and produce **conflicting
> board commits**. That is the serialization-on-claim we are trying to kill. Use a
> mutable, push-free coordination store instead: a **GitHub Issue** (one comment per
> claim, atomic via the API) or a tracking-issue **task list / labels**. The table below
> is the *logical schema*; store it as issue comments, not a committed file.

One owner per task; this *avoids* overlap up front so most PRs are conflict-free by
construction.

```
# .agents/board.md  — one row per task
| task           | owner        | branch              | files (globs)        | status   |
|----------------|--------------|---------------------|----------------------|----------|
| backend-auth   | agent-3      | agent/backend-auth  | src/auth/**          | building |
| ui-settings    | agent-7      | agent/ui-settings   | src/ui/settings/**   | ready    |
```

Protocol:

1. **CLAIM** — before starting, add your row with `status: building` and a *disjoint*
   `files` glob. If your glob overlaps an existing `building` row, pick different work.
2. **READY** — push branch, open PR, set row `status: ready`, label PR `ready-to-merge`.
3. **LANDED** — Coordinator sets `status: landed` and removes the row after cleanup (§1).
4. **BLOCKED** — set `status: blocked: <reason>`; the Coordinator or a human picks it up.

Status signals the classifier/coordinator reads (use these exact words in PR comments):
`READY`, `REBASING`, `EVICTED`, `BLOCKED`, `LANDED`.

---

## 9. Human approval gate

- The required `required_approving_review_count=1` (§3) means nothing lands without one
  approval. For autonomous fleets, designate a **reviewer agent** for low-risk PRs and
  require **human** approval for PRs touching protected paths.

```yaml
# .github/CODEOWNERS — force human eyes on dangerous paths
/infra/            @your-human-handle
/.github/          @your-human-handle
/migrations/       @your-human-handle
deploy.yml         @your-human-handle
```

- Add a `needs-human` label rule: any PR touching CODEOWNERS paths cannot get
  `ready-to-merge` until a human approves. The Coordinator must skip such PRs in §4.

---

## 10. Rollback

**First: the deploy job already self-heals.** On smoke-test failure, §5 redeploys
`PREV_GOOD_SHA` (the previous `deployed-*` tag) *in the same job* and exits non-zero. So
the serving target is restored before the coordinator even wakes. The steps below repair
**`main` itself** so the bad code doesn't ship again on the next deploy.

> **There is no "merge commit" to revert.** §3 uses **Squash** + `required_linear_history`,
> so each PR lands as one squash commit and a batch is N adjacent squash commits with no
> enclosing merge. Revert the *range that was deployed*, identified by the `deployed-*`
> tags — NOT a guessed "batch merge SHA."

```bash
# Coordinator only. Revert exactly the range that the failed deploy shipped.
git fetch origin main --tags
BAD=$(git tag -l 'deployed-*' --sort=-creatordate | sed -n 1p)   # the deploy that failed
GOOD=$(git tag -l 'deployed-*' --sort=-creatordate | sed -n 2p)  # last known-good deploy
# Revert every commit in (GOOD..BAD] as one new commit; linear-history safe.
git revert --no-edit "${GOOD}..${BAD}"
git push origin main                            # re-fires deploy.yml -> ships last-good
```

If even one PR in that range was fine and you want to keep it, instead revert only the
culprit's squash commit (`git revert --no-edit <culprit_sha>`) after the bisect in §11
identifies it.

Deploy-target-only rollback (no history change — fastest, already done by §5 on failure):

```bash
LAST_GOOD=$(git tag -l 'deployed-*' --sort=-creatordate | sed -n 2p)
make deploy REF="$LAST_GOOD"
```

Then the Coordinator opens a follow-up PR to fix-forward, and labels the culprit branch
`do-not-merge` until fixed.

---

## 11. Coordinator loop (the whole thing in one place)

```bash
# Run by the SINGLE Merge Coordinator agent, every ~1–5 min.
set -euo pipefail
git fetch origin main

# 1. Enqueue everything eligible (queue tests combined state in parallel).
for n in $(gh pr list --label ready-to-merge --json number,reviewDecision \
            --jq '.[] | select(.reviewDecision=="APPROVED") | .number'); do
  # Skip PRs needing human review of protected paths.
  gh pr view "$n" --json labels --jq '.labels[].name' | grep -qx needs-human && continue
  gh pr merge "$n" --squash --auto && echo "READY #$n enqueued"
done

# 2. On a batch failure, the QUEUE auto-ejects exactly the offender and re-tests the rest.
#    DO NOT relabel every status:failure PR — most are collateral (they failed only because
#    they sat behind the culprit's bad speculative state) and the queue will land them on
#    re-test. Relabeling them do-not-merge is the over-eviction bug. Only act on a PR that
#    the queue actually DEQUEUED (failure AND no longer present in the live merge queue).
enqueued="$(gh api "repos/${REPO}/merge-queue/main" --jq '.entries[].pull_request.number' 2>/dev/null || true)"
for n in $(gh pr list --search "status:failure label:ready-to-merge" --json number --jq '.[].number'); do
  grep -qx "$n" <<<"$enqueued" && continue          # still in queue → collateral, leave it
  gh pr edit "$n" --remove-label ready-to-merge --add-label do-not-merge
  gh pr comment "$n" --body "EVICTED: dequeued on a failing combined-state check; needs rebase/fix."
done

# 3. Clean up worktrees/branches for landed PRs.
#    `--force` on a LOCKED worktree fails, so a crashed agent that left a lock would leak
#    forever. Unlock stale worktrees first (a live agent re-locks on its next tick).
for wt in $(git worktree list --porcelain | sed -n 's/^worktree //p'); do
  case "$wt" in *"/.trees/"*) git worktree unlock "$wt" 2>/dev/null || true;; esac
done
for b in $(git branch -r --merged origin/main | grep 'origin/agent/' | sed 's#origin/##'); do
  task="${b#agent/}"
  git worktree remove ".trees/${task}" --force 2>/dev/null || true
  git push origin --delete "$b" 2>/dev/null || true
done
git worktree prune
```

---

## TL;DR — why this kills the 1-hour block

| Cause of the block                     | Fix in this file |
|----------------------------------------|------------------|
| Serial rebase-test-merge per PR        | Merge queue with **speculative parallel** checks (§3) |
| `strict` "branch up to date" requirement | Turned **off**; queue rebases against predicted state (§3) |
| Full CI re-run for every PR            | **Batch** up to 5 PRs → one CI run; **shard** the suite (§3, §5) |
| One deploy per merge                   | **Coalesced batched deploy** via `concurrency: deploy-main` (§5) |
| One bad PR rebuilds everything behind  | Auto-eject + **bisect**; the rest still land (§7, §11) |
| Agents clobbering the same checkout     | **Per-agent worktree** + deterministic port/DB (§1) |
| Two green PRs that conflict semantically | **Combined-state** test catches it before `main` (§4) |
| Flaky check freezes the queue          | Flaky-retry, long jobs **non-required/async** (§3, §7) |
| `main` locked while one agent merges    | **Optimistic**: main never locked; rebase-and-retry (§2, §6) |

---

## Addendum — when the bottleneck is REBASING, not CI

If your CI is fast (~2 min) but agents still stall for an hour, the problem isn't CI — it's
**rebase contention**: each merge moves `main`, so every other agent re-rebases against a moving
target. With 15 threads and 5–8 landing at once, the 3rd/4th/5th never catch up — a rebase cascade.

**Fix: take rebasing out of the agents' hands entirely.**
- An agent's job ends when it opens a green PR. **It never rebases a moving `main`.**
- One **lander owns `main`** (a coordinator agent, or GitHub's native merge queue via the
  `merge_group` trigger). The lander grabs the 5–8 ready PRs, rebases them **as one batch**, tests the
  combined state **once** (~2 min), and fast-forwards them together. On failure it **bisects** out the
  one bad PR and lands the rest.
- Result: 8 deploys cost ~one rebase+test, not eight. Nobody chases a moving target → the cascade dies.
