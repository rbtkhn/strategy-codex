"""Tests for shared git worktree snapshot used by coffee Step 1."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from git_worktree_snapshot import (  # noqa: E402
    GitWorktreeSnapshot,
    capture_git_worktree_snapshot,
    clear_git_worktree_snapshot_cache,
    format_git_state_summary,
    get_git_worktree_snapshot,
)


def test_capture_git_worktree_snapshot_parses_porcelain() -> None:
    def fake_run(argv, *, cwd, timeout):
        assert argv == ["git", "status", "-sb", "--porcelain"]
        return type(
            "Result",
            (),
            {
                "returncode": 0,
                "stdout": (
                    "## main...origin/main [ahead 1]\n"
                    " M statecraft/daily/2026-06-08.md\n"
                    "?? runtime/artifacts/tmp/\n"
                ),
                "stderr": "",
            },
        )()

    snap = capture_git_worktree_snapshot(runner=fake_run)
    assert snap.ok
    assert snap.branch_name == "main"
    assert snap.dirty_tracked_count == 1
    assert snap.untracked_count == 1
    assert "statecraft/daily/2026-06-08.md" in snap.changed_paths


def test_get_git_worktree_snapshot_uses_process_cache(monkeypatch) -> None:
    clear_git_worktree_snapshot_cache()
    calls = {"n": 0}

    def fake_run(argv, *, cwd, timeout):
        calls["n"] += 1
        return type(
            "Result",
            (),
            {"returncode": 0, "stdout": "## main...origin/main\n", "stderr": ""},
        )()

    monkeypatch.setattr("git_worktree_snapshot._default_runner", fake_run)
    first = get_git_worktree_snapshot(refresh=True)
    second = get_git_worktree_snapshot()
    assert first.branch_name == "main"
    assert second.branch_name == "main"
    assert calls["n"] == 1


def test_format_git_state_summary_reports_error() -> None:
    snap = GitWorktreeSnapshot(error="git status timed out after 20s")
    assert "unavailable" in format_git_state_summary(snap)
