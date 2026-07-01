"""Voice confidence drift (spread) over structured predictions."""

from __future__ import annotations

from typing import Any


def compute_voice_drift(
    structured_predictions: list[dict[str, Any]],
    *,
    event_id: str | None = None,
) -> dict[str, float]:
    preds = structured_predictions
    if event_id is not None:
        preds = [p for p in preds if p.get("event_id") == event_id]

    grouped: dict[str, list[float]] = {}
    for pred in preds:
        voice = str(pred.get("voice") or "")
        if not voice:
            continue
        grouped.setdefault(voice, []).append(float(pred.get("confidence") or 0.0))

    drift: dict[str, float] = {}
    for voice, confidences in grouped.items():
        if len(confidences) < 2:
            drift[voice] = 0.0
        else:
            drift[voice] = max(confidences) - min(confidences)
    return drift
