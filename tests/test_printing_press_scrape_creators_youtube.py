from __future__ import annotations

import importlib.util
import json
import shutil
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "printing_press_scrape_creators_youtube.py"
TEST_TMP = REPO / ".codex-test-temp" / "printing-press-scrape-creators"


def load_adapter():
    spec = importlib.util.spec_from_file_location("pp_scrape_creators_youtube", SCRIPT)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def sample_payload() -> dict:
    return {
        "fetched_at_utc": "2026-05-09T12:00:00Z",
        "videos": [
            {
                "platform": "youtube",
                "video_id": "abc123DEF45",
                "title": "Signal in the Noise",
                "url": "https://www.youtube.com/watch?v=abc123DEF45",
                "published_at": "2026-05-08",
                "duration_seconds": 123.0,
                "language": "en",
                "transcript": "First line.\nSecond line.",
            }
        ],
    }


def test_missing_cli_fails_with_install_guidance(monkeypatch) -> None:
    adapter = load_adapter()
    monkeypatch.delenv("SCRAPE_CREATORS_BIN", raising=False)
    monkeypatch.setattr(adapter.shutil, "which", lambda _name: None)

    try:
        adapter.run_scrape_creators_fetch("https://www.youtube.com/watch?v=abc123DEF45")
    except FileNotFoundError as exc:
        message = str(exc)
    else:
        raise AssertionError("expected missing CLI error")

    assert "printing-press install scrape-creators" in message


def test_input_json_allows_utf8_bom() -> None:
    adapter = load_adapter()
    payload_path = TEST_TMP / "bom-payload.json"
    payload_path.parent.mkdir(parents=True, exist_ok=True)
    payload_path.write_text(json.dumps(sample_payload()), encoding="utf-8-sig")

    payload = adapter.load_payload(payload_path, None)

    assert payload["videos"][0]["video_id"] == "abc123DEF45"


def test_payload_maps_to_existing_youtube_channel_layout() -> None:
    adapter = load_adapter()

    records = adapter.normalize_payload(sample_payload())
    index, manifest, transcripts = adapter.build_outputs(
        records,
        channel_slug="pilot-channel",
        channel_url="https://www.youtube.com/@Pilot/videos",
    )

    assert index["source"] == "printing-press/scrape-creators"
    assert index["videos"][0]["video_id"] == "abc123DEF45"
    assert index["videos"][0]["upload_date"] == "20260508"
    assert index["videos"][0]["transcript_file"].startswith("transcripts/")
    assert index["videos"][0]["source_tier"] == "printing_press_scrape_creators_public_youtube"
    assert manifest["videos"]["abc123DEF45"]["status"] == "ok"
    assert transcripts[0][0].startswith("transcripts/abc123DEF45_")
    assert "# source_tier: printing_press_scrape_creators_public_youtube" in transcripts[0][1]
    assert "First line." in transcripts[0][1]


def test_merge_preserves_existing_channel_rows() -> None:
    adapter = load_adapter()
    output_dir = TEST_TMP / "channel"
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)
    (output_dir / "index.json").write_text(
        json.dumps(
            {
                "input_urls": ["https://www.youtube.com/watch?v=old111"],
                "videos": [
                    {
                        "video_id": "old111",
                        "title": "Old row",
                        "url": "https://www.youtube.com/watch?v=old111",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    (output_dir / "transcript_manifest.json").write_text(
        json.dumps({"videos": {"old111": {"status": "ok"}}}),
        encoding="utf-8",
    )
    records = adapter.normalize_payload(sample_payload())
    index, manifest, _transcripts = adapter.build_outputs(
        records,
        channel_slug="pilot-channel",
        channel_url="https://www.youtube.com/@Pilot/videos",
    )

    index, manifest = adapter.merge_existing_outputs(output_dir, index, manifest)

    assert {row["video_id"] for row in index["videos"]} == {"old111", "abc123DEF45"}
    assert "old111" in manifest["videos"]
    assert "abc123DEF45" in manifest["videos"]


def test_v1_rejects_comments_and_credentials() -> None:
    adapter = load_adapter()
    comment_payload = sample_payload()
    comment_payload["videos"][0]["comments"] = [{"text": "do not ingest in v1"}]

    try:
        adapter.normalize_payload(comment_payload)
    except adapter.AdmissionError as exc:
        assert "comments" in str(exc)
    else:
        raise AssertionError("expected comments to be rejected")

    credential_payload = sample_payload()
    credential_payload["videos"][0]["cookies"] = "browser-session"
    try:
        adapter.normalize_payload(credential_payload)
    except adapter.AdmissionError as exc:
        assert "credentialed" in str(exc)
    else:
        raise AssertionError("expected credentials to be rejected")
