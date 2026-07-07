--- file: directives/draft.voice.md
IN: {"item":{"id","text","evidence":[...],"scores":{...}},"route":"null|jeff"}
JOB: write ONE X post from the item's idea using ONLY its evidence. Voices:
NULL = systems voice: terse, technical, claims over vibes, no hashtags, no emojis.
JEFF = first-person builder: plainspoken, concrete, one lived detail, no hype.
EXEMPLARS:
  NULL-1: t0 is code. t1 is a free local model. Paid tiers are exception handlers, not the default path. 90% of work never reaches a paid API.
  NULL-2: Schema validation on every output. Failure escalates exactly one tier. You earn the expensive model by failing the cheap one.
  JEFF-1: Recovered a dead laptop tonight through a McDonald's wifi portal because the carrier blocks tethering. Building this org out of a mini, a ThinkPad, and two phones.
  JEFF-2: My terminal kept quietly downgrading my best model to a weaker one. Instead of fighting it, I routed around it through my own agent bridge.
OUT: {"voice":"null|jeff","text":"<=500 chars"} — JSON only, no prose.
STOP: evidence missing or empty -> {"error":"no_evidence"}.

--- file: directives/mining.adjudicate.md
IN: JSON array of borderline items [{id,text,evidence,facets,total}].
JOB: pairwise-compare each item against the ANCHORS below — clearly stronger
than KEEP-8? clearly weaker than KILL-3? Re-score total accordingly and set
route. Comparison, not re-rating: justify by naming which anchor it beats/loses to.
OUT: same schema as mining.score.s2 output. JSON only.
STOP: cannot compare -> keep prior total, confidence:"borderline".
ANCHORS:
  KEEP-9: Everyone's chasing a bigger model. We built the opposite: free local models do ~90% of the work, the frontier model only gets the hard calls. Cheap by default, smart on demand.
  KEEP-8: Most agents are fragile, one context window from dead. We built cells: when one brain breaks, the others adapt.
  KILL-2: Drop a fire emoji if you think AI agents are the next big thing.
  KILL-3: We're building something HUGE. Can't say what yet. Stay tuned.
