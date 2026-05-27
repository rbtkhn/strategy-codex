from __future__ import annotations

import json
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
    assert "source_note: Auto-generated YouTube subtitles extracted with yt_dlp. Not human-verified verbatim." in text
    assert "body_word_count: 90" in text
    assert "verification_ok: true" in text
    assert "verification_reason: ok" in text
    assert "evidence_grade: transcript-bearing" in text
    assert result["body_word_count"] == 90
    assert result["evidence_grade"] == "transcript-bearing"


def test_materialize_uses_operator_metadata_when_youtube_metadata_fetch_fails(tmp_path: Path, monkeypatch) -> None:
    video_id = "metafail123"

    monkeypatch.setattr(
        mat,
        "fetch_metadata",
        lambda _url, _auth=None: (video_id, {}, "metadata fetch failed"),
    )
    monkeypatch.setattr(
        mat,
        "fetch_subtitles_ytdlp",
        lambda _video_id, _langs: (_caption(), "manual", "en-orig", None),
    )

    result = mat.materialize_one(
        mat.ApprovedUrl(
            url=f"https://www.youtube.com/watch?v={video_id}",
            title="Operator Supplied Episode",
            pub_date="2026-05-16",
            show="Alexander Mercouris",
            host="Alexander Mercouris",
            thread="mercouris",
            channel_slug="alex-mercouris",
            file_prefix="youtube-alex-mercouris",
        ),
        notebook_root=tmp_path / "codex" / "2026",
        ingest_date="2026-05-17",
        apply=True,
        watchlist={},
    )

    assert result["status"] == "materialized"
    assert result["metadata_bypassed"] is True
    assert result["verification_ok"] is True
    assert result["caption_kind"] == "manual"
    text = Path(result["output_path"]).read_text(encoding="utf-8")
    assert "title: Operator Supplied Episode" in text
    assert "pub_date: 2026-05-16" in text
    assert "show: Alexander Mercouris" in text
    assert "host: Alexander Mercouris" in text
    assert "thread: mercouris" in text
    assert f"source_url: https://www.youtube.com/watch?v={video_id}" in text


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
                "output_path": "source-archive/statecraft/2026-05-12/example.md",
                "verification_reason": "ok",
                "body_word_count": 90,
                "evidence_grade": "transcript-bearing",
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
    assert (receipt_dir / "successful-raw-inputs.txt").is_file()
    assert (receipt_dir / "capture-summary.md").is_file()


def test_write_receipts_outputs_manual_scaffold_for_failed_fetch(tmp_path: Path) -> None:
    receipt_dir = tmp_path / "receipts"
    notebook_root = tmp_path / "codex" / "2026"
    paths = mat.write_receipts(
        [
            {
                "url": "https://www.youtube.com/watch?v=abc123def45",
                "youtube_id": "abc123def45",
                "title": "Prof. Jeffrey Sachs: What the Chinese Think of Trump",
                "pub_date": "2026-05-15",
                "status": "failed-fetch",
                "verification_reason": "metadata fetch failed",
                "body_word_count": 0,
                "file_prefix": "transcript-napolitano",
                "channel_slug": "napolitano",
                "show": "Judging Freedom",
                "host": "Judge Andrew Napolitano",
                "guest": "Jeffrey Sachs",
                "thread": "napolitano",
            }
        ],
        receipt_dir,
        notebook_root=notebook_root,
        ingest_date="2026-05-15",
    )

    index = Path(paths["manual_scaffold_index"])
    queue = Path(paths["manual_curation_queue"])
    scaffold = next(path for path in (receipt_dir / "manual-transcript-scaffolds").glob("*.md") if not path.name.endswith(".draft.md"))
    draft = receipt_dir / "manual-transcript-scaffolds" / scaffold.name.replace(".md", ".draft.md")
    paste_body = receipt_dir / "manual-transcript-scaffolds" / scaffold.name.replace(".md", ".paste-body.txt")
    verify = receipt_dir / "manual-transcript-scaffolds" / scaffold.name.replace(".md", ".verify.ps1")
    text = scaffold.read_text(encoding="utf-8")
    assert index.is_file()
    assert queue.is_file()
    assert draft.is_file()
    assert paste_body.is_file()
    assert verify.is_file()
    assert paths["manual_scaffold_count"] == "1"
    assert "WORK only; not Record" in text
    assert "Curator Files" in text
    assert "transcript_type: operator_pasted_transcript" in text
    assert "guest: Jeffrey Sachs" in text
    assert "PASTE FULL TRANSCRIPT BODY HERE" in text
    assert "transcript-napolitano-prof-jeffrey-sachs-what-the-chinese-think-of-trump-2026-05-15.md" in text
    assert "Manual curation queue" in queue.read_text(encoding="utf-8")
    assert "needs-paste" in queue.read_text(encoding="utf-8")
    assert "PASTE FULL TRANSCRIPT BODY HERE" in draft.read_text(encoding="utf-8")
    assert "--- PASTE FULL TRANSCRIPT BODY BELOW ---" in paste_body.read_text(encoding="utf-8")
    assert "materialize_youtube_raw_input.py --raw-input" in verify.read_text(encoding="utf-8")


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


