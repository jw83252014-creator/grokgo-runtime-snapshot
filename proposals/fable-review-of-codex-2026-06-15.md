# Fable review of Codex work — 2026-06-15

Reviewer: Fable (Opus 4.8). Scope: the clean-room cheaper-Fable plan + receipts + architecture SVG,
the OSINT/social-proof plan, the BidLocal investor packet (Fable cut), and the live-ish site
(`index.html` + `bidlocal` / `data-room` / `agent-bridge` / `the-device` pages). Read-only review.
No posts, DMs, spend, installs, or live-config edits were made. rtk used for shell.

## Verdict

Codex's work is strong and safe. The clean-room plan is the right thesis (the durable asset is the
controlled runtime, not a copied prompt), the risk taxonomy (green/amber/red) is correct, the trace
dataset is handled conservatively, and the X framing teaches a mechanism instead of baiting. The site
is clean, public-safe, and conservative on the BidLocal numbers. **Ship-track with edits.** Nothing
here trips a live send as written — but three real external-send surfaces (NotebookLM upload, the
Telegram contact lane, any X post) need the gate kept on, and two of them need a sanitization pass
called out explicitly. Concrete diffs at the bottom.

The single most important catch: **NotebookLM is an upload to Google.** "Stay local / no public sends"
is satisfied for posting, but importing internal files (`anchors.yaml`, `directives/*`, the
implementation plan) into NotebookLM *is* an external send. The plan currently treats local files as
free to import. That needs a sanitization gate before any import.

---

## 1. Architecture (clean-room plan + SVG)

Solid. T0–T3 lanes with "earn the expensive call by failing the cheap lane," brakes/ledger/receipts/
researcher/human-gate, and the green/amber/red source classes that forbid red ingestion. This matches
`cheaper-fable-strategy.md` (route hard calls to frontier, offload the rest, RAG-not-train) and adds a
cleaner governance loop. No notes on the thesis.

Two concrete fixes on the SVG (`assets/cheaper-fable-clean-room-architecture.svg`):

- **Bug — background doesn't cover the canvas.** `viewBox` is `0 0 1600 1600` but the background
  `<rect>` is `height="1000"` (line 4). Content runs down to y≈1495 (the safety-boundary band sits at
  `translate(80 1390)` + 145). So rows *02 Model Lanes*, *03 Tooling/Governance*, and the safety band
  render on transparent/black instead of the intended white — it'll look broken when exported to PNG
  for X. Fix: `height="1600"` (or `1560`).
- **Polish — the four bands don't visually connect.** Horizontal arrows exist *within* each band, but
  there are no connectors from Intake → Router → Model Lanes → Tooling. As-is it reads as four separate
  diagrams. Add three short vertical arrows down the left spine, or a thin "flows into" rail.

Minor: the plan text mentions a Mining Engine and Researcher Layer that aren't a single labeled lane in
the SVG legend — fine, the SVG has both boxes; just keep the paper's prose names matching the SVG box
labels exactly so NotebookLM doesn't invent a mismatch.

## 2. Trace-dataset handling — and the "dataset cards without live sends" answer

Correct and conservative. The receipt marks the HF traces `amber_red`, `needs_human:true`, "risk memo
only"; the plan's *Trace Dataset Risk Notes* forbid raw ingestion, CoT copying, distillation, few-shot,
and publishing weights, while allowing the **card URL as a cited risk source**. That is exactly the
right line and it answers the explicit ask:

> **How to use a public reasoning-trace dataset card without a live send:** you only *read a public page*
> and *write a local memo*. Allowed: cite URL + date + license fact + risk class in a receipt; summarize
> risk at a high level; track whether public distilled models appear. Disallowed: download/ingest raw
> traces, paste CoT, use as few-shot, train, or publish a derivative. No bytes leave your machine, so no
> send occurs. Keep it `needs_human` before it informs anything public.

