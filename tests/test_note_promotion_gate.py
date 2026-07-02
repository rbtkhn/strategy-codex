"""Tests for notes registry reindex and essay promotion stub."""

from __future__ import annotations

import json
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
    md_out = REPO_ROOT / "runtime" / "artifacts" / "statecraft-notes-registry.md"
    json_out = REPO_ROOT / "runtime" / "artifacts" / "statecraft-notes-registry.json"
    assert md_out.is_file()
    assert json_out.is_file()
    text = md_out.read_text(encoding="utf-8")
    assert "conflict-iran-mou-theater" in text
    assert "Tier A health" in text
    assert "generated" in text.lower()
    payload = json.loads(json_out.read_text(encoding="utf-8"))
    assert payload["generator"] == "scripts/reindex_notes.py"
    assert "dashboard" in payload
    assert "notes" in payload

def test_reindex_notes_check_passes_after_regen() -> None:
    regen = subprocess.run(
        [sys.executable, "scripts/reindex_notes.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert regen.returncode == 0, regen.stderr
    proc = subprocess.run(
        [sys.executable, "scripts/reindex_notes.py", "--check"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout
    assert "ok:" in proc.stdout

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
