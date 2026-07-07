#!/usr/bin/env python3
"""load_anchors.py — inject Jeff's real KEEP/KILL anchors + voice exemplars.

One input file, three outputs, idempotent (safe to re-run after edits):
  - regenerates directives/mining.score.s2.md   (rubric + ANCHORS)
  - regenerates directives/mining.adjudicate.md (pairwise + ANCHORS)
  - regenerates directives/draft.voice.md       (voice cards + exemplars)
  - rewrites exemplars.jsonl from the KEEPs (embeds via Ollama if reachable;
    otherwise vec=null — run `mining_pipeline.py reembed` on the Mini)

Usage:  python3 load_anchors.py anchors.yaml
See anchors.example.yaml for the input format. NOTE: keep the "null" voice key
quoted in YAML — unquoted null parses as a None key (handled here, but ugly).
"""
import json
import os
import pathlib
import sys

import yaml

import mining_pipeline as mp

ROOT = pathlib.Path(os.environ.get("GROKGO_ROOT", str(pathlib.Path.home() / "grokgo")))
DIRECTIVES = ROOT / "directives"


def _anchor_block(keeps, kills):
    lines = ["ANCHORS (calibration examples — compare against these):"]
    for i, k in enumerate(keeps):
        score = k.get("score", max(9 - i, 8))
        why = f" — {k['why']}" if k.get("why") else ""
        lines.append(f'KEEP-{score}: "{k["text"]}"{why}')
    for i, k in enumerate(kills):
        score = k.get("score", min(2 + i, 3))
        why = f" — {k['why']}" if k.get("why") else ""
        lines.append(f'KILL-{score}: "{k["text"]}"{why}')
    return "\n".join(lines)


S2_TMPL = """IN: JSON array of stage-1 survivors [{{id, text, embed_prior}}].
JOB: score each facet 0-10 WITH extracted evidence. Facets: isomorphism (name the two
domains and the structural mapping — no nameable mapping means score <=3), novelty vs
the anchors below, voice_fit, actionability. Evidence first, then score.
OUT: JSON array [{{"id":"...","facets":{{"isomorphism":n,"novelty":n,"voice_fit":n,
"actionability":n}},"evidence":["<the claim that earned it>"],"total":n,
"route":"null|jeff|archive","confidence":"high|borderline"}}]. Nothing else.
STOP: cannot extract evidence for a facet -> that facet <=3, confidence:"borderline".

{anchors}
"""

ADJ_TMPL = """IN: JSON array of borderline items [{{id,text,evidence,facets,total}}].
JOB: pairwise-compare each item against the ANCHORS below — clearly stronger than the
weakest KEEP? clearly weaker than the strongest KILL? Re-score total accordingly and
set route. Comparison, not re-rating: justify by naming which anchor it beats/loses to.
OUT: same schema as mining.score.s2 output. JSON only.
STOP: cannot compare -> keep prior total, confidence:"borderline".

{anchors}
"""

VOICE_TMPL = """IN: {{"item":{{"id","text","evidence":[...],"scores":{{...}}}},"route":"null|jeff"}}
JOB: write ONE X post from the item's idea using ONLY its evidence. Voices:
NULL = systems voice: terse, technical, claims over vibes, no hashtags, no emojis.
JEFF = first-person builder: plainspoken, concrete, one lived detail, no hype.
EXEMPLARS:
{null_ex}
{jeff_ex}
OUT: {{"voice":"null|jeff","text":"<=500 chars"}} — JSON only, no prose.
STOP: evidence missing or empty -> {{"error":"no_evidence"}}.
"""


def main(path):
    data = yaml.safe_load(pathlib.Path(path).read_text())
    keeps, kills = data.get("keeps", []), data.get("kills", [])
    voices = data.get("voices", {}) or {}
    if None in voices:  # unquoted `null:` in YAML becomes a None key
        voices["null"] = voices.pop(None)
    if not keeps or not kills:
        sys.exit("anchors.yaml needs at least one keep and one kill")

    anchors = _anchor_block(keeps, kills)
    DIRECTIVES.mkdir(parents=True, exist_ok=True)
    (DIRECTIVES / "mining.score.s2.md").write_text(S2_TMPL.format(anchors=anchors))
    (DIRECTIVES / "mining.adjudicate.md").write_text(ADJ_TMPL.format(anchors=anchors))

    nx = "\n".join(f"  NULL-{i+1}: {t}" for i, t in enumerate(voices.get("null", [])[:2])) \
         or "  NULL-1: <none provided>"
    jx = "\n".join(f"  JEFF-{i+1}: {t}" for i, t in enumerate(voices.get("jeff", [])[:2])) \
         or "  JEFF-1: <none provided>"
    (DIRECTIVES / "draft.voice.md").write_text(VOICE_TMPL.format(null_ex=nx, jeff_ex=jx))

    cfg = mp._cfg()
    ex_path = ROOT / cfg["embed"]["exemplars"]
    embedded = 0
    with ex_path.open("w") as f:  # rewrite, not append: idempotent
        for k in keeps:
            text = " ".join(k["text"].split())
            vec = mp.embed(text, cfg)
            embedded += vec is not None
            f.write(json.dumps({"text": text, "vec": vec}) + "\n")

    print(f"[anchors] {len(keeps)} keeps + {len(kills)} kills -> 2 directives regenerated")
    print(f"[anchors] draft.voice.md regenerated "
          f"({len(voices.get('null', []))} null / {len(voices.get('jeff', []))} jeff exemplars)")
    print(f"[anchors] exemplars.jsonl rewritten: {embedded}/{len(keeps)} embedded"
          + ("" if embedded == len(keeps) else "  -> run `mining_pipeline.py reembed` on the Mini"))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "anchors.yaml")
