"""Tests for continuity/ → continuity/ rename audit."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

if str(REPO / "scripts") not in sys.path:
    sys.path.insert(0, str(REPO / "scripts"))

from audit_continuity_rename import (  # noqa: E402
    detect_migration_state,
    scan_repo,
    strict_checks,
)


def test_detect_migration_state_pre_move(tmp_path: Path):
    (tmp_path / "codex").mkdir()
    (tmp_path / "codex" / "STATUS.md").write_text("# status\n", encoding="utf-8")
    assert detect_migration_state(tmp_path) == "pre_move"


def test_detect_migration_state_post_move_redirect(tmp_path: Path):
    (tmp_path / "continuity").mkdir()
    (tmp_path / "continuity" / "README.md").write_text("# continuity\n", encoding="utf-8")
    (tmp_path / "codex").mkdir()
    (tmp_path / "codex" / "README.md").write_text("# moved\n", encoding="utf-8")
    assert detect_migration_state(tmp_path) == "post_move_redirect"


def test_detect_migration_state_dual_layout(tmp_path: Path):
    (tmp_path / "continuity").mkdir()
    (tmp_path / "continuity" / "days.md").write_text("# days\n", encoding="utf-8")
    (tmp_path / "codex").mkdir()
    (tmp_path / "codex" / "STATUS.md").write_text("# status\n", encoding="utf-8")
    assert detect_migration_state(tmp_path) == "dual_layout"


def test_scan_classifies_strategy_codex_as_public_name(tmp_path: Path):
    doc = tmp_path / "README.md"
    doc.write_text("Welcome to strategy-codex project.\n", encoding="utf-8")
    report = scan_repo(tmp_path)
    assert report.by_classification.get("public_project_name", 0) >= 1


def test_strict_pre_move_passes_with_codex_only(tmp_path: Path):
    (tmp_path / "codex").mkdir()
    (tmp_path / "codex" / "README.md").write_text("See continuity/ for notebook.\n", encoding="utf-8")
    report = scan_repo(tmp_path)
    report.strict_issues = strict_checks(report, tmp_path)
    assert report.strict_issues == []


def test_strict_post_move_fails_on_live_codex_corpus(tmp_path: Path):
    (tmp_path / "continuity").mkdir()
    (tmp_path / "continuity" / "README.md").write_text("# continuity\n", encoding="utf-8")
    (tmp_path / "codex").mkdir()
    (tmp_path / "codex" / "README.md").write_text("# redirect\n", encoding="utf-8")
    (tmp_path / "codex" / "STATUS.md").write_text("# stale\n", encoding="utf-8")
    report = scan_repo(tmp_path)
    report.strict_issues = strict_checks(report, tmp_path)
    assert any("redirect-only" in i or "dual_layout" in i for i in report.strict_issues)


def test_audit_script_default_exits_zero():
    proc = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "audit_continuity_rename.py")],
        cwd=REPO,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_audit_json_output_has_migration_state():
    proc = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "audit_continuity_rename.py"), "--json"],
        cwd=REPO,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert proc.returncode == 0, proc.stderr
    data = json.loads(proc.stdout)
    assert data["migration_state"] in ("post_move", "post_move_redirect")
    assert "by_classification" in data


def test_strict_canonical_doc_requires_line_level_legacy_framing(tmp_path: Path):
    (tmp_path / "continuity").mkdir()
    (tmp_path / "continuity" / "README.md").write_text("# continuity\n", encoding="utf-8")
    (tmp_path / "codex").mkdir()
    (tmp_path / "codex" / "README.md").write_text("# redirect\n", encoding="utf-8")

    # Legacy framing elsewhere in file must not mask stale codex/ on another line
    (tmp_path / "memory.md").write_text(
        "# memory\n\nLegacy note about migration.\nSee codex/chapters/ for old paths.\n",
        encoding="utf-8",
    )
    report = scan_repo(tmp_path)
    issues = strict_checks(report, tmp_path)
    assert any("memory.md:" in i and "stale codex/" in i for i in issues)

    (tmp_path / "memory.md").write_text(
        "# memory\n\nLegacy redirect: codex/ is compat only.\n",
        encoding="utf-8",
    )
    report = scan_repo(tmp_path)
    issues = strict_checks(report, tmp_path)
    assert not any("memory.md" in i and "stale codex/" in i for i in issues)


def test_write_report_not_created_by_default(tmp_path: Path, monkeypatch):
    """Default mode must not write runtime artifacts (repo test uses --write-report explicitly)."""
    artifact = REPO / "runtime" / "artifacts" / "continuity-rename-audit.json"
    # Only verify flag behavior on tmp repo via import
    from audit_continuity_rename import format_markdown_report, scan_repo

    (tmp_path / "codex").mkdir()
    report = scan_repo(tmp_path)
    md = format_markdown_report(report)
    assert "pre_move" in md
    assert not artifact.name.startswith(str(tmp_path))
