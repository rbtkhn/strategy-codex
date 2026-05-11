from __future__ import annotations

import json
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import snapshot_youtube_video_metrics as metrics  # noqa: E402


def test_fetch_metadata_routes_through_adapter(monkeypatch) -> None:
    calls: dict[str, object] = {}

    def fake_fetch(url: str, *, mode: str = "binary") -> dict:
        calls["url"] = url
        calls["mode"] = mode
        return {"id": "abc123def45"}

    monkeypatch.setattr(metrics, "fetch_video_metadata_subprocess", fake_fetch)
    data = metrics._fetch_metadata("https://www.youtube.com/watch?v=abc123def45")

    assert calls == {
        "url": "https://www.youtube.com/watch?v=abc123def45",
        "mode": "binary",
    }
    assert data["id"] == "abc123def45"


def test_snapshot_record_keeps_expected_json_shape() -> None:
    record = metrics._snapshot_record(
        {
            "id": "abc123def45",
            "webpage_url": "https://www.youtube.com/watch?v=abc123def45",
            "title": "Example",
            "channel": "Channel Name",
            "channel_id": "chan123",
            "channel_follower_count": 99,
            "view_count": 1000,
            "like_count": 100,
            "comment_count": 10,
            "upload_date": "20260503",
            "duration": 321,
        },
        tool_version="2026.05.01",
    )

    assert record["video_id"] == "abc123def45"
    assert record["tool"] == "yt-dlp"
    assert record["tool_version"] == "2026.05.01"
    assert record["upload_date"] == "20260503"
    assert record["duration"] == 321


def test_main_appends_jsonl_and_prints_record(tmp_path: Path, monkeypatch, capsys) -> None:
    out = tmp_path / "video-metrics.jsonl"
    monkeypatch.setattr(metrics, "_yt_dlp_version", lambda: "2026.05.01")
    monkeypatch.setattr(
        metrics,
        "_fetch_metadata",
        lambda url: {
            "id": "abc123def45",
            "webpage_url": url,
            "title": "Example",
            "channel": "Channel Name",
            "channel_id": "chan123",
            "channel_follower_count": 99,
            "view_count": 1000,
            "like_count": 100,
            "comment_count": 10,
            "upload_date": "20260503",
            "duration": 321,
        },
    )

    rc = metrics.main(["--video-id", "abc123def45", "--jsonl", str(out)])

    assert rc == 0
    payload = [json.loads(line) for line in out.read_text(encoding="utf-8").splitlines()]
    assert payload[0]["video_id"] == "abc123def45"
    assert payload[0]["tool_version"] == "2026.05.01"
    captured = capsys.readouterr()
    assert '"video_id": "abc123def45"' in captured.out
    assert f"Appended to {out}" in captured.err
