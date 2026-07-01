"""Tests for epistemic structuring layer (PR3)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
EPISTEMIC_ROOT = REPO_ROOT / "statecraft" / "epistemic"
FIXTURE_VOICE_DIR = EPISTEMIC_ROOT / "observation" / "voice_captures"
DEFAULT_REGISTRY = REPO_ROOT / "statecraft" / "data" / "event-registry.json"

if str(EPISTEMIC_ROOT) not in sys.path:
    sys.path.insert(0, str(EPISTEMIC_ROOT))

from observation.loader import load_voice_captures  # noqa: E402
from pipeline.run_pipeline import run_all_layers, run_structuring_layer  # noqa: E402
from structuring.event_matcher import match_event, similarity  # noqa: E402
from structuring.normalize import (  # noqa: E402
    load_event_registry,
    normalize_observation,
)
from structuring.schema import STRUCTURED_SCHEMA_KEYS, validate_structured  # noqa: E402
from structuring.stance_classifier import classify_stance  # noqa: E402


def test_classify_stance_high_confidence() -> None:
    stance, confidence = classify_stance("The US will face severe constraints.")
    assert stance == "high_confidence"
    assert confidence == 0.85


def test_classify_stance_medium_and_low() -> None:
    medium_stance, medium_conf = classify_stance("Escalation is likely if forces deploy.")
    low_stance, low_conf = classify_stance("Trade talks may continue without major yield.")
    assert medium_stance == "medium"
    assert medium_conf == 0.65
    assert low_stance == "low"
    assert low_conf == 0.45


def test_similarity_deterministic() -> None:
    left = "China capitulation tariff pressure"
    right = "Will China capitulate to tariff pressure"
    first = similarity(left, right)
    second = similarity(left, right)
    assert first == second
    assert first > 0.0


def test_match_event_top1_tiebreak() -> None:
    registry = {
        "event_b": {"question": "alpha beta gamma"},
        "event_a": {"question": "alpha beta gamma"},
    }
    observation = {
        "raw_text": "alpha beta gamma delta",
        "extracted_sentences": [],
    }
    assert match_event(observation, registry) == "event_a"


def test_match_event_unmatched_when_no_overlap() -> None:
    registry = {
        "event_a": {"question": "quantum computing breakthrough"},
    }
    observation = {
        "raw_text": "naval assets and operational constraints",
        "extracted_sentences": [],
    }
    assert match_event(observation, registry) == "unmatched"


def test_normalize_observation_schema() -> None:
    registry = {
        "event_a": {"question": "US escalation likely leads to operational failure"},
    }
    observation = {
        "observation_id": "obs-1",
        "voice": "macgregor",
        "raw_text": "The US will face severe operational constraints.",
        "extracted_sentences": [
            "The US will face severe operational constraints",
            "Escalation is likely if naval assets are deployed",
        ],
    }
    structured = normalize_observation(observation, registry)
    assert set(structured) == set(STRUCTURED_SCHEMA_KEYS)
    validate_structured(structured)
    assert structured["prediction"].startswith("The US will face severe operational constraints")
    assert structured["stance"] == "high_confidence"


def test_normalize_freeman_fixture_to_china_event() -> None:
    observations = load_voice_captures(voice_dir=FIXTURE_VOICE_DIR, repo_root=REPO_ROOT)
    freeman = next(obs for obs in observations if obs["voice"] == "freeman")
    registry = load_event_registry(path=DEFAULT_REGISTRY)
    structured = normalize_observation(freeman, registry)
    assert structured["event_id"] == "china_tariff_capitulation_2025"
    assert structured["voice"] == "freeman"
    assert structured["source_sentences"]


def test_run_structuring_layer_integration(tmp_path: Path) -> None:
    registry_path = tmp_path / "event-registry.json"
    registry_path.write_text(
        json.dumps(
            {
                "test_event": {
                    "question": "US escalation likely leads to operational failure",
                }
            }
        ),
        encoding="utf-8",
    )
    observations = [
        {
            "observation_id": "obs-1",
            "voice": "macgregor",
            "raw_text": "The US will face severe operational constraints.",
            "extracted_sentences": ["The US will face severe operational constraints"],
        }
    ]
    out_path = tmp_path / "structured_predictions.json"
    structured = run_structuring_layer(
        observations,
        registry_path=registry_path,
        out_path=out_path,
        write=True,
    )
    assert len(structured) == 1
    payload = json.loads(out_path.read_text(encoding="utf-8"))
    assert payload["_meta"]["layer"] == "structuring"
    assert payload["structured_predictions"][0]["event_id"] == "test_event"


def test_pipeline_all_layers(tmp_path: Path) -> None:
    voice_dir = tmp_path / "voice_captures" / "macgregor"
    voice_dir.mkdir(parents=True)
    (voice_dir / "sample.md").write_text(
        "The US will face severe operational constraints. Escalation is likely if naval assets are deployed.",
        encoding="utf-8",
    )
    registry_path = tmp_path / "event-registry.json"
    registry_path.write_text(
        json.dumps(
            {
                "test_event": {
                    "question": "US escalation likely leads to operational failure",
                }
            }
        ),
        encoding="utf-8",
    )
    observations_out = tmp_path / "observations.json"
    structured_out = tmp_path / "structured_predictions.json"

    observations, structured = run_all_layers(
        voice_dir=voice_dir.parent,
        observations_out=observations_out,
        registry_path=registry_path,
        structured_out=structured_out,
        repo_root=tmp_path,
        write=True,
    )

    assert len(observations) == 1
    assert len(structured) == 1
    assert observations_out.is_file()
    assert structured_out.is_file()
    structured_payload = json.loads(structured_out.read_text(encoding="utf-8"))
    assert structured_payload["structured_predictions"][0]["event_id"] == "test_event"
