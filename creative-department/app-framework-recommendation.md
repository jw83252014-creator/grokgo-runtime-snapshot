# App Framework Recommendation — Grok Go (Xcode App)

> Author: Fable (Opus 4.8), for Jeff. Date: 2026-06-18.
> Scope: (1) honest CrewAI verdict, (2) framework recommendation for OUR app (start easy → minimal MVP → add features), (3) a concrete "find the holes first" pre-build process.
> Status: research is web-verified (sources cited inline). This is a recommendation doc, not an authorization to post/spend anything.

---

## TL;DR

- **CrewAI is great for prototyping a multi-agent crew, not great as the spine of a shipping native app.** Use it to *demo an idea in an afternoon*; do not bet production reliability on it.
- **For OUR app, do not start with a multi-agent framework at all.** Start with a single agent loop (OpenAI Agents SDK *or* a plain Anthropic/loop with tools) behind a clean local HTTP server, and the Swift app talks to it over HTTP. Add a framework (LangGraph) only when you actually have ≥3 real branch/decision points. "Start easy" means *one* agent, *one* process, *one* contract.
- **The "github about finding holes BEFORE building" Jeff remembers is almost certainly one of:** GitHub **spec-kit** (spec-driven dev: constitution → specify → clarify → plan → analyze), **adversarial-spec** (multi-LLM debate over a spec), or **pm-skills** (`/red-team-prd`, `/pre-mortem`). All three are real and cited below. Our pre-build process steals the best of each.

---

## 1. CrewAI — honest verdict (as of mid-2026)

### What it is
CrewAI (github.com/crewAIInc/crewAI, ~44.6K stars) is a Python, code-first multi-agent framework built on a **role → task → crew** mental model: you give each agent a persona + tools and a task, and compose them into a crew. It is the fastest-growing multi-agent framework in 2026 and has first-class MCP support. [digitalapplied, openagents, langchain]

### Strengths (real)
- **Fastest demo-to-prototype ergonomics of the major frameworks** — a working multi-agent crew in ~2–4 hours, lowest barrier to entry. [digitalapplied, particula]
- **Clean, readable abstractions** for role-based collaboration with shared context. Good when the work is genuinely "a team of specialists hands a doc around." [presenc, codebridge]
- **Open-source core**, active community, MCP servers, and (new in 2026) CrewAI Flows + enterprise observability/scheduling for more controlled execution. [presenc, digitalapplied]

### Weaknesses (the part the tutorials hide)
- **Production reliability is the weak spot.** It trails LangGraph on observability and error recovery. Agents that work solo "fail when composed," costs spiral from unbounded loops, and debugging an 8-agent crew is far harder than a single model call. [presenc, agilesoftlabs]
- **Token cost is structural, not incidental.** Every agent makes its own LLM calls, every handoff passes conversation history, every reasoning loop burns more tokens — ReAct/CoT loops can use ~10x the tokens of a direct answer. Real coding/research crews run **$1.50–$12/hr**. [agilesoftlabs, daily.dev]
- **Light on branching, retries, and complex state.** The widely repeated production lesson: most serious CrewAI deployments end up bolting on **a thin LangGraph layer or a custom state machine** to handle conditional flow — i.e., the framework doesn't carry you to production by itself. [presenc, agilesoftlabs]
- **Needs guardrails to be safe:** `max_iter` (default 15), `max_execution_time`, `allow_delegation=False`, tool grounding, and observability are *mandatory*, not optional, to avoid loops/hallucination/cost overruns. [agilesoftlabs]

### vs LangGraph vs OpenAI Agents SDK
The 2026 consensus maps cleanly to architecture:

| | Mental model | Best for | Watch out for |
|---|---|---|---|
| **OpenAI Agents SDK** | imperative handoff chains | fastest 0→working agent (<100 lines) if you're OpenAI-native | **vendor lock-in** to OpenAI models |
| **LangGraph** (v0.4, 2026) | explicit state machine over a graph | **production standard** for stateful, auditable, human-in-the-loop workflows; persistence/checkpoints | heavier; more concepts up front |
| **CrewAI** (44.6K★) | role-driven crews + declarative tasks | **fastest path to a multi-agent prototype** | production reliability/observability; cost |

Rule of thumb from the comparisons: **<3 decision points → imperative framework wins on clarity; >3 → graph framework wins on maintainability.** Framework choice can move benchmark performance by up to ~30 points on identical models — so it matters, but it's a *later* decision than people think. [digitalapplied, codebridge, particula]

### Does CrewAI fit a native macOS agent app?
**Only as an optional internal engine, not as the app's backbone.** CrewAI is Python, so a Swift/Xcode app can't embed it natively — you'd run it as a separate Python process and the app would talk to it over HTTP (see §2). For a v1 native app, a multi-agent crew is *premature complexity*: more tokens, more failure modes, harder debugging, and a Python dependency to ship — in exchange for capability you don't need until you have a real multi-role workflow. **Verdict: keep CrewAI in your back pocket as a prototyping tool and a possible future "research crew" backend; do not build the MVP on it.**

