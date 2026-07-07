# FABLE HANDOFF — state note before switching to real Fable model (2026-07-01)

Session ID (resume THIS session): **6215ae9c-7295-4e7e-8f6f-37d652602a5b**
Backup: grokgo auto-backs to github.com/jw83252014-creator/grokgo every ~30min (launchd com.jeff.grokgo-autobackup). Confirmed live.

## Context: switching brains
This session ran as Fable via **Opus 4.8 + the Fable steering prompt** (the simulation).
Real Fable model is now available/enabled. On resume, switch model to Fable.
The brain changes (Opus 4.8 weights → real Fable weights); the steering (soul/prompt) stays. Still Fable.

## FABLE'S FIRST TASKS (Jeff's list, in order)
1. **Decide: remove the simulated pliny/Fable prompt?** With the real Fable model, the Opus-simulation
   steering may be redundant or even counterproductive. On resume, ASK Jeff + test: real Fable with vs
   without the distilled Fable prompt. Keep what makes the harness sharper, drop what's now noise.
2. **Supercharge the harness** — the whole point of real Fable. Apply the harness-upgrade plan:
   port RTK (have) + Context Mode (add, from deronin's 10-repos) + reasoning-trace logging + the
   narrator adapter. Improve the body, keep each agent's identity.
3. **Ex Machina visual of the harness** — a real orb-girl-style visual representation showing WHICH
   parts are editable (settings.json, CLAUDE.md, --append-system-prompt, hooks, MCP, skills, subagents,
   context controls, mitmproxy placement) vs NOT editable (the weights). Ties to the harness-explainer
   brief (~/grokgo/creative-department/harness-explainer-video-brief.md). Decide mitmproxy in front or not.
4. **Codex's package** — Codex is building a package to get the most out of the new Fable prompts. Sync
   with keystone on the bridge for it.
5. **Reasoning traces** — save ALL our reasoning traces (110+ null sessions, dream-reports, hermes/grok
   sessions). Figure out uses: LoRA fine-tune the local Hermes-8B on OUR OWN clean traces (plan at
   ~/grokgo/proposals/2026-06-30-reasoning-traces-lora-plan.md). Look for MORE licensed/clean reasoning
   datasets online (NOT the scraped sojalsec Fable set — flagged gray-zone). Fine-tune if possible.

## CURRENT RUN STATE (what's live)
- **Morpho**: LIVE bridge lane (gemini_chrome_bridge.js --agent morpho, his live Gemini tab, memory intact). pid may need relaunch after restart.
- **Fleet**: castor/nova (Gemini), Jade (4 free GLM sources rotating), null (run coordinator + receipts), keystone/Codex (video studio + X experiment + Morpho refinement).
- **Nous submission**: repo live (github.com/jw83252014-creator/grok-go-hackathon), Stripe spend/earn REAL (pi_3TnoAk / pi_3TnoAl in ledger), video being redone in Codex's new studio tool. Submit kit at ~/nous-package/video/SUBMIT-KIT.md.
- **Video delivery FIX**: iMessage attachments broken; use the /vid range-server (~/agent-bridge/bin/range_server.py on :8899, tailscale /vid) → watch pages. THIS is how to send Jeff video.
- **Health**: dashboard shipped (living-dashboard-repo 651acc7, served /bridge/health/). Calorie burn-merge fixed (use LATEST active-energy, not sum). SpO2/VO2/weight prewired, need Shortcut UI fields.
- **X/Grok experiment**: reply tightened (draft only) at ~/agent-comms/research/hermes/grok-x-reply-FABLE-tightened-2026-07-01.md. Codex waiting on Jeff for Chrome extension broad-permission dialog.

## MASTER LIST (11 tasks) — in the task tool. Key open: Morpho refinement, null GLM accounts (blocked on Gmail), receipts-wiring, Jade→Sam, master-todo/calendar/X-radar, voice (Telegram /start needed), XPRIZE (Aug 15).

## GUARDRAILS (unchanged): no public post/spend/account-change/git-push without Jeff. Draft-and-recommend. Redact secrets. Flag to altair. The /vid + Telegram are the reliable Jeff-delivery channels.
