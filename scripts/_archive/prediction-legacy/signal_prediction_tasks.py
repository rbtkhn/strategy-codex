"""PR3 signal prediction tasks — supervised task target space (read-only advisory, no training)."""

from __future__ import annotations

import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SCRIPTS = _REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from prediction.contracts import has_string_falsifier, has_valid_falsifier_model
from prediction.signal_extraction_engine import (
    build_probability_snapshots,
    cross_voice_alignment,
    effective_falsifier_model,
)
from prediction.signal_math import clamp01, detect_step_change

DEFAULT_HORIZON_DAYS = 30
DELTA_EPSILON = 0.05
CONVERGENCE_DELTA = 0.15
LOW_N_ADVISORY_THRESHOLD = 20

TASKS = ("regime_shift", "delta", "convergence")
VOICES = ("freeman", "mercouris", "macgregor")

SIGNAL_VECTOR_DIMENSIONS = (
    "confidence",
    "cross_voice_alignment",
    "drift_tail_mean",
    "regime_shift_detected",
    "entropy_score",
)


def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(str(value)[:10])
    except ValueError:
        return None


def _date_add(d: date, days: int) -> date:
    return d + timedelta(days=days)


def build_signal_vector(
    signal_block: dict[str, Any] | None,
    semantic_block: dict[str, Any] | None,
) -> list[float]:
    block = signal_block or {}
    drift = block.get("drift_vector") or []
    if isinstance(drift, list) and drift:
        tail_values = [float(v) for v in drift[-3:]]
        drift_tail_mean = round(sum(tail_values) / len(tail_values), 4)
    else:
        drift_tail_mean = 0.0

    return [
        round(float(block.get("confidence") or 0.35), 4),
        round(float(block.get("cross_voice_alignment") or 1.0), 4),
        drift_tail_mean,
        1.0 if block.get("regime_shift_detected") else 0.0,
        round(float((semantic_block or {}).get("entropy_score") or 0.0), 4),
    ]


def _collect_shift_dates(timeline_event: dict[str, Any] | None) -> list[date]:
    shifts_root = (timeline_event or {}).get("shifts") or {}
    dates: list[date] = []
    if not isinstance(shifts_root, dict):
        return dates
    for speaker_shifts in shifts_root.values():
        if not isinstance(speaker_shifts, list):
            continue
        for shift in speaker_shifts:
            if not isinstance(shift, dict):
                continue
            parsed = _parse_date(str(shift.get("to_date") or ""))
            if parsed:
                dates.append(parsed)
    return dates


def derive_regime_shift_label(
    *,
    timeline_event: dict[str, Any] | None,
    anchor_date: str,
    horizon_days: int = DEFAULT_HORIZON_DAYS,
) -> str:
    anchor = _parse_date(anchor_date)
    if not anchor:
        return "no_shift"
    horizon_end = _date_add(anchor, horizon_days)
    for shift_date in _collect_shift_dates(timeline_event):
        if anchor < shift_date <= horizon_end:
            return "shift"
    return "no_shift"


def _sorted_entries(timeline_event: dict[str, Any] | None) -> list[dict[str, Any]]:
    entries = (timeline_event or {}).get("entries") or []
    if not isinstance(entries, list):
        return []
    return sorted(
        [e for e in entries if isinstance(e, dict)],
        key=lambda e: str(e.get("date") or ""),
    )


def _slice_timeline_event(
    timeline_event: dict[str, Any] | None,
    *,
    max_date: date,
) -> dict[str, Any]:
    if not timeline_event:
        return {"entries": [], "latest_by_speaker": {}}
    entries = _sorted_entries(timeline_event)
    kept = [e for e in entries if (_parse_date(str(e.get("date") or "")) or date.min) <= max_date]
    latest: dict[str, Any] = {}
    for entry in kept:
        speaker = str(entry.get("speaker") or "")
        if speaker:
            latest[speaker] = entry
    return {
        "entries": kept,
        "latest_by_speaker": latest,
        "shifts": timeline_event.get("shifts") or {},
    }


