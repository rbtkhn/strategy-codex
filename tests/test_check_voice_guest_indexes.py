#!/usr/bin/env python3
"""Tests for check_voice_guest_indexes batch runner."""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import check_voice_guest_indexes as guest_check  # noqa: E402


def test_guest_index_batch_check_passes_on_repo() -> None:
    assert guest_check.main([]) == 0


def test_guest_index_batch_unknown_slug() -> None:
    assert guest_check.main(["--voice", "not-a-voice"]) == 1


def test_guest_index_single_voice_check(tmp_path: Path, monkeypatch) -> None:
    script = tmp_path / "build_sample_guest_index.py"
    script.write_text(
        "import sys\n"
        "if '--check' in sys.argv:\n"
        "    print('OK sample (0 rows)')\n"
        "    raise SystemExit(0)\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(
        guest_check,
        "GUEST_INDEX_BUILDERS",
        ("build_sample_guest_index.py",),
    )
    monkeypatch.setattr(guest_check, "SCRIPTS", tmp_path)
    assert guest_check.main([]) == 0
