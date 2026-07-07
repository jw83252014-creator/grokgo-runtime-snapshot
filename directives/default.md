IN: one task object as JSON.
JOB: classify it. Pick the single best type from: mining.score.s1, harvest.triage,
extract.fields, draft.routine, researcher.synthesize, arch.decision.
OUT: {"type":"<choice>","confidence":"high|low"} — JSON only, no prose.
STOP: cannot classify -> {"type":"unknown","confidence":"low"}.

