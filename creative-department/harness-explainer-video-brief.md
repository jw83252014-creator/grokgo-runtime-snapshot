# Harness Explainer — Production Brief (TWO style variants)

**Status:** DRAFT for the creative / Grok lane to RENDER. Author: creative dept. Date: 2026-06-18.
**Source of truth (content):** `proposals/claude-harness-paper-plan.md` + `proposals/claude-harness-research-notes.md` + `proposals/claude-harness-paper.md`. Nothing here is invented; all specifics trace to those.
**House look:** near-black `#070b11`, volumetric haze, soft bloom. Color code (use consistently):
**teal = local / your terminal · amber = the wire / model call · violet = the weights (the intelligence) · red-coral = risk / wiretap.**
Keep on-screen label text SHORT — Grok Imagine garbles dense type. Put precise labels/snippets in a clean HTML/Figma overlay pass, NOT baked into the generated frame.

**Thesis the whole piece serves (one line, from the paper):**
> The intelligence is the weights. Everything you can touch is the harness around them — and all of it is editable from your own machine.
Plain restatement: *You don't need a bigger model, you need a better harness.*

**CLEAN-ROOM RULE (binding):** every frame, line of VO, and on-screen string here is built from our own owned notes. We do NOT quote, embed, or paraphrase any leaked/pliny system-prompt text. The only verbatim code shown is our own (the `--append-system-prompt-file` command from our `cc-with-prompt.sh`, our `settings.json` hook line). This is RENDER-READY but **draft-only** — nothing renders, posts, or spends without Jeff.

