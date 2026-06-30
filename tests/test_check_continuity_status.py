"""Tests for check_continuity_status (re-exported checks in encoding test file too)."""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

if str(REPO / "scripts") not in sys.path:
    sys.path.insert(0, str(REPO / "scripts"))

from check_continuity_status import continuity_root  # noqa: E402


def test_continuity_root_prefers_continuity(tmp_path: Path):
    (tmp_path / "codex").mkdir()
    (tmp_path / "continuity").mkdir()
    assert continuity_root(tmp_path).name == "continuity"


def test_continuity_root_fallback_codex(tmp_path: Path):
    (tmp_path / "codex").mkdir()
    assert continuity_root(tmp_path).name == "codex"
