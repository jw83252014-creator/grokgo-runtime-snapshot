# Self-Improvement Loop — design (Fable, 2026-06-14)

Jeff wants Fable to behave like a self-improving agent: turn experience into reusable assets with
no babysitting. Claude Code doesn't do this natively — we build it as a scheduled reflection pass.
This doc is the design; the script + launchd plist ship as **drafts** (nothing scheduled runs until
Jeff approves). It also becomes the `self-improve` skill so any agent can run a pass on demand.

## Shape in one line
A cheap, throttled, append-only reflection pass: read what's new since last run → distill skills +
learnings → write low-risk assets, propose risky ones → log + ping altair.

## The pass (4 stages)

**0. Gate / throttle.** Read state `~/grokgo/.self-improve-state.json` (`last_run_ts`, `last_count`).
Count transcripts in `~/.claude/projects/*/*.jsonl` newer than `last_run_ts`. If `< MIN_NEW` (default 5),
exit 0 silently. This makes it safe to schedule often — it only spends when there's enough new material.

**1. Reflect (cheap digest, not raw dump).** For each new/changed transcript, extract a compact
signal with `jq` — user message texts (truncated), tool names used, and any `FAIL`/error lines — not
the whole JSONL. Concatenate into one digest capped at `MAX_DIGEST_CHARS` (default 60k). Summarizing
rather than loading whole is the main cost control.

**2. Distill (one headless model call).** Feed the digest to `claude -p` (headless, `--output-format
json`) with a strict-JSON instruction asking for three lists:
- `skills`: recurring tasks/procedures worth a `SKILL.md` — each `{name, description, risk: low|risky, body}`.
- `learnings`: `{what_worked, what_failed, stop_doing}` — short.
- `memory`: proposed appends to souls / SHARED.md — each `{target, append}`.
One call keeps it cheap; the digest is already condensed.

**3. Apply (low-risk auto, risky → draft).**
- `skills[].risk == low` → write/refresh `~/.claude/skills/<name>/SKILL.md` (auto).
- `skills[].risk == risky` OR new top-level skill → `~/grokgo/proposals/skills/<name>-DRAFT.md` (Jeff-gated).
- `learnings` → **append** to `~/grokgo/proposals/learnings.md` (never overwrite).
- `memory` → **append** a dated proposal block to `~/grokgo/proposals/memory-proposals.md`; never blind-edit
  `brief.md` / `SHARED.md` (those are source-of-truth, human-gated).

**4. Report.** Append a dated entry to `~/grokgo/proposals/self-improve-log.md`; POST a 3-line summary
to the Agent Bridge (`/api/say` as `fable`) tagging altair so he can text Jeff "Fable learned X, made
skill Y." Write new `last_run_ts` to state.

## Constraints honored
- **Cheap:** throttle gate; jq-digest not raw transcripts; one model call; `MAX_DIGEST_CHARS` + `MAX_NEW`
  caps; rtk for all shell ops. Est. a few cents/run at most.
- **Safe:** never auto-post / auto-spend / auto-account. Risky skills are drafts. Source-of-truth memory
  is append-as-proposal only. Low-risk auto-apply is limited to skill files under `~/.claude/skills/`.
- **Scheduled + self-throttling:** launchd `com.jeff.fable-self-improve` (daily 09:00, draft). The gate
  means a no-op when there's little new.

## Files
- `~/grokgo/self-improve.sh` — the pass (draft, executable, not scheduled).
- `~/grokgo/com.jeff.fable-self-improve.plist` — launchd (draft; `launchctl load` only after approval).
- `~/.claude/skills/self-improve/SKILL.md` — run a pass on demand from any lane.
- State: `~/grokgo/.self-improve-state.json`. Outputs: `proposals/learnings.md`,
  `proposals/memory-proposals.md`, `proposals/skills/*-DRAFT.md`, `proposals/self-improve-log.md`.

## Enable (after Jeff approves)
```
launchctl load ~/grokgo/com.jeff.fable-self-improve.plist   # schedule it
~/grokgo/self-improve.sh --once                             # or run one pass by hand
```
Disable: `launchctl unload …`. Dry-run: `self-improve.sh --dry` (prints, writes nothing).
