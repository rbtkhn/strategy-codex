from __future__ import annotations

import builtins
from pathlib import Path

import pytest

from grace_mar import predictive_history as ph


def test_infers_volume_from_game_theory_title() -> None:
    assert ph.infer_volume("Game Theory #23: The WWIII Chessboard") == "Volume IV - Game Theory"


def test_build_document_sets_predictive_history_frontmatter() -> None:
    filename, document, volume = ph.build_document(
        body="This is a test body.",
        title="Game Theory #23: The WWIII Chessboard",
        source_url="https://www.youtube.com/watch?v=6aNh6sBpqvQ",
        source_note="Predictive History corpus intake",
        ingest_date="2026-05-07",
        pub_date="2026-05-07",
        volume=None,
    )

    assert filename == "predictive-history-2026-05-07-game-theory-23-the-wwiii-chessboard.md"
    assert volume == "Volume IV - Game Theory"
    assert "series: Predictive History" in document
    assert 'volume: "Volume IV - Game Theory"' in document
    assert 'title: "Game Theory #23: The WWIII Chessboard"' in document
    assert "This is a test body." in document


def test_main_writes_file_with_explicit_volume(tmp_path: Path) -> None:
    body_file = tmp_path / "input.txt"
    body_file.write_text("Transcript body.\n", encoding="utf-8")
    outdir = tmp_path / "intake"

    rc = ph.main(
        [
            "--title",
            "A Predictive History upload",
            "--volume",
            "Volume VI - Interviews",
            "--body-file",
            str(body_file),
            "--outdir",
            str(outdir),
            "--pub-date",
            "2026-05-07",
            "--ingest-date",
            "2026-05-07",
        ]
    )

    assert rc == 0
    outpath = outdir / "predictive-history-2026-05-07-a-predictive-history-upload.md"
    assert outpath.is_file()
    text = outpath.read_text(encoding="utf-8")
    assert "series: Predictive History" in text
    assert 'volume: "Volume VI - Interviews"' in text
    assert "Transcript body." in text


def test_main_prompts_for_volume_when_interactive(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    body_file = tmp_path / "input.txt"
    body_file.write_text("Body without a clue.\n", encoding="utf-8")
    outdir = tmp_path / "intake"

    monkeypatch.setattr(ph.sys, "stdin", type("TTY", (), {"isatty": lambda self: True})())
    monkeypatch.setattr(builtins, "input", lambda _prompt="": "4")

    rc = ph.main(
        [
            "--title",
            "Ambiguous intake",
            "--body-file",
            str(body_file),
            "--outdir",
            str(outdir),
            "--pub-date",
            "2026-05-07",
            "--ingest-date",
            "2026-05-07",
        ]
    )

    assert rc == 0
    outpath = outdir / "predictive-history-2026-05-07-ambiguous-intake.md"
    text = outpath.read_text(encoding="utf-8")
    assert 'volume: "Volume IV - Game Theory"' in text


def test_main_requires_volume_when_ambiguous_and_noninteractive(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    body_file = tmp_path / "input.txt"
    body_file.write_text("Body without a clue.\n", encoding="utf-8")
    outdir = tmp_path / "intake"

    monkeypatch.setattr(ph.sys, "stdin", type("Pipe", (), {"isatty": lambda self: False})())

    with pytest.raises(SystemExit):
        ph.main(
            [
                "--title",
                "Ambiguous intake",
                "--body-file",
                str(body_file),
                "--outdir",
                str(outdir),
                "--pub-date",
                "2026-05-07",
                "--ingest-date",
                "2026-05-07",
            ]
        )
