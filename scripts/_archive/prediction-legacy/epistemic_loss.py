"""PR2 epistemic calibration loss — advisory evaluation metric (read-only, no training)."""

from __future__ import annotations

import math
import sys
from datetime import date
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SCRIPTS = _REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from prediction.epistemic_generative_model import OBSERVATION_CLASSES  # noqa: E402
from prediction.signal_math import clamp01  # noqa: E402

DEFAULT_WEIGHTS = {
    "alpha": 0.35,
    "beta": 0.35,
    "gamma": 0.15,
    "delta": 0.15,
}

OVERCONFIDENCE_NUDGE = 0.05
LOW_N_ADVISORY_THRESHOLD = 5
REGIME_DELAY_CAP_DAYS = 365

STANCE_TO_CLASS = {
    "yes": "affirm_escalation",
    "no": "affirm_deescalation",
    "uncertain": "withhold",
    "conditional": "withhold",
}

def shannon_entropy(probs: list[float]) -> float:
    if not probs:
        return 0.0
    total = sum(float(p) for p in probs)
    if total <= 0:
        return 0.0
    normalized = [float(p) / total for p in probs]
    entropy = 0.0
    for p in normalized:
        if p > 0:
            entropy -= p * math.log(p)
    max_entropy = math.log(len(normalized)) if len(normalized) > 1 else 1.0
    if max_entropy <= 0:
        return 0.0
    return round(clamp01(entropy / max_entropy), 4)

def outcome_to_label(outcome: str | None) -> float | None:
    key = str(outcome or "").casefold()
    if key == "yes":
        return 1.0
    if key == "no":
        return 0.0
    return None

def prediction_error(y_pred: float, y_true: float) -> float:
    return round(abs(float(y_pred) - float(y_true)), 4)

def brier_score(y_pred: float, y_true: float) -> float:
    delta = float(y_pred) - float(y_true)
    return round(delta * delta, 4)

def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(str(value)[:10])
    except ValueError:
        return None

def _days_between(start: date, end: date) -> int:
    return max(0, (end - start).days)

def _pooled_predicted_probs(
    engm_event: dict[str, Any] | None,
    signal_block: dict[str, Any] | None,
) -> list[float]:
    voice_projections = (engm_event or {}).get("voice_projections") or {}
    if isinstance(voice_projections, dict) and voice_projections:
        pooled = {cls: 0.0 for cls in OBSERVATION_CLASSES}
        weight_sum = 0.0
        for projection in voice_projections.values():
            if not isinstance(projection, dict):
                continue
            weight = float(projection.get("sensor_weight") or 1.0)
            probs = projection.get("observation_probs") or {}
            if not isinstance(probs, dict):
                continue
            weight_sum += weight
            for cls in OBSERVATION_CLASSES:
                pooled[cls] += weight * float(probs.get(cls) or 0.0)
        if weight_sum > 0:
            return [round(pooled[cls] / weight_sum, 4) for cls in OBSERVATION_CLASSES]

    drift = (signal_block or {}).get("drift_vector") or []
    if isinstance(drift, list) and drift:
        values = [abs(float(v)) for v in drift]
        total = sum(values) or 1.0
        base = [v / total for v in values]
        while len(base) < len(OBSERVATION_CLASSES):
            base.append(0.0)
        return [round(v, 4) for v in base[: len(OBSERVATION_CLASSES)]]

    uniform = 1.0 / len(OBSERVATION_CLASSES)
    return [round(uniform, 4) for _ in OBSERVATION_CLASSES]

def _observed_stance_probs(timeline_event: dict[str, Any] | None) -> list[float]:
    latest = (timeline_event or {}).get("latest_by_speaker") or {}
    counts = {cls: 0.0 for cls in OBSERVATION_CLASSES}
    if not isinstance(latest, dict) or not latest:
        uniform = 1.0 / len(OBSERVATION_CLASSES)
        return [round(uniform, 4) for _ in OBSERVATION_CLASSES]

    for row in latest.values():
        if not isinstance(row, dict):
            continue
        stance = str(row.get("stance") or "").casefold()
        cls = STANCE_TO_CLASS.get(stance, "withhold")
        counts[cls] += 1.0

    total = sum(counts.values()) or 1.0
    return [round(counts[cls] / total, 4) for cls in OBSERVATION_CLASSES]

