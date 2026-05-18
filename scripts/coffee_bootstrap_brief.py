#!/usr/bin/env python3
"""Compact first-command coffee bootstrap formatting.

Read-only WORK-layer helpers. These functions summarize cadence, coffee_close,
load, branch pressure, memory observability, and lane hints without mutating
Record or derived memory surfaces.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
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
    "D": "Singularity",
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


def _find_gh() -> str | None:
    gh = shutil.which("gh")
    if gh:
        return gh
    windows_gh = Path("C:/Program Files/GitHub CLI/gh.exe")
    if windows_gh.exists():
        return str(windows_gh)
    return None


def _git_credential_status() -> str:
    """Return a compact read-only GitHub credential hint for fresh chats."""
    origin = subprocess.run(
        ["git", "remote", "get-url", "origin"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
        check=False,
    )
    remote = origin.stdout.strip() if origin.returncode == 0 else "unknown"
    protocol = "https" if remote.startswith("https://") else "ssh" if remote.startswith("git@") else "unknown"

    gh = _find_gh()
    if not gh:
        return f"origin={protocol}; gh=missing; verify credentials before shell push"

    auth = subprocess.run(
        [gh, "auth", "status", "-h", "github.com"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=8,
        check=False,
    )
    output = f"{auth.stdout}\n{auth.stderr}".lower()
    if auth.returncode == 0:
        return f"origin={protocol}; gh=ok"
    if "token" in output and "invalid" in output:
        return f"origin={protocol}; gh=invalid token - run gh auth login before shell push"
    if "not logged" in output or "log in" in output:
        return f"origin={protocol}; gh=not logged in - run gh auth login before shell push"
    return f"origin={protocol}; gh=unverified - run gh auth status before shell push"


def _git_state_status() -> str:
    """Return a compact read-only branch/dirty-worktree hint for fresh chats."""
    result = subprocess.run(
        ["git", "status", "--short", "--branch"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=8,
        check=False,
    )
    if result.returncode != 0:
        return "unavailable - run git status --short --branch"

    lines = [line for line in result.stdout.splitlines() if line.strip()]
    if not lines:
        return "unknown"

    branch = lines[0].removeprefix("## ").strip() or "unknown branch"
    changes = lines[1:]
    dirty = sum(1 for line in changes if not line.startswith("??"))
    untracked = sum(1 for line in changes if line.startswith("??"))
    if dirty == 0 and untracked == 0:
        return f"{branch}; clean"

    parts: list[str] = []
    if dirty:
        parts.append(f"dirty={dirty}")
    if untracked:
        parts.append(f"untracked={untracked}")
    return f"{branch}; " + "; ".join(parts)


def _pytest_status() -> str:
    """Return whether the current Python runtime can run pytest."""
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "--version"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=8,
        check=False,
    )
    if result.returncode == 0:
        version = (result.stdout or result.stderr).strip().splitlines()[0]
        return f"available ({version})"
    output = f"{result.stdout}\n{result.stderr}"
    if "No module named pytest" in output:
        return "missing - install test extras before pytest verification"
    return "unverified - run python -m pytest --version before test work"


def _repo_identity_status() -> str:
    """Return a compact read-only repo identity guard for fresh chats."""
    try:
        from verify_repo_identity import format_repo_identity_status

        return format_repo_identity_status(REPO_ROOT)
    except Exception as exc:
        return f"unavailable - run python scripts/verify_repo_identity.py ({exc})"


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
        "repo_identity": _repo_identity_status(),
        "git_credentials": _git_credential_status(),
        "git_state": _git_state_status(),
        "pytest": _pytest_status(),
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
    repo_identity = brief.get("repo_identity")
    if repo_identity:
        lines.append(f"- Repo identity: {repo_identity}")
    git_credentials = brief.get("git_credentials")
    if git_credentials:
        lines.append(f"- Git credentials: {git_credentials}")
    git_state = brief.get("git_state")
    if git_state:
        lines.append(f"- Git state: {git_state}")
    pytest_status = brief.get("pytest")
    if pytest_status:
        lines.append(f"- Pytest: {pytest_status}")

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
