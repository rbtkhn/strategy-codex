from __future__ import annotations

from datetime import date
from pathlib import Path
from types import SimpleNamespace

_SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
import sys

if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from youtube_transcripts import ytdlp_adapter as adapter  # noqa: E402
from youtube_transcripts.subtitles_ytdlp import fetch_subtitles_ytdlp  # noqa: E402


def test_list_videos_flat_normalizes_watch_urls_and_respects_cutoff(monkeypatch) -> None:
    calls: dict[str, object] = {}

    class FakeYDL:
        def __init__(self, opts: dict[str, object]) -> None:
            calls["opts"] = opts

        def __enter__(self) -> "FakeYDL":
            return self

        def __exit__(self, exc_type, exc, tb) -> bool:
            return False

        def extract_info(self, url: str, download: bool = False) -> dict[str, object]:
            calls["url"] = url
            calls["download"] = download
            return {
                "entries": [
                    {
                        "id": "abc123def45",
                        "title": "Newest",
                        "upload_date": "20260503",
                        "duration": 321,
                        "url": "abc123def45",
                    },
                    {
                        "id": "old123def45",
                        "title": "Older",
                        "upload_date": "20260430",
                        "duration": 111,
                    },
                ]
            }

    monkeypatch.setattr(adapter, "yt_dlp", SimpleNamespace(YoutubeDL=FakeYDL))
    rows = adapter.list_videos_flat(
        "https://www.youtube.com/@Example/videos",
        limit=5,
        stop_before_date=date(2026, 5, 1),
        max_attempts=1,
    )

    assert calls["url"] == "https://www.youtube.com/@Example/videos"
    assert calls["download"] is False
    assert calls["opts"]["playlistend"] == 5
    assert rows == [
        {
            "id": "abc123def45",
            "title": "Newest",
            "upload_date": "20260503",
            "duration": "321",
            "url": "https://www.youtube.com/watch?v=abc123def45",
        }
    ]


def test_fetch_video_metadata_subprocess_builds_module_command(monkeypatch) -> None:
    calls: dict[str, object] = {}

    def fake_run(cmd: list[str], cwd=None, capture_output=False, text=False):
        calls["cmd"] = cmd
        calls["cwd"] = cwd
        calls["capture_output"] = capture_output
        calls["text"] = text
        return SimpleNamespace(returncode=0, stdout='debug\n{"id":"abc123def45","title":"Example"}\n', stderr="")

    monkeypatch.setattr(adapter.subprocess, "run", fake_run)
    data = adapter.fetch_video_metadata_subprocess(
        "abc123def45",
        mode="module",
        python_cmd="python-custom",
        cwd=Path("C:/repo"),
    )

    assert calls["cmd"] == [
        "python-custom",
        "-m",
        "yt_dlp",
        "--quiet",
        "--no-warnings",
        "--skip-download",
        "--no-write-comments",
        "--dump-single-json",
        "https://www.youtube.com/watch?v=abc123def45",
    ]
    assert calls["cwd"] == str(Path("C:/repo"))
    assert calls["capture_output"] is True
    assert calls["text"] is True
    assert data["title"] == "Example"


def test_fetch_subtitles_prefers_manual_file(monkeypatch) -> None:
    class FakeYDL:
        def __init__(self, opts: dict[str, object]) -> None:
            self.opts = opts

        def __enter__(self) -> "FakeYDL":
            return self

        def __exit__(self, exc_type, exc, tb) -> bool:
            return False

        def download(self, urls: list[str]) -> None:
            assert urls == ["https://www.youtube.com/watch?v=abc123def45"]
            base = Path(str(self.opts["outtmpl"]).replace("%(id)s", "abc123def45"))
            base.parent.mkdir(parents=True, exist_ok=True)
            (base.parent / "abc123def45.en.vtt").write_text(
                "WEBVTT\n\nhello manual\n",
                encoding="utf-8",
            )
            (base.parent / "abc123def45.en.auto.vtt").write_text(
                "WEBVTT\n\nhello auto\n",
                encoding="utf-8",
            )

    monkeypatch.setattr(adapter, "yt_dlp", SimpleNamespace(YoutubeDL=FakeYDL))
    text, kind, lang, error = fetch_subtitles_ytdlp("abc123def45", ["en"])

    assert error is None
    assert kind == "manual"
    assert lang == "en"
    assert text == "hello manual"


def test_fetch_subtitles_falls_back_to_auto_file(monkeypatch) -> None:
    class FakeYDL:
        def __init__(self, opts: dict[str, object]) -> None:
            self.opts = opts

        def __enter__(self) -> "FakeYDL":
            return self

        def __exit__(self, exc_type, exc, tb) -> bool:
            return False

        def download(self, urls: list[str]) -> None:
            base = Path(str(self.opts["outtmpl"]).replace("%(id)s", "abc123def45"))
            base.parent.mkdir(parents=True, exist_ok=True)
            (base.parent / "abc123def45.en.auto.vtt").write_text(
                "WEBVTT\n\nhello auto only\n",
                encoding="utf-8",
            )

    monkeypatch.setattr(adapter, "yt_dlp", SimpleNamespace(YoutubeDL=FakeYDL))
    text, kind, lang, error = fetch_subtitles_ytdlp("abc123def45", ["en"])

    assert error is None
    assert kind == "auto"
    assert lang == "en.auto"
    assert text == "hello auto only"
