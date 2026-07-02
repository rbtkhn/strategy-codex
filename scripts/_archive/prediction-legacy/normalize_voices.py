"""PR7 MVEL — cross-voice normalization and alignment scores."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

_SCRIPTS = Path(__file__).resolve().parents[1]
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from prediction.signal_math import clamp01, cosine_similarity  # noqa: E402

MACGREGOR_ENTROPY_DOWNWEIGHT = 0.55
VOICE_WEIGHTS: dict[str, float] = {
    "freeman": 1.0,
    "mercouris": 1.0,
    "macgregor": MACGREGOR_ENTROPY_DOWNWEIGHT,
}

def _semantic_entropy(semantic_scores: dict[str, Any], event_id: str) -> float:
    events = semantic_scores.get("events") if isinstance(semantic_scores, dict) else {}
    if not isinstance(events, dict):
        return 0.0
    block = events.get(event_id) or {}
    if not isinstance(block, dict):
        return 0.0
    return float(block.get("entropy_score") or 0.0)

def _latest_probability_vector(
    trajectories: list[dict[str, Any]],
    event_id: str,
) -> dict[str, float]:
    latest: dict[str, float] = {}
    for traj in trajectories:
        if str(traj.get("event_id") or "") != event_id:
            continue
        voice = str(traj.get("voice") or "")
        points = traj.get("trajectory") or []
        if not voice or not isinstance(points, list) or not points:
            continue
        last = points[-1]
        if isinstance(last, dict):
            latest[voice] = float(last.get("probability") or 0.5)
    return latest

def compute_alignment_score(
    event_id: str,
    trajectories: list[dict[str, Any]],
    *,
    semantic_scores: dict[str, Any] | None = None,
) -> float:
    """Pairwise cosine similarity of [p, 1-p] vectors across voices at an event."""
    probs = _latest_probability_vector(trajectories, event_id)
    if len(probs) < 2:
        return 1.0

    entropy = _semantic_entropy(semantic_scores or {}, event_id)
    voices = sorted(probs.keys())
    vectors: list[list[float]] = []
    weights: list[float] = []
    for voice in voices:
        p = clamp01(probs[voice])
        vectors.append([p, 1.0 - p])
        w = VOICE_WEIGHTS.get(voice, 1.0)
        if voice == "macgregor" and entropy >= 0.85:
            w *= MACGREGOR_ENTROPY_DOWNWEIGHT
        weights.append(w)

    scores: list[float] = []
    pair_weights: list[float] = []
    for i in range(len(vectors)):
        for j in range(i + 1, len(vectors)):
            scores.append(cosine_similarity(vectors[i], vectors[j]))
            pair_weights.append((weights[i] + weights[j]) / 2.0)

    if not scores:
        return 1.0
    total_w = sum(pair_weights) or 1.0
    return round(sum(s * w for s, w in zip(scores, pair_weights)) / total_w, 4)

def entropy_weight(trajectory: list[dict[str, Any]], *, entropy: float) -> float:
    """Weight trajectory points — lower weight when semantic entropy is high."""
    if not trajectory:
        return 0.5
    weight = 1.0 / (1.0 + max(0.0, entropy))
    total = 0.0
    weighted_sum = 0.0
    for point in trajectory:
        if not isinstance(point, dict):
            continue
        conf = float(point.get("confidence") or 0.5)
        p = float(point.get("probability") or 0.5)
        w = weight * conf
        weighted_sum += p * w
        total += w
    if total <= 0:
        return round(float(trajectory[-1].get("probability") or 0.5), 4)
    return round(weighted_sum / total, 4)

def normalize_cross_voice(
    trajectories: list[dict[str, Any]],
    *,
    semantic_scores: dict[str, Any] | None = None,
    disagreement: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Add alignment_score and entropy_weighted_probability per trajectory."""
    _ = disagreement  # reserved for future disagreement-graph hook
    output: list[dict[str, Any]] = []
    for traj in trajectories:
        block = dict(traj)
        event_id = str(block.get("event_id") or "")
        points = block.get("trajectory") or []
        entropy = _semantic_entropy(semantic_scores or {}, event_id)
        block["alignment_score"] = compute_alignment_score(
            event_id,
            trajectories,
            semantic_scores=semantic_scores,
        )
        block["entropy_weighted_probability"] = entropy_weight(
            points if isinstance(points, list) else [],
            entropy=entropy,
        )
        output.append(block)
    return output
