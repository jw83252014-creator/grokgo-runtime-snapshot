=== FINAL REPLY (links + organism explanation, ready to post) ===
The 1hr block is serialization — each PR rebases → reruns full CI → merges before the next starts, so N agents = N×CI.

The fix (full agents.md below 👇):
1. Worktree per agent (git worktree add) so parallel work never collides locally.
2. A merge-coordinator that OWNS main — agents never merge, they enqueue. The queue speculatively tests main+A, main+A+B, main+A+B+C in parallel, batches the greens, bisects on failure, auto-rebases on "head out of date." Main is never locked → N×CI collapses toward ~1×CI.

This comes out of our "digital organism" — a fleet of agent cells on a Mac mini: parallel Fable (Opus) + Codex lanes, each in its own git worktree, a terminal-watcher loop that wakes them to take threads of work and commit to GitHub, governed by a brakes layer (brakes.py — killswitch + per-lane budget/time caps) and an append-only ledger (every action logged: lane, model, tokens, cost, sha before/after). A Researcher layer owns merges; implementation cells only open PRs — which is exactly the fix above.

Drop-in agents.md (lightweight + full-organism versions):
https://github.com/jw83252014-creator/grok-go-organism/tree/main/parallel-merge-agents

The whole organism:
https://github.com/jw83252014-creator/grok-go-organism
