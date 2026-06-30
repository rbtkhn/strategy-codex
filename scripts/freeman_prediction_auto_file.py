#!/usr/bin/env python3
"""Score Freeman captures for auto-file prediction notes (no manifest audit)."""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
AUTO_FILE_CONFIG = REPO_ROOT / "statecraft" / "data" / "freeman-prediction-auto-file.json"
PREDICTIONS_DIR = REPO_ROOT / "statecraft" / "notes" / "predictions"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import shelf_index_utils as shelf_utils  # noqa: E402
from audit_statecraft_archive_index import iter_archive_captures_for_shelf  # noqa: E402
from build_freeman_index import parse_head, pub_date_key  # noqa: E402
from freeman_prediction_pilot import (  # noqa: E402
    FREEMAN_PILOT_EVENT_ORDER,
    FREEMAN_SPEAKER,
    REVIEW_SPEECH_ACTS,
    load_thesis_map,
    parse_register_capture_paths,
    patterns_match,
    iso_now,
)
from materialize_freeman_predictions import (  # noqa: E402
    EVENT_LABEL,
    EVENT_SLUG,
    _prediction_status,
    read_capture_meta,
    youtube_id_from_meta,
)
from prediction_lib import collect_prediction_notes  # noqa: E402

ARCHIVE = REPO_ROOT / "source-archive" / "statecraft"

FRONTMATTER_RE = re.compile(r"\A---\r?\n.*?\r?\n---\r?\n", re.DOTALL)
SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")
REST_RE = re.compile(
    r"\b(as I said|I['']ve argued|still believe|I was wrong|I misread|I was right|as I predicted)\b",
    re.I,
)
INTRO_SKIP = re.compile(
    r"^(hi everyone|hi everybody|okay\.|kind:|language:|# |judge andrew|today is |today's |ambassador chaz freeman will be)",
    re.I,
)
HOST_ONLY = re.compile(
    r"^(hi everyone|judge andrew|ambassador chaz freeman will be|today is tuesday)",
    re.I,
)
AUTO_FILE_RE = re.compile(r"^auto_file:\s*true\s*$", re.M)

@dataclass
class ScoredCandidate:
    event_id: str
    source: str
    pub_date: str
    score: float
    threshold: float
    quote: str
    stance: str
    speech_act: str
    reasons: list[str]
    youtube_id: str | None
    canonical_rank: tuple[int, str]

