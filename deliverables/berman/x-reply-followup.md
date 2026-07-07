=== FOLLOWUP REPLY (new context: rebase contention, not CI) ===

--- Version A (tight, nails the diagnosis) ---
That detail's the key — if CI is only ~2 min, this was never a CI problem. It's rebase contention: each merge moves main, so every other agent re-rebases against a moving target. With 15 threads and 5–8 landing at once, the 3rd/4th/5th never catch up — a rebase cascade.

Fix = take rebasing out of the agents' hands entirely:
• An agent's job ends when it opens a green PR. It never rebases a moving main.
• One lander owns main (a coordinator agent, or GitHub's merge queue via merge_group). It grabs the 5–8 ready PRs, rebases them as ONE batch, tests the combined state once (~2 min), fast-forwards them together. On failure it bisects out the bad one and lands the rest.

8 deploys then cost ~one rebase+test, not eight. Nobody chases a moving target → cascade dies. That's what the agents.md does — and it's what got us past the same wall running ~15 parallel lanes on a Mac mini.

--- Version B (for Peter / more technical) ---
The smoking gun is "constant rebasing" with 2-min CI — that's contention, not throughput. The agents are serializing themselves by each rebasing onto a main that 14 others are moving.

Decouple it: agents are write-only to their own worktree + branch; they never touch main. A single lander (merge queue w/ merge_group, or one coordinator) batches the ready set, does ONE rebase of the batch, one combined CI run, atomic fast-forward, bisect-evict on red. Optimistic, main never locked, throughput = batch size per CI cycle instead of 1 per rebase-race.

agents.md (drop-in + the full-organism version) in my reply above.
