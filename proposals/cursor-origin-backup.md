# Cursor Origin as a backup target for Jeff's repos — evaluation

**Date:** 2026-06-18
**Question:** Cursor launched a GitHub-like service called "Origin." What is it, how do you sign up, what's the pricing/security, and should we use it to back up ALL of Jeff's repos/data alongside GitHub?
**Short answer:** Not yet, and not as a backup tool. Origin is a competing **git forge** (a GitHub replacement), not a backup product, and as of June 2026 it's waitlist-only with **no public pricing, no published privacy/security terms, and no general availability**. For "back up everything alongside GitHub," a second private mirror (GitHub private repos + a cheap off-platform mirror) is the right move today.

---

## What Origin actually is

Cursor announced **Origin** on **June 16, 2026** at its inaugural "Compile" conference in San Francisco. Cursor's own tagline: *"A git forge for the agentic era... Code is moving faster than any infrastructure was built to handle."*

It is a **code storage + git hosting + collaboration platform** — i.e., a direct **GitHub/GitLab alternative (a "git forge")**, not a backup service and not just a sync tool. The differentiator is that it's designed assuming **AI agents, not humans, do most of the committing**:

- **Git-compatible** — works with standard git tooling, so existing clones/pushes work.
- **API + MCP extensibility** — agents can drive it programmatically; Cursor has committed to API and MCP support for CI/CD integration.
- **AI-powered automatic merge-conflict resolution** — built for many agents pushing parallel branches.
- **Stacked pull requests** — inherited from Cursor's **December 2025 acquisition of Graphite** (the code-review startup), whose re-architected tech Origin is built on.
- **Hybrid NVMe + S3 storage** with "infinite replicas."
- **Performance claims** from the launch demo: ~**22.6 commits/second** in a single repo, ~**296,000 clones/hour**, and **sub-400ms global sync latency**. (These are vendor demo numbers, unverified.)

Design framing from Cursor: traditional git was built on the premise that *"humans make decisions"*; Origin is built on the premise that *"agents work in parallel."*

**Key categorization for our purposes:** Origin is positioned as a **replacement/competitor** to GitHub, with migration tooling to *switch*, not parallel-run. It is **not** marketed as a backup/archival product, and self-hosting is not offered (hosted SaaS only).

### Strategic context (relevant to trust)
Coverage ties the launch to Cursor's reported acquisition by **SpaceX (via xAI)** in a ~$60B all-stock deal, with Cursor training a new ~1.5T-parameter model on xAI's Colossus supercomputer. This matters for a backup decision: putting *all* of Jeff's code into a brand-new forge owned by an AI lab that trains frontier models is exactly the scenario where data-handling terms need to be airtight — and those terms **are not published yet**.

---

## How to sign up

