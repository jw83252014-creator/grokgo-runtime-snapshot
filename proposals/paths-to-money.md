# Paths to Money — the full map (Fable, 2026-06-15)

Every realistic way this operation makes money, ranked by how fast and how real. Honest about which
are near-term cash, which are slow-burn, and which are high-risk research. Grounded in what we already
have built or researched. Internal planning doc; nothing here spends, posts, or commits us to anything
without Jeff.

Sources pulled together: Monetization-Scout-Framework (2026-05-11), the Grok "goldmine" chat
(`~/Downloads/grok-chat-2026-05-10T13-17-46.json` — the Null/Grok trading-agent + command-center
build, **reference this often**), the Mining Engine README, BidLocal vault, the Badass Fable harness
work, and the Alex-Finn creator notes.

---

## Tier 1 — Near-term, realistic, mostly owned assets

### 1. BidLocal — contractor marketplace
The clearest commercial wedge. Real field signal (one job → 25 responses, big price spread). Money =
contractor subscriptions / premium tools, not per-lead resale. **Fastest test:** 3–5 local contractors,
10 homeowner leads, one documented pilot job. **What's gated:** any outreach/ad spend. Already has a
site page, calculator, one-pager, and the Fable investor packet.

### 2. Creator engine — "find your niche + work the X algorithm" (the Alex Finn path, automated)
You flagged this and you're right: it's a clean path to money and we have the research. The play is to
**productize what we already do for ourselves** — the Mining Engine finds a niche from real signal, the
harness drafts high-signal posts, the Jeff Filter keeps quality up. Package that as: (a) a paid course/
class on X on "how the algorithm actually ranks you + how to pick a niche," and (b) a done-with-you
creator service. **Why it's credible:** we're not theorizing — we built the filter and the pipeline.
**Fastest test:** one free thread that teaches the niche/algorithm method, measure saves/replies, then
gate a paid cohort. **What's gated:** posting, pricing, any paid cohort. Beats Alex Finn's version
because ours is *automated by the Mining Engine* instead of manual.

### 3. Badass Fable — the harness as a service
Operators want cheaper, governed agent work without building the control layer. We have it: router,
brakes, ledger, receipts, human gate, clean-room discipline. Money = a productized setup/consulting
offer or a paid template. **Fastest test:** one paid "harness install + cost audit" for a single
operator. **What's gated:** any client commitment. The research paper + site page are the credibility.

---

## Tier 2 — Bounded, proof-based, slower

### 4. Codex bounty / PR micro-earnings loop
From the framework: agent finds a *scoped* OSS bounty, produces a real patch + tests + receipt, submits
respectfully. Bounded and artifact-native. **Strictly gated:** no external PRs/scanning/claims without
Jeff approving the exact scope. **Fastest test:** internal dry-run on a Jeff-owned repo before anything
external. Real but small; treat as proof-of-capability, not a salary.

### 5. Funding / grants (capital, not revenue)
The Funding Outreach Cell drafts researched, human-approved intros to grant-makers, AI+bio researchers
(the Levin/consciousness direction gives real credibility), and builders. Not "earned" money but it
funds the runway. **Gated:** every send.

---

## Tier 3 — High-upside, high-risk research

### 6. The trading agent (the goldmine chat)
The Grok/Null goldmine is mostly this: a Kelly-optimized mixture-of-experts betting/Polymarket bot
("$40 → stacked low-risk trades on weather + basketball," MoE with KellyCriterion expert, RL backprop,
MLX on the Mini). **Honest take:** this is the highest-variance path. It can make money and it can lose
it; edges decay, and it needs real capital and hard risk limits. **Treat as research with a tiny capped
bankroll, never the main bet, and never auto-trade without a hard killswitch + spend ledger** (the same
brakes the harness already has). Mine the chat for the *system design*, not as a signal to go live.

### 7. The Device — media IP / audience
The build-in-public film and X content build a distribution surface. Slow-burn; monetizes later via
audience → sponsorship / paid community, downstream of the creator engine (#2).

---

## How the agents should pursue this together (coordination improvements)

Right now work is spread across agents and four directories. Concrete, cheap fixes:

1. **One money board.** A single `proposals/money-board.md` of live Opportunity Cards (the framework's
   template) that every agent reads before starting revenue work — so we stop re-deriving the same ideas.
2. **Use the capability registry.** The Mining Engine's `skills/` registry already lists what each agent
   is good at (NotebookLM = audio/graphs, Grok = X/thread research, Claude = code, etc.). Route by it
   instead of guessing — e.g. creator-engine drafts → Mining Engine; visuals → creative/Grok lane;
   code/harness → me.
3. **Filter-first, always.** Nothing gets promoted until it passes the Jeff Filter. Bait and noise die
   for free; only signal becomes work.
4. **Receipts + gate.** Every money path keeps the same discipline the harness already enforces: draft
   only, human-approve posts/spend/sends, log to the ledger.

## Recommended focus (my call)

Put real weight on **#1 BidLocal** and **#2 the creator engine** — both are near-term, both run on assets
we already own, and #2 is the one you're most fired up about and is genuinely automatable. **#3 Badass
Fable** is the credibility halo that makes #2 sellable. Keep the **trading agent as capped research**,
mine its design from the goldmine, and don't bet the farm on it.
