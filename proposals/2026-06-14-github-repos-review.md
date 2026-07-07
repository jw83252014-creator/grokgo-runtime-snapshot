# Review: public GitHub repos (grok-go-organism + mining-engine)

**Status:** DRAFT review. Date: 2026-06-14. No changes made, nothing pushed.
**Repos (both PUBLIC):**
- `github.com/jw83252014-creator/grok-go-organism` ← `~/grok-go-organism-share` (458 files)
- `github.com/jw83252014-creator/mining-engine` ← `~/mining-engine` (397 files)

## 🔴 SENSITIVE — flag to altair, do NOT fix silently
**Personal email + internal infra leaked in `mining-engine`** via two committed raw chat
dumps:
- `research-sources/chat-exports/grok--bridge-ai-os-roadmap-2026-0519_0605.md`
- `research-sources/grok-chats/Telegram-AgentBridge-for-AI-OS (2).md`

These contain Jeff's two **personal Gmail addresses** (`nullaxiom0@gmail.com`,
`jw83252014@gmail.com`) repeated ~20+ times, plus detailed operational internals: which
account is logged into which AI lane, Hermes profile paths/launchd labels
(`~/.hermes-null`, `ai.hermes-null.gateway`), bridge methods, and the full account→agent
roster. That's a doxxing + recon surface, not research value. `grok-go-organism` is **clean**
of these emails (0 files).

**Recommended (Jeff's call — involves history rewrite + force-push, an account action):**
1. `git rm` both dump files (and ideally the whole `research-sources/chat-exports/` +
   `grok-chats/` raw-dump trees — keep the *distilled* `extracts/` which are the actual
   product).
2. Because they're already in history, scrub with `git filter-repo` (or BFG) and force-push,
   then rotate anything that *referenced* a credential. Treat the emails as already-public
   (assume scraped) — the value is stopping further indexing, not secrecy restoration.
3. Add the .gitignore rules below so raw exports can't be re-committed.

**Good news:** no live secrets found in tracked files of either repo. The
`TELEGRAM_*_TOKEN` hits are just env-var *names* in code (correct), the `xai-oauth`
mentions are descriptive, and the Polymarket wallet/`0x…` address is NOT in these repos
(it lives under `agent-comms`, unpublished).

## mining-engine — structural
- **No `.gitignore` at all.** For a repo whose entire job is ingesting chat exports,
  research, and `mining-runs/`, this is the root cause of the leak above — nothing stops a
  raw dump or a stray `.env` from being committed. **Add one first** (highest-leverage fix):
  ```
  .DS_Store
  __pycache__/  *.pyc  .venv/  venv/  node_modules/
  .env  *.env
  research-sources/chat-exports/   # raw dumps — commit only distilled extracts/
  research-sources/grok-chats/
  mining-runs/*.log
  ```
- README is strong and clear on purpose. `CONTRIBUTING.md` exists. `mine.py` at root is a
  reasonable entry point.
- Suggest a one-line README note: "raw conversation exports are NOT committed; only distilled
  `extracts/` are public" — makes the boundary explicit for future contributors/agents.

## grok-go-organism — structural
- Solid: has `LICENSE`, a 9.4K README (clear biological framing + repo layout + public
  links), and a real `.gitignore` that already excludes `.env`, logs, pids,
  `next-autonomous-prompt.txt`, watcher state. This is the better-hygiene repo.
- 458 tracked files is heavy for a "harness" repo — it's carrying `terrarium-web/`,
  `research-paper/`, `dashboard/`, `agent-comms/`, etc. Consider whether everything needs to
  be in the *public* mirror, or whether the public repo should be a curated subset (the
  watcher + directives + paper) rather than a near-full working-tree copy. Smaller public
  surface = less to audit and less accidental leakage.
- `.gitignore` ignores `gist/` but the dir is present — confirm nothing sensitive staged there.

## Priority order
1. 🔴 mining-engine: add `.gitignore`, then remove + history-scrub the two raw chat dumps
   (Jeff-gated: force-push is an account action). — *altair*
2. mining-engine: README note on the raw-vs-distilled boundary.
3. organism: decide on curated-subset vs full-mirror to shrink the public surface.
4. organism: verify `gist/` has nothing sensitive.

All of the above is draft/recommendation only — no edits, no `git rm`, no push performed.
