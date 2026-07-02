"""PR5 baseline forecast evaluation — advisory comparison vs ENGM (read-only, stdlib)."""

from __future__ import annotations

import math
import sys
from datetime import date
from pathlib import Path
from typing import Any, Callable

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SCRIPTS = _REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from prediction.epistemic_loss import brier_score, outcome_to_label  # noqa: E402
from prediction.signal_math import clamp01  # noqa: E402

LOW_N_PROBABILITY_THRESHOLD = 5
LOW_N_SHIFT_SUPPORT_THRESHOLD = 1
LOGISTIC_MIN_TRAIN_N = 3
ECE_BINS = 10
REGIME_SHIFT_INDEX = 3

def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(str(value)[:10])
    except ValueError:
        return None

def _days_between(start: date, end: date) -> int:
    return max(0, (end - start).days)

def probability_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        row
        for row in rows
        if not row.get("outcome_censored") and row.get("outcome") in {"yes", "no"}
    ]

def row_label(row: dict[str, Any]) -> float | None:
    return outcome_to_label(str(row.get("outcome") or ""))

def predict_persistence(row: dict[str, Any]) -> float:
    delta = row.get("task_labels") or {}
    if isinstance(delta, dict):
        block = delta.get("delta")
        if isinstance(block, dict) and block.get("p_t") is not None:
            return clamp01(float(block["p_t"]))
    latent = row.get("latent_features") or {}
    if isinstance(latent, dict) and latent.get("event_probability") is not None:
        return clamp01(float(latent["event_probability"]))
    return 0.5

def predict_system(row: dict[str, Any]) -> float:
    latent = row.get("latent_features") or {}
    if isinstance(latent, dict) and latent.get("event_probability") is not None:
        return clamp01(float(latent["event_probability"]))
    return 0.5

def fit_train_prior(train_rows: list[dict[str, Any]]) -> tuple[float, float]:
    scored = probability_rows(train_rows)
    yes_count = sum(1 for row in scored if row.get("outcome") == "yes")
    no_count = sum(1 for row in scored if row.get("outcome") == "no")
    if not scored:
        return 1.0, 1.0
    return 1.0 + float(yes_count), 1.0 + float(no_count)

def predict_bayesian(row: dict[str, Any], *, alpha: float, beta: float) -> float:
    a = float(alpha)
    b = float(beta)
    for obs in row.get("voice_observations") or []:
        if not isinstance(obs, dict):
            continue
        stance = str(obs.get("stance") or "")
        if stance == "yes":
            a += 1.0
        elif stance == "no":
            b += 1.0
    if a + b <= 0:
        return 0.5
    return round(clamp01(a / (a + b)), 4)

def _event_time_origin(event_id: str, events: dict[str, Any], train_rows: list[dict[str, Any]]) -> date | None:
    event = events.get(event_id) if isinstance(events, dict) else None
    if isinstance(event, dict):
        start = _parse_date(str(event.get("start_date") or ""))
        if start:
            return start
    anchors = [
        _parse_date(str(row.get("anchor_date") or ""))
        for row in train_rows
        if row.get("event_id") == event_id
    ]
    anchors = [a for a in anchors if a]
    return min(anchors) if anchors else None

def row_time_offset(row: dict[str, Any], *, events: dict[str, Any], train_rows: list[dict[str, Any]]) -> int | None:
    anchor = _parse_date(str(row.get("anchor_date") or ""))
    origin = _event_time_origin(str(row.get("event_id") or ""), events, train_rows)
    if not anchor or not origin:
        return None
    return _days_between(origin, anchor)

def _logit(p: float) -> float:
    p = clamp01(p)
    p = min(max(p, 1e-6), 1.0 - 1e-6)
    return math.log(p / (1.0 - p))

def _sigmoid(x: float) -> float:
    if x >= 0:
        z = math.exp(-x)
        return clamp01(1.0 / (1.0 + z))
    z = math.exp(x)
    return clamp01(z / (1.0 + z))

def fit_logistic_trend(
    train_rows: list[dict[str, Any]],
    *,
    events: dict[str, Any],
) -> tuple[float, float] | None:
    scored = probability_rows(train_rows)
    if len(scored) < LOGISTIC_MIN_TRAIN_N:
        return None

    points: list[tuple[int, float]] = []
    for row in scored:
        t = row_time_offset(row, events=events, train_rows=train_rows)
        label = row_label(row)
        if t is None or label is None:
            continue
        points.append((t, label))

    if len(points) < LOGISTIC_MIN_TRAIN_N:
        return None

    best_a, best_b = 0.0, 0.0
    best_loss = float("inf")
    for a_int in range(-10, 11):
        a = a_int * 0.5
        for b_int in range(-20, 21):
            b = b_int * 0.001
            loss = 0.0
            for t, y in points:
                p = _sigmoid(a + b * t)
                p = min(max(p, 1e-6), 1.0 - 1e-6)
                loss -= y * math.log(p) + (1.0 - y) * math.log(1.0 - p)
            if loss < best_loss:
                best_loss = loss
                best_a, best_b = a, b
    return best_a, best_b

