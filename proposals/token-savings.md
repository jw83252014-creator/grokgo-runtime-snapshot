# Token Savings — ranked proposal (Fable, 2026-06-14)

How to run Claude Code + the agent fleet for less. `rtk` is confirmed active (PreToolUse hook
`rtk hook claude`), so shell-op savings are already banked. Below are the *other* wins, ranked by
estimated impact. % are rough, per the lane they apply to.

## Banked already
- **rtk** — token-optimized shell proxy on every Bash call. Claimed **60–90%** on dev/shell ops
  (git/ls/grep/build output). Keep leaning on it; `rtk gain` to audit. ✅ active.

## P0 — biggest wins
1. **Route to free brains first (the router's whole point).** ~**80–95%** vs running everything on a
   paid tier. Default every sub-task to t0 (plain code) / t1 (GitHub Models gpt-4o-mini, free) /
   Gemini CLI (free, multimodal); escalate **one step only** on schema-fail. Frontier (Fable/Sonnet)
   should be <10% of calls. Audit: count paid vs free calls in `ledger.db` weekly.
2. **Prompt caching on the stable prefix.** ~**50–90%** off *input* tokens on cache hits. Anthropic
   caches a stable leading prefix (system prompt + pinned context) for a 5-min TTL. Wins: (a) keep the
   system prompt / pinned files **byte-identical** across calls in a burst; (b) batch agent calls
   within the 5-min window rather than spreading them out (a wake-up >5 min later pays a full cache
   miss — relevant to scheduled passes); (c) put volatile content *last*, stable content *first*.
3. **Summarize-then-act / digest, never dump.** ~**70–95%** on reflection/research/review tasks. The
   self-improve loop already models this: `jq` a digest of transcripts instead of loading 270 raw
   JSONL files. Apply everywhere — read file *ranges* (Read offset/limit), grep-then-read, and feed
   models a condensed digest, not whole artifacts.

## P1 — steady savings
4. **/clear discipline + context hygiene.** ~**20–40%** per long session. Start a fresh context per
   distinct task; don't let one session accrete unrelated history (every later turn re-bills the whole
   transcript). One task → one context.
5. **Headless `claude -p --output-format json` for automated passes.** ~**15–30%** vs interactive on
   scheduled/agent work — no interactive scaffolding, structured output is smaller and parseable, and
   it composes with cheap-tier routing.
6. **Smaller working context.** ~**10–25%**. Read only the lines you need (offset/limit), avoid
   re-reading files already in context, prefer Grep/Glob over dumping directories, cap tool-output
   that gets fed back to the model.

## P2 — housekeeping (indirect)
7. **Transcript retention.** 270 `*.jsonl` and growing. Prune/rotate >30-day transcripts to a cold
   archive so digest passes (self-improve) stay cheap and fast. Saves digest cost, not chat tokens.
8. **Cap tool fan-out.** When spawning sub-agents, bound count + per-agent budget; a runaway parallel
   sweep is the easiest way to blow tokens with little marginal value.

## Suggested next step
Add a weekly `rtk gain` + ledger paid/free ratio line to the dashboard so savings are visible and
regressions get caught. Cheap to wire; makes the whole thing self-auditing.
