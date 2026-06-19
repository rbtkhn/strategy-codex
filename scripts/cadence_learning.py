#!/usr/bin/env python3
"""WORK-only cadence learning ledger for coffee and dream."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from repo_io import profile_dir, resolve_ledger_path

LEDGER_NAME = "cadence-learning-events.jsonl"
ACTION_ORDER = ("confirm", "test", "deepen", "reframe")
ACTION_LABELS = {
    "confirm": ("A", "Confirm"),
    "test": ("B", "Test"),
    "deepen": ("C", "Deepen"),
    "reframe": ("D", "Reframe"),
}
LETTER_TO_ACTION = {letter: action for action, (letter, _label) in ACTION_LABELS.items()}


def default_ledger_path(user_id: str) -> Path:
    return resolve_ledger_path(user_id, LEDGER_NAME)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def label_for_action(action: str) -> tuple[str, str]:
    return ACTION_LABELS.get(action, ("?", action.title() if action else "Unknown"))


def action_for_letter(letter: str | None) -> str:
    if not letter:
        return ""
    return LETTER_TO_ACTION.get(str(letter).strip().upper(), "")


def append_learning_event(
    user_id: str,
    event_type: str,
    payload: dict[str, Any],
    *,
    ledger_path: Path | None = None,
) -> Path:
    path = ledger_path or default_ledger_path(user_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    row = {
        "ts": utc_now_iso(),
        "user_id": user_id,
        "event_type": event_type,
        **payload,
    }
    with open(path, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    return path


def load_learning_events(user_id: str, *, ledger_path: Path | None = None) -> list[dict[str, Any]]:
    path = ledger_path or default_ledger_path(user_id)
    if not path.is_file():
        return []
    rows: list[dict[str, Any]] = []
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if str(row.get("user_id") or "") != user_id:
                continue
            rows.append(row)
    return rows


def _last_unlinked_dream_stage(events: list[dict[str, Any]]) -> dict[str, Any] | None:
    linked = {
        str(row.get("dream_id"))
        for row in events
        if row.get("event_type") == "coffee_choice" and row.get("dream_id")
    }
    for row in reversed(events):
        if row.get("event_type") != "dream_stage":
            continue
        dream_id = str(row.get("dream_id") or "")
        if dream_id and dream_id not in linked:
            return row
    return None


def _last_unresolved_coffee_choice(events: list[dict[str, Any]]) -> dict[str, Any] | None:
    resolved = {
        str(row.get("coffee_id"))
        for row in events
        if row.get("event_type") == "coffee_resolution" and row.get("coffee_id")
    }
    for row in reversed(events):
        if row.get("event_type") != "coffee_choice":
            continue
        coffee_id = str(row.get("coffee_id") or "")
        if coffee_id and coffee_id not in resolved:
            return row
    return None


def log_dream_stage(
    user_id: str,
    *,
    handoff: dict[str, Any],
    ledger_path: Path | None = None,
) -> Path:
    action = str(handoff.get("learning_action_recommendation") or "").strip()
    letter, label = label_for_action(action)
    dream_id = str(handoff.get("generated_at") or utc_now_iso())
    payload = {
        "dream_id": dream_id,
        "dream_generated_at": handoff.get("generated_at"),
        "learning_action_recommendation": action,
        "predicted_menu_letter": letter,
        "predicted_menu_label": label,
        "learning_action_reason": handoff.get("learning_action_reason", ""),
        "carry_forward_object": handoff.get("carry_forward_object", ""),
        "carry_forward_test": handoff.get("carry_forward_test", ""),
        "confidence_class": handoff.get("confidence_class", ""),
        "bias_strength": handoff.get("bias_strength", ""),
        "tomorrow_inherits": handoff.get("tomorrow_inherits", ""),
        "source_ref": "last-dream.json",
    }
    return append_learning_event(user_id, "dream_stage", payload, ledger_path=ledger_path)


def log_coffee_choice_start(
    user_id: str,
    *,
    coffee_id: str,
    load_result: dict[str, Any],
    ledger_path: Path | None = None,
) -> Path:
    events = load_learning_events(user_id, ledger_path=ledger_path)
    dream_stage = _last_unlinked_dream_stage(events)
    action = str(load_result.get("recommended_action") or "").strip()
    letter, label = label_for_action(action)
    payload = {
        "coffee_id": coffee_id,
        "recommended_learning_action": action,
        "recommended_menu_letter": letter,
        "recommended_menu_label": label,
        "recommendation_reason": load_result.get("recommendation_reason", ""),
        "recommendation_source": load_result.get("recommendation_source", "assess_session_load"),
        "dream_id": str((dream_stage or {}).get("dream_id") or ""),
        "dream_recommendation": str((dream_stage or {}).get("learning_action_recommendation") or ""),
        "downstream_hint": str(load_result.get("downstream_hint") or ""),
        "source_ref": "operator_coffee",
    }
    return append_learning_event(user_id, "coffee_choice", payload, ledger_path=ledger_path)


def _hindsight_from_close(outcome: str, readiness: str) -> str:
    if outcome == "done" and readiness in {"ship_ready", "execution_ready"}:
        return "validated"
    if outcome == "partial":
        return "partially_validated"
    if outcome in {"blocked", "parked"} or readiness == "blocked":
        return "invalidated"
    return "still_open"


def _lesson_candidate(actual_action: str, hindsight: str, loops: list[str]) -> str:
    if actual_action == "confirm" and hindsight in {"invalidated", "still_open"}:
        return "We kept confirming before the slice proved itself. Recommended adjustment: test before confirm."
    if actual_action == "deepen" and hindsight == "invalidated":
        return "We kept deepening an unstable frame. Recommended adjustment: test before deepen."
    if actual_action == "test" and hindsight == "validated" and loops:
        return f"Testing helped on recurring loop `{loops[0]}`. Preserve that move."
    if actual_action == "reframe" and hindsight == "validated":
        return "Reframing improved the next move. Preserve category repair when the field feels stale."
    return ""


def log_coffee_resolution_from_close(
    user_id: str,
    *,
    picked: str,
    outcome: str,
    readiness: str,
    artifacts: list[str] | None = None,
    loops: list[str] | None = None,
    next_slug: str | None = None,
    ledger_path: Path | None = None,
) -> Path | None:
    events = load_learning_events(user_id, ledger_path=ledger_path)
    choice = _last_unresolved_coffee_choice(events)
    if choice is None:
        return None

    actual_action = action_for_letter(picked)
    hindsight = _hindsight_from_close(outcome, readiness)
    dream_action = str(choice.get("dream_recommendation") or "")
    match_class = "unresolved"
    if dream_action and actual_action:
        if dream_action == actual_action:
            match_class = "confirmed"
        elif actual_action in {"confirm", "test"} and dream_action in {"confirm", "test"}:
            match_class = "partial"
        else:
            match_class = "missed"

    loop_list = [item for item in (loops or []) if str(item).strip()]
    payload = {
        "coffee_id": choice.get("coffee_id", ""),
        "dream_id": choice.get("dream_id", ""),
        "actual_menu_letter": picked,
        "actual_learning_action": actual_action,
        "recommended_learning_action": choice.get("recommended_learning_action", ""),
        "recommendation_followed": str(
            bool(actual_action and actual_action == choice.get("recommended_learning_action"))
        ).lower(),
        "dream_match_class": match_class,
        "outcome": outcome,
        "readiness": readiness,
        "hindsight_class": hindsight,
        "runtime/artifacts": ",".join(artifacts or []),
        "loops": ",".join(loop_list),
        "next": next_slug or "",
        "lesson_candidate": _lesson_candidate(actual_action, hindsight, loop_list),
        "source_ref": "coffee_close",
    }
    return append_learning_event(user_id, "coffee_resolution", payload, ledger_path=ledger_path)


def build_pattern_watch(user_id: str, *, ledger_path: Path | None = None) -> dict[str, str] | None:
    events = load_learning_events(user_id, ledger_path=ledger_path)
    resolutions = [row for row in events if row.get("event_type") == "coffee_resolution"]
    if len(resolutions) < 2:
        return None
    recent = resolutions[-2:]
    actual = [str(row.get("actual_learning_action") or "") for row in recent]
    hindsight = [str(row.get("hindsight_class") or "") for row in recent]
    if actual == ["confirm", "confirm"] and all(
        item in {"invalidated", "still_open", "partially_validated"} for item in hindsight
    ):
        return {
            "pattern": "repeated_premature_confirm",
            "message": "Pattern watch: we keep confirming before the slice really proves itself.",
            "recommended_action": "test",
            "adjustment": "Recommended adjustment: test before confirm.",
        }
    if actual == ["deepen", "deepen"] and all(item in {"invalidated", "partially_validated"} for item in hindsight):
        return {
            "pattern": "repeated_unstable_deepen",
            "message": "Pattern watch: we keep deepening before the frame is stable enough.",
            "recommended_action": "test",
            "adjustment": "Recommended adjustment: test before deepen.",
        }
    dream_matches = [str(row.get("dream_match_class") or "") for row in recent]
    if all(item == "missed" for item in dream_matches):
        return {
            "pattern": "dream_mismatch_streak",
            "message": "Pattern watch: dream has missed the last two realized coffee moves.",
            "recommended_action": "reframe",
            "adjustment": "Recommended adjustment: reframe before inheriting the dream seam again.",
        }
    return None


def summarize_learning(user_id: str, *, ledger_path: Path | None = None) -> dict[str, Any]:
    events = load_learning_events(user_id, ledger_path=ledger_path)
    by_type = {"dream_stage": 0, "coffee_choice": 0, "coffee_resolution": 0}
    dream_matches: dict[str, int] = {}
    hindsight: dict[str, int] = {}
    action_counts: dict[str, int] = {}
    for row in events:
        event_type = str(row.get("event_type") or "")
        if event_type in by_type:
            by_type[event_type] += 1
        match_class = str(row.get("dream_match_class") or "")
        if match_class:
            dream_matches[match_class] = dream_matches.get(match_class, 0) + 1
        hindsight_class = str(row.get("hindsight_class") or "")
        if hindsight_class:
            hindsight[hindsight_class] = hindsight.get(hindsight_class, 0) + 1
        action = str(row.get("actual_learning_action") or row.get("recommended_learning_action") or "")
        if action:
            action_counts[action] = action_counts.get(action, 0) + 1
    return {
        "counts": by_type,
        "dream_match_classes": dream_matches,
        "hindsight_classes": hindsight,
        "action_counts": action_counts,
        "pattern_watch": build_pattern_watch(user_id, ledger_path=ledger_path),
        "events": events,
    }