---

## 2. Framework recommendation for OUR app

Design constraint Jeff stated: **start easy = a minimal MVP, then add features.** That maps to one principle: **defer the framework decision; ship the contract first.**

### Architecture: thin Swift UI ↔ local agent server
The robust, well-trodden pattern for a native macOS app with an LLM/agent backend is a **decoupled local server**, not embedding Python in the app:

- **Swift app** = UI + a tiny HTTP client. Owns nothing about agents.
- **Agent backend** = a separate local process (run as a launchd agent), exposing a small HTTP/JSON API. API key in Keychain. This keeps the two decoupled — the backend can be swapped, run standalone, or even hit via `curl`. [Apple dev forums, brightdigit/Sublimation]
- Alternatives exist (PythonKit to embed Python, or Swift 6.2 `Subprocess` to spawn a script) but they tie you to the host Python install and couple UI to engine. **Prefer the local-server pattern for anything you intend to ship.** [PythonKit/MLBoy, swift-subprocess, mjtsai]

This boundary is the single most valuable early decision: it lets you change the agent framework later **without touching the app.**

### Phased framework choice (matches "start easy → add features")

**Phase 0 — MVP (do this first):**
- **One agent, one loop, behind the HTTP contract.** Use either the **OpenAI Agents SDK** (fastest 0→1 if you accept OpenAI lock-in) or — given this house runs on Anthropic/Claude — a **plain Claude tool-use loop** (system prompt + tools + a `while not done` loop). No CrewAI, no LangGraph.
- Why: with <3 decision points, an imperative single agent is clearer, cheaper, and easier to debug. You get a shippable app *and* learn what the agent actually needs to do.
- ⚠️ Provider note: if the agent runs on Claude/Anthropic, confirm current model IDs/pricing/limits via the `claude-api` skill before wiring — do not hardcode from memory.

**Phase 1 — add structure when (not before) you hit real branching:**
- The moment you have **≥3 genuine decision points / retries / human-in-the-loop checkpoints**, graduate the *backend* to **LangGraph** (2026 production standard for stateful, auditable, persisted agent workflows). The Swift app doesn't change — same HTTP contract.

**Phase 2 — add a crew only if the work is genuinely multi-role:**
- If a feature is truly "a team of specialists passing a document around" (e.g., a research crew), spin up **CrewAI** as one backend service behind the same contract — with `max_iter`, `max_execution_time`, bounded delegation, tool grounding, and observability from day one. Treat its cost as a line item.

**One-line recommendation:** *Single Claude/OpenAI agent loop → local HTTP server → Swift UI for the MVP. LangGraph when you have real state. CrewAI only for a real multi-role crew. Never let the framework choice block the MVP.*

---

## 3. "Find the holes first" — concrete pre-build process

Jeff's memory of "a github about doing product development BEFORE building an app — finding holes/gaps first" most likely points to one (or a blend) of these real repos/tools:

- **github/spec-kit** — GitHub's open-source Spec-Driven Development toolkit. Workflow: `/speckit.constitution` → `/speckit.specify` → `/speckit.clarify` (structured questioning to fill gaps) → `/speckit.plan` → `/speckit.tasks` → `/speckit.analyze` (cross-artifact consistency review) → `/speckit.implement`. The **clarify** and **analyze** steps are literally "find the holes before coding." Works with Claude Code, Copilot, Gemini CLI. [github/spec-kit, github.blog, github.github.io/spec-kit]
- **zscole/adversarial-spec** — Claude Code plugin: drafts a PRD, then runs a **multi-LLM adversarial debate** (GPT/Gemini/Grok + Claude as a substantive participant, not just moderator) that loops until models converge — surfacing gaps, edge cases, and security holes any single model would miss. [zscole/adversarial-spec]
- **phuryn/pm-skills** — 100+ PM skills incl. **`/red-team-prd`** (surface load-bearing assumptions, name what makes each fail, rank by *cheapest test*), **`/pre-mortem`** (Tigers / Paper Tigers / Elephants risk classification), `identify-assumptions`, and `prioritize-assumptions` (Impact × Risk matrix). [phuryn/pm-skills, explainx.ai]
- **boshu2/agentops** (`pre-mortem` skill) — emits a PASS/WARN/FAIL verdict on a validation/slice plan before you build. [boshu2/agentops]
- **Pre-mortem** (Klein/Kahneman) — the underlying technique: imagine the project has *already failed*, then work backward to causes. Beats groupthink, surfaces threats while there's still time to act. [Wikipedia: Pre-mortem]

### OUR process (steal the best of each — runs before any Xcode code)

