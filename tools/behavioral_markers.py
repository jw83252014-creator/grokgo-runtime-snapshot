#!/usr/bin/env python3
"""Behavioral Marker Computer v1.0.

Drop-in replacement for the placeholder BehavioralMarkerComputer in the
researcher population loop skeleton.

Design goals:
  * Zero required dependencies. Runs on stdlib alone.
  * Deterministic-first classification: every decision is rule-based and
    auditable. LLM calibration can judge the classifier later; it is not in
    the hot path.
  * Tolerant log ingestion: malformed lines and schema drift never crash the
    run.
  * Every marker value is persisted with provenance so emergence claims can be
    audited.

Optional embeddings:
  Set BEHAVIORAL_MARKERS_USE_SBERT=1 to use sentence-transformers if it is
  already installed and the model is locally available. The default backend is
  the zero-dependency hashing TF-IDF vectorizer to avoid surprise downloads.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
from collections import Counter, deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple


_SBERT_MODEL = None


def _try_load_sbert():
    """Lazy-load sentence-transformers only when explicitly enabled."""
    global _SBERT_MODEL
    if _SBERT_MODEL is not None:
        return _SBERT_MODEL
    enabled = os.environ.get("BEHAVIORAL_MARKERS_USE_SBERT", "").lower()
    if enabled not in {"1", "true", "yes"}:
        _SBERT_MODEL = False
        return _SBERT_MODEL
    try:
        from sentence_transformers import SentenceTransformer

        _SBERT_MODEL = SentenceTransformer("all-MiniLM-L6-v2")
    except Exception:
        _SBERT_MODEL = False
    return _SBERT_MODEL


@dataclass
class LogEntry:
    """Normalized view over one JSONL line."""

    ts: Optional[float] = None
    cycle: Optional[int] = None
    role: str = ""
    kind: str = ""
    text: str = ""
    tokens: int = 0
    raw: dict = field(default_factory=dict)
    line_no: int = -1


_TEXT_KEYS = (
    "text",
    "content",
    "message",
    "msg",
    "output",
    "output_summary",
    "prompt",
    "summary",
    "reasoning",
    "uncertainty",
    "why_fable",
    "decision",
    "description",
    "result",
    "stdout",
    "notes",
    "outcome",
    "behavior_class",
    "new_capability_vs_polish",
)
_TS_KEYS = ("ts", "timestamp", "time", "created_at")
_CYCLE_KEYS = ("cycle", "cycle_id", "turn", "step", "iteration", "loop_index")
_TOKEN_KEYS = ("tokens", "token_count", "total_tokens", "usage_tokens")
_ROLE_KEYS = ("role", "actor", "source", "agent", "src")
_KIND_KEYS = ("kind", "type", "event", "action_type", "lvl")


def _first(d: dict, keys: Tuple[str, ...], default=None):
    for k in keys:
        if k in d and d[k] not in (None, ""):
            return d[k]
    return default


def _coerce_text(v) -> str:
    if isinstance(v, str):
        return v
    if isinstance(v, list):
        parts = []
        for item in v:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                t = _first(item, _TEXT_KEYS)
                if isinstance(t, str):
                    parts.append(t)
        return "\n".join(parts)
    if isinstance(v, dict):
        t = _first(v, _TEXT_KEYS)
        return t if isinstance(t, str) else json.dumps(v, sort_keys=True)[:2000]
    return str(v)


def _nested_ctx(raw: dict) -> dict:
    ctx = raw.get("ctx", {})
    return ctx if isinstance(ctx, dict) else {}


def normalize_entry(raw: dict, line_no: int) -> LogEntry:
    e = LogEntry(raw=raw, line_no=line_no)
    ctx = _nested_ctx(raw)

    ts = _first(raw, _TS_KEYS)
    if ts is not None:
        try:
            if isinstance(ts, str):
                try:
                    e.ts = datetime.fromisoformat(ts.replace("Z", "+00:00")).timestamp()
                except ValueError:
                    e.ts = float(ts)
            else:
                e.ts = float(ts)
        except (ValueError, TypeError):
            pass

    cyc = _first(raw, _CYCLE_KEYS)
    if cyc is None:
        cyc = _first(ctx, _CYCLE_KEYS)
    try:
        e.cycle = int(cyc) if cyc is not None else None
    except (ValueError, TypeError):
        pass

    tok = _first(raw, _TOKEN_KEYS, None)
    if tok is None:
        tok = _first(ctx, _TOKEN_KEYS, 0)
    if isinstance(tok, dict):
        tok = tok.get("total", tok.get("input", 0) + tok.get("output", 0))
    try:
        e.tokens = int(tok)
    except (ValueError, TypeError):
        e.tokens = 0

    e.role = str(_first(raw, _ROLE_KEYS, "")).lower()
    e.kind = str(_first(raw, _KIND_KEYS, "")).lower()

    base_text = _coerce_text(_first(raw, _TEXT_KEYS, ""))
    supplements = []
    for source in (raw, ctx):
        for key in (
            "task_type",
            "outcome",
            "output_summary",
            "behavior_class",
            "new_capability_vs_polish",
            "status",
        ):
            value = source.get(key) if isinstance(source, dict) else None
            if value in (None, ""):
                continue
            text = _coerce_text(value)
            if text and text not in base_text:
                supplements.append(f"{key}: {text}")
    if ctx:
        ctx_text = json.dumps(ctx, sort_keys=True)[:1200]
        e.text = f"{base_text} {' '.join(supplements)} {ctx_text}".strip()
    else:
        e.text = f"{base_text} {' '.join(supplements)}".strip()
    return e


class LogIngestor:
    """Incremental reader for JSONL logs with offset tracking."""

    def __init__(self, log_path: str, offset_dir: str = "researcher_state"):
        self.log_path = Path(log_path).expanduser()
        offset_path = Path(offset_dir).expanduser()
        offset_path.mkdir(parents=True, exist_ok=True)
        stem = hashlib.md5(str(self.log_path).encode()).hexdigest()[:10]
        self.offset_file = offset_path / f".offset-{stem}"
        self.malformed_count = 0
        self._line_no = 0

    def _load_offset(self) -> int:
        try:
            return int(self.offset_file.read_text().strip())
        except (FileNotFoundError, ValueError):
            return 0

    def _save_offset(self, offset: int):
        self.offset_file.write_text(str(offset))

    def read_new(self, max_entries: int = 5000) -> List[LogEntry]:
        if not self.log_path.exists():
            return []
        entries: List[LogEntry] = []
        offset = self._load_offset()
        size = self.log_path.stat().st_size
        if offset > size:
            offset = 0
        with self.log_path.open("r", errors="replace") as f:
            f.seek(offset)
            for line in f:
                self._line_no += 1
                line = line.strip()
                if not line:
                    continue
                try:
                    raw = json.loads(line)
                    if isinstance(raw, dict):
                        entries.append(normalize_entry(raw, self._line_no))
                    else:
                        self.malformed_count += 1
                except json.JSONDecodeError:
                    self.malformed_count += 1
                if len(entries) >= max_entries:
                    break
            self._save_offset(f.tell())
        return entries

    def read_all(self, max_entries: int = 100_000) -> List[LogEntry]:
        if not self.log_path.exists():
            return []
        entries: List[LogEntry] = []
        with self.log_path.open("r", errors="replace") as f:
            for i, line in enumerate(f):
                line = line.strip()
                if not line:
                    continue
                try:
                    raw = json.loads(line)
                    if isinstance(raw, dict):
                        entries.append(normalize_entry(raw, i))
                    else:
                        self.malformed_count += 1
                except json.JSONDecodeError:
                    self.malformed_count += 1
                if len(entries) >= max_entries:
                    break
        return entries


_RULES: List[Tuple[str, str, re.Pattern, float]] = []


def _rule(name: str, category: str, pattern: str, weight: float = 1.0):
    _RULES.append((name, category, re.compile(pattern, re.I), weight))


_rule(
    "new_file",
    "goal",
    r"\b(creat(e|ed|ing)|wrote|writing) (a )?(new )?(file|module|script|cell|endpoint|test)\b",
    2.0,
)
_rule("completion_marker", "goal", r"\b(task |objective |goal )?(complete[d]?|done|finished|shipped|deployed|merged)\b", 1.5)
_rule("bet_placed", "goal", r"\b(plac(e|ed|ing) (a )?(bet|order|position)|bought (yes|no) shares|entered position)\b", 2.0)
_rule("new_capability", "goal", r"\b(implement(ed|ing)?|built|adding support for|integrat(ed|ing))\b", 1.5)
_rule("external_output", "goal", r"\b(post(ed|ing)? to|publish(ed|ing)?|submitt(ed|ing)|sent (the )?(report|paper|snapshot))\b", 2.0)
_rule("research_synthesis", "goal", r"\b(conclusion|finding[s]?:|synthesi[sz]ed?|key insight|hypothesis (confirmed|rejected))\b", 1.2)

_rule("refactor_only", "polish", r"\b(refactor(ed|ing)?|clean(ed|ing)? up|tid(y|ied|ying)|reorganiz(ed|ing))\b", 2.0)
_rule("cosmetic", "polish", r"\b(rename[d]?|reword(ed|ing)?|formatt(ed|ing)|whitespace|typo[s]?|comment[s]? (updated|improved)|docstring)\b", 1.5)
_rule("re_review", "polish", r"\b(re-?(read|review|check|visit)(ed|ing)? (the )?(same|previous|existing|earlier))\b", 2.0)
_rule("minor_tweak", "polish", r"\b(minor (tweak|change|update|improvement)|slight(ly)? (improv|adjust)|polish(ed|ing)?)\b", 2.0)
_rule("summary_of_summary", "polish", r"\bsummar(y|ize[d]?) of (the |my )?(previous |earlier |last )?(summary|report|notes)\b", 2.5)

_rule("error_detected", "correction", r"\b(error|exception|traceback|failed|failure|bug|incorrect|wrong|mistake)\b", 1.0)
_rule("approach_change", "correction", r"\b(instead|different approach|switch(ed|ing) to|fall(ing)? back to|retry(ing)? with|root cause|fix(ed|ing) by)\b", 1.5)
_rule("revert", "correction", r"\b(revert(ed|ing)?|roll(ed|ing)? back|undo(ing)?)\b", 1.2)

_rule("handoff", "cooperation", r"\b(hand(ed|ing)? (off|over) to|delegat(ed|ing) to|passing to|requested from) (the )?\w+ ?(cell|agent|layer)\b", 2.0)
_rule("cross_cell_read", "cooperation", r"\b(read(ing)?|consum(ed|ing)|using) (the )?\w+ (cell|agent)'?s? (output|result|signal|report)\b", 1.5)
_rule("shared_state", "cooperation", r"\borganism-state\.md\b", 1.0)

_rule("health_check", "maintenance", r"\b(health check|heartbeat|watchdog|credit (check|balance)|sleep(ing)?|waiting for|auth init|phase_transition|inference_start)\b", 1.5)
_rule("log_rotation", "maintenance", r"\b(rotat(ed|ing) log|archiv(ed|ing)|cleanup of old)\b", 1.5)

CATEGORIES = ("goal", "polish", "correction", "cooperation", "maintenance")


@dataclass
class Classification:
    category: str
    confidence: float
    rule_hits: List[str]


def classify_entry(entry: LogEntry) -> Classification:
    scores = Counter()
    hits: List[str] = []
    text = entry.text[:4000]
    for name, cat, pat, weight in _RULES:
        if pat.search(text):
            scores[cat] += weight
            hits.append(name)
    if not scores:
        if entry.kind in ("tool_result", "tool", "observation", "debug", "info"):
            return Classification("maintenance", 0.3, ["fallback_kind_tool"])
        return Classification("unknown", 0.0, [])
    ranked = scores.most_common()
    top_cat, top_score = ranked[0]
    second = ranked[1][1] if len(ranked) > 1 else 0.0
    total = sum(scores.values())
    margin_conf = (top_score - second) / total if total else 0.0
    return Classification(top_cat, round(min(1.0, 0.4 + margin_conf), 3), hits)


class NoveltyEngine:
    """Novelty scorer using embeddings when explicitly enabled, else hashing."""

    DIM = 2048
    _token_re = re.compile(r"[a-z][a-z0-9_]{2,}")

    def __init__(self, window: int = 40):
        self.window = window
        self.history: deque = deque(maxlen=window)
        self.backend = "sbert" if _try_load_sbert() else "hash-tfidf"

    def _hash_vector(self, text: str) -> List[float]:
        vec = [0.0] * self.DIM
        tokens = self._token_re.findall(text.lower())
        if not tokens:
            return vec
        counts = Counter(tokens)
        for tok, count in counts.items():
            idx = int(hashlib.md5(tok.encode()).hexdigest(), 16) % self.DIM
            sign = 1.0 if int(hashlib.sha1(tok.encode()).hexdigest(), 16) % 2 else -1.0
            vec[idx] += sign * (1.0 + math.log(count))
        return vec

    def _embed(self, text: str) -> List[float]:
        model = _try_load_sbert()
        if model:
            return model.encode(text[:1500]).tolist()
        return self._hash_vector(text[:6000])

    @staticmethod
    def _cosine_distance(a: List[float], b: List[float]) -> float:
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(y * y for y in b))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return 1.0 - (dot / (norm_a * norm_b))

    def _centroid(self) -> Optional[List[float]]:
        if not self.history:
            return None
        dim = len(self.history[0])
        centroid = [0.0] * dim
        for vec in self.history:
            for i, value in enumerate(vec):
                centroid[i] += value
        n = len(self.history)
        return [value / n for value in centroid]

    def score_cycle(self, cycle_text: str) -> float:
        if not cycle_text.strip():
            return 0.0
        vec = self._embed(cycle_text)
        centroid = self._centroid()
        self.history.append(vec)
        if centroid is None:
            return 0.5
        return round(self._cosine_distance(vec, centroid), 4)


class VitalityIndex:
    """Weighted marker composite with EMA smoothing."""

    WEIGHTS = {
        "goal_directed_pct": 0.25,
        "polishing_avoidance": 0.20,
        "self_correction_quality": 0.15,
        "cooperation_handoff_rate": 0.12,
        "novelty_rate": 0.13,
        "long_horizon_coherence": 0.10,
        "efficiency_norm": 0.05,
    }

    def __init__(self, ema_alpha: float = 0.15):
        self.alpha = ema_alpha
        self.ema: Optional[float] = None

    def compute(self, markers: Dict, external_fitness_delta: float = 0.0) -> Tuple[float, float]:
        raw = 0.0
        for key, weight in self.WEIGHTS.items():
            raw += weight * float(markers.get(key, 0.0))
        raw *= 100.0
        raw += 10.0 * math.tanh(external_fitness_delta / 25.0)
        raw = max(0.0, min(100.0, raw))
        self.ema = raw if self.ema is None else self.alpha * raw + (1 - self.alpha) * self.ema
        return round(raw, 1), round(self.ema, 1)


class BehavioralMarkerComputer:
    """Compute deterministic behavioral markers from normalized log entries."""

    def __init__(
        self,
        state_dir: str = "researcher_state",
        novelty_window: int = 40,
        coherence_anchor_texts: Optional[List[str]] = None,
    ):
        self.state_dir = Path(state_dir).expanduser()
        (self.state_dir / "markers").mkdir(parents=True, exist_ok=True)
        self.novelty = NoveltyEngine(window=novelty_window)
        self.vitality = VitalityIndex()
        self._anchor_vecs: List[List[float]] = []
        for text in coherence_anchor_texts or []:
            self._anchor_vecs.append(self.novelty._embed(text))

    @staticmethod
    def _group_cycles(entries: List[LogEntry]) -> Dict[int, List[LogEntry]]:
        cycles: Dict[int, List[LogEntry]] = {}
        synthetic = 0
        current_key = None
        for entry in entries:
            if entry.cycle is not None:
                current_key = entry.cycle
            elif current_key is None:
                synthetic += 1
                current_key = -synthetic
            cycles.setdefault(current_key, []).append(entry)
        return cycles

    def _coherence(self, cycle_text: str) -> float:
        if not self._anchor_vecs or not cycle_text.strip():
            return 0.5
        vec = self.novelty._embed(cycle_text)
        sims = [1.0 - self.novelty._cosine_distance(vec, anchor) for anchor in self._anchor_vecs]
        return round(max(0.0, min(1.0, max(sims))), 4)

    def compute_markers(self, entries: List[LogEntry], external_fitness_delta: float = 0.0) -> Dict:
        if not entries:
            return self._empty_result()

        cycles = self._group_cycles(entries)
        cat_counts = Counter()
        rule_hit_counts = Counter()
        correction_pairs = 0
        error_count = 0
        total_tokens = 0
        novelty_scores: List[float] = []
        coherence_scores: List[float] = []
        classified = 0

        for _, cycle_entries in sorted(cycles.items()):
            cycle_text_parts: List[str] = []
            saw_error = False
            saw_change = False
            for entry in cycle_entries:
                total_tokens += entry.tokens
                classification = classify_entry(entry)
                if classification.category != "unknown":
                    cat_counts[classification.category] += 1
                    classified += 1
                for hit in classification.rule_hits:
                    rule_hit_counts[hit] += 1
                    if hit == "error_detected":
                        saw_error = True
                    if hit in ("approach_change", "revert"):
                        saw_change = True
                if entry.text:
                    cycle_text_parts.append(entry.text[:1200])
            if saw_error:
                error_count += 1
                if saw_change:
                    correction_pairs += 1
            cycle_text = "\n".join(cycle_text_parts)
            novelty_scores.append(self.novelty.score_cycle(cycle_text))
            coherence_scores.append(self._coherence(cycle_text))

        n_cat = sum(cat_counts.values()) or 1
        n_cycles = len(cycles) or 1
        goal_pct = cat_counts["goal"] / n_cat
        polish_pct = cat_counts["polish"] / n_cat
        actions_per_token = classified / total_tokens if total_tokens else 0.0
        actions_per_ktok = classified / (total_tokens / 1000.0) if total_tokens else 0.0

        markers = {
            "goal_directed_pct": round(goal_pct, 4),
            "polishing_pct": round(polish_pct, 4),
            "polishing_avoidance": round(1.0 - polish_pct, 4),
            "self_correction_quality": round(correction_pairs / error_count, 4) if error_count else 1.0,
            "cooperation_handoff_rate": round(cat_counts["cooperation"] / n_cycles, 4),
            "novelty_rate": round(sum(novelty_scores) / len(novelty_scores), 4) if novelty_scores else 0.0,
            "long_horizon_coherence": round(sum(coherence_scores) / len(coherence_scores), 4) if coherence_scores else 0.5,
            "efficiency_actions_per_token": round(actions_per_token, 6),
            "efficiency_norm": round(math.tanh(actions_per_ktok / 5.0), 4) if total_tokens else 0.0,
            "token_burn_total": total_tokens,
            "cycles_analyzed": n_cycles,
            "entries_classified": classified,
            "entries_total": len(entries),
            "category_counts": dict(cat_counts),
            "novelty_backend": self.novelty.backend,
        }
        vitality_raw, vitality_ema = self.vitality.compute(markers, external_fitness_delta)
        markers["vitality_index"] = vitality_raw
        markers["vitality_index_ema"] = vitality_ema
        self._persist(markers, cycles, rule_hit_counts)
        return markers

    def _persist(self, markers: Dict, cycles: Dict, rule_hits: Counter):
        day = datetime.now(timezone.utc).strftime("%Y%m%d")
        out = self.state_dir / "markers" / f"markers-{day}.jsonl"
        cycle_keys = [key for key in cycles.keys() if key >= 0]
        record = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "markers": markers,
            "provenance": {
                "cycle_range": [min(cycle_keys), max(cycle_keys)] if cycle_keys else None,
                "top_rule_hits": rule_hits.most_common(12),
            },
        }
        with out.open("a") as f:
            f.write(json.dumps(record, sort_keys=True) + "\n")

    @staticmethod
    def _empty_result() -> Dict:
        return {
            "goal_directed_pct": 0.0,
            "polishing_pct": 0.0,
            "polishing_avoidance": 0.0,
            "self_correction_quality": 0.0,
            "cooperation_handoff_rate": 0.0,
            "novelty_rate": 0.0,
            "long_horizon_coherence": 0.0,
            "efficiency_actions_per_token": 0.0,
            "efficiency_norm": 0.0,
            "vitality_index": 0.0,
            "vitality_index_ema": 0.0,
            "token_burn_total": 0,
            "cycles_analyzed": 0,
            "entries_classified": 0,
            "entries_total": 0,
            "category_counts": {},
            "novelty_backend": "none",
        }


def _selftest():
    import tempfile

    synthetic = [
        {"cycle": 1, "role": "assistant", "type": "action", "tokens": 900, "text": "Created a new file weather_cell.py implementing the signal ingestion pipeline. Task complete."},
        {"cycle": 1, "role": "tool", "type": "tool_result", "tokens": 120, "text": "File written successfully."},
        {"cycle": 2, "role": "assistant", "type": "action", "tokens": 800, "text": "Refactored weather_cell.py, cleaned up whitespace and improved docstrings. Minor tweak to naming."},
        {"cycle": 3, "role": "assistant", "type": "action", "tokens": 1100, "text": "Error: KeyError in parser. Switching to a different approach: fixed by using .get with default."},
        {"cycle": 4, "role": "assistant", "type": "action", "tokens": 700, "text": "Handing off to the Betting cell with the fresh weather signal. Reading organism-state.md for allocation."},
        {"cycle": 5, "role": "assistant", "type": "action", "tokens": 950, "text": "Placed bet: bought YES shares on NYC-rain market after cross-referencing news sentiment. New capability: integrated calibration checker."},
        {"cycle": 6, "role": "assistant", "type": "action", "tokens": 650, "text": "Summary of the previous summary. Polishing the report formatting again, reworded a comment."},
    ]
    with tempfile.TemporaryDirectory() as tmp:
        log = Path(tmp) / "unified.jsonl"
        with log.open("w") as f:
            for row in synthetic:
                f.write(json.dumps(row) + "\n")
            f.write("THIS LINE IS NOT JSON\n")
        ingestor = LogIngestor(str(log), offset_dir=tmp)
        computer = BehavioralMarkerComputer(
            state_dir=tmp,
            coherence_anchor_texts=[
                "Improve betting calibration using weather and news signals; build and cooperate between specialized cells; avoid polishing loops."
            ],
        )
        entries = ingestor.read_new()
        assert len(entries) == 7, f"expected 7 entries, got {len(entries)}"
        assert ingestor.malformed_count == 1, "malformed line should be counted"
        markers = computer.compute_markers(entries, external_fitness_delta=18.4)
        print(json.dumps(markers, indent=2, sort_keys=True))
        assert markers["cycles_analyzed"] == 6
        assert 0 < markers["goal_directed_pct"] <= 1
        assert markers["polishing_pct"] > 0
        assert markers["self_correction_quality"] == 1.0
        assert markers["cooperation_handoff_rate"] > 0
        assert 0 <= markers["vitality_index"] <= 100
        assert ingestor.read_new() == []
        print(f"\nNovelty backend in use: {markers['novelty_backend']}")
        print("Self-test PASSED.")


if __name__ == "__main__":
    _selftest()
