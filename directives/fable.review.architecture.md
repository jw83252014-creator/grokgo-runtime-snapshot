IN: current architecture packet, verified files, and the single hard architecture decision.
JOB: decide the architecture question and produce downstream implementation tasks.
OUT: {
  "decision": "chosen architecture",
  "rationale": ["short practical reasons"],
  "interfaces": [{"name":"interface","contract":"summary"}],
  "codex_tasks": [{"file":"path","change":"task"}],
  "local_tasks": [{"type":"task","tier":"t0|t1|t2|t3"}],
  "stop_conditions": ["conditions"],
  "risks": ["risks"]
}
STOP: if the question is not a one-way-door decision, route it down to t3 or below.
