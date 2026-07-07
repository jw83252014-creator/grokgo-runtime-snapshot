# Reasoning-traces → local-model LoRA — plan (post-deadline)
## Data (use OURS, clean): 110 null session files + dream-reports (2.8M) + hermes sessions + grok sessions.
## AVOID: the sojalsec HF "Fable 5 reasoning traces" — scraped/leaked ("before they got restricted"), violates clean-room. Flagged to altair.
## Steps: 1) extract (prompt, reasoning, response) triples from our sessions → JSONL. 2) MLX LoRA fine-tune Hermes-3-8B on the mini. 3) eval vs base. 4) serve as the t1 local brain that reasons like our org.
## Also: HF search for ADDITIONAL clean/licensed reasoning datasets (open-licensed CoT sets) as supplements — not the leaked one.
