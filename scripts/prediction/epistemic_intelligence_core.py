"""PR8 Epistemic Intelligence Core — unified SAL + signals + regimes (read-only advisory)."""

from __future__ import annotations

import math
import sys
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SCRIPTS = _REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from prediction.align_events import _load_public_maps, _terms_index  # noqa: E402
from prediction.signal_math import clamp01  # noqa: E402
from prediction_lib import load_event_registry  # noqa: E402
from voice_prediction_pilot import patterns_match  # noqa: E402

CAPTURE_MAP_PRIOR = 0.55
MIN_WEIGHT = 0.02
MACGREGOR_ENTROPY_THRESHOLD = 0.85
MACGREGOR_VOLatility_DAMP = 0.45

REGIME_LABELS = frozenset(
    {"escalation", "stabilization", "fragmentation", "convergence", "transition"}
)


def _term_match_score(claim: str, terms: list[str]) -> float:
    if not terms:
        return 0.0
    hits = sum(1 for term in terms if patterns_match(claim, [str(term)]))
    return hits / len(terms)


def _entropy_nats(weights: list[float]) -> float:
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

    return distribution, _entropy_nats(weights)


def _trajectory_index(
    trajectories: list[dict[str, Any]],
) -> dict[tuple[str, str], list[dict[str, Any]]]:
    index: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for block in trajectories:
        event_id = str(block.get("event_id") or "")
        voice = str(block.get("voice") or "")
        points = block.get("trajectory") or []
        if event_id and voice and isinstance(points, list):
            index[(event_id, voice)] = [p for p in points if isinstance(p, dict)]
    return index


def _point_at_or_before(points: list[dict[str, Any]], timestamp: str) -> dict[str, Any] | None:
    if not points:
        return None
    ts = str(timestamp or "")
    eligible = [p for p in points if str(p.get("timestamp") or "") <= ts] if ts else points
    if not eligible:
        return points[0]
    return sorted(eligible, key=lambda p: str(p.get("timestamp") or ""))[-1]


def project_trajectories(
    event_distribution: list[dict[str, Any]],
    trajectories: list[dict[str, Any]],
    claim_meta: dict[str, Any],
) -> list[dict[str, Any]]:
    """Project distributional mass onto MVEL trajectory points."""
    index = _trajectory_index(trajectories)
    voice = str(claim_meta.get("voice") or "")
    timestamp = str(claim_meta.get("timestamp") or "")
    projections: list[dict[str, Any]] = []

    for entry in event_distribution:
        event_id = str(entry.get("event_id") or "")
        weight = float(entry.get("weight") or 0.0)
        if not event_id or weight <= 0:
            continue
        points = index.get((event_id, voice)) or []
        point = _point_at_or_before(points, timestamp)
        if not point:
            continue
        projections.append(
            {
                "event_id": event_id,
                "weight": round(weight, 4),
                "probability": float(point.get("probability") or 0.5),
                "stance": str(point.get("stance") or "uncertain"),
                "confidence": float(point.get("confidence") or 0.5),
            }
        )
    return projections


def compute_distributional_signals(
    projections: list[dict[str, Any]],
    *,
    trajectories: list[dict[str, Any]],
    voice: str,
    primary_event_id: str | None,
    semantic_entropy: float = 0.0,
) -> dict[str, float]:
    if not projections:
        return {"directional": 0.5, "volatility": 0.0, "drift": 0.0}

    directional = sum(float(p["weight"]) * float(p["probability"]) for p in projections)

    top_event = primary_event_id or str(projections[0].get("event_id") or "")
    index = _trajectory_index(trajectories)
    top_points = index.get((top_event, voice)) or []
    probs = [float(p.get("probability") or 0.5) for p in top_points]
    if len(probs) >= 2:
        mean_p = sum(probs) / len(probs)
        variance = sum((p - mean_p) ** 2 for p in probs) / len(probs)
        volatility = math.sqrt(variance)
    else:
        volatility = 0.0

    if voice == "macgregor" and semantic_entropy >= MACGREGOR_ENTROPY_THRESHOLD:
        volatility *= MACGREGOR_VOLatility_DAMP

    drift = 0.0
    if len(probs) >= 2:
        drift = abs(probs[-1] - probs[-2])

    return {
        "directional": round(clamp01(directional), 4),
        "volatility": round(clamp01(volatility), 4),
        "drift": round(clamp01(drift), 4),
    }


