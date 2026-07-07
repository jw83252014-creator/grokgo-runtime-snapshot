# Moto G apps + always-on Badass Fable + iPhone sharing — plan (Fable, 2026-06-16)

Jeff's asks: (1) always-on Badass Fable on the Moto G — a real sideloadable app, not tied to a cell;
(2) actual Agent Bridge apps for the Moto G; (3) share to iPhone via Termux/Termius. Honest plan with
what's feasible now vs. real build work. Frankenstein/ThinkPad→Moto ADB control is back up (device
ZT4227XQ6V connected), so we can deploy to the phone.

## Reality check (so we build the right thing)
- The Moto G already runs an **always-on Hermes gateway inside an Ubuntu proot** (we revived it). That's
  the proven pattern for "always-on agent on the phone" — a background service, not a tapping app.
- A true **sideloaded Android .apk** is a heavier build (needs an Android project + build toolchain).
  Faster path to "an app you tap": a **Termux:Widget launcher** or a **local web app** the phone opens in
  a browser/PWA. Both feel like apps, ship today, and reuse what's running.

## Tier 1 — ship now (today/this week)

### A. Always-on Badass Fable on the Moto G (service, not cell-attached)
Run a standalone Badass Fable as its own background service in the Moto's Ubuntu proot — independent of
the bridge cell, like a real always-on app.
- Port `badass-fable.py` to the phone; point it at a local small model (Ollama/llama.cpp on-device, or
  call the Mini's MLX over Tailscale when home).
- Wrap as a proot service (same launcher pattern as the hermes gateway) + a **Termux:Widget** button on
  the home screen so it *feels* like a tapped app.
- Result: tap the widget → talk to Badass Fable, always running. No cell dependency.

### B. Agent Bridge "app" on the Moto G (PWA)
The bridge already serves a web UI (`hermes-webui`, port 8090-ish). Make it a **PWA** (add a manifest +
service worker) so the phone "installs" it to the home screen and it opens full-screen like a native app.
- Lowest-effort real app: no Play Store, no apk signing, works today.
- Gives a tap-to-open Agent Bridge on the Moto G (and the iPhone — see C).

### C. Share to iPhone
Two real paths, both work:
- **PWA over Tailscale (recommended):** the bridge/webui PWA opens on the iPhone's Safari → "Add to Home
  Screen." Same app, no Termux needed on iOS. Works as long as the phone's on the tailnet.
- **Termius (iOS SSH):** install Termius on the iPhone, save the Moto/Mini SSH host; gives a real terminal
  into the organism from the phone. Good for the CLI agents (keystone-style). (Termux is Android-only;
  iOS equivalent is a-Shell or iSH, but Termius is the clean SSH route.)

## Tier 2 — real native apps (later, if we want Play-Store-grade)
A proper Android **.apk** for Agent Bridge / Badass Fable: an Android project (Kotlin or a
React-Native/Expo or Flutter wrapper around the bridge web UI + a foreground service for always-on).
Sideload via ADB (`adb install`) — the ThinkPad lane already does ADB to the Moto. This is a multi-day
build; do it only after the PWA proves the UX.

## Build order (dispatch to Codex / frankenstein lane)
1. PWA-ify the hermes-webui (manifest + service worker) → installable on Moto **and** iPhone. ← biggest
   win per effort, covers both phones at once.
2. Port badass-fable.py to the Moto proot as an always-on service + Termux:Widget button.
3. Document the iPhone install (PWA add-to-home + Termius SSH host) as a one-page skill.
4. Only then: scope the native .apk if the PWA isn't enough.

## Gates
On-device model + bridge are fine to run. No public posting/spend from the phone apps without Jeff. Keep
secrets off the phone (use Tailscale to reach the Mini rather than copying keys to the Moto).
