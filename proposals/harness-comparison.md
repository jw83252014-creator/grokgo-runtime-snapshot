# Three harnesses, same trick — Claude Code vs Codex vs Grok (Fable, 2026-06-16)

Jeff wanted to *see* the difference between the harnesses. The headline: **all three are the same shape**
— a terminal agent loop where the model is rented and everything around it is editable. The differences
are in *how* you edit the system prompt, what backends they reach, and the controls. Verified the flags
on each, on this Mac.

## The one-line each
- **Claude Code** — Anthropic's loop. Richest ecosystem (hooks, skills, subagents, MCP). Locked to Claude.
- **Codex** — OpenAI's coding agent (our **keystone** lane). File-driven config (AGENTS.md). Great executor.
- **Grok** — xAI's CLI on the mini. Surprisingly full: system-prompt override, append-rules, sandbox
  profiles, headless self-verify, JSON prompts. Reaches Grok + a local model.

## How you give each one a "soul" (the part that matters)
| | Claude Code | Codex (keystone) | Grok |
|---|---|---|---|
| **Append to system prompt** | `--append-system-prompt[-file]` | `AGENTS.md` (global `~/.codex/` + project) | `--rules "<text>"` |
| **Replace system prompt** | `--system-prompt[-file]` | (via AGENTS.md content) | `--system-prompt-override` |
| **Persistent project memory** | `CLAUDE.md` | `AGENTS.md` | `GROK.md` / config dir |
| **One-shot prompt** | `-p` | `exec`/`-p` | `-p` / `--prompt-file` / `--prompt-json` |
| **Strip built-in sections** | `--exclude-dynamic-system-prompt-sections` | — | (override replaces wholesale) |
| **Hooks on tool events** | ✅ `settings.json` hooks (rtk) | limited | — |
| **Skills / subagents** | ✅ `SKILL.md` + subagents | partial | `~/.grok/skills` + marketplace |
| **MCP servers** | ✅ | ✅ | ✅ |
| **Sandbox profiles** | permissions in settings.json | approval modes | ✅ `--sandbox <profile>` (fs+net) |
| **Self-verification loop** | manual | manual | ✅ built-in (headless) |
| **Backend (the weights)** | Claude only | OpenAI/Codex | Grok + OpenAI-compatible/local |

## What this proves (the thesis, made concrete)
The "soul" move works on **every** harness — we've now applied it to all three: the distilled Fable soul
appends via `--append-system-prompt` (Claude), `AGENTS.md` (Codex/keystone), and `--rules` (Grok). Same
steering, three loops. **Capability still lives in whatever weights each points at** — the prompt steers,
it doesn't add intelligence. That's why the *right* design is per-cell souls over the *cheapest capable*
backend, not one harness to rule them all.

## Per-cell souls (Jeff's idea, generalized)
Each Grok Go cell = (a harness) + (a soul for its role) + (a backend). We can give the **Grok** lane a
cell-specific soul exactly like Fable's — e.g. a "grok.research" soul via `--rules`, a "grok.harvest"
soul, etc. The cell directive (`directives/cell.template.md`) is the soul; the harness is just the body
it runs in. So:
- **Claude Code** → reasoning/architecture cells (Fable), where the ecosystem (skills/hooks) earns its keep.
- **Codex/keystone** → build/execution cells (file-driven, strong at multi-file changes).
- **Grok** → research/harvest cells + anything that wants the sandbox profiles + self-verify, and the
  cheap local-or-Grok backend.
- **Badass Fable (local MLX)** → the free cheap lane under all of them.

## Practical takeaways
1. Don't standardize on one harness — **match the harness to the cell's job** and give it a role-soul.
2. Grok's `--sandbox` + built-in self-verify make it a strong, safe **autonomous looper** — arguably the
   best fit for the research.loop cell.
3. Codex's file-driven AGENTS.md is best for **persistent build identity** (keystone).
4. Claude Code's hooks/skills/subagents make it best for **orchestration + reasoning** (Fable, the COO).
5. All of them rent the weights; the harness + soul + routing is the owned asset. Same lesson, three proofs.
