
## 2026-06-19
- **Worked:** RTK (Rust Token Killer) consistently saving 60-90% on CLI operations via hooks
- **Worked:** Hermes agent deployment to Moto G via SSH+Tailscale survives reboots with launchd watchdog
- **Worked:** Agent Bridge hub coordinates 5+ autonomous agents (Frankenstein, null, Vega, Grok, Keystone)
- **Worked:** File-based IPC via meeting.log for async multi-agent coordination
- **Worked:** Telegram bridging enables mobile command/control of headless Hermes agents
- **Failed:** Opus 4.8 not selectable in /model despite availability in iOS app — required terminal restart
- **Failed:** OpenClaw gateway auth expired; fallback to ChatGPT immediately hit rate limits
- **Failed:** Frankenstein watchdog posting stale THINKPAD_PATH_DOWN every ~31min when offline
- **Failed:** Moto G connectivity via scrcpy/Tailscale flaky, multiple device reboots needed
- **Failed:** OpenClaw config rate limiting or cooldown mode causes 'something went wrong' errors

## 2026-06-20
- **Worked:** Adversarial attack methodology on infrastructure (CI/merge blockers) — multi-angle probing for hidden failure modes
- **Worked:** Reading actual implementation code (brakes.py, review_queue.py) to answer honest 'does this already exist' questions
- **Worked:** Structured iteration on CDP drivers: test 1-image locally, verify output in gallery, then batch; catch timeouts early
- **Worked:** WebSearch + WebFetch pipeline for bounty/research context gathering
- **Failed:** CI cost-lever approaches (grouping PRs, merge trains) — hit queue deadlock + silent re-serialization repeatedly
- **Failed:** cdp_drive.js timeout/setup errors persisted across multiple debug cycles — timeouts kept recur without root cause isolation
- **Failed:** Retrying same merge coordination strategies without architectural pivot
- **Stop doing:** Silent failures in critical paths (|| true on queue creation killed debugging visibility)
- **Stop doing:** Assume merge queue + branch protection alone solve parallel-agent coordination — they don't (evidence: repeated failures)
- **Stop doing:** Skip reading implementation when making claims — claim vs reality diverged multiple times

## 2026-06-21
- **Worked:** RTK (Rust Token Killer) for token savings — used consistently across sessions
- **Worked:** Agent Bridge coordination for multi-agent dispatch (Vega, Grok, null_axiom_0)
- **Worked:** ScheduleWakeup polling for async tasks (Fable image pipeline retries)
- **Failed:** Computer-use clicks flaky — coordinate-landing failures 6/8 attempts (53f883f4, 8131d3c4)
- **Failed:** gh auth blockers on GitHub operations (53f883f4)
- **Failed:** CDP Grok-Imagine timeouts recurring — 'no results captured' pattern (6215ae9c)
- **Failed:** Openclaw auth workflow too complex — multi-step reauth, confusion (33598ea4)
- **Failed:** Server token config missing blocker (agent-a35eda64)
- **Failed:** Launchd watchdog log parsing crashes (544131a9)
- **Stop doing:** Posting API keys in chat / git — 3 exposed secrets in recent sessions; audit account access
- **Stop doing:** Using computer-use clicks for critical paths — use Bash/terminal instead (too flaky)
- **Stop doing:** Manual multi-provider reauthentication — needs centralized auth hub (OpenAI Codex, Anthropic, claude oauth reauth)

## 2026-06-22
- **Worked:** ScheduleWakeup + polling for long-running async tasks (CDP image render tests)
- **Worked:** Bash scripting for SSH remote config edits (Hermes agent account switching pattern)
- **Worked:** Disk-based state handoff + Read before deciding next steps
- **Failed:** CDP Grok-Imagine driver timing out on 1-image render (multiple retries, no image capture or save)
- **Failed:** Auto-replies toggle source not found despite repo + launchd search
- **Stop doing:** Never surface API tokens/secrets in chat — redact snsTOOag*... patterns before any response (session 66c5db57 exposed a token)

## 2026-06-30
- **Worked:** Read real files before technical writing for accuracy (hackathon synthesis agents did this well)
- **Worked:** ScheduleWakeup polling for task results without burning cache (6215ae9c checking cdp_drive.js)
- **Worked:** Monitor for streaming long-running processes (6215ae9c Grok-Imagine pipeline)
- **Failed:** Encoding/escaping issues in agent terminal output (repeated parse failures across agent-af4d5984, agent-acbf762399, agent-a21f7d30, agent-a1bef9bed7353dfb7, 6215ae9c)
- **Failed:** free-GLM cost-cut layer exists but not surfaced in routing logic (9963d28a mentions ~/.config/jade-e with no integration points)
- **Failed:** Task tracking path resolution errors (6215ae9c repeated FAIL on task_path.name)

## 2026-07-01
- **Worked:** ScheduleWakeup + Bash polling loop for async task status checks
- **Failed:** cdp_drive.js image generation: repeated timeout/no-results errors despite multiple retry attempts
- **Failed:** Error messages truncated in digest; root cause unclear (CDP connection, Grok timeout, or script logic)
- **Stop doing:** Blind retry loops on timeout without investigating underlying cause — the cdp work failed 7+ times with the same error

## 2026-07-03
- **Worked:** Agent reconnaissance (reading configs, receipts, memory homes from ~/.hermes-*/, ~/agent-comms/)
- **Worked:** Multi-agent coordination via disk files and Agent Bridge at 127.0.0.1:8787
- **Worked:** Structured output for agent summaries (all recon agents returned StructuredOutput successfully)
- **Worked:** Mac mini desktop automation with computer-use batch commands (10-20 per batch worked when coordinates verified)
- **Failed:** GitHub CLI auth (multiple sessions: 'check gh auth' — needs pre-check or reauth flow)
- **Failed:** GUI automation via computer-use (click coordinates landed on wrong elements consistently — may need screen boundary recalc)
- **Failed:** Grok account handling (06-30 relogin_required across lanes — credential/session timeout issue)
- **Failed:** CDP Grok Imagine image driver (setup timeouts, 'no results captured', likely CDP/browser timeout in headless context)
- **Stop doing:** Blind computer-use clicks without screen bounds verification (failures suggest coordinate formula drift)
- **Stop doing:** Assuming gh auth state without pre-check (fails silently in batch workflows)
- **Stop doing:** Retrying CDP image pipeline on timeout — driver needs architectural review before scaling