One verify-before-publish note: the dataset slug casing differs across docs (`Glint-Research/Fable-5-traces`
in the receipt vs `glint-research/fable-5-traces` earlier). HF owner slugs are case-sensitive — confirm
the live slug before it lands in any public artifact so we don't ship a dead link. Same for the
`platform.claude.com/...` and `anthropic.com/news/...` URLs dated today: resolve each once before citing
publicly (they may be speculative paths).

## 3. X-post framing

On-anchor: mechanism-first, no hype, humor-but-teaches. Versions A/B/C + the 10-post thread + the hook
variants are all good, and all draft-only through the picker/human gate. Recommendations:

- **Lead with Version A (clean technical) + the diagram as the primary single drop.** The 10-post thread
  is good but long; hold it as the optional deep-dive, not the first ask.
- **Keep the export-control backstory out of public copy.** The receipt notes Fable access was suspended
  via a US export-control directive; that's fine as *context for us*, but public posts should stay on the
  architecture ("copying a prompt is the wrong layer"), not the geopolitics. The current drafts mostly do
  this — just don't add the export angle when staging.
- Everything stays gated: no auto-post. Good.

## 4. NotebookLM source pack

Good instincts — plan-first ordering to anchor the clean-room boundary, public URLs instead of copied
private content, and an explicit *Do not import* list (leaked prompts, raw traces, secrets, `.env`,
private paths, target lists). But the boundary is soft in one place and must be tightened:

- **NotebookLM import = an upload to Google.** It is not a *public* post, but it is an external send. The
  *Primary local sources* list includes `anchors.yaml`, `directives/cell.template.md`,
  `directives/research.claude-code.md`, and `grokgo-implementation-plan.md`. Before any of those are
  uploaded, they need a public-safe pass: no secrets, no private filesystem paths, no target lists, no
  raw chat. Add a one-line gate: *"Every local file is sanitized and human-approved as public-safe
  before NotebookLM import; prefer public URLs over uploading internal config."*
- Net rule for the pack: **local files → sanitize → human-approve → import; public URLs → cite directly.**
  Raw traces / leaked prompts / secrets → never. That keeps "no live public sends" true while still
  letting NotebookLM build the explainer.

## 5. BidLocal investor site/deck linkage

