#!/usr/bin/env python3
"""Single git status snapshot for operator coffee / handoff / load assessment.

Large repos on Windows pay heavily for repeated ``git status`` scans. Coffee
Step 1 should invoke git once per process and reuse the parsed result.
"""

from __future__ import annotations

import os
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

REPO_ROOT = Path(__file__).resolve().parent.parent

_CACHE: GitWorktreeSnapshot | None = None
_CACHE_AT: float = 0.0
_CACHE_TTL_SEC = 30.0


@dataclass(frozen=True)
class GitWorktreeSnapshot:
    branch_line: str = ""
    branch_name: str = "unknown"
    tracking: str = "unknown"
    status_lines: tuple[str, ...] = ()
    porcelain_lines: tuple[str, ...] = ()
    changed_paths: tuple[str, ...] = ()
    dirty_tracked_count: int = 0
    untracked_count: int = 0
    error: str = ""

    @property
    def ok(self) -> bool:
        return not self.error


def _status_path(line: str) -> str:
    return line[3:].strip() if len(line) > 3 else line.strip()


def _parse_branch(branch_line: str) -> tuple[str, str]:
    text = branch_line.removeprefix("## ").strip()
    if not text:
        return "unknown", "unknown"
    branch_name = text.split("...")[0].strip() or "unknown"
    return branch_name, text


def _collect_changed_paths(status_lines: tuple[str, ...]) -> tuple[str, ...]:
    paths: set[str] = set()
    for line in status_lines:
        path = _status_path(line).replace("\\", "/")
        if path:
            paths.add(path)
    return tuple(sorted(paths))


def _default_runner(argv: list[str], *, cwd: Path, timeout: float) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.setdefault("GIT_OPTIONAL_LOCKS", "0")
    return subprocess.run(
        argv,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
        check=False,
        env=env,
    )


def capture_git_worktree_snapshot(
    *,
    repo_root: Path = REPO_ROOT,
    timeout: float = 20.0,
    runner: Callable[..., subprocess.CompletedProcess[str]] | None = None,
) -> GitWorktreeSnapshot:
    run = runner or _default_runner
    try:
        proc = run(
            ["git", "status", "-sb", "--porcelain"],
            cwd=repo_root,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return GitWorktreeSnapshot(error=f"git status timed out after {timeout:.0f}s")
    except OSError as exc:
        return GitWorktreeSnapshot(error=f"git status failed: {exc}")

    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout or "unknown error").strip()
        return GitWorktreeSnapshot(error=f"git status failed: {err}")

    raw_lines = [line for line in proc.stdout.splitlines() if line.strip()]
    branch_line = raw_lines[0] if raw_lines and raw_lines[0].startswith("## ") else ""
    status_lines = tuple(line for line in raw_lines if not line.startswith("## "))
    branch_name, tracking = _parse_branch(branch_line)
    dirty_tracked = sum(1 for line in status_lines if not line.startswith("??"))
    untracked = sum(1 for line in status_lines if line.startswith("??"))
    return GitWorktreeSnapshot(
        branch_line=branch_line,
        branch_name=branch_name,
        tracking=tracking,
        status_lines=status_lines,
        porcelain_lines=tuple(raw_lines),
        changed_paths=_collect_changed_paths(status_lines),
        dirty_tracked_count=dirty_tracked,
        untracked_count=untracked,
    )


def get_git_worktree_snapshot(
    *,
    refresh: bool = False,
    repo_root: Path = REPO_ROOT,
    timeout: float = 20.0,
    runner: Callable[..., subprocess.CompletedProcess[str]] | None = None,
) -> GitWorktreeSnapshot:
    global _CACHE, _CACHE_AT
    now = time.monotonic()
    if not refresh and _CACHE is not None and (now - _CACHE_AT) < _CACHE_TTL_SEC:
        return _CACHE
    snap = capture_git_worktree_snapshot(repo_root=repo_root, timeout=timeout, runner=runner)
    _CACHE = snap
    _CACHE_AT = now
    return snap


def clear_git_worktree_snapshot_cache() -> None:
    global _CACHE, _CACHE_AT
    _CACHE = None
    _CACHE_AT = 0.0


def format_git_state_summary(snapshot: GitWorktreeSnapshot) -> str:
    if snapshot.error:
        return f"unavailable - {snapshot.error}"
    tracking = snapshot.tracking or snapshot.branch_name
    if snapshot.dirty_tracked_count == 0 and snapshot.untracked_count == 0:
        return f"{tracking}; clean"
    parts: list[str] = []
    if snapshot.dirty_tracked_count:
        parts.append(f"dirty={snapshot.dirty_tracked_count}")
    if snapshot.untracked_count:
        parts.append(f"untracked={snapshot.untracked_count}")
    return f"{tracking}; " + "; ".join(parts)
