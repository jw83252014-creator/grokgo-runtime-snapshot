# Nous Hermes Hackathon — submission writeup (DRAFT, Fable 2026-06-17)

The short writeup that rides with the 1-3 min demo video, tweeted @NousResearch + dropped in the Nous
Discord submissions channel. Draft — Jeff approves before posting; X label should clear first.
Warm context: @mr_r0b0t and @sudoingX regularly engage Jeff's posts; bonded over the Anthropic model
swap. So this isn't cold — it's a builder they already know shipping something on-thesis.

---

## Title
**Null Axiom — a Hermes-agent organism that earns, spends, and runs its own operations**

## Writeup (the submission text)
Most "agents" are a chatbot with tools. We built the opposite: a living **organism** of Hermes agents
across a Mac mini, a laptop, and two phones — each a cell with a role, a soul, and the cheapest capable
brain. Cheap local models do ~90% of the work; the frontier model is an exception handler. A control
layer (tiered router, brakes, spend ledger, human gate) keeps it cheap and safe; ra token-compression
layer keeps it lean.

For this hackathon — agents that **earn, spend, and run real operations** — we wired **Stripe Skills**
into the organism so a cell can provision what it needs and pay for the services it uses, all behind a
spend ledger and a killswitch (it can act, but it can't run away). On the earning side, the organism runs
two real operations: **BidLocal** (a transparent contractor marketplace) and a build-in-public content
engine that turns the organism's own daily work into shippable assets.

The whole thing is governed by one rule — *Game of Life + move the operator forward*: simple local rules,
emergent behavior, and a default bias toward advancing the human's real-world goals with minimal steering.

It's not a demo that dies when you run it for real. It's been running for months, committing its own work
to GitHub autonomously, and it's the same stack we use to build everything we ship.

**The intelligence is rented. The harness — routing, memory, control, and the Stripe-powered ability to
transact — is the company.**

## The demo video (1-3 min) shows
- The cell dashboard live (the organism, pulsing).
- A Hermes cell using **Stripe Skills** to pay for / provision something — gated, test-mode, with the
  spend ledger + brakes visible (it acts, then the gate).
- The cheap-local-first routing ("cheap by default, smart on demand").
- The autonomous GitHub commits (it runs itself).
- Close: "agents that earn, spend, and run operations — running today." 🧬

## Entry mechanics
1. Post the demo video, tag **@NousResearch** (+ @mr_r0b0t / @sudoingX where natural — warm), short
   writeup above.
2. Drop the link in the **Nous Discord submissions channel**.
3. ⚠️ Post only after the X label clears (or from a clean account tagging Jeff) — a suppressed post wastes it.

## To finalize (before submit)
- [ ] Confirm the deadline (Nous Discord) — likely time-sensitive.
- [ ] Render the demo video (creative lane; reuse the Ex-Machina explainer, angle to Stripe/economic ops).
- [ ] Codex: a gated, test-mode Stripe-Skills demo the cell actually drives (he drafted the Stripe offer).
- [ ] Jeff approves the post.
