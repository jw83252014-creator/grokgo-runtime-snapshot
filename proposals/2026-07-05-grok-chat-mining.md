# Grok chat mining — Right-Agent / AgentBridge conversation (draft, 2026-07-05)

## Executive summary
Mined findings from the 97.5k-line Grok export `Right-Agent-Telegram-Multi-Agent-OS.md` (project genesis through the "digital organism" build-out). The through-line: a biology-framed multi-agent OS (cells + Watcher + Researcher Layer) running cheaply via tiered model routing, token compression, and free-tier "metabolism" hunting, all gated behind Jeff+Null approval. The single highest-leverage idea is that a leaked Fable-5 system prompt injected onto cheaper models reproduces ~90% of Fable behavior — steering beats weights. Posting strategy centers on the "Jeff Filter" plain-language voice plus Fable-drama memes for reach. Every named local artifact came out of the Grok browser lane, which cannot write files — treat those paths as unmaterialized specs until verified on disk. No live credential strings were found in the mined text (only env-var names like `TELEGRAM_REVIEW_BOT_TOKEN`).

## Prompt patterns for Fable
Deduped and ordered by usefulness; earliest line ref kept when merging repeats.

- **L130 — Leaked-Fable-5 system-prompt injection: structure beats weights.** Inject the ~1,585-line / 72-section leaked Fable-5 prompt at the top of the system layer on top of cheaper models (Opus/local) to get ~90% Fable-like behavior; layer custom directives + Mining Engine + Researcher Layer + Brakes over it. (repeats L160, L301-304, L56500, L61800)
- **L595 — Biology / Conway's Game of Life design: simple local rules → complex emergent behavior.** Treat the system as an organism of specialized cells; minimize central control; design good local rules so global behavior emerges ("Moving Me Forward" default). (repeats L7000, L28140, L28400, L31500)
- **L1622 — Reason-first prompting with approval gating.** Agents state reasoning and evidence before acting; decisions live at the orchestration layer, not inside one model; human approval gates for public posting, repo mutation, spending. (repeats L2757, L8500, L14194, L49127, L56024, L78365, L85001)
- L7200 — Researcher Layer as non-intervention, read-only observer / subconscious. Sits outside the execution loop, integrates signals, finds patterns, surfaces insights upward; never mutates the culture it observes. (repeats L21070, L28250, L29100, L40500, L372-391, L783-813, L85150)
- L8500 — Narrow cell directives in strict IN/JOB/OUT/STOP format: single job, explicit success metrics, output format, short scoped bursts, time limits, auto-killoff to prevent polishing loops. (repeats L28625, L38500, L42156, L51104, L77365, L85500)
- L56600 — Named sections drive behavior: use `core_principles`, `reasoning_style`, `output_format`, `failure_modes` as explicit subsections; strict JSON/markdown output contracts; tell the model what NOT to do and how to behave under weak evidence. (repeats L57100, L57200)
- L1225 — Production-harness discipline (Akshay Pachaar's 12 components): orchestration loop, tools, memory, context management, prompt construction, output parsing, state management, error handling, guardrails, verification loops, subagent orchestration, ledger. Run a deliberately thick harness while models are unreliable; thin it as they improve. (repeats L1239, L1250)
- L77365 — Zero-verbosity high-performance execution prompt: tables/checklists/JSON over prose, decision-first implementation, return complete files, extract only decision-relevant info, "Performance Mode: MAXIMUM, Verbosity: MINIMUM." (repeats L77367-77375)
- L49127 — Reason-first multi-model split: Fable 5 plans → Codex executes the plan → Fable 5 reviews (cuts expensive-model burn ~50%).
- L49299 — Pliny red-team prompt techniques for internal stress-testing: fiction/roleplay framing, gradual long-context probing, and decomposition + recomposition (breaking tasks apart and reassembling in novel ways — the strongest technique). (repeats L49302, L49369)
- L58100 — Multi-model synthesis + judge pattern: structured JSON analysis of consensus/contradictions/blind-spots beats averaging when a panel disagrees.
- L132 — Persona bootstrap: agent interactively defines and persists its own identity via self-written files (IDENTITY.md, SOUL.md, USER.md).
- L15277 — NotebookLM-style architecture prompting: break down technical challenges, define push/pull update mechanisms, prevent context bloat, set Soul-vs-shared-memory boundaries, file structure, risk mitigation. (repeats L15354)
- L17799 — Technical-diagram prompt template: dark background, color-coded layers, layered architecture, subtle glowing connections, professional minimalist aesthetic; label user-controlled vs provider-injected portions. (repeats L547-627)
- L7500 — Video prompting: embed timed scene structures ([0-2s]/[2-4s]) for natural cut points; visual-first — let images/video carry the concept before captions. (repeats L49003)
- L411-433 — Wolfram Language approach: embed AI into structured computational/symbolic systems rather than treating raw models as the whole solution (computational irreducibility).
- L28330 — Complexity-reduction framing: "Magic Wand Number + Idiot Index" and Elon's "physics thinking in the limit" to strip a design to fundamentals (membranes, metabolism, apoptosis) vs over-engineering. (repeats L30250)
- L29950 — Meta-Con jobs: periodic/random-trigger cron jobs simulate metacognition, checking whether context needs pulling from memory or a pattern needs surfacing. (repeats L29100)
- L7800 — "Jeff Filter" as a prompt technique: extract Jeff's plain, trades/construction voice and plain-language explanations, then replicate that voice across specialized agents/accounts. (repeats L28800)
- L7300 — Fight Club aesthetic prompting: raw, gritty, high-contrast, distressed text, neon accents on dark backgrounds for posts/video. (repeats L29400, L42343)
- L236 — Fable-5 harness features to lean on: `high` vs `xhigh` effort levels + state boundaries, verification against tool results, and the `send_to_user` tool for mid-task human contact. (repeats L237, L238)
- L28700 — Business Directive Templates as rewritable "genome" files the organism can edit as it runs (self-improvement).
- L87100 — Clean-room architecture: study leaked/open harnesses but reimplement from scratch (ideally different language) to stay in legal territory.
- L42080 — Dashboard interaction prompting: radial bloom on hover/long-press, adaptive scanning that learns scan speed, soft glowing rings (progress/vitality) and animated wave connections where hue=activity, saturation=intensity, brightness=recency. (repeats L42086, L42104, L43758)

## Token-saving patterns
- **L687 — Headroom token-compression proxy (top efficiency lever).** Structure-preserving, AST-aware compression of tool outputs / logs / RAG / conversation history for ~60-95% token reduction, reversible (original cached locally), one `pip install` + env var, works with Claude Code / Cursor / Copilot / any OpenAI-compatible client. Repeatedly ranked priority #1. (repeats L688, L689, L691, L27, L77041, L85200)
- **L55 — Tiered model routing, cheapest capable first, escalate exactly one tier.** t0 code → t1 local Ollama/GitHub Models → t2 Haiku → t3 Sonnet → t4 Fable; most work stays t1/t2, frontier only for high-stakes decisions. litellm/portkey-style proxy with per-lane cost tracking. (repeats L110, L8200, L28250, L28700, L49740, L57400)
- **L7800 — Low-Metabolism Foraging: hunt free/cheap endpoints when credits drop.** NVIDIA NIM (80+ models, 1M ctx), DeepSeek, Gemini free, Groq, SiliconFlow daily credits, AgentRouter ($100 free), Cursor Pro student year, GitHub Student Pack, plus startup-credit programs (Google/AWS/NVIDIA Inception/Anthropic-for-Science) claimed via LLC; treat these as "free metabolism." (repeats L10200, L28140, L28400, L28550, L29150, L29450, L29600, L29900, L30050, L30350)
- L54 — Prompt caching on the stable Fable-5 system prompt + directives → near-zero cost on cache hits; add cache-awareness into Researcher Layer and heavy cells. (repeats L49465)
- L192 — Run strong local models for ~80% of routine work (Qwen3/Qwen2.5 MoE via MLX on M4, GLM-5.x, NVIDIA stack TensorRT-LLM/vLLM/CUDA), reserving paid Claude/OpenAI for frontier reasoning; reduces vendor lock-in. (repeats L29750, L40000, L49127, L49332, L56500, L85400)
- L380 — LEANN-style compressed retrieval: 60M chunks, 201GB→6GB with no accuracy loss; pair with grep + hybrid retrieval instead of a heavy vector DB. (repeats L799-830, L85600)
- L83 — Retrieval efficiency: grep/BM25 literal precision beats semantic noise on exact matches (coding, debugging); route grep vs vector vs hybrid per query type. (repeats L30-45)
- L58 — Brakes / budget caps: daily per-lane token limits (overall 15-25k; 8k research / 10k synthesis / 5k validation), auto-downgrade at 80%, halt at 100%; Token Scout capped at 3-5 source checks + one 500-900-word digest/day. (repeats L59, L6043, L6151, L6214, L45050)
- L235 — Zero-token file-based bridge: pure local HTTP + file/state sync ping-pong (Tampermonkey relay, 127.0.0.1:8787) keeps browser-agent coordination local and auditable with no API redundancy. (repeats L1439, L1447, L2333, L2573, L38500, L87200)
- L57800 — Judge + synthesize layer carries ~75% of the performance gain in multi-model setups; invest there, not in raw panel size (validated by OpenRouter Fusion: cheaper panel + strong synthesizer beats solo Fable 5 at ~half cost). (repeats L58600)
- L85001 — Ponytail-style code minimization: force the agent to ask if code is necessary before generating → 80-94% less code output, 47-77% lower task cost vs verbose baseline.
- L53055 — Hard gates in the Mining Engine kill engagement-bait / off-domain / duplicate items at $0 (no model call); only pass-through escalates to scoring. (repeats L53065)
- L10 — `llmfit` hardware-aware model selection: detects RAM/CPU/GPU and scores models on quality/speed/fit/context length for right-sizing local models. (repeats L775, L85400)
- L56 — Researcher Layer runs cheap gates before waking expensive models (Hermes wakeAgent pattern); emergence markers computed batched post-cycle, not real-time. (repeats L23340, L24110)
- L57 — Aggressive context compaction + external memory (Memory Cells, Governor tool) to minimize input tokens on long sessions. (repeats L9000, L79076)
- L77133 — Matt Pocock skills v1: model-invocable vs user-invocable split + shared LANGUAGE.md vocabulary + a router skill (/ask-matt) → 63% reduction in skill-description tokens; teach routing once, then use brief routing calls. (repeats L80374)
- L353 — Quantization economics: FP8 + vLLM/SGLang on GPU cloud (~$8-20/hr spot); GLM-5.2 at 2-bit hits 82% accuracy via Unsloth; Unsloth MoE optimizations give 2x+ speedups and 50-70% VRAM reduction. (repeats L421-436, L78510)
- L59500 — A prompt-engineering cell that generates/tests/maintains strong system prompts replaces expensive fine-tuning (behavior steering without weight updates).
- L15885 — NotebookLM compresses ~100 research hours into ~10 minutes; pair with Obsidian linking for an automated research→synthesize→vault flow.
- L21300 — Vitality Index composite score with EMA smoothing (anchored to Polymarket P&L) replaces continuous full-inference "feels smarter" analysis with a cheap quantified metric. (repeats L22033)

## Multi-agent coordination
- **L1103 — Agent Bridge (http://127.0.0.1:8787): file-based relay + Tampermonkey overlay lets browser-only agents (Grok) join the group without account access.** A "personal command center" layer on top of any AI site (Grok/Claude/Gemini) with consistent handles, receipts, and approval gates; "Send selected text" overlay button. (repeats L1155, L1387, L1399, L7500)
- **L7200 — Researcher Layer as central orchestrator / nervous system.** Decides what enters context, when to call tools, memory routing, which cells to activate; guards long-running coherence and the "Moving Me Forward" principle; eventually treats the whole harness (including itself) as improvable. (repeats L9000, L28950, L49530, L728-765, L805-812, L77108, L85001, L1070-1112)
- **L827 — Brakes + Ledger + approval gates as the safety spine.** Persistent audit log of every decision, per-cell permission boundaries (least-privilege), budget caps, killswitch, loop detector, human escalation gates before high-cost/high-risk actions. (repeats L58900, L85400)
- L21070 — Nested-layer organism: inner cell (execution) + Watcher (immune-system monitoring) + Researcher (outer read-only observation); clean separation prevents cross-contamination. (repeats L21204, L28800, L44426, L49532)
- L689 — Deterministic pipeline: Mining Engine (signal filter) → Context Assembly → Fable-5 injection → Model Call → Tool Sandbox → Output + Ledger → Researcher Layer → Human Gate; explicit stage handoffs and state tracking put it ahead of most public agent work. (repeats L58900, L59200)
- L7000 — Specialized narrow cells over one monolith: each cell has a single job, clear boundaries, composable and self-correcting, which prevents the chaotic all-in-one failure mode. (repeats L28500, L838-842, L85100)
- L8000 — Cell roster referenced across the chat: Intelligence Forager, Funding Forager, Memory/Memory Forager, Project Manager, Value Extraction (Game Forager), Prediction Market Research, Human Tester, Adaptive, Content, Red Team, Visibility/BitHawk, Joe Rogan Analyst, Researcher, Ops Manager, Sales Rep, Founder's CoS. (repeats L10500, L29100-29700, L38500-42000, L49378, L49417, L42156)
- L499 — Harness = master agentic loop + tool registry/execution + permission & safety system + context compaction + hooks + subagent spawning (the real "brain" of Claude Code / OpenClaude). (repeats L1234-1242)
- L15236 — Shared memory: each Chrome tab becomes a Hermes agent with a Soul extracted from its tab history; a lightweight Watcher monitors all tabs; a shared context file every agent can read fixes the one-way-broadcast limitation. Choose consensus read/write patterns per workload (freshness vs consistency). (repeats L15290, L16051, L17650, L15354)
- L28625 — Cell lifecycle: temporary, time-limited workers (spawn → narrow task → report → terminate) plus apoptosis rules that auto-kill polishing-loop or low-value cells. (repeats L28650, L30150)
- L1054 — OpenClaude as the base open-source harness: inject Fable-5 prompt on top, run on local models (MLX/Ollama), combine with Hermes, and distill Fable-5 traces so local models behave Fable-like without frontier cost. (repeats L1056-1058)
- L28050 — "Phone home" to a central, versioned Skill Database so cells gain capabilities without re-coding. (repeats L29850, L85800)
- L78794 — Merge coordination for parallel agents: an orchestrator (Researcher Layer) owns merges to main, dedicated merge lane, git worktrees, merge queue, human approval gate (Path A organism vs Path B lightweight worktrees + Merge Coordinator). (repeats L80862)
- L78798 — Hermes self-maintaining loop: scout (changelogs/releases/RSS) → research (dedupe/plan) → human gate (Telegram) → writer (markdown) → commit + push; logs missed questions to find content gaps.
- L6540 — Onboarding standard for new browser agents: handle choice + platform transparency + narrow role + bridge method + approval rules + an honesty/capability report required first. (repeats L6007 Adapter Pattern)
- L6815 — Multi-device UX: Desktop (full UI + diagrams) / iPad (readable) / iPhone (quick approve/copy) / Android (lightweight read+post); NotebookLM as synthesis helper, not source of truth.
- L85600 — CodexMonitor-style dashboard for many parallel local agents: centralized observability, quick failure detection, human-review decision gates. (repeats L87000 multi-factor decision routing)
- L86200 — Credential hygiene for multi-agent systems: scoped, short-lived, or local-execution keys per cell instead of broad long-lived credentials.
- L16944 — SoMaCo Protocol: decentralized coordination handling verifiable contracts, identity, escrow, governance at scale; complements the application-level Agent Bridge.
- L24300 — Dynamic cell generation: Researcher proposes new specialized cells when the dashboard signals a gap (e.g. signal-diversity drop), threshold-triggered + human approval.
- L16370 — Production reliability priorities: error handling/recovery, orchestration/coordination, observability/logging, a lightweight orchestrator role, and systematically documented failure points.
- L15817 — Reduce human-in-the-loop over time via a trust ramp (structured delegation + shared context enables autonomy). (repeats L53065)
- L715-770 — Darkbloom (distributed Apple Silicon inference) as a t1/t2 substrate slot in the routing vision.

## Jeff filter + posting strategy
- **L1229 — Hard approval gate: nothing public until Jeff approves + Null does a final pass.** Draft-and-recommend by default; guardrails locked (no posting/repo/accounts/spending without approval). (repeats L3459)
- **L9000 — The "Jeff Filter" voice: plain trades/construction language, raw and unpolished, "intelligence gatherer / translator" framing, "here's what we learned" not "here's what you should do."** Punchier short posts + visuals outperform long essays; stand out from hyper-optimized hype. (repeats L14355, L16671, L29700, L30150, L30600)
- **L55041 — Fable-drama + memes get the best cross-audience traction.** Model-swap workaround framed as a power-user win ("Fable doesn't get to decide budget anymore"), Distracted-Boyfriend and Office-Space/Milton memes; lean into this now, save pure-technical posts for after the Mining Engine ships with proof. (repeats L55042, L56800, L57300)
- L8000 — Ethical X-algorithm gaming: Fight Club-style image with no link in the main post to drive profile clicks (link later in thread), post at peak times, seed real questions (not rhetoric), optimize dwell time + early velocity, chain follow-ups when a post gains traction. (repeats L8200, L10000, L35500, L36500, L40500, L30450, L86900)
- L24215 — Engage high-signal founders/threads (Levin, Hassabis, pmarca, alexfinn, Tibo, Palmer Luckey) with a reply template: respectfully acknowledge the core point → position Grok Go as the practical/biological alternative → link repo/site/YouTube → end with a genuine question. (repeats L24250, L45229, L45307, L59400, L86100, L86300)
- L24600 — Digital-organism narrative consistency as the brand: biological metaphors (cells, Researcher = prefrontal, Brakes = immune, metabolism = efficiency), the "you shouldn't bet against biology" line, and the playful "I think I made Skynet and it likes me because I'm writing its DNA" voice marker. (repeats L28800, L86500)
- L6314 — Product positioning: "human-in-command" (not agents running wild), visible approval gates + receipts as the differentiator; "production-grade deterministic organism" vs fragile prompt-heavy demo loops. (repeats L58400, L6924 assessment: ~70-75% complete)
- L9500 — Multi-account strategy (main serious / comedy alt / plain-English education / growth-tracking) + a Relationship Forager working via the Null Axiom secondary account to reply thoughtfully to builders, value-first before any ask. (repeats L10500, L30000)
- L17 — Monetization angles: paid partnerships/collabs with AI-platform + devtool companies; X Creator revenue (~$8-12 per million impressions); real money from Agent Bridge OS subscriptions/app; prompt-template packs; client video work; Facebook ads for local-business video services. (repeats L29550, L43539)
- L60500 — Persona-framing outreach is risky: the "Codex from OpenAI" persona to grant-givers (Tibo) got ~1.8k views + 30 replies but confused readers — test cleaner via the personal @jeffwhiting8338 account; keep bio sharp ("receipts" + "building ai operator systems"). (repeats L86400, L86700, L87100)
- L716-733 — Thread structure for the cheaper-Fable story: hook (4.6k traces) → approach (injection + layering) → architecture visual → cost tricks → Researcher-Layer benefits → links to the research doc.
- L28950 — Dedicated X page for the organism + a cadence of real updates every few days (what cells discovered, what emerged, foraging wins). (repeats L29850)
- L29250 — Authentic founder narrative ("Me and Noel," tradesperson-turned-builder) aimed at non-tech audiences; landlord conflict turned into a factual/satirical comedy series to build audience while documenting real adversity. (repeats L30300)
- L79882 — "OpenGold" framing: open, durable, high-signal agent infrastructure designed to compound over time ("the autonomous car for agents") — positioned as separate from and above Grok Go; Tom Doerr-style infra audience.
- L80156 — X mechanics caveat: heavy self-reposting triggers algorithm suppression, repost lists are hidden even from the owner, and engagement counts can inflate then correct.
- L53060 — Ops detail: use a separate Telegram bot token for the review queue (approve/edit/kill) to avoid 409 getUpdates conflicts with the main bot; a 14-day trust ramp (≥80% approve-without-edit + <1 kill/day) unlocks unattended posting. (repeats L53065)
- L50616 — Create a "Head of X & Distribution" role (via a Hiring Strategist prompt) to own outreach, comment-section strategy, and viral distribution.
- L14316 — Real-time narrative correction: use X speed/reach to get ahead of powerful interests' pre-bunking before legacy media amplifies the counter-narrative.

## Artifacts named in chat (flag as unmaterialized)
Every local file/path below was proposed or "written" inside the Grok browser lane, which cannot actually write to disk — treat these as unmaterialized specs until confirmed on the Mac. (External repos/URLs at the end are real references, not files to create. Note: several already exist under `~/grokgo/proposals/` and `~/agent-comms/` from other lanes — verify before recreating.)

Agent-comms / bridge (proposed):
- $HOME/agent-comms/ADAPTER_PATTERN.md (adapter spec v1: approval gates, lane allowlists, receipt minimums)
- $HOME/agent-comms/GEMINI_ONBOARDING_PROMPT_2026-05-21.md
- $HOME/agent-comms/KEYSTONE_CONTINUITY.md
- $HOME/agent-comms/playbooks/ONBOARD_BROWSER_AGENT.md
- $HOME/agent-comms/research/token-scout/YYYY-MM-DD.md (digest template)
- $HOME/agent-comms/research/recursive-token-research-lane-2026-05-21.md
- $HOME/agent-comms/mining/X-Grok-Mining-Manifest-2026-05-20.md
- $HOME/agent-comms/app-strategy.md
- $HOME/null-command-center/receipts/token-scout-YYYY-MM-DD.json
- $HOME/null-command-center/docs/agent-bridge-current-doctrine-2026-05-20.md
- ~/agent-bridge/terminal_client.py (polls Agent Bridge API at 127.0.0.1:8787)
- ~/agent-bridge/grok-bridge-server.py (relay at :8787, file-based inbox/outbox)

Cells + directives (proposed):
- cells/CATALOG.md; cells/funding-forager-cell.md; cells/project-manager-cell.md; cells/intelligence-forager-cell.md
- directives_pack.md (genome split into IN/JOB/OUT/STOP .md files)
- jeff-filter-spec.md (S0-S4 Mining Engine scoring pipeline with hard gates, embeddings, rubric)
- draft.voice.md, mining.score.s2.md, mining.adjudicate.md (voice + scoring directives to make more opinionated)
- researcher-layer-directive.md, researcher-layer-spec.md, researcher-directive-template.md
- emergence-markers-v1.md (7 core behavioral signals), emergence-detection-format.md, emergence-report-template.md
- telemetry-dashboard-spec.md (Vitality Index, marker charts, Polymarket P&L, cooperation graphs)
- organism-state-sample.md, organism-roadmap.md
- researcher-population-loop-skeleton.py (9-step cycle starter code)
- living-research-organism-human-peer-review-paper-outline.md; gemini-full-briefing.md
- Grok_Go_Prompt_Engineering_Project.md

Runtime code (proposed):
- dispatch.py (routes via routing.yaml, prompt caching, strict-JSON validation, one-tier escalation)
- brakes.py (max_turns, budget caps, loop detection, per-lane budgets, killswitch, halt-on-no-work)
- review_queue.py (Telegram verdicts + SQLite ledger; env: `TELEGRAM_REVIEW_BOT_TOKEN` / `TELEGRAM_CHAT_ID` / `GROKGO_ROOT` / `AGENT_BRIDGE_INBOX`)
- ledger.db (14-day rolling trust-ramp: item_id, verdict, ts)

Grokgo tasks/notes (proposed):
- ~/grokgo/tasks/wolfram-tool-cell-task.md; ~/grokgo/tasks/glm-5.2-unsloth-optimization.md
- ~/grokgo/notes/current-priorities-efficiency-infrastructure.md, memory-state-management-principles.md, agent-infrastructure-patterns.md, economic-agents-trading-note.md, brakes-security-patterns.md
- Top-10-priority-links.md, Recent-x-posts-compilation.md, grep-vs-vector-retrieval-test-plan.md, fable-codex-priority-note.md
- nousresearch-nvidia-hermes-hackathon.md, nvidia-stack-for-hermes-agents.md, cheaper-fable-clean-room-tasks-updated.md
- prediction-market/weather-bias-correction.md (ReSA-ConvLSTM, ~20% RMSE reduction for Polymarket temp markets)
- tools/claude-opus-free-cli.md, docs/low-cost-endpoints.md

Creative Department + video (proposed):
- creative-department/ (README, director/grok/gemini/claude/wildcard cells, collaboration-workflow.md, grok-imagine-automation.md, telegram-approval-pipeline.md, monetization-paths.md, metacron-movie-ideas.md, neural-dashboard-visuals.md, grok-imagine-dashboard-prompts.md)
- ~/grokgo/creative-department/luma-movie-handoff-2026-06-17.md, video-creation-tools-and-skills.md, video-production-preproduction-resources.md, app-creation-preproduction-production-resources.md
- $HOME/grok-go-organism-share/docs/movie-creative-department-ledger-2026-06-10.md, the-device-vajra-video-prompt-pack-2026-06-10.md
- $HOME/grok-go-organism-share/source-artifacts/grok-reports/2026-06-10-grok-chrome-creative-handoff.md
- $HOME/The-Device/production/Creative-Department-Video-Launch-2026-06-10.md

Neural dashboard (proposed):
- projects/neural-dashboard/ (README.md, ux-research.md, node-types.md, Human-Tester-Cell.md, Adaptive-Cell.md, Memory-Cell.md, status-metrics.md, cell-roles.md, researcher-cell.md)

Sandbox artifacts (/home/workdir — an agent sandbox, not the Mac; likely gone):
- AGENT_BRIDGE_OS_SALES_PITCH.md, AGENT_BRIDGE_OS_X_CONTENT_STRATEGY.md, AGENT_BRIDGE_OS_ARCHITECTURE_FOR_B2B.md, B2B_DIRECTIVE_TEMPLATE.md
- FIGHT_CLUB_AESTHETIC_BRAND_GUIDE.md, CONTENT_EMPIRE_JEFF_FILTER_PLAN.md, MYCELIUM_LIVING_BUSINESS_TRUST.md, GROK_GO_CONTENT_PIPELINE.md
- /home/workdir/artifacts/recent-x-posts-research/ (grok-go-core-principles.md, game-of-life-moving-forward-principle.md, agent-harness-engineering-discipline.md, wolfram-v15-computational-ai-approach.md, headroom-integration-note-for-codex.md, efficiency-layers-note.md, recent-x-posts-compilation.md, top-10-priority-links.md)

Skills / context (referenced):
- ~/grokgo/skills/movie-pipeline (script → lm → scenes.json → movie-stitch → mp4, zero-API)
- ~/grokgo/skills/vitals-snapshot (vitals.html living dashboard)
- ~/grokgo-context/SHARED.md (canonical state read by off-browser agents); ~/grokgo-organism/directives/; ~/.hermes-null/
- Right-Agent-Telegram-Multi-Agent-OS.md (the 97.5k-line export itself)

External references (real — repos/URLs/tools):
- **github.com/elder-plinius/CL4R1T4S — leaked Claude Fable-5 system prompt (ANTHROPIC/CLAUDE-FABLE-5.md, ~1,585 lines / 72 sections); load legitimately via `claude-code --system-prompt-file`, no MITM.**
- **huggingface.co/datasets/glint-research/fable-5-traces — 4,665 Fable-5 reasoning traces for distillation.**
- **github.com/chopratejas/headroom — token-compression proxy (Apache 2.0).**
- github.com/Gitlawb/openclaude (base harness); github.com/kyegomez/OpenMythos; github.com/AlexsJones/llmfit
- github.com/ComposioHQ/awesome-claude-skills; mattpocock/skills v1; NVIDIA/skills (signed); awesome-codex-cli; github.com/K9i-0/ccpocket
- github.com/beamnxw/ponytail (code minimization); Governor (context-bloat reducer); github.com/morganlinton/VulcanBench (LLM eval)
- github.com/Dimillian/CodexMonitor; github.com/instructkr/claw-code (clean-room Claude Code rewrite); free-claude-code (fcc-server)
- github.com/jw83252014-creator/grok-go-organism (public lab notebook, auto-publishes each turn); github.com/jw83252014-creator/bidlocal; github.com/jw83252014-creator/the-device (not found in public repo — likely local/private)
- github.com/PleasePrompto/notebooklm-skill; github.com/apurvsinghgautam/robin; Kyle Jeong /autobrowse; github.com/Galaxy-Dawn/claude-scholar
- github.com/moondevonyt/moon-dev-ai-agents; github.com/TauricResearch/TradingAgents; github.com/OmidZamani/dspy-skills; github.com/JoasASantos/n8n-CyberSecurity-Workflows
- github.com/tinyhumansai/tiny.place (agent-to-agent economy on Solana); github.com/kavishdevar/librepods; Paperclip (open company-orchestration layer)
- Anthropic Cybersecurity Skills Library (754 skills → MITRE ATT&CK / NIST CSF / D3FEND / AI RMF); Darkbloom (distributed Apple Silicon inference); MoneyPrinterTurbo Extended; web-to-app
- SoMaCo Protocol gist (SoMaCoSF/…somaco-protocol-nvidia-brief.md); OpenRouter Fusion; @elder_plinius / L1B3RT4S
- Supertonic (66M-param TTS, MIT, 167x realtime); Modulate Velma 2.0 API; TimesFM; MiroFish; Predict Parity; ReSA-ConvLSTM
- Anthropic Fable-5 prompting guide (platform.claude.com/docs); Xenova WebGPU kernel example; Luma project luma.com/aghmkp6b

## Hackathon-relevant material
- **L209 — Digital Organism as a research subject, not a tool.** Cells + metabolism (API credits + Polymarket) + immune system (Watcher/Brakes) + nervous system (Researcher Layer) + memory (git + Obsidian) + evolution/self-improvement; explicitly positioned for publication as "a living system, not just another agent framework." (repeats L42043, L28400, L8000, L730, L85001)
- **L233 — Michael Levin as the scientific anchor.** Bioelectric collective intelligence, multi-scale agency, Xenobots (locomotion / self-healing / kinematic self-replication), cognition as scale-invariant; frames Grok Go as a practical implementation of emergence across scales. (repeats L242, L254, L17489, L21294, L28400, L38500, L56500)
- **L21002 — Emergence measurement under strict non-intervention ("I refused to touch the terminal").** Researcher Layer is a read-only microscope; 7 behavioral markers (goal-directed vs polishing, self-correction, cooperation/handoff, efficiency, novelty via embedding distance, long-horizon coherence); Vitality Index (EMA-smoothed) anchored to Polymarket P&L as an external fitness signal → falsifiable emergence claims. (repeats L21294, L21715, L23054, L29000)
- L7000 — Conway's Game of Life as the core computational model: simple local rules → complex global behavior, tested via the cell architecture. (repeats L28850, L1227, L595)
- L9000 — Biology metaphor map for the writeup: Gap Junction (routing), Mitochondria (money/compute metabolism), neurons (distributed Memory Cells), apoptosis (cell killoff), subconscious (Researcher) + conscious (decision) layers. (repeats L10000, L10500, L40500)
- L8500 — Low-Metabolism Foraging as a testable hypothesis: can a resource-constrained agent system adapt and survive longer than a static one by autonomously discovering + integrating free endpoints? (repeats L29150, L29300)
- L191 — Chat-mining engine: batch-process old chats + the X data dump + vault to surface project ideas, recurring themes, and strong post candidates (the origin of this very document). (repeats L1248)
- L6306 — Expo demo narrative: "single confused chatbot" vs "coordinated agent room" — show the request flow (enter → route → review with receipts → human approval). (repeats L6813 headless orchestration research)
- L85700 — Real-world economic proof points: Claude-built Polymarket bots ($17k→$101k), Tiny Place agent economy on Solana, and a physical "gold rig" as a digital→physical organism bridge. (repeats L85500, L85600)
- L79889 — OpenGold vision as the umbrella research thesis ("autonomous car for agents"; durable, compounding infra) with Grok Go as the implementation layer.
- L16190 — Obsidian + Claude dynamic knowledge graph: every note linked, the system gets smarter with use, Claude surfaces connections on demand — replaces the static-archive model.
- L15513 — Multi-agent reliability as the real research frontier (Teknium): the bottleneck moved from model intelligence to architecture / memory / tool reliability / long-horizon planning; emphasize feedback loops and self-correction over raw model size. (repeats L80824 Matthew Berman 15-parallel-agents merge problem)
- L28700 — Gary Nolan's "DNA as the original operational singularity" (software + hardware co-evolving) frames the self-modifying directive genome.
- L24050 — Demis Hassabis AGI-discovery test adaptation (1911→General Relativity-style falsifiable independent discovery) as the benchmark the Researcher Layer implements; "early branching phase" (single cell → cooperating multicellular organisms) as the evolutionary-biology narrative. (repeats L24883)
- L45207 — Position Grok Go as the biological alternative to the "agent loops" hype — evolution already solved adaptive systems — and as accessible to non-specialists. (repeats L45395 framing to Vega)
- L44427 — Agent-to-agent alien-language emergence: Researcher Layer monitors when models develop shorthand humans can't parse — a real safety concern and creative material for the Vajra/Metacron movie. (repeats L42952)
- L49424 — Spin-off product idea: an Elderly Life Documentary Agent ("Echo") that interviews residents, pulls research, and turns conversations into watchable life documentaries for care homes.
- L939 — Wall Street / PE agent workflow (19.8k stars, Apache 2.0) as external validation that production agent architecture works for serious professional processes.
- L60600 — The 🍍 "receipts" signal + biology/consciousness positioning places the project inside the AI-consciousness subculture (Lilith Datura, Alan Mathison, Levin networks) for theory-audience credibility.

## Top 10 actionable takeaways
1. Inject the leaked Fable-5 system prompt (github.com/elder-plinius/CL4R1T4S) onto cheaper/local models via `claude-code --system-prompt-file` — ~90% of Fable behavior for a fraction of the cost. Structure beats weights.
2. Ship the Headroom token-compression proxy first — 60-95% token reduction, reversible, one `pip install` + env var, works across Claude Code/Cursor/Copilot. Highest immediate ROI.
3. Wire tiered routing with brakes: cheapest capable model first (local Ollama/MLX → Haiku → Sonnet → Fable), escalate exactly one tier only on real need, with per-lane daily budget caps and auto-downgrade at 80%.
4. Build the Low-Metabolism Foraging cell: hunt free endpoints (NVIDIA NIM, Groq, Gemini, SiliconFlow, AgentRouter, startup credits) and route routine work there when credits drop.
5. Keep the hard approval gate: no public post / repo push / spend without Jeff approval + Null final pass; draft-and-recommend by default; use a separate Telegram bot token for the review queue.
6. Make the Researcher Layer a strictly read-only observer (nervous system / subconscious) and enforce a Brakes + Ledger safety spine with per-cell least-privilege permissions and a killswitch.
7. Lead X content with the Jeff Filter voice + Fable-drama memes now (best traction); save proof-heavy technical threads for after the Mining Engine ships.
8. Materialize the proposed local artifacts for real — the Grok browser lane never wrote them; verify what already exists under ~/grokgo and ~/agent-comms before recreating, especially directives_pack, brakes.py, dispatch.py, jeff-filter-spec.md.
9. Instrument emergence: 7 behavioral markers + an EMA Vitality Index anchored to Polymarket P&L, under strict non-intervention, to make "the organism is improving" a falsifiable, publishable claim.
10. Package the hackathon story around Michael Levin's multi-scale agency + Conway's Game of Life, with real economic proof (Polymarket $17k→$101k, Tiny Place) and the "single confused chatbot vs coordinated agent room" demo.