def load_auto_file_config(path: Path | None = None) -> dict[str, Any]:
    target = path or AUTO_FILE_CONFIG
    data = json.loads(target.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("auto-file config must be a JSON object")
    return data

def iter_freeman_captures() -> list[tuple[str, Path, dict[str, Any]]]:
    rows: list[tuple[str, Path, dict[str, Any]]] = []
    for path in iter_archive_captures_for_shelf("freeman", ARCHIVE):
        meta = parse_head(path)
        body = path.read_text(encoding="utf-8", errors="replace")[:12000]
        if shelf_utils.shelf_capture_excluded("freeman", path, meta, body):
            continue
        pub = pub_date_key(meta, path)
        rows.append((pub, path, meta))
    rows.sort(key=lambda t: (t[0], t[1].name))
    return rows

def normalize_register_notes(raw: Any) -> list[str]:
    if not raw:
        return []
    if isinstance(raw, str):
        return [raw.replace("\\", "/")]
    return [str(rel).replace("\\", "/") for rel in raw]

def build_register_index(
    thesis: dict[str, dict[str, Any]],
    auto_cfg: dict[str, Any],
) -> dict[str, set[str]]:
    out: dict[str, set[str]] = {}
    events = auto_cfg.get("events") or {}
    for event_id in FREEMAN_PILOT_EVENT_ORDER:
        paths: set[str] = set()
        reg_list = normalize_register_notes((events.get(event_id) or {}).get("register_notes"))
        if not reg_list:
            reg_list = normalize_register_notes((thesis.get(event_id) or {}).get("register_notes"))
        for rel in reg_list:
            reg_path = REPO_ROOT / rel
            paths.update(parse_register_capture_paths(reg_path))
        out[event_id] = paths
    return out

def existing_note_keys() -> set[tuple[str, str]]:
    keys: set[tuple[str, str]] = set()
    for note in collect_prediction_notes():
        if note.speaker != FREEMAN_SPEAKER:
            continue
        keys.add((note.source.replace("\\", "/"), note.event_id))
    return keys

def existing_note_dates() -> dict[tuple[str, str], str]:
    """event_id, pub_date -> source of existing note (first wins)."""
    out: dict[tuple[str, str], str] = {}
    for note in sorted(
        collect_prediction_notes(),
        key=lambda n: (n.event_id, n.date_made, n.file),
    ):
        if note.speaker != FREEMAN_SPEAKER:
            continue
        key = (note.event_id, note.date_made)
        out.setdefault(key, note.source.replace("\\", "/"))
    return out

def review_speech_act(body: str, quote: str) -> str | None:
    for hay in (quote, body[:6000]):
        m = REST_RE.search(hay)
        if not m:
            continue
        phrase = m.group(1).casefold()
        if "wrong" in phrase or "misread" in phrase:
            return "self_acknowledged_incorrect"
        if "right" in phrase or "predicted" in phrase:
            return "self_acknowledged_correct"
        return "restated"
    return None

def split_hooks(
    hooks: list[str],
    weak_hooks: list[str] | None,
) -> tuple[list[str], set[str]]:
    weak = {h.casefold() for h in (weak_hooks or [])}
    strong = [h for h in hooks if h.casefold() not in weak]
    return strong, weak

def extract_hook_window(
    hay_body: str,
    hooks: list[str],
    *,
    excludes: list[str],
    trajectory_lemmas: list[str] | None,
    half_window: int = 120,
    max_quote: int = 240,
    weak_hook_set: set[str] | None = None,
) -> tuple[str, float, list[str]]:
    hay_cf = hay_body.casefold()
    weak = weak_hook_set or set()
    ordered_hooks = sorted(
        hooks,
        key=lambda h: (0 if h.casefold() not in weak else 1, -len(h)),
    )
    best = ""
    best_score = 0.0
    matched: list[str] = []
    for hook in ordered_hooks:
        hook_cf = hook.casefold()
        start = 0
        while True:
            idx = hay_cf.find(hook_cf, start)
            if idx < 0:
                break
            chunk_start = max(0, idx - half_window)
            chunk_end = min(len(hay_body), idx + len(hook) + half_window)
            s = hay_body[chunk_start:chunk_end].strip()
            if len(s) < 40:
                start = idx + 1
                continue
            if INTRO_SKIP.search(s[:80]) or HOST_ONLY.search(s[:80]):
                start = idx + 1
                continue
            if excludes and patterns_match(s, excludes):
                start = idx + 1
                continue
            if trajectory_lemmas and not any(lem in s.casefold() for lem in trajectory_lemmas):
                traj_start = max(0, idx - half_window * 3)
                traj_end = min(len(hay_body), idx + len(hook) + half_window * 3)
                traj_slice = hay_body[traj_start:traj_end].casefold()
                if not any(lem in traj_slice for lem in trajectory_lemmas):
                    start = idx + 1
                    continue
            hit_hooks = [h for h in hooks if match_text(s, h)]
            hit_count = len(hit_hooks)
            score = min(1.0, 0.5 + 0.15 * hit_count)
            if weak and hit_hooks and not any(h.casefold() not in weak for h in hit_hooks):
                score = min(score, 0.45)
            if score > best_score:
                best_score = score
                best = s[:max_quote]
                matched = hit_hooks
            start = idx + 1
    return best, best_score, matched

def best_hook_sentence(
    body: str,
    hooks: list[str],
    excludes: list[str],
    trajectory_lemmas: list[str] | None = None,
    weak_hooks: list[str] | None = None,
) -> tuple[str, float, list[str]]:
    hay_body = body_without_frontmatter(body)
    weak_set = {h.casefold() for h in (weak_hooks or [])}
    best = ""
    best_score = 0.0
    matched: list[str] = []
    for sentence in SENTENCE_SPLIT.split(hay_body):
        s = sentence.strip()
        if len(s) < 40 or len(s) > 320:
            continue
        if INTRO_SKIP.search(s) or HOST_ONLY.search(s):
            continue
        if excludes and patterns_match(s, excludes):
            continue
        if trajectory_lemmas and not any(lem in s.casefold() for lem in trajectory_lemmas):
            continue
        hit_hooks = [hook for hook in hooks if match_text(s, hook)]
        hit_count = len(hit_hooks)
        if hit_count == 0:
            continue
        score = min(1.0, 0.5 + 0.15 * hit_count)
        if score > best_score:
            best_score = score
            best = s[:240]
            matched = hit_hooks
    if best_score <= 0:
        best, best_score, matched = extract_hook_window(
            hay_body,
            hooks,
            excludes=excludes,
            trajectory_lemmas=trajectory_lemmas,
            weak_hook_set=weak_set,
        )
    if best_score <= 0:
        return "", 0.0, []
    if weak_set and matched and not any(h.casefold() not in weak_set for h in matched):
        best_score = min(best_score, 0.45)
    return best, best_score, matched

def body_without_frontmatter(text: str) -> str:
    return FRONTMATTER_RE.sub("", text.lstrip("\ufeff"), count=1)

def match_text(haystack: str, pattern: str) -> bool:
    return pattern.casefold() in haystack.casefold()

def canonical_rank(*, source: str, meta: dict[str, Any]) -> tuple[int, str]:
    s = source.replace("\\", "/").casefold()
    note = str(meta.get("source_note") or "").casefold()
    slug = str(meta.get("channel_slug") or "").casefold()
    rank = 0
    if "glenn-diesen" in s or slug == "glenn-diesen":
        rank -= 20
    if "dialogue-works" in s and "mis-attributed" in note:
        rank += 30
    if "judging-freedom" in s:
        rank -= 3
    return (rank, s)

def derive_speech_act_for_note(
    *,
    event_id: str,
    date_made: str,
    stance: str,
    review_act: str | None,
) -> str:
    if review_act in REVIEW_SPEECH_ACTS:
        return review_act
    priors = [
        n
        for n in collect_prediction_notes()
        if n.speaker == FREEMAN_SPEAKER
        and n.event_id == event_id
        and n.date_made < date_made
    ]
    priors.sort(key=lambda n: (n.date_made, n.file))
    if not priors:
        return "initial"
    last = priors[-1]
    if last.stance != stance:
        return "iterated"
    return "restated"

def score_capture_for_event(
    *,
    event_id: str,
    source: str,
    pub_date: str,
    title: str,
    body: str,
    meta: dict[str, Any],
    thesis_cfg: dict[str, Any],
    event_auto_cfg: dict[str, Any],
    auto_cfg: dict[str, Any],
    register_sources: set[str],
) -> ScoredCandidate | None:
    weights = auto_cfg.get("score_weights") or {}
    threshold = float(event_auto_cfg.get("threshold") or auto_cfg.get("default_threshold") or 0.75)
    stance = str(event_auto_cfg.get("default_stance") or "yes")
    title_patterns = list(
        event_auto_cfg.get("title_match_patterns")
        or thesis_cfg.get("title_patterns")
        or []
    )
    excludes = list(thesis_cfg.get("exclude_patterns") or [])
    body_hooks = list(event_auto_cfg.get("body_hooks") or title_patterns)
    weak_hooks = list(event_auto_cfg.get("weak_body_hooks") or [])
    strong_hooks, weak_hook_set = split_hooks(body_hooks, weak_hooks)
    trajectory_lemmas = list(event_auto_cfg.get("trajectory_lemmas") or [])
    early_window = event_auto_cfg.get("early_body_window") or {}

    gate = thesis_cfg.get("close_date_gate")
    if gate and pub_date > str(gate):
        return None

    hay_title = f"{title} {Path(source).name}"
    if patterns_match(hay_title, excludes) or patterns_match(body[:2000], excludes):
        return None

    src_norm = source.replace("\\", "/")
    conflict_patterns = list(event_auto_cfg.get("title_conflict_patterns") or [])
    if conflict_patterns and patterns_match(hay_title, conflict_patterns):
        lane_title = patterns_match(hay_title, title_patterns)
        register_conflict_strict = bool(event_auto_cfg.get("register_conflict_strict"))
        if not lane_title:
            if src_norm not in register_sources:
                return None
            if register_conflict_strict:
                return None

    score = 0.0
    reasons: list[str] = []

    if patterns_match(hay_title, title_patterns):
        score += float(weights.get("title_match", 0.4))
        reasons.append("title_match")

    quote, hook_strength, matched_hooks = best_hook_sentence(
        body,
        body_hooks,
        excludes,
        None
        if (
            src_norm in register_sources
            and bool(event_auto_cfg.get("register_relax_trajectory_hooks"))
        )
        else trajectory_lemmas,
        weak_hooks=weak_hooks,
    )
    strong_hit = any(h.casefold() not in weak_hook_set for h in matched_hooks)
    if hook_strength > 0:
        score += float(weights.get("body_hook", 0.3))
        reasons.append("body_hook")
        if strong_hit:
            reasons.append("strong_body_hook")
        elif matched_hooks:
            reasons.append("weak_body_hook_only")

    review = review_speech_act(body, quote)
    if review:
        score += float(weights.get("restatement_cue", 0.2))
        reasons.append("restatement_cue")

    if trajectory_lemmas and quote:
        src_norm = source.replace("\\", "/")
        traj_in_quote = any(lem in quote.casefold() for lem in trajectory_lemmas)
        register_traj_waiver = bool(event_auto_cfg.get("register_trajectory_waiver", True))
        if register_traj_waiver and bool(event_auto_cfg.get("register_requires_body_hook")):
            register_traj_waiver = False
        if traj_in_quote or (src_norm in register_sources and register_traj_waiver):
            score += float(weights.get("trajectory_cooccur", 0.2))
            reasons.append("trajectory_cooccur")
            if src_norm in register_sources and not traj_in_quote:
                reasons.append("register_trajectory_waiver")

    if source.replace("\\", "/") in register_sources:
        score += float(weights.get("register_capture", 0.15))
        reasons.append("register_capture")

    if not quote and patterns_match(hay_title, title_patterns):
        quote = title.strip()[:240]
        reasons.append("title_quote_fallback")

    if not quote or INTRO_SKIP.search(quote):
        return None

    allow_title_only = bool(event_auto_cfg.get("allow_title_only_filing", True))
    title_only_min = float(
        event_auto_cfg.get("title_only_min_score")
        or float(weights.get("title_match", 0.4)) * 0.95
    )
    if not allow_title_only:
        title_only_min = threshold
    title_only_ok = "title_match" in reasons and score >= title_only_min
    register_requires_body = bool(event_auto_cfg.get("register_requires_body_hook"))
    register_min_hook = float(event_auto_cfg.get("register_min_hook_strength") or 0.5)
    register_ok = "register_capture" in reasons and hook_strength > 0
    if register_requires_body:
        register_ok = register_ok and strong_hit and hook_strength >= register_min_hook
    early_ok = False
    early_strong_hooks = {
        h.casefold() for h in (event_auto_cfg.get("early_strong_hooks") or [])
    }
    if early_window:
        start = str(early_window.get("start") or "")
        end = str(early_window.get("end") or "")
        min_early = float(early_window.get("min_score") or 0.5)
        needs_strong = bool(early_window.get("requires_strong_hook", True))
        if start and end and start <= pub_date <= end:
            early_hook_ok = hook_strength >= min_early and (
                not needs_strong or strong_hit or "register_capture" in reasons
            )
            if early_strong_hooks:
                early_hook_ok = early_hook_ok and any(
                    h.casefold() in early_strong_hooks for h in matched_hooks
                )
            if early_hook_ok:
                early_traj_ok = not trajectory_lemmas or "trajectory_cooccur" in reasons or (
                    bool(event_auto_cfg.get("trajectory_waive_on_title_match"))
                    and "title_match" in reasons
                ) or (
                    src_norm in register_sources
                    and bool(event_auto_cfg.get("register_relax_trajectory_hooks"))
                )
                if early_traj_ok:
                    early_ok = True
                    reasons.append("early_body_window")
    traj_gate_ok = not trajectory_lemmas or "trajectory_cooccur" in reasons or (
        bool(event_auto_cfg.get("trajectory_waive_on_title_match"))
        and "title_match" in reasons
    )
    body_ok = (
        "body_hook" in reasons
        and traj_gate_ok
        and (
            score >= threshold
            or register_ok
            or "restatement_cue" in reasons
            or "title_match" in reasons
            or early_ok
        )
        and "weak_body_hook_only" not in reasons
    )
    threshold_ok = score >= threshold and "weak_body_hook_only" not in reasons
    strict_min = event_auto_cfg.get("strict_filing_min_score")
    if strict_min is not None and score < float(strict_min) and not early_ok:
        return None
    if not (title_only_ok or body_ok or register_ok or threshold_ok):
        return None

    speech_act = derive_speech_act_for_note(
        event_id=event_id,
        date_made=pub_date,
        stance=stance,
        review_act=review if review in REVIEW_SPEECH_ACTS else None,
    )

    yt = youtube_id_from_meta(meta, body)
    rank = canonical_rank(source=source, meta=meta)

    return ScoredCandidate(
        event_id=event_id,
        source=source.replace("\\", "/"),
        pub_date=pub_date,
        score=round(score, 3),
        threshold=threshold,
        quote=quote,
        stance=stance,
        speech_act=speech_act,
        reasons=reasons,
        youtube_id=yt,
        canonical_rank=rank,
    )

def group_key(candidate: ScoredCandidate) -> tuple:
    return (candidate.event_id, candidate.pub_date)

def pick_group_winner(candidates: list[ScoredCandidate]) -> ScoredCandidate:
    return sorted(
        candidates,
        key=lambda c: (-c.score, c.canonical_rank[0], c.canonical_rank[1]),
    )[0]

def collect_auto_file_candidates(
    *,
    auto_cfg: dict[str, Any] | None = None,
    event_id_filter: str | None = None,
    respect_existing: bool = True,
) -> list[ScoredCandidate]:
    auto_cfg = auto_cfg or load_auto_file_config()
    thesis = load_thesis_map()
    register_index = build_register_index(thesis, auto_cfg)
    skip_keys = existing_note_keys() if respect_existing else set()
    skip_dates = existing_note_dates() if respect_existing else {}
    grouped: dict[tuple, list[ScoredCandidate]] = {}

    for pub, path, meta in iter_freeman_captures():
        source = path.relative_to(REPO_ROOT).as_posix()
        title = str(meta.get("title") or path.name)
        body = path.read_text(encoding="utf-8", errors="replace")
        cap_meta = read_capture_meta(path)

        for event_id in FREEMAN_PILOT_EVENT_ORDER:
            if event_id_filter and event_id != event_id_filter:
                continue
            if (source, event_id) in skip_keys:
                continue
            existing_src = skip_dates.get((event_id, pub))
            if existing_src and existing_src != source:
                continue

            event_auto = (auto_cfg.get("events") or {}).get(event_id) or {}
            thesis_cfg = thesis.get(event_id) or {}
            scored = score_capture_for_event(
                event_id=event_id,
                source=source,
                pub_date=pub,
                title=title,
                body=body,
                meta=cap_meta,
                thesis_cfg=thesis_cfg,
                event_auto_cfg=event_auto,
                auto_cfg=auto_cfg,
                register_sources=register_index.get(event_id) or set(),
            )
            if scored is None:
                continue
            grouped.setdefault(group_key(scored), []).append(scored)

    winners: list[ScoredCandidate] = []
    for group in grouped.values():
        winners.append(pick_group_winner(group))
    winners.sort(key=lambda c: (c.event_id, c.pub_date, c.source))
    return winners

def render_auto_file_note(candidate: ScoredCandidate, alias_sources: list[str] | None = None) -> str:
    label = EVENT_LABEL.get(candidate.event_id, candidate.event_id)
    parts = [
        "---",
        "note_type: prediction",
        f"event_id: {candidate.event_id}",
        f"speaker: {FREEMAN_SPEAKER}",
        f"date_made: {candidate.pub_date}",
        f"stance: {candidate.stance}",
        "confidence: high",
        f"source: {candidate.source}",
        f"speech_act: {candidate.speech_act}",
        "auto_file: true",
        f"auto_file_score: {candidate.score}",
        f"status: {_prediction_status(candidate.event_id)}",
        "---",
        "",
        f"# Freeman — {label} ({candidate.pub_date})",
        "",
        "## Quote (audit)",
        "",
        candidate.quote,
        "",
    ]
    if alias_sources:
        yt = f" `{candidate.youtube_id}`" if candidate.youtube_id else ""
        parts.extend(
            [
                "## Tier-3 context (audit — not stance)",
                "",
                f"Auto-file score {candidate.score} ({', '.join(candidate.reasons)}).",
            ]
        )
        for alias in alias_sources:
            parts.append(f"Alias capture (same episode{yt}): `{alias}`.")
        parts.append("")
    return "\n".join(parts).rstrip() + "\n"

def note_path_for(candidate: ScoredCandidate) -> Path:
    slug = EVENT_SLUG.get(candidate.event_id)
    if not slug:
        raise ValueError(f"unknown event_id: {candidate.event_id}")
    return PREDICTIONS_DIR / f"{slug}-freeman-{candidate.pub_date}.md"

def iter_on_disk_auto_file_notes() -> list[Any]:
    notes = []
    for note in collect_prediction_notes():
        if note.speaker != FREEMAN_SPEAKER:
            continue
        text = note.path.read_text(encoding="utf-8", errors="replace")
        if AUTO_FILE_RE.search(text):
            notes.append(note)
    return notes

def prune_stale_auto_file_notes(
    *,
    dry_run: bool = False,
    event_id_filter: str | None = None,
) -> tuple[list[Path], list[ScoredCandidate]]:
    """Remove auto_file notes that the current scorer would not file."""
    auto_cfg = load_auto_file_config()
    winners = collect_auto_file_candidates(
        auto_cfg=auto_cfg,
        event_id_filter=event_id_filter,
        respect_existing=False,
    )
    winner_by_key = {(c.event_id, c.pub_date): c for c in winners}
    pruned: list[Path] = []

    for note in iter_on_disk_auto_file_notes():
        if event_id_filter and note.event_id != event_id_filter:
            continue
        winner = winner_by_key.get((note.event_id, note.date_made))
        src = note.source.replace("\\", "/")
        stale = winner is None or winner.source != src
        if not stale:
            continue
        pruned.append(note.path)
        rel = note.path.relative_to(REPO_ROOT).as_posix()
        if dry_run:
            print(f"[dry-run] prune {rel}")
        else:
            note.path.unlink()
            print(f"[ok] pruned {rel}")

    return pruned, winners

def build_report_payload(candidates: list[ScoredCandidate]) -> dict[str, Any]:
    by_event: dict[str, int] = {}
    for c in candidates:
        by_event[c.event_id] = by_event.get(c.event_id, 0) + 1
    return {
        "_meta": {
            "source": "scripts/auto_materialize_freeman_predictions.py",
            "generated_at": iso_now(),
            "candidate_count": len(candidates),
        },
        "by_event": by_event,
        "candidates": [
            {
                "event_id": c.event_id,
                "pub_date": c.pub_date,
                "source": c.source,
                "score": c.score,
                "threshold": c.threshold,
                "stance": c.stance,
                "speech_act": c.speech_act,
                "reasons": c.reasons,
                "quote_preview": c.quote[:120],
            }
            for c in candidates
        ],
    }
