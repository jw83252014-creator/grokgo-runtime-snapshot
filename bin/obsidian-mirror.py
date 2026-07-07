#!/usr/bin/env python3
"""One-way mirror of Grok Go knowledge into the Obsidian vault (Jwnull) as linked markdown.
NEVER touches the rest of the vault — writes only under <vault>/GrokGo/. Source of truth stays in the
repos; this is a read-only-into-Obsidian projection so Dataview/Juggl/Graph Analysis can use it.
"""
import shutil, pathlib, datetime

VAULT = pathlib.Path("~/Documents/Jwnull").expanduser()
DEST = VAULT / "GrokGo"
SOURCES = {
    "mining":    pathlib.Path("~/mining-engine/mining-runs").expanduser(),
    "proposals": pathlib.Path("~/grokgo/proposals").expanduser(),
    "opengold":  pathlib.Path("~/OpenGoldSDR/docs").expanduser(),
    "research":  pathlib.Path("~/OpenGoldSDR/research").expanduser(),
}

def mirror():
    if DEST.exists():
        shutil.rmtree(DEST)          # one-way: rebuild our subtree only
    DEST.mkdir(parents=True)
    counts = {}
    for name, src in SOURCES.items():
        if not src.exists():
            continue
        out = DEST / name; out.mkdir(parents=True, exist_ok=True)
        n = 0
        for f in src.glob("*.md"):
            shutil.copy2(f, out / f.name); n += 1
        counts[name] = n
    # index with wikilinks + a Dataview query (Jwnull already has Dataview)
    ts = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    lines = [f"# Grok Go (mirror)\n", f"_One-way mirror, rebuilt {ts}. Edit sources in the repos, not here._\n"]
    for name, n in counts.items():
        lines.append(f"## {name} ({n})")
        for f in sorted((DEST / name).glob("*.md")):
            lines.append(f"- [[{name}/{f.stem}]]")
        lines.append("")
    lines += ["## All notes (Dataview)", "```dataview", 'LIST FROM "GrokGo"', "```", ""]
    (DEST / "INDEX.md").write_text("\n".join(lines))
    print(f"mirrored {sum(counts.values())} notes -> {DEST}  ({counts})")

if __name__ == "__main__":
    mirror()
