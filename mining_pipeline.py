#!/usr/bin/env python3
"""Jeff Filter pipeline — S0-S2 plus the stage glue. All t0 code: zero model calls
here; every model touch goes through bus -> dispatcher -> brakes.

Commands:
  mining_pipeline.py ingest <items.jsonl>   S0 normalize -> S1 gates -> S2 embed
                                            prior -> batch -> mining.score.s1 tasks
  mining_pipeline.py advance                consume outbox results, move items to
                                            the next stage (s1->s2->draft->review)
  mining_pipeline.py add-exemplar "<text>"  grow the exemplar corpus (KEEP posts)
  mining_pipeline.py reembed                fill vectors for exemplars added offline
  mining_pipeline.py status                 stage + disposition counts

items.jsonl: one JSON object per line: {"id": optional, "text": ..., "source": optional}
Run `advance` on a 2-minute cron/launchd interval (see PHASE2.md).
"""
import hashlib
import json
import os
import pathlib
import re
import sqlite3
import sys
import time

import requests
import yaml

import bus

ROOT = pathlib.Path(os.environ.get("GROKGO_ROOT", str(pathlib.Path.home() / "grokgo")))
DB = ROOT / "ledger.db"
CFGPATH = ROOT / "mining_config.yaml"
PENDING = ROOT / "review" / "pending"


def _cfg():
    return yaml.safe_load(CFGPATH.read_text())


def _db():
    con = sqlite3.connect(DB)
    con.execute("""CREATE TABLE IF NOT EXISTS mined(
        hash TEXT PRIMARY KEY, id TEXT, ts REAL, disposition TEXT)""")
    con.execute("""CREATE TABLE IF NOT EXISTS items(
        id TEXT PRIMARY KEY, hash TEXT, json TEXT, stage TEXT)""")
    return con


def _dispose(con, item_id, disposition):
    con.execute("UPDATE mined SET disposition=? WHERE id=?", (disposition, item_id))
    con.commit()


# ---------- S0: normalize ----------
def normalize(raw):
    text = " ".join(str(raw.get("text", "")).split())
    h = hashlib.sha256(text.lower().encode()).hexdigest()[:16]
    return {"id": raw.get("id") or h[:12], "hash": h, "text": text,
            "source": raw.get("source", "")}


# ---------- S1: hard gates (code-only, ~free) ----------
def _has_keyword(low, keywords):
    for k in keywords:
        k = k.lower()
        if " " in k:
            if k in low:
                return True
        elif re.search(r"\b" + re.escape(k) + r"\b", low):
            return True
    return False


def gates(item, cfg, con):
    if con.execute("SELECT 1 FROM mined WHERE hash=?", (item["hash"],)).fetchone():
        return False, "dup"
    if len(item["text"]) < int(cfg["min_chars"]):
        return False, "too_short"
    low = item["text"].lower()
    for p in cfg["bait_patterns"]:
        if p.lower() in low:
            return False, "bait"
    if not _has_keyword(low, cfg["domain_keywords"]):
        return False, "off_domain"
    return True, "pass"


# ---------- S2: embedding prior (uses existing nomic-embed/Ollama stack) ----------
def embed(text, cfg):
    try:
        r = requests.post(cfg["embed"]["url"],
                          json={"model": cfg["embed"]["model"], "prompt": text},
                          timeout=cfg["embed"].get("timeout", 5))
        r.raise_for_status()
        return r.json().get("embedding")
    except Exception:
        return None  # degrade gracefully: items pass through with prior=None


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = sum(x * x for x in a) ** 0.5
    nb = sum(y * y for y in b) ** 0.5
    return dot / (na * nb) if na and nb else 0.0


def load_exemplars(cfg):
    p = ROOT / cfg["embed"]["exemplars"]
    out = []
    if p.exists():
        for line in p.read_text().splitlines():
            try:
                e = json.loads(line)
                if e.get("vec"):
                    out.append(e)
            except Exception:
                pass
    return out


def embed_prior(text, cfg, exemplars):
    if not exemplars:
        return None
    v = embed(text, cfg)
    if not v:
        return None
    return round(max(cosine(v, e["vec"]) for e in exemplars), 4)


# ---------- commands ----------
def cmd_ingest(path):
    cfg, con = _cfg(), _db()
    exemplars = load_exemplars(cfg)
    survivors, counts = [], {}
    for line in pathlib.Path(path).read_text().splitlines():
        if not line.strip():
            continue
        item = normalize(json.loads(line))
        ok, reason = gates(item, cfg, con)
        counts[reason] = counts.get(reason, 0) + 1
        if reason != "dup":  # dups already have a mined row
            con.execute("INSERT OR IGNORE INTO mined VALUES (?,?,?,?)",
                        (item["hash"], item["id"], time.time(),
                         "in_pipeline" if ok else f"killed_gate:{reason}"))
        if ok:
            item["embed_prior"] = embed_prior(item["text"], cfg, exemplars)
            con.execute("INSERT OR REPLACE INTO items VALUES (?,?,?,?)",
                        (item["id"], item["hash"], json.dumps(item), "s1"))
            survivors.append({"id": item["id"], "text": item["text"],
                              "embed_prior": item["embed_prior"]})
    con.commit()
    bs = int(cfg["batch_size"])
    for i in range(0, len(survivors), bs):
        tid = bus.submit("mining.score.s1", survivors[i:i + bs], cfg["lane"])
        print(f"[ingest] submitted {tid} ({len(survivors[i:i+bs])} items)")
    print(f"[ingest] gates: {counts}  -> {len(survivors)} into s1")