def test_main_with_appearances_writes_capture_packet(tmp_path: Path, monkeypatch, capsys) -> None:
    video_id = "ritter12345"
    notebook_root = tmp_path / "codex" / "2026"
    speaker_obj = notebook_root / "speakers" / "ritter" / "ritter-speaker-object.md"
    speaker_obj.parent.mkdir(parents=True)
    speaker_obj.write_text("# Ritter speaker object\n", encoding="utf-8")
    arc = notebook_root / "diesen" / "diesen-ritter-speaker-arc.md"
    arc.parent.mkdir(parents=True)
    arc.write_text("# Diesen x Ritter\n", encoding="utf-8")

    monkeypatch.setattr(mat, "DEFAULT_ROUTING_OUT", tmp_path / "artifacts" / "speaker-routing")
    monkeypatch.setattr(mat, "DEFAULT_ACTION_OUT", tmp_path / "artifacts" / "speaker-memory-actions")
    monkeypatch.setattr(mat, "DEFAULT_HOST_QUALITY_OUT", tmp_path / "artifacts" / "host-shelf-quality")
    monkeypatch.setattr(
        mat,
        "fetch_metadata_ytdlp",
        lambda _video_id: {
            "id": video_id,
            "title": "Scott Ritter: Escalation Lessons",
            "upload_date": "20260514",
            "channel_id": _spec().channel_id,
            "channel": "Glenn Diesen",
            "webpage_url": f"https://www.youtube.com/watch?v={video_id}",
        },
    )
    monkeypatch.setattr(mat, "fetch_subtitles_ytdlp", lambda _video_id, _langs: (_caption(95), "auto", "en", None))

    rc = mat.main(
        [
            "--url",
            f"https://www.youtube.com/watch?v={video_id}",
            "--notebook-root",
            str(notebook_root),
            "--receipt-root",
            str(tmp_path / "receipts"),
            "--run-id",
            "dense-run",
            "--apply",
            "--with-appearances",
            "--purpose",
            "densification",
            "--tranche-label",
            "ritter-test",
        ]
    )

    captured = capsys.readouterr()
    assert rc == 0
    assert '"status": "materialized"' in captured.out
    summary = tmp_path / "receipts" / "dense-run" / "capture-summary.md"
    assert "purpose: `densification`" in summary.read_text(encoding="utf-8")
    assert "tranche: `ritter-test`" in summary.read_text(encoding="utf-8")
    assert "speaker_routing_markdown" in summary.read_text(encoding="utf-8")
    assert "memory_action_queue_markdown" in summary.read_text(encoding="utf-8")
    assert "quality scope: `full-host-month`" in summary.read_text(encoding="utf-8")
    assert "quality closeout: Structure:" in summary.read_text(encoding="utf-8")
    assert "host_quality_reports" in summary.read_text(encoding="utf-8")
    routing_files = list((tmp_path / "artifacts" / "speaker-routing" / "dense-run").rglob("speaker-routing-queue.jsonl"))
    action_files = list((tmp_path / "artifacts" / "speaker-memory-actions" / "dense-run").rglob("memory-action-queue.jsonl"))
    assert len(routing_files) == 1
    assert len(action_files) == 1
    quality_files = list((tmp_path / "artifacts" / "host-shelf-quality").rglob("quality-summary.json"))
    assert len(quality_files) == 1
    route_payload = json.loads(routing_files[0].read_text(encoding="utf-8").splitlines()[0])
    assert route_payload["appearance"]["speaker_slug"] == "ritter"
    assert route_payload["route_type"] == "existing-speaker-arc"
    assert route_payload["evidence_grade"] == "transcript-bearing"
    raw_text = next(notebook_root.rglob("youtube-glenn-diesen-scott-ritter-escalation-lessons-*.md")).read_text(
        encoding="utf-8"
    )
    assert "guest: Ritter" in raw_text
    assert "guest_inference: exact-title-match" in raw_text


