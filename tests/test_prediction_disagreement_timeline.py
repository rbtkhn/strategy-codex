"""Tests for prediction disagreement and timeline pipeline."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import check_prediction_disagreement as check_disagreement  # noqa: E402
import check_prediction_timeline as check_timeline  # noqa: E402
import prediction_lib as lib  # noqa: E402


def test_disagreement_fixture_values() -> None:
    registry = lib.build_registry_payload()
    payload = lib.build_disagreement_payload(registry)
    block = payload["events"]["russia_odessa_control"]

    pred = block["prediction_level"]
    assert pred["distribution"] == {"yes": 1, "no": 1, "conditional": 1, "uncertain": 0}
    assert pred["disagreement_score_raw"] == 0.6667
    assert pred["disagreement_score_normalized"] == 0.8889

    voice = block["latest_voice_level"]
    assert voice["distribution"] == {"yes": 1, "no": 0, "conditional": 1, "uncertain": 0}
    assert voice["disagreement_score_raw"] == 0.5
    assert voice["disagreement_score_normalized"] == 0.6667


def test_timeline_mercouris_qualification_shift() -> None:
    registry = lib.build_registry_payload()
    payload = lib.build_timeline_payload(registry)
    shifts = payload["events"]["russia_odessa_control"]["shifts"]["mercouris"]
    assert len(shifts) == 1
    shift = shifts[0]
    assert shift["type"] == "qualification_shift"
    assert shift["from"] == "no"
    assert shift["to"] == "conditional"


def test_disagreement_and_timeline_checks_pass_on_repo() -> None:
    assert check_disagreement.run_check() == 0
    assert check_timeline.run_check() == 0
