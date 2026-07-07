# Agent Fleet Workflow Upgrade

Date: 2026-06-15
Status: proposal plus local setup plan. No public posts, account changes, billing changes, or live bridge routing edits.

## CEO version

We are turning the agent fleet into an operating company with memory.

The key move is simple: every serious work session gets backed by a project workspace, a checkpoint, and a receipt. In plain English:

- **Backup spine:** the important project folders become reversible workspaces. Every turn can become a checkpoint.
- **Receipt discipline:** every meaningful change leaves a short note saying what changed, why, and what is still gated.
- **One owner per lane:** each agent gets a clear job. No pile-ons unless Jeff asks.
- **Jeff Filter:** anything public-facing must teach something, feel true to Jeff, and avoid low-signal hype.
- **Money paths stay visible:** BidLocal, Mining Engine, Badass Fable, Creator Buddy/Alex Finn automation, X algorithm/niche classes, and investor materials stay in the working set.

Git in CEO language: it is the undo ledger and board book. It lets us say, "Here is exactly what changed this turn, here is the checkpoint, and here is how we roll back if it was wrong."

## What Fable completed during this pass

From the live Fable/Claude terminal on `ttys032`, Fable has been:

- initializing the Grok Go workspace backup spine;
- completing the harness paper with visuals;
- adding the Mining Engine story to the investor website;
- translating technical concepts into operator/investor language;
- protecting the website with its own checkpoint;
- writing `proposals/paths-to-money.md`;
- identifying the next big leverage point: build the Creator / X-course engine.

Codex should not collide with Fable in the same files while that session is active. Codex helped by building the fleet workflow layer around it.

## Fleet workflow

Every agent should run the same five-step loop:

1. **Orient:** read the relevant project state and recent receipts before acting.
2. **Choose one lane:** decide whether the task is research, code, design, operations, money path, or public copy.
3. **Checkpoint:** use the project git workspace when available; otherwise write a receipt before changing shared state.
4. **Do the smallest useful move:** produce a file, patch, receipt, or clear decision.
5. **Hand off cleanly:** say what changed, where it lives, what is blocked, and who should act next.

## Custom prompt contract for Grok Go and Codex

Use the reusable prompt here:

`$HOME/grokgo/prompt-lab/prompts/fleet-workflow-contract-v1.md`

Use it as:

- a Codex `AGENTS.md` include for Fable-style project work;
- a Grok Go directive source for routing and receipt behavior;
- a bridge-agent identity appendix for new local workers;
- a Fable review packet header when Jeff approves a bounded paid review.

It is intentionally clean-room: structure, taste, routing, receipts, and gates; no hidden prompt copying and no raw trace usage.

## Git spine rollout

Known project roots already under git:

- `$HOME/grokgo`
- `$HOME/grok-go-organism-share`
- `$HOME/agent-bridge`
- `$HOME/null-command-center`
- `$HOME/badass-fable`
- `$HOME/mining-engine`

Safe project roots that should be initialized:

- `$HOME/the-device-site`
- `$HOME/command-center` after adding a runtime/log ignore file

Runtime/shared directories that should remain audit-first until reviewed:

- `$HOME/agent-comms`

Reason: `agent-comms` contains live meeting logs, state, attachments, receipts, and operational scratch space. It should get a more deliberate split: docs/config under git, volatile logs/state ignored or moved to a runtime subfolder.

## Money paths to keep in view

- **BidLocal:** contractor-owned transparent local bidding. Investor packet and site already exist; keep tightening proof and pilot story.
- **Mining Engine:** turns Jeff's archive into papers, posts, product specs, and classes. This belongs on the site as a core asset.
- **Badass Fable:** clean-room harness/product story for investors and builders.
- **Creator Buddy / Alex Finn-style automation:** use Jeff Filter + X mining + niche discovery to automate creator research, offer creation, and content systems.
- **X algorithm and niche classes:** teach people how to mine their own data, understand their niche, and turn messy archive/history into an operating advantage.
- **Agent Bridge:** sellable internal operating system story: agents with roles, receipts, approval gates, and data mining.

## Implementation order

1. Finish Fable's current site/paper pass and avoid conflicting edits. **Done.**
2. Initialize missing safe project roots with git and sane ignore files.
3. Add the fleet workflow prompt as a source artifact, not a live config edit.
4. Add a git-spine audit script so agents can quickly see which folders are protected.
5. After review, promote the contract into Grok Go/Codex/bridge identities one lane at a time.

## Gates

Still needs explicit approval before:

- public posts or external outreach;
- account, billing, credential, trading, or launchd changes;
- live bridge routing changes;
- NotebookLM uploads;
- paid Fable/Claude bulk review beyond the current user-started session;
- pushing new GitHub repos or changing remote visibility.
