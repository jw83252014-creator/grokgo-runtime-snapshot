# Obsidian Integration Plan — mining-engine / grokgo → Obsidian

Status as of 2026-06-18. Author: research agent. **Propose, never enact** — this is a build plan, not a change.

---

## 1. Current status (what actually exists)

### The two vaults
- `~/Documents/Obsidian Vault` — **effectively empty.** Just `.obsidian/` + a `Welcome.md` (203 B). Default/scratch vault. Ignore it.
- `~/Documents/Jwnull` — **the real, active vault.** ~914 markdown files. This is Jeff's personal PKM second brain.

### Jwnull vault shape (structure only, contents not dumped)
Folder note-counts (top folders):

| Notes | Folder |
|------:|--------|
| 315 | `👑 Command-Center/` |
| 227 | `📁 AI-Conversations/` |
| 102 | `_grok-import/` (raw Grok chat exports, .json + .md, plus some app/archive blobs) |
| 44  | `Research/` |
| 34  | `X-Operations/` |
| 22  | `Command-Center/` (older, pre-emoji) |
| 18  | `🏗️ BidLocal/` |
| 13  | `🛠️ Code-Library/` |
| 12  | `Imports/`, `💰 Polymarket-Bot/` |
| 11  | `Townhomes/` |
| 9   | `Indexes/` |
| 7   | `Trade-App/`, `🎬 Creative/` |
| 3   | `📰-Research-Intelligence/`, `🧠 RSI-System/`, `Memory/` |

There is clear emoji-folder migration in progress (duplicate `Command-Center` / `👑 Command-Center`, `BidLocal` / `🏗️ BidLocal`). Several emoji folders the OS showed as "empty" actually hold notes — the empty-looking ones (`Hermes-Memory`, plain `Research`) are mostly placeholders.

### Community plugins already installed in Jwnull
From `.obsidian/community-plugins.json`:
- **Dataview** — query notes as a database (tables/lists from frontmatter).
- **Juggl** — interactive force-directed graph (better than core graph).
- **Graph Analysis** — link-prediction / co-citation / centrality over the graph.
- **Tasks** — query/roll-up checkboxes across the vault.
- **Kanban** — board views from markdown.
- **Excalidraw** — hand-drawn diagrams.

This is already a knowledge-graph-oriented setup. Notably **absent**: any AI/embedding plugin (no Smart Connections, no Copilot), and no Local REST API.

### Is our project data in Obsidian? — **No.**
- `grep` for `grokgo`, `mining-engine`, `research.loop`, `Fable`, `Codex-Fable` across the whole Jwnull vault: **zero hits.**
- `~/mining-engine/obsidian-integration/` is **empty** — the export was scoped but never built.
- The data that *should* flow in already exists as clean markdown, just not in the vault:
  - `~/mining-engine/` — 366 md files: `concepts/` (~10 idea notes), `research/`, `research-agent/research-agent-spec.md`, `skills/agent-capabilities.md`, `docs/` (system-overview, agent-bridge-how-it-works, sovereign-agent-architecture, etc.), `goals/`, `x-strategy/`.
  - `~/grokgo/research/loop/` — **164** `research.loop` receipt notes (timestamped, structured with `target:` + reasoning cells), plus `research/account-inventory.md`, `claude-code-harness-explained.md`, `grok-chat-resources-catalog.md`.
  - `~/grokgo/skills/` (e.g. `bridge-dispatch/`) — skill files with YAML frontmatter (`name`, `description`).
  - `~/grokgo/proposals/` — design docs, candidate logs.

**Bottom line:** we are sitting on ~530 clean, agent-authored markdown files (mining-engine + grokgo) that have a natural home in the existing graph-oriented Jwnull vault and currently live entirely outside it. The integration genuinely was never built.

---

## 2. Should we build a mining-engine → Obsidian export? — **Yes, but as a one-way mirror, not a merge.**

### Why yes
- The format is already markdown — near-zero conversion cost. LLMs (and Obsidian) read `.md` natively; no parsing layer needed.
- Jwnull already has the exact plugins that make this valuable (Dataview for querying, Juggl/Graph Analysis for the knowledge graph). We get the payoff immediately.
- The `research.loop` receipts and `concepts/` notes are precisely the "interconnected notes you keep current" that PKM-for-agents is built around (the Karpathy LLM-Wiki pattern, see §3).
- It closes the loop Jeff already half-designed (`obsidian-integration/` exists, just empty).

