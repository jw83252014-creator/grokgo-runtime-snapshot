# Data → Skills audit plan (Fable, 2026-06-15)

Goal: systematically look through ALL our data and turn recurring procedures into reusable skills, so
knowledge stops dying in chat exports and starts compounding. This is the Mining Engine's core job;
this plan makes it a repeatable pass. Fable designs/codes the harness; lanes + local routing do the
bulk reading.

## The data we have (sources to mine)
- **Downloads** — big Telegram "Agent Bridge for AI OS" exports (2.7M each), Grok chat exports
  (trading + consciousness goldmine), strategy/spec docs.
- **Jwnull vault** (`~/Documents/Jwnull/`) — organized notes + topic Indexes (BidLocal, Trading,
  Consciousness-RSI, Hermes, Soma, X-Intelligence, Operations-Security).
- **mining-engine** — concepts, prompts, x-strategy, research-sources, skills registry.
- **agent-comms** — research, checklists, NotebookLM sources, identity, roster.
- **.openclaw archive** — older workspace + command-center notes.
- **Claude Code transcripts** — already mined daily by the self-improve loop.

## What qualifies as a skill
A skill is a **reusable procedure** we'd otherwise re-explain: a `SKILL.md` with a clear trigger +
steps. Signal it's skill-worthy: we've done it 2+ times, it has a deterministic shape, and a future
agent would benefit. (Examples already built: x-data-scrape, grok-imagine-video, self-improve,
hermes-agentify.)

## The pass (repeatable)
1. **Inventory** — list source files per area; cheap, local.
2. **Mine** — focused passes per topic ("everything we know about building agents", "every X/creator
   procedure", "every trading-system design step"). Route the bulk reading to local models / cheap
   lanes; Fable + frontier only for the hard synthesis.
3. **Filter** — Jeff Filter drops noise; keep only repeatable procedures + durable concepts.
4. **Extract** — for each repeatable procedure, draft a `SKILL.md` (trigger + steps + gates). Durable
   *concepts* (not procedures) go to `mining-engine/concepts/` instead.
5. **Dedupe** — check the existing skills registry (`mining-engine/skills/agent-capabilities.md`) so we
   don't duplicate.
6. **Commit** — real files, backed up to git. Receipts logged.
7. **Register** — add each new skill to the registry + the relevant agent's soul.

## Candidate skills already visible (first harvest)
- **chrome-debug-launch** — bring up the logged-in debug Chrome on :9222 (script now exists).
- **x-data-pull** — one-command: launch debug Chrome + run the scraper (wrap the existing skill).
- **bridge-dispatch** — post a gated task to a lane via `/api/say` with the standard format.
- **telegram-notify** — send Jeff a status DM via the hermes-null gateway (pattern in use).
- **moto-frankenstein-revive** — start the phone gateway over SSH (steps proven this session).
- **vercel-deploy** — build + ship the site (once CLI is in).
- **creator-post-loop** — watch→filter→draft→visual→gate (the Creator Engine, when wired).

## Automation
The **self-improve loop** (now enabled, daily) already does step 2–6 against Claude Code transcripts.
Extend it to also sweep one archive area per run (round-robin) so the whole corpus gets covered over
time without a giant one-shot. Local model lane (once solid) makes this nearly free.

## Owner
Mining Engine runs the passes (local routing for bulk); Fable codes the harness + does hard synthesis;
Jeff approves anything that would become live config or public output.
