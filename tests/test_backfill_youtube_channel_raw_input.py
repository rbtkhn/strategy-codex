"""Tests for the graph-first YouTube raw-input helper (no network)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from backfill_youtube_channel_raw_input import (  # noqa: E402
    _direct_channel_index,
    backfill_channel,
    convert_index_to_raw_input,
    infer_guest_from_title,
)

def _write_transcript_fixture(
    output_dir: Path,
    *,
    video_id: str,
    title: str,
    upload_date: str,
    body: str,
    transcript_file: str,
    status: str = "ok",
) -> None:
    (output_dir / "transcripts").mkdir(parents=True, exist_ok=True)
    (output_dir / transcript_file).write_text(
        "# video_id: %s\n# title: %s\n\n%s\n" % (video_id, title, body),
        encoding="utf-8",
    )
    payload = {
        "videos": [
            {
                "video_id": video_id,
                "title": title,
                "upload_date": upload_date,
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "transcript_file": transcript_file,
                "status": status,
            }
        ]
    }
    (output_dir / "index.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

def test_infer_guest_from_title_dialogue_works() -> None:
    assert infer_guest_from_title("Nima x Glenn Diesen - Iran, War, and Order") == "Glenn Diesen"
    assert infer_guest_from_title("Nima x Scott Ritter: The Iran Strategy") == "Scott Ritter"

def test_convert_index_to_raw_input_writes_threaded_capture(tmp_path: Path) -> None:
    out_dir = tmp_path / "youtube"
    nb_root = tmp_path / "notebook"
    upload_date = "2026-04-29"
    transcript_file = "vid1_title.txt"
    _write_transcript_fixture(
        out_dir,
        video_id="abc123def45",
        title="Daniel Davis Deep Dive - Iran War's Global Economic Shockwave",
        upload_date=upload_date,
        body="line one\nline two",
        transcript_file=transcript_file,
    )

    rc = convert_index_to_raw_input(
        output_dir=out_dir,
        notebook_root=nb_root,
        ingest_date="2026-05-01",
        apply=True,
        channel_slug="daniel-davis-deep-dive",
        channel_url="https://www.youtube.com/@DanielDavisDeepDive/videos",
        show="Daniel Davis Deep Dive",
        host="Daniel Davis",
        thread="davis",
        file_prefix="youtube-daniel-davis-deep-dive",
        source_note="Automated YouTube transcript fetch for Daniel Davis Deep Dive.",
        infer_guest=True,
        index_only=False,
    )

    assert rc == 0
    matches = list((nb_root / "raw-input" / upload_date).glob("youtube-daniel-davis-deep-dive-*.md"))
    assert len(matches) == 1
    out = matches[0]
    text = out.read_text(encoding="utf-8")
    assert "thread: davis" in text
    assert "show: Daniel Davis Deep Dive" in text
    assert "host: Daniel Davis" in text
    assert "channel_slug: \"daniel-davis-deep-dive\"" in text
    assert "line one" in text
    assert "line two" in text

def test_convert_index_to_raw_input_allows_threadless_hub(tmp_path: Path) -> None:
    out_dir = tmp_path / "youtube-hub"
    nb_root = tmp_path / "notebook-hub"
    upload_date = "2026-04-29"
    transcript_file = "vid2_title.txt"
    _write_transcript_fixture(
        out_dir,
        video_id="zxy98765432",
        title="The Duran - UAE Quits OPEC As Gulf States Buckle",
        upload_date=upload_date,
        body="alpha\nbeta",
        transcript_file=transcript_file,
    )

    rc = convert_index_to_raw_input(
        output_dir=out_dir,
        notebook_root=nb_root,
        ingest_date="2026-05-01",
        apply=True,
        channel_slug="the-duran",
        channel_url="https://www.youtube.com/@TheDuran/videos",
        show="The Duran",
        host="Alexander Mercouris / Alex Christoforou",
        thread=None,
        file_prefix="youtube-the-duran",
        source_note="Automated YouTube transcript fetch for The Duran hub capture.",
        infer_guest=False,
        index_only=False,
    )

    assert rc == 0
    matches = list((nb_root / "raw-input" / upload_date).glob("youtube-the-duran-*.md"))
    assert len(matches) == 1
    out = matches[0]
    text = out.read_text(encoding="utf-8")
    assert "thread:" not in text
    assert "show: The Duran" in text
    assert "host: Alexander Mercouris / Alex Christoforou" in text
    assert "alpha" in text
    assert "beta" in text

def test_backfill_channel_index_only_single_worker_enriches_metadata(tmp_path: Path, monkeypatch) -> None:
    work_dir = tmp_path / "work"
    nb_root = tmp_path / "notebook"

    monkeypatch.setattr(
        "backfill_youtube_channel_raw_input._direct_channel_index",
        lambda **_: [
            {
                "video_id": "abc123def45",
                "title": "Placeholder",
                "upload_date": "",
                "duration_seconds": "",
                "url": "https://www.youtube.com/watch?v=abc123def45",
                "transcript_file": None,
                "status": "listed_only",
                "language": None,
                "error": None,
            }
        ],
    )
    monkeypatch.setattr(
        "backfill_youtube_channel_raw_input.fetch_metadata_ytdlp",
        lambda video_id, max_attempts=4: {
            "title": f"Title for {video_id}",
            "upload_date": "20260503",
            "duration": 321,
        },
    )

    rc = backfill_channel(
        channel_url="https://www.youtube.com/@Example/videos",
        channel_slug="example",
        show="Example Show",
        host="Example Host",
        thread="example",
        file_prefix="youtube-example",
        source_note="Example index-only mirror.",
        work_dir=work_dir,
        notebook_root=nb_root,
        ingest_date="2026-05-04",
        limit=5,
        apply=True,
        infer_guest=False,
        index_only=True,
        enrich_concurrency=1,
    )

    assert rc == 0
    payload = json.loads((work_dir / "index.json").read_text(encoding="utf-8"))
    assert payload["video_count"] == 1
    assert payload["videos"][0]["title"] == "Title for abc123def45"
    assert payload["videos"][0]["upload_date"] == "20260503"
    assert payload["videos"][0]["duration_seconds"] == "321"
    matches = list((nb_root / "raw-input" / "2026-05-03").glob("youtube-example-*.md"))
    assert len(matches) == 1
    assert "# Title for abc123def45" in matches[0].read_text(encoding="utf-8")

def test_direct_channel_index_routes_through_adapter(monkeypatch) -> None:
    calls: dict[str, object] = {}

    def fake_list(channel_url: str, *, limit: int, cwd: Path, python_cmd: str) -> list[dict[str, str]]:
        calls["channel_url"] = channel_url
        calls["limit"] = limit
        calls["cwd"] = cwd
        calls["python_cmd"] = python_cmd
        return [
            {
                "id": "abc123def45",
                "title": "Example title",
                "upload_date": "",
                "duration": "",
                "url": "https://www.youtube.com/watch?v=abc123def45",
            }
        ]

    monkeypatch.setattr("backfill_youtube_channel_raw_input.list_channel_entries_subprocess", fake_list)
    rows = _direct_channel_index(channel_url="https://www.youtube.com/@Example/videos", limit=3)

    assert calls["channel_url"] == "https://www.youtube.com/@Example/videos"
    assert calls["limit"] == 3
    assert rows == [
        {
            "video_id": "abc123def45",
            "title": "Example title",
            "upload_date": "",
            "duration_seconds": "",
            "url": "https://www.youtube.com/watch?v=abc123def45",
            "transcript_file": None,
            "status": "listed_only",
            "language": None,
            "error": None,
        }
    ]

def test_backfill_channel_transcript_mode_uses_python_cmd(tmp_path: Path, monkeypatch) -> None:
    work_dir = tmp_path / "work"
    nb_root = tmp_path / "notebook"
    called: dict[str, object] = {}

    def fake_run(cmd: list[str], cwd: str | None = None, capture_output: bool = False, text: bool = False):
        called["cmd"] = cmd
        called["cwd"] = cwd

        class Proc:
            returncode = 0

        return Proc()

    def fake_convert_index(**kwargs):
        called["convert_index"] = kwargs
        return 0

    monkeypatch.setattr("backfill_youtube_channel_raw_input.subprocess.run", fake_run)
    monkeypatch.setattr("backfill_youtube_channel_raw_input.convert_index_to_raw_input", fake_convert_index)

    rc = backfill_channel(
        channel_url="https://www.youtube.com/@Example/videos",
        channel_slug="example",
        show="Example Show",
        host="Example Host",
        thread=None,
        file_prefix="youtube-example",
        source_note="Example transcript mirror.",
        work_dir=work_dir,
        notebook_root=nb_root,
        ingest_date="2026-05-04",
        limit=7,
        sleep=0.5,
        apply=False,
        infer_guest=False,
        index_only=False,
    )

    assert rc == 0
    assert called["cmd"][0] == sys.executable
    assert called["cmd"][1].endswith("fetch_youtube_channel_transcripts.py")
    assert "--channel" in called["cmd"]
    assert "--sleep" in called["cmd"]
    assert called["convert_index"]["index_only"] is False
