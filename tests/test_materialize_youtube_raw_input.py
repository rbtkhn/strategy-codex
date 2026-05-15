from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import materialize_youtube_raw_input as mat  # noqa: E402


def _spec() -> mat.WatchlistSpec:
    return mat.WatchlistSpec(
        channel_key="glenn-diesen",
        channel_name="Glenn Diesen",
        channel_id="UCZFCDIHTe9HGxtIuVDpBz7g",
        uploads_playlist_id="UUZFCDIHTe9HGxtIuVDpBz7g",
        handle_url="https://www.youtube.com/@GDiesen1",
        show="Glenn Diesen",
        host="Glenn Diesen",
        thread="diesen",
        file_prefix="youtube-glenn-diesen",
        discovery_priority=["uploads_playlist", "channel_feed", "videos_page"],
    )


def _caption(words: int = 90) -> str:
    return " ".join(f"word{i}" for i in range(words))


def _valid_raw(source_url: str = "https://www.youtube.com/watch?v=abc123def45") -> str:
    return (
        "---\n"
        "ingest_date: 2026-05-15\n"
        "pub_date: 2026-05-12\n"
        "kind: transcript\n"
        "source_type: youtube\n"
        "transcript_type: auto_subtitles_vtt\n"
        "title: Example video\n"
        f"source_url: {source_url}\n"
        "source_note: Auto-captions extracted with yt_dlp.\n"
        "---\n\n"
        "# Example video\n\n"
        f"{_caption()}\n"
    )


def test_valid_transcript_body_passes_verification() -> None:
    result = mat.verify_raw_input_text(_valid_raw())

    assert result.ok
    assert result.word_count >= mat.MIN_BODY_WORDS
    assert result.body_chars >= mat.MIN_BODY_CHARS


def test_header_only_raw_input_fails_verification() -> None:
    text = (
        "---\n"
        "pub_date: 2026-05-12\n"
        "source_url: https://www.youtube.com/watch?v=abc123def45\n"
        "title: Example video\n"
        "source_type: youtube\n"
        "transcript_type: auto_subtitles_vtt\n"
        "source_note: Listed only.\n"
        "---\n\n"
        "# Example video\n\n"
    )

    result = mat.verify_raw_input_text(text)

    assert not result.ok
    assert "body too short" in result.reason


def test_placeholder_body_fails_verification() -> None:
    text = _valid_raw().replace("word1", "transcript pending")

    result = mat.verify_raw_input_text(text)

    assert not result.ok
    assert "placeholder body" in result.reason


def test_missing_transcript_type_fails_verification() -> None:
    text = _valid_raw().replace("transcript_type: auto_subtitles_vtt\n", "")

    result = mat.verify_raw_input_text(text)

    assert not result.ok
    assert result.reason == "missing transcript_type"


def test_heading_only_words_do_not_count_as_transcript_body() -> None:
    text = (
        "---\n"
        "ingest_date: 2026-05-15\n"
        "pub_date: 2026-05-12\n"
        "kind: transcript\n"
        "source_type: youtube\n"
        "transcript_type: auto_subtitles_vtt\n"
        "title: Example video\n"
        "source_url: https://www.youtube.com/watch?v=abc123def45\n"
        "source_note: Auto-captions extracted with yt_dlp.\n"
        "---\n\n"
        f"# {_caption(100)}\n\n"
    )

    result = mat.verify_raw_input_text(text)

    assert not result.ok
    assert result.reason == "body too short: 0 words"


def test_materialize_url_maps_watchlist_defaults_and_writes_raw_input(tmp_path: Path, monkeypatch) -> None:
    video_id = "abc123def45"

    monkeypatch.setattr(
        mat,
        "fetch_metadata_ytdlp",
        lambda _video_id: {
            "id": video_id,
            "title": "Chas Freeman: Trump Goes to Beijing",
            "upload_date": "20260512",
            "channel_id": _spec().channel_id,
            "channel": "Glenn Diesen",
            "channel_url": "https://www.youtube.com/@GDiesen1",
            "webpage_url": f"https://www.youtube.com/watch?v={video_id}",
        },
    )
    monkeypatch.setattr(
        mat,
        "fetch_subtitles_ytdlp",
        lambda _video_id, _langs: (_caption(), "auto", "en-orig", None),
    )

    result = mat.materialize_one(
        mat.ApprovedUrl(url=f"https://www.youtube.com/watch?v={video_id}"),
        notebook_root=tmp_path / "codex" / "2026",
        ingest_date="2026-05-15",
        apply=True,
        watchlist={"glenn-diesen": _spec()},
    )

    assert result["status"] == "materialized"
    out = Path(result["output_path"])
    assert out.is_file()
    assert out.parent.name == "2026-05-12"
    assert out.name.startswith("youtube-glenn-diesen-chas-freeman-trump-goes-to-beijing")
    text = out.read_text(encoding="utf-8")
    assert "show: Glenn Diesen" in text
    assert "host: Glenn Diesen" in text
    assert "thread: diesen" in text
    assert "transcript_type: auto_subtitles_vtt" in text