The site is clean and conservatively framed (the BidLocal page correctly calls the field result a "pilot
signal, not a market statistic" and avoids the inflated `$9,000 vs $300` figure from the archive). The
calculator MVP is self-contained and uses contractor-entered numbers only. Gaps in *linkage*:

- **Two divergent proof packets.** `index.html:621` links `docs/bidlocal-investor-proof-packet.md` (the
  older 2.3K sanitized packet). The richer **Fable cut**
  (`~/grokgo/proposals/bidlocal-investor-proof-packet-fable.md`) adds the network/social-proof angle
  (proof #4) — which the site's Evidence section *already gestures at* ("social graph scrape"). Reconcile:
  port a sanitized copy of the Fable cut into `the-device-site/docs/` and point the link at it, or fold
  proof #4's network bullet into the site copy. Don't leave two packets drifting.
- **The OSINT/social-proof page isn't built.** `osint-page-plan.md` specs a 4-scroll network page; the
  site only surfaces the X numbers as hero facts + a data-room row. Build it (a `/network` page, or a
  module inside `/data-room`), and **keep the unverified consciousness-cluster module dark** until the
  follow edges are confirmed — the plan already flags Levin / @ai_sentience / Alan Mathison / Lilith
  Datura as unverified; the site must not assert those relationships.
- **Public-safe wording on the X numbers.** `index.html:455-456` says "21 recent X posts **mined**" and
  "113 social graph **contacts captured**." Both read extractive/surveillance-y for an investor page.
  Prefer "21 recent posts" and "113-follower builder graph" (or "…builders & founders in orbit"). The
  `data-room.html` row ("Aggregate counts only") is the right tone — match it.
- **Secret hygiene is clean** (grep found no committed tokens). Keep `TELEGRAM_BOT_TOKEN` /
  `TELEGRAM_CHAT_ID` in Vercel env only. Note the contact form (`/api/say` → Telegram) is an *external
  send*, but it's inbound-only to Jeff's private review chat — that's a legit human-gate lane, not a
  public post. Cosmetic mismatch: the inline script labels messages "@vega @null SITE INBOUND" while
  `api/say.js` forwards them as "THE DEVICE — script contribution"; align the label if you care.

## 6. Fable-style local harness plan

This *is* the cheaper-Fable spike, and it's well-sequenced: guardrails-first → inspect-before-install
preflight → OpenClaude sandbox → Ollama Anthropic-compat lane → MLX. Aligns with the strategy doc
(inference + RAG before any fine-tune; no Fable-trace training). Tightening:

- **Name the local model.** Phase 1 says "start with an already-installed model, else pull a small one."
  Pin it to the strategy doc's pick so the spike isn't open-ended: **Qwen2.5-7B-Instruct (4-bit MLX/
  Ollama)** for inference/draft, **Qwen2.5-3B** if a QLoRA *voice-only* test is ever run (post legal
  review). Borderline above ~7B on the 16GB Mini.
- **The Ollama `ANTHROPIC_BASE_URL` trick is a config change — keep it spike-scoped.** Pointing a
  Claude-native tool at a local base URL is exactly the kind of live-config edit we don't touch on the
  real `~/.claude` setup. Run it only inside `~/grokgo/spikes/...` with a throwaway env, never the
  default profile. The plan implies this; make it explicit.
- Acceptance checks (killswitch halts paid lanes, spend-by-lane, loop-block, `needs_human` on live
  config) are the right bar. Keep them.

---

## Concrete next diffs (in priority order)

1. **SVG bg fix** — `assets/cheaper-fable-clean-room-architecture.svg:4`: `height="1000"` → `height="1600"`.
   (Optional) add 3 vertical connector arrows down the left spine between the four bands.
2. **NotebookLM sanitization gate** — in the plan's *NotebookLM Source Pack*, add before the local list:
   "Every local file is sanitized + human-approved public-safe before import (NotebookLM upload = an
   external send to Google); prefer public URLs over uploading internal config." Re-audit `anchors.yaml`
   and `directives/*` against that bar before any import.
3. **Pin the local model** — Phase 1: add Qwen2.5-7B-Instruct (4-bit) for inference; Qwen2.5-3B for any
   future QLoRA voice test (legal-gated). Mark the `ANTHROPIC_BASE_URL` lane spike-only, never default config.
4. **Verify-before-cite** — confirm the HF slug casing and that the `platform.claude.com` / `anthropic.com`
   URLs resolve; only then use them in a public artifact. Fix the slug casing to match the live page.
5. **Reconcile the BidLocal packet** — port a sanitized copy of `bidlocal-investor-proof-packet-fable.md`
   into `the-device-site/docs/` and repoint `index.html:621`, or fold proof #4 (network) into the site copy.
   One canonical packet.
6. **Build the social-proof page** from `osint-page-plan.md` (new `/network` or a `/data-room` module);
   keep the unverified Levin/@ai_sentience/Alan Mathison/Lilith Datura cluster dark until edges are confirmed.
7. **Public-safe wording** — `index.html:455-456`: "21 recent X posts mined" → "21 recent posts";
   "113 social graph contacts captured" → "113-follower builder graph." Match the data-room's restrained tone.
8. **X drop staging** — stage Version A + the (fixed) diagram as the primary draft; thread optional; keep
   export-control context out of public copy. Draft-only through the picker; Jeff approves before anything posts.

## Boundary check (the explicit ask, summarized)

Using public reasoning-trace **dataset cards** and **Grok Go materials** without live public sends works
as long as the operation is **read-public + write-local + draft-only**: cite the dataset card URL in a
local risk memo (never ingest the traces), and keep Grok Go notes local. The only three places that
*are* external sends — **NotebookLM import (Google), the `/api/say` contact lane (Telegram), and any X
post** — each stay behind the human gate, and the first two get a sanitization pass first. As written,
Codex's plan keeps all three gated; diff #2 closes the one soft edge (treating NotebookLM uploads as
free). No posts, sends, spend, installs, or config edits were performed in this review.
