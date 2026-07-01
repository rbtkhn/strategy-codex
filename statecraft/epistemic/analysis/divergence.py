"""Cross-voice divergence within events."""

from __future__ import annotations

from typing import Any

from .metrics import mean_abs_deviation


def compute_divergence(structured_predictions: list[dict[str, Any]]) -> dict[str, float]:
    by_event: dict[str, list[dict[str, Any]]] = {}
    for pred in structured_predictions:
        event_id = str(pred.get("event_id") or "")
        if not event_id:
            continue
        by_event.setdefault(event_id, []).append(pred)

    divergence: dict[str, float] = {}
    for event_id, preds in by_event.items():
        confidences = [float(p.get("confidence") or 0.0) for p in preds]
        divergence[event_id] = mean_abs_deviation(confidences)
    return divergence
