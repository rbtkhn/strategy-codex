"""Episystem SAL — sole soft alignment authority (claim → event_distribution)."""

from __future__ import annotations

import math
import sys
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SCRIPTS = _REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from voice_prediction_pilot import (  # noqa: E402
    VOICE_REGISTRY,
    get_voice_config,
    load_public_map,
    patterns_match,
)

CAPTURE_MAP_PRIOR = 0.55
MIN_WEIGHT = 0.02

def load_public_maps() -> dict[str, dict[str, dict[str, Any]]]:
    by_voice: dict[str, dict[str, dict[str, Any]]] = {}
    for speaker in sorted(VOICE_REGISTRY.keys()):
        cfg = get_voice_config(speaker)
        if not cfg.public_map_path.is_file():
            continue
        by_voice[speaker] = load_public_map(
            cfg.public_map_path,
            event_order=cfg.pilot_event_order,
        )
    return by_voice

def load_terms_index(
    public_maps: dict[str, dict[str, dict[str, Any]]] | None = None,
) -> dict[str, list[str]]:
    maps = public_maps if public_maps is not None else load_public_maps()
    index: dict[str, list[str]] = {}
    for events in maps.values():
        for event_id, entry in events.items():
            terms = entry.get("prediction_object_terms") or []
            if not isinstance(terms, list):
                continue
            existing = index.setdefault(str(event_id), [])
            for term in terms:
                t = str(term).strip()
                if t and t not in existing:
                    existing.append(t)
    return index

def _term_match_score(claim: str, terms: list[str]) -> float:
    if not terms:
        return 0.0
    hits = sum(1 for term in terms if patterns_match(claim, [str(term)]))
    return hits / len(terms)

def entropy_nats(weights: list[float]) -> float:
    if not weights:
        return 0.0
    total = sum(float(w) for w in weights if float(w) > 0)
    if total <= 0:
        return 0.0
    entropy = 0.0
    for w in weights:
        p = float(w) / total
        if p > 0:
            entropy -= p * math.log(p)
    return round(entropy, 4)

def soft_align(
    claim: str,
    *,
    capture_event_id: str | None,
    terms_index: dict[str, list[str]],
    registry: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], float]:
    """Return event_distribution weights and alignment entropy (nats)."""
    scores: dict[str, float] = {}
    for event_id in sorted(registry.keys()):
        terms = terms_index.get(event_id) or []
        score = _term_match_score(claim, terms)
        if score > 0:
            scores[event_id] = score

    prior_id = str(capture_event_id or "").strip()
    if prior_id and prior_id in registry:
        scores[prior_id] = scores.get(prior_id, 0.0) + CAPTURE_MAP_PRIOR

    if not scores:
        if prior_id and prior_id in registry:
            return [{"event_id": prior_id, "weight": 1.0}], 0.0
        return [], 0.0

    total = sum(scores.values())
    distribution: list[dict[str, Any]] = []
    weights: list[float] = []
    for event_id in sorted(scores.keys()):
        weight = round(scores[event_id] / total, 4)
        if weight >= MIN_WEIGHT:
            distribution.append({"event_id": event_id, "weight": weight})
            weights.append(weight)

    if not distribution and prior_id and prior_id in registry:
        return [{"event_id": prior_id, "weight": 1.0}], 0.0

    return distribution, entropy_nats(weights)
