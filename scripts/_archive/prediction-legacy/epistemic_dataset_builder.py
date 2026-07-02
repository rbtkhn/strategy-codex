"""PR4 epistemic dataset builder — ML-ready rows with temporal split (read-only advisory)."""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SCRIPTS = _REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from prediction.contracts import find_duplicate_fingerprints, has_string_falsifier, has_valid_falsifier_model
from prediction.epistemic_generative_model import LATENT_DIMENSIONS
from prediction.signal_extraction_engine import effective_falsifier_model
from prediction.signal_prediction_tasks import (
    DEFAULT_HORIZON_DAYS,
    SIGNAL_VECTOR_DIMENSIONS,
    _parse_date,
    _slice_timeline_event,
    _sorted_entries,
    _voice_states_at_anchor,
    build_signal_vector,
    derive_convergence_label,
    derive_delta_label,
    derive_regime_shift_label,
)

DEFAULT_SPLIT_DATE = "2026-01-01"
LOW_N_ADVISORY_THRESHOLD = 20
CLAIM_MAX_LEN = 120

def _truncate(text: str, limit: int = CLAIM_MAX_LEN) -> str:
    cleaned = " ".join(str(text or "").split())
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[: limit - 3] + "..."

def build_voice_observations(
    event: dict[str, Any],
    timeline_event: dict[str, Any] | None,
    *,
    anchor_date: str,
) -> list[dict[str, Any]]:
    question = _truncate(str(event.get("question") or ""))
    anchor = _parse_date(anchor_date)
    if not anchor:
        return []
    sliced = _slice_timeline_event(timeline_event, max_date=anchor)
    latest = sliced.get("latest_by_speaker") or {}
    observations: list[dict[str, Any]] = []
    if not isinstance(latest, dict):
        return observations
    for voice in sorted(latest.keys()):
        row = latest[voice]
        if not isinstance(row, dict):
            continue
        stance = str(row.get("stance") or "")
        claim = f"{voice}:{stance} | {question}" if question else f"{voice}:{stance}"
        observations.append(
            {
                "voice": str(voice),
                "stance": stance,
                "claim": claim,
            }
        )
    return observations

def build_latent_features(
    *,
    engm_event: dict[str, Any] | None,
    engm_latent: dict[str, Any] | None,
    signal_vector: list[float],
) -> dict[str, Any]:
    latent = engm_latent or {}
    event_block = engm_event or {}
    z = latent.get("Z") if isinstance(latent.get("Z"), list) else []
    return {
        "Z": list(z),
        "Z_dimensions": list(latent.get("dimensions") or LATENT_DIMENSIONS),
        "signal_vector": list(signal_vector),
        "signal_vector_dimensions": list(SIGNAL_VECTOR_DIMENSIONS),
        "event_probability": round(float(event_block.get("event_probability") or 0.5), 4),
        "inference_source": "heuristic_v1",
    }

def _outcome_at_anchor(event: dict[str, Any], anchor_date: str) -> tuple[str | None, bool]:
    status = str(event.get("status") or "")
    outcome = event.get("outcome")
    if status != "resolved" or outcome not in {"yes", "no"}:
        return None, True
    resolved = _parse_date(str(event.get("resolved_date") or ""))
    anchor = _parse_date(anchor_date)
    if not resolved or not anchor:
        return None, True
    if resolved <= anchor:
        return str(outcome), False
    return None, True

def _timestamps_to_anchor(timeline_event: dict[str, Any] | None, anchor_date: str) -> list[str]:
    anchor = _parse_date(anchor_date)
    if not anchor:
        return [anchor_date]
    dates: list[str] = []
    for entry in _sorted_entries(timeline_event):
        entry_date = _parse_date(str(entry.get("date") or ""))
        if entry_date and entry_date <= anchor:
            dates.append(entry_date.isoformat())
    return dates or [anchor_date]

def _falsifier_model_snapshot(event_id: str, event: dict[str, Any]) -> dict[str, Any]:
    model, distribution_source = effective_falsifier_model(event_id, event)
    modes = model.get("failure_modes") if isinstance(model.get("failure_modes"), list) else []
    slim_modes = []
    for mode in modes:
        if not isinstance(mode, dict):
            continue
        slim_modes.append(
            {
                "id": mode.get("id"),
                "probability": mode.get("probability"),
            }
        )
    return {
        "distribution_source": distribution_source,
        "failure_modes": slim_modes,
    }

