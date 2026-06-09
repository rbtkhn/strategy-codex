#!/usr/bin/env python3
"""Assess coffee session load and recommend a mission-control learning action."""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from cadence_learning import ACTION_LABELS, build_pattern_watch
from repo_io import DEFAULT_PROFILE_ID, profile_dir

DEFAULT_USER = DEFAULT_PROFILE_ID
ACTION_BY_LETTER = {letter: action for action, (letter, _label) in ACTION_LABELS.items()}
LABEL_BY_LETTER = {letter: label for _action, (letter, label) in ACTION_LABELS.items()}


def _collect_cadence_today(user_id: str) -> dict[str, Any] | None:
    try:
        from audit_cadence_rhythm import parse_events
    except ImportError:
        from scripts.audit_cadence_rhythm import parse_events  # type: ignore

    now = datetime.now(timezone.utc)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_events = [e for e in parse_events(user_id) if e["dt"] >= today_start]
    by_kind: dict[str, int] = {}
    for event in today_events:
        by_kind[event["kind"]] = by_kind.get(event["kind"], 0) + 1
    return {
        "total": len(today_events),
        "coffees": by_kind.get("coffee", 0),
        "bridges": by_kind.get("bridge", 0),
        "dreams": by_kind.get("dream", 0),
        "by_kind": by_kind,
    }


def _collect_gate_depth(user_id: str) -> dict[str, int] | None:
    gate_path = profile_dir(user_id) / "recursion-gate.md"
    if not gate_path.is_file():
        return None
    try:
        from gate_block_parser import iter_candidate_yaml_blocks, pending_candidates_region
    except ImportError:
        from scripts.gate_block_parser import iter_candidate_yaml_blocks, pending_candidates_region  # type: ignore
    content = gate_path.read_text(encoding="utf-8")
    pending = len(list(iter_candidate_yaml_blocks(pending_candidates_region(content))))
    return {"pending": pending}


def _collect_capture_gap(user_id: str) -> dict[str, Any] | None:
    try:
        from detect_capture_gap import detect_gap
    except ImportError:
        try:
            from scripts.detect_capture_gap import detect_gap  # type: ignore
        except ImportError:
            return None
    return detect_gap(user_id)


