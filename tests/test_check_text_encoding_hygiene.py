"""Tests for continuity-layer encoding and status checkers."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

if str(REPO / "scripts") not in sys.path:
    sys.path.insert(0, str(REPO / "scripts"))

from check_continuity_status import check_status  # noqa: E402
from check_text_encoding_hygiene import scan_tree  # noqa: E402


def test_encoding_scan_finds_mojibake(tmp_path: Path):
    root = tmp_path / "codex"
    root.mkdir()
    dirty = root / "note.md"
    dirty.write_text("Session wrapper ÃƒÆ'Ã†â€™ note\n", encoding="utf-8")
    matches = scan_tree(root, tmp_path)
    assert len(matches) == 1
    assert matches[0].pattern.startswith("Ãƒ")


def test_encoding_scan_clean_file(tmp_path: Path):
    root = tmp_path / "codex"
    root.mkdir()
    (root / "clean.md").write_text("# Clean\n\nNormal apostrophe's text.\n", encoding="utf-8")
    assert scan_tree(root, tmp_path) == []


def test_encoding_hygiene_warn_exits_zero_on_dirty(tmp_path: Path, monkeypatch):
    root = tmp_path / "codex"
    root.mkdir()
    (root / "x.md").write_text("bad Ãƒ text\n", encoding="utf-8")
    proc = subprocess.run(
        [
            sys.executable,
            str(REPO / "scripts" / "check_text_encoding_hygiene.py"),
            "--scope",
            "codex",
            "--warn",
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert proc.returncode == 0


def test_encoding_hygiene_strict_fails_on_dirty(tmp_path: Path):
    root = tmp_path / "codex"
    root.mkdir()
    (root / "x.md").write_text("bad Ãƒ text\n", encoding="utf-8")
    proc = subprocess.run(
        [
            sys.executable,
            str(REPO / "scripts" / "check_text_encoding_hygiene.py"),
            "--scope",
            "codex",
            "--strict",
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert proc.returncode == 1


def _write_min_status(root: Path) -> None:
    days_dir = root / "chapters" / "2026-06"
    days_dir.mkdir(parents=True)
    days = days_dir / "days.md"
    days.write_text("## 2026-06-21\n\nEntry.\n", encoding="utf-8")
    (root / "daily-strategy-inbox.md").write_text("# inbox\n", encoding="utf-8")
    (root / "strategy-expert-predictions.md").write_text("# preds\n", encoding="utf-8")
    status = root / "STATUS.md"
    status.write_text(
        """# status

| Field | Value |
| **Last substantive entry** | `2026-06-21` — [`days`](chapters/2026-06/days.md#2026-06-21) |
| **Active chapter** | [`chapters/2026-06/days.md`](chapters/2026-06/days.md) |

## Next actions

1. Keep going.
""",
        encoding="utf-8",
    )


def test_check_status_passes_min_layout(tmp_path: Path):
    root = tmp_path / "codex"
    root.mkdir()
    _write_min_status(root)
    report = check_status(tmp_path)
    assert report.status_exists
    assert report.last_entry_anchor_found
    assert report.errors == []


def test_check_status_fails_missing_anchor(tmp_path: Path):
    root = tmp_path / "codex"
    root.mkdir()
    _write_min_status(root)
    days = root / "chapters" / "2026-06" / "days.md"
    days.write_text("## 2026-06-20\n", encoding="utf-8")
    report = check_status(tmp_path)
    assert any("anchor" in e for e in report.errors)


def test_check_continuity_status_on_repo():
    proc = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "check_continuity_status.py")],
        cwd=REPO,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_check_codex_status_wrapper():
    proc = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "check_codex_status.py"), "--json"],
        cwd=REPO,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert proc.returncode == 0, proc.stderr
    data = json.loads(proc.stdout)
    assert data["status_exists"] is True