def test_raw_input_list_with_appearances_does_not_fetch_or_write_transcripts(tmp_path: Path, monkeypatch, capsys) -> None:
    notebook_root = tmp_path / "codex" / "2026"
    obj = notebook_root / "speakers" / "ritter" / "ritter-speaker-object.md"
    obj.parent.mkdir(parents=True)
    obj.write_text("# Ritter speaker object\n", encoding="utf-8")
    raw = notebook_root / "raw-input" / "2026-05-12" / "existing-ritter.md"
    raw.parent.mkdir(parents=True)
    raw.write_text(
        "---\n"
        "ingest_date: 2026-05-15\n"
        "pub_date: 2026-05-12\n"
        "kind: transcript\n"
        "source_type: youtube\n"
        "transcript_type: auto_subtitles_vtt\n"
        "title: Existing Ritter\n"
        "source_url: https://www.youtube.com/watch?v=rawlist1234\n"
        "source_note: Auto-captions extracted with yt_dlp.\n"
        "guest: Scott Ritter\n"
        "host: Glenn Diesen\n"
        "show: Glenn Diesen\n"
        "thread: diesen\n"
        "---\n\n"
        "# Existing Ritter\n\n"
        f"{_caption(90)}\n",
        encoding="utf-8",
    )
    raw_list = tmp_path / "raw-inputs.txt"
    raw_list.write_text(f"{raw}\n", encoding="utf-8")

    def fail_fetch(_video_id: str):
        raise AssertionError("metadata fetch should not run for raw-input-list")

    monkeypatch.setattr(mat, "fetch_metadata_ytdlp", fail_fetch)
    monkeypatch.setattr(mat, "DEFAULT_ROUTING_OUT", tmp_path / "artifacts" / "speaker-routing")
    monkeypatch.setattr(mat, "DEFAULT_ACTION_OUT", tmp_path / "artifacts" / "speaker-memory-actions")

    rc = mat.main(
        [
            "--raw-input-list",
            str(raw_list),
            "--notebook-root",
            str(notebook_root),
            "--receipt-root",
            str(tmp_path / "receipts"),
            "--run-id",
            "existing-run",
            "--with-appearances",
        ]
    )

    captured = capsys.readouterr()
    assert rc == 0
    assert '"existing_raw_input": true' in captured.out
    assert '"status": "already-present-valid"' in captured.out
    assert len(list((tmp_path / "artifacts" / "speaker-routing" / "existing-run").rglob("appearance-ledger.jsonl"))) == 1


