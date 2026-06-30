"""Tests for statecraft notes contract checker."""

from __future__ import annotations

import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "check_statecraft_notes.py"


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )


def _import_module():
    import importlib.util

    spec = importlib.util.spec_from_file_location("check_statecraft_notes", SCRIPT)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def test_warn_mode_exits_zero_on_full_scan() -> None:
    proc = _run("--warn")
    assert proc.returncode == 0


def test_script_importable() -> None:
    mod = _import_module()
    assert hasattr(mod, "parse_note_metadata")
    assert "mechanism" in mod.TIER_A_TYPES


def test_parse_frontmatter_and_fenced_yaml() -> None:
    mod = _import_module()
    path = REPO_ROOT / "statecraft/notes/arc-karaganov-diesen-host.md"
    text = path.read_text(encoding="utf-8")
    meta = mod.parse_note_metadata(path, text)
    assert meta.note_type == "arc"
    assert meta.prefix_inferred_type == "arc"

    conflict = REPO_ROOT / "statecraft/notes/conflict-iran-mou-theater.md"
    meta2 = mod.parse_note_metadata(conflict, conflict.read_text(encoding="utf-8"))
    assert meta2.note_type == "conflict"


def test_stub_exempt_from_validation(tmp_path: Path) -> None:
    mod = _import_module()
    notes = tmp_path / "statecraft" / "notes"
    notes.mkdir(parents=True)
    stub = notes / "legacy-stub.md"
    stub.write_text(
        "Deprecated compatibility stub\n\nSee [new](./new.md).\n",
        encoding="utf-8",
    )
    meta = mod.parse_note_metadata(stub)
    assert meta.is_stub
    issues = mod.validate_note(meta, text=stub.read_text(encoding="utf-8"))
    assert issues == []


def test_prefix_inference_thread_arc() -> None:
    mod = _import_module()
    for name, expected in (("arc-pape-escalation-trap.md", "arc"), ("trend-china-ai-implementation.md", "trend")):
        path = REPO_ROOT / "statecraft/notes" / name
        meta = mod.parse_note_metadata(path)
        assert meta.prefix_inferred_type == expected


def test_strict_fails_incomplete_tier_a_note(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    mod = _import_module()
    notes = tmp_path / "statecraft" / "notes"
    notes.mkdir(parents=True)
    bad = notes / "mechanism-no-contract.md"
    bad.write_text(
        textwrap.dedent(
            """\
            WORK only; not Record.

            # Incomplete
            """
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(mod, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(mod, "NOTES_ROOT", notes)
    meta = mod.parse_note_metadata(bad)
    issues = mod.validate_note(meta, text=bad.read_text(encoding="utf-8"))
    assert any("missing note_type" in i for i in issues)
    assert any("missing source_basis" in i for i in issues)


def test_shelf_native_requires_archive_anchor(tmp_path: Path) -> None:
    mod = _import_module()
    notes = tmp_path / "statecraft" / "notes"
    notes.mkdir(parents=True)
    note = notes / "risk-no-anchor.md"
    note.write_text(
        textwrap.dedent(
            """\
            ---
            note_type: risk
            authority_level: shelf-native
            source_basis: source-archive
            ---

            WORK only; not Record.
            """
        ),
        encoding="utf-8",
    )
    meta = mod.parse_note_metadata(note)
    issues = mod.validate_note(meta, text=note.read_text(encoding="utf-8"))
    assert any("archive anchor" in i for i in issues)


def test_changed_only_flag_accepted() -> None:
    proc = _run("--warn", "--changed-only", "--tier-a-only")
    assert proc.returncode == 0


def test_exemplar_notes_validate_clean() -> None:
    mod = _import_module()
    inbound = mod.build_inbound_note_links(list(mod.NOTES_ROOT.rglob("*.md")))
    exemplars = (
        "conflict-iran-mou-theater.md",
        "trend-china-ai-implementation.md",
        "arc-pape-escalation-trap.md",
        "formal-sovereignty-vs-internal-carriage.md",
        "barnes-johnson-aguilar-kent-on-section-224.md",
    )
    for name in exemplars:
        path = REPO_ROOT / "statecraft" / "notes" / name
        text = path.read_text(encoding="utf-8")
        meta = mod.parse_note_metadata(path, text)
        issues = mod.validate_note(meta, text=text, inbound_count=inbound.get(meta.rel, 0))
        assert meta.note_type, name
        assert not issues, f"{name}: {issues}"


def test_prediction_note_tier_p_validates_clean() -> None:
    mod = _import_module()
    path = REPO_ROOT / "statecraft/notes/predictions/russia-odessa-control-mercouris-2025-01-10.md"
    text = path.read_text(encoding="utf-8")
    meta = mod.parse_note_metadata(path, text)
    assert meta.tier == "P"
    assert meta.note_type == "prediction"
    issues = mod.validate_note(meta, text=text)
    assert not issues


def test_prediction_note_rejects_shelf_native(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    mod = _import_module()
    notes = tmp_path / "statecraft" / "notes" / "predictions"
    notes.mkdir(parents=True)
    note = notes / "bad-prediction.md"
    note.write_text(
        textwrap.dedent(
            """\
            ---
            note_type: prediction
            event_id: russia_odessa_control
            speaker: mercouris
            date_made: 2025-01-01
            stance: no
            source: source-archive/statecraft/2025-01-01/example.md
            authority_level: shelf-native
            ---

            WORK only; not Record.
            """
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(mod, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(mod, "NOTES_ROOT", tmp_path / "statecraft" / "notes")
    meta = mod.parse_note_metadata(note)
    issues = mod.validate_note(meta, text=note.read_text(encoding="utf-8"))
    assert any("shelf-native" in i for i in issues)
