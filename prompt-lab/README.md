# Grok Go Prompt Lab

This is the clean way to test stronger Claude Code behavior.

## Dumb Version

You put your prompt in:

`~/grokgo/prompt-lab/prompts/user-fable-style.md`

Then run:

```bash
rtk bash ~/grokgo/prompt-lab/RUN_PROMPT_TEST.sh
```

The script asks before calling Claude.

## What It Does

It uses Claude Code's normal documented prompt hook:

`--append-system-prompt-file`

That means:

- Claude keeps its normal coding instructions.
- Your extra rules get appended.
- No MITM.
- No hidden prompt extraction.
- No traffic stripping.
- Results get saved under `~/grokgo/prompt-lab/results/`.

## What You Can Test

- Your own Fable-style prompt.
- A public prompt you are allowed to use.
- A shorter directive template.
- A research-layer style.
- Before/after behavior against the same test input.

## What Not To Put Here

- Secrets.
- Cookies.
- OAuth tokens.
- Private chat dumps unless you want them sent to the model.
- Hidden provider system prompts.