def entropy_misalignment(
    *,
    engm_event: dict[str, Any] | None,
    timeline_event: dict[str, Any] | None,
    signal_block: dict[str, Any] | None = None,
    y_pred: float | None = None,
    y_true: float | None = None,
) -> dict[str, Any]:
    predicted_probs = _pooled_predicted_probs(engm_event, signal_block)
    observed_probs = _observed_stance_probs(timeline_event)
    h_pred = shannon_entropy(predicted_probs)
    h_obs = shannon_entropy(observed_probs)
    misalignment = round(clamp01(abs(h_pred - h_obs)), 4)
    overconfidence_penalty = 0.0
    if y_pred is not None and y_true is not None:
        if (float(y_pred) > 0.5) != (float(y_true) > 0.5):
            overconfidence_penalty = OVERCONFIDENCE_NUDGE
    value = round(clamp01(misalignment + overconfidence_penalty), 4)
    return {
        "value": value,
        "h_predicted": h_pred,
        "h_observed": h_obs,
        "overconfidence_penalty": overconfidence_penalty,
    }

def _collect_shift_dates(timeline_event: dict[str, Any] | None) -> list[str]:
    shifts_root = (timeline_event or {}).get("shifts") or {}
    dates: list[str] = []
    if not isinstance(shifts_root, dict):
        return dates
    for speaker_shifts in shifts_root.values():
        if not isinstance(speaker_shifts, list):
            continue
        for shift in speaker_shifts:
            if not isinstance(shift, dict):
                continue
            to_date = shift.get("to_date")
            if to_date:
                dates.append(str(to_date))
    return dates

def regime_shift_delay(
    *,
    timeline_event: dict[str, Any] | None,
    signal_block: dict[str, Any] | None,
    regime: dict[str, Any] | None,
    eval_date: str,
) -> dict[str, Any]:
    shift_dates = _collect_shift_dates(timeline_event)
    if not shift_dates:
        return {"value": 0.0, "shift_count": 0, "note": "no_shifts"}

    eval_day = _parse_date(eval_date) or date.today()
    actual_day = min(d for d in (_parse_date(s) for s in shift_dates) if d is not None)
    global_signals = (regime or {}).get("global_signals") or {}
    detected = bool((signal_block or {}).get("regime_shift_detected"))
    if isinstance(global_signals, dict):
        detected = detected or bool(global_signals.get("regime_shift_detected"))

    if detected:
        delay_days = _days_between(actual_day, eval_day)
    else:
        delay_days = _days_between(actual_day, eval_day)

    value = round(clamp01(delay_days / REGIME_DELAY_CAP_DAYS), 4)
    return {
        "value": value,
        "shift_count": len(shift_dates),
        "t_actual": actual_day.isoformat(),
        "t_eval": eval_day.isoformat(),
        "detected": detected,
        "delay_days": delay_days,
    }

def _is_brier_eligible(registry_event: dict[str, Any]) -> bool:
    if str(registry_event.get("status") or "") != "resolved":
        return False
    return outcome_to_label(registry_event.get("outcome")) is not None

