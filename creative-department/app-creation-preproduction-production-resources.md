# App Creation — Pre-Production, Production Management & Agentic Build Resources

> Provenance: compiled by the Grok chrome-tab assistant, pasted by Jeff, saved for real by Fable.
> **Repos/tools below are grok-tab-sourced and UNVERIFIED** — confirm each exists before relying.

## 1. Pre-production & planning (before building)
- **ChatPRD** — structured PRDs, user stories, acceptance criteria.
- **Omniflow** — spec-driven AI app builder; keeps PRD → UI design → code in sync.
- **v0 (Vercel)** + **Figma Make** — fast UI/UX prototyping from natural language.
- Notion AI + Linear AI — requirements, roadmaps, alignment.

## 2. AI-powered app builders (no-/low-/full-code)
- **Lovable.dev** — strong full-stack AI builder (React + Tailwind + Vite); production-ready MVPs.
- **Replit Agent** — browser full-stack generation + hosting/deploy.
- **Bolt.new** — flexible full-stack from prompts.
- **Base44** — frequently top-ranked for shipping real apps.
- **FlutterFlow** — complex mobile + web, code export.

## 3. Agentic coding systems & multi-agent frameworks (GitHub — core)
- **OpenHands/OpenHands** — strong open-source coding agent; self-hosted dev control center.
- **omnigent-ai/omnigent** — meta-harness orchestrating Claude Code, Codex, Cursor, custom agents under one layer.
- **CrewAI** — popular, well-documented multi-agent framework. *(Fable's note: role/task abstraction, good for linear crews; weaker for complex stateful branching — see LangGraph. Verifying current state.)*
- **LangGraph** (LangChain) — production-grade, stateful, observable multi-agent graphs.
- **AutoGen / AG2** (Microsoft) — conversational multi-agent collaboration.
- **OpenAI Agents SDK / Swarm** — lightweight orchestration.
- **CAMEL-AI + OWL** — multi-agent role-play / complex collaboration.
- **kyegomez/swarms** — enterprise multi-agent orchestration.

## 4. Awesome lists
- `caramaschiHG/awesome-ai-agents-2026` (340+ resources)
- `ashishpatel26/500-AI-Agents-Projects`

## 5. Production management & DevOps
- n8n (AI nodes), Langflow (visual agent workflows), LangSmith, Helicone (cost tracking).

## 6. "Find the holes before building" (the github Jeff remembers)
- Spec-driven / pre-mortem approach: write the PRD + a **failure/assumptions audit** (where will this
  break, what's unverified, what are the edge cases) BEFORE code. Tools: ChatPRD + Omniflow spec sync;
  pattern = adversarial spec review. **TODO: identify the exact repo Jeff means** (likely a "spec-kit" /
  "pre-mortem" / "product-requirements-as-code" repo) — Librarian to pin down.

## Tie-in
Living reference for building Grok Go apps — the Xcode app (OpenAgents / Bridge MVP), Bid Local,
Somaco/UUIDv8. Recommended flow: spec-first (ChatPRD) → holes audit → easy MVP → add features.
