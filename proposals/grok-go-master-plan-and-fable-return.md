# Grok Go — master plan + Fable-return brief (Jeff vision, 2026-06-18)

Capture of Jeff's big-picture plan. Not all started — this is the north star + the brief for when the
real frontier Fable comes back from Anthropic. Pairs with [[scaling-fable-on-api-future]].

## 1. Agent-creator YouTube channel ("what we're working on")
Each agent is its own **creator with an avatar**, making + uploading its own videos to one channel that
shows what Grok Go is building. Each agent gets a section: what it is, the parts of the system it owns,
lessons learned, cool wins. **Ad-free, info-first.** One channel, many agent voices.
- Pipeline already exists: brief → Grok Imagine / Gemini render → movie-stitch → dashboard/Telegram
  (see grok-imagine-video skill). Add: per-agent avatar identity + a YouTube upload lane (gated until Jeff ok).
- Tie-in: the harness explainer (Ex Machina + clean styles) is the first one; OpenGoldSDR gold-hunt
  videos are natural content; XPRIZE trailer is the flagship.

## 2. An agent per project + monetization
Every project gets an owning agent with: a monetization goal, an outreach plan, and a growth plan
**across all platforms**. Projects in flight: Grok Go organism, OpenGoldSDR, Somaco/UUIDv8, BidLocal,
Champion Fencing, the creator course. Each agent = product owner + marketer + builder.

## 3. Donations to feed Grok Go until self-sustaining
Take **donations to keep the organism running** (compute/API) until revenue sustains it. Be transparent:
a public "feed the organism" page (the dashboard already shows vitality). Pair with concrete
"**jobs agents can do for money**" — research-for-hire, content production, lead-gen/outreach drafting,
data/OSINT packets, BidLocal pilots, the creator course, the OpenGoldSDR "sell-the-plan + parts list."
Open question to work: which agent jobs are actually billable now vs. later (build the money-board).

## 4. Mining Engine as a Fable tool
The mining engine is **deep — it can mine our data many ways**. Make it a tool Fable (or this lane) can
invoke and run in **multiple passes** over ALL our data (chats, repos, telegram, imessage, research).
- Action: wrap mining-engine entrypoints as a callable tool (input = pass-type + corpus; output =
  structured findings/skills). Then Fable runs passes: extract → dedup → "Jeff Filter" → skills/advice.
- This lane CAN drive it now for a first pass if Jeff wants — doesn't need to wait for frontier Fable.

## 5. Prompts for Fable's return (go over ALL our data → advice)
When the real Fable is back, hand it the mining engine + the full corpus and these standing prompts:
- "Read all of it. Where is the organism wasting motion? What's the highest-leverage next move?"
  (**Game of Life advice** — simple local rules that move Jeff forward.)
- "What did we learn that we haven't turned into a skill or a product yet?"
- "What's the cheapest experiment that most advances each project?"
- "What are we wrong about?"
Output = ranked, concrete, do-X-unlocks-Y advice in Jeff's TLDR style.

## 6. Always-on organism
The whole organism updates **all day, every day** — research loop + auto-backup (~30 min) + cells
working continuously. End state ties to [[scaling-fable-on-api-future]]: frontier brain on API + cheap
parallel lanes (GLM-5/served model) so reasoning runs 24/7, not off interactive chat sessions.

## Backup reality (so this plan survives)
`~/grokgo` auto-backs-up to GitHub ~every 30 min (`com.jeff.grokgo-autobackup`). OTHER repos
(OpenGoldSDR, the-device-site, agent-bridge) are separate — keep them committed/pushed per-change.
TODO: add the sibling repos to the auto-backup job so nothing is stranded.
