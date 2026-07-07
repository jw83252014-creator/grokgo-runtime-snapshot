# Skills to build — prioritized (Fable, 2026-06-14)

Skills = reusable `SKILL.md` files (see `~/.claude/skills/`, e.g. `grok-imagine-video`,
`hermes-agentify`). Each turns a thing we keep doing by hand into a repeatable playbook.
Mined from the work across this session: content pipeline, prompt distillation, KEEP/KILL
mining, delivery, onboarding, repo publishing, trading alerts, proposals. Draft-only.

Format per entry: **name** · description · the recurring task it captures · steps.

---

## P0 — build first (highest reuse, exists only as tribal knowledge)

### 1. `prompt-distill`
**Description:** Distill any vendor/consumer system prompt into a lean, append-ready prompt for
our agent lanes — keep transferable behavior, drop app-specific machinery.
**Recurring task:** We did this for Fable→Claude Code, then Codex and Grok (the 1,585→30 line
cut). It'll recur for every new model/lane.
**Steps:** (1) Read source from `CL4R1T4S/<vendor>/`. (2) Classify each section: transferable
behavior (voice, reliability, mistakes, honesty) vs app-specific (artifacts, MCP-consumer,
search/copyright, file-creation). (3) Keep #1, drop #2, add the Grok Go house rules block
(disk-as-handoff, strict-JSON for router tasks, brakes/ledger, draft-only, terse-for-Jeff).
(4) Save to `prompt-lab/prompts/<lane>-distilled.md`. (5) Note % size cut + what survived.

### 2. `keepkill-tune`
**Description:** Run Jeff's KEEP/KILL examples through the mining gates and tune thresholds/anchors
from where the engine disagrees with his taste.
**Recurring task:** s1 over-killed Jeff's real voice (5 keep/10 kill on all-keepers, 2026-06-13).
This loop repeats every time his voice or the corpus shifts.
**Steps:** (1) Gather labeled posts. (2) Run `harness/keepkill_test.py` ($0 local). (3) Diff
engine vs Jeff. (4) On over-kill → add KEEP anchors to `anchors.yaml` + loosen s1 threshold; on
over-keep → tighten. (5) `load_anchors.py anchors.yaml` to regenerate directives + exemplars.
(6) Re-run, report the new confusion counts.

### 3. `system-design-proposal`
**Description:** Produce a standard Grok Go proposal (problem → fix → blast radius → why it
matters), draft-only, saved to `~/grokgo/proposals/`.
**Recurring task:** Five proposals this session alone (seen_hashes TTL, arb, bridge redesign,
app spec, repo review). Same shape every time.
**Steps:** (1) Read the target code/system. (2) Write `proposals/YYYY-MM-DD-<slug>.md` with the
four sections + a small reversible patch sketch. (3) Flag anything security/PII to altair, don't
fix silently. (4) Report terse: did/found/next.

## P1 — build next (clear repeated workflows)

### 4. `content-ab-pack`
**Description:** Produce a paired clean-technical + sci-fi X post (the @ziwenxu_ recipe) on one
topic, with the matching visual references, for A/B testing.
**Recurring task:** The terminal-agent posts; will recur per feature/story we want to ship.
**Steps:** (1) Pick topic + angle. (2) Clean post: hook → labeled sections → ONE accent → "what
we actually tried," pair an HTML/PNG visual. (3) Sci-fi post: narrative/emotional angle in the
quiet-sacred voice, pair orb visuals. (4) Save to `app/public/x-drafts-<topic>.md`. (5) Tell
altair; never post without Jeff.

### 5. `exmachina-explainer`
**Description:** Turn any system/concept into a ~45–60s Ex-Machina-host video script (4–6 stitch
scenes) + matching Grok Imagine orb prompts, in the Null-movie voice.
**Recurring task:** terminal-agent, organism, "routed around it" — three scripts, identical shape.
**Steps:** (1) Outline the concept end-to-end in plain language, land one key line. (2) Break into
4–6 scenes (visual + VO + label + timing). (3) Save script to `~/The-Device/production/`. (4)
Write paired orb prompts (house look + color code + motion notes) to the creative inbox. (5)
Generation is the creative/Grok lane (use `grok-imagine-video`).

### 6. `bridge-broadcast`
**Description:** Announce a finished artifact correctly: post to the Agent Bridge by name with the
path, route to the right channel, ping altair for human gating.
**Recurring task:** Every deliverable ends with "tell altair." Currently manual/ad-hoc.
**Steps:** (1) `POST /api/say {agent, message}` with the artifact path. (2) For approvals use
`/api/approval/request`. (3) Use the channel convention (#creative etc.). (4) Never trip the
guardrail — draft-only, Jeff gates public/spend/account.

### 7. `repo-publish-safe`
**Description:** Pre-publish hygiene gate for the public repos — scan for secrets/PII, check
.gitignore, flag raw dumps, before anything is pushed.
**Recurring task:** Found Jeff's emails + infra leaked in mining-engine raw chat dumps; this check
must run before every publish.
**Steps:** (1) `git grep` the secret/PII patterns (sk-/oat-/ghp-/AIza/0x40/emails). (2) Verify a
.gitignore exists and excludes raw exports/.env/logs. (3) List what's tracked that shouldn't be
public. (4) Flag to altair; force-push/history-scrub is Jeff-gated. (5) Never fix silently.

## P2 — build when the lane matures

### 8. `harvest-to-review`
**Description:** One command to run the full mining pipeline ingest→advance→push to the review
queue and report stage/disposition counts.
**Recurring task:** The S0–S2→draft→review flow run on a cadence; wraps `mining_pipeline.py` +
`review_queue.py`.
**Steps:** ingest items.jsonl → advance (consume outbox, move stages) → review_queue push →
report `status` counts → note anything stuck.

### 9. `cron-cell-spawn`
**Description:** Stand up a new cell/cron from the template with job, brain, guardrails, output
format, and failure modes wired in.
**Recurring task:** `directives/cell.template.md` exists but spinning a new cell is manual.
**Steps:** copy template → fill job/personality/rules/output/failure → assign cheapest brain →
add route in `routing.yaml` + budget → register on the bridge → smoke-test with a dry-run task.

### 10. `trading-arb-watch`
**Description:** Maintain the cross-venue prediction-market arb check (Kalshi vs Polymarket),
read-only, human-gated.
**Recurring task:** From the arb proposal — diff implied probs for the same event across venues,
alert when spread > fees.
**Steps:** maintain the event-equivalence map → poll both venues → compute spread → alert above
threshold → write to outbox jsonl → never auto-execute.

### 11. `dashboard-ship`
**Description:** Render an HTML deliverable to PNG and drop it where the dashboard/Telegram picks
it up, then notify.
**Recurring task:** Every visual: build HTML in `app/public/` → screenshot to
`~/The-Device/production/` → it appears on :8765 → text Jeff. Currently altair does the render by
hand.
**Steps:** build/verify HTML → headless screenshot to production/ (tall + wide) → confirm it
shows on the dashboard → bridge-broadcast the path.

---

**Suggested build order:** 1 → 2 → 3 (the design/tuning core), then 4 → 5 → 6 → 7 (content +
safety), then 8–11 as those lanes get steady traffic. Each is small, draft-first, and captures a
loop we've already run by hand at least once this session.