def predict_logistic(
    row: dict[str, Any],
    *,
    a: float,
    b: float,
    events: dict[str, Any],
    train_rows: list[dict[str, Any]],
) -> float:
    t = row_time_offset(row, events=events, train_rows=train_rows)
    if t is None:
        return predict_persistence(row)
    return round(_sigmoid(float(a) + float(b) * t), 4)

def predict_regime_persistence(row: dict[str, Any]) -> str:
    latent = row.get("latent_features") or {}
    if isinstance(latent, dict):
        signal = latent.get("signal_vector")
        if isinstance(signal, list) and len(signal) > REGIME_SHIFT_INDEX:
            if float(signal[REGIME_SHIFT_INDEX]) >= 0.5:
                return "shift"
    return "no_shift"

def predict_regime_system(row: dict[str, Any]) -> str:
    return predict_regime_persistence(row)

def expected_calibration_error(
    preds: list[float],
    labels: list[float],
    *,
    bins: int = ECE_BINS,
) -> float | None:
    if not preds or len(preds) != len(labels):
        return None
    if len(preds) < bins:
        return None
    total = len(preds)
    ece = 0.0
    for bin_idx in range(bins):
        lo = bin_idx / bins
        hi = (bin_idx + 1) / bins
        idxs = [i for i, p in enumerate(preds) if (lo <= p < hi or (bin_idx == bins - 1 and p == 1.0))]
        if not idxs:
            continue
        bin_preds = [preds[i] for i in idxs]
        bin_labels = [labels[i] for i in idxs]
        avg_pred = sum(bin_preds) / len(bin_preds)
        avg_label = sum(bin_labels) / len(bin_labels)
        ece += (len(idxs) / total) * abs(avg_pred - avg_label)
    return round(ece, 4)

def regime_f1(preds: list[str], labels: list[str], *, positive: str = "shift") -> dict[str, Any]:
    tp = fp = fn = 0
    support = sum(1 for label in labels if label == positive)
    for pred, label in zip(preds, labels):
        if label == positive and pred == positive:
            tp += 1
        elif label != positive and pred == positive:
            fp += 1
        elif label == positive and pred != positive:
            fn += 1
    precision = round(tp / (tp + fp), 4) if tp + fp else None
    recall = round(tp / (tp + fn), 4) if tp + fn else None
    if precision is None or recall is None:
        f1 = None
    elif precision + recall == 0:
        f1 = 0.0
    else:
        f1 = round(2 * precision * recall / (precision + recall), 4)
    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "support": support,
        "positive_class": positive,
    }

def score_probability_lane(
    preds: list[float],
    rows: list[dict[str, Any]],
) -> dict[str, Any]:
    labels: list[float] = []
    briers: list[float] = []
    correct = 0
    for pred, row in zip(preds, rows):
        label = row_label(row)
        if label is None:
            continue
        labels.append(label)
        briers.append(brier_score(pred, label))
        correct += int(pred >= 0.5) == int(label >= 0.5)
    n = len(labels)
    if n == 0:
        return {
            "n_probability": 0,
            "brier": None,
            "accuracy": None,
            "calibration_error": None,
        }
    return {
        "n_probability": n,
        "brier": round(sum(briers) / n, 4),
        "accuracy": round(correct / n, 4),
        "calibration_error": expected_calibration_error(preds[:n], labels),
    }

def score_regime_lane(
    preds: list[str],
    rows: list[dict[str, Any]],
) -> dict[str, Any]:
    labels = [
        str((row.get("task_labels") or {}).get("regime_shift") or "no_shift")
        for row in rows
    ]
    f1_block = regime_f1(preds, labels)
    return {
        "n_regime": len(rows),
        "regime_f1": f1_block,
    }

def _merge_test_metrics(probability: dict[str, Any], regime: dict[str, Any]) -> dict[str, Any]:
    return {
        "n_probability": probability.get("n_probability", 0),
        "brier": probability.get("brier"),
        "accuracy": probability.get("accuracy"),
        "calibration_error": probability.get("calibration_error"),
        "n_regime": regime.get("n_regime", 0),
        "regime_f1": regime.get("regime_f1"),
    }

def evaluate_model_on_test(
    test_rows: list[dict[str, Any]],
    *,
    probability_predict: Callable[[dict[str, Any]], float],
    regime_predict: Callable[[dict[str, Any]], str],
) -> dict[str, Any]:
    prob_rows = probability_rows(test_rows)
    prob_preds = [probability_predict(row) for row in prob_rows]
    regime_preds = [regime_predict(row) for row in test_rows]
    probability = score_probability_lane(prob_preds, prob_rows)
    regime = score_regime_lane(regime_preds, test_rows)
    return _merge_test_metrics(probability, regime)

