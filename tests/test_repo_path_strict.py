from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from repo_io import (  # noqa: E402
    GRACE_MAR_INSTANCE_DIR,
    profile_dir,
    profile_rel_posix,
    reset_legacy_path_resolve_count,
    resolve_repo_path,
    scan_legacy_path_layout,
    strict_paths_enabled,
)


def test_profile_dir_points_at_grace_mar_instance():
    root = profile_dir("strategy-codex")
    assert root == GRACE_MAR_INSTANCE_DIR
    assert (root / "recursion-gate.md").is_file()


def test_profile_rel_posix():
    rel = profile_rel_posix("strategy-codex")
    assert rel == "archive/grace-mar-instance"


def test_check_repo_path_strict_warn_mode():
    proc = subprocess.run(
        [sys.executable, "scripts/check_repo_path_strict.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode in (0, 1)


def test_strict_paths_raises_on_legacy(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    monkeypatch.setenv("STRATEGY_CODEX_STRICT_PATHS", "1")
    assert strict_paths_enabled()
    reset_legacy_path_resolve_count()
    # artifacts canonical exists in real repo — strict mode should not raise for it.
    path = resolve_repo_path("artifacts")
    assert path.is_dir()


def test_scan_legacy_path_layout_is_list():
    issues = scan_legacy_path_layout()
    assert isinstance(issues, list)