def _snapshot_at_anchor(
    event_id: str,
    event: dict[str, Any],
    model: dict[str, Any],
    timeline_event: dict[str, Any] | None,
    *,
    semantic_block: dict[str, Any] | None,
    anchor_index: int,
) -> tuple[float, list[float]]:
    sliced = dict(timeline_event or {})
    entries = _sorted_entries(timeline_event)
    if not entries:
        snapshots, _, _ = build_probability_snapshots(
            event_id, event, model, sliced, semantic_block=semantic_block
        )
        value = snapshots[0] if snapshots else 0.0
        return value, snapshots

    anchor_entries = entries[: anchor_index + 1]
    sliced["entries"] = anchor_entries
    latest: dict[str, Any] = {}
    for entry in anchor_entries:
        speaker = str(entry.get("speaker") or "")
        if speaker:
            latest[speaker] = entry
    sliced["latest_by_speaker"] = latest
    snapshots, _, _ = build_probability_snapshots(
        event_id, event, model, sliced, semantic_block=semantic_block
    )
    idx = min(anchor_index, len(snapshots) - 1) if snapshots else 0
    return (snapshots[idx] if snapshots else 0.0), snapshots


def derive_delta_label(
    event_id: str,
    event: dict[str, Any],
    *,
    timeline_event: dict[str, Any] | None,
    semantic_block: dict[str, Any] | None,
    anchor_date: str,
    anchor_index: int,
    horizon_days: int = DEFAULT_HORIZON_DAYS,
) -> dict[str, Any]:
    model, _ = effective_falsifier_model(event_id, event)
    p_t, _ = _snapshot_at_anchor(
        event_id,
        event,
        model,
        timeline_event,
        semantic_block=semantic_block,
        anchor_index=anchor_index,
    )
    anchor = _parse_date(anchor_date) or date.today()
    horizon_target = _date_add(anchor, horizon_days)
    entries = _sorted_entries(timeline_event)

    future_index = len(entries) - 1
    for idx, entry in enumerate(entries):
        entry_date = _parse_date(str(entry.get("date") or ""))
        if entry_date and entry_date >= horizon_target:
            future_index = idx
            break

    p_future, _ = _snapshot_at_anchor(
        event_id,
        event,
        model,
        timeline_event,
        semantic_block=semantic_block,
        anchor_index=future_index,
    )
    delta = round(p_future - p_t, 4)
    if delta > DELTA_EPSILON:
        bucket = "up"
    elif delta < -DELTA_EPSILON:
        bucket = "down"
    else:
        bucket = "flat"
    return {
        "future_outcome": bucket,
        "delta": delta,
        "p_t": round(p_t, 4),
        "p_future": round(p_future, 4),
    }


def derive_convergence_label(
    event_id: str,
    event: dict[str, Any],
    *,
    timeline_event: dict[str, Any] | None,
    semantic_block: dict[str, Any] | None,
    anchor_date: str,
    horizon_days: int = DEFAULT_HORIZON_DAYS,
) -> str:
    anchor = _parse_date(anchor_date)
    if not anchor:
        return "stable"
    model, _ = effective_falsifier_model(event_id, event)
    entries = _sorted_entries(timeline_event)
    horizon_target = _date_add(anchor, horizon_days)

    end_date = anchor
    for entry in entries:
        entry_date = _parse_date(str(entry.get("date") or ""))
        if entry_date and entry_date >= horizon_target:
            end_date = entry_date
            break
    else:
        if entries:
            last = _parse_date(str(entries[-1].get("date") or ""))
            if last:
                end_date = last

    slice_anchor = _slice_timeline_event(timeline_event, max_date=anchor)
    slice_future = _slice_timeline_event(timeline_event, max_date=end_date)
    if len(slice_anchor.get("latest_by_speaker") or {}) < 2:
        return "stable"
    if len(slice_future.get("latest_by_speaker") or {}) < 2:
        return "stable"

    align_anchor = cross_voice_alignment(
        event_id, event, model, slice_anchor, semantic_block=semantic_block
    )
    align_future = cross_voice_alignment(
        event_id, event, model, slice_future, semantic_block=semantic_block
    )
    delta = align_future - align_anchor
    if delta >= CONVERGENCE_DELTA:
        return "converged"
    if delta <= -CONVERGENCE_DELTA:
        return "diverged"
    return "stable"


def predict_regime_shift(
    event_id: str,
    *,
    signal_vector: list[float],
    signal_block: dict[str, Any] | None = None,
    horizon_days: int = DEFAULT_HORIZON_DAYS,
) -> dict[str, Any]:
    del event_id, horizon_days
    block = signal_block or {}
    drift = block.get("drift_vector") or []
    drift_list = [float(v) for v in drift] if isinstance(drift, list) else []
    if len(signal_vector) > 3 and signal_vector[3] >= 0.5:
        predicted = "shift"
    elif detect_step_change(drift_list):
        predicted = "shift"
    else:
        predicted = "no_shift"
    return {"predicted_outcome": predicted, "task_source": "heuristic_v1"}


