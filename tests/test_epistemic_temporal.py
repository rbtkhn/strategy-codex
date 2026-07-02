"""Tests for epistemic temporal scaffolding layer (PR5)."""

from __future__ import annotations

import json

import sys

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

EPISTEMIC_ROOT = REPO_ROOT / "statecraft" / "epistemic"

if str(EPISTEMIC_ROOT) not in sys.path:

    sys.path.insert(0, str(EPISTEMIC_ROOT))

from pipeline.run_pipeline import run_all_layers, run_temporal_layer  # noqa: E402

from temporal.grouping import group_by_event  # noqa: E402

from temporal.ordering import assign_time_index  # noqa: E402

from temporal.temporal_engine import build_temporal_view, enrich_with_timestamps  # noqa: E402

EVENT_A = "event_alpha"

def _structured(

    *,

    observation_id: str,

    voice: str,

    event_id: str,

    confidence: float,

) -> dict:

    return {

        "observation_id": observation_id,

        "voice": voice,

        "event_id": event_id,

        "prediction": f"prediction from {voice}",

        "stance": "medium",

        "confidence": confidence,

        "sentences": [f"prediction from {voice}"],

    }

def _observation(*, observation_id: str, timestamp: str) -> dict:

    return {

        "observation_id": observation_id,

        "voice": "macgregor",

        "source_file": "sample.md",

        "timestamp": timestamp,

        "raw_text": "sample",

        "sentences": [],

    }

def test_assign_time_index_orders_by_timestamp() -> None:

    preds = [

        {"observation_id": "b", "voice": "freeman", "timestamp": "2026-02-01T00:00:00+00:00", "confidence": 0.5},

        {"observation_id": "a", "voice": "macgregor", "timestamp": "2026-01-01T00:00:00+00:00", "confidence": 0.8},

    ]

    indexed = assign_time_index(preds)

    assert indexed[0]["observation_id"] == "a"

    assert indexed[0]["time_index"] == 0

    assert indexed[1]["time_index"] == 1

def test_assign_time_index_tiebreak_voice() -> None:

    preds = [

        {"observation_id": "b", "voice": "mercouris", "timestamp": "2026-01-01T00:00:00+00:00", "confidence": 0.5},

        {"observation_id": "a", "voice": "freeman", "timestamp": "2026-01-01T00:00:00+00:00", "confidence": 0.8},

    ]

    indexed = assign_time_index(preds)

    assert indexed[0]["voice"] == "freeman"

    assert indexed[1]["voice"] == "mercouris"

def test_group_by_event() -> None:

    preds = [

        _structured(observation_id="1", voice="macgregor", event_id=EVENT_A, confidence=0.8),

        _structured(observation_id="2", voice="freeman", event_id="unmatched", confidence=0.5),

    ]

    groups = group_by_event(preds)

    assert EVENT_A in groups

    assert "unmatched" not in groups

    assert len(groups[EVENT_A]) == 1

def test_enrich_with_timestamps_join() -> None:

    structured = [_structured(observation_id="obs-1", voice="macgregor", event_id=EVENT_A, confidence=0.8)]

    observations = [_observation(observation_id="obs-1", timestamp="2026-01-01T00:00:00+00:00")]

    enriched = enrich_with_timestamps(structured, observations)

    assert enriched[0]["timestamp"] == "2026-01-01T00:00:00+00:00"

def test_build_temporal_view_schema() -> None:

    structured = [

        _structured(observation_id="1", voice="macgregor", event_id=EVENT_A, confidence=0.85),

        _structured(observation_id="2", voice="freeman", event_id=EVENT_A, confidence=0.45),

    ]

    observations = [

        _observation(observation_id="1", timestamp="2026-01-01T00:00:00+00:00"),

        _observation(observation_id="2", timestamp="2026-02-01T00:00:00+00:00"),

    ]

    temporal_by_event, summary = build_temporal_view(structured, observations)

    assert len(temporal_by_event) == 1

    record = temporal_by_event[0]

    assert set(record) == {"event_id", "timeline"}

    assert len(record["timeline"]) == 2

    assert set(record["timeline"][0]) == {"voice", "time_index", "confidence", "timestamp"}

    assert summary == {"event_count": 1}

