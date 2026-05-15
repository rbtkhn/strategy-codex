#!/usr/bin/env python3
"""Compact first-command coffee bootstrap formatting.

Read-only WORK-layer helpers. These functions summarize cadence, coffee_close,
load, branch pressure, memory observability, and lane hints without mutating
Record or derived memory surfaces.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

try:
    from audit_cadence_rhythm import (
        EVENTS_PATH,
        compute_coffee_recursion_summary,
        parse_events,
    )
    from repo_io import DEFAULT_USER_ID
except ImportError:
    from scripts.audit_cadence_rhythm import (
        EVENTS_PATH,
        compute_coffee_recursion_summary,
        parse_events,
    )
    from scripts.repo_io import DEFAULT_USER_ID


HUB_LABELS = {
    "A": "Steward",
    "B": "Engineer",
    "C": "Strategist",
    "D": "Capitalist",
}


def _as_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    if value is None:
        return []
    return [part.strip() for part in str(value).split(",") if part.strip()]


def _truncate(value: str, limit: int = 140) -> str:
    text = " ".join(str(value).split())
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def _kind_phrase(event: dict[str, Any]) -> str:
    kind = str(event.get("kind") or "event")
    kv = event.get("kv") or {}
    if kind == "coffee":
        mode = kv.get("mode")
        return f"coffee {mode}" if mode else "coffee"
    if kind == "coffee_pick":
        picked = kv.get("picked")
        conductor = kv.get("conductor")
        if conductor:
            return f"coffee pick conductor={conductor}"
        return f"coffee pick {picked}" if picked else "coffee pick"
    if kind == "coffee_close":
        readiness = kv.get("readiness")
        outcome = kv.get("outcome")
        return f"coffee close {outcome or 'outcome'} / {readiness or 'readiness unknown'}"
    if kind == "dream":
        ok = kv.get("ok")
        return "dream pass" if ok == "true" else "dream"
    if kind == "bridge":
        ref = kv.get("commit") or kv.get("packet") or kv.get("kind")
        return f"bridge {ref}" if ref else "bridge"
    return kind


def format_coffee_recent_rhythm(
    user_id: str,
    *,
    days: int = 14,
    events_path: Path = EVENTS_PATH,
    now: datetime | None = None,
) -> str:
    """Return 2-4 human lines for coffee Step 0, preferring coffee_close."""
    now = now or datetime.now(timezone.utc)
    recursion = compute_coffee_recursion_summary(
        user_id, days=days, events_path=events_path, now=now
    )
    last_close = recursion.get("last_close")
    lines: list[str] = ["Recent rhythm:"]

    if last_close:
        picked = last_close.get("picked") or "unknown"
        outcome = last_close.get("outcome") or "unknown"
        readiness = last_close.get("readiness") or "unknown"
        next_step = last_close.get("next")
        first = f"- Last close picked {picked}: {outcome}, readiness {readiness}."
        if next_step:
            first += f" Next: {next_step}."
        lines.append(first)
        artifacts = _as_list(last_close.get("artifacts"))
        if artifacts:
            lines.append("- Artifact anchors: " + ", ".join(artifacts[:4]) + ".")
    else:
        events = parse_events(user_id, events_path=events_path)
        if not events:
            lines.append("- No prior cadence events found for this user.")
        else:
            recent = [_kind_phrase(event) for event in events[-4:]]
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
            f"{conductor.get('conductor')} is {conductor.get('state')} "
            f"from {conductor.get('source')}."
        )

    return "\n".join(lines[:5])


def _memory_status(user_id: str) -> str:
    try:
        from build_memory_observability import build_report

        report = build_report(user_id)
    except Exception:
        return "unknown"
    return str(report.get("overall_status") or "unknown")


def _lane_hint_status() -> str:
    try:
        from coffee_lane_next_hints import format_lane_next_hints

        text = format_lane_next_hints(REPO_ROOT)
    except Exception:
        return "unavailable"
    compact = " ".join(
        line.strip("- ").strip()
        for line in text.splitlines()
        if line.strip() and not line.lower().startswith("lane context")
    )
    return _truncate(compact or "available", 160)


def build_coffee_bootstrap_brief(
    user_id: str,
    *,
    events_path: Path = EVENTS_PATH,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Build a structured first-command coffee brief."""
    now = now or datetime.now(timezone.utc)
    try:
        from assess_session_load import assess_load

        load = assess_load(user_id)
    except Exception:
        load = {
            "load_level": "unknown",
            "branch_count": 0,
            "recommended": "C",
            "recommendation_reason": "fallback when session load is unavailable",
            "signals": [],
        }

    recursion = compute_coffee_recursion_summary(
        user_id, days=14, events_path=events_path, now=now
    )
    last_close = recursion.get("last_close")
    repeated = recursion.get("repeated_unresolved_loops") or []
    artifacts = _as_list(last_close.get("artifacts") if last_close else None)
    if not artifacts:
        artifact_counts = recursion.get("artifact_counts") or {}
        artifacts = list(artifact_counts)[:4]

    recommended = str(load.get("recommended") or "C")
    return {
        "user_id": user_id,
        "start_state": (
            f"load={load.get('load_level', 'unknown')}; "
            f"branches={load.get('branch_count', 0)}; "
            f"memory={_memory_status(user_id)}"
        ),
        "recent_rhythm": format_coffee_recent_rhythm(
            user_id, events_path=events_path, now=now
        ),
        "last_close": last_close,
        "open_loops": repeated,
        "artifact_anchors": artifacts[:4],
        "conductor_continuity": recursion.get("latest_conductor_state"),
        "lane_hints": _lane_hint_status(),
        "recommended_hub": recommended,
        "recommended_label": HUB_LABELS.get(recommended, recommended),
        "reason": load.get("recommendation_reason") or "best current fit",
        "load_signals": load.get("signals") or [],
    }