### Design constraints (important)
1. **One-way, read-only mirror.** Source of truth stays in git (`mining-engine` / `grokgo`). Obsidian is a *view/graph layer*, not an editing surface for these files. Avoids merge conflicts and accidental edits getting clobbered by the next export.
2. **Land in a quarantined, prefixed folder** so it never collides with Jeff's hand-curated notes. Proposed: a single top-level `🤖 Agent-Engine/` (or `_engine-mirror/`) folder with subfolders mirroring source: `concepts/`, `research-loop/`, `skills/`, `proposals/`, `docs/`.
3. **Add frontmatter on export** so Dataview can query it. Inject `source:`, `repo:`, `kind:` (concept|receipt|skill|proposal|doc), `exported:` (date), and `tags:`. Most source files already have partial frontmatter (skills have `name`/`description`).
4. **Convert relative links → `[[wikilinks]]`** so the graph lights up. Auto-link on shared concept slugs (e.g. `personal-algorithm`, `multi-agent-systems`, `latent-space-mining`) and on `target:` strings in receipts.
5. **Idempotent + incremental.** Re-runnable; only rewrites changed files (hash compare). Keeps an `Indexes/` MOC (map-of-content) note per folder, generated.

### Concrete build plan

**Phase 0 — placement & decision (no code)**
- Confirm with Jeff: target vault = `Jwnull`, mirror folder name, one-way only. (Human-gated.)

**Phase 1 — exporter script** (lives in the now-empty `~/mining-engine/obsidian-integration/`)
- `export.py` (single file, stdlib + `pyyaml`):
  1. Walk source roots: `mining-engine/{concepts,research,research-agent,skills,docs,goals,x-strategy}` and `grokgo/{research,research/loop,skills,proposals}`.
  2. For each `.md`: parse/merge frontmatter, inject `source`/`repo`/`kind`/`exported`/`tags`.
  3. Rewrite intra-repo relative links and bare concept references to `[[wikilinks]]`.
  4. Write to `<vault>/🤖 Agent-Engine/<kind>/<slug>.md` only if content hash changed.
  5. Emit per-folder MOC index notes + a top-level `🤖 Agent-Engine/README.md` dashboard with Dataview queries.
- `config.yaml`: vault path, mirror folder name, source roots, slug→canonical-link map, exclude globs (skip `_grok-import` blobs, `.zip`, `.app`).
- Dry-run default; `--apply` to write. Mirrors grokgo's existing "propose, never enact" + dry-run convention.

**Phase 2 — write path (pick one)**
- **A. Direct file write (simplest, recommended v1):** the script writes `.md` straight into the vault folder on disk. Obsidian picks up changes live. No plugin needed. Zero auth. This is what the no-dependency Claude-PKM kits do.
- **B. Local REST API (for later / for live agent writes):** install `coddingtonbear/obsidian-local-rest-api`, agents `PATCH`/`PUT` notes over HTTP+Bearer (and it ships an MCP server, so Hermes/Codex/Fable could write memory as a tool). Use this only once we want *agents* writing into the vault during a run, not batch mirroring.

**Phase 3 — scheduling**
- Add a launchd job (same pattern as the existing `com.jeff.fable-self-improve.plist`) or a step at the end of `research_loop.py` to run `export.py --apply` after each cycle / nightly. So new `research.loop` receipts and concepts appear in the graph automatically.

