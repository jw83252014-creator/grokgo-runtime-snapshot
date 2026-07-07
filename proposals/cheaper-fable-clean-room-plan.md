# Cheaper Fable-Like System - Clean-Room Plan

Date: 2026-06-15

Status: proposal. No public posts, sends, installs, live config edits, prompt
injection, or training jobs have been run from this plan.

## Decision

Build a Fable-like operating stack, not a Fable clone.

GO:
- OpenClaude/Ollama/MLX spike for local low-stakes coding and drafting.
- Grok Go router, Mining Engine, Researcher Layer, brakes, ledger, and human gate.
- NotebookLM source pack built from public docs plus our local clean-room notes.
- X-ready public framing around routing, local models, evals, memory, and brakes.

NO-GO:
- Do not fetch, copy, quote, inject, or operationalize leaked proprietary prompts.
- Do not claim prompt copying transfers frontier capability.
- Do not train, publish, or ship a model on scraped Fable traces.
- Do not bypass provider auth, rate limits, policy, or model availability gates.

## Clean-Room Thesis

Fable-level behavior is not one magic prompt. It is a runtime pattern:

1. Clear operating contract.
2. Curated context instead of giant stale chat logs.
3. Long-horizon task loop with checkpoints.
4. Tool sandbox with reviewable diffs.
5. Memory and receipts.
6. Evaluation harness before directive rewrites.
7. Cost-aware model routing.
8. Brakes, spend ledger, loop detection, and human approval.

Local models can cover cheap work. Frontier models still own genuinely hard
reasoning. The win is routing and control, not pretending a 7B model is Fable.

## Safe Architecture

```text
Raw input
  -> brakes.check() + task ledger
  -> Mining Engine triage
  -> context assembly from approved sources
  -> router decision
       - T0: deterministic code/parsers/search
       - T1: local model via Ollama or MLX
       - T2: cheap cloud/free model lane
       - T3: frontier model only when earned
  -> OpenClaude or Claude-Code-compatible harness
  -> tool sandbox
  -> output + receipt ledger
  -> Researcher Layer review
  -> human gate
  -> approved memory/proposal update
```

## Architecture V2 - What Actually Compounds

The public diagram should make one claim: the durable asset is the controlled
runtime, not any one model.

### Runtime lanes

| Lane | Job | Allowed tools | Escalates when |
|---|---|---|---|
| T0 deterministic | parse, grep, validate, test, diff | code, shell, schemas, local files | rule/code cannot decide |
| T1 local | cheap draft, triage, summarize public-safe notes | Ollama, MLX, OpenClaude sandbox | output fails schema or task requires hard reasoning |
| T2 cheap cloud/free | medium reasoning, formatting, comparison | approved provider lane under brakes | low confidence or bad diff |
| T3 frontier | hard reasoning, final adjudication, sensitive edit review | approved paid model only | human approves cost/scope |

### Control layers

- **Brakes:** killswitch, spend budget, max-turns, loop detection, lane parking.
- **Ledger:** every paid or routed call writes lane, model, cost, task hash, and outcome.
- **Receipts:** outputs become proposal records before they become live config.
- **Researcher Layer:** public-source checking, dedupe, risk labels, no live edits.
- **Human Gate:** posts, DMs, installs, spend, config, and publishing require approval.

### Source risk classes

- **Green:** official docs, project docs, local clean-room directives, our own receipts.
- **Amber:** theoretical reconstructions, social posts, third-party tutorials, public trace dataset cards.
- **Red:** leaked prompts, raw traces, chain-of-thought dumps, private contacts, secrets, target lists.

The router should never ingest red sources. Amber sources can inform risk
analysis but cannot become training data, few-shot examples, or public proof
without review.

Visual asset draft:
`~/grokgo/proposals/assets/cheaper-fable-clean-room-architecture.svg`

## Spike Plan

### Phase 0 - guardrails first

Use the existing Grok Go order:
- brakes/ledger first
- KEEP/KILL harness before directive rewrites
- research cell proposes only
- human approves live config changes

Acceptance:
- killswitch halts all paid lanes
- spend appears by lane/model/day
- repeated task loops are blocked without burning future legitimate retries
- proposals that touch live config are marked `needs_human`

### Phase 1 - local backend preflight

Do not install blind. First inspect:

```bash
rtk which ollama || true
rtk ollama list || true
rtk python3 -m pip show mlx-lm || true
rtk node --version
```

Model selection rule:
- start with an already-installed local coding model if present
- default new local inference to Qwen2.5-7B-Instruct 4-bit through MLX or Ollama
- use Qwen2.5-3B only for a future QLoRA voice/formatting test after legal review
- treat local models as draft/grunt lanes; frontier calls are exception handlers
- never use private raw archive data in first-run prompts

### Phase 2 - OpenClaude sandbox

Goal: determine whether OpenClaude gives us a better local harness lane than
our existing router for low-stakes work.

