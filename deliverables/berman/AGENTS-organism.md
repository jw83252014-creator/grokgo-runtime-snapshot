# AGENTS.md — The Digital-Organism Merge Organism

> Drop this file at the root of your repo. It is the operating contract for a
> fleet of coding agents that merge into `main` and deploy **back-to-back, in
> quick succession, without ever blocking each other for an hour.**
>
> The short version of why the 1-hour block happens: a naive setup makes every
> agent **serialize** through one lane — each PR rebases on the new `main`,
> re-runs the full CI suite, deploys, and only *then* does the next PR start.
> With N agents and CI time T you pay ~N×T, and any mid-chain failure rebuilds
> everything in flight. **Every rule below exists to break that serial chain.**
>
> This is not "spawn agents and hope." It is a small **digital organism**: many
> dumb-but-isolated **Tool Cells** doing work in parallel, one smart
> **Orchestrator** that owns the single merge lane, and a **Brakes + Ledger**
> nervous system that makes the whole thing safe to run unattended. The naive
> "one worktree, one merge queue" answer is the *easy* path. This is the more
> powerful long-term one, because it gets cheaper and smarter the more you run
> it.

---

## 0. The three organs (read this first)

| Organ | Count | Owns | Never does |
|---|---|---|---|
| **Tool Cell** | many (scales horizontally) | one isolated worktree + one branch; does the actual coding work | merge to `main`, touch CI config, touch another cell's worktree |
| **Orchestrator** | exactly **one** writer at a time | global state of `main` + all open PRs + CI health; **the only thing allowed to merge** | write feature code |
| **Brakes + Ledger** | always-on | human gates, cost/time caps, audit log, rollback, KILLSWITCH | make policy decisions (it enforces, it doesn't strategize) |

**The single load-bearing invariant: a Tool Cell NEVER merges to `main`.**
Cells produce *ready branches*. The Orchestrator decides order, resolves
conflicts, and lands them. Removing the merge decision from N parallel cells
and giving it to one stateful coordinator is what kills the block — N writers
fighting over one `main` is the bug; one writer with a global view is the fix.

---

## 1. Tool Cell contract (the parallel workers)

Each cell is a worker that takes one scoped task and produces one mergeable
branch. Cells are **interchangeable and disposable** — that is what lets you
add more of them.

### 1.1 Isolation — git worktree per cell (mandatory)

You get a private working directory and a private branch. You share the
`.git` object store with everyone; you share **nothing else**.

```bash
# Orchestrator hands you a task; you claim a worktree:
BRANCH="agent/${TASK_ID}"
git worktree add ".trees/${TASK_ID}" -b "$BRANCH" origin/main
cd ".trees/${TASK_ID}"
```

- `.trees/` is in `.gitignore`. One directory per cell, one branch per cell.
- **Worktrees isolate FILES, not runtime.** This is the gap that bites people.
  Before you run anything, derive a deterministic, collision-free runtime:

```bash
# deterministic per-branch port (3100–9998), DB schema, and env.
# NOTE: keep A-Z in the tr set — dropping it makes "agent/T-481" and
# "agent/T_481" both collapse to the same schema, silently sharing a DB.
export PORT=$(( 3100 + $(echo "$BRANCH" | cksum | cut -d' ' -f1) % 6899 ))
export DB_SCHEMA="agent_$(echo "$BRANCH" | tr -c 'a-zA-Z0-9' '_')"
cp .env.example .env.local && echo "PORT=$PORT" >> .env.local
# If your tests touch real ports/DBs/caches, run inside a container, not bare:
#   docker compose -p "$TASK_ID" up   (Linux namespaces give true isolation)
```

- When you finish, you **do not delete your worktree** — the Orchestrator does,
  after the branch lands. Leaving it lets the Orchestrator bisect failures.

### 1.2 Keep changes small and mergeable

- Target **200–400 line PRs.** Research is consistent: small PRs have ~40%
  fewer defects and merge ~3× faster. Small PRs also batch and bisect cleanly.
- If your task is bigger, **stack it**: each branch targets the previous branch,
  not `main`. Use `gh stack` so a rebase cascades across the whole stack and
  each layer stays independently reviewable. A stack-aware merge queue tests the
  whole stack in parallel.

### 1.3 Claim protocol (so two cells never grab the same work)

Claiming a task and claiming a *merge slot* are different acts. Cells claim
**tasks**; only the Orchestrator hands out **merge slots**.

```bash
# Claim a task atomically (tmp + os.replace pattern — same as grokgo bus.py).
# A claim is a receipt: it has an owner, a lane, a worktree, and a deadline.
```

Claim record (`claims/<task_id>.json`, written atomically):

```json
{ "task_id": "T-481", "owner": "cell-backend-2", "lane": "backend",
  "branch": "agent/T-481", "worktree": ".trees/T-481",
  "claimed_at": "2026-06-19T23:10:00Z", "wip_limit_ok": true,
  "status": "working" }
```

- **WIP limit:** a cell holds **at most one** open claim. No hoarding work.
- Status flows: `working → ready → enqueued → landed | evicted`.
- A claim older than its deadline with status `working` is reaped by Brakes and
  the worktree torn down — a dead cell never wedges the queue.

### 1.4 When you're done: hand off, don't merge

```bash
# One-time in the repo root: git config --global rerere.enabled true
# (so the conflict resolutions you make below auto-replay and stay deterministic).
git fetch origin main
git rebase origin/main          # rebase onto latest; you eat your own conflicts
# run the fast required checks locally first — don't waste a merge slot on red:
make ci-fast
git push --force-with-lease -u origin "$BRANCH"   # rebase rewrote history;
                                                  # --force-with-lease is safe (fails
                                                  # if someone else moved your branch)
gh pr create --base main --fill --label ready-to-merge
```

Then flip your claim to `ready` and **stop.** The Orchestrator takes it from
here. You never run `git merge` / `git push origin main`. Ever.

### 1.5 Cell failure modes

| When… | Do this |
|---|---|
| `git rebase` hits a conflict you can resolve deterministically | Resolve, re-run `ci-fast`, push. |
| Conflict is semantic / you're guessing | **Do not guess.** Flip claim to `ready` with `conflict: true` and let the Orchestrator (which has global state) decide. |
| Your branch gets `evicted` from a batch | Re-`git fetch && git rebase origin/main`, re-run `ci-fast`, re-enqueue. Back off (exponential) so you don't thrash the queue. |
| Tempted to "just merge to unblock myself" | **Forbidden.** That is the exact behavior that creates the 1-hour block. |

---

## 2. Orchestrator contract (owns the merge to `main`)

There is **one** Orchestrator with write authority to `main` at any moment
(enforce with a *time-bounded* lease; see §2.5). It is the brain of the organism: it
holds **global state** and makes the **strategic merge decisions** that a
single isolated cell structurally cannot.

> **It is also the single point of failure — design for that.** "Exactly one
> writer" is the load-bearing invariant, but a plain create-or-fail lock turns a
> *crashed* Orchestrator into a permanent fleet stall (the very block we're
> killing). The lease MUST have a TTL + heartbeat so a standby can take over.
> The Orchestrator is otherwise **stateless between cycles** — all its state is
> in `state/*.json` and GitHub (§2.1) — so any process holding a fresh lease can
> resume mid-queue. Run a warm standby; on a missed heartbeat it steals the
> lease and continues. No failover = the org wedges the first time the brain OOMs.

### 2.1 Global state it holds (and persists)

```
state/main.json        # current main SHA, last deploy SHA, deploy health
state/prs.json         # every open PR: branch, base, CI status, size, age, conflict flag
state/ci.json          # runner pool depth, flaky-test registry, avg CI time T
state/queue.json       # ordered merge queue + speculative batch tree
state/deploys.json     # deploy lock state, last N deploy results, rollback points
```

These are git-versioned receipts (grokgo convention): every Orchestrator
decision is an auditable write, never an in-memory-only choice.

> **State drift is the silent killer here. `git`/GitHub are the source of truth;
> `state/*.json` is a derived cache.** `main.json`'s SHA, `prs.json`'s PR/CI
> status, etc. can go stale (a PR re-pushed, closed, or merged out-of-band) and a
> stale cache makes the Orchestrator enqueue a dead PR or fast-forward a wrong
> SHA. Two rules keep them honest:
> 1. **Reconcile before you act, not just after.** At the top of every cycle,
>    re-derive from truth (`git fetch`, `gh pr list`, `gh pr checks`) and
>    overwrite the cache. Treat `state/*.json` as a *snapshot for this cycle and
>    the ledger*, never as authority. If cache and truth disagree, truth wins and
>    you log the drift.
> 2. **Don't commit live state onto `main`.** Writing `state/*.json` into the same
>    branch the queue is merging creates commit races with the very `main` you're
>    landing PRs onto. Keep it on a separate orphan branch (e.g. `agents/state`)
>    or an external store; only the *ledger* (§3.4, append-only) and decisions
>    need durable history.

### 2.2 Never lock `main` — run a **speculative, batched** merge queue

This is the core anti-block mechanism. Do **not** test PRs one at a time.

**Eligibility to enqueue (the everyday gate, not just the failure gates in §3.3):**
A PR enters the queue only when ALL hold — otherwise 30 cells land unreviewed code
into `main` by default:
- label `ready-to-merge`, claim status `ready`, and **no** `do-not-merge`/`needs-human`;
- fast required checks green on the PR;
- ≤ ~400 changed lines (or a declared stack);
- **≥1 approval** — a reviewer-agent for low-risk PRs, a **human** for any
  CODEOWNERS path (`/infra`, `/.github`, `/migrations`, `deploy.yml`). The §3.3
  gates handle *failures*; this gate decides what's allowed to land in the first place.

**Speculative parallel checks (branch prediction for merges):**
Instead of testing `main→PR1`, then `main+PR1→PR2`, then `...→PR3` serially,
build the future-state branches and test them **all in parallel**:

```
test( main + PR1 )
test( main + PR1 + PR2 )
test( main + PR1 + PR2 + PR3 )      # all three CI runs fire at once
```

- All green → fast-forward `main` to `main+PR1+PR2+PR3` in one shot.
- PR2 fails → **PR1 still lands immediately**, PR3 is re-tested as `main+PR1+PR3`.
  Nobody waits on the failure. This collapses per-PR latency from ~N×T back
  toward ~T even at 50+ PRs/day. **This is what makes "quick succession" real.**

**Batching to control CI cost:** group e.g. 4 ready PRs into ONE integration
branch and test the combined state once. Green → land all 4. Batches of 4 ≈ 25%
of the CI runs; teams report cutting queue CI bills 50–75%.

**Bisect-on-failure:** when a batch goes red, do an n-ary/binary split to find
the one culprit PR in ~log(N) extra rounds instead of exhaustively re-testing
serially. Eject the culprit (mark its claim `evicted`), re-batch the rest.

**Combined-change gate = semantic-conflict catcher:** because you test
`main+A+B` *together*, two PRs that are each green alone but encode opposite
directions get caught **before** they corrupt `main`. This is the failure mode
plain branch-protection misses, and it's a common hidden cause of "it merged
but main is broken, now everything's blocked."

```bash
# integration branch build (conceptual)
git fetch origin
git switch -c "queue/batch-$(date +%s)" origin/main
for pr in $READY_BATCH; do git merge --no-edit "origin/$pr" || mark_conflict "$pr"; done
git push origin HEAD          # fires merge_group CI on the combined state
```

> **Pick ONE merge engine — never run both.** GitHub Merge Queue does most of
> this natively once you add the `merge_group` event trigger to your Actions
> workflows; if you use it, the Orchestrator *drives* it (order, batch size,
> ejects, bisects) and must **not** also fast-forward `main` itself via the
> hand-rolled integration-branch builder above — two writers = double-merges and
> the multi-writer bug this whole design exists to kill. The integration-branch
> builder is the fallback for when native Merge Queue isn't available. Graphite's
> queue is stack-aware if you use stacked PRs.

### 2.3 Order & strategy (the part a single cell can't do)

The Orchestrator decides merge order with the global view:

1. **Conflict-free PRs first** — land the easy wins, shrink the queue fast.
2. **Small before large** — small PRs land cheaply and reduce the rebase surface
   for everything behind them.
3. **Flagged-conflict PRs:** the Orchestrator owns conflict resolution because
   it knows what *else* is landing. Auto-rebase onto latest `main`; if the
   result is deterministic, retry. If genuinely semantic, route to the AI
   conflict resolver on a **throwaway** branch (never the cell's worktree), test
   the resolution in the queue, and only then land.
4. **Flaky-test grace:** if a required check fails speculatively but passes
   further back in the queue, consult `state/ci.json`'s flaky registry — mark it
   flaky and keep merging rather than freezing the whole queue. Flaky required
   checks are the #1 cause of stuck queues.

### 2.4 Decouple deploy from merge — coalesce releases

Merging fast is pointless if deploy re-serializes you. **One deploy per merge is
the second half of the 1-hour trap.**

- A single **deploy lease** (not a per-PR lock): the Orchestrator holds it and
  **batches** deploys. Land a batch of merges → deploy the resulting `main`
  **once**.
- A **coalescing deploy queue**: if 5 merges land during an in-flight deploy,
  the next deploy ships the latest `main` once — it does **not** run 5 deploys.
- Multi-environment deploys run as a **fan-out matrix in parallel**, not env
  after env. Each env's slow checks are async and non-blocking on the merge.
- Every deploy writes a rollback point to `state/deploys.json` (see §3.4).

### 2.5 Orchestrator failure modes

| When… | Do this |
|---|---|
| Two Orchestrators somehow run | The merge lease (`state/merge.lock`: atomic create-or-fail, holds `{owner, expires_at}`) makes exactly one the writer; the other becomes read-only and waits. |
| **The Orchestrator dies / hangs (the SPOF)** | The lease carries a TTL the live Orchestrator renews each cycle (heartbeat). When it stops renewing, the lease expires and a **warm standby steals it** and resumes from `state/*.json` + GitHub — never block waiting on the dead one. **A lock with no TTL = a dead brain wedges the whole fleet, recreating the hour-long block.** Brakes reaps stale leases the same way it reaps dead cells (§1.3). |
| Queue stalls on one red PR | Bisect, eject the culprit, keep the rest moving. Never block the queue on one PR. |
| `main` got broken anyway | Trigger rollback (§3.4), freeze the queue, open a `RED-MAIN` receipt for a human gate. |
| "Jump to top of queue" requested | Refuse by default — it forces a full rebuild of everything in flight and is itself a block-generator. Allow only behind a human gate. |
| Merge produces a deterministic conflict | Auto-rebase + retry. Only escalate to human when resolution is non-deterministic. |

---

## 3. Brakes + Ledger contract (the nervous system)

Borrowed directly from grokgo's `brakes.py`: **every paid/irreversible action
goes through `check()` BEFORE and `log()` AFTER. No exceptions.** This is what
makes the organism safe to run unattended overnight.

### 3.1 Hard caps (cost + time)

- **KILLSWITCH:** `touch ./KILLSWITCH` → all cells and the Orchestrator stop
  claiming and merging at the next checkpoint. Single file, single source of
  truth.
- **Per-lane daily budget:** at 80% of budget, downgrade the lane's model tier;
  at 100%, halt the lane. (Lanes = `backend`, `frontend`, `infra`, … — the same
  accounting boundary grokgo already uses.)
- **Per-task `max_turns`** and **per-claim deadline:** a runaway cell dies; its
  worktree is reaped; its slot frees.
- **Merge-rate cap:** max deploys/hour as a safety throttle — high velocity, but
  bounded.

### 3.2 Loop / wasted-work detection

- Dedup on `(task_id, input_hash)` — same task + same state seen twice = the cell
  is spinning; park it. (grokgo's `seen_hashes` guard.)
- **Evict back-off:** a branch evicted 3× from batches is auto-routed to a human
  gate instead of thrashing the queue forever.

### 3.3 Human gates (the "decide when it succeeded" gates)

The skill is designing the check that decides when an action is *allowed* to
proceed. Gate exactly these, nothing more (over-gating recreates the block):

| Gate | Trigger |
|---|---|
| `RED-MAIN` | `main` failed post-merge verification → freeze + page a human. |
| `SEMANTIC-CONFLICT` | AI conflict resolution is non-deterministic / low-confidence. |
| `BUDGET-100` | a lane hit 100% of daily budget. |
| `DEPLOY-ROLLBACK` | an auto-rollback fired → human confirms root cause before unfreeze. |
| `FORCE-JUMP` | someone wants to jump the queue (rebuilds everything in flight). |

Everything else runs autonomously. Each gate is an entry in an approvals queue;
the Orchestrator blocks **only** the affected lane/queue, not the whole fleet.

### 3.4 Audit log + rollback

- **Ledger (SQLite):** every action — claim, CI run, merge, deploy, eviction,
  gate — logged with `(lane, model, tokens, est_cost, sha_before, sha_after,
  status, ts)`. This is your audit trail and your cost dashboard.
- **Rollback:** every merge records `sha_before`; every deploy records its
  rollback point. `DEPLOY-ROLLBACK` does `git revert`/redeploy of the last good
  `main` SHA automatically, then opens the human gate. Because deploys are
  coalesced and batched, rollback is one operation, not N.

### 3.5 The before/after wrapper (copy this shape)

```python
# Pseudocode mirroring grokgo brakes.check()/log()
def land(pr_batch):
    brakes.check(action="merge", lane=batch_lane, cfg=cfg)   # caps, killswitch, gates
    sha_before = git_head("main")
    result = merge_queue.land(pr_batch)                       # speculative+batched
    brakes.log(action="merge", sha_before=sha_before,
               sha_after=git_head("main"), status=result.status, cfg=cfg)
    return result
```

---

## 4. Why this beats "just add a merge queue" (the long-term path)

A merge queue alone is the *easy* answer and it does help. This organism is the
**more powerful** one because of three properties a bare queue lacks:

### 4.1 It scales past a few agents

- **Tool Cells scale horizontally** — they're stateless and isolated, so 5 → 50
  cells is just more worktrees and more elastic CI runners. The merge decision
  stays centralized (one Orchestrator), so adding cells never adds
  merge-contention.
- **Parallel CI scales with queue depth:** test sharding + matrix builds +
  elastic runners mean lanes scale *with* load instead of choking on it.
- **Lanes partition the fleet:** `backend`/`frontend`/`infra` cells touch mostly
  disjoint files, so conflicts are rare *by construction*, and each lane has its
  own budget and its own slice of the queue.
- **Sub-orchestrators** if you outgrow one: shard the queue by lane, each lane a
  merge sub-lane that fast-forwards into a top-level integration step. The
  pattern is supervisor → lane-orchestrators → cells.

### 4.2 It gets smarter over time (the organism part)

The Ledger is a training corpus, not just an audit log. Over runs it learns:

- **Flaky-test registry** (`state/ci.json`) grows automatically — repeat
  offenders get auto-quarantined from required checks, so the queue stops
  stalling on the same flakes.
- **Conflict memory:** pairs of files/areas that historically conflict get
  flagged, so the Orchestrator *schedules them apart* (never in the same batch)
  before they collide — prevention, not just resolution.
- **Adaptive batch size:** the Orchestrator tunes batch size from observed
  green-rate. High green-rate → bigger batches (cheaper CI); rising failure →
  smaller batches (more isolation). This is the RCV velocity/consistency dial,
  driven by data instead of a guess.
- **Task scoping feedback:** tasks that produced evicted/conflicting branches
  teach the up-front task-splitter to scope future work with less overlap.

A bare merge queue does the same thing every day. This one is measurably better
next month than it is today, because every merge/deploy/eviction is a labeled
example feeding the Orchestrator's policy.

### 4.3 It's safe to run unattended

The Brakes + Ledger layer means you can point 30 agents at `main` overnight and
the worst case is bounded: capped spend, capped deploy rate, auto-rollback,
KILLSWITCH, and a human-gate queue waiting in the morning — not a corrupted
`main` and a surprise bill.

---

## 5. Bring-up checklist (do these in order)

1. `echo ".trees/" >> .gitignore` and commit.
2. Add the `merge_group` event trigger to your CI workflows (enables GitHub
   Merge Queue) **or** stand up the integration-branch builder in §2.2.
3. **Trim required checks to the fast, deterministic minimum.** Move e2e/perf to
   async non-required jobs. Add `concurrency:` groups to cancel stale runs. Every
   required check is something that can flake and block — minimize them.
4. Wire `brakes.check()`/`log()` around every merge and deploy (§3.5).
5. Stand up the single Orchestrator with the merge lease (§2.5) and the
   `state/*.json` files.
6. Launch Tool Cells: each does `git worktree add` (§1.1), claims one task
   (§1.3), produces one small PR (§1.2/1.4), and **never merges**.
7. Turn on the coalescing deploy queue + deploy lease (§2.4).
8. Verify the kill: open 8 green PRs from 8 cells at once. **Success = they
   land as 1–2 batched, speculative-tested merges and deploy once, in minutes —
   not 8 serial rebuild-test-deploy cycles over an hour.**

---

## 6. The one-paragraph mental model

Many isolated **Tool Cells** work in parallel in private git worktrees and
produce small, ready branches — they **never** touch `main`. A single
**Orchestrator** holds global state (`main` + all open PRs + CI/deploy health)
and is the *only* thing that merges: it runs a **speculative, batched** merge
queue (test future states in parallel, land green ones immediately, bisect and
eject failures, catch semantic conflicts by testing combined states) and
**coalesces deploys** so quick-succession releases ship as batched deploys, not
N serial ones. A **Brakes + Ledger** nervous system wraps every merge/deploy
with cost/time caps, human gates, an audit log, and one-command rollback, and it
quietly turns the log into a smarter Orchestrator over time. Serialization — the
thing that blocks you for an hour — is removed by isolating writers and
centralizing the merge decision behind a non-blocking, parallel queue.
