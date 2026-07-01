"""Stdlib math helpers for Phase 4.5 signal extraction."""

from __future__ import annotations

import math
from typing import Sequence


def cosine_similarity(v1: Sequence[float], v2: Sequence[float]) -> float:
    if len(v1) != len(v2) or not v1:
        return 0.0
    dot = sum(float(a) * float(b) for a, b in zip(v1, v2))
    norm1 = math.sqrt(sum(float(a) * float(a) for a in v1))
    norm2 = math.sqrt(sum(float(b) * float(b) for b in v2))
    if norm1 <= 0 or norm2 <= 0:
        return 0.0
    return max(0.0, min(1.0, dot / (norm1 * norm2)))


def drift_vector(series: Sequence[float]) -> list[float]:
    values = [float(v) for v in series]
    if len(values) < 2:
        return []
    return [round(values[i] - values[i - 1], 4) for i in range(1, len(values))]


def is_monotonic_increasing(drift: Sequence[float], *, min_steps: int = 2) -> bool:
    if len(drift) < min_steps:
        return False
    return all(float(d) >= 0 for d in drift)


def is_monotonic_decreasing(drift: Sequence[float], *, min_steps: int = 2) -> bool:
    if len(drift) < min_steps:
        return False
    return all(float(d) <= 0 for d in drift)


def detect_step_change(drift: Sequence[float], *, threshold: float = 0.15) -> bool:
    return any(abs(float(d)) >= threshold for d in drift)


def entropy_stable_high(
    entropy_series: Sequence[float],
    *,
    window: int = 3,
    min_entropy: float = 0.65,
    max_delta: float = 0.05,
) -> bool:
    values = [float(v) for v in entropy_series]
    if len(values) < window:
        return False
    tail = values[-window:]
    if max(tail) < min_entropy:
        return False
    return max(tail) - min(tail) <= max_delta


def mean_pairwise_cosine(vectors: list[list[float]]) -> float:
    if len(vectors) < 2:
        return 1.0 if vectors else 0.0
    scores: list[float] = []
    for i in range(len(vectors)):
        for j in range(i + 1, len(vectors)):
            scores.append(cosine_similarity(vectors[i], vectors[j]))
    return round(sum(scores) / len(scores), 4) if scores else 0.0


def clamp01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))
