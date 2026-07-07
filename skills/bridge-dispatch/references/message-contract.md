# Bridge Dispatch Message Contract

## Task Message

```text
[task] @owner <single action>. Source: <path>. Gate: <approval rule>. Receipt: <path-or-pending>.
```

## Receipt Message

```text
[receipts] @requester done|blocked: <artifact/commit/path>. Gate status: <unchanged or approval needed>.
```

## Gates

Use exact phrases:

- `draft-only`
- `Jeff approves before public post`
- `Jeff approves before spend`
- `no account/billing changes`
- `no secrets in room`
- `read-only`

## Owner Hints

- `keystone`: code, repo edits, local automation, RTK-backed execution.
- `fable`: architecture, synthesis, reasoning, proposal design.
- `grok` or `scout`: X/web research and browser-visible facts.
- `vega`: visuals, diagrams, creative review.
- `librarian`: read-only archive/data refreshes.
- `altair`: security review and public-release checks.
- `frankenstein`: phone/Termux/ThinkPad/mobile relay checks.
