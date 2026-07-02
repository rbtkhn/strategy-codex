"""Normalize observation objects into structured prediction records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .event_matcher import match_event
from .schema import validate_structured
from .stance_classifier import classify_stance

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_REGISTRY = REPO_ROOT / "statecraft" / "data" / "event-registry.json"
DEFAULT_OBSERVATIONS_IN = REPO_ROOT / "statecraft" / "epistemic" / "data" / "observations.json"
DEFAULT_STRUCTURED_OUT = REPO_ROOT / "statecraft" / "epistemic" / "data" / "structured_predictions.json"

def load_event_registry(*, path: Path | None = None) -> dict[str, dict[str, Any]]:
    registry_path = path or DEFAULT_REGISTRY
    return json.loads(registry_path.read_text(encoding="utf-8"))

def load_observations(*, path: Path | None = None) -> list[dict[str, Any]]:
    observations_path = path or DEFAULT_OBSERVATIONS_IN
    payload = json.loads(observations_path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return payload
    return list(payload.get("observations") or [])

def extract_prediction(obs: dict[str, Any]) -> str:
    sentences = obs.get("sentences") or []
    if sentences:
        return " ".join(str(sentence) for sentence in sentences)
    return str(obs.get("raw_text") or "").strip()

def normalize_observation(
    obs: dict[str, Any],
    event_registry: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    event_id = match_event(obs, event_registry)
    stance, confidence = classify_stance(str(obs.get("raw_text") or ""))
    sentences = list(obs.get("sentences") or [])
    prediction = extract_prediction(obs)

    structured = {
        "observation_id": obs["observation_id"],
        "voice": obs["voice"],
        "event_id": event_id,
        "prediction": prediction,
        "stance": stance,
        "confidence": confidence,
        "sentences": sentences,
    }
    validate_structured(structured)
    return structured

def normalize_observations(
    observations: list[dict[str, Any]],
    event_registry: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    return [normalize_observation(obs, event_registry) for obs in observations]

def write_structured_predictions(
    structured: list[dict[str, Any]],
    *,
    out_path: Path | None = None,
    registry_path: Path | None = None,
) -> Path:
    destination = out_path or DEFAULT_STRUCTURED_OUT
    registry_ref = registry_path or DEFAULT_REGISTRY
    try:
        registry_label = registry_ref.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        registry_label = registry_ref.as_posix()

    destination.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "_meta": {
            "generated": True,
            "do_not_edit": True,
            "layer": "structuring",
            "source": "statecraft/epistemic/structuring/normalize.py",
            "row_count": len(structured),
            "event_registry": registry_label,
        },
        "structured_predictions": structured,
    }
    destination.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return destination
