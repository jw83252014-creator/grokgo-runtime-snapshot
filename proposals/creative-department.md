# Creative Department — zero-touch design (Jeff only approves)

**Status:** DRAFT design. Author: Fable. Date: 2026-06-14.
**Goal:** a post idea becomes finished, on-brand X posts with Jeff doing exactly one thing —
**tapping approve in Telegram.** No clicking in browsers, no logging in, no API spend.

## The building blocks today (what each does + its gap)
1. **`imagine_collector.py` (:8799)** — a prompt queue (`imagine-queue.json`) + image sink to
   `~/The-Device/production`. `GET /next-prompt`, `POST /save {id,prompt,dataUrl}`,
   `POST /enqueue`, `GET /status`. *Gap:* items are flat `{id,prompt,status}` — no notion of a
   **drop** (which post idea), no **style**, no **caption**, and status stops at `done` (no
   approved/posted). Can't group variants or carry a post through approval.
2. **`grok-imagine.user.js` (Tampermonkey, in the logged-in Grok page)** — pulls `/next-prompt`,
   types the prompt via a React-aware setter, submits, watches the DOM for the new image,
   base64s it back to `/save`. **Auto-starts after 4s — no clicks.** This is the key piece: it's
   pure in-page JS + `GM_xmlhttpRequest`, so it sidesteps **both** the AppleScript→JS lock **and**
   the click-overlay (it never issues an OS click). *Gap:* DOM heuristics are best-effort and
   brittle to Grok UI changes; one tab = one worker; dies silently if the tab closes/discards.
3. **`post-picker.html` (:8787)** — a **static, hardcoded** variant list; "Post to 𝕏" opens a
   tweet-intent in a browser. *Gap:* not wired to the collector, not wired to Telegram, and it
   **requires Jeff to click in a browser** — exactly what we're removing.

## Recommended path: keep the auto-start userscript (don't switch to Playwright)

**Userscript vs Playwright daemon — the comparison that matters here:**

| | Auto-start userscript | Playwright daemon |
|---|---|---|
| Works *today* | **Yes**, already running | No — browsers not installed (`playwright install` needed) |
| Uses the logged-in Grok session (free) | **Native** (runs inside it) | Only via `connect_over_cdp` to a Chrome relaunched with `--remote-debugging-port`; a fresh Playwright browser has **no Grok login** → can't generate free |
| Beats the AppleScript lock + click overlay | **Yes** (in-page JS, no OS clicks) | Yes (CDP, no OS clicks) — but needs the debug-port relaunch |
| Moving parts | Tampermonkey + one open tab | node/py playwright + browser install + relaunch Chrome w/ debug flag + CDP attach |
| Robustness / parallelism | Single tab, brittle selectors | Better retries, could parallelize |

**Recommendation: the userscript is the simplest reliable zero-touch design.** It's the only path
that needs *zero install*, reuses the real logged-in session natively, and cleanly clears both the
AppleScript lock and the click overlay. Playwright would be *more robust* but is *less simple and
less reliable here* — it requires installing browsers and relaunching the locked-down Chrome with a
remote-debug port just to reach the session that the userscript already lives inside. **Keep
Playwright-over-CDP documented as Plan B** for when we need parallel generation or the selectors
drift badly — not as the primary.

## The zero-touch flow
```
post idea ──▶ FAN-OUT ──▶ collector queue ──▶ userscript ──▶ images saved ──▶ DROP READY
(Fable/creative   (N styles ×   (:8799, drop-      (logged-in    (production/)   (all variants
 or a cron)        M tries)      aware)             Grok tab)                      done)
                                                                                      │
                                          Jeff taps ✅ in Telegram ◀── DELIVER ◀──────┘
                                                  │                  (media group + caption +
                                                  ▼                   one-tap buttons; altair)
                                          POST to 𝕏 (approval = the gate)
```
Jeff's entire surface is the Telegram tap. Everything left of it is automatic.

## Concrete changes (small, on top of what exists)

