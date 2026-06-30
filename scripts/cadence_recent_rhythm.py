#!/usr/bin/env python3
"""Shared recent-rhythm formatter for coffee and dream."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from audit_cadence_rhythm import EVENTS_PATH, compute_coffee_recursion_summary, parse_events
    from repo_io import DEFAULT_USER_ID
except ImportError:
    from scripts.audit_cadence_rhythm import EVENTS_PATH, compute_coffee_recursion_summary, parse_events
    from scripts.repo_io import DEFAULT_USER_ID

def _as_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    if value is None:
        return []
    return [part.strip() for part in str(value).split(",") if part.strip()]

def _normalize_repo_path(value: str) -> str:
    return str(value).strip().replace("\\", "/").rstrip("/")

def _artifacts_overlap_changed_paths(
    artifacts: list[str] | tuple[str, ...] | None,
    changed_paths: list[str] | tuple[str, ...] | None,
) -> bool:
    if changed_paths is None:
        return bool(artifacts)
    if not artifacts or not changed_paths:
        return False
    normalized_changes = tuple(_normalize_repo_path(path) for path in changed_paths if str(path).strip())
    for artifact in artifacts:
        candidate = _normalize_repo_path(artifact)
        if not candidate:
            continue
        if any(
            path == candidate or path.startswith(candidate + "/") or candidate.startswith(path + "/")
            for path in normalized_changes
        ):
            return True
    return False

def _summarize_event(event: dict[str, Any]) -> str:
    kind = str(event.get("kind") or "")
    kv = event.get("kv") or {}
    if kind == "coffee_close":
        picked = kv.get("picked") or "a branch"
        outcome = kv.get("outcome") or "an unfinished slice"
        readiness = kv.get("readiness") or "unknown"
        return f"we materially settled {picked} and left it {outcome} with {readiness} readiness"
    if kind == "coffee_pick":
        conductor = kv.get("conductor")
        picked = kv.get("picked")
        if conductor:
            return f"we ran a {conductor} conductor emphasis"
        if picked:
            return f"we chose coffee branch {picked}"
        return "we made a coffee branch choice"
    if kind == "coffee":
        mode = kv.get("mode")
        if mode and mode != "standard":
            return f"we used coffee in {mode} mode"
        return "we reoriented with coffee"
    if kind == "dream":
        ok = str(kv.get("ok") or "").lower()
        if ok == "true":
            return "we already gave the day a consolidation pass"
        return "dream surfaced something that still needs repair"
    if kind == "bridge":
        return "we sealed a session handoff"
    if kind == "harvest":
        return "we packed a harvest handoff"
    if kind == "thanks":
        return "we paused and parked the thread on purpose"
    if kind == "coffee_conductor_outcome":
        verdict = kv.get("verdict") or "an outcome"
        conductor = kv.get("conductor") or "the conductor arc"
        return f"we closed {conductor} with a {verdict} outcome"
    return f"we logged {kind}"

def format_coffee_recent_rhythm(
    user_id: str,
    *,
    days: int = 14,
    events_path: Path = EVENTS_PATH,
    now: datetime | None = None,
    changed_paths: list[str] | None = None,
) -> str:
    now = now or datetime.now(timezone.utc)
    recursion = compute_coffee_recursion_summary(user_id, days=days, events_path=events_path, now=now)
    last_close = recursion.get("last_close")
    lines: list[str] = ["Recent rhythm:"]

    if last_close:
        picked = last_close.get("picked") or "unknown"
        outcome = last_close.get("outcome") or "unknown"
        readiness = last_close.get("readiness") or "unknown"
        next_step = last_close.get("next")
        artifacts = _as_list(last_close.get("artifacts"))
        artifacts_live = _artifacts_overlap_changed_paths(artifacts, changed_paths)
        first = f"- Last close picked {picked}: {outcome}, readiness {readiness}."
        if next_step and artifacts_live:
            first += f" Next: {next_step}."
        elif next_step:
            first += " Current changes no longer match that slice."
        lines.append(first)
        if artifacts and artifacts_live:
            lines.append("- Artifact anchors: " + ", ".join(artifacts[:4]) + ".")
    else:
        events = parse_events(user_id, events_path=events_path)
        if not events:
            lines.append("- No prior cadence events found for this user.")
        else:
            recent = [_summarize_event(event) for event in events[-4:]]
            lines.append("- Recent cadence: " + " -> ".join(recent) + ".")
            lines.append("- No coffee_close receipt yet, so the branch outcome is not explicit.")

    repeated = recursion.get("repeated_unresolved_loops") or []
    if repeated:
        loops = ", ".join(f"{row['loop']} x{row['count']}" for row in repeated[:3])
        lines.append("- Repeated unresolved loops: " + loops + ".")

    conductor = recursion.get("latest_conductor_state")
    if conductor:
        lines.append(
            "- Conductor continuity: "
            f"{conductor.get('conductor')} is {conductor.get('state')} from {conductor.get('source')}."
        )

    return "\n".join(lines[:5])

def format_dream_recent_rhythm(
    user_id: str,
    *,
    count: int = 4,
    events_path: Path = EVENTS_PATH,
) -> str:
    events = parse_events(user_id, events_path=events_path)
    if not events:
        return "Recent rhythm: no prior cadence events were logged, so tonight starts from a quiet surface."

    tail = events[-max(1, count):]
    phrases: list[str] = []
    seen: set[str] = set()
    for event in tail:
        phrase = _summarize_event(event)
        if phrase not in seen:
            seen.add(phrase)
            phrases.append(phrase)

    first = phrases[0] if phrases else "we moved through the cadence without leaving a strong pressure signal"
    if len(phrases) == 1:
        body = first
    elif len(phrases) == 2:
        body = f"{first}, then {phrases[1]}"
    else:
        body = f"{first}, then {phrases[1]}, and later {phrases[-1]}"

    recursion = compute_coffee_recursion_summary(user_id, days=14, events_path=events_path)
    repeated = recursion.get("repeated_unresolved_loops") or []
    last_close = recursion.get("last_close") or {}
    next_step = str(last_close.get("next") or "").strip()
    readiness = str(last_close.get("readiness") or "").strip()
    if repeated:
        inherit = f"The main thing still echoing is {repeated[0]['loop']}."
    elif next_step and readiness:
        inherit = f"Tomorrow most naturally inherits the {readiness} slice around {next_step}."
    elif next_step:
        inherit = f"Tomorrow most naturally inherits {next_step}."
    else:
        inherit = "Tomorrow inherits a quieter surface unless a new pressure shows up."

    return f"Recent rhythm: {body}. {inherit}"

def build_recent_rhythm(
    user_id: str,
    *,
    ritual: str,
    count: int | None = None,
    days: int = 14,
    events_path: Path = EVENTS_PATH,
    now: datetime | None = None,
    changed_paths: list[str] | None = None,
) -> str:
    if ritual == "dream":
        return format_dream_recent_rhythm(user_id, count=count or 4, events_path=events_path)
    if ritual == "coffee":
        return format_coffee_recent_rhythm(
            user_id,
            days=days,
            events_path=events_path,
            now=now,
            changed_paths=changed_paths,
        )
    raise ValueError(f"Unsupported ritual: {ritual}")

def main() -> int:
    parser = argparse.ArgumentParser(description="Format recent cadence rhythm for coffee or dream.")
    parser.add_argument("-u", "--user", default=DEFAULT_USER_ID)
    parser.add_argument("--ritual", choices=("coffee", "dream"), required=True)
    parser.add_argument("--count", type=int, default=None)
    parser.add_argument("--days", type=int, default=14)
    parser.add_argument("--changed-path", action="append", default=[])
    args = parser.parse_args()
    print(
        build_recent_rhythm(
            args.user,
            ritual=args.ritual,
            count=args.count,
            days=args.days,
            changed_paths=args.changed_path or None,
        )
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