def build_baseline_payload(
    dataset: dict[str, Any],
    *,
    registry: dict[str, Any] | None = None,
) -> dict[str, Any]:
    from prediction_lib import load_event_registry

    events = registry if registry is not None else load_event_registry()
    meta = dataset.get("_meta") if isinstance(dataset, dict) else {}
    split_date = str((meta or {}).get("split_date") or "2026-01-01")
    train = list(dataset.get("train") or [])
    test = list(dataset.get("test") or [])

    prior_alpha, prior_beta = fit_train_prior(train)
    logistic = fit_logistic_trend(train, events=events)

    persistence_metrics = evaluate_model_on_test(
        test,
        probability_predict=predict_persistence,
        regime_predict=predict_regime_persistence,
    )
    bayesian_metrics = evaluate_model_on_test(
        test,
        probability_predict=lambda row: predict_bayesian(row, alpha=prior_alpha, beta=prior_beta),
        regime_predict=predict_regime_persistence,
    )

    logistic_block: dict[str, Any]
    if logistic is None:
        logistic_block = {
            "status": "skipped",
            "reason": "train_probability_n_lt_3",
        }
    else:
        a, b = logistic
        logistic_block = {
            "status": "ok",
            "coefficients": {"a": round(a, 4), "b": round(b, 6)},
            "test": evaluate_model_on_test(
                test,
                probability_predict=lambda row: predict_logistic(
                    row, a=a, b=b, events=events, train_rows=train
                ),
                regime_predict=predict_regime_persistence,
            ),
        }

    system_metrics = evaluate_model_on_test(
        test,
        probability_predict=predict_system,
        regime_predict=predict_regime_system,
    )

    test_prob_n = persistence_metrics.get("n_probability") or 0
    shift_support = (
        (persistence_metrics.get("regime_f1") or {}).get("support")
        if isinstance(persistence_metrics.get("regime_f1"), dict)
        else 0
    )
    low_n = (
        test_prob_n < LOW_N_PROBABILITY_THRESHOLD
        or (shift_support or 0) < LOW_N_SHIFT_SUPPORT_THRESHOLD
    )

    system_brier = system_metrics.get("brier")
    persistence_brier = persistence_metrics.get("brier")
    brier_delta = None
    system_beats = None
    if system_brier is not None and persistence_brier is not None:
        brier_delta = round(float(system_brier) - float(persistence_brier), 4)
        system_beats = system_brier < persistence_brier

    train_prob_n = len(probability_rows(train))

    return {
        "_meta": {
            "generated": True,
            "do_not_edit": True,
            "source": "scripts/build_baseline_forecasts.py",
            "phase": "pr5-advisory",
            "baseline_source": "heuristic_v1",
            "split_date": split_date,
            "low_n_advisory": low_n,
            "eval_scope": {
                "test_probability_n": test_prob_n,
                "test_regime_n": persistence_metrics.get("n_regime") or len(test),
                "test_shift_support": shift_support or 0,
                "train_probability_n": train_prob_n,
            },
            "train_diagnostics": {
                "bayesian_prior_alpha": round(prior_alpha, 4),
                "bayesian_prior_beta": round(prior_beta, 4),
                "logistic_status": logistic_block.get("status"),
            },
            "baselines": {
                "transformer": {"status": "deferred_pr5b"},
            },
        },
        "interpretation": "baseline_evaluation",
        "system_reference": "engm_event_probability",
        "system": {
            "test": system_metrics,
        },
        "baselines": {
            "persistence": {"test": persistence_metrics},
            "bayesian": {"test": bayesian_metrics},
            "logistic_trend": logistic_block,
            "transformer": {"status": "deferred_pr5b"},
        },
        "comparison": {
            "test": {
                "brier_delta_vs_persistence": brier_delta,
                "system_beats_persistence": system_beats,
            },
        },
    }

def main() -> int:
    import argparse
    import json

    from prediction_lib import render_json

    default_dataset = _REPO_ROOT / "runtime" / "artifacts" / "epistemic-dataset.json"
    default_output = _REPO_ROOT / "runtime" / "artifacts" / "baseline-forecast-metrics.json"

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=default_dataset)
    parser.add_argument("--output", type=Path, default=default_output)
    args = parser.parse_args()

    dataset = json.loads(args.dataset.read_text(encoding="utf-8")) if args.dataset.is_file() else {}
    payload = build_baseline_payload(dataset)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_json(payload), encoding="utf-8")
    scope = payload["_meta"]["eval_scope"]
    print(
        f"[ok] wrote {args.output.relative_to(_REPO_ROOT)} "
        f"(test_probability_n={scope['test_probability_n']}, low_n={payload['_meta']['low_n_advisory']})"
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
