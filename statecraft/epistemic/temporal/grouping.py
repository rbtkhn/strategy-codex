"""Group structured predictions by event."""

from __future__ import annotations

from typing import Any

UNMATCHED_EVENT = "unmatched"


def group_by_event(structured_predictions: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    groups: dict[str, list[dict[str, Any]]] = {}
    for pred in structured_predictions:
        event_id = str(pred.get("event_id") or "")
        if not event_id or event_id == UNMATCHED_EVENT:
            continue
        groups.setdefault(event_id, []).append(pred)
    return groups
