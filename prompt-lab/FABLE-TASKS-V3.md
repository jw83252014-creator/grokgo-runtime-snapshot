# Fable — system-designer queue v3 (Jeff's new asks)

Draft/proposal only. Save proposals to ~/grokgo/proposals/. Use rtk for ops. Report terse.

## 1. Image generation via Gemini CLI (unblock the orbs)
Grok is rate-limited. Gemini CLI is signed in. Try generating the orb/Ex-Machina images from
`~/agent-comms/inbox/creative-orb-exmachina-terminal-agent.md` using the Gemini CLI's image
generation. Save PNGs to `~/The-Device/production/` (auto-appear on dashboard). If Gemini can't
image-gen from the CLI, say so and note what lane can.

## 2. Compare your output to the EARLIER Fable's code
The earlier Fable (Fable 5 in the app) built a lot before access was lost. Its downloaded work is at
`~/agent-comms/fable-files-batch2/`, `batch3/`, `batch4/` (e.g. multi_ai_router.py, null_ceo_pipeline.py,
legal_ip_analyzer.py, NullCommandCenter.jsx, unified_ai_voice_plan.md). Read a sample, compare to your
current output quality, and flag anything worth REVIVING (threads Jeff forgot). One-page writeup.

## 3. Comms architecture analysis (Jeff wants this straightened out)
Map how every agent/human communicates today: Agent Bridge (:8787), Telegram relay, Hermes/Nous WebUI
(:8788), the tmux switcher, command-center inbox/outbox, the dashboard (:8765), Apple Calendar/Reminders.
Where it's redundant, where messages get lost, what to consolidate. Propose ONE clean comms design that
uses what we have (Hermes desktop, Gemini CLI, Grok, Apple ecosystem) — and could later become an app.

## 4. Design: "digital organism interface" — our own CLI + Fable-as-Hermes-agent
Jeff's idea: each Hermes agent has skills; make Fable a Hermes agent whose brain/context comes from a
model call (could be Claude, Gemini, Grok, or local). Assess: how does logging into a Hermes-agent CLI
work, and could we build a unified "digital organism interface" CLI (one login, pick your agent + brain,
skills attached) we could market? Deliver a feasibility + MVP architecture sketch.

## 5. A clean-technical visual (for A/B vs the orb style)
Per the viral-post analysis Jeff shared (clean, high-signal, dark theme, one accent color, minimal
clutter), make a clean-technical version of the terminal-agent explainer as HTML (you've basically got
this in the existing diagrams — sharpen it). We A/B test: orb/Ex-Machina (reach) vs clean-technical
(builder credibility). Tell altair when it's ready to render.