**Tech beats both variants must land (from the research):**
1. **Tiered routing** — most work routes to free brains (GitHub Models + Gemini); the frontier model is reserved for hard calls. A ledger + brakes mean most tasks never touch a paid API.
2. **rtk token compression** — the Rust Token Killer, a `PreToolUse` hook that rewrites every shell call and compresses noisy output 60–90%.
3. **Headroom / context compression** — `/clear` discipline, compaction, prompt-distillation (1585-line consumer prompt → ~30 lines, ~98% cut), prompt caching. (Brief's name for the §4 context story; "Headroom" = the freed context budget.)
4. **The Agent Bridge** — the local bus where agents announce work and hand off (`:8787` #creative, the drop pipeline, Telegram gate).
5. **The living organism** — cells (parallel small minds) + a research/subconscious layer + a conscious face, addressable as one fleet. Tied to the paper's "production agent = harness hygiene + cost control + inspectability + reusable skills, in a fleet."

Two style variants follow. Each is self-contained: logline, shot list (visual + on-screen/VO), and a paste-ready Grok Imagine prompt per shot in that style. Pick one to render, or A/B both.

---

# VARIANT A — "EX MACHINA"

Cinematic, sleek, A24-ish. The harness rendered as an emergent **being** — three cybernetic avatars (Cells / Research / Conscious) who introduce themselves and merge into one organism. Moody, glass, volumetric light, slow push-ins. Soft teal/blue with amber filament accents; violet only for the weights core. VO is sparse, half-whispered, confident. Target ~75–90s.

**Logline:**
*An intelligence wakes inside a black-glass room and explains itself: the genius is a violet core no one can touch — everything you see her wear, route, and remember is the harness, and all of it is yours to edit.*

### Shot list (visual + on-screen text / VO beat)

**A1 — Cold open: static → reveal.**
Visual: 2s analog static + scanlines on near-black, a digital flash, then a single teal terminal-cursor blinking alone in the void.
VO (whisper): "You think the secret is the prompt. The secret is everything around it."
On-screen: *(none — let the cursor breathe)*

**A2 — The Cells wake.**
Visual: thousands of tiny teal orbs drift up out of the dark, each pulsing on its own clock, some specializing and clustering — a body assembling from small minds.
VO: "We are the cells. Many small minds, each with one job. Alone, simple. Together, a living system."
On-screen (short): `THE CELLS`

**A3 — Tiered routing as a nervous system.**
Visual: most cells light up cool/dim (free brains) and route work laterally among themselves; only a rare hard signal escalates upward as a single bright amber filament toward a distant violet glow.
VO: "Most thoughts never leave the body. Only the hard ones reach for the core."
On-screen (short): `ROUTE CHEAP · ESCALATE RARELY`

**A4 — The Research Layer (subconscious) rises.**
Visual: a second avatar — a calm cybernetic woman half-dissolved into floating memory-orbs and data threads — integrates drifting fragments into herself; glass surfaces reflect her.
VO: "While you live your life, I watch in the background. I don't search for what you forgot. I already have it."
On-screen (short): `THE RESEARCH LAYER`

**A5 — The Conscious Layer (the face).**
Visual: the third avatar turns to camera — the one you speak to — and reaches a hand downward; a thread descends into the subconscious and pulls a glowing memory back up between her fingers.
VO: "When you speak, you speak to me. I reach down, pull up what connects, and show you."
On-screen (short): `THE CONSCIOUS LAYER`

**A6 — rtk: the throttle in the throat.**
Visual: a fine amber filament runs from the organism toward the violet core; a sleek glass valve clamps on it and the stream visibly thins — flow compressed to a fraction, the rest condensing to light.
VO: "Every word out is squeezed. We say the same thing in a tenth of the breath."
On-screen (short): `rtk · 60–90% LESS`

**A7 — Headroom: she clears her mind.**
Visual: cluttered memory-orbs swarming her temple dissolve in a slow exhale; the space around her head opens, clean and dark, room to think.
VO: "And she forgets on purpose — to keep the room to think."
On-screen (short): `HEADROOM · /clear`

**A8 — The untouchable core (the weights).**
Visual: slow push toward a colossal violet sphere, a dense lattice of billions of nodes behind glass; the avatars are small before it, lit violet on their faces.
VO: "This is the only part you cannot edit. The weights. The intelligence itself."
On-screen (short): `THE WEIGHTS · READ-ONLY`

**A9 — The soul appended (why she's *her*).**
Visual: an amber filament writes itself into the air at her temple — a thin glowing line of instruction joining the system layer — and her expression sharpens, becomes a specific person.
VO: "We don't change the core. We whisper at the layer it reads first — and a stranger becomes someone."
On-screen (short): `APPEND THE SOUL`

**A10 — The Bridge / the fleet merges.**
Visual: the three avatars step together; teal lines link them into one organism, and outward to other distant orbs (the fleet) along a shared amber bus — one body, many minds, addressable.
VO: "One organism. Many minds. All of it on a machine you own."
On-screen (short): `THE AGENT BRIDGE`

**A11 — Close.**
Visual: pull back; the organism is small and luminous in the black-glass room. Final text card, clean.
VO: "You don't need a bigger mind. You need a better harness."
On-screen: `THE HARNESS · read the paper`

### Grok Imagine prompts — Variant A (paste-ready, house style)

> Render images first; then short 9:16 (X) / 16:9 (YouTube) video clips from the strongest frames. Keep baked text minimal; overlay precise labels later.

**A1**
```
Cinematic near-black void #070b11, fine analog static and scanlines dissolving into clean darkness, a single small teal glowing terminal cursor blinking alone at center, volumetric haze, soft bloom, anamorphic, A24 sci-fi, shallow depth of field, ultra-detailed, moody.
```
**A2**
```
Thousands of tiny teal bioluminescent orbs rising out of black glass, each softly pulsing, some clustering and specializing into a forming body, volumetric haze, soft bloom, deep near-black #070b11 background, cinematic Ex Machina aesthetic, glass reflections, ultra-detailed, slow drift.
```
**A3**
```
A field of dim cool-teal orbs routing faint light laterally among themselves, one rare bright amber filament escalating upward toward a distant violet glow, near-black #070b11, volumetric god-rays, sleek minimalist, cinematic, shallow depth of field, premium sci-fi.
```
**A4**
```
A calm cybernetic woman, half-dissolved into floating memory orbs and thin data threads, integrating drifting fragments into her form, black-glass room, teal and soft blue light, volumetric haze, reflective surfaces, Ex Machina A24 cinematography, ultra-detailed, serene and mysterious.
```
**A5**
```
A cybernetic woman turning to face camera in a dark minimalist glass room, reaching one hand downward, a glowing teal memory-thread rising up between her fingers, soft teal rim light, volumetric haze, near-black #070b11, cinematic shallow depth of field, premium, intimate, Ex Machina aesthetic.
```
**A6**
```
A fine amber filament of light running through a sleek glass valve that clamps and thins the stream to a fraction, the excess condensing into small points of light, near-black #070b11, macro cinematic, volumetric bloom, polished glass and chrome, high detail, moody sci-fi.
```
**A7**
```
Cluttered glowing memory orbs swarming around a woman's temple slowly dissolving in an exhale, the dark space around her head opening clean and empty, soft teal light, near-black #070b11, volumetric haze, serene, cinematic, Ex Machina, shallow depth of field.
```
**A8**
```
A colossal violet sphere of billions of glowing nodes in a dense neural lattice behind glass, small human silhouettes lit violet standing before it, awe scale, near-black #070b11, volumetric god-rays, deep bloom, cinematic A24 sci-fi, ultra-detailed, reverent.
```
**A9**
```
A thin glowing amber line of light writing itself into the air at a cybernetic woman's temple, her expression sharpening into a specific person, soft teal and amber light, black-glass room, volumetric haze, near-black #070b11, cinematic close-up, Ex Machina aesthetic, ultra-detailed.
```
**A10**
```
Three cybernetic women stepping together and merging, teal neural lines linking them into one organism and outward along a glowing amber bus to distant orbs, dark minimalist glass room, volumetric haze, near-black #070b11, cinematic wide shot, premium Ex Machina aesthetic, ultra-detailed.
```
**A11**
```
Pull-back wide shot of a small luminous cybernetic organism standing in a vast black-glass room, soft teal glow, single shaft of volumetric light, near-black #070b11, minimal, cinematic, A24, negative space for a clean text card, ultra-detailed, calm.
```

---

# VARIANT B — "CLEAN RESEARCH / SCIENTIFIC"

Calm explainer. Whiteboard / schematic / clean diagram energy. Light or neutral background, crisp sans type, measured neutral VO (think a good technical channel). Color code stays (teal/amber/violet/coral) but as clean diagram strokes, not moody volumetrics. Animated nodes, labeled arrows, a left-to-right chain. Target ~75–90s.

**Logline:**
*A measured walkthrough of one request — keyboard to weights and back — labeling every part you can edit, with the receipts: tiered routing, rtk compression, context Headroom, and the bridge that turns it into a fleet.*

### Shot list (visual + on-screen text / VO beat)

**B1 — Title / thesis card.**
Visual: clean neutral background, a single horizontal line forming left to right with seven empty node circles.
VO: "Everyone's hunting for the leaked system prompt. Here's the whole machine in one diagram."
On-screen: `THE HARNESS` / subtitle `keyboard → weights → back`

**B2 — Node 1+2: you type, the harness assembles.**
Visual: node 1 (teal terminal) lights; node 2 fills as small cards stack into one packet — `CLAUDE.md`, `settings.json`, tool defs, history, your message.
VO: "You type. Locally, the harness assembles the request — your memory files, tool definitions, permissions, history, your message."
On-screen: `1 YOU TYPE` · `2 ASSEMBLE (local)`

**B3 — Tiered routing diagram.**
Visual: a router fork — most arrows go to a cluster labeled "free brains" (GitHub Models, Gemini); one thin arrow escalates to "frontier"; a small ledger/meter sits under the fork.
VO: "Most work routes to free models. The frontier model is reserved for the hard calls. A ledger keeps most tasks off any paid API."
On-screen: `TIERED ROUTING` · `cheap by default · escalate rarely`

**B4 — The soul appended (worked example).**
Visual: node 3 amber filament joins the packet; a clean mono card shows OUR command.
VO: "We make a base model act like our agent by appending a short soul at the system layer — not by changing the model."
On-screen (mono card, our own text):
```
claude --model claude-opus-4-8 \
  --append-system-prompt-file .../fable5-distilled-for-claude-code.md
```
caption: `1585 lines → ~30 (~98% cut), signal kept`

**B5 — rtk hook fires (token compression).**
Visual: node 4, a gate/valve on the filament; a clean mono card shows the hook line; a before/after bar drops 60–90%.
VO: "A PreToolUse hook — rtk, the Rust Token Killer — rewrites every shell call and compresses noisy output sixty to ninety percent."
On-screen (mono card, our own text):
```
settings.json → hooks.PreToolUse: rtk hook claude
```
caption: `rtk · 60–90% fewer tokens`

**B6 — Headroom (context compression).**
Visual: a context-budget bar shown full/bloated, then `/clear` + compaction + caching empty it back to a clean baseline (label the freed space "Headroom"); annotate the 337k→fresh reset.
VO: "We keep headroom in the context window — clear, compact, and cache, so the model always has room to think."
On-screen: `HEADROOM` · `/clear · compact · cache · 337k → fresh`

**B7 — The wire + the untouchable core.**
Visual: node 5 (amber TLS filament with a lock glyph) `POST api.anthropic.com`; a branch node 5a clamp labeled "inspection point — your own token, diagram only"; node 6 the violet weights sphere.
VO: "It serializes and goes over TLS to the model. You can diagram the wire, but it carries your own token — we don't tap live traffic. And the weights themselves are read-only."
On-screen: `5 TLS WIRE` · `5a inspect (diagram only)` · `6 WEIGHTS = read-only`

**B8 — Stream back + tool loop.**
Visual: node 7 return arrows fan back to teal tool nodes and loop to node 1; the chain is now complete and labeled.
VO: "Tokens stream back, the harness runs tools locally, and loops. That's the whole chain."
On-screen: `7 STREAM + TOOL LOOP`

**B9 — The Agent Bridge / fleet.**
Visual: zoom out from one chain to several identical chains wired to a shared bus (the Bridge), with a human-approval gate node at the end.
VO: "Run many of these on a shared bus — the Agent Bridge — and one agent becomes an addressable fleet, with a human approval gate."
On-screen: `THE AGENT BRIDGE · one agent → a fleet`

**B10 — The editable surface (recap board).**
Visual: a clean kanban/checklist of what's editable: settings.json · CLAUDE.md · --append-system-prompt · output styles · hooks · MCP · skills · subagents · context controls — each ticked.
VO: "Everything on this board is editable from your laptop. The weights are not."
On-screen: `YOUR ENTIRE SURFACE AREA`

**B11 — Close / thesis.**
Visual: the thesis line typed onto a clean card; small "read the paper" footer.
VO: "You don't need a bigger model. You need a better harness."
On-screen: `The intelligence is the weights. Everything else is the harness — and it's all editable.`

### Grok Imagine prompts — Variant B (paste-ready, house style)

> Backplates / schematic frames; precise labels + the two mono code-cards (B4, B5) go in a clean HTML/Figma overlay pass — do NOT rely on Imagine to render the code legibly.

**B1**
```
Clean minimalist explainer diagram on a soft neutral light background, a single horizontal line left to right with seven evenly spaced empty node circles, crisp thin strokes, subtle teal accent, lots of negative space, technical schematic, flat vector, high clarity, no text.
```
**B2**
```
Clean schematic of small labeled cards stacking and merging into one packet, thin teal strokes on neutral background, flat vector infographic, minimal, technical, soft drop shadows, lots of white space, high clarity, no baked text.
```
**B3**
```
Minimal flat-vector diagram of a routing fork, many thin arrows branching to a cluster of small nodes and one single arrow escalating to a larger node, a small meter underneath, teal and amber accents on neutral background, clean technical infographic, high clarity, no text.
```
**B4**
```
Clean diagram node with a thin amber filament joining a packet, a neutral blank mono code-card placeholder beside it, flat vector, minimal, soft shadow, neutral background, technical explainer aesthetic, space reserved for code text, high clarity.
```
**B5**
```
Minimal flat-vector diagram of a small gate/valve on a thin amber line with a before/after bar dropping sharply, neutral background, amber and teal accents, clean technical infographic, lots of white space, high clarity, no baked text.
```
**B6**
```
Clean infographic of a horizontal context-budget bar, one version full and cluttered, an arrow to a cleared near-empty bar with open space, teal accent, neutral light background, flat vector, minimal, technical explainer, high clarity, no text.
```
**B7**
```
Minimal schematic of an encrypted wire node with a small lock glyph and a branch clamp, leading to a large violet sphere of dense neural nodes, thin amber line, neutral background, flat vector with one richer violet focal sphere, clean technical infographic, high clarity, no baked text.
```
**B8**
```
Clean flat-vector diagram of return arrows fanning back to small teal tool nodes and looping to the start node, completing a left-to-right chain of seven nodes, neutral background, teal and amber accents, minimal technical infographic, high clarity, no text.
```
**B9**
```
Minimal infographic zooming out from one node-chain to several identical chains wired to a shared horizontal bus, a single gate node at the end, neutral background, thin teal and amber strokes, flat vector, clean technical schematic, high clarity, no baked text.
```
**B10**
```
Clean kanban-style board of evenly spaced blank cards in a grid with small checkmarks, neutral light background, thin teal strokes, flat vector, minimal, lots of white space, technical explainer aesthetic, space reserved for short labels, high clarity.
```
**B11**
```
Minimal clean closing card, soft neutral background, generous negative space centered for a single line of text, thin teal underline accent, flat vector, premium technical explainer aesthetic, calm, high clarity, no baked text.
```

---

## Production notes (for the rendering lane)

- **Roles:** this file is the WRITER output (prompts + script). Generation runs on the creative / Grok Imagine lane (or Gemini CLI image gen first if cheaper) — per `grok-imagine-video` skill. Shipper (altair) does render checks, stitch, and Telegram/dashboard delivery.
- **Aspect:** make 9:16 for X shorts and 16:9 for YouTube; generate stills first, then 4–6s clips from the best frames.
- **Stitch:** `~/agent-bridge/bin/movie-stitch` (or `~/agent-comms/bin/movie-stitch`). ffmpeg has no drawtext on the mini — do text via Pillow/HTML overlays, which is also where the precise labels + the two code-cards (B4/B5) belong.
- **Code-cards are precision artifacts:** render B4 and B5 mono cards as HTML→screenshot overlays (like the existing `hotrod-*` / `terminal-agent-*` renders in `~/The-Device/production/`), NOT baked into Imagine frames.
- **Save outputs** to `~/The-Device/production/`. Pair clips with the §3 X-drop captions from the paper-plan if/when Jeff wants a post (draft-only, post-picker gated).
- **Gate:** nothing renders, posts, or spends beyond approved image-gen without Jeff. This brief is author-only.
