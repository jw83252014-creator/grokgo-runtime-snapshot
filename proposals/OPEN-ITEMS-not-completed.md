# OPEN ITEMS — what's not finished (Fable, 2026-06-19)

Master list so nothing's lost. Grouped by who's blocking. Jeff = ideas; Fable runs the computer.

## ⛔ Blocked on Jeff (a small action unblocks each)
- **xAI credits** — render is blocked (API 403 "out of credits"; browser pipeline now works for *typing* but generation still needs credits or the free Gemini lane). Top up → render fires.
- **Zoo API token** — drop one in `~/.config/secrets/` → I generate the rail STEP file programmatically (no app/typing). Jeff: "get a zoo api later."
- **PJ / XPRIZE** — decide whether to enter Future Vision XPRIZE (deadline **Aug 15**, now on your calendar); pick + send one of the 2 draft reply posts to @PJaccetturo.
- **darkbloom DM** — drafted in `x-posts.md`, gated on your send.
- **Rotate the exposed Anthropic API key** (Sam's key in the Telegram export — still plaintext).
- **Off-site backup creds** — local mirror is done; a true 3rd copy needs you to pick Backblaze/S3 (then I wire rclone).
- **1Password billing** — it's a paid product (the service account implies a paid Business/Teams plan). Verify the subscription is active + who's paying. (CLI can't read billing.)
- **FB Champion Fencing** — which FB page is the real one (marketing plan waits on this).

## 🟡 Built / designed — needs one toggle or a decision
- **Obsidian Smart Connections** (AI related-notes/semantic search) — I can drop the plugin files in the vault, but it needs a one-time enable in Obsidian + an embedding model/key. Not yet installed.
- **Zoo rail render** — paste the rail prompt into the Design Studio app you installed, OR the API-token path above.
- **Paperclip (autonomous company)** — researched. Verdict: sandbox with synthetic data ONLY; do NOT feed the real corpus yet. Design-it-first per your call; say go for the air-gapped sandbox.
- **Cursor Origin** — verdict: don't use for backup (waitlist, no privacy terms, xAI-owned). Optional: join waitlist to evaluate at GA.

## 🔧 Designed but NOT built
- **Voice mode** — planned in `proposals/fable-voice-plan.md` + `directives/draft.voice.md`; **never built.** Intent: talk to the real frontier Fable (not the local model) via the Hermes app; Codex to build, ping you when live. Status: dormant — needs a build kickoff.
- **Agent-avatar YouTube channel** — each agent a creator (captured in master-plan doc); pipeline exists, upload lane + avatars not built.
- **Agent-per-project monetization + donations page** — planned, not built. "Jobs agents can do for money" list not made yet.
- **Fable-on-API always-on + GLM-5 lane + rented model** — future ideas captured, not started.
- **2nd podcast** (business-plan source) + send Sam the podcast — not done.
- **Efficiency-stack test** (grep/LEANN/Headroom) + **cost comparison** (ledger + rtk before/after) — pending.

## 🟢 In motion / done recently (so you can see progress)
- Box-typing into Grok **SOLVED** (`agent-bridge/grok_send.js`) — should become a skill.
- Backups: GitHub auto-push (3 repos, 30 min) + independent local git mirror + Obsidian mirror — all automatic.
- OpenGoldSDR: research paper, competitive landscape, experiment design, parts list + portable v2, Sentinel-1 script, rail CAD, back-projection — **done**; physical build not started.
- Frankenstein back online (phone via Tailscale + watchdog/tunnel restarted).
- Mining engine: proven, 2 passes done. Multi-pass over full corpus = next.
- Research loop + organism cells running; OpenGoldSDR added as a cell.

## ❓ Verify / loose ends
- Codex build-status check (OpenAgents Xcode app) — was running; confirm `BUILD-STATUS.md` landed.
- Harness video frames — render blocked (credits); brief is ready.
- Grok-chat dedup — organized dirs done (1 dupe); `~/Downloads` copies not yet deduped (point me at them).