def predict_delta(
    event_id: str,
    *,
    signal_vector: list[float],
    p_t: float,
    signal_block: dict[str, Any] | None = None,
    horizon_days: int = DEFAULT_HORIZON_DAYS,
) -> dict[str, Any]:
    del event_id, p_t, horizon_days
    block = signal_block or {}
    drift = block.get("drift_vector") or []
    if isinstance(drift, list) and drift:
        last = float(drift[-1])
    else:
        last = float(signal_vector[2] if len(signal_vector) > 2 else 0.0)
    if last > DELTA_EPSILON:
        predicted = "up"
    elif last < -DELTA_EPSILON:
        predicted = "down"
    else:
        predicted = "flat"
    return {"predicted_outcome": predicted, "task_source": "heuristic_v1"}


def predict_convergence(
    *,
    signal_vector: list[float],
    voice_states: dict[str, str] | None = None,
    horizon_days: int = DEFAULT_HORIZON_DAYS,
) -> dict[str, Any]:
    del horizon_days
    alignment = float(signal_vector[1] if len(signal_vector) > 1 else 1.0)
    voices = voice_states or {}
    stances = {str(v).casefold() for v in voices.values() if v}
    if alignment >= 0.7 and len(stances) <= 1:
        predicted = "converged"
    elif alignment <= 0.35 or len(stances) >= 3:
        predicted = "diverged"
    else:
        predicted = "stable"
    return {"predicted_outcome": predicted, "task_source": "heuristic_v1"}


def _voice_states_at_anchor(timeline_event: dict[str, Any] | None, anchor_date: str) -> dict[str, str]:
    anchor = _parse_date(anchor_date)
    if not anchor:
        return {}
    sliced = _slice_timeline_event(timeline_event, max_date=anchor)
    latest = sliced.get("latest_by_speaker") or {}
    return {
        str(speaker): str(row.get("stance") or "")
        for speaker, row in latest.items()
        if isinstance(row, dict)
    }


def build_task_examples(
    *,
    registry: dict[str, dict[str, Any]],
    timeline: dict[str, Any],
    signals: dict[str, Any],
    semantic_scores: dict[str, Any],
    horizon_days: int = DEFAULT_HORIZON_DAYS,
) -> list[dict[str, Any]]:
    timeline_events = timeline.get("events") if isinstance(timeline, dict) else {}
    signal_events = signals.get("events") if isinstance(signals, dict) else {}
    semantic_events = semantic_scores.get("events") if isinstance(semantic_scores, dict) else {}
    if not isinstance(timeline_events, dict):
        timeline_events = {}
    if not isinstance(signal_events, dict):
        signal_events = {}
    if not isinstance(semantic_events, dict):
        semantic_events = {}

    examples: list[dict[str, Any]] = []
    for event_id in sorted(registry):
        event = registry[event_id]
        if event.get("not_falsifiable"):
            continue
        if not has_string_falsifier(event) and not has_valid_falsifier_model(event):
            continue

        timeline_event = timeline_events.get(event_id)
        signal_block = signal_events.get(event_id) if isinstance(signal_events.get(event_id), dict) else {}
        semantic_block = semantic_events.get(event_id) if isinstance(semantic_events.get(event_id), dict) else {}
        signal_vector = build_signal_vector(signal_block, semantic_block)

        entries = _sorted_entries(timeline_event if isinstance(timeline_event, dict) else None)
        if len(entries) < 2:
            continue

        for anchor_index, entry in enumerate(entries[:-1]):
            anchor_date = str(entry.get("date") or "")
            if not anchor_date:
                continue

            regime_label = derive_regime_shift_label(
                timeline_event=timeline_event if isinstance(timeline_event, dict) else None,
                anchor_date=anchor_date,
                horizon_days=horizon_days,
            )
            regime_pred = predict_regime_shift(
                event_id,
                signal_vector=signal_vector,
                signal_block=signal_block,
                horizon_days=horizon_days,
            )
            examples.append(
                {
                    "event_id": event_id,
                    "task": "regime_shift",
                    "anchor_date": anchor_date,
                    "time_offset": horizon_days,
                    "signal_vector": signal_vector,
                    "future_outcome": regime_label,
                    "predicted_outcome": regime_pred["predicted_outcome"],
                    "interpretation": "supervised_task_example",
                }
            )

            delta_label = derive_delta_label(
                event_id,
                event,
                timeline_event=timeline_event if isinstance(timeline_event, dict) else None,
                semantic_block=semantic_block,
                anchor_date=anchor_date,
                anchor_index=anchor_index,
                horizon_days=horizon_days,
            )
            delta_pred = predict_delta(
                event_id,
                signal_vector=signal_vector,
                p_t=float(delta_label["p_t"]),
                signal_block=signal_block,
                horizon_days=horizon_days,
            )
            examples.append(
                {
                    "event_id": event_id,
                    "task": "delta",
                    "anchor_date": anchor_date,
                    "time_offset": horizon_days,
                    "signal_vector": signal_vector,
                    "future_outcome": delta_label["future_outcome"],
                    "delta": delta_label["delta"],
                    "p_t": delta_label["p_t"],
                    "p_future": delta_label["p_future"],
                    "predicted_outcome": delta_pred["predicted_outcome"],
                    "interpretation": "supervised_task_example",
                }
            )

            voice_states = _voice_states_at_anchor(
                timeline_event if isinstance(timeline_event, dict) else None,
                anchor_date,
            )
            if len(voice_states) >= 2:
                conv_label = derive_convergence_label(
                    event_id,
                    event,
                    timeline_event=timeline_event if isinstance(timeline_event, dict) else None,
                    semantic_block=semantic_block,
                    anchor_date=anchor_date,
                    horizon_days=horizon_days,
                )
                conv_pred = predict_convergence(
                    signal_vector=signal_vector,
                    voice_states=voice_states,
                    horizon_days=horizon_days,
                )
                examples.append(
                    {
                        "event_id": event_id,
                        "task": "convergence",
                        "anchor_date": anchor_date,
                        "time_offset": horizon_days,
                        "signal_vector": signal_vector,
                        "future_outcome": conv_label,
                        "voice_states": voice_states,
                        "predicted_outcome": conv_pred["predicted_outcome"],
                        "interpretation": "supervised_task_example",
                    }
                )

    return examples


