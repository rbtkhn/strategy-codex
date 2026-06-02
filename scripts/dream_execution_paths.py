#!/usr/bin/env python3
"""Deterministic mission-control learning actions for dream and coffee."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from cadence_learning import ACTION_LABELS, ACTION_ORDER, label_for_action

_ACTION_LABEL_TO_PATH_ID = {
    "confirm": "confirm",
    "test": "test",
    "deepen": "deepen",
    "reframe": "reframe",
}


def _action_meta(action: str) -> tuple[str, str]:
    return label_for_action(action)


def _humanize_reason(reason: str) -> str:
    reason_map = {
        "integrity_or_governance_pressure": "integrity or governance pressure is still live",
        "repeated_unresolved_loop": "a repeated unresolved loop is still live",
        "validated_follow_through": "recent receipts suggest clean follow-through",
        "blocked_outcome": "a blocked outcome should be tested before more motion",
        "underformed_object": "the object is real but still underformed",
        "gate_backlog": "gate backlog suggests the inherited category may be wrong",
        "reentry_heavy": "reentry pressure suggests reframing before another push",
        "calendar_mod4": "the field is quiet enough for ordinary deepening",
    }
    return reason_map.get(reason, reason.replace("_", " "))


def coffee_menu_hint_from_dream(dream: dict[str, Any]) -> str | None:
    action = str(
        dream.get("learning_action_recommendation")
        or (dream.get("execution_paths") or [{}])[int(dream.get("suggested_execution_path_index") or 0)].get("id", "")
    ).strip()
    if not action:
        return None
    letter, label = _action_meta(action)
    reason = str(dream.get("learning_action_reason") or dream.get("execution_path_suggestion_reason") or "").strip()
    bias = str(dream.get("bias_strength") or "soft").strip()
    why = _humanize_reason(reason) if reason else "carry-forward from dream"
    return (
        f"- **Dream -> coffee action:** lean **{letter} - {label}** "
        f"({bias}) - {why}; operational hint only (not policy or Record)."
    )


def build_execution_paths(
    *,
    user_id: str,
    now_utc: datetime | None = None,
    integrity_ok: bool = True,
    governance_ok: bool = True,
    reviewable_count: int = 0,
    contradiction_count: int = 0,
    coffee_count_24h: int = 0,
    gate_pending_count: int = 0,
    max_pending_candidates: int | None = None,
    coffee_recursion: dict[str, Any] | None = None,
) -> tuple[list[dict[str, Any]], int, str]:
    del user_id, now_utc

    last_close = (coffee_recursion or {}).get("last_close") or {}
    repeated = (coffee_recursion or {}).get("repeated_unresolved_loops") or []
    readiness = str(last_close.get("readiness") or "").strip()
    outcome = str(last_close.get("outcome") or "").strip()

    suggested_action = "deepen"
    suggestion_reason = "calendar_mod4"

    if not integrity_ok or not governance_ok:
        suggested_action = "test"
        suggestion_reason = "integrity_or_governance_pressure"
    elif repeated:
        suggested_action = "test"
        suggestion_reason = "repeated_unresolved_loop"
    elif outcome == "done" and readiness in {"ship_ready", "execution_ready"}:
        suggested_action = "confirm"
        suggestion_reason = "validated_follow_through"
    elif outcome == "blocked" or readiness == "blocked":
        suggested_action = "test"
        suggestion_reason = "blocked_outcome"
    elif reviewable_count > 0 or contradiction_count > 0:
        suggested_action = "deepen"
        suggestion_reason = "underformed_object"
    elif max_pending_candidates is not None and gate_pending_count > int(max_pending_candidates):
        suggested_action = "reframe"
        suggestion_reason = "gate_backlog"
    elif coffee_count_24h >= 5:
        suggested_action = "reframe"
        suggestion_reason = "reentry_heavy"

    suggested_index = ACTION_ORDER.index(suggested_action)
    paths: list[dict[str, Any]] = [
        {
            "id": "confirm",
            "title": "Confirm the current line and follow through",
            "first_move": "Use recent receipts to validate and execute the next move.",
            "stop_rule": "Stop once the prior judgment is either validated or clearly no longer live.",
            "signals_used": ["outcome_receipts", "artifact_overlap", "dream_confidence"],
        },
        {
            "id": "test",
            "title": "Test the current frame before deepening it",
            "first_move": "Probe the strongest uncertainty or blocker first.",
            "stop_rule": "Stop once one bounded falsifier materially sharpens the field.",
            "signals_used": ["blocked_outcomes", "repeated_loops", "dream_mismatch"],
        },
        {
            "id": "deepen",
            "title": "Deepen the object until the model is good enough to act",
            "first_move": "Clarify mechanism, object shape, or missing context.",
            "stop_rule": "Stop when the object is clear enough for a later confirm or test.",
            "signals_used": ["reviewable_digest", "low_readiness", "object_formation"],
        },
        {
            "id": "reframe",
            "title": "Reframe when the inherited category is wrong",
            "first_move": "Question the object, menu, or carry-forward assumption itself.",
            "stop_rule": "Stop once a better object or better frame replaces the stale one.",
            "signals_used": ["category_drift", "stale_inheritance", "pattern_watch"],
        },
    ]
    return paths, suggested_index, suggestion_reason


def format_tomorrow_inherits_line(
    paths: list[dict[str, Any]],
    suggested_index: int,
    suggestion_reason: str,
    *,
    carry_forward_object: str = "",
    carry_forward_test: str = "",
) -> str:
    idx = max(0, min(suggested_index, len(paths) - 1)) if paths else 0
    path = paths[idx] if paths else {}
    action = str(path.get("id") or "")
    _letter, label = _action_meta(action)

    reason_text = _humanize_reason(suggestion_reason)
    if carry_forward_object and carry_forward_test:
        return (
            f"Tomorrow inherits (hint): **{label}** - object: {carry_forward_object}; "
            f"next test: {carry_forward_test}; {reason_text}; not policy or Record."
        )
    if carry_forward_object:
        return (
            f"Tomorrow inherits (hint): **{label}** - object: {carry_forward_object}; "
            f"{reason_text}; not policy or Record."
        )
    return f"Tomorrow inherits (hint): **{label}** - {reason_text}; not policy or Record."


def build_learning_stage(
    *,
    paths: list[dict[str, Any]],
    suggested_index: int,
    suggestion_reason: str,
    coffee_recursion: dict[str, Any] | None = None,
    integrity_ok: bool = True,
    governance_ok: bool = True,
    extra_followups: list[str] | None = None,
) -> dict[str, str]:
    path = paths[max(0, min(suggested_index, len(paths) - 1))] if paths else {}
    action = str(path.get("id") or "deepen")
    repeated = (coffee_recursion or {}).get("repeated_unresolved_loops") or []
    last_close = (coffee_recursion or {}).get("last_close") or {}
    readiness = str(last_close.get("readiness") or "").strip()
    next_step = str(last_close.get("next") or "").strip()
    artifacts = str(last_close.get("artifacts") or "").strip()

    if not integrity_ok or not governance_ok:
        carry_object = "integrity / governance repair"
        carry_test = "Do the checks pass cleanly on the next coffee?"
        confidence = "high"
        bias = "strong"
    elif repeated:
        carry_object = repeated[0].get("loop", "repeated unresolved loop")
        carry_test = "Does the next move reduce this loop instead of repeating it?"
        confidence = "high"
        bias = "strong"
    elif readiness in {"ship_ready", "execution_ready"} and next_step:
        carry_object = next_step
        carry_test = "Is the prior judgment still live enough to follow through cleanly?"
        confidence = "medium"
        bias = "soft"
    elif extra_followups:
        carry_object = extra_followups[0][:120]
        carry_test = "Can the next coffee turn this into one bounded action or falsifier?"
        confidence = "medium"
        bias = "soft"
    elif artifacts:
        carry_object = artifacts.split(",")[0]
        carry_test = "Does this still look like the right object tomorrow morning?"
        confidence = "low"
        bias = "quiet"
    else:
        carry_object = "the live object is still underformed"
        carry_test = "What single move would make the field less ambiguous?"
        confidence = "low"
        bias = "quiet"

    return {
        "learning_action_recommendation": action,
        "learning_action_reason": _humanize_reason(suggestion_reason),
        "carry_forward_object": carry_object,
        "carry_forward_test": carry_test,
        "confidence_class": confidence,
        "bias_strength": bias,
    }