- **Waitlist only.** Go to **https://cursor.com/origin** and "Join the waitlist." Cursor's page: *"We'll reach out when Origin is ready for you."*
- **No self-serve signup, no general availability.** Target launch is **"this fall" (fall 2026)**.
- No stated requirements beyond a Cursor account / waitlist email. (Pricing tier, org requirements, and whether it's gated to paid Cursor plans are all **unannounced**.)

---

## Pricing

**Not disclosed.** No public pricing of any kind has been announced for Origin as of June 2026. You cannot price or budget this yet.

---

## Privacy & security — the critical gap

**For Origin specifically: nothing published.** No pricing terms, no data-handling/privacy policy, no security certifications, no statement on whether hosted code is used for training, and no self-hosting option have been released for Origin. Multiple independent write-ups flag the **training-data / data-privacy question as explicitly open and unresolved**.

**What we can infer from Cursor's existing posture** (the *editor*, not Origin — do not assume it transfers):
- Cursor the IDE is **SOC 2 Type II** certified, runs **Privacy Mode** (on by default for Enterprise, can be enforced org-wide), and claims **Zero Data Retention (ZDR)** agreements with model providers (OpenAI, Anthropic, Google Vertex, xAI Grok), plus encryption at rest/in transit and optional CMEK on Enterprise.
- **Caveat:** Origin is a different product on different infrastructure. None of the above has been confirmed to apply to repositories stored in Origin. Treat Origin's security as **unknown** until Cursor ships terms at trust.cursor.com.

**Bottom line on privacy:** It is premature to entrust *all* of Jeff's source and data — much of which is sensitive (agent fleet config, business plans, Stripe drafts, OSINT) — to a forge with no published data-handling guarantees, owned by an AI lab. That's a hard blocker for "back up everything."

---

## Origin vs. just using private GitHub repos

| Dimension | Cursor Origin (today) | Private GitHub repos |
|---|---|---|
| **Availability** | Waitlist only; fall 2026 | Available now |
| **Pricing** | Unknown | Free for unlimited private repos (Free tier); paid plans known |
| **Security/privacy terms** | None published | Published; SOC 2, mature, GitHub Advanced Security available |
| **Maturity** | Brand-new, unproven | 17+ years, battle-tested |
| **Backup-as-a-feature** | Not a backup product | Not a backup product either — but it *is* a stable remote |
| **Agent throughput** | Purpose-built, very high (claimed) | Adequate for normal use; rate limits at extreme agent volume |
| **Vendor risk** | New entity under SpaceX/xAI; terms unknown | Microsoft-owned, stable, known terms |
| **Ecosystem (CI/CD, Actions, integrations)** | Minimal at launch; API/MCP promised | Huge mature ecosystem |
| **Lock-in / portability** | Git-compatible (portable) | Git-compatible (portable) |

**Important framing:** Neither GitHub nor Origin is *itself* a backup. A single remote is **not a backup** — if the account is suspended, the repo is DMCA'd, or the provider has an outage, you lose access. Real backup = **the same history in two independent locations**. So the right question isn't "Origin vs GitHub for backup," it's "what second, independent copy do we keep alongside GitHub?"

---

## Recommendation

**Do not adopt Cursor Origin for backing up Jeff's repos/data right now.** Reasons:
1. It's **waitlist-only / not GA** — you can't actually use it for production backup yet.
2. **No published pricing or privacy/security terms** — entrusting *all* repos (including sensitive business/agent data) to an AI-lab-owned forge with unknown data handling is an unacceptable risk for a backup-everything mandate.
3. It's a **forge replacement, not a backup tool** — adopting it means *migrating*, not *adding redundancy*. Using it as a redundant mirror would just be a worse, less-proven copy of what GitHub already does.

**What to do instead for "back up everything alongside GitHub" — today:**
1. **Keep GitHub private repos as primary** (already free for unlimited private repos).
2. **Add a true second copy** that's independent of GitHub. Cheapest robust options:
   - **`git clone --mirror`** of every repo to a local/NAS disk on a cron (full history incl. all refs), plus an encrypted off-site copy (e.g. rclone to B2/S3). This is provider-agnostic and the real "backup."
   - Optionally a **second hosted mirror** (GitLab/Codeberg/self-hosted Gitea) via push mirroring if you want a live off-GitHub remote.
3. **For non-git data** (the proposals, JSONL receipts, souls, assets in this tree): include them in the same encrypted off-site backup; git remotes only protect committed code.

**Revisit Origin when:** it reaches GA **and** publishes (a) pricing, (b) a data-handling/privacy policy that explicitly states code is not used for training, and (c) SOC 2 / trust-center coverage *for Origin specifically*. At that point it could be worth piloting on a **non-sensitive throwaway repo** to evaluate its agent-throughput benefits — but as an experiment, not as the backup of record.

---

## Sources

- Cursor official Origin landing page — https://cursor.com/origin
- eesel AI, "What is Cursor Origin?" — https://www.eesel.ai/blog/what-is-cursor-origin
- explainx.ai, "Cursor Origin: agent-first git hosting and GitHub alternative (2026)" — https://explainx.ai/blog/cursor-origin-git-hosting-github-alternative-ai-agents-2026
- BigGo Finance, "Cursor Unveils Origin Code Hosting Platform" — https://finance.biggo.com/news/979fe270-a07e-4684-b99e-f1af5d31317e
- TimesOfAI, "How Cursor's Origin Challenges GitHub's Decade-Old Model" — https://www.timesofai.com/news/cursor-origin-vs-github/
- EveryDev.ai, "Cursor Origin — Git forge for AI agents" — https://www.everydev.ai/tools/cursor-origin
- Cursor Privacy & Data docs — https://cursor.com/help/security-and-privacy/privacy
- Cursor Security — https://cursor.com/security
- Cursor Enterprise privacy & data governance — https://cursor.com/docs/enterprise/privacy-and-data-governance
