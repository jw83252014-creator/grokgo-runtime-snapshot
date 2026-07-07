# Stripe Draft — Creator Course Payment Link

Status: draft-only, test-mode spec. No live payment link, no charges, no keys in code.

## Offer

**Find Your Niche by Mining Your Own Data**

Audience: creators/operators who already have messy archives, posts, chats, and ideas, but need a
high-signal niche map and a repeatable content board without becoming engagement-bait.

Format: 90-minute workshop or recorded class.

Deliverables:

- Niche thesis.
- Audience map.
- Three content pillars.
- 14-day posting experiment board.
- Jeff Filter checklist for killing generic drafts.

## Draft Stripe Object

Source JSON: `proposals/stripe-drafts/creator-course-payment-link.draft.json`

Recommended Stripe mode: `test`.

Payment link action: create only in Stripe test mode after Jeff approves the price and copy.

## Draft Copy

Headline:

> Find your niche by mining your own data.

Description:

> Bring your messy archive. We help you find the repeated signal, map what your audience will actually
> care about, and leave with a 14-day posting board that keeps your voice intact.

## Gates

- Jeff approves price before any Stripe object is created.
- Test mode only until Jeff explicitly approves live mode.
- No keys in git, shell history, docs, screenshots, or Agent Bridge.
- No checkout link sent externally without Jeff approval.
- No customer data processing without consent boundaries.

## Implementation Notes For Hermes Desktop

1. Open Stripe in Hermes desktop.
2. Confirm the dashboard is in test mode.
3. Create product from the JSON draft.
4. Create one test payment link only.
5. Save the resulting test URL in a local private receipt, not in public docs.
6. Ask Jeff before live mode, posting, outreach, pricing changes, or real charges.