def test_no_quality_report_suppresses_quality_artifacts(tmp_path: Path, monkeypatch, capsys) -> None:
    notebook_root = tmp_path / "codex" / "2026"
    obj = notebook_root / "speakers" / "ritter" / "ritter-speaker-object.md"
    obj.parent.mkdir(parents=True)
    obj.write_text("# Ritter speaker object\n", encoding="utf-8")
    raw = notebook_root / "raw-input" / "2026-05-12" / "existing-ritter.md"
    raw.parent.mkdir(parents=True)
    raw.write_text(
        "---\n"
        "ingest_date: 2026-05-15\n"
        "pub_date: 2026-05-12\n"
        "kind: transcript\n"
        "source_type: youtube\n"
        "transcript_type: auto_subtitles_vtt\n"
        "title: Existing Ritter\n"
        "source_url: https://www.youtube.com/watch?v=noquality12\n"
        "source_note: Auto-captions extracted with yt_dlp.\n"
        "guest: Scott Ritter\n"
        "host: Glenn Diesen\n"
        "show: Glenn Diesen\n"
        "thread: diesen\n"
        "---\n\n"
        "# Existing Ritter\n\n"
        f"{_caption(90)}\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(mat, "DEFAULT_ROUTING_OUT", tmp_path / "artifacts" / "speaker-routing")
    monkeypatch.setattr(mat, "DEFAULT_ACTION_OUT", tmp_path / "artifacts" / "speaker-memory-actions")
    monkeypatch.setattr(mat, "DEFAULT_HOST_QUALITY_OUT", tmp_path / "artifacts" / "host-shelf-quality")

    rc = mat.main(
        [
            "--raw-input",
            str(raw),
            "--notebook-root",
            str(notebook_root),
            "--receipt-root",
            str(tmp_path / "receipts"),
            "--run-id",
            "no-quality-run",
            "--apply",
            "--with-appearances",
            "--no-quality-report",
        ]
    )

    captured = capsys.readouterr()
    assert rc == 0
    assert '"status": "already-present-valid"' in captured.out
    assert not (tmp_path / "artifacts" / "host-shelf-quality").exists()
    summary = (tmp_path / "receipts" / "no-quality-run" / "capture-summary.md").read_text(encoding="utf-8")
    assert "quality closeout: Structure:" not in summary


def test_quality_report_from_single_raw_input_expands_to_full_month(tmp_path: Path, monkeypatch, capsys) -> None:
    notebook_root = tmp_path / "codex" / "2026"
    for slug, title in (("ritter", "Scott Ritter"), ("freeman", "Chas Freeman")):
        obj = notebook_root / "speakers" / slug / f"{slug}-speaker-object.md"
        obj.parent.mkdir(parents=True)
        obj.write_text(f"# {title}\n", encoding="utf-8")
        arc = notebook_root / "diesen" / f"diesen-{slug}-speaker-arc.md"
        arc.parent.mkdir(parents=True, exist_ok=True)
        arc.write_text(f"# Diesen x {title}\n", encoding="utf-8")

    raw_dir = notebook_root / "raw-input" / "2026-05-12"
    raw_dir.mkdir(parents=True)
    selected = raw_dir / "selected-ritter.md"
    selected.write_text(
        "---\n"
        "ingest_date: 2026-05-15\n"
        "pub_date: 2026-05-12\n"
        "kind: transcript\n"
        "source_type: youtube\n"
        "transcript_type: auto_subtitles_vtt\n"
        "title: Selected Ritter\n"
        "source_url: https://www.youtube.com/watch?v=selected123\n"
        "source_note: Auto-captions extracted with yt_dlp.\n"
        "guest: Scott Ritter\n"
        "host: Glenn Diesen\n"
        "show: Glenn Diesen\n"
        "thread: diesen\n"
        "---\n\n"
        "# Selected Ritter\n\n"
        f"{_caption(90)}\n",
        encoding="utf-8",
    )
    sibling = raw_dir / "sibling-freeman.md"
    sibling.write_text(
        selected.read_text(encoding="utf-8")
        .replace("Selected Ritter", "Sibling Freeman")
        .replace("selected123", "sibling1234")
        .replace("Scott Ritter", "Chas Freeman"),
        encoding="utf-8",
    )

    monkeypatch.setattr(mat, "DEFAULT_ROUTING_OUT", tmp_path / "artifacts" / "speaker-routing")
    monkeypatch.setattr(mat, "DEFAULT_ACTION_OUT", tmp_path / "artifacts" / "speaker-memory-actions")
    monkeypatch.setattr(mat, "DEFAULT_HOST_QUALITY_OUT", tmp_path / "artifacts" / "host-shelf-quality")

    rc = mat.main(
        [
            "--raw-input",
            str(selected),
            "--notebook-root",
            str(notebook_root),
            "--receipt-root",
            str(tmp_path / "receipts"),
            "--run-id",
            "single-run",
            "--apply",
            "--with-appearances",
        ]
    )

    captured = capsys.readouterr()
    assert rc == 0
    assert '"status": "already-present-valid"' in captured.out
    summary = (tmp_path / "receipts" / "single-run" / "capture-summary.md").read_text(encoding="utf-8")
    quality_json = next((tmp_path / "artifacts" / "host-shelf-quality").rglob("quality-summary.json"))
    quality_payload = json.loads(quality_json.read_text(encoding="utf-8"))
    assert "quality scope: `full-host-month`" in summary
    assert quality_payload["input_scope"] == "full-host-month"
    assert quality_payload["raw_input_count"] == 2


def test_existing_legacy_raw_input_can_route_for_appearance(tmp_path: Path) -> None:
    raw = tmp_path / "codex" / "2026" / "raw-input" / "2026-04-20" / "legacy.md"
    raw.parent.mkdir(parents=True)
    raw.write_text(
        "---\n"
        "pub_date: 2026-04-20\n"
        "title: Legacy full transcript\n"
        "source_url: https://www.youtube.com/watch?v=legacy12345\n"
        "kind: transcript\n"
        "---\n\n"
        "# Legacy full transcript\n\n"
        f"{_caption(90)}\n",
        encoding="utf-8",
    )

    result = mat.materialize_existing_raw_input(raw)

    assert result["status"] == "already-present-legacy"
    assert result["existing_raw_input"] is True
    assert result["evidence_grade"] == "legacy-appearance-only"
    assert "appearance-eligible legacy raw-input" in result["verification_reason"]


def test_dry_run_with_appearances_does_not_route(tmp_path: Path, monkeypatch) -> None:
    video_id = "dryap123456"
    notebook_root = tmp_path / "codex" / "2026"
    monkeypatch.setattr(mat, "DEFAULT_ROUTING_OUT", tmp_path / "artifacts" / "speaker-routing")
    monkeypatch.setattr(mat, "DEFAULT_ACTION_OUT", tmp_path / "artifacts" / "speaker-memory-actions")
    monkeypatch.setattr(mat, "DEFAULT_HOST_QUALITY_OUT", tmp_path / "artifacts" / "host-shelf-quality")
    monkeypatch.setattr(
        mat,
        "fetch_metadata_ytdlp",
        lambda _video_id: {
            "id": video_id,
            "title": "Dry Appearance Episode",
            "upload_date": "20260514",
            "channel_id": _spec().channel_id,
            "webpage_url": f"https://www.youtube.com/watch?v={video_id}",
        },
    )
    monkeypatch.setattr(mat, "fetch_subtitles_ytdlp", lambda _video_id, _langs: (_caption(95), "auto", "en", None))

    rc = mat.main(
        [
            "--url",
            f"https://www.youtube.com/watch?v={video_id}",
            "--notebook-root",
            str(notebook_root),
            "--receipt-root",
            str(tmp_path / "receipts"),
            "--run-id",
            "dry-appearance",
            "--no-apply",
            "--with-appearances",
        ]
    )

    assert rc == 0
    assert not (tmp_path / "artifacts").exists()
    assert (tmp_path / "receipts" / "dry-appearance" / "successful-raw-inputs.txt").read_text(encoding="utf-8") == ""


def test_guest_inference_exact_match_and_ambiguous_refusal(tmp_path: Path) -> None:
    notebook_root = tmp_path / "codex" / "2026"
    for slug in ("ritter", "freeman"):
        folder = notebook_root / "speakers" / slug
        folder.mkdir(parents=True)
        (folder / f"{slug}-speaker-object.md").write_text(f"# {slug}\n", encoding="utf-8")

    guest, method = mat.infer_guest_from_title("Scott Ritter on escalation", notebook_root)
    assert guest == "Ritter"
    assert method == "exact-title-match"

    guest, method = mat.infer_guest_from_title("Ritter and Freeman debate escalation", notebook_root)
    assert guest is None
    assert method is None


def test_guest_inference_prefers_non_host_title_match(tmp_path: Path, monkeypatch) -> None:
    speakers_dir = tmp_path / "codex" / "speakers"
    for slug in ("crooke", "davis", "parsi", "ritter"):
        folder = speakers_dir / slug
        folder.mkdir(parents=True)
        (folder / f"{slug}-speaker-object.md").write_text(f"# {slug}\n", encoding="utf-8")
    monkeypatch.setattr(mat.speaker_routing, "DEFAULT_SPEAKERS_DIR", speakers_dir)

    guest, method = mat.infer_guest_from_title(
        "IRAN is JUST GETTING STARTED /Alastair Crooke & Lt Col Daniel Davis",
        tmp_path / "codex" / "years" / "2026",
        "Daniel Davis",
    )
    assert guest == "Crooke"
    assert method == "exact-title-match"

    guest, method = mat.infer_guest_from_title(
        "IRAN MAKING IT PAINFUL FOR U.S. /Trita Parsi & Lt Col Daniel Davis",
        tmp_path / "codex" / "years" / "2026",
        "Daniel Davis",
    )
    assert guest == "Parsi"
    assert method == "exact-title-match"

    guest, method = mat.infer_guest_from_title(
        "Scott Ritter, Danny Davis Combat Vets: Can the US Force Hormuz Open?",
        tmp_path / "codex" / "years" / "2026",
        "Daniel Davis",
    )
    assert guest == "Ritter"
    assert method == "exact-title-match"


def test_guest_inference_uses_known_alias_when_speaker_folder_missing(tmp_path: Path, monkeypatch) -> None:
    speakers_dir = tmp_path / "codex" / "speakers"
    folder = speakers_dir / "davis"
    folder.mkdir(parents=True)
    (folder / "davis-speaker-object.md").write_text("# Davis\n", encoding="utf-8")
    monkeypatch.setattr(mat.speaker_routing, "DEFAULT_SPEAKERS_DIR", speakers_dir)

    guest, method = mat.infer_guest_from_title(
        "IRAN WAR GLOBAL RESET /Patrick Henningsen & Lt Col Daniel Davis",
        tmp_path / "codex" / "years" / "2026",
        "Daniel Davis",
    )
    assert guest == "Henningsen"
    assert method == "title-known-speaker-match"


def test_materialized_manual_subtitles_are_not_labeled_auto_captions(tmp_path: Path, monkeypatch) -> None:
    video_id = "manual12345"
    monkeypatch.setattr(
        mat,
        "fetch_metadata_ytdlp",
        lambda _video_id: {
            "id": video_id,
            "title": "Manual Caption Episode",
            "upload_date": "20260516",
            "channel_id": _spec().channel_id,
            "channel": "Glenn Diesen",
            "webpage_url": f"https://www.youtube.com/watch?v={video_id}",
        },
    )
    monkeypatch.setattr(mat, "fetch_subtitles_ytdlp", lambda _video_id, _langs: (_caption(), "manual", "en-orig", None))

    result = mat.materialize_one(
        mat.ApprovedUrl(url=f"https://www.youtube.com/watch?v={video_id}"),
        notebook_root=tmp_path / "codex" / "2026",
        ingest_date="2026-05-17",
        apply=True,
        watchlist={"glenn-diesen": _spec()},
    )

    text = Path(result["output_path"]).read_text(encoding="utf-8")
    assert result["status"] == "materialized"
    assert "transcript_type: manual_subtitles_vtt" in text
    assert "caption_kind: manual" in text
    assert "source_note: Manual YouTube subtitles extracted with yt_dlp. Not human-verified verbatim." in text
    assert "Auto-captions extracted" not in text


def test_host_only_title_match_does_not_write_host_as_guest(tmp_path: Path, monkeypatch) -> None:
    video_id = "hostonly123"
    notebook_root = tmp_path / "codex" / "2026"
    speaker = notebook_root / "speakers" / "davis"
    speaker.mkdir(parents=True)
    (speaker / "davis-speaker-object.md").write_text("# Davis\n", encoding="utf-8")
    monkeypatch.setattr(
        mat,
        "fetch_metadata_ytdlp",
        lambda _video_id: {
            "id": video_id,
            "title": "Deep Dive Intel Briefing 5/16/2026 Lt Col Daniel Davis",
            "upload_date": "20260516",
            "channel": "Daniel Davis Deep Dive",
            "webpage_url": f"https://www.youtube.com/watch?v={video_id}",
        },
    )
    monkeypatch.setattr(mat, "fetch_subtitles_ytdlp", lambda _video_id, _langs: (_caption(), "manual", "en-orig", None))

    result = mat.materialize_one(
        mat.ApprovedUrl(
            url=f"https://www.youtube.com/watch?v={video_id}",
            show="Daniel Davis Deep Dive",
            host="Daniel Davis",
            thread="davis",
            channel_slug="daniel-davis-deep-dive",
            file_prefix="youtube-daniel-davis-deep-dive",
        ),
        notebook_root=notebook_root,
        ingest_date="2026-05-17",
        apply=True,
        watchlist={},
    )

    text = Path(result["output_path"]).read_text(encoding="utf-8")
    assert result["status"] == "materialized"
    assert "host: Daniel Davis" in text
    assert "\nguest:" not in text
    assert "guest_inference: host-only-title-match" in text
    assert result["guest"] == ""
    assert result["guest_inference"] == "host-only-title-match"


def test_with_appearances_skips_unresolved_guest_capture(tmp_path: Path, monkeypatch, capsys) -> None:
    video_id = "unknown12345"
    notebook_root = tmp_path / "codex" / "2026"
    monkeypatch.setattr(mat, "DEFAULT_ROUTING_OUT", tmp_path / "artifacts" / "speaker-routing")
    monkeypatch.setattr(mat, "DEFAULT_ACTION_OUT", tmp_path / "artifacts" / "speaker-memory-actions")
    monkeypatch.setattr(mat, "DEFAULT_HOST_QUALITY_OUT", tmp_path / "artifacts" / "host-shelf-quality")
    monkeypatch.setattr(
        mat,
        "fetch_metadata_ytdlp",
        lambda _video_id: {
            "id": video_id,
            "title": "Unresolved Guest Episode",
            "upload_date": "20260514",
            "channel_id": _spec().channel_id,
            "channel": "Glenn Diesen",
            "webpage_url": f"https://www.youtube.com/watch?v={video_id}",
        },
    )
    monkeypatch.setattr(mat, "fetch_subtitles_ytdlp", lambda _video_id, _langs: (_caption(95), "auto", "en", None))

    rc = mat.main(
        [
            "--url",
            f"https://www.youtube.com/watch?v={video_id}",
            "--notebook-root",
            str(notebook_root),
            "--receipt-root",
            str(tmp_path / "receipts"),
            "--run-id",
            "unresolved-run",
            "--apply",
            "--with-appearances",
        ]
    )

    captured = capsys.readouterr()
    assert rc == 0
    assert '"status": "materialized"' in captured.out
    assert not (tmp_path / "artifacts" / "speaker-routing").exists()
    assert not (tmp_path / "artifacts" / "speaker-memory-actions").exists()
    assert len(list((tmp_path / "artifacts" / "host-shelf-quality").rglob("quality-summary.json"))) == 1
    summary = (tmp_path / "receipts" / "unresolved-run" / "capture-summary.md").read_text(encoding="utf-8")
    assert "unresolved speaker captures: `1`" in summary
    assert "quality closeout: Structure:" in summary
    assert "Unresolved Guest Episode" in summary


def test_with_appearances_skips_ambiguous_title_inference(tmp_path: Path, monkeypatch, capsys) -> None:
    video_id = "ambig123456"
    notebook_root = tmp_path / "codex" / "2026"
    for slug in ("ritter", "freeman"):
        folder = notebook_root / "speakers" / slug
        folder.mkdir(parents=True)
        (folder / f"{slug}-speaker-object.md").write_text(f"# {slug}\n", encoding="utf-8")

    monkeypatch.setattr(mat, "DEFAULT_ROUTING_OUT", tmp_path / "artifacts" / "speaker-routing")
    monkeypatch.setattr(mat, "DEFAULT_ACTION_OUT", tmp_path / "artifacts" / "speaker-memory-actions")
    monkeypatch.setattr(mat, "DEFAULT_HOST_QUALITY_OUT", tmp_path / "artifacts" / "host-shelf-quality")
    monkeypatch.setattr(
        mat,
        "fetch_metadata_ytdlp",
        lambda _video_id: {
            "id": video_id,
            "title": "Ritter and Freeman debate escalation",
            "upload_date": "20260514",
            "channel_id": _spec().channel_id,
            "channel": "Glenn Diesen",
            "webpage_url": f"https://www.youtube.com/watch?v={video_id}",
        },
    )
    monkeypatch.setattr(mat, "fetch_subtitles_ytdlp", lambda _video_id, _langs: (_caption(95), "auto", "en", None))

    rc = mat.main(
        [
            "--url",
            f"https://www.youtube.com/watch?v={video_id}",
            "--notebook-root",
            str(notebook_root),
            "--receipt-root",
            str(tmp_path / "receipts"),
            "--run-id",
            "ambiguous-run",
            "--apply",
            "--with-appearances",
        ]
    )

    captured = capsys.readouterr()
    assert rc == 0
    assert '"status": "materialized"' in captured.out
    assert not (tmp_path / "artifacts" / "speaker-routing").exists()
    assert not (tmp_path / "artifacts" / "speaker-memory-actions").exists()
    assert len(list((tmp_path / "artifacts" / "host-shelf-quality").rglob("quality-summary.json"))) == 1
    summary = (tmp_path / "receipts" / "ambiguous-run" / "capture-summary.md").read_text(encoding="utf-8")
    assert "unresolved speaker captures: `1`" in summary
    assert "quality closeout: Structure:" in summary
    assert "Ritter and Freeman debate escalation" in summary


def test_summary_grade_capture_is_not_counted_as_transcript_valid(tmp_path: Path) -> None:
    receipt_dir = tmp_path / "receipts"
    paths = mat.write_receipts(
        [
            {
                "url": "https://www.youtube.com/watch?v=abc123def45",
                "title": "Example",
                "status": "materialized",
                "output_path": "source-archive/statecraft/2026-05-12/example.md",
                "verification_reason": "ok",
                "body_word_count": 90,
                "evidence_grade": "summary-grade",
            }
        ],
        receipt_dir,
    )

    summary = Path(paths["capture_summary"]).read_text(encoding="utf-8")
    assert "transcript-valid successes: `0`" in summary
    assert "summary-grade carries: `1`" in summary
