"""Phase 3 prediction data contracts — SSOT enums and normalizers."""

from __future__ import annotations

from typing import Any

EVENT_TYPES = frozenset({"atomic", "trajectory"})
PREDICTION_TYPES = frozenset(
    {"falsifiable_claim", "probabilistic_claim", "trajectory", "not_falsifiable"}
)
HORIZONS = frozenset({"short", "medium", "long"})
OUTCOME_RECORDS = frozenset(
    {"pending", "correct", "incorrect", "mixed", "not_scorable"}
)
SEMANTIC_SHIFT_TYPES = frozenset(
    {"stance_shift", "mechanism_shift", "horizon_shift", "contradiction"}
)

ISRAEL_CHILD_IDS = (
    "israel_moral_pariah_status",
    "israel_regional_isolation",
    "israel_us_support_erosion",
    "israel_military_overextension",
    "israel_economic_emigration_pressure",
    "israel_internal_political_fragmentation",
)


def infer_horizon(event: dict[str, Any]) -> str:
    if event.get("horizon"):
        return str(event["horizon"])
    start = str(event.get("start_date") or "")
    if start >= "2025-06-01":
        return "short"
    if start >= "2024-01-01":
        return "medium"
    return "long"


def infer_prediction_type(event: dict[str, Any]) -> str:
    if event.get("prediction_type") in PREDICTION_TYPES:
        return str(event["prediction_type"])
    if event.get("not_falsifiable") is True:
        return "not_falsifiable"
    dims = event.get("dimensions") or []
    if dims or str(event.get("event_type") or "") == "trajectory":
        return "trajectory"
    return "falsifiable_claim"


def infer_event_type(event: dict[str, Any]) -> str:
    if event.get("event_type") in EVENT_TYPES:
        return str(event["event_type"])
    dims = event.get("dimensions") or []
    if dims:
        return "trajectory"
    if "trajectory" in str(event.get("event_id") or ""):
        return "trajectory"
    return "atomic"


def infer_outcome_record(event: dict[str, Any]) -> str:
    if event.get("outcome_record") in OUTCOME_RECORDS:
        return str(event["outcome_record"])
    status = str(event.get("status") or "open")
    if status in {"void", "deprecated"}:
        return "not_scorable"
    if status != "resolved":
        return "pending"
    outcome = event.get("outcome")
    if outcome in {"yes", "no"}:
        return "correct"
    return "mixed"


def normalize_event_v4(event_id: str, event: dict[str, Any]) -> dict[str, Any]:
    out = dict(event)
    out.pop("parent_event_id", None)
    out.pop("child_event_ids", None)
    out["event_type"] = infer_event_type(out)
    out["prediction_type"] = infer_prediction_type(out)
    out["horizon"] = infer_horizon(out)
    out["outcome_record"] = infer_outcome_record(out)
    if not out.get("first_seen"):
        out["first_seen"] = str(out.get("start_date") or "")
    if not out.get("last_seen"):
        out["last_seen"] = str(out.get("resolved_date") or out.get("start_date") or "")
    return out


def predictive_fingerprint(event_id: str, event: dict[str, Any]) -> tuple[str, ...]:
    event_type = infer_event_type(event)
    horizon = infer_horizon(event)
    falsifier = str(event.get("falsifier") or "").strip().casefold()
    mechanism = str(event.get("mechanism_tag") or "unknown").strip().casefold()
    question = str(event.get("question") or event_id).strip().casefold()
    if event_type == "trajectory":
        dim_ids = tuple(sorted(str(d.get("id") or "") for d in (event.get("dimensions") or [])))
        return ("trajectory", question, falsifier, horizon, mechanism, dim_ids)
    return ("atomic", question, falsifier, horizon, mechanism)


def find_duplicate_fingerprints(
    events: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    by_fp: dict[tuple[str, ...], list[str]] = {}
    for event_id, event in events.items():
        fp = predictive_fingerprint(event_id, event)
        by_fp.setdefault(fp, []).append(event_id)
    dupes: list[dict[str, Any]] = []
    for fp, ids in sorted(by_fp.items()):
        if len(ids) > 1:
            dupes.append({"fingerprint": fp, "event_ids": ids})
    return dupes


def fingerprint_gate_errors(events: dict[str, dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    for dupe in find_duplicate_fingerprints(events):
        ids = dupe["event_ids"]
        active = [
            eid
            for eid in ids
            if str(events.get(eid, {}).get("status") or "") != "deprecated"
        ]
        if len(active) > 1:
            errors.append(f"duplicate predictive fingerprint: {active}")
    return errors


def upsert_fingerprint_collision(
    event_id: str,
    event: dict[str, Any],
    registry: dict[str, dict[str, Any]],
) -> list[str]:
    normalized = normalize_event_v4(event_id, event)
    fp = predictive_fingerprint(event_id, normalized)
    errors: list[str] = []
    for other_id, other in registry.items():
        if other_id == event_id:
            continue
        if str(other.get("status") or "") == "deprecated":
            continue
        if predictive_fingerprint(other_id, other) == fp:
            errors.append(f"{event_id}: fingerprint collision with {other_id}")
    return errors


def map_speech_act_to_semantic(speech_act: str | None, *, stance_flip: bool = False) -> str:
    act = str(speech_act or "").strip()
    if stance_flip and act not in {"restated", "self_acknowledged_correct", "self_acknowledged_incorrect"}:
        return "contradiction"
    if act in {"initial", "iterated"}:
        return "assertion"
    if act in {"restated", "self_acknowledged_correct", "self_acknowledged_incorrect"}:
        return "revision"
    if act == "outcome_commentary":
        return "hedge"
    return "assertion"
