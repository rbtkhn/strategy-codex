"""Tests for scripts/land_statecraft_intake.py."""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture()
def intake_mod(monkeypatch, tmp_path: Path):
    path = REPO_ROOT / "scripts" / "land_statecraft_intake.py"
    spec = importlib.util.spec_from_file_location("land_statecraft_intake_test", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    monkeypatch.setattr(mod, "REPO_ROOT", tmp_path)
    return mod


def _day_out(tmp_path: Path, day: str, stem: str) -> Path:
    return tmp_path / "source-archive" / "statecraft" / day / f"{stem}-{day}.md"


def _mercouris_header(intake_mod, *, title: str = "Test episode", day: str = "2026-06-99") -> str:
    return intake_mod._build_mercouris_solo_header(
        title=title,
        pub_date=day,
        ingest_date=day,
        youtube_id="TESTVID01",
        source_url=None,
        source_note="pytest capture",
    )


def test_detect_family_mercouris_solo(intake_mod, tmp_path: Path):
    out = _day_out(tmp_path, "2026-06-99", "source-alex-mercouris-fixture")
    assert intake_mod._detect_family(out, "auto") == "mercouris-solo"


def test_mercouris_solo_always_chunks_even_when_small(intake_mod):
    body = "Short solo paragraph.\n"
    assert intake_mod._needs_chunked_land(body, "mercouris-solo") is True


def test_generic_small_body_not_chunked(intake_mod):
    body = "Small generic body.\n"
    assert intake_mod._needs_chunked_land(body, "generic") is False


def test_generic_large_body_chunks_by_byte_threshold(intake_mod):
    body = ("x" * (12 * 1024)) + "\n"
    assert intake_mod._needs_chunked_land(body, "generic") is True


def test_split_body_chunks_at_paragraph_boundaries(intake_mod):
    para_a = "a" * 8_000
    para_b = "b" * 8_000
    body = f"{para_a}\n\n{para_b}\n"
    chunks = intake_mod._split_body_chunks(body)
    assert len(chunks) == 2
    assert para_a in chunks[0]
    assert para_b in chunks[1]


def test_land_intake_mercouris_chunked_roundtrip(intake_mod, tmp_path: Path):
    day = "2026-06-99"
    out = _day_out(tmp_path, day, "source-alex-mercouris-pytest-roundtrip")
    body = ("Good day. " + "Mercouris monologue. ") * 400 + "\n"
    header = _mercouris_header(intake_mod, day=day)

    rc = intake_mod.land_intake(
        out=out,
        body=body,
        header_text=header,
        family="mercouris-solo",
        dry_run=False,
        keep_sidecars=False,
        skip_post_land=True,
    )
    assert rc == 0
    assert out.is_file()

    text = out.read_text(encoding="utf-8")
    assert "source_form: solo" in text
    assert "youtube_id: TESTVID01" in text
    match = re.search(r"^## Transcript\s*\n(.*)$", text, re.DOTALL | re.MULTILINE)
    assert match is not None
    assert match.group(1).strip() == body.strip()

    slug = intake_mod._slug_from_out(out)
    sidecar = out.parent / f"_land_{slug}"
    assert not sidecar.exists()


def test_land_intake_dry_run_writes_no_archive_file(intake_mod, tmp_path: Path, capsys):
    day = "2026-06-99"
    out = _day_out(tmp_path, day, "source-alex-mercouris-pytest-dry-run")
    body = "Dry run body paragraph.\n"
    header = _mercouris_header(intake_mod, day=day)

    rc = intake_mod.land_intake(
        out=out,
        body=body,
        header_text=header,
        family="mercouris-solo",
        dry_run=True,
        keep_sidecars=False,
        skip_post_land=True,
    )
    assert rc == 0
    assert not out.is_file()

    captured = capsys.readouterr()
    assert "dry-run: would write" in captured.out
    assert "chunked: True" in captured.out


def test_main_requires_body_source(intake_mod, tmp_path: Path, monkeypatch, capsys):
    day = "2026-06-99"
    out = _day_out(tmp_path, day, "source-alex-mercouris-pytest-main")
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "land_statecraft_intake.py",
            "--out",
            str(out),
            "--youtube-id",
            "TESTVID01",
            "--title",
            "Main test",
        ],
    )
    rc = intake_mod.main()
    assert rc == 1
    assert "supply --body-file" in capsys.readouterr().err


def test_main_mercouris_requires_title_or_header(intake_mod, tmp_path: Path, monkeypatch, capsys):
    day = "2026-06-99"
    out = _day_out(tmp_path, day, "source-alex-mercouris-pytest-main")
    body_file = tmp_path / "body.txt"
    body_file.write_text("Body only.\n", encoding="utf-8")
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "land_statecraft_intake.py",
            "--out",
            str(out),
            "--body-file",
            str(body_file),
            "--youtube-id",
            "TESTVID01",
        ],
    )
    rc = intake_mod.main()
    assert rc == 1
    assert "requires --title" in capsys.readouterr().err
