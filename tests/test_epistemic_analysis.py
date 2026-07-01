"""Tests for epistemic analysis layer (PR4)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
EPISTEMIC_ROOT = REPO_ROOT / "statecraft" / "epistemic"

if str(EPISTEMIC_ROOT) not in sys.path:
    sys.path.insert(0, str(EPISTEMIC_ROOT))

from analysis.divergence import compute_divergence  # noqa: E402
from analysis.drift import compute_voice_drift  # noqa: E402
from analysis.engine import analyze, analyze_all, analyze_event  # noqa: E402
from analysis.metrics import entropy, mean_abs_deviation  # noqa: E402
from analysis.regime import classify_regime  # noqa: E402
from pipeline.run_pipeline import run_all_layers, run_analysis_layer  # noqa: E402

EVENT_A = "event_alpha"
EVENT_B = "event_beta"


def _pred(
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
        "source_sentences": [f"prediction from {voice}"],
    }


def test_entropy_basic() -> None:
    first = entropy([0.5, 0.5])
    second = entropy([0.5, 0.5])
    assert first == second
    assert first >= 0.0


def test_compute_voice_drift_spread() -> None:
    preds = [
        _pred(observation_id="1", voice="macgregor", event_id=EVENT_A, confidence=0.85),
        _pred(observation_id="2", voice="macgregor", event_id=EVENT_A, confidence=0.45),
    ]
    drift = compute_voice_drift(preds)
    assert drift["macgregor"] == pytest.approx(0.4)


def test_compute_divergence_single_voice() -> None:
    preds = [_pred(observation_id="1", voice="macgregor", event_id=EVENT_A, confidence=0.85)]
    divergence = compute_divergence(preds)
    assert divergence[EVENT_A] == 0.0


def test_compute_divergence_multi_voice() -> None:
    preds = [
        _pred(observation_id="1", voice="macgregor", event_id=EVENT_A, confidence=0.85),
        _pred(observation_id="2", voice="freeman", event_id=EVENT_A, confidence=0.45),
    ]
    divergence = compute_divergence(preds)
    assert divergence[EVENT_A] > 0.0
    assert mean_abs_deviation([0.85, 0.45]) == divergence[EVENT_A]


def test_classify_regime_fragmentation() -> None:
    assert classify_regime(0.8, 0.5) == "fragmentation"


def test_classify_regime_stability() -> None:
    assert classify_regime(0.3, 0.1) == "stability"


def test_analyze_event_schema() -> None:
    preds = [
        _pred(observation_id="1", voice="macgregor", event_id=EVENT_A, confidence=0.85),
        _pred(observation_id="2", voice="freeman", event_id=EVENT_A, confidence=0.45),
    ]
    record = analyze_event(EVENT_A, preds)
    assert record["event_id"] == EVENT_A
    assert set(record) == {
        "event_id",
        "voice_drift",
        "cross_voice_divergence",
        "regime_of_discourse",
        "trend",
    }


def test_analyze_global_summary() -> None:
    preds = [
        _pred(observation_id="1", voice="macgregor", event_id=EVENT_A, confidence=0.85),
        _pred(observation_id="2", voice="freeman", event_id=EVENT_A, confidence=0.45),
        _pred(observation_id="3", voice="mercouris", event_id=EVENT_B, confidence=0.55),
    ]
    summary = analyze(preds)
    assert set(summary) == {
        "voice_drift",
        "cross_voice_divergence",
        "regime_of_discourse",
        "trend",
    }


def test_run_analysis_layer_integration(tmp_path: Path) -> None:
    structured_path = tmp_path / "structured_predictions.json"
    structured_path.write_text(
        json.dumps(
            {
                "structured_predictions": [
                    _pred(observation_id="1", voice="macgregor", event_id=EVENT_A, confidence=0.85),
                    _pred(observation_id="2", voice="freeman", event_id=EVENT_A, confidence=0.45),
                ]
            }
        ),
        encoding="utf-8",
    )
    out_path = tmp_path / "analysis.json"
    analysis_by_event, summary = run_analysis_layer(
        structured_path=structured_path,
        out_path=out_path,
        write=True,
    )
    assert len(analysis_by_event) == 1
    assert summary["regime_of_discourse"]
    payload = json.loads(out_path.read_text(encoding="utf-8"))
    assert payload["_meta"]["layer"] == "analysis"
    assert payload["summary"]["voice_drift"]


def test_pipeline_all_layers_includes_analysis(tmp_path: Path) -> None:
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
    analysis_out = tmp_path / "analysis.json"

    observations, structured, analysis_by_event, summary = run_all_layers(
        voice_dir=voice_dir.parent,
        observations_out=observations_out,
        registry_path=registry_path,
        structured_out=structured_out,
        analysis_out=analysis_out,
        repo_root=tmp_path,
        write=True,
    )

    assert len(observations) == 1
    assert len(structured) == 1
    assert len(analysis_by_event) == 1
    assert summary["regime_of_discourse"]
    assert analysis_out.is_file()


def test_analyze_all_skips_unmatched() -> None:
    preds = [
        _pred(observation_id="1", voice="macgregor", event_id="unmatched", confidence=0.85),
        _pred(observation_id="2", voice="freeman", event_id=EVENT_A, confidence=0.45),
    ]
    analysis_by_event, _summary = analyze_all(preds)
    assert len(analysis_by_event) == 1
    assert analysis_by_event[0]["event_id"] == EVENT_A