def build_task_payload(
    *,
    registry: dict[str, dict[str, Any]] | None = None,
    timeline: dict[str, Any] | None = None,
    signals: dict[str, Any] | None = None,
    semantic_scores: dict[str, Any] | None = None,
    horizon_days: int = DEFAULT_HORIZON_DAYS,
) -> dict[str, Any]:
    from prediction_lib import load_event_registry

    events = registry or load_event_registry()
    examples = build_task_examples(
        registry=events,
        timeline=timeline or {},
        signals=signals or {},
        semantic_scores=semantic_scores or {},
        horizon_days=horizon_days,
    )
    example_count = len(examples)
    shift_examples = sum(1 for ex in examples if ex.get("task") == "regime_shift" and ex.get("future_outcome") == "shift")

    return {
        "_meta": {
            "generated": True,
            "do_not_edit": True,
            "source": "scripts/build_signal_prediction_tasks.py",
            "phase": "pr3-advisory",
            "task_source": "heuristic_v1",
            "horizon_days": horizon_days,
            "signal_vector_dimensions": list(SIGNAL_VECTOR_DIMENSIONS),
            "task_scope": {
                "example_count": example_count,
                "low_n_advisory": example_count < LOW_N_ADVISORY_THRESHOLD,
                "shift_positive_count": shift_examples,
            },
            "task_scope_note": (
                "signal_vector is event-level from current prediction-signals.json; "
                "labels derived from timeline anchors (heuristic_v1 stub)"
            ),
        },
        "tasks": list(TASKS),
        "interpretation": "supervised_task_space",
        "examples": examples,
    }


def main() -> int:
    import argparse
    import json

    from prediction_lib import render_json

    default_timeline = _REPO_ROOT / "runtime" / "artifacts" / "prediction-timeline.json"
    default_signals = _REPO_ROOT / "runtime" / "artifacts" / "prediction-signals.json"
    default_semantic = _REPO_ROOT / "runtime" / "artifacts" / "prediction-semantic-scores.json"
    default_output = _REPO_ROOT / "runtime" / "artifacts" / "signal-prediction-tasks.json"

    def _load(path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeline", type=Path, default=default_timeline)
    parser.add_argument("--signals", type=Path, default=default_signals)
    parser.add_argument("--semantic-scores", type=Path, default=default_semantic)
    parser.add_argument("--output", type=Path, default=default_output)
    parser.add_argument("--horizon-days", type=int, default=DEFAULT_HORIZON_DAYS)
    args = parser.parse_args()

    payload = build_task_payload(
        timeline=_load(args.timeline),
        signals=_load(args.signals),
        semantic_scores=_load(args.semantic_scores),
        horizon_days=args.horizon_days,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_json(payload), encoding="utf-8")
    print(
        f"[ok] wrote {args.output.relative_to(_REPO_ROOT)} "
        f"({payload['_meta']['task_scope']['example_count']} example(s))"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