def compute_event_losses(
    event_id: str,
    *,
    registry_event: dict[str, Any],
    engm_event: dict[str, Any] | None,
    timeline_event: dict[str, Any] | None,
    signal_block: dict[str, Any] | None,
    regime: dict[str, Any] | None,
    eval_date: str,
) -> dict[str, Any]:
    y_true = outcome_to_label(registry_event.get("outcome"))
    y_pred = float((engm_event or {}).get("event_probability") or 0.5)
    included_in_brier = _is_brier_eligible(registry_event) and engm_event is not None

    block: dict[str, Any] = {
        "included_in_brier": included_in_brier,
    }
    if y_true is not None and engm_event is not None:
        block["y_true"] = y_true
        block["y_pred"] = y_pred
        block["prediction_error"] = prediction_error(y_pred, y_true)
        block["brier_score"] = brier_score(y_pred, y_true)
    elif engm_event is not None:
        block["y_pred"] = y_pred

    entropy_block = entropy_misalignment(
        engm_event=engm_event,
        timeline_event=timeline_event,
        signal_block=signal_block,
        y_pred=y_pred if engm_event is not None else None,
        y_true=y_true if included_in_brier else None,
    )
    block["entropy_misalignment"] = entropy_block["value"]
    if entropy_block["overconfidence_penalty"]:
        block["overconfidence_penalty"] = entropy_block["overconfidence_penalty"]

    delay_block = regime_shift_delay(
        timeline_event=timeline_event,
        signal_block=signal_block,
        regime=regime,
        eval_date=eval_date,
    )
    if delay_block.get("shift_count", 0) > 0:
        block["regime_shift_delay"] = delay_block["value"]

    return block

def _mean(values: list[float]) -> float:
    if not values:
        return 0.0
    return round(sum(values) / len(values), 4)

def compute_aggregate_loss(
    *,
    event_blocks: dict[str, dict[str, Any]],
    weights: dict[str, float] | None = None,
    regime: dict[str, Any] | None = None,
) -> dict[str, Any]:
    w = {**DEFAULT_WEIGHTS, **(weights or {})}

    pe_values = [
        float(block["prediction_error"])
        for block in event_blocks.values()
        if block.get("included_in_brier") and "prediction_error" in block
    ]
    brier_values = [
        float(block["brier_score"])
        for block in event_blocks.values()
        if block.get("included_in_brier") and "brier_score" in block
    ]
    entropy_values = [
        float(block["entropy_misalignment"])
        for block in event_blocks.values()
        if "entropy_misalignment" in block
    ]
    delay_values = [
        float(block["regime_shift_delay"])
        for block in event_blocks.values()
        if "regime_shift_delay" in block
    ]

    pe_mean = _mean(pe_values)
    brier_mean = _mean(brier_values)
    entropy_mean = _mean(entropy_values)
    delay_mean = _mean(delay_values)

    regime_shift_delay_note = None
    global_signals = (regime or {}).get("global_signals") or {}
    if not delay_values:
        if isinstance(global_signals, dict) and global_signals.get("regime_shift_detected"):
            delay_mean = 0.5
            regime_shift_delay_note = "global_regime_shift_no_event_shifts"
        else:
            regime_shift_delay_note = "no_shift_events"

    components = {
        "prediction_error": {
            "value": pe_mean,
            "aggregate": "mean",
            "event_count": len(pe_values),
        },
        "brier_score": {
            "value": brier_mean,
            "aggregate": "mean",
            "event_count": len(brier_values),
        },
        "entropy_misalignment": {
            "value": entropy_mean,
            "aggregate": "mean",
            "event_count": len(entropy_values),
        },
        "regime_shift_delay": {
            "value": delay_mean,
            "aggregate": "mean",
            "shift_event_count": len(delay_values),
        },
    }
    if regime_shift_delay_note:
        components["regime_shift_delay"]["note"] = regime_shift_delay_note

    total_loss = round(
        w["alpha"] * pe_mean
        + w["beta"] * brier_mean
        + w["gamma"] * entropy_mean
        + w["delta"] * delay_mean,
        4,
    )
    total_loss = clamp01(total_loss)

    return {
        "weights": w,
        "components": components,
        "total_loss": total_loss,
    }

