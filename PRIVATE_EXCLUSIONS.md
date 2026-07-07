# Private Exclusions

This public snapshot was created from `/Users/rentamac/grokgo` but deliberately
does not include every file.

## Excluded

- `.claude/` and `.claude/backups/`
  - local Claude/account/session state and scheduled-task locks
- `logs/`
  - raw terminal and launchd output, including Fable terminal scrollback
- `ledger.db`, `ledger.db-shm`, `ledger.db-wal`
  - live SQLite runtime ledger files
- `spikes/`
  - large nested third-party repos, caches, experiments, and unrelated worktrees
- `agents/grok-tab/memory/`
  - private captured Grok tab memory
- `inbox/fable-preserve/`
  - raw preserved clipboard/terminal scrollback
- `_dedup-quarantine/`
  - raw dedup/input quarantine material
- `prompt-lab/CL4R1T4S/`
  - large third-party/reference prompt dump, not needed for Fable to understand
    Grok Go runtime behavior
- `prompt-lab/prompts/reference/`
  - reference prompts that should not be treated as public runtime code
- `prompt-lab/*dangerous*`
  - local reset/resume helpers that are not useful public documentation
- `proposals/accounts-registry.md`
  - account inventory
- `research/account-inventory.md`
  - account inventory
- `*.env`, `*.key`, `*secret*.txt`
  - secret-shaped local files

## Why

Fable needs the architecture, routing, task shape, directives, and evidence of
how the system runs. It does not need raw local credentials, account/session
state, caches, or unredacted logs.

The private `grokgo` repo remains available locally for full forensic work on
the Mac Mini. This public snapshot is the safe review surface.
