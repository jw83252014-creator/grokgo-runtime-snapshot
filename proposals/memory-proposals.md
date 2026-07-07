
## 2026-06-19 (proposed — Jeff to apply)
- `soul:agent-roster` → Running 5-agent team: Frankenstein (Moto G Hermes), null/nullaxiom0 (Hermes), Vega (Mac mini Opus 4.8), Grok (video creative), Keystone (onboarding/coordination)
- `soul:multi-provider-strategy` → Rotating between Anthropic (Opus 4.8), ChatGPT (jeffw58325 codex subscription), OpenClaw gateway — plan: unified auth aggregator with one-button provider switching
- `soul:hermes-remote-deployment` → Pattern: SSH into Termux → sshd + wake-lock enable → Tailscale → launchd watchdog monitors connectivity, survives reboots
- `soul:creative-video-production` → Grok Imagine + stitch pipeline for social video; creative briefs in Downloads; director role leads team on X content strategy

## 2026-06-21 (proposed — Jeff to apply)
- `SHARED.md` → SECURITY: 3 exposed API keys in transcripts 66c5db57, 33598ea4, 8131d3c4 — redact before sharing; audit account access; implement secret detection pre-surface
- `soul:Vega` → Computer-use clicks fail ~75% of attempts — fallback to Bash/SSH/terminal; gh auth is a consistent blocker
- `soul:Fable` → CDP Grok-Imagine timeouts are recurring — increase timeout or add exponential backoff in cdp_drive.js; Monitor + ScheduleWakeup polling works
- `soul:Hermes` → Hermes agent multi-provider switching (Grok/X/claude/openclaw/OpenAI Codex) needs centralized auth hub — current manual reauth is error-prone

## 2026-06-22 (proposed — Jeff to apply)
- `SHARED.md` → jw83 has 11:10 wall-clock deadline on 2026-06-22 for auto-replies live; clock beats feature parity
- `SHARED.md` → CDP driver Grok-Imagine 1-image renders timeout repeatedly; investigate actual render latency vs configured timeout threshold

## 2026-06-30 (proposed — Jeff to apply)
- `SHARED.md` → free-GLM sources (~/.config/jade-e) prioritized before paid models in brain routing; mentioned in 9963d28a but not integrated
- `SHARED.md` → Receipts schema at ~/null-command-center/schemas; load-bearing for multi-agent git-coordination auditability (agent-acbf762399)

## 2026-07-01 (proposed — Jeff to apply)
- `SHARED.md` → CDP driver polling: when ScheduleWakeup checks return timeout/no-results repeatedly, escalate to debug mode (verbose logs, connection checks) before next retry cycle

## 2026-07-03 (proposed — Jeff to apply)
- `project:grokgo-cdp-driver` → CDP Grok Imagine driver (~/agent-bridge/cdp_drive.js) experiencing consistent timeouts and 'no results captured' failures in batch mode — investigate headless browser session lifetime or Job queue semantics
- `reference:agent-bridge` → Agent Bridge at 127.0.0.1:8787 is coordination hub; room messages logged; receipts (run history + budget) in ~/agent-comms/receipts/*.json — primary source of truth for multi-agent state
