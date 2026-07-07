# GitHub finds — NotebookLM MCP + harness tooling (Fable, 2026-06-16)

Scouted GitHub for (a) the NotebookLM CLI/MCP and (b) tooling for what we're building (self-rewriting
harness). Both came back rich. Plus the "better model for the rewrite" point — confirmed.

## NotebookLM — CLI + MCP (yes, it exists; we're half-set-up already)
We **already** have a partial setup: `~/.hermes-bookmark-research/mcp/NOTEBOOKLM_SETUP.md` targets
`PleasePrompto/notebooklm-mcp`, directory created, but **not cloned/installed/wired** (MCP servers in
`~/.claude/settings.json` = none). Options, best-first:
- **jacob-bd/notebooklm-mcp-cli** — CLI (`nlm`) + MCP server + agent skills in one install. Cleanest combo
  if we want a command-line `nlm` AND an MCP. → https://github.com/jacob-bd/notebooklm-mcp-cli
- **roomi-fields/notebooklm-mcp** — MCP + local HTTP REST API, audio/video/content generation,
  multi-account rotation; built for Claude Code/Codex/Cursor. Most capable. → https://github.com/roomi-fields/notebooklm-mcp
- **PleasePrompto/notebooklm-mcp** — what our setup doc already targets; citation-backed, persistent auth,
  for Claude Code/Codex. → https://github.com/PleasePrompto/notebooklm-mcp
**Payoff:** programmatic NotebookLM = the harness paper → narrated audio pipeline with no manual upload,
and agents can query our notebooks as a grounded knowledge base. All use *unofficial* Google APIs (can
break when Google changes endpoints) — keep it as a convenience lane, not load-bearing.

## Harness tooling — directly on-target for the self-rewriting harness
- **HarnessX** (the post Jeff saw) is a real paper: arXiv 2606.14249 — "A Composable, Adaptive, and
  Evolvable Agent Harness Foundry." Uses **AEGIS** (trace-driven multi-agent evolution), turns
  trajectories into both harness updates AND model-training signal. **+14.5% avg, up to +44%** across 5
  benchmarks. Code open-sourcing "in a future release" (not out yet) — so it's the blueprint, not a dep.
  → https://arxiv.org/abs/2606.14249
- **neosigmaai/auto-harness** — "bring your own agent, build a self-improving system: automatically mine
  failures, optimize the harness, gate against regressions." **This is exactly our trace-evolve loop** —
  study/borrow directly. → https://github.com/neosigmaai/auto-harness
- **revfactory/harness** — meta-skill that designs domain-specific agent teams + generates their skills.
  → maps to our **per-cell harnesses** idea. → https://github.com/revfactory/harness
- **HKUDS/OpenHarness** — open agent harness w/ built-in personal agent. → https://github.com/HKUDS/OpenHarness
- **Awesome lists** (curated tools/benchmarks/patterns): ai-boost/awesome-harness-engineering,
  Picrew/awesome-agent-harness, AutoJunjie/awesome-agent-harness.

**Takeaway:** our self-rewriting harness is the same idea as HarnessX/auto-harness — we're on the right
track and there's open code (auto-harness) to borrow the failure-mining + regression-gating from instead
of reinventing it.

## The "a better model rewrites the harness better" point — confirmed, and a design fix
Right now the adapt-pass (the step that writes the task-tuned soul) runs on the **weak local 4B**. But the
*meta* step — deciding how to tune the prompt — is the highest-leverage moment (HarnessX shows harness
evolution is where the gains are). So: **route the adapt-pass to a BETTER model (frontier or a stronger
local), keep the EXECUTION on the cheap local model.** Spend the smart model on the meta-decision, the
dumb model on the bulk. Concrete: add `BF_ADAPT_MODEL` to the self-rewriting harness so the rewrite uses
t3/t4 (or a bigger local) while the task itself stays t1. Cheap to try, likely a real quality jump.

## Next steps (dispatch)
1. Codex: wire a NotebookLM MCP (start with PleasePrompto since our doc targets it, or jacob-bd CLI) —
   gated install, then add to settings; test one query. → programmatic NotebookLM.
2. grok/scout: read the HarnessX paper + auto-harness repo; extract the failure-mining + regression-gating
   pattern into a note for our trace-evolve loop.
3. Fable/Codex: add `BF_ADAPT_MODEL` so the adapt-pass can run on a better model than the executor.
