"""Tests for PR5 baseline forecast models."""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from prediction.baseline_models import (  # noqa: E402
    build_baseline_payload,
    expected_calibration_error,
    fit_logistic_trend,
    fit_train_prior,
    predict_bayesian,
    predict_persistence,
    predict_regime_persistence,
    probability_rows,
    regime_f1,
    score_probability_lane,
)


def _row(
    *,
    outcome: str | None = "no",
    censored: bool = False,
    p_t: float = 0.4,
    engm: float = 0.6,
    stances: list[tuple[str, str]] | None = None,
    regime_shift: str = "no_shift",
    anchor: str = "2025-01-10",
    event_id: str = "evt_a",
) -> dict:
    observations = [
        {"voice": voice, "stance": stance, "claim": f"{voice}:{stance}"}
        for voice, stance in (stances if stances is not None else [("freeman", "no")])
    ]
    return {
        "event_id": event_id,
        "anchor_date": anchor,
        "split": "train",
        "voice_observations": observations,
        "latent_features": {
            "event_probability": engm,
            "signal_vector": [0.35, 1.0, 0.4, 1.0 if regime_shift == "shift" else 0.0, 0.0],
        },
        "task_labels": {
            "regime_shift": regime_shift,
            "delta": {"p_t": p_t, "p_future": p_t},
        },
        "outcome": outcome,
        "outcome_censored": censored,
    }


def test_predict_persistence_uses_p_t() -> None:
    row = _row(p_t=0.44, engm=0.57)
    assert predict_persistence(row) == 0.44


def test_bayesian_posterior_with_no_stances() -> None:
    row = _row(stances=[])
    assert predict_bayesian(row, alpha=1.0, beta=3.0) == 0.25


def test_fit_train_prior_smoothing() -> None:
    train = [_row(outcome="no"), _row(outcome="yes", event_id="evt_b", anchor="2025-02-01")]
    alpha, beta = fit_train_prior(train)
    assert alpha == 2.0
    assert beta == 2.0


def test_probability_rows_excludes_censored() -> None:
    rows = [_row(censored=True, outcome=None), _row(outcome="no")]
    assert len(probability_rows(rows)) == 1


def test_score_probability_lane() -> None:
    rows = [_row(outcome="no", p_t=0.4), _row(outcome="no", p_t=0.4, anchor="2025-02-01")]
    preds = [0.4, 0.4]
    metrics = score_probability_lane(preds, rows)
    assert metrics["n_probability"] == 2
    assert metrics["brier"] == 0.16
    assert metrics["accuracy"] == 1.0


def test_regime_f1_with_shift_class() -> None:
    preds = ["shift", "no_shift", "no_shift"]
    labels = ["shift", "shift", "no_shift"]
    block = regime_f1(preds, labels)
    assert block["precision"] == 1.0
    assert block["recall"] == 0.5
    assert block["support"] == 2


def test_expected_calibration_error() -> None:
    preds = [0.1 * i for i in range(1, 11)]
    labels = [0.0] * 10
    ece = expected_calibration_error(preds, labels, bins=10)
    assert ece is not None
    assert ece >= 0.0


def test_fit_logistic_trend_requires_min_train() -> None:
    train = [_row(outcome="no"), _row(outcome="no", anchor="2025-02-01")]
    assert fit_logistic_trend(train, events={"evt_a": {"start_date": "2025-01-01"}}) is None


def test_build_baseline_payload_shape() -> None:
    dataset = {
        "_meta": {"split_date": "2026-01-01"},
        "train": [
            _row(outcome="no", anchor="2025-01-10"),
            _row(outcome="no", anchor="2025-02-01"),
            _row(outcome="yes", anchor="2025-03-01", stances=[("freeman", "yes")]),
        ],
        "test": [
            _row(outcome="no", anchor="2026-02-01", regime_shift="shift"),
            _row(outcome=None, anchor="2026-03-01", regime_shift="no_shift", censored=True),
        ],
    }
    payload = build_baseline_payload(dataset, registry={"evt_a": {"start_date": "2025-01-01"}})
    assert payload["interpretation"] == "baseline_evaluation"
    assert payload["system_reference"] == "engm_event_probability"
    assert "persistence" in payload["baselines"]
    assert payload["baselines"]["transformer"]["status"] == "deferred_pr5b"
    assert "test" in payload["baselines"]["persistence"]
    assert payload["comparison"]["test"]["brier_delta_vs_persistence"] is not None


def test_predict_regime_persistence_from_signal() -> None:
    row = _row(regime_shift="shift")
    assert predict_regime_persistence(row) == "shift"