**Step 1 — SPEC (1 short doc).** Adapt spec-kit. Write, in order:
1. **Constitution** — non-negotiables for *this* app (clean-room/owned-content rule, no auto-post, native-first, single-agent MVP).
2. **Spec** — the one job the MVP does, user stories, explicit acceptance criteria ("done" = X observable behavior).
3. **Clarify** — list every place the spec is vague and answer it. If you can't answer, that's a hole.

**Step 2 — ASSUMPTIONS / FAILURE AUDIT (the "find the holes" core).** Before any code:
1. **List load-bearing assumptions** across Value / Usability / Viability / Feasibility (pm-skills framing). For each: *"what would make this false?"*
2. **Red-team the spec** (`/red-team-prd` style) and run a **pre-mortem**: "It's 3 months from now and the app failed — why?" Classify risks (Tigers = real & likely, Paper Tigers = scary but cheap to kill, Elephants = big & ignored).
3. **Adversarial pass** (adversarial-spec style): have ≥1 *other* model attack the spec; integrate real gaps, defend intentional choices. (Clean-room: feed it only our own spec text — never leaked/system-prompt content.)
4. **Rank every risk by CHEAPEST TEST**, not by size. The output of this step is a short ordered list: *"riskiest assumption → cheapest experiment that would disprove it."*

**Step 3 — MVP (build only what survived the audit).**
1. Build the **thinnest slice that tests the #1 riskiest assumption** — usually: single agent loop behind the HTTP contract + one Swift screen.
2. Acceptance criteria from Step 1 are the definition of done; the pre-mortem's Tigers are your test cases.
3. Add features one at a time, re-running a *mini* assumptions audit per feature. Graduate the backend to LangGraph/CrewAI only when §2's triggers fire.

**The whole point:** spec-kit gives you the *structure*, adversarial-spec/red-team give you the *holes*, the pre-mortem ranks them by *cheapest test*, and the MVP exists to *kill the single riskiest assumption first* — so you find the gaps on paper (cheap) instead of in shipped Swift (expensive).

---

## Recommended starter repos to pull (verify before relying)
- `github/spec-kit` — adopt the spec → clarify → analyze flow as our pre-build template.
- `zscole/adversarial-spec` — Claude Code plugin for the adversarial spec pass.
- `phuryn/pm-skills` — for `/red-team-prd` and `/pre-mortem`.
- (Optional, later) `swiftlang/swift-subprocess` and the launchd-agent local-server pattern for the Swift↔backend boundary.

---

## Sources
- [Multi-Agent Orchestration Frameworks 2026 — Presenc AI](https://presenc.ai/research/multi-agent-orchestration-frameworks-2026)
- [OpenAI Agents SDK vs LangGraph vs CrewAI: 2026 Matrix — DigitalApplied](https://www.digitalapplied.com/blog/openai-agents-sdk-vs-langgraph-vs-crewai-matrix-2026)
- [LangGraph vs CrewAI vs OpenAI Agents SDK: 2026 Guide — Codebridge](https://www.codebridge.tech/articles/choosing-a-multi-agent-framework-langgraph-crewai-microsoft-agent-framework-or-openai-agents-sdk)
- [LangGraph vs CrewAI vs OpenAI Agents SDK 2026 — Particula](https://particula.tech/blog/langgraph-vs-crewai-vs-openai-agents-sdk-2026)
- [CrewAI in Production 2026: Real Lessons — AgileSoftLabs](https://www.agilesoftlabs.com/blog/2026/06/crewai-in-production-2026-real-lessons)
- [AI agents in production: LangChain & CrewAI patterns 2026 — daily.dev](https://daily.dev/blog/ai-agents-guide-for-developers-langchain-crewai/)
- [The best AI agent frameworks in 2026 — LangChain](https://www.langchain.com/resources/ai-agent-frameworks)
- [GitHub Spec Kit repo](https://github.com/github/spec-kit) and [GitHub Blog: Spec-driven development with AI](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)
- [zscole/adversarial-spec](https://github.com/zscole/adversarial-spec)
- [phuryn/pm-skills](https://github.com/phuryn/pm-skills) and [pre-mortem skill — explainx.ai](https://explainx.ai/skills/phuryn/pm-skills/pre-mortem)
- [boshu2/agentops — pre-mortem skill](https://github.com/boshu2/agentops/blob/main/skills/pre-mortem/SKILL.md)
- [Pre-mortem — Wikipedia](https://en.wikipedia.org/wiki/Pre-mortem)
- [Python Backend alongside macOS Swift app — Apple Developer Forums](https://developer.apple.com/forums/thread/766464); [swiftlang/swift-subprocess](https://github.com/swiftlang/swift-subprocess); [Calling Python from Swift (PythonKit) — MLBoy](https://rockyshikoku.medium.com/calling-python-scripts-from-swift-by-pythonkit-faf41757e890)
</content>
</invoke>
