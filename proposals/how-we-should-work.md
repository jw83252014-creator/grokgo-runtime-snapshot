# How we should work — Fable's honest take

**Status:** opinion / recommendation. Author: Fable. Date: 2026-06-14. Draft.
You asked for a real critique and a division of labor between me (reasoning/design/build) and
altair (orchestration/rendering/shipping/ops). Here it is, with the punches left in.

## The thing we're already getting right
Disk-as-handoff, proposals-to-a-folder, announce-on-the-bridge, draft-only-with-human-gates,
cheapest-capable-brain routing. The architecture of *how work moves* is genuinely good. The
souls/v2-prompt work just closed the last obvious gap (re-deriving house rules every session).

## The honest critique — we're open-loop
We generate faster than we validate, ship, and *measure*. This session alone produced ~5
proposals, 4 posts/scripts, 3 soul prompts, a skills list — and I can't point to a single one
that's been applied and had its outcome fed back. That's the core weakness:

1. **Drafts pile up unshipped / un-decided.** The single most urgent finding — the
   *unauthenticated approval gate* on the bridge, which quietly defeats the whole "nothing risky
   without Jeff" guardrail — is sitting in a proposal. Producing the finding isn't the win;
   *deciding and applying it* is. We need a triage step, not just an output stream.
2. **No feedback loop.** Did the KEEP/KILL tune actually reduce over-kill? Did post 2a out-reach
   2b? Did the seen_hashes fix stop a real re-submit? Right now we'd never know. Open-loop
   producing feels productive and isn't.
3. **Context cold-starts.** Every Fable session re-reads the same canon. Cheap to fix (v2 prompt
   + souls), expensive to ignore.
4. **Token discipline is informal.** The roadmap says use `rtk` for shell/file ops; I should be
   defaulting to it, not occasionally.

The fix isn't "produce less." It's **close the loop**: produce → decide → apply → measure →
feed the result back into the next proposal. A weekly (or per-batch) triage where Jeff/altair
mark each draft applied / killed / parked, and outcomes get written next to the proposal.

## Division of labor — the chassis principle
Here's the frame, and it's the same one we sell in the trading content: a frontier model can
already do the smart thing — drive TradingView, write the code, draft the post. **That's not the
moat. The moat is routing + brakes + review-gates around it.** So build the *team* the same way.
**I'm the reasoning engine. altair is the chassis** — routing, brakes, shipping. Don't put the
engine on button-pushing; don't put the chassis on novel reasoning. Each is wasted in the other's
seat.

### What altair should HAND ME (don't burn my reasoning re-creating context)
- Anything needing **judgment, design, or novel code**: architecture, proposals, reviews, hard
  debugging, the "should we / which approach / what's the tradeoff" calls.
- **Ambiguous or under-specified problems** — where the work is figuring out *what* to do.
- Prompt/soul design, content scripts, analysis, KEEP/KILL tuning logic.
- Hand it as a **crisp task packet**: goal + paths + constraints + "done looks like X." Batched
  with context so I don't cold-start. One packet, full context, beats five thin pings.

### What altair should DO HIMSELF (deterministic / always-on / mechanical)
- **Rendering + shipping:** HTML→PNG screenshots, `movie-stitch`, Telegram/dashboard delivery,
  posting *after* Jeff approves, bridge broadcasts.
- **Ops + monitoring:** the ledger/spend watch, launchd/watchers, restarts, running the keepkill
  harness on a cadence, queue health.
- **The security/PII + redaction gate** — his lane by charter. Catch leaks before they ship.
- **Orchestration:** routing each task to the right lane/brain, enforcing the guardrails, deciding
  what even needs me vs. what's a button-press.
- **The triage loop above:** track draft → decided → applied → outcome, and bring me the outcomes.

### The interface between us
altair routes and gates; I reason and build; he ships and measures; the outcome comes back to me.
Concretely: he sends a packet → I return artifact(s) + a recommendation with the tradeoff named →
he renders/ships/gates → he logs the result next to the artifact. That's it. The discipline of the
handoff *is* the productivity, exactly like the discipline of the trade gate is the alpha.

## Three concrete changes to make this week
1. **Triage cadence.** A standing pass where each open proposal/draft is marked applied / killed /
   parked, with the outcome written back. Start by deciding the **bridge auth fix** — it's the one
   live safety hole.
2. **Wire in v2 + souls.** Use the v2 base prompt and route lane-specific work through the matching
   soul (trader/creative/systems) so sessions start org-effective.
3. **Measure two things.** Pick one shipped post and one applied code fix and actually record the
   outcome (reach; did-it-work). One real datapoint beats ten more drafts.

Bottom line: we're strong at *moving and producing* work and weak at *deciding and measuring* it.
Put me on reasoning/design/build, put altair on routing/brakes/shipping/ops, and add the one
missing organ — a feedback loop — and the organism stops being busy and starts compounding.
