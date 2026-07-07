# Handoff: X Content Agent System (Mining Engine + Jeff Filter + Researcher Layer)

Source: Grok Chrome tab ("Right-Agent" conversation), pasted by Jeff 2026-07-05.
Materialized to disk by Fable because the Grok browser lane cannot write files.
Status: DRAFT — review gate stays human until Jeff says otherwise. No public posting without Jeff.

## Goal
A reliable, semi-autonomous cell whose job is to:
- Monitor X for high-signal posts in the AI/agent space.
- Research and connect them to Grok Go / Digital Organism work.
- Produce high-quality X posts (visuals / short videos via Grok Imagine).
- Analyze performance and adapt using X-algorithm knowledge + the Jeff Filter.

Treated as a real recurring job inside the organism, not random posting.

## Recommended agent
- Primary: **Jade** (GLM 5.2 via free/low-cost endpoints — currently `~/agent-bridge/bin/ask-glm.sh` → Cloudflare Workers AI `@cf/zai-org/glm-5.2`, mitm-ledgered, killswitch-aware).
- Heavy research/reasoning: escalate to Fable **only when necessary** (t4 contract applies: why_fable, stop conditions, receipt).
- Fallback: any agent with credits.
- Role name: "X Intelligence & Content Cell" / "Signal Miner".

## Workflow (per Grok's plan)
1. **Scan & Mine** — X MCP (once connected; browser scraping is BANNED on Jeff's account after the platform-manipulation flag) + Mining Engine pull recent high-signal posts.
2. **Score & Filter** — Jeff Filter: isomorphism, relevance to our work, timeliness, virality potential.
3. **Research** — deep research on top-scoring posts; connect to architecture/current projects.
4. **Create** — draft post + visuals/video suggestion; house voice; tie back to Grok Go / Digital Organism.
5. **Review gate** — human (Jeff) first; possibly Researcher Layer later. HARD GATE: no publish without Jeff.
6. **Post & Log** — performance data feeds back into Mining Engine / Jeff Filter.

## Success metrics
- High-quality posts/week; engagement vs baseline; Jeff-Filter hit-rate improvement over time; token cost per post stays cheap-tier.

## Implementation priorities (for Codex)
1. Basic loop (Scan → Score → Research → Create).
2. Mining Engine + Jeff Filter integration.
3. Reusable skill/prompt template `skill-x-content-agent.md` (any agent can run it).
4. Review/approval step (human first).
5. Performance logging → self-improvement.

## Blockers noted 2026-07-05
- No X MCP found connected on the mini despite Jeff recalling one exists — resolve before the Scan step is real (X API/MCP, NOT browser automation on Jeff's flagged account).
- Jade endpoint list beyond Cloudflare (NVIDIA NIM, together.ai, OpenRouter free) is research-only until Jeff approves accounts/keys.