def format_coffee_bootstrap_brief(brief: dict[str, Any]) -> str:
    """Format the structured brief for first-command coffee output."""
    lines = ["Coffee Bootstrap Brief"]
    lines.append(f"- Start state: {brief.get('start_state', 'unknown')}")

    recent = str(brief.get("recent_rhythm") or "").splitlines()
    if recent:
        lines.extend(recent)
    recent_text = "\n".join(recent)

    loops = brief.get("open_loops") or []
    if loops and "Repeated unresolved loops:" not in recent_text:
        loop_text = ", ".join(f"{row['loop']} x{row['count']}" for row in loops[:3])
        lines.append(f"- Open loops: {loop_text}.")

    artifacts = _as_list(brief.get("artifact_anchors"))
    if artifacts and "Artifact anchors:" not in recent_text:
        lines.append("- Artifact anchors: " + ", ".join(artifacts[:4]) + ".")

    conductor = brief.get("conductor_continuity")
    if conductor and "Conductor continuity:" not in recent_text:
        lines.append(
            "- Conductor continuity: "
            f"{conductor.get('conductor')} {conductor.get('state')} "
            f"({conductor.get('source')})."
        )

    lane_hints = brief.get("lane_hints")
    if lane_hints and lane_hints != "unavailable":
        lines.append(f"- Lane hints: {lane_hints}")

    rec = brief.get("recommended_hub") or "C"
    label = brief.get("recommended_label") or HUB_LABELS.get(str(rec), str(rec))
    reason = brief.get("reason") or "best current fit"
    lines.append(f"- Recommended hub: {rec}. {label} - {reason}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Print the first-command coffee bootstrap brief.")
    parser.add_argument("-u", "--user", default=DEFAULT_USER_ID)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    brief = build_coffee_bootstrap_brief(args.user)
    if args.json:
        print(json.dumps(brief, indent=2, default=str))
    else:
        print(format_coffee_bootstrap_brief(brief))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
