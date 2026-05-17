from __future__ import annotations

import hashlib
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import clean_raw_input_transcript as clean  # noqa: E402


def _body(words: int = 90) -> str:
    return " ".join(f"word{i}" for i in range(words))


def _raw_input(body: str | None = None) -> str:
    return (
        "---\n"
        "ingest_date: 2026-05-17\n"
        "pub_date: 2026-01-02\n"
        "kind: transcript\n"
        "source_type: youtube\n"
        "transcript_type: manual_subtitles_vtt\n"
        "title: Example Transcript\n"
        "source_url: https://www.youtube.com/watch?v=abc123def45\n"
        "youtube_id: abc123def45\n"
        "channel_slug: dialogue-works\n"
        "source_note: Manual YouTube subtitles extracted with yt_dlp. Not human-verified verbatim.\n"
        "editorial_note: Atomic materialization verified a non-stub subtitle body before success was reported.\n"
        "show: Dialogue Works\n"
        "host: Nima Alkhorshid\n"
        "guest: Chas Freeman & Mohammad Marandi\n"
        "thread: marandi\n"
        "caption_language: en-orig\n"
        "caption_kind: manual\n"
        "body_word_count: 90\n"
        "verification_ok: true\n"
        "verification_reason: ok\n"
        "evidence_grade: transcript-grade\n"
        "---\n\n"
        "# Example Transcript\n\n"
        f"{body or _body()}\n"
    )


def test_dry_run_does_not_write_derivative(tmp_path: Path) -> None:
    source = tmp_path / "raw.md"
    source.write_text(_raw_input("Kind: captions\nLanguage: en\n" + _body()), encoding="utf-8")

    result, content = clean.clean_one(source, receipt_dir=None, apply=False)

    assert result.status == "dry-run"
    assert result.output_path.name == "raw.cleaned.md"
    assert content is None
    assert not result.output_path.exists()


def test_apply_writes_cleaned_derivative_without_modifying_source(tmp_path: Path) -> None:
    source = tmp_path / "raw.md"
    source.write_text(_raw_input("Kind: captions\nLanguage: en\nProfessor Mandi said " + _body()), encoding="utf-8")
    before_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    receipt_dir = tmp_path / "receipts"

    result, content = clean.clean_one(source, receipt_dir=receipt_dir, apply=True)
    clean.write_receipts([result], receipt_dir, batch_label="unit")

    assert hashlib.sha256(source.read_bytes()).hexdigest() == before_hash
    assert result.output_path.is_file()
    assert content is not None
    text = result.output_path.read_text(encoding="utf-8")
    assert "source_raw_input:" in text
    assert "cleanup_score:" in text
    assert "cleanup_grade: cleaned-transcript-80" in text
    assert "cleanup_method: machine-assisted-caption-cleanup" in text
    assert "human_review: spot-check" in text
    assert "audio_verified: false" in text
    assert "proper_noun_policy: known-glossary-only" in text
    assert "Professor Marandi" in text
    assert "Professor Mandi" not in text
    assert "Kind: captions" not in text
    assert "Language: en" not in text


def test_glossary_only_replaces_known_terms_and_leaves_unknowns() -> None:
    text, corrections = clean.apply_glossary("Zalinski met Unknownistan near the sea of Azorov.")

    assert text == "Zelensky met Unknownistan near the Sea of Azov."
    assert corrections == {
        "sea of Azorov -> Sea of Azov": 1,
        "Zalinski -> Zelensky": 1,
    }


def test_guest_glossary_is_limited_to_declared_guest() -> None:
    text = "Andre Martiano joined Andre after the break."

    unchanged, no_corrections = clean.apply_glossary(text, {"guest": "Someone Else"})
    corrected, corrections = clean.apply_glossary(text, {"guest": "Andrei Martyanov"})

    assert unchanged == text
    assert no_corrections == {}
    assert corrected == "Andrei Martyanov joined Andrei after the break."
    assert corrections == {
        "Andre Martiano -> Andrei Martyanov": 1,
        "Andre -> Andrei": 1,
    }


def test_guest_glossary_supports_second_declared_guest_alias() -> None:
    text = "Larry Wilkinson and Larry Wilkenson joined the panel."

    unchanged, no_corrections = clean.apply_glossary(text, {"guest": "Andrei Martyanov"})
    corrected, corrections = clean.apply_glossary(text, {"guest": "Larry Wilkerson"})

    assert unchanged == text
    assert no_corrections == {}
    assert corrected == "Larry Wilkerson and Larry Wilkerson joined the panel."
    assert corrections == {
        "Larry Wilkinson -> Larry Wilkerson": 1,
        "Larry Wilkenson -> Larry Wilkerson": 1,
    }


def test_guest_name_residual_prevents_perfect_score() -> None:
    components = clean.compute_components(
        source_meta={"source_url": "https://www.youtube.com/watch?v=abc123def45", "pub_date": "2026-01-01", "title": "Example", "guest": "Andrei Martyanov"},
        source_body="Andre Martiano " + _body(100),
        cleaned_body="Andre Martiano " + _body(100),
        artifact_removed_count=0,
        duplicate_removed_count=0,
        corrections={},
        residual_terms=clean.residual_noise_terms("Andre Martiano " + _body(100), {"guest": "Andrei Martyanov"}),
    )

    assert clean.score_from_components(components) < 100
    assert "Andre Martiano" in components["residual_noise_scan"]["terms"]


def test_score_below_80_stays_cleaned_draft() -> None:
    components = clean.compute_components(
        source_meta={},
        source_body=_body(100),
        cleaned_body=_body(100),
        artifact_removed_count=0,
        duplicate_removed_count=0,
        corrections={},
        residual_terms=["Mandi", "Zalinski", "TAD"],
    )
    score = clean.score_from_components(components)
    grade = "cleaned-transcript-80" if score >= 80 else "transcript-grade-cleaned-draft"

    assert score < 80
    assert grade == "transcript-grade-cleaned-draft"


def test_main_writes_batch_receipts(tmp_path: Path, capsys) -> None:
    source = tmp_path / "raw.md"
    source.write_text(_raw_input("Kind: captions\nLanguage: en\n" + _body(95)), encoding="utf-8")
    receipt_root = tmp_path / "artifacts"

    rc = clean.main(
        [
            "--raw-input",
            str(source),
            "--receipt-root",
            str(receipt_root),
            "--run-id",
            "batch",
            "--batch-label",
            "jan-2-cleaned-80",
            "--apply",
        ]
    )

    captured = capsys.readouterr()
    assert rc == 0
    assert '"cleanup_grade": "cleaned-transcript-80"' in captured.out
    assert (receipt_root / "batch" / "cleanup-ledger.jsonl").is_file()
    assert (receipt_root / "batch" / "cleanup-summary.md").is_file()
    assert next((receipt_root / "batch" / "details").glob("*.cleanup.json")).is_file()


def test_main_accepts_raw_input_list(tmp_path: Path, capsys) -> None:
    source = tmp_path / "raw.md"
    source.write_text(_raw_input("Kind: captions\nLanguage: en\n" + _body(95)), encoding="utf-8")
    raw_list = tmp_path / "raw-inputs.txt"
    raw_list.write_text(f"{source}\n", encoding="utf-8")

    rc = clean.main(
        [
            "--raw-input-list",
            str(raw_list),
            "--receipt-root",
            str(tmp_path / "receipts"),
            "--run-id",
            "list-run",
            "--apply",
        ]
    )

    captured = capsys.readouterr()
    assert rc == 0
    assert '"status": "cleaned"' in captured.out
    assert source.with_name("raw.cleaned.md").is_file()
