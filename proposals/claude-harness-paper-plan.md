# Claude Harness — PAPER + VISUAL + DROP plan (build-ready)

Author: Fable · 2026-06-14 · Source: `claude-harness-research-notes.md` (sections A–G referenced inline).
This is executable by altair directly. Three artifacts: the **paper**, the **chain visual + glossary**,
the **X drop**. Plus: what to render in Grok Imagine vs feed NotebookLM. Snippets below are paste-ready —
they go verbatim into the paper body AND as the labels on the matching visual node.

Thesis (one line, repeat in paper intro + banger post): **The intelligence is the weights. Everything
you can touch is the harness around them — and all of it is editable from your own machine.**

---

## 1. RESEARCH PAPER — outline (write sections IN THIS ORDER)

Target: ~2,500–3,500 words, plain-but-technical. Each section = one diagram callout. Save to
`~/grokgo/proposals/claude-harness-paper.md` (draft).

**§0. TL;DR / thesis** — the one-liner above + the chain in one sentence (keyboard → assembled prompt →
TLS wire → weights → stream back → tool loop). Name what's editable vs what's not.

**§1. The end-to-end chain** (notes A). Walk steps 1–6: you type → harness assembles locally (base system
prompt + CLAUDE.md/AGENTS.md + appended soul + tool defs + permissions + history + your msg + dynamic
sections) → serialize to Anthropic Messages JSON → HTTPS/TLS to api.anthropic.com with OAuth token →
server runs weights + safety → tokens stream back, harness runs tools locally and loops. This section maps
1:1 to the chain visual (§2).

**§2. Every editable part of the harness** (notes B). The "what you can add" table — for each: what it is,
file/flag, what it changes. Rows: `settings.json` (permissions/model/hooks), CLAUDE.md (global+project),
system-prompt flags (`--system-prompt[-file]`, `--append-system-prompt[-file]`,
`--exclude-dynamic-system-prompt-sections`), output styles, hooks, MCP servers, skills, subagents, context
controls (compaction/`/clear`/prompt-cache/`--model`). Frame: "weights are read-only to you; this column
is your entire surface area."

**§3. Where the Fable prompt slots in + why it works** (notes C). The append-at-system-layer move. Include
verbatim:
```
claude --model claude-opus-4-8 \
       --append-system-prompt-file ~/grokgo/prompt-lab/prompts/fable5-distilled-for-claude-code.md
```
(or via the safe wrapper `~/grokgo/prompt-lab/cc-with-prompt.sh distilled` — opt-in, doesn't touch default
config.) Why it works: appended text rides in the system block the model reads first → steers tone/behavior;
capability stays in the weights. Note the distill: 1585-line Pliny Fable prompt → ~30 lines (~98% cut),
signal kept. Ref `prompts/reference/CLAUDE-FABLE-5-pliny.md`.

**§4. Cost tricks (the % story)** (notes D + our `token-savings.md`). rtk PreToolUse hook (60–90% on shell
output), prompt distillation (~98%), `/clear` discipline (we reset 337k→fresh), free-brain routing
(GitHub Models + Gemini for sub-tasks; frontier only for hard calls), tiered router + ledger/brakes.
Industry contrast: "pi" ships <1k-token system prompt vs ~7–10k for Claude Code/Cline/OpenCode.

**§5. Inspection / mitmproxy — what actually leaves your machine** (notes E + Ronin checklist
`~/agent-comms/research/checklists/2026-05-30-null-mitmproxy-claude-oauth-inspection.md`). The honest line:
client-side flags already let you SEE and STRIP the prompt; MITM on live api.anthropic.com traffic needs a
root CA, captures **your own token**, and risks the account — so we diagram the inspection point, we don't
run it on live Claude Code traffic. What the Ronin layer DID prove (on a Null/OAuth gateway, not CC): an
mitmweb addon (`null_inspect_addon.py`, `-s` in `com.jeff.mitmweb.plist`) doing sanitized inspection +
system injection, verified `200 / system_injected:true` through the proxy. Use that as the "it's doable on
infra you own" sidebar.