def _collect_dream_quality(user_id: str) -> dict[str, Any] | None:
    dream_path = profile_dir(user_id) / "last-dream.json"
    if not dream_path.is_file():
        return None
    try:
        data = json.loads(dream_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return {
        "integrity_ok": data.get("integrity_ok", True),
        "governance_ok": data.get("governance_ok", True),
        "contradiction_count": data.get("contradiction_count", 0),
        "reviewable_count": data.get("reviewable_count", 0),
        "followup_count": len(data.get("followups", [])),
        "ok": data.get("ok", True),
        "learning_action_recommendation": data.get("learning_action_recommendation", ""),
        "learning_action_reason": data.get("learning_action_reason", ""),
        "confidence_class": data.get("confidence_class", ""),
        "bias_strength": data.get("bias_strength", ""),
    }


def _collect_coffee_recursion(user_id: str) -> dict[str, Any] | None:
    try:
        from audit_cadence_rhythm import compute_coffee_recursion_summary
    except ImportError:
        try:
            from scripts.audit_cadence_rhythm import compute_coffee_recursion_summary  # type: ignore
        except ImportError:
            return None
    return compute_coffee_recursion_summary(user_id, days=14)


def _collect_branch_count() -> int:
    import subprocess

    try:
        result = subprocess.run(
            ["git", "branch"],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
            timeout=5,
            check=False,
        )
    except Exception:
        return 0
    branches = [
        line.strip()
        for line in result.stdout.splitlines()
        if line.strip() and not line.strip().lstrip("* ").startswith("main")
    ]
    return len(branches)


def _collect_changed_paths() -> list[str]:
    import subprocess

    changed: set[str] = set()

    def _run_git(args: list[str]) -> None:
        try:
            result = subprocess.run(
                ["git", *args],
                capture_output=True,
                text=True,
                cwd=str(REPO_ROOT),
                timeout=5,
                check=False,
            )
        except Exception:
            return
        if result.returncode != 0:
            return
        for raw in result.stdout.splitlines():
            item = raw.strip()
            if item:
                changed.add(item.replace("\\", "/"))

    _run_git(["diff", "--name-only", "origin/main..HEAD"])
    _run_git(["diff", "--name-only"])
    _run_git(["ls-files", "--others", "--exclude-standard"])
    return sorted(changed)


def _time_of_day_energy() -> str:
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "morning"
    if 12 <= hour < 17:
        return "afternoon"
    return "evening"


def _artifacts_overlap_current_changes(
    artifacts: list[str] | tuple[str, ...] | None, changed_paths: list[str] | None
) -> bool:
    if changed_paths is None:
        return bool(artifacts)
    if not artifacts or not changed_paths:
        return False
    normalized_changes = tuple(path.replace("\\", "/") for path in changed_paths)
    for artifact in artifacts:
        candidate = str(artifact).strip().replace("\\", "/").rstrip("/")
        if not candidate:
            continue
        if any(
            path == candidate or path.startswith(candidate + "/") or candidate.startswith(path + "/")
            for path in normalized_changes
        ):
            return True
    return False


def _compute_load_level(
    cadence: dict[str, Any] | None,
    gate: dict[str, Any] | None,
    gap: dict[str, Any] | None,
    dream: dict[str, Any] | None,
) -> tuple[str, list[str]]:
    weight = 0
    signals: list[str] = []
    if cadence:
        coffees = int(cadence.get("coffees", 0) or 0)
        if coffees >= 4:
            weight += 2
            signals.append(f"{coffees} coffees today (reorientation pressure)")
        elif coffees >= 2:
            weight += 1
            signals.append(f"{coffees} coffees today")
    if gate:
        pending = int(gate.get("pending", 0) or 0)
        if pending >= 5:
            weight += 2
            signals.append(f"{pending} pending gate candidates")
        elif pending >= 2:
            weight += 1
            signals.append(f"{pending} pending gate candidates")
    if gap:
        level = gap.get("level", "ok")
        days = gap.get("days_since_evidence")
        if level == "alert":
            weight += 2
            signals.append(f"capture gap alert ({days}d)")
        elif level == "warning":
            weight += 1
            signals.append(f"capture gap warning ({days}d)")
    if dream:
        if not dream.get("integrity_ok", True) or not dream.get("governance_ok", True):
            weight += 2
            signals.append("dream integrity/governance pressure")
        elif dream.get("followup_count", 0):
            weight += 1
            signals.append(f"{dream['followup_count']} dream followup(s)")
    if _time_of_day_energy() == "evening":
        weight += 1
        signals.append("evening session")

    if weight >= 5:
        return "heavy", signals
    if weight >= 2:
        return "moderate", signals
    return "light", signals


def _compute_option_weights(
    load_level: str,
    gate: dict[str, Any] | None,
    branch_count: int,
    coffee_recursion: dict[str, Any] | None = None,
    changed_paths: list[str] | None = None,
) -> dict[str, dict[str, str]]:
    pending = int((gate or {}).get("pending", 0) or 0)
    weights: dict[str, dict[str, str]] = {
        "A": {"cost": "light", "note": "Confirm - validate follow-through when prior judgment still looks right"},
        "B": {"cost": "moderate", "note": "Test - falsify blockers, repeated loops, or unstable assumptions"},
        "C": {"cost": "light", "note": "Deepen - clarify the object until the model is good enough to act"},
        "D": {"cost": "moderate", "note": "Reframe - change the object or category when the inherited frame looks wrong"},
    }

    if branch_count >= 3:
        weights["D"] = {"cost": "heavy", "note": f"Reframe - {branch_count} branches suggest stale context or split attention"}
    elif branch_count >= 1:
        weights["D"]["note"] = f"Reframe - {branch_count} non-main branch(es) may signal category drift"

    if pending >= 5:
        weights["D"]["cost"] = "moderate"
        weights["D"]["note"] = f"Reframe - {pending} pending items suggest inherited routing may be too narrow"
    elif pending >= 1:
        weights["C"]["note"] = f"Deepen - {pending} pending candidate(s) imply underformed judgment"

    last_close = (coffee_recursion or {}).get("last_close") or {}
    readiness = str(last_close.get("readiness") or "").strip()
    artifacts = last_close.get("artifacts") or []
    artifacts_live = _artifacts_overlap_current_changes(artifacts, changed_paths)
    if readiness == "ship_ready":
        if artifacts_live:
            weights["A"]["note"] = "Confirm - last close is ship_ready and still lines up with current work"
        else:
            weights["D"]["note"] = "Reframe - ship-ready receipt exists, but current changes moved on"
        weights["A"]["cost"] = "light"
    elif readiness == "execution_ready" and artifacts_live:
        weights["A"]["note"] = "Confirm - last close is execution_ready on a still-live slice"
        weights["A"]["cost"] = "light"
    elif readiness == "blocked":
        weights["B"]["note"] = "Test - last close is blocked and should be falsified before more motion"
        weights["B"]["cost"] = "light"
    elif readiness == "orientation":
        weights["C"]["note"] = "Deepen - last close was orientation-only and the object still needs shape"
        weights["C"]["cost"] = "light"

    if load_level == "heavy":
        weights["C"]["cost"] = "light"
    return weights


def _pick_recommendation(
    load_level: str,
    weights: dict[str, dict[str, str]],
    signals: list[str],
    coffee_recursion: dict[str, Any] | None = None,
    changed_paths: list[str] | None = None,
    dream: dict[str, Any] | None = None,
    user_id: str = DEFAULT_USER,
) -> tuple[str, str]:
    last_close = (coffee_recursion or {}).get("last_close") or {}
    readiness = str(last_close.get("readiness") or "").strip()
    outcome = str(last_close.get("outcome") or "").strip()
    artifacts = last_close.get("artifacts") or []
    artifacts_live = _artifacts_overlap_current_changes(artifacts, changed_paths)
    repeated = (coffee_recursion or {}).get("repeated_unresolved_loops") or []

    if readiness == "ship_ready":
        if not artifacts_live:
            return "D", "ship-ready receipt exists, but current changes no longer match that slice"
        return "A", "validated follow-through pressure from a still-live ship-ready slice"
    if readiness == "execution_ready" and artifacts_live:
        return "A", "validated follow-through pressure from a still-live execution-ready slice"
    if repeated:
        return "B", f"repeated unresolved loop pressure ({repeated[0]['loop']}) should be tested before more motion"
    if readiness == "orientation":
        return "C", "the object is still orientation-only and should be deepened before commitment"
    if readiness == "blocked" or outcome == "blocked":
        return "B", "the last close blocked, so the current frame should be tested before another push"
    if outcome == "partial":
        return "B", "the last close only partially landed, so the remaining frame should be tested"

    pattern_watch = build_pattern_watch(user_id)
    if pattern_watch and pattern_watch.get("recommended_action"):
        reverse = {"confirm": "A", "test": "B", "deepen": "C", "reframe": "D"}
        action = reverse.get(str(pattern_watch["recommended_action"]))
        if action:
            return action, f"{pattern_watch['message']} {pattern_watch['adjustment']}"

    if dream:
        action = str(dream.get("learning_action_recommendation") or "").strip()
        bias = str(dream.get("bias_strength") or "").strip()
        reverse = {"confirm": "A", "test": "B", "deepen": "C", "reframe": "D"}
        if action in reverse and bias in {"strong", "soft"}:
            return reverse[action], str(dream.get("learning_action_reason") or "dream carry-forward")

    if load_level == "heavy":
        return "C", "heavy load - deepen the object instead of forcing a false conclusion"
    if load_level == "moderate":
        return "C", "moderate load - deepen keeps the next move bounded without overcommitting"
    if "capture gap warning" in " ".join(signals).lower():
        return "B", "light load, but a capture gap warning makes testing safer than premature confirmation"
    return "C", "light load - good conditions to deepen the live object before a harder commitment"


def assess_load(user_id: str) -> dict[str, Any]:
    try:
        from strategy_codex_config import record_frozen
    except ImportError:
        from scripts.strategy_codex_config import record_frozen  # type: ignore
    frozen = record_frozen()
    cadence = _collect_cadence_today(user_id)
    gate = None if frozen else _collect_gate_depth(user_id)
    gap = None if frozen else _collect_capture_gap(user_id)
    dream = _collect_dream_quality(user_id)
    coffee_recursion = _collect_coffee_recursion(user_id)
    branch_count = _collect_branch_count()
    changed_paths = _collect_changed_paths()

    load_level, signals = _compute_load_level(cadence, gate, gap, dream)
    weights = _compute_option_weights(load_level, gate, branch_count, coffee_recursion, changed_paths)
    recommended, reason = _pick_recommendation(
        load_level,
        weights,
        signals,
        coffee_recursion=coffee_recursion,
        changed_paths=changed_paths,
        dream=dream,
        user_id=user_id,
    )
    pattern_watch = build_pattern_watch(user_id)

    return {
        "load_level": load_level,
        "signals": signals,
        "option_weights": weights,
        "recommended": recommended,
        "recommended_action": ACTION_BY_LETTER.get(recommended, ""),
        "recommendation_reason": reason,
        "recommendation_source": "assess_session_load",
        "downstream_hint": weights.get(recommended, {}).get("note", ""),
        "pattern_watch": pattern_watch,
        "time_of_day": _time_of_day_energy(),
        "branch_count": branch_count,
        "changed_paths": changed_paths,
        "coffee_recursion": coffee_recursion,
        "dream": dream,
    }


def format_load_one_liner(result: dict[str, Any]) -> str:
    level = result.get("load_level", "unknown")
    signals = result.get("signals", [])
    rec = result.get("recommended", "?")
    label = LABEL_BY_LETTER.get(rec, rec)
    summary_parts = signals[:3] if signals else ["no strong signals"]
    return f"Session load: {level.upper()} — {', '.join(summary_parts)} (recommended: {rec} - {label})"


def format_default_acceptance_line(result: dict[str, Any]) -> str:
    rec = result.get("recommended") or "?"
    label = LABEL_BY_LETTER.get(rec, rec)
    reason = result.get("recommendation_reason") or "best current fit"
    return f'Recommended default: {rec} - {label} — say "go" to accept, or pick another hub letter. ({reason})'


def format_annotated_menu(result: dict[str, Any]) -> str:
    weights = result.get("option_weights", {})
    rec = result.get("recommended", "")
    lines = []
    for letter in ("A", "B", "C", "D"):
        weight = weights.get(letter, {"cost": "?", "note": ""})
        label = LABEL_BY_LETTER[letter]
        rec_tag = " recommended" if letter == rec else ""
        lines.append(f"**{letter}. {label}** — ({weight['cost']}){rec_tag}: {weight['note']}")
    pattern_watch = result.get("pattern_watch") or {}
    if pattern_watch.get("message"):
        lines.append(f"Pattern watch: {pattern_watch['message']} {pattern_watch['adjustment']}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Assess coffee session load.")
    parser.add_argument("-u", "--user", default=os.getenv("GRACE_MAR_USER_ID", DEFAULT_USER).strip() or DEFAULT_USER)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = assess_load(args.user)
    if args.json:
        print(json.dumps(result, indent=2, default=str))
    else:
        print(format_load_one_liner(result))
        print(format_default_acceptance_line(result))
        print()
        print("Annotated menu:")
        print(format_annotated_menu(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
