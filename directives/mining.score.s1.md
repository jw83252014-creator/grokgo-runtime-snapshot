IN: JSON array of items [{id, text, embed_prior}] (embed_prior = cosine vs exemplar corpus, 0-1).
JOB: kill obvious junk only. Keep anything plausibly substantive, novel, on-domain.
Loose on purpose: recall over precision at this stage. Treat embed_prior ≥ 0.55 as a
strong keep signal, ≤ 0.25 as a strong kill signal.
OUT: JSON array [{"id":"...","keep":true|false,"reason":"<≤10 words>"}]. Nothing else.
STOP: empty input -> []. Malformed item -> keep:false, reason:"malformed".

