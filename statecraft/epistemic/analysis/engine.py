"""Main analysis engine — cross-sectional divergence and voice spread."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .divergence import compute_divergence
from .spread import compute_voice_spread

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_STRUCTURED_IN = REPO_ROOT / "statecraft" / "epistemic" / "data" / "structured_predictions.json"
DEFAULT_ANALYSIS_OUT = REPO_ROOT / "statecraft" / "epistemic" / "data" / "analysis.json"

UNMATCHED_EVENT = "unmatched"

def load_structured_predictions(*, path: Path | None = None) -> list[dict[str, Any]]:
    structured_path = path or DEFAULT_STRUCTURED_IN
    payload = json.loads(structured_path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return payload
    return list(payload.get("structured_predictions") or [])

def analyze_event(event_id: str, preds: list[dict[str, Any]]) -> dict[str, Any]:
    voice_spread = compute_voice_spread(preds, event_id=event_id)
    divergence_map = compute_divergence(preds)
    cross_voice_divergence = divergence_map.get(event_id, 0.0)
    return {
        "event_id": event_id,
        "cross_voice_divergence": cross_voice_divergence,
        "voice_spread": voice_spread,
    }

def analyze(structured_predictions: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "voice_spread": compute_voice_spread(structured_predictions),
        "cross_voice_divergence": compute_divergence(structured_predictions),
    }

def analyze_all(
    structured_predictions: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    by_event: dict[str, list[dict[str, Any]]] = {}
    for pred in structured_predictions:
        event_id = str(pred.get("event_id") or "")
        if not event_id or event_id == UNMATCHED_EVENT:
            continue
        by_event.setdefault(event_id, []).append(pred)

    analysis_by_event = [
        analyze_event(event_id, by_event[event_id]) for event_id in sorted(by_event)
    ]
    summary = analyze(structured_predictions)
    return analysis_by_event, summary

def write_analysis(
    analysis_by_event: list[dict[str, Any]],
    summary: dict[str, Any],
    *,
    out_path: Path | None = None,
    structured_path: Path | None = None,
) -> Path:
    destination = out_path or DEFAULT_ANALYSIS_OUT
    structured_ref = structured_path or DEFAULT_STRUCTURED_IN
    try:
        structured_label = structured_ref.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        structured_label = structured_ref.as_posix()

    destination.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "_meta": {
            "generated": True,
            "do_not_edit": True,
            "layer": "analysis",
            "source": "statecraft/epistemic/analysis/engine.py",
            "row_count": len(analysis_by_event),
            "structured_input": structured_label,
        },
        "analysis_by_event": analysis_by_event,
        "summary": summary,
    }
    destination.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return destination
