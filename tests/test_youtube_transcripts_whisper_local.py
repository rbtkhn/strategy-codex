from __future__ import annotations

import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from youtube_transcripts import whisper_local  # noqa: E402


def test_download_audio_wav_routes_through_adapter(tmp_path: Path, monkeypatch) -> None:
    calls: dict[str, object] = {}
    out_wav = tmp_path / "abc123def45.wav"

    def fake_download(video_id: str, destination: Path) -> None:
        calls["video_id"] = video_id
        calls["destination"] = destination
        destination.write_bytes(b"wav")

    monkeypatch.setattr(whisper_local, "download_audio_wav", fake_download)
    err = whisper_local._download_audio_wav("abc123def45", out_wav)

    assert err is None
    assert calls == {
        "video_id": "abc123def45",
        "destination": out_wav,
    }
