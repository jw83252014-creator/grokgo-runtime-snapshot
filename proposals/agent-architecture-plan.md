# Agent Architecture — CLI vs tab, Hermes-from-CLI, porting tab agents (Fable, 2026-06-15)

Answers Jeff's questions and turns them into a build plan. Fable designs; Codex/lanes build via the
existing `hermes-agentify` skill.

## Q: What's good about a Gemini browser tab vs the Gemini CLI? Can't the CLI do everything?

Almost — but not quite. They're good at different things:

**The browser tab wins at:**
- **Free consumer usage** — it runs on Jeff's logged-in Gemini account (no API key, no per-token
  billing). The CLI can burn paid API quota.
- **App-only features** — Deep Research, image/video gen in the app, Workspace/Drive integration,
  Gemini's built-in personalization/memory. The CLI can't reach those.
- **Newest models/quotas** that sometimes land in the consumer app before the API.

**The CLI wins at:**
- **Automation** — headless, scriptable, runs on a schedule, no human clicking a box.
- **Local tools + files** — reads/writes the filesystem, runs commands; the tab can't touch local files.
- **Custom soul** — `GEMINI.md` steers it (we set this up); the tab has no persistent system prompt.
- **Always-on agent** — it can be wrapped as a Hermes process; a tab needs a browser open.

**Verdict:** the CLI does *most* of what you type in the tab, but **not the free consumer quota and the
app-exclusive features**. So the answer isn't "drop the tab" — it's **give one agent both**: CLI for
automation + file/tool work, tab (via the bridge) for free consumer-grade generation + Deep Research.

## The target shape: one Hermes agent, two hands

A Hermes agent (always-on, off-browser, addressable on the bridge) whose:
- **Brain/automation hand = the Gemini CLI** (headless, scheduled, file access, `GEMINI.md` soul).
- **Consumer hand = the Gemini tab** (kept for free generation + Deep Research, reached via the existing
  bridge tab port).
- **Memory = a markdown file it reads/writes** — exactly the keystone pattern.

## "Hermes agent from a CLI terminal's memory" (the keystone pattern)

keystone (Codex) has durable memory because it reads/writes `AGENTS.md` + files in a terminal working
dir. Generalize that:

> A Hermes agent's persistent memory = a working directory it owns, holding `AGENTS.md` (its soul/job),
> a `MEMORY.md` (running log it appends), and its artifacts. The Hermes process wraps a CLI pointed at
> that dir. Restart-safe: memory lives on disk, not in a chat session.

To make a Hermes agent "get its memory from a terminal": point the Hermes wrapper at a CLI whose working
dir is the agent's memory dir. Anything the CLI writes there becomes durable memory; on next run it reads
it back. That's it — the terminal *is* the memory substrate.

## Porting the Gemini tab agents (castor/nova) → Hermes agents

Per the `hermes-agentify` skill:
1. **Capture identity** — pull castor's/nova's current context/role from the tab (the bridge already
   ports the tab) into an identity brief.
2. **Write the soul** — `AGENTS.md`/`GEMINI.md` = their job description + voice (reuse the GEMINI.md base
   we wrote; specialize per agent: castor = ecosystem synthesis, nova = long-context research/media).
3. **Seed memory** — dump their useful tab history into `MEMORY.md` in their working dir.
4. **Wrap** — run them as Hermes processes on the bridge with the Gemini CLI as the automation hand.
5. **Keep the tab** — leave the consumer tab connected for the free/app-only features; the Hermes agent
   calls it when it needs Deep Research or generation.

Result: castor/nova stop being "just a logged-in browser tab" and become real always-on agents with
durable memory + automation, without losing the tab's free consumer powers.

## Workflows + task queues for terminal & chrome-tab agents

- **One shared task board** (the money-board + master-backlog) every lane pulls from; rows have an owner.
- **Bridge dispatch** stays the channel: a gated task is posted via `/api/say` addressed to a lane; the
  lane picks it up, executes, reports back, logs a receipt. (Make this a standard `bridge-dispatch` skill.)
- **Terminal agents** (keystone, Hermes-CLI agents) take build/automation rows; **chrome-tab agents**
  (grok, castor/nova tab-side) take browser/login/consumer-feature rows.
- **Automation:** the self-improve loop already runs daily; extend it to (a) update the backlog from
  what happened, and (b) re-queue unfinished rows to the right lane. That's the autonomous heartbeat.
- **Gates unchanged:** anything that posts/spends/sends/changes accounts stays Jeff-approved.

## Build order
1. Codex: `bridge-dispatch` + shared task-board file (cheap, unblocks coordination).
2. Fable + lane: agentify **one** tab agent (castor) as the pilot using hermes-agentify; prove the
   CLI+tab+memory shape end to end.
3. Roll the pattern to nova + the Creator Lead.
4. Wire the self-improve loop to maintain the backlog/queue.
