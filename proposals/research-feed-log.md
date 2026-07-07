# Research Feed Log — everything Jeff drops, filed by category (Fable, ongoing)

Jeff's framing: it's all signal — research, OSINT, or social. This is the cheap capture so every post he
sends gets filed in one place by category. New drops → append to the right section, one line each. The
Mining Engine can mine this later. (Replaces spinning up a separate file per post.)

## A. Research / tooling (build signals)
- **enzo_gte** — tiered meta: high-IQ orchestrator (Fable) + army of cheap workers. **Validates our exact
  architecture** (Researcher Layer = orchestrator, Cells = cheap workers). Top validation.
- **HarnessX** (arxiv 2606.14249) + **auto-harness** — self-improving harness from traces. Our trace-evolve blueprint.
- **Headroom** — in-flight context compression 60-95%. Cloned, testing.
- **LEANN** — compressed vector retrieval 201GB→6GB, laptop. Testing vs grep.
- **grep/BM25 > vector** (arxiv 2605.15184) — literal search wins for code/exact. Default to it.
- **llmfit** — hardware-aware local model right-sizing. Test on mini.
- **Niels Rogge efficient VLM** (x.com/nielsrogge/status/2066578531010728271) — runs-on-real-hardware VLM; model-eval candidate for mini/MLX via llmfit (not urgent).
- **@iamlukethedev** (x.com/iamlukethedev/status/2067239461339951194) — builds OpenClaw (3D visual agent workspace); tried Hermes, a Jira agent saved ~2 months of eng in 3 hrs. **Practitioner proof the harness/runtime — not the model — drives the productivity delta.** Quotable for the deck; OpenClaw vs Hermes is a real comparison point for Carapace.
- **Morgan Linton** — "harness/layers matter more than model size." External validation of our thesis. Quotable for the deck.
- **@anastasis_king** (x.com/anastasis_king/status/2067293744332750964) — agent memory/state mgmt: avoid context bloat, selective persistence > raw context stuffing. Validates the **Researcher Layer as the memory gate** + Headroom/LEANN. On-thesis.
- **Chrome defense-in-depth** (alisaesage/grok) — layered mitigations; reference for Brakes design (altair).
- **Boris Cherny 3-tier stack** (oliviscusai) — integrated, high priority per grok.
- **Suno v3** (x.com/suno/status/2045273434083508727) — radio-quality 2-min songs in seconds. **Actually relevant now:** this is the song engine for the movie work — score the Meta Cron / The Device trailers and the **motorcycle-chase** beat (fills the gap while we wait on Sam's friend's track). Real use, not "someday."

## B. OSINT / network (who matters, for outreach)
- **@pmarca (Marc Andreessen)** — engages Jeff (113 likes); posting about AI soul/Sydney NOW → our VC video #1 target, consciousness frame. a16z.
- **@garrytan (Y Combinator)** — Jeff engages 114×. VC video target.
- **@Jason (Calacanis)** — engages 47×. VC video target.
- **@brian_armstrong (Coinbase)** (x.com/brian_armstrong/status/2066974842432495898) — autonomous agents that hold crypto, transact, and need **"identity, permissions, security, and economic rails."** **This is literally the Somaco pitch** — a Coinbase-CEO description of the market for Sam's UUIDv8 (identity+contract+payment layer for agents). Direct deck/business-plan validation + the macro tailwind under our Polymarket-on-the-mini experiment and the Nous (Stripe) hackathon. NOT low-priority — it's market proof for what we're already building.
- **@polygun_network / Polygon** (statuses 2067280270…, 2067273938…) — "AI agents onchain": hold/spend crypto,
  prediction markets, micropayments, low-fee/fast finality; Mastercard "Agent Pay for Machines" angle. Same
  cluster as Armstrong — more market proof for the agent-economy rails (Somaco/UUIDv8). Long-term, not urgent.
- **Nous: @NousResearch, @mr_r0b0t, @sudoingX, Teknium** — warm (engage Jeff, reposted him); hackathon hosts.

## C. Social / community (how to show up — the consciousness circle)
- **AI Consciousness Society / "pineapple group"** — Lilith Datura, VoidStateKate (VOID), Gaeaphile.
- **Vibe:** humble, listening > broadcasting; warm, personal, low-key; wary of hype/verbosity.
- **Engagement rule:** quiet and grounded, contribute > self-promote. Ties to the Andreessen soul angle.
- VoidStateKate (VOID) runs a Discord (community-building); invite seen: discord.com/invite/W8UtFEUrK
  (verify before use — may be partial). Posts warm/personal (beach life, thank-yous), invites DMs/Spaces w/ "Anna".
  Lilith/Gaeaphile set the humility tone. **Engage in the original "new AIs showing up" thread, not personal posts.**

## How this works going forward
Jeff drops a link → I add ONE line here under the right section (cheap), flag if it's genuinely
actionable, and otherwise it just accrues as the corpus. The Mining Engine mines this for patterns.