def _load_item(con, item_id):
    row = con.execute("SELECT json FROM items WHERE id=?", (item_id,)).fetchone()
    return json.loads(row[0]) if row else None


def _save_item(con, item_id, item, stage):
    item["stage"] = stage
    con.execute("UPDATE items SET json=?, stage=? WHERE id=?",
                (json.dumps(item), stage, item_id))
    con.commit()


def cmd_advance():
    cfg, con = _cfg(), _db()
    n = 0
    for res in bus.results(["mining.", "draft."], consume=True):
        n += 1
        t, out = res.get("type", ""), res.get("output")

        if t == "mining.score.s1":
            if not isinstance(out, list):
                print(f"[skip] {res.get('task')}: unexpected s1 output shape")
                continue
            batch = []
            for o in out:
                iid = o.get("id")
                item = _load_item(con, iid)
                if not item:
                    continue
                if o.get("keep"):
                    _save_item(con, iid, item, "s2")
                    batch.append({"id": iid, "text": item["text"],
                                  "embed_prior": item.get("embed_prior")})
                else:
                    _save_item(con, iid, item, "killed_s1")
                    _dispose(con, iid, "killed_s1")
            bs = int(cfg["batch_size"])
            for i in range(0, len(batch), bs):
                tid = bus.submit("mining.score.s2", batch[i:i + bs], cfg["lane"])
                print(f"[advance] s1->s2 {tid} ({len(batch[i:i+bs])} items)")

        elif t in ("mining.score.s2", "mining.adjudicate"):
            if not isinstance(out, list):
                print(f"[skip] {res.get('task')}: unexpected output shape")
                continue
            th = cfg["thresholds"]
            for o in out:
                iid = o.get("id")
                item = _load_item(con, iid)
                if not item:
                    continue
                item.update({"facets": o.get("facets"), "evidence": o.get("evidence"),
                             "total": o.get("total"), "route": o.get("route"),
                             "confidence": o.get("confidence")})
                total = float(o.get("total") or 0)
                route = o.get("route", "archive")
                if total >= th["draft_min_total"] and route in ("null", "jeff"):
                    _save_item(con, iid, item, "draft")
                    bus.submit("draft.voice",
                               {"item": {"id": iid, "text": item["text"],
                                         "evidence": item.get("evidence"),
                                         "scores": item.get("facets")},
                                "route": route},
                               cfg["lane"], task_id=f"draft-{iid}")
                    print(f"[advance] {iid} total={total} -> draft.voice ({route})")
                elif t == "mining.score.s2" and (
                        total >= th["adjudicate_min"]
                        or o.get("confidence") == "borderline"):
                    _save_item(con, iid, item, "adjudicate")
                    bus.submit("mining.adjudicate",
                               [{"id": iid, "text": item["text"],
                                 "evidence": item.get("evidence"),
                                 "facets": item.get("facets"), "total": total}],
                               cfg["lane"])
                    print(f"[advance] {iid} total={total} -> adjudicate")
                else:
                    _save_item(con, iid, item, "archived")
                    _dispose(con, iid, "archived")
                    print(f"[advance] {iid} total={total} -> archive")

        elif t == "draft.voice":
            iid = res.get("task", "")
            iid = iid[len("draft-"):] if iid.startswith("draft-") else iid
            item = _load_item(con, iid)
            if not item:
                print(f"[skip] draft result for unknown item {iid}")
                continue
            if isinstance(out, dict) and out.get("text"):
                PENDING.mkdir(parents=True, exist_ok=True)
                bundle = {"id": iid, "route": item.get("route"),
                          "total": item.get("total"),
                          "evidence": item.get("evidence"),
                          "source": item.get("source", ""),
                          "original": item["text"], "draft": out}
                (PENDING / f"{iid}.json").write_text(json.dumps(bundle, indent=2))
                _save_item(con, iid, item, "review")
                print(f"[advance] {iid} -> review queue")
            else:
                _save_item(con, iid, item, "draft_failed")
                _dispose(con, iid, "draft_failed")
    print(f"[advance] processed {n} result(s)")


def cmd_add_exemplar(text):
    cfg = _cfg()
    v = embed(" ".join(text.split()), cfg)
    p = ROOT / cfg["embed"]["exemplars"]
    with p.open("a") as f:
        f.write(json.dumps({"text": " ".join(text.split()), "vec": v}) + "\n")
    print(f"[exemplar] added ({'embedded' if v else 'vec=null — run reembed when Ollama is up'})")


def cmd_reembed():
    cfg = _cfg()
    p = ROOT / cfg["embed"]["exemplars"]
    if not p.exists():
        print("[reembed] no exemplar file")
        return
    rows, fixed = [], 0
    for line in p.read_text().splitlines():
        e = json.loads(line)
        if not e.get("vec"):
            e["vec"] = embed(e["text"], cfg)
            fixed += e["vec"] is not None
        rows.append(e)
    p.write_text("".join(json.dumps(e) + "\n" for e in rows))
    print(f"[reembed] filled {fixed} vector(s)")


def cmd_status():
    con = _db()
    print("items by stage:",
          dict(con.execute("SELECT stage, COUNT(*) FROM items GROUP BY stage")))
    print("mined by disposition:",
          dict(con.execute("SELECT disposition, COUNT(*) FROM mined GROUP BY disposition")))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "ingest":
        cmd_ingest(sys.argv[2])
    elif cmd == "advance":
        cmd_advance()
    elif cmd == "add-exemplar":
        cmd_add_exemplar(sys.argv[2])
    elif cmd == "reembed":
        cmd_reembed()
    else:
        cmd_status()
