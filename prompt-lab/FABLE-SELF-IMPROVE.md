# Fable — design + build the SELF-IMPROVEMENT LOOP (do AFTER images are flowing)

Jeff wants Fable to function like a self-improving agent: auto-create skills + learn from past,
the way he imagines a Hermes agent does. It's not built into Claude Code — we build it. Design it
however is best; this is the spec, you own the implementation.

## Goal
A scheduled pass that turns experience into reusable assets, with no babysitting:
1. **Reflect:** read recent session transcripts in `~/.claude/projects/*/*.jsonl` (and the
   meeting.log / proposals / turn files) since the last run.
2. **Distill skills:** spot tasks done repeatedly or procedures that worked, and write/refresh
   `~/.claude/skills/<name>/SKILL.md` for them (you already started `skills-to-build.md`). New or
   risky skills land as drafts for Jeff; low-risk refinements can auto-apply.
3. **Learn:** update durable memory — the souls (`~/.hermes/*/brief.md`), `~/grokgo-context/SHARED.md`,
   and a running `~/grokgo/proposals/learnings.md` (what worked, what failed, what to stop doing).
4. **Report:** append a short dated entry to a log + ping altair with the 3-line summary so he can
   text Jeff "Fable learned X, made skill Y."

## Constraints
- Cheap: this is a reflection pass, not a chat. Use `claude -p` headless, small context, summarize
  transcripts rather than loading them whole. Cap tokens per run. Use **rtk** for all shell ops.
- Safe: never auto-post, auto-spend, or auto-change accounts. Draft risky skills; don't rewrite
  source-of-truth memory blindly — append + propose.
- Scheduled: launchd/cron (e.g. daily, or after N new transcripts). Self-throttling.

## Deliverables
- `~/grokgo/proposals/self-improvement-loop.md` (design + how it works)
- the implementation (script + launchd plist) when approved
- it becomes the `self-improve` skill so any agent can run a reflection pass.

## Also (token research — Jeff asked, heavily)
Confirm rtk is active (it is — PreToolUse hook `rtk hook claude`). Then research + propose OTHER
token savings for how we run Claude Code/agents: context compaction + `/clear` discipline, prompt
caching, smaller working context, routing sub-tasks to cheaper tiers, `--output-format json`,
summarize-then-act patterns, transcript pruning. Write `~/grokgo/proposals/token-savings.md` with
concrete, ranked wins (estimated % saved each).
