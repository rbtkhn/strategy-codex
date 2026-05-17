"""Tests for scripts/verify_repo_identity.py."""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

from verify_repo_identity import EXPECTED_ORIGIN, verify_repo_identity


def test_verify_repo_identity_accepts_strategy_codex(tmp_path: Path) -> None:
    root = tmp_path / "strategy-codex"
    root.mkdir()
    (root / "AGENTS.md").write_text(
        "**Active repo identity:** `strategy-codex` is the active development repo.\n",
        encoding="utf-8",
    )

    def fake_runner(argv: list[str], cwd: Path) -> tuple[int, str, str]:
        if argv == ["git", "rev-parse", "--show-toplevel"]:
            return 0, str(root), ""
        if argv == ["git", "remote", "get-url", "origin"]:
            return 0, EXPECTED_ORIGIN, ""
        raise AssertionError(argv)

    ok, lines = verify_repo_identity(root, runner=fake_runner)

    assert ok is True
    assert "root-name=strategy-codex" in lines
    assert "origin=https rbtkhn/strategy-codex" in lines
    assert "AGENTS=active strategy-codex" in lines


def test_verify_repo_identity_rejects_wrong_origin(tmp_path: Path) -> None:
    root = tmp_path / "strategy-codex"
    root.mkdir()
    (root / "AGENTS.md").write_text(
        "**Active repo identity:** `strategy-codex` is the active development repo.\n",
        encoding="utf-8",
    )

    def fake_runner(argv: list[str], cwd: Path) -> tuple[int, str, str]:
        if argv == ["git", "rev-parse", "--show-toplevel"]:
            return 0, str(root), ""
        if argv == ["git", "remote", "get-url", "origin"]:
            return 0, "https://github.com/rbtkhn/ph-workshop.git", ""
        raise AssertionError(argv)

    ok, lines = verify_repo_identity(root, runner=fake_runner)

    assert ok is False
    assert any("expected=https://github.com/rbtkhn/strategy-codex.git" in line for line in lines)
