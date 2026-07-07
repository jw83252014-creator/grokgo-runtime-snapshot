# Proposal: Drops — one link in, every agent thinks, one page out

Date: 2026-07-05
Status: draft for Jeff review (no wiring done yet)

## Problem

Jeff drops a link/idea into ONE surface (usually the Grok Chrome "Right-Agent" tab because it holds the long context). Nothing else sees it. The Grok tab is a browser UI with **no filesystem and no bridge write access** — its analyses die in the tab unless Jeff manually ferries them (which is exactly what he's doing today: pasting Grok's handoff into Fable). Direct answer to "has this been happening?": **No.** The bridge mirror only relays some chat traffic; the creative team, Jade, Null, and Fable do not see what goes into the Grok tab. Continuity today = Jeff's clipboard.

## Fix (small, uses what exists)

A **drop** is a first-class object on the bridge:

1. **One entry point.** Jeff posts a link/thought once — any of: `bin/say drop <url or text>`, Telegram bot command `/drop ...` (@claudemacmini143bot), or a Drop box on the Command Center page (:8787).
2. **Canonical artifact on disk.** Dispatcher writes `~/agent-comms/drops/YYYY-MM-DD-HHMM-<slug>/drop.md` (url, Jeff's words, trace_id). Disk is the handoff layer; the tab is not.
3. **Fan-out to every registered lane** — Fable, Null, Jade (`ask-glm.sh`), castor/nova, grok-terminal, creative dept. Each gets the same bounded task: *"Read drop.md. 150 words max: relevance to your lane + one concrete action. Cheap tier; no Fable escalation unless the drop is flagged hard."* Grok-tab lane gets the drop pasted in by the relay so its long context stays in the loop too.
4. **Receipts, visible.** Each response lands at `drops/<slug>/responses/<agent>.md` + a JSONL receipt row. A drops page on the dashboard (:8765) shows the drop + all takes side by side. One place to see everyone's thinking — no tab hopping.
5. **Synthesis + gate.** Fable (or Researcher Layer later) writes `synthesis.md` — merged take + recommended action. Nothing goes public, gets sent, or spends money from a drop; it's thinking, not posting.

## Blast radius

New: one dispatcher script + one dashboard page + a `/drop` handler in the two Telegram relays. Reuses: bridge (:8787), receipts pattern, killswitch, existing lane watchers. No auth changes, no new accounts, no config overwrites on existing lanes. Fully reversible (delete the script + page).

## Why it matters

This is the actual fix for "I can only talk to one agent." Jeff stops being the message bus. One drop → whole organism responds → one page shows receipts. It also makes the Grok tab a *feeder* instead of a trap: its signal enters the same pipeline as everyone else's.

## Open question for Jeff

Default response tier for drops: t1 local / t2 cheap (recommended — drops are frequent), with a `!hard` flag to allow one t4 Fable take?
