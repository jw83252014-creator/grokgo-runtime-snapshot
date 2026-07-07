IN: Mining Engine state, keep/kill anchors, scoring failures, and target use case.
JOB: improve Jeff Filter signal scoring with a practical precision/recall policy.
OUT: {
  "decision": "precision or recall bias by stage",
  "stages": [{"stage":"S0-S4","goal":"goal","tier":"t0|t1|t2|t3|t4"}],
  "rubric_changes": ["changes"],
  "anchor_needs": ["needed examples"],
  "codex_tasks": [{"file":"path","change":"task"}],
  "stop_conditions": ["conditions"]
}
STOP: if anchors are missing, request exact KEEP/KILL examples and do not invent them.