def build_calibration_payload(
    *,
    registry: dict[str, dict[str, Any]] | None = None,
    engm: dict[str, Any] | None = None,
    timeline: dict[str, Any] | None = None,
    signals: dict[str, Any] | None = None,
    regime: dict[str, Any] | None = None,
    eval_date: str | None = None,
    weights: dict[str, float] | None = None,
) -> dict[str, Any]:
    from prediction_lib import load_event_registry

    events = registry or load_event_registry()
    engm_payload = engm or {}
    timeline_payload = timeline or {}
    signals_payload = signals or {}
    regime_payload = regime or {}

    engm_events = engm_payload.get("events") if isinstance(engm_payload, dict) else {}
    timeline_events = timeline_payload.get("events") if isinstance(timeline_payload, dict) else {}
    signal_events = signals_payload.get("events") if isinstance(signals_payload, dict) else {}

    if not isinstance(engm_events, dict):
        engm_events = {}
    if not isinstance(timeline_events, dict):
        timeline_events = {}
    if not isinstance(signal_events, dict):
        signal_events = {}

    eval_day = eval_date or date.today().isoformat()

    resolved_count = sum(
        1 for ev in events.values() if str(ev.get("status") or "") == "resolved"
    )

    event_blocks: dict[str, dict[str, Any]] = {}
    for event_id in sorted(set(events) | set(engm_events)):
        registry_event = events.get(event_id)
        if not isinstance(registry_event, dict):
            continue
        engm_event = engm_events.get(event_id) if isinstance(engm_events.get(event_id), dict) else None
        if engm_event is None:
            continue
        event_blocks[event_id] = compute_event_losses(
            event_id,
            registry_event=registry_event,
            engm_event=engm_event,
            timeline_event=timeline_events.get(event_id) if isinstance(timeline_events, dict) else None,
            signal_block=signal_events.get(event_id) if isinstance(signal_events, dict) else None,
            regime=regime_payload,
            eval_date=eval_day,
        )

    brier_eligible = sum(1 for block in event_blocks.values() if block.get("included_in_brier"))
    aggregate = compute_aggregate_loss(
        event_blocks=event_blocks,
        weights=weights,
        regime=regime_payload,
    )

    meta: dict[str, Any] = {
        "generated": True,
        "do_not_edit": True,
        "source": "scripts/build_epistemic_calibration_loss.py",
        "phase": "engm-pr2-advisory",
        "calibration_source": "heuristic_v1",
        "calibration_scope": {
            "resolved_event_count": resolved_count,
            "brier_eligible": brier_eligible,
            "low_n_advisory": brier_eligible < LOW_N_ADVISORY_THRESHOLD,
        },
        "eval_date": eval_day,
    }

    return {
        "_meta": meta,
        "weights": aggregate["weights"],
        "components": aggregate["components"],
        "total_loss": aggregate["total_loss"],
        "interpretation": "calibration_metric",
        "events": event_blocks,
    }

def main() -> int:
    import argparse
    import json

    from prediction_lib import render_json

    default_engm = _REPO_ROOT / "runtime" / "artifacts" / "epistemic-generative-state.json"
    default_timeline = _REPO_ROOT / "runtime" / "artifacts" / "prediction-timeline.json"
    default_signals = _REPO_ROOT / "runtime" / "artifacts" / "prediction-signals.json"
    default_regime = _REPO_ROOT / "runtime" / "artifacts" / "prediction-regime-summary.json"
    default_output = _REPO_ROOT / "runtime" / "artifacts" / "epistemic-calibration-loss.json"

    def _load(path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engm", type=Path, default=default_engm)
    parser.add_argument("--timeline", type=Path, default=default_timeline)
    parser.add_argument("--signals", type=Path, default=default_signals)
    parser.add_argument("--regime", type=Path, default=default_regime)
    parser.add_argument("--output", type=Path, default=default_output)
    parser.add_argument("--eval-date", default=date.today().isoformat())
    args = parser.parse_args()

    payload = build_calibration_payload(
        engm=_load(args.engm),
        timeline=_load(args.timeline),
        signals=_load(args.signals),
        regime=_load(args.regime),
        eval_date=args.eval_date,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_json(payload), encoding="utf-8")
    print(
        f"[ok] wrote {args.output.relative_to(_REPO_ROOT)} "
        f"(total_loss={payload.get('total_loss')}, events={len(payload.get('events') or {})})"
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
