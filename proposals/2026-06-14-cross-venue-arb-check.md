# Proposal: cross-venue arbitrage signal for prediction-market research

**Status:** DRAFT — not applied. Read-only, human-gated. Date: 2026-06-14.

## Problem
Today the Kalshi + Polymarket monitors fire on a raw ≥5¢ move on a single venue.
That's a *noise* signal: it triggers equally on a thin market and a deep one, and
can't tell a real repricing from bid/ask jitter. Kalshi has **no volume floor at
all** (Polymarket gates on `min_volume_usd: 50000`). The research goal is "is there
a tradeable edge right now," which a single-venue delta can't answer.

## Fix — two parts
1. **Kalshi volume floor.** Add `min_volume`/`min_open_interest` to `kalshi-config.json`
   and skip alerts below it, matching the Poly side. Cheap, removes most noise.
2. **Cross-venue spread check.** The same real-world event (election, rate decision,
   etc.) is often listed on *both* venues. Maintain a small hand-mapped table of
   equivalent markets `{event_key: {kalshi_ticker, poly_token}}`. Each poll, compute
   the implied-prob spread `|p_kalshi - p_poly|`. Alert only when
   `spread > fees + slippage_buffer` (configurable, e.g. 4¢). That converts "something
   moved" → "venue A and venue B disagree by more than it costs to trade the gap."

```jsonc
// cross-venue-map.json (hand-curated, starts tiny)
{ "2026-senate-control": { "kalshi": "SENATE-26-R", "poly": "0xabc…" } }
```
Alert payload: event_key, both prices, spread, which side is cheap. Still writes to
the existing `outbox/*.jsonl`, still notify-only, still `human_approve_only: true`.

## Why it matters
Arb/divergence is the one prediction-market signal that's *model-free and verifiable*
— no edge model, no forecasting, just "two prices for the same thing." It's the
highest-signal upgrade that stays inside the no-execution guardrail.

## Out of scope (flag, don't build)
Auto-execution, position sizing, and the `dexter` wallet path stay untouched and
human-gated. This proposal only improves *what gets surfaced for Jeff to decide on*.
