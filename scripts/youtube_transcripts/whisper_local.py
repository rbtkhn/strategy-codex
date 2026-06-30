"""Tier 3: optional whisper.cpp local binary on downloaded audio."""

from __future__ import annotations

import os
import subprocess
import tempfile
from pathlib import Path

from youtube_transcripts.ytdlp_adapter import YtDlpError, download_audio_wav

def _download_audio_wav(video_id: str, out_wav: Path) -> str | None:
    out_dir = out_wav.parent
    stem = out_wav.stem
    try:
        download_audio_wav(video_id, out_wav)
    except YtDlpError as exc:
        return str(exc)
    if out_wav.exists():
        return None
    alt = out_dir / f"{stem}.wav"
    if alt.exists():
        return None
    return "wav not found after extract (need ffmpeg in PATH)"

def run_whisper_cpp(wav_path: Path) -> tuple[str | None, str | None]:
    """
    Run whisper.cpp CLI. Env:
      WHISPER_CPP_BIN — path to main binary (default whisper-cli)
      WHISPER_CPP_MODEL — path to .bin model (required)
    """
    bin_path = (os.environ.get("WHISPER_CPP_BIN") or "whisper-cli").strip()
    model = (os.environ.get("WHISPER_CPP_MODEL") or "").strip()
    if not model:
        return None, "WHISPER_CPP_MODEL not set"
    if not wav_path.is_file():
        return None, "missing wav"
    try:
        proc = subprocess.run(
            [bin_path, "-m", model, "-f", str(wav_path), "-otxt"],
            capture_output=True,
            text=True,
            timeout=3600,
        )
    except FileNotFoundError:
        return None, f"whisper binary not found: {bin_path}"
    except subprocess.TimeoutExpired:
        return None, "whisper timeout"
    if proc.returncode != 0:
        return None, (proc.stderr or proc.stdout or "whisper failed")[:500]
    txt = wav_path.with_suffix(".txt")
    if txt.exists():
        return txt.read_text(encoding="utf-8", errors="replace").strip(), None
    return None, "whisper did not produce .txt"

def transcribe_video_whisper(video_id: str) -> tuple[str | None, str | None]:
    """Download best audio to temp WAV and run whisper.cpp; returns (text, error)."""
    with tempfile.TemporaryDirectory(prefix="whisper_") as tmp:
        wav = Path(tmp) / f"{video_id}.wav"
        err = _download_audio_wav(video_id, wav)
        if err:
            return None, err
        return run_whisper_cpp(wav)
