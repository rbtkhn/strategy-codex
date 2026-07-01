"""Temporal scaffolding engine — ordering, grouping, weak trends."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from structuring.normalize import load_observations

from .grouping import group_by_event
from .ordering import assign_time_index
from .trends import compute_trend

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OBSERVATIONS_IN = REPO_ROOT / "statecraft" / "epistemic" / "data" / "observations.json"
DEFAULT_STRUCTURED_IN = REPO_ROOT / "statecraft" / "epistemic" / "data" / "structured_predictions.json"
DEFAULT_TEMPORAL_OUT = REPO_ROOT / "statecraft" / "epistemic" / "data" / "temporal.json"


def load_structured_predictions(*, path: Path | None = None) -> list[dict[str, Any]]:
    structured_path = path or DEFAULT_STRUCTURED_IN
    payload = json.loads(structured_path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return payload
    return list(payload.get("structured_predictions") or [])


def enrich_with_timestamps(
    structured: list[dict[str, Any]],
    observations: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    ts_by_id = {obs["observation_id"]: obs.get("timestamp", "") for obs in observations}
    enriched: list[dict[str, Any]] = []
    for pred in structured:
        copy = dict(pred)
        copy["timestamp"] = ts_by_id.get(pred["observation_id"], "")
        enriched.append(copy)
    return enriched


def build_timeline_entry(pred: dict[str, Any]) -> dict[str, Any]:
    return {
        "voice": pred["voice"],
        "time_index": pred["time_index"],
        "confidence": pred["confidence"],
        "timestamp": pred.get("timestamp") or "",
    }


def ordering_confidence_for_event(preds: list[dict[str, Any]]) -> float:
    if not preds:
        return 0.0
    with_timestamp = sum(1 for pred in preds if pred.get("timestamp"))
    return round(with_timestamp / len(preds), 2)


def build_temporal_view(
    structured: list[dict[str, Any]],
    observations: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    enriched = enrich_with_timestamps(structured, observations)
    indexed = assign_time_index(enriched)
    grouped = group_by_event(indexed)

    temporal_by_event: list[dict[str, Any]] = []
    ordering_scores: list[float] = []

    for event_id in sorted(grouped):
        preds = sorted(grouped[event_id], key=lambda p: int(p.get("time_index", 0)))
        ordering_confidence = ordering_confidence_for_event(preds)
        ordering_scores.append(ordering_confidence)
        temporal_by_event.append(
            {
                "event_id": event_id,
                "timeline": [build_timeline_entry(pred) for pred in preds],
                "trend": compute_trend(preds),
                "ordering_confidence": ordering_confidence,
            }
        )

    summary = {
        "event_count": len(temporal_by_event),
        "ordering_confidence_avg": round(
            sum(ordering_scores) / len(ordering_scores) if ordering_scores else 0.0,
            2,
        ),
    }
    return temporal_by_event, summary


def write_temporal_view(
    temporal_by_event: list[dict[str, Any]],
    summary: dict[str, Any],
    *,
    out_path: Path | None = None,
    structured_path: Path | None = None,
    observations_path: Path | None = None,
) -> Path:
    destination = out_path or DEFAULT_TEMPORAL_OUT
    structured_ref = structured_path or DEFAULT_STRUCTURED_IN
    observations_ref = observations_path or DEFAULT_OBSERVATIONS_IN

    def _label(path: Path) -> str:
        try:
            return path.relative_to(REPO_ROOT).as_posix()
        except ValueError:
            return path.as_posix()

    destination.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "_meta": {
            "generated": True,
            "do_not_edit": True,
            "layer": "temporal",
            "source": "statecraft/epistemic/temporal/temporal_engine.py",
            "row_count": len(temporal_by_event),
            "structured_input": _label(structured_ref),
            "observations_input": _label(observations_ref),
        },
        "temporal_by_event": temporal_by_event,
        "summary": summary,
    }
    destination.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return destination
