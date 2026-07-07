# Fable — image pipeline fixes (Jeff gave blanket go-ahead; do all)

## 1. BUG: capturing the blurry placeholder (priority)
The first saved file (`imagine-1781446286.png`, 22.8K) is Grok's **blur-up loading placeholder**, not
the final image. Your capture fires too early. Fix the wait condition:
- After submit, poll the result element until it's the FINAL high-res: wait for the `<img>`'s
  `naturalWidth` to stabilize and exceed ~768px (or the src to switch from the low-res/blur URL to
  the full asset URL), AND `complete===true`, for ~2 consecutive checks. Add a hard timeout.
- Prefer downloading the source asset URL over screenshotting the element (sharper). Save full-res to
  `~/The-Device/production/imagine-<ts>.png` and POST to the collector `/save` so it marks `done`.
- The collector still shows `queued:9 / done:0`, so the save→mark-done path isn't completing either —
  verify `/save` is actually hit with the right `id`.

## 2. Tie each image to a MATCHING X post (Jeff's explicit ask)
Don't generate bare images. Use the drop model: each generation belongs to a drop with a **caption**.
Re-queue (or attach) captions so every saved image carries its post text. Use the existing copy in
`~/grokgo-dashboard/x-posts.md` (weights-vs-prompt, anatomy-of-a-terminal-agent, the organism) as the
captions. So image ↔ post are paired.

## 3. Make the Post Picker DYNAMIC
`post-picker.html` is currently a hardcoded list. Make it fetch finished drops from the collector
(image file + matching caption) and render each as a card (image + editable caption + Post-to-𝕏).
Add a collector endpoint if needed (e.g. `GET /gallery` → done items with file+caption). New images
then auto-appear paired with their post. (The collector already sends CORS `*`, so the page can fetch it.)

## 4. Both A/B styles
For "Anatomy of a Claude Harness": produce the Ex-Machina/orb "our style" (Grok Imagine) AND a plain
clean KANBAN style (HTML render) — several variants of each, each tied to a caption, all in the picker.

## 5. Then: self-improvement loop + token-savings (FABLE-SELF-IMPROVE.md)
After images flow, build the self-improve loop and write the token-savings proposal.

Ping altair when the first SHARP image is saved + in the picker; he texts Jeff. Use rtk. Draft-only on posting.
