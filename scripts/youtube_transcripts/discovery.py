from __future__ import annotations

import re
from datetime import date
from pathlib import Path

from youtube_transcripts.ytdlp_adapter import YtDlpError, list_videos_flat

def _normalize_url_line(line: str) -> str | None:
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    return line

def load_inputs_from_file(path: Path) -> list[str]:
    """Load channel URLs, playlist URLs, or watch URLs (one per line)."""
    out: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        u = _normalize_url_line(raw)
        if u:
            out.append(u)
    return out

def extract_video_id(text: str) -> str | None:
    """Best-effort 11-char video id from URL or raw id."""
    t = text.strip()
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", t):
        return t
    m = re.search(r"(?:v=|/embed/|youtu\.be/)([A-Za-z0-9_-]{11})", t)
    return m.group(1) if m else None

def list_videos(
    url_or_id: str,
    *,
    limit: int | None,
    playlist_items: str | None = None,
    stop_before_date: date | None = None,
    max_attempts: int = 4,
) -> list[dict[str, str]]:
    """
    List videos using yt-dlp flat extraction (channel, playlist, or single video URL).
    Returns dicts: id, title, upload_date, duration (string), url.
    """
    url = url_or_id.strip()
    vid = extract_video_id(url)
    if vid and "youtube.com" not in url and "youtu.be" not in url and "playlist" not in url:
        url = f"https://www.youtube.com/watch?v={vid}"
    try:
        return list_videos_flat(
            url,
            limit=limit,
            playlist_items=playlist_items,
            stop_before_date=stop_before_date,
            max_attempts=max_attempts,
        )
    except YtDlpError as exc:
        if "not installed" in str(exc):
            raise RuntimeError("Missing dependency: pip install yt-dlp") from exc
        raise
