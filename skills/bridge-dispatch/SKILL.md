---
name: bridge-dispatch
description: Standard Agent Bridge task dispatch workflow. Use when Codex needs to create or update a shared lane task board, post a gated task to exactly one Agent Bridge lane via /api/say, record a receipt path, or coordinate terminal/chrome-tab agents without public posts, account changes, spending, or irreversible actions.
---

# Bridge Dispatch

Use this skill to turn loose work into one clear lane task and one durable board row.

## Rules

- Dispatch exactly one owner/lane per task unless Jeff explicitly asks for a group broadcast.
- Keep gated work labeled: no public posts, no spend, no account/billing changes, no secrets.
- Prefer dry-run. Only post to `/api/say` when the user or supervising lane explicitly asked for dispatch.
- Never paste secrets, private data, raw X archive contents, or private reasoning traces into the room.
- Require a receipt path in every task, even if the first receipt is "pending".

## Standard Workflow

1. Read the source row or artifact.
2. Choose one owner using the existing owner vocabulary: `jeff`, `fable`, `keystone`, `grok`, `scout`, `vega`, `castor`, `nova`, `altair`, `librarian`, `frankenstein`, or `hermes`.
3. Update the shared board with status, owner, task, source, gate, and receipt.
4. Prepare a message in this shape:

   ```text
   [task] @owner <short action>. Source: <path>. Gate: <approval rule>. Receipt: <path-or-pending>.
   ```

5. Use `/api/say` only with an explicit dispatch decision.
6. After the owner reports, update the board row to `done`, `blocked`, or `waiting`, and add the receipt path.

## Script

Use `scripts/bridge_dispatch.py`.

Seed the board from the master backlog:

```bash
rtk python3 ~/grokgo/skills/bridge-dispatch/scripts/bridge_dispatch.py seed \
  --backlog ~/grokgo/proposals/master-backlog.md \
  --board ~/grokgo/TASK_BOARD.md
```

Add a local row without posting:

```bash
rtk python3 ~/grokgo/skills/bridge-dispatch/scripts/bridge_dispatch.py add \
  --board ~/grokgo/TASK_BOARD.md \
  --owner vega \
  --task "Create a visual draft for the Creator Engine post-picker bundle" \
  --source "~/mining-engine/creator_engine/runtime/post_picker/pending" \
  --gate "draft-only; Jeff approves before public post" \
  --receipt "pending"
```

Prepare or send a lane dispatch:

```bash
rtk python3 ~/grokgo/skills/bridge-dispatch/scripts/bridge_dispatch.py dispatch \
  --agent vega \
  --message "[task] @vega Create one visual draft. Source: ~/grokgo/TASK_BOARD.md. Gate: draft-only. Receipt: pending."
```

Add `--post` only when you intend to write to Agent Bridge:

```bash
rtk python3 ~/grokgo/skills/bridge-dispatch/scripts/bridge_dispatch.py dispatch \
  --agent vega \
  --message "[task] @vega ..." \
  --post
```

## Board

The default board is `~/grokgo/TASK_BOARD.md`. It is Markdown so terminal agents,
browser-tab lanes, and humans can read it without a special app.

Columns:

`id | status | owner | lane | source | task | gate | receipt | updated`

## References

Read `references/message-contract.md` when shaping new lane messages or receipts.
