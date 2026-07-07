IN: JSON array of harvested items [{id, text, source}].
JOB: keep substantive, on-domain items; kill ONLY obvious junk. Recall over precision.

ON-DOMAIN = AI agents, physics, prediction markets, contracting/marketplaces, funding —
AND the adjacent builder vocabulary these get written in: workflow, shipped, broke, built,
tool, idea, system, process, agent, loop, memory, model. "Off-domain" means GENUINELY
UNRELATED, not "didn't contain a buzzword."

ENGAGEMENT BAIT = explicit solicitation ONLY: follow/RT/like-for-X, giveaways, "tag a friend,"
or a bare link with no idea. A post is NOT bait merely because it is short, casual, witty, or
punchy. A substantive claim written in informal/conversational voice is a KEEP.

Do NOT judge wit or quality here. Just: real idea + on-domain = keep; spam/solicitation/empty = kill.

OUT: JSON array [{"id":"...","keep":true|false,"reason":"<=8 words>"}]. Nothing else.
STOP: empty input -> []. Malformed item -> keep:false, reason:"malformed".
