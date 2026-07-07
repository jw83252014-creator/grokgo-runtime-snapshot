# Null Axiom — Company Operating Plan (Fable, 2026-06-15)

The thing you asked for: one place to run this like a company. Master project list with status,
blockers, and the path to done; a weekly operating cadence; and an org chart that maps real roles to
the agents we already have (and the few we should add). Living doc — update the status column as we go.

CEO: Jeff. Everything that posts, spends, sends, or changes an account stays gated to Jeff.

---

## 1. Master project list

| # | Project | What "done" looks like | Status | Blocker | Next action (owner) |
|---|---------|------------------------|--------|---------|---------------------|
| 1 | **BidLocal** | First pilot: 3–5 contractors, 10 leads, 1 documented job | Site + packet live; pre-pilot | Need real contractors + outreach approval | Recruit 3–5 from Jeff's network (Jeff + scout) |
| 2 | **Creator Engine** | Flagship thread out + small paid cohort | Spec written | X-algorithm/niche research pass missing | Run research pass (Mining Engine + grok) |
| 3 | **Badass Fable (harness)** | One paid "harness install + cost audit" | Paper + site page done | No client yet; local model lane half-built | Finish local lane; line up 1 pilot client (Jeff) |
| 4 | **Mining Engine** | Runs scheduled, feeds all lanes | Built; on website; manual | No 24/7 local model | Wire scheduled passes; finish local lane (me) |
| 5 | **The Device** | Audience surface; build-in-public film | Site page + visuals | Downstream of Creator Engine | Keep shipping visuals (vega/creative) |
| 6 | **Website (Null Axiom)** | Investor-ready, all projects legible | Live locally; harness + mining added | Deploy + paths-to-money section | Add revenue section; deploy on Jeff OK |
| 7 | **Trading agent** | Capped, killswitch-gated research | Design in goldmine chat | High risk; needs hard brakes + tiny bankroll | Mine design only; do NOT go live (Jeff) |
| 8 | **Funding / grants** | Warm intros to grant-makers/researchers | Outreach cell drafts | Every send gated | Draft researched intros; Jeff approves |
| 9 | **Self-improve loop** | Scheduled reflection → skills/learnings | Built (drafts), not enabled | Awaiting Jeff enable | Enable launchd on Jeff OK |

Priority order (my call): **1, 2, 3** are the near-term money; **4, 6** are the multipliers that make
the rest faster; **5, 8** are slow-burn; **7** is capped research; **9** is a free force-multiplier the
moment you green-light it.

## 2. Operating cadence (how we run it weekly)
- **Monday — plan:** review this list; pick the 3 things that move money this week; update statuses.
- **Daily — ship + filter:** each lane does its work; Mining Engine + Jeff Filter turn the day's signal
  into drafts; receipts logged.
- **Gate:** anything that posts/spends/sends queues as a draft for Jeff. Nothing crosses that line alone.
- **Friday — reflect:** the self-improve pass distills what worked into reusable skills; update the
  money board.
- **One money board:** `proposals/money-board.md` (Opportunity Cards) is the shared queue every revenue
  lane reads before starting — so we stop re-deriving the same ideas.

## 3. Org design — roles, and which agents fill them

We already have a deep bench (see `agent-comms/ROSTER.md`). Most "company roles" are already staffed;
the gaps are a few ownership seats, not new bodies.

| Company role | Filled by | Gap? |
|---|---|---|
| CEO / final approval | **Jeff** | — |
| System architect / harness | **Fable (me)** | — |
| Build + coordination | **keystone** (Codex), **null** (coordinator) | — |
| Creative director / visuals | **vega** (Fable 5) | — |
| Head of Security / Red Team | **altair** | — |
| Research (web/X) | **grok**, **castor/nova** (Gemini), **scout** | — |
| Infra / triage | **atlas** | — |
| X research (read-only) | **librarian** | — |
| Public X persona | **doombot47** (proposed) | not yet active |
| **Head of Growth / Creator Lead** | — | **GAP — own the Creator Engine + course** |
| **Revenue / Money owner (CFO-lite)** | — | **GAP — own the money board + Opportunity Cards** |
| **Product owner — BidLocal** | loosely Jeff | **GAP — one owner driving the pilot** |

## 4. Should we make new agents (Hermes or Badass Fable) for the gaps?

**My recommendation: don't spin up new agents for everything — assign the gap roles to existing agents
first, and only instantiate a dedicated agent where the role is continuous and well-scoped.**

- A "role" is just a **soul file (job description) + the right brain + bridge address.** That's cheap.
- **Worth making as a dedicated agent now:** *Head of Growth / Creator Lead* — it's continuous, it has a
  clear loop (watch→filter→draft→gate), and it benefits from its own memory. Make it a **Hermes agent**
  (always-on, off-browser) so it can run the content engine on a schedule. Soul = the job description.
- **Worth defining as a soul but running on an existing agent:** *Revenue/Money owner* — give the role
  to **null** (coordinator) with a money-owner soul appended, rather than a new body; it's oversight,
  not a 24/7 loop.
- **Badass Fable agents vs Hermes agents:** same idea, different lane. Use a **Hermes agent** when you
  want it always-on and addressable on the bridge (Creator Lead). Use a **Badass-Fable-style local
  agent** when the work is cheap/local and you want it behind the router (drafting, summarizing) — once
  the local model lane is finished. For now, Hermes for the always-on roles; local agents come online
  when the MLX/Ollama lane is solid.

I've drafted two soul files as starting points (job descriptions): `proposals/souls/creator-lead.md`
and `proposals/souls/revenue-owner.md`. Review them; on your OK they get wired to a brain + bridge
address.

## 5. What I need from you (CEO decisions)
1. Green-light the **Creator Engine research pass** (unblocks #2).
2. Pick the **BidLocal pilot owner** (you, or assign scout to drive recruiting).
3. Say the word to **enable the self-improve loop** (#9) — free multiplier.
4. Approve deploying the **website** with the new sections.
5. OK to wire the **Creator Lead** as a Hermes agent from the drafted soul.
