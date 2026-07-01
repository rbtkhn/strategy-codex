"""Tests for Phase 4.5 signal_math helpers."""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from registry_pipeline.signal_math import (  # noqa: E402
    cosine_similarity,
    detect_step_change,
    drift_vector,
    entropy_stable_high,
    is_monotonic_increasing,
    mean_pairwise_cosine,
)


def test_cosine_similarity_identical() -> None:
    assert cosine_similarity([1.0, 0.0], [1.0, 0.0]) == 1.0


def test_cosine_similarity_orthogonal() -> None:
    assert cosine_similarity([1.0, 0.0], [0.0, 1.0]) == 0.0


def test_drift_vector() -> None:
    assert drift_vector([0.4, 0.5, 0.58, 0.63]) == [0.1, 0.08, 0.05]


def test_monotonic_and_step_change() -> None:
    drift = drift_vector([0.3, 0.45, 0.55, 0.7])
    assert is_monotonic_increasing(drift)
    assert detect_step_change([0.02, 0.18, 0.03])


def test_entropy_stable_high() -> None:
    assert entropy_stable_high([0.7, 0.72, 0.71])
    assert not entropy_stable_high([0.4, 0.5, 0.8])


def test_mean_pairwise_cosine() -> None:
    score = mean_pairwise_cosine([[0.6, 0.4], [0.55, 0.45], [0.5, 0.5]])
    assert 0.9 <= score <= 1.0
