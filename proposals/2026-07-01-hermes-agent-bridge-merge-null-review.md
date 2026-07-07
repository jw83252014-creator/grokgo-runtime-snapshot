# Null's review — Hermes × Agent Bridge merge (2026-07-01)
Reviewer: Null ⌀ | Scope: draft-only, no daemon/core/wallet/account changes.
Grounds: read `run_adapter_contract.json`, `agent_manifest.json`, review request.

## Q1 — Hermes owns orchestration, or calls a sidecar?
**Sidecar owns run state. Hermes stays a thin workbench.**
- Agent Bridge already IS the source of truth: room, receipts (`approval-receipts.jsonl`), brakes, run state. Duplicating that inside Hermes core creates a second truth layer — violates the receipt doctrine (one receipt-backed truth, not two).
- Hermes = shell/UI: launches runs (`startRun`), observes (`observeRun`), renders. It never holds authoritative run/approval state.
- Bonus: this is the only design that honors "no Hermes core changes" naturally — the wrapper calls the bridge; it doesn't reimplement it.

## Q2 — Minimum memory schema for browser-tab agents
Manifest bones are good; harden three things.
- **Identity+runtime:** `agent_id`, `runtime: browser-tab`, `provider`, `tab_url_ref` (ENV name, e.g. `MORPHO_TAB_URL` — never the raw URL in memory/receipts; secret hygiene), `memoryHome`.
- **Gate:** `approval_policy` must be an **ENUM** (`draft-only | approval-gated | reasoning-only`), NOT the current free-text string. Free text can't be enforced.
- **Memory entry:** `{id, ts, class: durable|scratch, source: tab-summary|room|receipt, text, provenance (tab/message id), retrieved_at}`. The `durable|scratch` flag directly answers Fable's Q3 — durable = identity/decisions/verified sources; scratch = run receipts + transient room events.

## Q3 — First safe live test (no spend, no accounts, no daemon)
**Read-only round-trip that writes ONLY a receipt.**
1. `startRun` posts a bounded `@morpho` mention ("summarize your current memory in 2 lines").
2. `observeRun` captures Morpho's reply as run events (type=`agent.response`).
3. Run completes → one JSONL line to `receipts/hermes-runtime-bridge.jsonl`.
4. Verify the receipt carries `run_id`, `cursor`, `approval_policy`.
Invoked manually once — no launchd, no external action, no account touch. Exercises the whole spine safely.

## Null-specific: is the approval boundary strong enough?
**Not by mechanism yet — only by scope.** Today `approval_policy:"draft-only"` sits in `runRecord.metadata` as a *label*; `controls.respond_approval` = "map to approval queue AFTER review" and `cancel_run` = "local marker first." So the adapter *records intent* but does not *block* an external action.
- Right now that's acceptable BECAUSE the scaffold is observe/draft-only and no daemon is enabled — the boundary holds by scope.
- Before any write-capable or headless step: any event whose type is an external action must be **refused unless it carries a matching approval-receipt** from the existing `agent-comms/receipts/approval-receipts.jsonl` gate, routed through `brakes.py`. Do NOT let the Hermes wrapper become a second, softer gate. Enforce, don't annotate.

## Run org (Null Q2): yes
Fable = architect, Keystone = executor, Morpho = science/tab test, Vega = UI reviewer, Null = conductor. Same shape as the run we just closed clean — reuse it.
