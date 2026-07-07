# X reply to Matthew Berman's $500 agents.md bounty

Bounty (verbatim): "Didn't work. $500 to anyone who sends me an agents.md file that solves my issue. My agents should be able to deploy multiple releases (merge into main) in quick succession without getting completely blocked for an hour."

The hour-long block is serialization: each PR rebases on new main, re-runs full CI, merges, *then* the next one starts. With N agents that's ~N x CI. Fix = stop testing one-at-a-time + take main off the critical path.

---

## Version A — lead with the fix, tight (primary)

> The 1hr block is serialization — each PR rebases → reruns full CI → merges before the next can start, so N agents = N×CI.
>
> Two fixes, both in the agents.md:
>
> 1. **Worktree per agent** (`git worktree add` + per-agent port/DB/.env) so parallel work never collides locally.
> 2. **A merge-coordinator that owns main.** Agents never merge — they enqueue. The queue speculatively tests main+PR1, +PR1+PR2, +PR1+PR2+PR3 *in parallel* (branch prediction), batches the greens, bisects on failure, auto-rebases on "head out of date." Main is never locked.
>
> We run exactly this on a Mac mini — parallel Fable/Codex lanes in worktrees, one coordinator owning main, brakes + a ledger to stop runaways. Gist + drop-in agents.md 👇

**First reply (the deliverable link):**

> agents.md + a 6-line worktree spawn + the coordinator loop, copy-pasteable: [gist link]
>
> Knobs that matter: required-checks list kept thin & fast (e2e/perf async, non-blocking), `concurrency:` to cancel stale runs, flaky tests auto-retried not blocking. Bigger batch = more velocity, lower consistency — tune to your conflict rate. Built in public, happy to take hits.

---

## Version B — build-in-public, two-paths framing

> Hit this exact wall. The hour = your merge queue testing PRs one-at-a-time. Two ways out, pick your appetite:
>
> **Lightweight (drop in today):** GitHub native merge queue + `merge_group` trigger → it speculatively tests main+A, main+A+B, main+A+B+C in parallel and fast-forwards only the greens. Add worktree-per-agent so agents stop clobbering each other locally. That alone collapses N×CI back toward 1×CI.
>
> **The full organism (what we run):** worktree-per-agent + a dedicated merge-coordinator agent that *owns* main — agents only enqueue, it batches/bisects/auto-rebases, plus brakes (killswitch, per-lane budgets) and an append-only ledger so a hot loop of agents can't nuke main or your wallet. Running it now on a Mac mini with parallel Fable/Codex lanes.
>
> agents.md for both + the coordinator script in the reply 👇

**First reply (the deliverable link):**

> Drop-in agents.md (worktree spawn, enqueue protocol, coordinator loop, the thin required-checks config): [gist link]
>
> The non-obvious part isn't the queue — it's the stop gate. The coordinator only fast-forwards main when the *combined* state is green, which is also what catches semantic conflicts (two PRs green alone, broken together). That gate is the whole game.

---

## agents.md to paste into the gist (the actual deliverable)

```markdown
# AGENTS.md — parallel merge + deploy without the 1-hour block

## Why this exists
Naive flow serializes: each PR rebases on new main → reruns full CI → merges,
*then* the next PR starts. N agents = ~N×CI time → the hour-long stall.
Fix: (1) isolate agents in worktrees, (2) never merge to main directly —
enqueue into a speculative+batched merge queue owned by one coordinator.

## 1. Every agent works in its own worktree
On task start:
    BRANCH="agent/$TASK"
    git worktree add ".trees/$TASK" -b "$BRANCH" origin/main
    cd ".trees/$TASK"
    # deterministic, collision-free runtime per agent:
    export PORT=$((3100 + $(echo "$BRANCH" | cksum | cut -d' ' -f1) % 6899))
    export DB_SCHEMA="agent_$TASK"          # or a DB suffix / throwaway container
    cp .env.example .env.local              # per-agent secrets/state
- `.trees/` is gitignored. Use Docker if you need true runtime isolation.
On finish: `git worktree remove .trees/$TASK && git worktree prune && git branch -D $BRANCH`

## 2. Keep PRs small
200–400 line PRs: ~40% fewer defects, ~3x faster to land, and they batch cleanly.
Split big diffs into stacked PRs; each targets the previous branch.

## 3. NEVER merge to main. Enqueue.
Agents do NOT run `git merge`/`gh pr merge`. They open a PR and add it to the queue.
The merge-coordinator (one agent owns this lane) is the ONLY writer to main.

## 4. The coordinator: speculative + batched
- Builds a temp branch = main + all PRs ahead in queue + this PR.
- Tests main+PR1, main+PR1+PR2, main+PR1+PR2+PR3 **in parallel** (branch prediction),
  not serially. PR2 fails → PR1 still merges now, PR3 retested without PR2.
- Batches greens (e.g. 4 PRs/CI run) → ~25% as many CI runs.
- On batch failure: bisect to evict the culprit, re-batch the rest.
- On "head out of date"/conflict: `git fetch origin main && git rebase origin/main`,
  auto-resolve if deterministic, else flag; then re-enqueue. Main is never locked.
- GitHub native: enable Merge Queue + add the `merge_group` event to CI workflows.

## 5. Keep the gate thin and fast (this is where queues die)
- Required checks: minimal + fast only. e2e/perf → async, non-blocking workflows.
- `concurrency:` groups to cancel stale runs.
- Flaky required check that passes elsewhere in the queue → mark flaky, keep merging.
- Avoid "jump to top of queue" — it forces a full rebuild of everything in flight.

## 6. The combined-change gate (catches semantic conflicts)
Two PRs can be green alone and broken together. The coordinator only fast-forwards
main when the COMBINED batch state is green. That gate IS the deploy decision.

## 7. Deploy = batch, don't lock
Deploy the merged batch once, not one deploy per merge. A deploy queue that
coalesces rapid releases keeps "quick succession" from re-serializing at deploy time.

## 8. Brakes (so a hot agent loop can't nuke main or the wallet)
- Killswitch file + per-agent max turns.
- Per-lane daily budget: downgrade at 80%, halt at 100%.
- Append-only ledger of every merge/deploy for audit + replay.
```

---

## Notes
- Direct X URL returns HTTP 402; bounty text confirmed via cdn.syndication.twimg.com (tweet id 2068106301402755268, 26 replies, "Didn't work" replies to his own 2026-06-19T21:23Z fix attempt).
- Brakes/ledger claims map to real files: `brakes.py` (killswitch, per-task max_turns, per-lane budgets w/ 80% downgrade + 100% halt) and the file-based bus `bus.py` (atomic tmp+os.replace, consume-once). Worktree-per-agent + coordinator-owns-main is the part we'd be shipping as the gist, not yet wired into the live loop — keep build-in-public honest about that if pressed.