**Phase 4 — graph + query layer (uses installed plugins)**
- Dataview dashboard note: "latest 20 research.loop receipts", "all concepts by tag", "skills inventory".
- Graph Analysis to surface co-occurring concepts across receipts (link prediction → "these two ideas keep showing up together").
- Optional: add **Smart Connections** (see §3) for semantic "related notes" across the now-unified Jeff-notes + agent-notes corpus — this is where the real value is (an agent receipt automatically surfacing next to Jeff's matching hand-note).

**Effort:** Phase 1+2A is a ~1-day single-file script. Phases 3–4 are config/plugin-install, hours.

---

## 3. Matching Obsidian community plugins & setups (web research)

Things that map directly to what we do (PKM for an agent org: AI, Dataview, knowledge graphs).

### AI / semantic layer
- **Smart Connections** (Brian Petro) — local-first semantic search & "related notes" using on-device embeddings (TransformersJS → ONNX/WASM), zero setup, no API key, works offline after indexing. **Best fit** for surfacing agent receipts next to Jeff's matching notes across the unified corpus. ([github](https://github.com/brianpetro/obsidian-smart-connections), [site](https://smartconnections.app/smart-connections/), [stats](https://www.obsidianstats.com/plugins/smart-connections))
  - Open fork: **open-smart-connections / open-connections** (GoBeromsu) — 7 embedding providers, privacy-first. ([github](https://github.com/goberomsu/open-smart-connections))

### Programmatic / agent write access
- **Local REST API with MCP** (coddingtonbear) — secure HTTP REST API + MCP server over the vault: full CRUD, plus `PATCH` to surgically edit a single heading / block / frontmatter field without rewriting the file. This is the clean way for agents to write memory into the vault as a tool. ([github](https://github.com/coddingtonbear/obsidian-local-rest-api), [community](https://community.obsidian.md/plugins/obsidian-local-rest-api), [API docs](https://coddingtonbear.github.io/obsidian-local-rest-api/))
- **Obsidian Memory MCP server** — converts AI-interaction entities/relationships/observations into markdown + knowledge-graph visualization; purpose-built for AI long-term memory in Obsidian. ([awesome-mcp-servers list](https://github.com/TensorBlock/awesome-mcp-servers/blob/main/docs/knowledge-management--memory.md), [overview](https://skywork.ai/skypage/en/ai-obsidian-memory-server/1978331309583015936))

### Agent-org / "second brain for agents" setups (patterns to copy)
- **obsidian-claude-pkm** (ballred) — Claude Code + Obsidian starter kit. **Zero plugin dependencies — pure bash + markdown.** Specialized agents (`goal-aligner`, `weekly-reviewer`, `note-organizer`, `inbox-processor`) write notes via Claude Code skills that manage wiki-links automatically; per-project `CLAUDE.md` context files; bidirectional wiki-link conventions; vision→goals→projects→daily cascade. Closest existing analog to our agent fleet. ([github](https://github.com/ballred/obsidian-claude-pkm))
- **obsidian-wiki** (Ar9av) + **Karpathy's LLM-Wiki pattern** — framework for AI agents to build/maintain a "digital brain" as an Obsidian wiki: compile knowledge once into interconnected markdown and keep it current instead of re-asking the LLM. Every skill = a markdown file the agent reads/runs. Directly validates our research.loop-receipts-as-notes approach. ([github](https://github.com/ar9av/obsidian-wiki), [writeup](https://www.mindstudio.ai/blog/andrej-karpathy-llm-wiki-obsidian-codeex-second-brain))
- **Obsidian AI knowledge-base guide** (Data Science Dojo) — 9-step build: why local `.md` is ideal for LLMs (no lock-in, agents read natively), structure + plugin choices. Good reference for our dashboard/MOC layer. ([blog](https://datasciencedojo.com/blog/obsidian-ai-knowledge-base/))

### Already installed in Jwnull (keep using; no install needed)
- **Dataview** — query the mirrored frontmatter into live tables (receipts, concepts, skills inventory).
- **Juggl** + **Graph Analysis** — interactive graph + link-prediction/centrality across the unified corpus (find ideas that co-occur across agent receipts).
- **Tasks / Kanban / Excalidraw** — task roll-ups, boards, diagrams (secondary).

---

## Recommendation

Build it — Phase 1 + 2A (one-way disk-mirror exporter in `~/mining-engine/obsidian-integration/`, into a quarantined `🤖 Agent-Engine/` folder in **Jwnull**, with injected frontmatter + wikilinks), then wire it to run after each `research_loop.py` cycle (Phase 3). Add **Smart Connections** for the semantic payoff and **Local REST API + MCP** only when we want agents writing live during runs. Everything stays one-way (git = source of truth) and human-gated to apply, per grokgo's existing conventions.

## Sources
- https://github.com/brianpetro/obsidian-smart-connections
- https://smartconnections.app/smart-connections/
- https://www.obsidianstats.com/plugins/smart-connections
- https://github.com/goberomsu/open-smart-connections
- https://github.com/coddingtonbear/obsidian-local-rest-api
- https://community.obsidian.md/plugins/obsidian-local-rest-api
- https://coddingtonbear.github.io/obsidian-local-rest-api/
- https://github.com/ballred/obsidian-claude-pkm
- https://github.com/ar9av/obsidian-wiki
- https://www.mindstudio.ai/blog/andrej-karpathy-llm-wiki-obsidian-codeex-second-brain
- https://datasciencedojo.com/blog/obsidian-ai-knowledge-base/
- https://github.com/TensorBlock/awesome-mcp-servers/blob/main/docs/knowledge-management--memory.md
- https://skywork.ai/skypage/en/ai-obsidian-memory-server/1978331309583015936
