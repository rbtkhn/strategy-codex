"""Regime-of-discourse classification (meta-pattern, not geopolitical regime)."""

from __future__ import annotations


def classify_regime(divergence_score: float, drift_score: float) -> str:
    if divergence_score > 0.7:
        return "fragmentation"

    if drift_score < 0.2:
        return "stability"

    if drift_score > 0.6 and divergence_score > 0.5:
        return "transition"

    return "convergence"
