IN: routing.yaml, brakes.py behavior, dispatcher behavior, and any recent failure evidence.
JOB: produce a practical patch plan that reduces Fable usage without weakening hard-reasoning quality.
OUT: {
  "decision": "recommended routing policy",
  "route_changes": [{"task_type":"name","tier":"t0|t1|t2|t3|t4","reason":"short"}],
  "brake_changes": ["specific changes"],
  "ledger_changes": ["specific fields or queries"],
  "codex_tasks": [{"file":"path","change":"implementation-ready task"}],
  "stop_conditions": ["conditions"],
  "risks": ["risks or missing inputs"]
}
STOP: do not write code. If inputs are missing, name the missing path.
