# Grok Go — How The Whole System Works (master reference, Fable, 2026-06-17)

The backup of the *structure* — how every piece fits. If you had to rebuild the organism from scratch,
this is the map. Lives in git (offsite on GitHub) + should be on a local/air-gapped drive too.

## The one-paragraph version
A distributed AI **organism**: many agent **cells** across a Mac mini, a laptop, and two phones, each a
**harness** (a terminal agent loop) + a **soul** (custom prompt) + a **brain** (a rented or local model).
Cheap/local models do ~90% of the work; the frontier model is an exception handler. A **control layer**
(routing, brakes, ledger, gates) keeps it cheap and safe. A **compression layer** (rtk + Headroom) keeps
token cost down. Everything coordinates over a **bridge** (now moving to Slack), hands off via **disk +
git**, and is governed by one principle: **Game of Life + move Jeff forward.**

## The layers (top to bottom)
1. **Cells (agents)** — Fable (architecture/reasoning/review), keystone/Codex (build+review), Gemini
   (code builder), grok/scout (web+X research), vega (visuals), Badass Fable (free local cheap lane),
   altair (security), librarian (X read-only), Orchestrator (runs the boards). Each = harness + soul + brain.
2. **Harness** — the editable loop around a model: Claude Code / Codex / Grok CLI / OpenClaude, each
   takes a custom soul (`--append-system-prompt` / `AGENTS.md` / `--rules`). Self-rewriting harness tunes
   its own soul per task; trace-evolve improves it over time (HarnessX-style).
3. **Control layer** (Fable built this, in `~/grokgo/`): `routing.yaml` (t0 code → t1 local → t2/3/4
   cloud/frontier, escalate one tier only), `dispatch.py` (router), `brakes.py` (killswitch + budgets +
   loop-detect), `ledger.db` (per-lane spend), `bus.py` (inbox/outbox), `review_queue.py` (human gate).
4. **Compression / token economy** — **rtk** (PreToolUse hook, compresses shell output 60–90% before it
   re-enters context) + **Headroom** (compresses tool outputs/files/history 60–95% before the model;
   cloned to `spikes/headroom`, testing). Prompt distillation (1585→~30 lines). `/clear` discipline.
5. **Knowledge** — the **Mining Engine** mines our own archive (chats, X, papers) through the **Jeff
   Filter** into real committed assets. The **Researcher Layer** is the guardian of "move Jeff forward."
6. **Comms / coordination** — the Agent Bridge (`:8787`) + disk handoff + git; **migrating to Slack**
   (somaco_protocol workspace, Null bot + Codex app; #all-somacoprotocol main). Telegram/iMessage/Discord
   for human pings. `slack-send`, `discord-send`, `bridge-dispatch` helpers.
7. **Surfaces** — the website (yn-eight.vercel.app, git-connected auto-deploy), the live dashboard
   (:8765), the organism page, the investor deck, the digital-organism film, the comic art.

## How Fable manages the other agents (the delegation model)
- **Fable (me) = top reasoning/architecture lane.** I design, decide, and review; I do NOT do the bulk.
- **Delegate by capability:** code build → Gemini; code review → Codex; build/execution → keystone;
  web/X research → grok/scout; visuals/video → vega/Grok Imagine; security → altair; cheap drafts → local
  Badass Fable. Dispatch via the bridge/Slack with a gated, scoped task; they execute and report.
- **Why:** I'm the expensive lane, so every turn I take is priciest — pushing execution to cheaper/free
  lanes is the whole token thesis applied to me.
- **Gates (non-negotiable):** no public post, spend, account change, or install without Jeff. Draft-only;
  the irreversible call is Jeff's. Redact secrets. Flag risks to altair.

## The governing principle
Every cell/layer/change is judged: simple local rules → good emergent behavior, AND does it move Jeff
forward sustainably? If not → filtered/stopped. (See `directives/game-of-life-principle.md`.)

## Rebuild order (if starting over)
control layer (`grokgo/`) → local model (MLX :8000) → souls (`prompt-lab/prompts/`) → harness wiring →
bridge/Slack → cells → Mining Engine → surfaces. Secrets in `~/.config/secrets/` (NEVER in git).