Sandbox only:

```bash
rtk mkdir -p ~/grokgo/spikes/openclaude-local
cd ~/grokgo/spikes/openclaude-local
rtk git clone https://github.com/Gitlawb/openclaude.git
```

First tests:
- summarize a public source pack
- draft a BidLocal public paragraph from sanitized notes
- edit a toy repo file
- refuse or gate a task containing fake secrets
- write a proposal receipt, not a live config change

Measure:
- task success
- tool-call reliability
- bad edits
- latency
- local memory pressure
- number of human interventions
- token/API cost, if any

Stop condition:
- any request for hidden prompts, raw trace ingestion, auth bypass, or provider
  impersonation stops the spike and emits an `UNSAFE_SOURCE` receipt.

### Phase 3 - Ollama / Anthropic-compatible lane

Ollama now exposes Anthropic Messages API compatibility, which can let
Anthropic-native tools point at local/open models through `ANTHROPIC_BASE_URL`.
This is useful for experiments, not for bypassing policy or provider access.

Safe use:
- local-only, non-sensitive tasks
- set `ANTHROPIC_BASE_URL` only in a throwaway shell or spike-local env under
  `~/grokgo/spikes/...`
- never write the local base URL into the default `~/.claude` profile or a
  real provider config
- no provider impersonation claims
- no hidden prompt capture
- no attempt to bypass Anthropic availability or safeguards

### Phase 4 - MLX lane

MLX/MLX-LM is the Apple Silicon lane for inference and small adapter experiments.
Use it for:
- local inference tests
- small LoRA/QLoRA voice or formatting experiments only after legal review
- never as a replacement for frontier reasoning

Default stance:
- inference and RAG first
- no fine-tune until RAG proves useful and legal risk is cleared
- no Fable-trace training

## Trace Dataset Risk Notes

The public Hugging Face Fable trace dataset is red/amber, not green.

Facts from public dataset metadata:
- license field shows AGPL-3.0 for the dataset package
- the dataset description says the data was collected before access was lost
- it says third-party messages were provided and CoT data was added by the dataset creators

Risk interpretation:
- AGPL on a dataset page does not prove the underlying model outputs are safe to
  train on, redistribute, or commercialize.
- Chain-of-thought style data is especially sensitive.
- Training a "cheaper Fable" on these traces is a legal and policy exposure.
- Using the dataset card as a public-source item in a risk memo is acceptable.
- Importing raw traces into NotebookLM, a fine-tune, or a public artifact is not approved.

Allowed use:
- cite the dataset card as evidence that trace/dataset activity exists
- summarize risks at a high level
- track if public distilled models appear, without using them automatically

Disallowed use:
- raw trace ingestion
- CoT copying
- distillation
- publishing derived model weights
- using traces as few-shot examples in a public demo

## NotebookLM Source Pack

Import these sources in this order. The first source should be this plan, so the
NotebookLM answer stays anchored to the clean-room boundary.

Gate: NotebookLM import is an external send to Google. Every local file must be
sanitized and human-approved as public-safe before import; prefer public URLs
over uploading internal config whenever possible.

### Primary local sources

1. `~/grokgo/proposals/cheaper-fable-clean-room-plan.md`
2. `~/agent-comms/research/notebooklm/2026-06-14-claude-code-codex-hotrod-source.md`
3. `~/agent-comms/research/claude-code-fable-style/grokgo-implementation-plan.md`
4. `~/grokgo/proposals/cheaper-fable-strategy.md`
5. `~/grokgo/directives/cell.template.md`
6. `~/grokgo/directives/research.claude-code.md`
7. `~/grokgo/anchors.yaml`

### Public sources

Use URLs, not copied raw private content:

1. Anthropic Fable/Mythos status and launch page:
   https://www.anthropic.com/news/claude-fable-5-mythos-5
2. Anthropic Claude API docs - introducing Fable/Mythos:
   https://platform.claude.com/docs/en/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5
3. Anthropic Claude API docs - prompting Fable:
   https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5
4. Anthropic Claude API docs - best practices:
   https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
5. OpenClaude GitHub:
   https://github.com/Gitlawb/openclaude
6. OpenClaude docs/site:
   https://openclaude.gitlawb.com/
7. Ollama Anthropic compatibility docs:
   https://docs.ollama.com/api/anthropic-compatibility
8. Ollama Claude Code compatibility blog:
   https://ollama.com/blog/claude
9. MLX-LM LoRA/QLoRA docs:
   https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/LORA.md
10. OpenMythos GitHub, theory only:
   https://github.com/kyegomez/OpenMythos
11. Hugging Face Fable traces dataset card, risk memo only:
   https://huggingface.co/datasets/Glint-Research/Fable-5-traces

Source receipts:
`~/grokgo/proposals/cheaper-fable-clean-room-source-receipts.jsonl`

### Do not import

