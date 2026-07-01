"""Deterministic epistemic stance classification from language markers."""

from __future__ import annotations


def classify_stance(text: str) -> tuple[str, float]:
    lowered = text.lower()

    if "will" in lowered or "certain" in lowered:
        return "high_confidence", 0.85

    if "likely" in lowered or "probable" in lowered:
        return "medium", 0.65

    if "possible" in lowered or "may" in lowered:
        return "low", 0.45

    return "uncertain", 0.30
