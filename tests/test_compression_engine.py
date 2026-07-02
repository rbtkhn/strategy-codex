"""Tests for Phase 3 compression engine."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from registry_pipeline.compression_engine import compression_report  # noqa: E402
from registry_pipeline.contracts import find_duplicate_fingerprints, predictive_fingerprint  # noqa: E402
from prediction_lib import load_event_registry  # noqa: E402

def test_no_duplicate_fingerprints_in_registry() -> None:
    events = load_event_registry()
    dupes = find_duplicate_fingerprints(events)
    assert not dupes, dupes

def test_israel_trajectory_fingerprint_is_trajectory_type() -> None:
    events = load_event_registry()
    parent = events["israel_self_destruction_trajectory"]
    fp = predictive_fingerprint("israel_self_destruction_trajectory", parent)
    assert fp[0] == "trajectory"
    assert len(fp[-1]) == 6

def test_fingerprint_uses_falsifier_model_conditions() -> None:
    from registry_pipeline.probabilistic_falsifier_engine import infer_falsifier_model

    event_id = "model_fp_row"
    event = {"question": "Iran airpower trajectory?", "tags": ["iran"]}
    model = infer_falsifier_model(event_id, event)
    row = {"question": event["question"], "falsifier_model": model}
    fp = predictive_fingerprint(event_id, row)
    assert fp[2]  # falsifier key non-empty
    assert isinstance(fp[2], tuple)

def test_compression_report_lists_macgregor_merge_proposals() -> None:
    report = compression_report()
    assert report["event_count"] >= 14
    assert isinstance(report["macgregor_merge_proposals"], list)

def test_macgregor_merge_proposals_closed_after_operator_review() -> None:
    report = compression_report()
    source_ids = {p["source_id"] for p in report["macgregor_merge_proposals"]}
    assert "ukraine_western_aid_prolongs_war" not in source_ids
    assert "nato_strategic_exposure_ukraine" not in source_ids