def build_task_labels_for_anchor(
    event_id: str,
    event: dict[str, Any],
    *,
    timeline_event: dict[str, Any] | None,
    semantic_block: dict[str, Any] | None,
    anchor_date: str,
    anchor_index: int,
    horizon_days: int = DEFAULT_HORIZON_DAYS,
) -> dict[str, Any]:
    tl = timeline_event if isinstance(timeline_event, dict) else None
    labels: dict[str, Any] = {
        "regime_shift": derive_regime_shift_label(
            timeline_event=tl,
            anchor_date=anchor_date,
            horizon_days=horizon_days,
        ),
        "delta": derive_delta_label(
            event_id,
            event,
            timeline_event=tl,
            semantic_block=semantic_block,
            anchor_date=anchor_date,
            anchor_index=anchor_index,
            horizon_days=horizon_days,
        ),
        "convergence": None,
    }
    voice_states = _voice_states_at_anchor(tl, anchor_date)
    if len(voice_states) >= 2:
        labels["convergence"] = derive_convergence_label(
            event_id,
            event,
            timeline_event=tl,
            semantic_block=semantic_block,
            anchor_date=anchor_date,
            horizon_days=horizon_days,
        )
    delta_block = labels["delta"]
    if isinstance(delta_block, dict):
        labels["delta"] = {
            "bucket": delta_block.get("future_outcome"),
            "delta": delta_block.get("delta"),
            "p_t": delta_block.get("p_t"),
            "p_future": delta_block.get("p_future"),
        }
    return labels

def build_dataset_row(
    event_id: str,
    event: dict[str, Any],
    *,
    timeline_event: dict[str, Any] | None,
    signal_block: dict[str, Any] | None,
    semantic_block: dict[str, Any] | None,
    engm_event: dict[str, Any] | None,
    engm_latent: dict[str, Any] | None,
    anchor_date: str,
    anchor_index: int,
    split_date: str,
    horizon_days: int = DEFAULT_HORIZON_DAYS,
) -> dict[str, Any]:
    signal_vector = build_signal_vector(signal_block, semantic_block)
    outcome, censored = _outcome_at_anchor(event, anchor_date)
    anchor = _parse_date(anchor_date) or date.today()
    split = _parse_date(split_date) or date.fromisoformat(DEFAULT_SPLIT_DATE)
    split_label = "test" if anchor >= split else "train"

    return {
        "event_id": event_id,
        "anchor_date": anchor_date,
        "split": split_label,
        "voice_observations": build_voice_observations(event, timeline_event, anchor_date=anchor_date),
        "latent_features": build_latent_features(
            engm_event=engm_event,
            engm_latent=engm_latent,
            signal_vector=signal_vector,
        ),
        "task_labels": build_task_labels_for_anchor(
            event_id,
            event,
            timeline_event=timeline_event,
            semantic_block=semantic_block,
            anchor_date=anchor_date,
            anchor_index=anchor_index,
            horizon_days=horizon_days,
        ),
        "outcome": outcome,
        "outcome_censored": censored,
        "timestamps": _timestamps_to_anchor(timeline_event, anchor_date),
        "falsifier_model_snapshot": _falsifier_model_snapshot(event_id, event),
        "interpretation": "epistemic_dataset_row",
    }