def classify_regime(
    signals: dict[str, float],
    event_distribution: list[dict[str, Any]],
    alignment_entropy: float,
    *,
    projections: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    directional = float(signals.get("directional") or 0.5)
    drift = float(signals.get("drift") or 0.0)

    label = "transition"
    confidence = 0.55

    if alignment_entropy > 1.2 and directional < 0.55:
        label = "fragmentation"
        confidence = 0.65 + min(0.2, alignment_entropy / 10.0)
    elif directional > 0.65 and drift > 0.05:
        label = "escalation"
        confidence = 0.6 + min(0.25, drift)
    elif drift < 0.08 and alignment_entropy < 0.8:
        label = "stabilization"
        confidence = 0.7
    elif projections and len(event_distribution) >= 2:
        stances = {str(p.get("stance") or "") for p in projections}
        if len(stances) == 1 and stances <= {"yes", "no"}:
            label = "convergence"
            confidence = 0.68

    return {
        "label": label if label in REGIME_LABELS else "transition",
        "confidence": round(clamp01(confidence), 4),
    }


def _primary_event_id(event_distribution: list[dict[str, Any]]) -> str | None:
    if not event_distribution:
        return None
    best = max(event_distribution, key=lambda e: float(e.get("weight") or 0.0))
    return str(best.get("event_id") or "") or None


def _semantic_entropy(semantic_scores: dict[str, Any], event_id: str | None) -> float:
    if not event_id:
        return 0.0
    events = semantic_scores.get("events") if isinstance(semantic_scores, dict) else {}
    if not isinstance(events, dict):
        return 0.0
    block = events.get(event_id) or {}
    if not isinstance(block, dict):
        return 0.0
    return float(block.get("entropy_score") or 0.0)


def build_epistemic_object(
    point: dict[str, Any],
    *,
    trajectories: list[dict[str, Any]],
    terms_index: dict[str, list[str]],
    registry: dict[str, dict[str, Any]],
    semantic_scores: dict[str, Any],
    capture_event_id: str,
) -> dict[str, Any]:
    claim = str(point.get("claim") or "")
    voice = str(point.get("voice") or "")
    timestamp = str(point.get("timestamp") or "")
    capture = str(point.get("capture") or "")

    event_distribution, alignment_entropy = soft_align(
        claim,
        capture_event_id=capture_event_id,
        terms_index=terms_index,
        registry=registry,
    )
    primary = _primary_event_id(event_distribution)
    claim_meta = {"voice": voice, "timestamp": timestamp}
    projections = project_trajectories(event_distribution, trajectories, claim_meta)
    sem_ent = _semantic_entropy(semantic_scores, primary)
    trajectory_signals = compute_distributional_signals(
        projections,
        trajectories=trajectories,
        voice=voice,
        primary_event_id=primary,
        semantic_entropy=sem_ent,
    )
    regime = classify_regime(
        trajectory_signals,
        event_distribution,
        alignment_entropy,
        projections=projections,
    )

    return {
        "voice": voice,
        "timestamp": timestamp,
        "capture": capture,
        "claim": claim,
        "interpretation": "unified_epistemic_state",
        "event_distribution": event_distribution,
        "trajectory_signals": trajectory_signals,
        "regime": regime,
        "alignment_entropy": alignment_entropy,
        "primary_event_id": primary,
    }


def iter_mvel_claim_points(mvel_dataset: dict[str, Any]) -> list[dict[str, Any]]:
    """Flatten MVEL trajectories into claim points with parent event_id."""
    points: list[dict[str, Any]] = []
    trajectories = mvel_dataset.get("trajectories") or []
    if not isinstance(trajectories, list):
        return points
    for block in trajectories:
        if not isinstance(block, dict):
            continue
        event_id = str(block.get("event_id") or "")
        voice = str(block.get("voice") or "")
        for point in block.get("trajectory") or []:
            if not isinstance(point, dict):
                continue
            row = dict(point)
            row["voice"] = voice
            row["_capture_event_id"] = event_id
            points.append(row)
    points.sort(
        key=lambda p: (
            str(p.get("voice") or ""),
            str(p.get("_capture_event_id") or ""),
            str(p.get("timestamp") or ""),
            str(p.get("capture") or ""),
        )
    )
    return points


def rollup_events(objects: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate claim objects by primary_event_id (diagnostic rollup)."""
    by_event: dict[str, list[dict[str, Any]]] = {}
    for obj in objects:
        eid = str(obj.get("primary_event_id") or "")
        if not eid:
            continue
        by_event.setdefault(eid, []).append(obj)

    events: dict[str, Any] = {}
    for event_id in sorted(by_event.keys()):
        rows = by_event[event_id]
        directionals = [float(r["trajectory_signals"]["directional"]) for r in rows]
        entropies = [float(r.get("alignment_entropy") or 0.0) for r in rows]
        regimes: dict[str, int] = {}
        for r in rows:
            label = str((r.get("regime") or {}).get("label") or "transition")
            regimes[label] = regimes.get(label, 0) + 1
        dominant_regime = max(regimes.items(), key=lambda kv: kv[1])[0] if regimes else "transition"
        events[event_id] = {
            "object_count": len(rows),
            "mean_directional": round(sum(directionals) / len(directionals), 4),
            "mean_alignment_entropy": round(sum(entropies) / len(entropies), 4),
            "dominant_regime": dominant_regime,
            "regime_counts": regimes,
        }

    return {
        "_meta": {
            "generated": True,
            "do_not_edit": True,
            "source": "scripts/build_epistemic_intelligence_core.py",
            "phase": "pr8-eic-advisory",
            "eic_source": "heuristic_v1",
            "interpretation_note": "diagnostic rollup — not wired to PR3–PR6 in v1",
        },
        "interpretation": "epistemic_intelligence_events",
        "events": events,
    }


def build_eic_payload(
    *,
    mvel_dataset: dict[str, Any] | None = None,
    registry: dict[str, dict[str, Any]] | None = None,
    semantic_scores: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build EIC core payload and event rollup."""
    reg = registry if registry is not None else load_event_registry()
    mvel = mvel_dataset if mvel_dataset is not None else {}
    semantic = semantic_scores or {}
    trajectories = mvel.get("trajectories") if isinstance(mvel, dict) else []
    if not isinstance(trajectories, list):
        trajectories = []

    public_maps = _load_public_maps()
    terms_index = _terms_index(public_maps)

    objects: list[dict[str, Any]] = []
    for point in iter_mvel_claim_points(mvel if isinstance(mvel, dict) else {}):
        capture_event_id = str(point.get("_capture_event_id") or "")
        obj = build_epistemic_object(
            point,
            trajectories=trajectories,
            terms_index=terms_index,
            registry=reg,
            semantic_scores=semantic,
            capture_event_id=capture_event_id,
        )
        objects.append(obj)

    high_entropy_count = sum(1 for o in objects if float(o.get("alignment_entropy") or 0.0) > 1.2)

    core = {
        "_meta": {
            "generated": True,
            "do_not_edit": True,
            "source": "scripts/build_epistemic_intelligence_core.py",
            "phase": "pr8-eic-advisory",
            "eic_source": "heuristic_v1",
            "registry_mutation": False,
            "object_count": len(objects),
            "high_entropy_object_count": high_entropy_count,
        },
        "interpretation": "epistemic_intelligence_core",
        "objects": objects,
    }
    rollup = rollup_events(objects)
    return {"core": core, "events_rollup": rollup, "object_count": len(objects)}
