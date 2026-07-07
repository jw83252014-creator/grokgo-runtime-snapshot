#!/usr/bin/env python3
"""research.loop — the looping Badass Fable researcher cell.

Reads directives/research.loop.md, runs a research cycle on the FREE local model (via badass-fable.py),
writes a findings receipt + an improvement candidate, commits to git (milestone), sleeps, loops.
Local + free, so it can run continuously. Brakes: a STOP_LOOP file halts it; a max-cycle cap backstops.

Usage: python3 research_loop.py [--once] [--interval SECONDS] [--max N]
"""
import os, sys, subprocess, time
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
BF = ROOT / "spikes/openclaude-local/badass-fable.py"
DIRECTIVE = ROOT / "directives/research.loop.md"
OUT = ROOT / "research/loop"
CANDIDATES = ROOT / "proposals/research-loop-candidates.md"
STOP = ROOT / "STOP_LOOP"

TARGETS = [
    "better local models for the cheap lane (HF: Qwen/Llama/Phi/DeepSeek-distill, size vs quality on 16GB)",
    "fable-trace RAG: which exemplars actually help, retrieval quality",
    "harness techniques worth stealing from the open agent ecosystem",
    "distilled/open datasets that could make a local cell reason better",
    "cheaper/faster local inference (MLX tricks, quantization, speculative decoding)",
    "QLoRA on the traces: what to expect, how to measure before/after",
]


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def ask_fable(prompt: str, timeout=300) -> str:
    r = subprocess.run([sys.executable, str(BF), prompt], capture_output=True, text=True, timeout=timeout)
    return (r.stdout or "").strip() or (r.stderr or "").strip()


def cycle(n: int):
    target = TARGETS[n % len(TARGETS)]
    recent = sorted(OUT.glob("*.md"))[-3:] if OUT.exists() else []
    recent_note = "Prior receipts exist; do NOT repeat them." if recent else "First cycles."
    directive = DIRECTIVE.read_text() if DIRECTIVE.exists() else ""
    prompt = (
        f"You are the research.loop cell. Your directive:\n\n{directive}\n\n"
        f"THIS CYCLE'S TARGET: {target}\n{recent_note}\n"
        "Produce ONLY the findings receipt in the §5 format (target/found/candidate/next). "
        "Tag every factual claim verified|UNCERTAIN|needs:web|needs:frontier. No hype, no fabrication."
    )
    receipt = ask_fable(prompt)
    OUT.mkdir(parents=True, exist_ok=True)
    slug = target.split("(")[0].strip().replace(" ", "-").replace("/", "-")[:40]
    fn = OUT / f"{now().replace(':','').replace('-','')[:15]}-{slug}.md"
    fn.write_text(f"# research.loop receipt — {now()}\n\ntarget: {target}\n\n{receipt}\n")
    # append a candidate line (best-effort parse)
    cand = next((l for l in receipt.splitlines() if l.lower().strip().startswith("candidate")), "candidate: (see receipt)")
    with open(CANDIDATES, "a") as f:
        f.write(f"- [{now()}] ({slug}) {cand.split(':',1)[-1].strip()}\n")
    return fn


def git_commit(msg: str):
    subprocess.run(["git", "-C", str(ROOT), "-c", "user.name=Jeff Whiting",
                    "-c", "user.email=nullaxiom0@gmail.com", "add", "-A"], capture_output=True)
    subprocess.run(["git", "-C", str(ROOT), "-c", "user.name=Jeff Whiting",
                    "-c", "user.email=nullaxiom0@gmail.com", "commit", "-q", "-m", msg], capture_output=True)
    subprocess.run(["git", "-C", str(ROOT), "push", "-q", "origin", "main"], capture_output=True)


def main():
    once = "--once" in sys.argv
    interval = int(sys.argv[sys.argv.index("--interval")+1]) if "--interval" in sys.argv else 900
    mx = int(sys.argv[sys.argv.index("--max")+1]) if "--max" in sys.argv else (1 if once else 1000)
    if not CANDIDATES.exists():
        CANDIDATES.write_text("# research.loop — improvement candidates (append-only)\n\n")
    n = 0
    while n < mx:
        if STOP.exists():
            print(f"[{now()}] STOP_LOOP present — halting cleanly."); break
        try:
            fn = cycle(n)
            git_commit(f"research.loop cycle {n+1}: {fn.name}\n\nCo-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>")
            print(f"[{now()}] cycle {n+1} → {fn.name} (committed+pushed)")
        except Exception as e:
            print(f"[{now()}] cycle {n+1} error: {e}")
        n += 1
        if once or n >= mx:
            break
        time.sleep(interval)
    print(f"[{now()}] loop done ({n} cycles).")


if __name__ == "__main__":
    main()