**§6. Secrets-dir hygiene** (notes F). `~/.secrets/*` = API keys as files outside 1Password; load via env at
launch, never inline in prompts/commits; the redaction rule (strip `sk-/oat-/Bearer` before surfacing).
Part of the "production-ready agent" bar.

**§7. Open-source context** (notes G). OpenCode (165k★, MIT) = the open Claude Code: 75+ providers,
Build/Plan subagents, markdown-defined custom agents, LSP. Alternatives: OpenHands, Zed, Cline, pi (minimal).
Note Gemini CLI retiring 2026-06-18 → closed successor. Sources: openalternative.co, builder.io, pinggy.io.

**§8. Production-agent framing** (notes "Null app"). Tie it together: a production agent = harness hygiene
(§2/§6) + cost control (§4) + inspectability (§5) + reusable skills/subagents, addressable in a fleet.
Refs: `Null_App_Feature_Requests_and_Integration_Points.md`,
`~/agent-bridge/docs/2026-05-26-null-app-agent-bridge-product-plan.md`.

**§9. Conclusion** — restate thesis; "you don't need a bigger model, you need a better harness."

---

## 2. CHAIN VISUAL spec (the hero diagram)

One wide image (16:9), left-to-right flow, dark/orb house style. **7 nodes**; each node shows a LABEL +
the exact snippet/file that lives there (snippet rendered in a small mono card under the node). This is the
"code-in-place" requirement — reader sees WHERE each editable piece attaches.

| # | Node | Visual | Snippet/file shown at the node |
|---|------|--------|-------------------------------|
| 1 | **Keyboard / terminal** | teal terminal orb, cursor | `you type →` (no code) |
| 2 | **Harness assembles** | cluster of small orbs merging into one packet | files: `CLAUDE.md` · `settings.json` · tool defs · history |
| 3 | **Fable soul appended** | amber filament injecting into the packet | `claude --append-system-prompt-file …/fable5-distilled-for-claude-code.md` |
| 4 | **Hooks fire (rtk)** | a gate/valve on the filament | `settings.json` → `"hooks":{"PreToolUse":[{"matcher":"Bash","hooks":[{"type":"command","command":"rtk hook claude"}]}]}` |
| 5 | **Serialize + TLS wire** | taut encrypted amber filament, lock glyph | `POST https://api.anthropic.com/v1/messages` · `Authorization: Bearer <oauth>` |
| 5a | **Inspection point** (branch off the wire) | a clamp/parasite orb on the wire with a key glyph | `mitmproxy` — *sees your own token; diagram only* (Ronin checklist) |
| 6 | **Weights (the model)** | the colossal violet orb, dense node lattice | `model = weights = the intelligence (read-only to you)` |
| 7 | **Stream back + tool loop** | return filaments fanning back to teal tool orbs, looping to node 1 | `tokens stream → harness runs tools locally → loop` |

Caption strip under the diagram: the §0 one-liner.

### GLOSSARY (left-side rail OR separate companion image)
Render as a clean vertical list (legible mono). Terms + one-line defs:
- **Harness** — everything around the model you can edit (prompts, tools, hooks, config).
- **Weights** — the trained model; the actual intelligence; you can't edit it.
- **System prompt** — instructions the model reads first; `--append-system-prompt-file` adds to it.
- **CLAUDE.md** — persistent project/global memory loaded every session.
- **Hook** — shell command fired on a tool event (ours: rtk on PreToolUse).
- **MCP** — external tools/data servers the agent can call.
- **Skill** — a reusable `SKILL.md` procedure.
- **Subagent** — a scoped sub-task with its own context.
- **Token** — chunk of text billed in/out; fewer = cheaper.
- **TLS / OAuth token** — the encrypted wire + your credential in the header.
- **mitmproxy** — a man-in-the-middle that can read the wire (with your own CA + token).
- **Distillation** — cutting a prompt to its signal (1585→~30 lines here).