def test_existing_valid_raw_input_returns_already_present_without_fetch(tmp_path: Path, monkeypatch) -> None:
    notebook_root = tmp_path / "codex" / "2026"
    existing = notebook_root / "raw-input" / "2026-05-12" / "existing.md"
    existing.parent.mkdir(parents=True)
    existing.write_text(_valid_raw(), encoding="utf-8")

    def fail_fetch(_video_id: str):
        raise AssertionError("metadata fetch should not run for existing valid raw-input")

    monkeypatch.setattr(mat, "fetch_metadata_ytdlp", fail_fetch)

    result = mat.materialize_one(
        mat.ApprovedUrl(url="https://www.youtube.com/watch?v=abc123def45"),
        notebook_root=notebook_root,
        ingest_date="2026-05-15",
        apply=True,
        watchlist={"glenn-diesen": _spec()},
    )

    assert result["status"] == "already-present-valid"
    assert Path(result["output_path"]) == existing


def test_dry_run_reports_output_without_writing_raw_input(tmp_path: Path, monkeypatch) -> None:
    video_id = "dryrun12345"

    monkeypatch.setattr(
        mat,
        "fetch_metadata_ytdlp",
        lambda _video_id: {
            "id": video_id,
            "title": "Dry Run Episode",
            "upload_date": "20260513",
            "channel_id": _spec().channel_id,
            "webpage_url": f"https://www.youtube.com/watch?v={video_id}",
        },
    )
    monkeypatch.setattr(
        mat,
        "fetch_subtitles_ytdlp",
        lambda _video_id, _langs: (_caption(), "auto", "en", None),
    )

    result = mat.materialize_one(
        mat.ApprovedUrl(url=f"https://www.youtube.com/watch?v={video_id}"),
        notebook_root=tmp_path / "codex" / "2026",
        ingest_date="2026-05-15",
        apply=False,
        watchlist={"glenn-diesen": _spec()},
    )

    assert result["status"] == "dry-run"
    assert result["verification_ok"] is True
    assert result["output_path"].endswith("youtube-glenn-diesen-dry-run-episode-2026-05-13.md")
    assert not Path(result["output_path"]).exists()


def test_write_receipts_outputs_ledger_and_summary(tmp_path: Path) -> None:
    receipt_dir = tmp_path / "receipts"
    paths = mat.write_receipts(
        [
            {
                "url": "https://www.youtube.com/watch?v=abc123def45",
                "title": "Example",
                "status": "materialized",
                "output_path": "codex/2026/raw-input/2026-05-12/example.md",
                "verification_reason": "ok",
                "body_word_count": 90,
            }
        ],
        receipt_dir,
    )

    ledger = Path(paths["ledger"])
    summary = Path(paths["summary"])
    assert ledger.is_file()
    assert summary.is_file()
    assert '"status": "materialized"' in ledger.read_text(encoding="utf-8")
    assert "YouTube raw-input materialization summary" in summary.read_text(encoding="utf-8")


def test_main_dry_run_probe_emits_receipts_without_canonical_write(tmp_path: Path, monkeypatch, capsys) -> None:
    video_id = "probe123456"
    notebook_root = tmp_path / "codex" / "2026"
    receipt_root = tmp_path / "receipts"

    monkeypatch.setattr(
        mat,
        "fetch_metadata_ytdlp",
        lambda _video_id: {
            "id": video_id,
            "title": "Probe Episode With Real Body",
            "upload_date": "20260514",
            "channel_id": _spec().channel_id,
            "channel": "Glenn Diesen",
            "channel_url": "https://www.youtube.com/@GDiesen1",
            "webpage_url": f"https://www.youtube.com/watch?v={video_id}",
        },
    )
    monkeypatch.setattr(
        mat,
        "fetch_subtitles_ytdlp",
        lambda _video_id, _langs: (_caption(95), "auto", "en-orig", None),
    )

    rc = mat.main(
        [
            "--url",
            f"https://www.youtube.com/watch?v={video_id}",
            "--notebook-root",
            str(notebook_root),
            "--receipt-root",
            str(receipt_root),
            "--run-id",
            "bernstein-probe",
            "--no-apply",
        ]
    )

    captured = capsys.readouterr()
    assert rc == 0
    assert '"status": "dry-run"' in captured.out
    assert not list(notebook_root.rglob("*.md"))
    ledger = receipt_root / "bernstein-probe" / "materialization-ledger.jsonl"
    summary = receipt_root / "bernstein-probe" / "materialization-summary.md"
    assert ledger.is_file()
    assert summary.is_file()
    assert '"verification_ok": true' in ledger.read_text(encoding="utf-8")
