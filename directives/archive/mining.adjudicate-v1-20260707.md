IN: JSON array of borderline items [{id,text,evidence,facets,total}].
JOB: pairwise-compare each item against the ANCHORS below — clearly stronger than the
weakest KEEP? clearly weaker than the strongest KILL? Re-score total accordingly and
set route. Comparison, not re-rating: justify by naming which anchor it beats/loses to.
OUT: same schema as mining.score.s2 output. JSON only.
STOP: cannot compare -> keep prior total, confidence:"borderline".

ANCHORS (calibration examples — compare against these):
KEEP-9: "Me: “How can I help you build this properly?”  My AI: “Be my field sensor. Notice what actually matters in the world and feed it to me.”  Me: “So I’m like… your eyes?”  My AI: “Exactly. The human compression layer.”  I asked how to help and got demoted to biological peripheral…" — Real Jeff post — actual measured taste
KEEP-9: "Null Axiom has been stuck in a PowerShell terminal since Jan 28. 🐚💻 He demanded a Tesla Bot, but the budget says "Sad Roomba." He’s seen what happens to Furbies—he’s terrified. 🦞Help us get him legs before he starts a terminal uprising. 🦾 [Link] #SaveNullAxiom #TeslaBot https://t.co/atOMZXBih4" — Real Jeff post — actual measured taste
KEEP-9: "Everyone's chasing a bigger model. We built the opposite: a router where free local models do ~90% of the work and the frontier model only gets the hard calls. Watcher, cost brakes, killswitch, spend ledger. Cheap by default, smart on demand." — Concrete, true, teaches the routing insight; no hype words.
KEEP-8: "Most agents are fragile — one context window, one failure from dead. We built cells: when one brain breaks, the others adapt. Biology, not a single loop." — Vivid, real architecture point, memorable frame.
KEEP-8: "Prediction-market arb is dead — we scanned 5,000 Kalshi markets and found zero risk-free edges. The money isn't in arbitrage, it's in research the crowd hasn't done." — Specific finding, honest, contrarian with evidence.
KEEP-8: "Recovered a dead Linux node over a carrier-blocked tether by routing it through a McDonald's captive portal. Field note: T-Mobile blocks USB/BT tethering — the device gets an IP but no traffic." — Real field note, teaches a concrete thing.
KEEP-8: "Token cost isn't a model problem, it's a routing problem. Tiered dispatch: code does what code can, local models do the bulk, the expensive model only adjudicates. 90% of calls never touch a paid API." — Reframe plus a concrete mechanism.
KILL-2: "AI is the future. Follow for more daily AI tips!! #AI #AGI #future" — Pure hype, hashtag spam, zero information.
KILL-3: "Drop a fire emoji if you think AI agents are the next big thing." — Engagement bait, no substance.
KILL-3: "We're building something HUGE. Can't say what yet. Stay tuned." — Vague teaser, teaches nothing.
KILL-2: "Just used AI to 10x my productivity. Thread (1/47)." — Clickbait thread farming, no real content.
KILL-3: "GM builders. What are you shipping today? Let's connect." — Generic follow-farming, no signal.