def temporal_split(rows: list[dict[str, Any]], *, split_date: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    split = _parse_date(split_date) or date.fromisoformat(DEFAULT_SPLIT_DATE)
    train: list[dict[str, Any]] = []
    test: list[dict[str, Any]] = []
    for row in rows:
        anchor = _parse_date(str(row.get("anchor_date") or ""))
        if anchor and anchor >= split:
            test.append(row)
        else:
            train.append(row)
    return train, test

def expand_registry_no_compression(registry: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    expanded = dict(registry)
    for dupe in find_duplicate_fingerprints(registry):
        for event_id in dupe.get("event_ids") or []:
            if event_id in registry:
                expanded[event_id] = registry[event_id]
    try:
        from prediction.compression_engine import MACGREGOR_MERGE_CANDIDATES

        for source_id in MACGREGOR_MERGE_CANDIDATES:
            if source_id in registry:
                expanded[source_id] = registry[source_id]
    except ImportError:
        pass
    return expanded

def build_dataset_rows(
    *,
    registry: dict[str, dict[str, Any]],
    timeline: dict[str, Any],
    signals: dict[str, Any],
    semantic_scores: dict[str, Any],
    engm: dict[str, Any],
    split_date: str = DEFAULT_SPLIT_DATE,
    horizon_days: int = DEFAULT_HORIZON_DAYS,
) -> list[dict[str, Any]]:
    timeline_events = timeline.get("events") if isinstance(timeline, dict) else {}
    signal_events = signals.get("events") if isinstance(signals, dict) else {}
    semantic_events = semantic_scores.get("events") if isinstance(semantic_scores, dict) else {}
    engm_events = engm.get("events") if isinstance(engm, dict) else {}
    engm_latent = engm.get("latent_state") if isinstance(engm, dict) else {}

    if not isinstance(timeline_events, dict):
        timeline_events = {}
    if not isinstance(signal_events, dict):
        signal_events = {}
    if not isinstance(semantic_events, dict):
        semantic_events = {}
    if not isinstance(engm_events, dict):
        engm_events = {}

    rows: list[dict[str, Any]] = []
    for event_id in sorted(registry):
        event = registry[event_id]
        if event.get("not_falsifiable"):
            continue
        if not has_string_falsifier(event) and not has_valid_falsifier_model(event):
            continue

        timeline_event = timeline_events.get(event_id)
        entries = _sorted_entries(timeline_event if isinstance(timeline_event, dict) else None)
        if len(entries) < 2:
            continue

        signal_block = signal_events.get(event_id) if isinstance(signal_events.get(event_id), dict) else {}
        semantic_block = semantic_events.get(event_id) if isinstance(semantic_events.get(event_id), dict) else {}
        engm_event = engm_events.get(event_id) if isinstance(engm_events.get(event_id), dict) else None

        for anchor_index, entry in enumerate(entries[:-1]):
            anchor_date = str(entry.get("date") or "")
            if not anchor_date:
                continue
            rows.append(
                build_dataset_row(
                    event_id,
                    event,
                    timeline_event=timeline_event if isinstance(timeline_event, dict) else None,
                    signal_block=signal_block,
                    semantic_block=semantic_block,
                    engm_event=engm_event,
                    engm_latent=engm_latent if isinstance(engm_latent, dict) else None,
                    anchor_date=anchor_date,
                    anchor_index=anchor_index,
                    split_date=split_date,
                    horizon_days=horizon_days,
                )
            )
    return rows

def build_dataset_payload(
    *,
    registry: dict[str, dict[str, Any]] | None = None,
    timeline: dict[str, Any] | None = None,
    signals: dict[str, Any] | None = None,
    semantic_scores: dict[str, Any] | None = None,
    engm: dict[str, Any] | None = None,
    split_date: str = DEFAULT_SPLIT_DATE,
    horizon_days: int = DEFAULT_HORIZON_DAYS,
    compression_checked: bool = True,
    include_duplicate_fingerprint_events: bool = False,
) -> dict[str, Any]:
    from prediction_lib import load_event_registry

    events = registry or load_event_registry()
    if include_duplicate_fingerprint_events:
        events = expand_registry_no_compression(events)
        compression_checked = False
    rows = build_dataset_rows(
        registry=events,
        timeline=timeline or {},
        signals=signals or {},
        semantic_scores=semantic_scores or {},
        engm=engm or {},
        split_date=split_date,
        horizon_days=horizon_days,
    )
    train, test = temporal_split(rows, split_date=split_date)
    total = len(rows)

    return {
        "_meta": {
            "generated": True,
            "do_not_edit": True,
            "source": "scripts/build_epistemic_dataset.py",
            "phase": "pr4-advisory",
            "dataset_source": "heuristic_v1",
            "split_date": split_date,
            "split_strategy": "temporal_anchor",
            "horizon_days": horizon_days,
            "label_policy": (
                "task_labels are future-facing supervision from timeline anchors; "
                "outcome is registry yes/no only when resolved_date <= anchor_date"
            ),
            "guarantees": {
                "compression_checked": compression_checked,
                "dedup_policy": "registry_falsifier_gate",
                "falsifier_snapshot": "in_row_only_no_registry_write",
            },
            "dataset_scope": {
                "train_count": len(train),
                "test_count": len(test),
                "row_count": total,
                "low_n_advisory": total < LOW_N_ADVISORY_THRESHOLD,
            },
        },
        "interpretation": "ml_ready_dataset",
        "train": train,
        "test": test,
    }

def main() -> int:
    import argparse
    import json

    from prediction_lib import render_json

    default_timeline = _REPO_ROOT / "runtime" / "artifacts" / "prediction-timeline.json"
    default_signals = _REPO_ROOT / "runtime" / "artifacts" / "prediction-signals.json"
    default_semantic = _REPO_ROOT / "runtime" / "artifacts" / "prediction-semantic-scores.json"
    default_engm = _REPO_ROOT / "runtime" / "artifacts" / "epistemic-generative-state.json"
    default_output = _REPO_ROOT / "runtime" / "artifacts" / "epistemic-dataset.json"

    def _load(path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeline", type=Path, default=default_timeline)
    parser.add_argument("--signals", type=Path, default=default_signals)
    parser.add_argument("--semantic-scores", type=Path, default=default_semantic)
    parser.add_argument("--engm", type=Path, default=default_engm)
    parser.add_argument("--output", type=Path, default=default_output)
    parser.add_argument("--split-date", default=DEFAULT_SPLIT_DATE)
    parser.add_argument("--horizon-days", type=int, default=DEFAULT_HORIZON_DAYS)
    args = parser.parse_args()

    payload = build_dataset_payload(
        timeline=_load(args.timeline),
        signals=_load(args.signals),
        semantic_scores=_load(args.semantic_scores),
        engm=_load(args.engm),
        split_date=args.split_date,
        horizon_days=args.horizon_days,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_json(payload), encoding="utf-8")
    scope = payload["_meta"]["dataset_scope"]
    print(
        f"[ok] wrote {args.output.relative_to(_REPO_ROOT)} "
        f"(train={scope['train_count']}, test={scope['test_count']})"
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
