# X Intelligence + Second Brain GitHub Knowledge Base Plan

## Purpose

Create a Git-safe knowledge base that agents can use without re-scanning all of Jeff's history. Private/raw material remains in `agent-comms`; sanitized summaries and reusable structures live in the Grok Go repo.

## Proposed Root

`/Users/rentamac/grokgo/knowledge-base/x-intelligence/`

## Structure

```text
knowledge-base/x-intelligence/
  README.md
  topics/
    README.md
  people/
    README.md
  sources/
    README.md
  drafts/
    README.md
  verdicts/
    README.md
  science/
    README.md
```

## What Goes Where

| Folder | Contents | Public/Git Rule |
| --- | --- | --- |
| `topics/` | Topic maps, convergence clusters, project links | Git-safe summaries only |
| `people/` | Key account/researcher cards and public relationship notes | No private DMs/contact details |
| `sources/` | Source summaries with URLs/dates/hashes | Summaries, not copied full articles |
| `drafts/` | Candidate post/comment drafts | Draft-only, no auto-post |
| `verdicts/` | Jeff approve/edit/kill notes and performance summaries | Avoid sensitive personal data |
| `science/` | Michael Levin and related science explainers | Cite sources, mark uncertainty |

## Promotion Path

```text
raw X/Grok/Telegram/chat data
  -> agent-comms private notes/receipts
  -> sanitized summary
  -> grokgo knowledge-base
  -> optional GitHub push after Jeff approval
```

## Agent Use

- Jade reads the knowledge base for cheap scoring and first-pass drafts.
- Fable reads only bounded packets that cite knowledge-base files.
- Keystone updates files and receipts.
- Jeff approves public posting and GitHub pushes.

## Initial Rules

1. No raw DMs, secrets, private filesystem paths, or private contact details.
2. No public claims without source links or receipts.
3. Do not copy whole articles, threads, or transcripts into Git.
4. Store source URLs and short summaries.
5. Keep "Jeff voice" examples only from approved public posts or explicit private anchors.

