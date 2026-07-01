"""Main analysis engine — drift, divergence, regime-of-discourse."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .divergence import compute_divergence
from .drift import compute_voice_drift
from .regime import classify_regime

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


def trend_label(divergence_score: float) -> str:
    if divergence_score > 0.6:
        return "increasing disagreement over time"
    return "stable discourse"


def analyze_event(event_id: str, preds: list[dict[str, Any]]) -> dict[str, Any]:
    voice_drift = compute_voice_drift(preds, event_id=event_id)
    divergence_map = compute_divergence(preds)
    cross_voice_divergence = divergence_map.get(event_id, 0.0)
    avg_drift = sum(voice_drift.values()) / len(voice_drift) if voice_drift else 0.0
    regime = classify_regime(cross_voice_divergence, avg_drift)
    return {
        "event_id": event_id,
        "voice_drift": voice_drift,
        "cross_voice_divergence": cross_voice_divergence,
        "regime_of_discourse": regime,
        "trend": trend_label(cross_voice_divergence),
    }


def analyze(structured_predictions: list[dict[str, Any]]) -> dict[str, Any]:
    drift = compute_voice_drift(structured_predictions)
    divergence = compute_divergence(structured_predictions)

    avg_divergence = sum(divergence.values()) / len(divergence) if divergence else 0.0
    avg_drift = sum(drift.values()) / len(drift) if drift else 0.0
    regime = classify_regime(avg_divergence, avg_drift)

    return {
        "voice_drift": drift,
        "cross_voice_divergence": avg_divergence,
        "regime_of_discourse": regime,
        "trend": trend_label(avg_divergence),
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
