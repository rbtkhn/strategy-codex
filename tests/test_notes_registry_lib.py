"""Tests for notes_registry_lib broken-link spec and dashboard."""

from __future__ import annotations

import importlib.util
import sys
import textwrap
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
LIB = REPO_ROOT / "scripts" / "notes_registry_lib.py"


def _import_lib():
    spec = importlib.util.spec_from_file_location("notes_registry_lib", LIB)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def test_broken_link_spec_counts_missing_note_only(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    lib = _import_lib()
    notes = tmp_path / "statecraft" / "notes"
    notes.mkdir(parents=True)
    good = notes / "good-target.md"
    good.write_text("# Good\n", encoding="utf-8")
    archive_dir = tmp_path / "source-archive" / "statecraft" / "2026-01-01"
    archive_dir.mkdir(parents=True)
    archive = archive_dir / "source-x.md"
    archive.write_text("# Archive\n", encoding="utf-8")

    source = notes / "source-note.md"
    source.write_text(
        textwrap.dedent(
            f"""\
            WORK only.

            - [good](./good-target.md)
            - [missing](./missing-note.md)
            - [archive](../../source-archive/statecraft/2026-01-01/source-x.md)
            """
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(lib, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(lib, "NOTES_ROOT", notes)

    text = source.read_text(encoding="utf-8")
    count, paths = lib.count_broken_note_links(source, text)
    assert count == 1
    assert "./missing-note.md" in paths


def test_valid_archive_link_not_broken(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    lib = _import_lib()
    notes = tmp_path / "statecraft" / "notes"
    notes.mkdir(parents=True)
    archive_dir = tmp_path / "source-archive" / "statecraft" / "2026-01-01"
    archive_dir.mkdir(parents=True)
    (archive_dir / "source-x.md").write_text("# Archive\n", encoding="utf-8")
    source = notes / "linked.md"
    source.write_text(
        "See [archive](../../source-archive/statecraft/2026-01-01/source-x.md).\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(lib, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(lib, "NOTES_ROOT", notes)
    count, _ = lib.count_broken_note_links(source, source.read_text(encoding="utf-8"))
    assert count == 0


def test_dashboard_tier_a_vs_tier_b_summary() -> None:
    lib = _import_lib()
    rows = [
        lib.RegistryRow(
            tier="A",
            path="statecraft/notes/risk-x.md",
            title="risk-x",
            note_type="risk",
            authority_level="shelf-native",
            source_basis="source-archive",
            archive_anchor_count=2,
            inbound_links=1,
            outbound_links=0,
            broken_links=1,
            essay_candidate=True,
            updated_at="2026-06-01",
            warnings=["weak_anchor", "essay_underproof"],
        ),
        lib.RegistryRow(
            tier="B",
            path="statecraft/notes/wire/foo.md",
            title="foo",
            note_type="wire",
            authority_level="",
            source_basis="",
            archive_anchor_count=0,
            inbound_links=0,
            outbound_links=0,
            broken_links=0,
            essay_candidate=False,
            updated_at="",
            warnings=["missing_contract"],
            subfolder="wire",
        ),
    ]
    dashboard = lib.build_dashboard(rows)
    assert dashboard["tier_a"]["total"] == 1
    assert dashboard["tier_a"]["broken_internal_note_links"] == 1
    assert dashboard["tier_a"]["essay_candidates"] == 1
    assert dashboard["tier_b_summary"]["total"] == 1
    assert dashboard["tier_b_summary"]["wire"] == 1
    assert dashboard["tier_b_summary"]["contract_gaps"] == 1
    assert len(dashboard["essay_queue"]) == 1
    assert dashboard["essay_queue"][0]["path"] == "statecraft/notes/risk-x.md"