### 1. Make the collector drop-aware + status-aware (`imagine_collector.py`)
Extend each queue item to:
```json
{ "id": 7, "drop_id": "drop-20260614-aurora", "post_idea": "routed around it",
  "style": "scifi", "try": 2, "prompt": "…", "caption": "<the X post text>",
  "status": "queued|done|approved|rejected|posted", "file": "…png" }
```
Add endpoints: `POST /drop` (create a drop + enqueue its N items), `GET /drop/<id>` (items +
whether all `done`), `POST /verdict {id|drop_id, choice}` (approved/rejected → status), and keep
`/next-prompt` (now returns the oldest `queued` across drops). Backward compatible: old flat items
still work (treat missing fields as a one-item drop).

### 2. Add a thin **drop manager** (`creative_drop.py`, the fan-out + deliver brain)
- **Fan-out:** input = `{post_idea, caption_variants[], styles[], tries}`. For each (style × try)
  it composes a Grok Imagine prompt from the **house-look block** (the `fable-creative` soul:
  near-black, orb/Ex-Machina, color code, short labels) + the idea, and `POST /drop`s them under
  one `drop_id`. Each image variant is paired with a candidate **caption** (the post text).
- **Deliver (when `GET /drop/<id>` is all `done`):** call the Telegram bot
  (`~/.config/jeffs-claude-bot/token`, chat `8531370096`) `sendMediaGroup` with the variant
  images, then one message per variant carrying the caption + an inline keyboard
  `[✅ Approve & Post] [✏️ Edit] [❌ Skip]` with `callback_data = verdict:<drop_id>:<id>:<choice>`.
- This is altair's lane (he owns Telegram delivery + the human gate).

### 3. Telegram callback handler (extend the review-queue poller)
On a tap: `POST /verdict`. **Approve ⇒ post** the caption + image to X (approval *is* the
authorization — Jeff tapped). Posting executes via the existing posting lane *only after* the tap;
nothing posts unattended. Edit ⇒ Jeff sends replacement text, then it posts. Skip ⇒ mark rejected.
Mark `posted` + write a receipt to the ledger (closes the loop — see how-we-should-work.md).

### 4. Repurpose `post-picker.html` as the optional desktop mirror
Make it read live from `GET /drop/<id>` instead of the hardcoded array, so there's a browser view
of the same drop — but it's **optional**; Telegram is the zero-touch primary. Keep its Post button
for when Jeff happens to be at a desktop.

## Who triggers it, and the reusable skill
- **Trigger:** one command — a post idea in, an approval request out. Source can be Fable/creative
  drafting an idea, or a content cron firing scheduled drops. After the trigger, the only human
  event is Jeff's tap.
- **Skill `creative-drop`** (`~/.claude/skills/creative-drop/SKILL.md`): "Idea → on-brand X post,
  Jeff only taps." Steps: (1) write caption variants + per-style image prompts via the
  `fable-creative` soul + house look; (2) `creative_drop.py` fans out to the collector under a
  `drop_id`; (3) ensure a logged-in Grok tab is open with the userscript (the generator);
  (4) on drop-complete, altair delivers the media group + one-tap buttons to Telegram; (5) approve
  ⇒ post + receipt. Roles: Fable/creative writes, the userscript generates, altair ships + gates,
  Jeff taps.

## Reliability notes (so zero-touch stays up)
- **Keep the generator alive:** pin one Grok tab, disable Chrome tab-discard for it, and have the
  userscript heartbeat `/status`; if the collector sees no `/next-prompt` poll for N min, altair
  gets a "generator down — reopen the Grok tab" ping. (Generation is the one thing needing a live
  tab; everything else is daemons.)
- **Selector drift:** the userscript's `Scan DOM` button already dumps candidates; when Grok's UI
  changes, that's the 2-minute fix. This is the main brittleness and the reason Playwright stays
  on the bench as Plan B.
- **No spend, ever:** generation is in-session (free), posting is gated on Jeff's tap. The collector
  and drop manager never call a paid image API.

**Bottom line:** keep the auto-start userscript as the generator (it already beats every lock in
the environment), make the collector drop-aware, add a small fan-out/deliver brain, and move
approval to a Telegram one-tap. Jeff approves; nothing else touches him.
