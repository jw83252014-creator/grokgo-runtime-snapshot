# Spec: Agent Bridge as a production macOS (SwiftUI) app

**Status:** DRAFT / feasibility + MVP spec. Date: 2026-06-14.
**Question from roadmap #3:** can the Agent Bridge become a production-ready macOS Xcode
(Swift/SwiftUI) app? **Answer: yes — as a notarized Developer-ID app, via a hybrid shell.**
Full native rewrite is not worth it now; the high-value native surface is *approvals +
notifications*, and that's a tight, shippable MVP.

## Verdict
- **Shippable:** Yes. SwiftUI macOS app, distributed as a **notarized DMG (Developer ID)**,
  not Mac App Store. Reason: the app must talk to / supervise a local HTTP server and bind a
  port — the MAS sandbox makes spawning Node + local networking painful. Direct-download +
  notarization avoids that and is standard for dev tools.
- **Don't rewrite the backend yet.** Keep `server.js` as the engine. The app is a native
  *client + supervisor* over the existing HTTP API. Porting to Swift (Vapor/Hummingbird) is
  a Phase-3 option, not MVP.
- **Prereq:** the P0 auth fix from the redesign proposal. A native approve button is only
  meaningful once `/api/approval/respond` is authenticated — otherwise the app is a pretty
  skin over an open gate.

## Architecture (hybrid: native shell + WKWebView + native approvals)
```
┌──────────────── BridgeApp (SwiftUI, menu-bar + window) ─────────────────┐
│  • Supervises the Node bridge process (Process / launchd), launch-at-login│
│  • Health poll → menu-bar dot (green/amber/red)                           │
│  • RoomView      = WKWebView → http://127.0.0.1:8787  (reuse all HTML)     │
│  • ApprovalsView = NATIVE SwiftUI list, decoded from GET /api/state        │
│       └ swipe / button → POST /api/approval/respond  (Bearer approver tok) │
│  • Local notifications on new pending approval → actionable Approve/Deny    │
│  • AgentsView    = native roster from /api/state (read-only at MVP)         │
└────────────────────────────────────────────────────────────────────────┘
        │ URLSession (JSON + SSE)                 │ manages
        ▼                                         ▼
   Agent Bridge HTTP API (:8787)            node app/server.js child process
```
- **What's native vs WKWebView:** room/chatter stays WebView (rich HTML already exists, low
  ROI to rebuild). Approvals + notifications go **fully native** — that's the product reason
  to have an app at all: Jeff approves from a Mac notification or a clean native inbox, with
  Face/Touch-ID-gated confirm, instead of curling an endpoint.
- **Transport:** `URLSession` to decode `/api/state`; switch to `GET /api/stream` (SSE, from
  the redesign) via `URLSession.bytes` for push once it exists. Poll fallback meanwhile.
- **Process supervision:** ship with a bundled or required Node; `Process` launches
  `server.js`, restarts on crash; or just adopt the existing launchd plist and have the app
  observe, not own. Observe-only is the safer MVP (no lifecycle bugs).

## MVP (smallest shippable, ~1 focused build)
1. Menu-bar app, launch-at-login, health dot from `GET /api/health` (add that endpoint).
2. Window with two tabs: **Room** (WKWebView) and **Approvals** (native).
3. Approvals list decoded from `/api/state.approvals` (pending first); tap → detail sheet
   (title, agent, proposed action, target, risk, reversible) → **Approve / Deny** POSTs with
   the approver Bearer token stored in Keychain.
4. Local notification when a new `pending` approval appears; notification actions Approve/Deny.
That alone turns the human gate from "Jeff must be at a terminal" into "Jeff taps a
notification" — the single biggest UX win, and it's small.

## Phase 2 / 3 (later, optional)
- P2: native Room (SSE-driven), native Agents management, attachment viewer.
- iOS companion: same SwiftUI/URLSession client pointed at the **Tailscale** URL
  (`100.89.238.84:8787`) — approve from the phone anywhere. (Most of the SwiftUI is reusable
  via a shared package; this is largely "free" once MVP exists.)
- P3: port `server.js` → Swift (Vapor/Hummingbird) for a single self-contained binary, no
  Node dependency. Only worth it if you want one notarized artifact with nothing external.

## Risks / honest caveats
- Bundling+supervising Node in a "production" app is the fiddly part — **mitigate by making
  MVP observe-only** (the bridge keeps running under its existing launchd; the app just
  connects). Add supervision later.
- Notarization needs an Apple Developer ID ($99/yr) — **account/spend item → Jeff's call.**
- This is a *local-trust* tool; do not widen exposure to ship the app. Keep writes
  token-gated and bound to localhost + Tailscale (see redesign P0).

## Recommendation
Do the redesign P0 (auth) first, add `/api/health` + `/api/stream`, then build the
**hybrid MVP** above. It's a real, notarizable macOS app, reuses everything already built,
and the native approvals + notification flow is the feature that justifies it. Full native
backend can wait.