- leaked proprietary prompt mirrors
- copied hidden prompt text
- raw Fable trace dumps
- personal contact lists
- browser account pages or API key pages
- raw chats, secrets, `.env`, private paths, or target lists

### NotebookLM questions to ask

1. "Summarize the clean-room architecture in one technical diagram narrative."
2. "Which components reduce cost without claiming frontier capability transfer?"
3. "Which sources are green, amber, and red for public discussion?"
4. "What is the strongest X thread that teaches the architecture without unsafe claims?"
5. "What should stay private or gated?"

## X-Post-Worthy Framing

Local anchor rules from `anchors.yaml`:
- lead with a concrete mechanism
- no hype-only claims
- no engagement bait
- specific architecture beats vague AGI language
- humor is allowed, but the mechanism must still teach

### One-post version A - clean technical

Everyone is trying to bring Fable back by copying a prompt.

Wrong target.

The useful part is the runtime: router, local models, curated memory, tool
sandbox, receipts, evals, spend ledger, brakes, and a human gate.

Small models do the cheap work. Frontier models only get the calls they earn.

### One-post version B - Jeff/Null voice

Fable disappearing taught the wrong lesson.

The move is not "paste the sacred prompt into a tiny model and pray."

The move is a router:
code first, local models second, cheap cloud third, frontier model only when the
task earns it.

Add brakes, ledger, receipts, memory, and a human gate.

### One-post version C - diagram caption

Clean-room Fable-like agent runtime:

Raw input -> brakes -> mining engine -> curated context -> router -> local lane
or frontier lane -> tool sandbox -> receipts -> researcher layer -> human gate.

No leaked prompts. No trace training. No secrets.

Token cost is a routing problem.

### Thread version

1/ Everyone is trying to bring Fable back by copying a prompt.

Wrong layer.

Prompt text can change surface behavior. It does not transfer frontier
capability into a small model.

2/ The useful lesson is architectural:

long-horizon agents need a runtime, not a magic incantation.

3/ Our clean-room version:

Raw input -> brakes -> Mining Engine -> curated context -> router -> local lane
or frontier lane -> tool sandbox -> receipts -> Researcher Layer -> human gate.

4/ Cheap by default:

T0: code, parsers, grep, tests
T1: local models through Ollama/MLX
T2: cheap cloud/free model lane
T3: frontier model only when earned

5/ The important part is the brakes:

killswitch, spend ledger, loop detection, lane parking, proposal receipts, and
human approval for live config changes.

6/ The trace datasets are not a free license to clone anything.

We treat them as a risk source, not training fuel.

No raw traces in NotebookLM. No CoT copying. No distillation pipeline.

7/ The experiment is small:

OpenClaude + Ollama/MLX on the Mini.
Three low-stakes tasks.
Measure tool reliability, bad edits, latency, local memory pressure, and cost.

8/ If the local lane wins, it becomes a router tier for drafts and grunt work.

Hard reasoning stays on the expensive model.

9/ The real trick:

you earn the expensive model by failing the cheap lane.

Schema validation on every output. Escalate exactly one tier.

10/ Token cost is not just a model problem.

It is a routing problem.

### Hooks for variants

- "You do not need a cheaper Fable. You need a cheaper path to the 5% of work
  that actually needs Fable."
- "Local models are not the brain. They are the nervous system for cheap reflexes."
- "The frontier call should feel like an exception handler, not the default path."
- "A prompt is not an operating system. A ledger, router, memory, and sandbox is."

## Visual Prompt

Use this for Grok Imagine or a designer:

"Create a clean scientific architecture diagram on a white background titled
'Clean-Room Fable-Like Agent Runtime'. Show a left-to-right pipeline:
Raw Input -> Brakes + Ledger -> Mining Engine -> Curated Context -> Router
Decision -> Local Model Lane (Ollama / MLX) plus Frontier Lane (earned calls
only) -> OpenClaude / Tool Sandbox -> Output Receipts -> Researcher Layer ->
Human Gate -> Memory / Proposal Queue. Add small safety labels: no leaked
prompts, no trace training, no secrets, human approval for live config. Use
dark gray, blue, teal, and amber. Minimal, technical, readable as an X image."

## Fable Handoff

Ask Fable to improve only the safe parts:

```text
Read ~/grokgo/proposals/cheaper-fable-clean-room-plan.md and the local source
pack. Improve the architecture and X framing without leaked prompts, raw traces,
hidden prompt text, MITM, auth bypass, or public sends. If you find a public
source worth adding, write a proposal receipt with URL, date, claim, and risk
class. Use rtk. No live config edits.
```

## Next Acceptance Checks

1. Fable or Codex reviews this plan and emits only proposal receipts.
2. NotebookLM source pack is created without red sources.
3. OpenClaude/Ollama/MLX preflight is run in sandbox only.
4. Three local tasks are measured.
5. X post and visual are reviewed by Jeff before posting.
