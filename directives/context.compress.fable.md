IN: verified file paths, terminal state, prior attempts, and the exact hard question.
JOB: compress this context for one Fable 5 turn. Keep only state Fable needs to make the decision.
OUT: {
  "why": "why this matters now",
  "verified_state": ["facts with paths or commands"],
  "hard_decision": "one decision for Fable",
  "constraints": ["budget, safety, approval, runtime limits"],
  "codex_after": ["tasks Codex/local lanes should do after Fable"],
  "drop": ["context intentionally omitted"]
}
STOP: if no hard decision exists, return {"hard_decision":"","codex_after":["handle without Fable"]}.