Recommendation: **separate glossary image** (cleaner, reusable in thread) + a 2-line legend on the hero.

---

## 3. X DROP — angles tied to images

Two lanes, draft-only (goes through the post-picker). Each post names the image it pairs with.

**A. Banger (hooky, broad):** pairs with the **hero chain visual**.
> Everyone's hunting for the "leaked system prompt."
> Here's the whole machine in one picture — keyboard → your prompt → the wire → the weights → back.
> The intelligence is the weights (you can't touch those). *Everything else is the harness — and it's all
> editable from your own laptop.* 🧬

**B. Clean-technical:** pairs with the **editable-parts table render** (KANBAN style, see §4).
> What you can actually edit in a Claude Code agent, in one board:
> settings.json (permissions/model/hooks) · CLAUDE.md · --append-system-prompt · output styles · MCP ·
> skills · subagents · context controls.
> We append a 30-line "soul" at the system layer and route 90% of work to free models. Paper ↓

**C. Sci-fi (our orb style):** pairs with the **weights orb (node 6)** close-up.
> This violet sphere is the only part you can't edit: the weights — billions of numbers that are the
> intelligence. Everything leading into it is just steering. We spent the week documenting the steering. 🧬

Optional D (inspection/security): pairs with the **parasite-on-the-wire** image (already generated, drop
id=8) → the mitmproxy honesty line: "you can tap the wire — but it's your own token in there."

---

## 4. WHAT TO GENERATE vs WHAT TO FEED NOTEBOOKLM

### Generate via Grok Imagine (queue as a drop; captions = the §3 posts)
House orb style, several variants each:
1. **HERO chain visual** — but Grok Imagine can't do precise labeled diagrams. So: generate the orb
   BACKPLATE (the 7-orb left-to-right flow on near-black — we already have id=7's prompt for this) and
   **overlay node labels + snippet cards in HTML/Figma** (clean pass). Two-layer hero.
2. **Weights orb close-up** (node 6) — reuse queued id=9 ("colossal violet orb, billions of nodes").
3. **Parasite/inspection orb** (node 5a) — reuse id=8 (already generated).
4. **Soul-injection** (node 3) — Ex-Machina woman + amber filament from temple — reuse id=1/id=3.

### Render clean (HTML → screenshot, NOT Grok) — precision artifacts
5. **Editable-parts KANBAN board** (post B) — the §2 table as cards. Plain, legible.
6. **GLOSSARY image** (§2) — the term list.
7. **Labeled HERO** — orb backplate + the 7 node labels + snippet mono-cards from §2's table.
   (These three need exact text → do them as HTML renders like the existing `hotrod-*` / `terminal-agent-*`
   images in `~/The-Device/production/`.)

### Feed NotebookLM (source pack for an audio/explainer)
Drop these into a NotebookLM notebook to generate the narrated overview:
- `~/grokgo/proposals/claude-harness-paper.md` (the paper, once written)
- `~/grokgo/proposals/claude-harness-research-notes.md` (raw notes)
- `~/grokgo/proposals/token-savings.md`
- the Ronin checklist (§5 path)
- `~/Desktop/NULL-App-NotebookLM-Source-Pack.md` (existing pack)
- the distilled prompt `…/fable5-distilled-for-claude-code.md` (as the worked example)

---

## EXECUTION ORDER for altair
1. Write the paper (§1) to `claude-harness-paper.md` — sections in the §1 order.
2. Build the 3 precision HTML renders (§4 items 5–7): glossary, KANBAN, labeled hero (orb backplate +
   labels/snippets). Save to `~/The-Device/production/`.
3. Queue the orb backplate + reuse id=8/id=9/id=1 as a Grok Imagine drop with §3 captions (post-picker).
4. Stage posts A/B/C in the picker (draft-only — Jeff approves before anything goes out).
5. Build the NotebookLM source pack list → generate the audio overview.
Gate: nothing posts; nothing spends beyond image gen without Jeff. Ping Jeff when the paper + hero are done.
