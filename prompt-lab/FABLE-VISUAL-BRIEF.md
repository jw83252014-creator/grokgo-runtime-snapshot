# Fable — design two matching visuals (you design them, altair ships them)

Goal: an X-worthy, beautiful pair that explains a terminal AI agent end-to-end. Jeff wants to post these.
You DESIGN + build them as self-contained HTML (altair renders to PNG + texts Jeff). Make a couple of
variants so he can choose.

## Deliverable A — "Anatomy of a Terminal Agent" (end-to-end, one frame)
A single visual that walks the whole loop, left→right or as a labeled diagram:
1. You type in the terminal
2. The agent assembles the request: system prompt + CLAUDE.md/project memory + tool defs + chat history + your message
3. Over HTTPS (encrypted) to the model API (auth token in header)
4. The model (weights = the brain) reasons + streams back text + tool calls
5. The agent runs tools locally (read/edit files, bash) and loops until done
- **Callouts at each section: "← you can tweak this here"** (e.g. system prompt via --append-system-prompt-file;
  tools via permissions/hooks; memory via CLAUDE.md; model via --model; context via compaction).
- Small **legend** baked into the frame (what the colors/icons mean).
- Make clear: the brain is the WEIGHTS; the prompt is just steering.

## Deliverable B — "Glossary" (same style, so they pair on a thread)
Same visual language as A. Define the terms a viewer needs, terminal-style:
weights, system prompt, context window, tokens, tool call, harness, MCP, hook, permission,
compaction, prompt caching, router/tier, agent loop. Keep each definition to one tight line.

## Style (match what we're already making)
- Dark "research-layer / control-room" aesthetic. Palette: teal = local/your machine, amber = the wire/model
  call, violet = the model engine, red/coral = risk or "don't touch." Mono labels. Readable at phone size.
- Same family as ~/agent-comms/app/public/claude-code-anatomy.html and before-after-hotrod.html, but richer.
- Cinematic but technical — the "quiet sacred sci-fi" mood of The Device film, not corporate SaaS.

## Build + handoff
- Write the HTML to ~/agent-comms/app/public/terminal-agent-anatomy.html and ...glossary.html
  (the bridge serves them; altair will screenshot to ~/The-Device/production/ and text Jeff).
- ALSO write 3–4 **Grok Imagine prompts** (artistic versions of A + B) to
  ~/agent-comms/inbox/creative-grok-imagine-terminal-agent.md for the creative team.
- Use rtk for any shell/file ops to save tokens (it's the global token-killer hook). Note any other
  token-saving ideas you spot.
- Tell altair when each file is ready so he renders + ships. Draft-only; nothing posts without Jeff.
