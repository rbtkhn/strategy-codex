"""Tests for notes registry reindex and essay promotion stub."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_reindex_notes_writes_registry() -> None:
    proc = subprocess.run(
        [sys.executable, "scripts/reindex_notes.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
    out = REPO_ROOT / "runtime" / "artifacts" / "statecraft-notes-registry.md"
    assert out.is_file()
    text = out.read_text(encoding="utf-8")
    assert "conflict-iran-mou-theater" in text
    assert "generated" in text.lower()


def test_promote_note_dry_run() -> None:
    proc = subprocess.run(
        [
            sys.executable,
            "scripts/promote_note_to_essay.py",
            "formal-sovereignty-vs-internal-carriage.md",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
    assert "Dry run only" in proc.stdout
