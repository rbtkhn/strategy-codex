#!/usr/bin/env python3
"""Compact first-command coffee bootstrap formatting.

Read-only WORK-layer helpers. These functions summarize cadence, coffee_close,
load, branch pressure, memory observability, and lane hints without mutating
Record or derived memory surfaces.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
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
    from audit_cadence_rhythm import EVENTS_PATH, compute_coffee_recursion_summary
    from cadence_recent_rhythm import format_coffee_recent_rhythm
    from dream_coffee_rollup import rollup_object_closes_24h
    from repo_io import DEFAULT_USER_ID
except ImportError:
    from scripts.audit_cadence_rhythm import EVENTS_PATH, compute_coffee_recursion_summary
    from scripts.cadence_recent_rhythm import format_coffee_recent_rhythm
    from scripts.dream_coffee_rollup import rollup_object_closes_24h
    from scripts.repo_io import DEFAULT_USER_ID


HUB_LABELS = {
    "A": "Confirm",
    "B": "Test",
    "C": "Deepen",
    "D": "Reframe",
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


def _normalize_repo_path(value: str) -> str:
    return str(value).strip().replace("\\", "/").rstrip("/")


def _artifacts_overlap_changed_paths(
    artifacts: list[str] | tuple[str, ...] | None, changed_paths: list[str] | tuple[str, ...] | None
) -> bool:
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


def _git_credential_status(*, skip_gh: bool = False) -> str:
    """Return a compact read-only GitHub credential hint for fresh chats."""
    origin = subprocess.run(
        ["git", "remote", "get-url", "origin"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=3,
        check=False,
    )
    remote = origin.stdout.strip() if origin.returncode == 0 else "unknown"
    protocol = "https" if remote.startswith("https://") else "ssh" if remote.startswith("git@") else "unknown"

    if skip_gh or os.environ.get("COFFEE_SKIP_GH", "").strip().lower() in {"1", "true", "yes"}:
        return f"origin={protocol}; gh=skipped"
    if os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN"):
        return f"origin={protocol}; gh=token-env"

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
        timeout=2,
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
    try:
        from git_worktree_snapshot import format_git_state_summary, get_git_worktree_snapshot
    except ImportError:
        from scripts.git_worktree_snapshot import format_git_state_summary, get_git_worktree_snapshot  # type: ignore

    return format_git_state_summary(get_git_worktree_snapshot())


def _pytest_status(*, skip_subprocess: bool = False) -> str:
    """Return whether the current Python runtime can run pytest."""
    if skip_subprocess or os.environ.get("COFFEE_SKIP_PYTEST", "").strip().lower() in {"1", "true", "yes"}:
        if importlib.util.find_spec("pytest") is None:
            return "missing - install test extras before pytest verification"
        return "available (import check)"

    result = subprocess.run(
        [sys.executable, "-m", "pytest", "--version"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=3,
        check=False,
    )
    if result.returncode == 0:
        version = (result.stdout or result.stderr).strip().splitlines()[0]
        return f"available ({version})"
    output = f"{result.stdout}\n{result.stderr}"
    if "No module named pytest" in output:
        return "missing - install test extras before pytest verification"
    if importlib.util.find_spec("pytest") is not None:
        return "available (import check)"
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
    fast: bool = False,
) -> dict[str, Any]:
    """Build a structured first-command coffee brief."""
    now = now or datetime.now(timezone.utc)
    try:
        from git_worktree_snapshot import get_git_worktree_snapshot
    except ImportError:
        from scripts.git_worktree_snapshot import get_git_worktree_snapshot  # type: ignore

    get_git_worktree_snapshot(refresh=True)
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
    load_changed_paths = _as_list(load.get("changed_paths"))
    artifacts = _as_list(last_close.get("artifacts") if last_close else None)
    if not artifacts:
        artifact_counts = recursion.get("artifact_counts") or {}
        artifacts = list(artifact_counts)[:4]

    recommended = str(load.get("recommended") or "C")
    object_close_rollup = rollup_object_closes_24h(
        user_id=user_id, events_path=events_path, now_utc=now
    )
    return {
        "user_id": user_id,
        "start_state": (
            f"load={load.get('load_level', 'unknown')}; "
            f"branches={load.get('branch_count', 0)}; "
            f"memory={_memory_status(user_id)}"
        ),
        "repo_identity": _repo_identity_status() if not fast else "skipped (--fast)",
        "git_credentials": _git_credential_status(skip_gh=fast),
        "git_state": _git_state_status(),
        "pytest": _pytest_status(skip_subprocess=fast),
        "recent_rhythm": format_coffee_recent_rhythm(
            user_id, events_path=events_path, now=now, changed_paths=load_changed_paths
        ),
        "last_close": last_close,
        "open_loops": repeated,
        "artifact_anchors": (
            artifacts[:4]
            if _artifacts_overlap_changed_paths(artifacts, load_changed_paths)
            else []
        ),
        "conductor_continuity": recursion.get("latest_conductor_state"),
        "object_close_24h": object_close_rollup,
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

    object_close = brief.get("object_close_24h") or {}
    if isinstance(object_close, dict):
        echo = str(object_close.get("echo") or "").strip()
        if echo and "Object close echo:" not in recent_text:
            lines.append(f"- Object close echo: {echo}")

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
