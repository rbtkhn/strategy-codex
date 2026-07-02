"""Tests for continuity_paths dual-path resolution."""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

from continuity_paths import (  # noqa: E402
    CANONICAL_CONTINUITY_DIR,
    LEGACY_CODEX_DIR,
    continuity_root,
    continuity_subpath,
)
from repo_io import CONTINUITY_DIR, continuity_dir, resolve_repo_path  # noqa: E402

def test_continuity_root_codex_only(tmp_path: Path):
    (tmp_path / LEGACY_CODEX_DIR).mkdir()
    assert continuity_root(tmp_path).name == LEGACY_CODEX_DIR

def test_continuity_root_prefers_continuity(tmp_path: Path):
    (tmp_path / LEGACY_CODEX_DIR).mkdir()
    (tmp_path / CANONICAL_CONTINUITY_DIR).mkdir()
    assert continuity_root(tmp_path).name == CANONICAL_CONTINUITY_DIR

def test_continuity_subpath(tmp_path: Path):
    root = tmp_path / LEGACY_CODEX_DIR
    root.mkdir()
    assert continuity_subpath(tmp_path, "STATUS.md") == root / "STATUS.md"

def test_repo_io_continuity_dir_resolves_codex_pre_move():
    root = continuity_dir()
    assert root.is_dir()
    assert root.name in (LEGACY_CODEX_DIR, CANONICAL_CONTINUITY_DIR)

def test_repo_io_resolve_repo_path_codex_key():
    p = resolve_repo_path("codex")
    assert p.name in (LEGACY_CODEX_DIR, CANONICAL_CONTINUITY_DIR)
    assert p == CONTINUITY_DIR
