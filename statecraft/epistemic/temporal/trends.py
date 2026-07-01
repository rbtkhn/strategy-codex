"""Weak directional trend detection over ordered confidence series."""

from __future__ import annotations

from typing import Any


def compute_trend(event_predictions: list[dict[str, Any]]) -> str:
    ordered = sorted(event_predictions, key=lambda p: int(p.get("time_index", 0)))
    confidences = [float(p.get("confidence") or 0.0) for p in ordered]

    if len(confidences) < 2:
        return "stable"

    delta = confidences[-1] - confidences[0]
    if delta > 0.1:
        return "slight_increase"
    if delta < -0.1:
        return "slight_decrease"
    return "stable"