def test_run_temporal_layer_integration(tmp_path: Path) -> None:

    structured_path = tmp_path / "structured_predictions.json"

    observations_path = tmp_path / "observations.json"

    structured_path.write_text(

        json.dumps(

            {

                "structured_predictions": [

                    _structured(observation_id="1", voice="macgregor", event_id=EVENT_A, confidence=0.85),

                    _structured(observation_id="2", voice="freeman", event_id=EVENT_A, confidence=0.45),

                ]

            }

        ),

        encoding="utf-8",

    )

    observations_path.write_text(

        json.dumps(

            {

                "observations": [

                    _observation(observation_id="1", timestamp="2026-01-01T00:00:00+00:00"),

                    _observation(observation_id="2", timestamp="2026-02-01T00:00:00+00:00"),

                ]

            }

        ),

        encoding="utf-8",

    )

    out_path = tmp_path / "temporal.json"

    temporal_by_event, summary = run_temporal_layer(

        structured_path=structured_path,

        observations_path=observations_path,

        out_path=out_path,

        write=True,

    )

    assert len(temporal_by_event) == 1

    assert summary["event_count"] == 1

    payload = json.loads(out_path.read_text(encoding="utf-8"))

    assert payload["_meta"]["layer"] == "temporal"

def test_pipeline_all_layers_includes_temporal(tmp_path: Path) -> None:

    voice_dir = tmp_path / "voice_captures" / "macgregor"

    voice_dir.mkdir(parents=True)

    (voice_dir / "sample.md").write_text(

        "The US will face severe operational constraints. Escalation is likely if naval assets are deployed.",

        encoding="utf-8",

    )

    registry_path = tmp_path / "event-registry.json"

    registry_path.write_text(

        json.dumps({"test_event": {"question": "US escalation likely leads to operational failure"}}),

        encoding="utf-8",

    )

    observations_out = tmp_path / "observations.json"

    structured_out = tmp_path / "structured_predictions.json"

    analysis_out = tmp_path / "analysis.json"

    temporal_out = tmp_path / "temporal.json"

    (

        observations,

        structured,

        analysis_by_event,

        analysis_summary,

        temporal_by_event,

        temporal_summary,

    ) = run_all_layers(

        voice_dir=voice_dir.parent,

        observations_out=observations_out,

        registry_path=registry_path,

        structured_out=structured_out,

        analysis_out=analysis_out,

        temporal_out=temporal_out,

        repo_root=tmp_path,

        write=True,

    )

    assert len(observations) == 1

    assert len(structured) == 1

    assert len(analysis_by_event) == 1

    assert "cross_voice_divergence" in analysis_summary

    assert len(temporal_by_event) == 1

    assert temporal_summary["event_count"] == 1

    assert temporal_out.is_file()

def test_structured_artifact_unchanged(tmp_path: Path) -> None:

    structured_path = tmp_path / "structured_predictions.json"

    observations_path = tmp_path / "observations.json"

    original = {

        "structured_predictions": [

            _structured(observation_id="1", voice="macgregor", event_id=EVENT_A, confidence=0.85),

        ]

    }

    structured_path.write_text(json.dumps(original), encoding="utf-8")

    before = structured_path.read_bytes()

    observations_path.write_text(

        json.dumps({"observations": [_observation(observation_id="1", timestamp="2026-01-01T00:00:00+00:00")]}),

        encoding="utf-8",

    )

    run_temporal_layer(

        structured_path=structured_path,

        observations_path=observations_path,

        out_path=tmp_path / "temporal.json",

        write=True,

    )

    after = structured_path.read_bytes()

    assert before == after

