from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from youtube_transcripts.ytdlp_adapter import normalize_upload_date


def load_index_videos(index_path: Path) -> list[dict[str, Any]]:
    payload = json.loads(index_path.read_text(encoding="utf-8"))
    videos_raw = payload.get("videos") or []
    videos: list[dict[str, Any]] = []
    for raw in videos_raw:
        if not isinstance(raw, dict):
            continue
        videos.append(
            {
                "video_id": str(raw.get("video_id") or "").strip(),
                "title": str(raw.get("title") or "").strip(),
                "upload_date": normalize_upload_date(str(raw.get("upload_date") or "")) or "",
                "url": str(raw.get("url") or "").strip(),
                "transcript_file": raw.get("transcript_file"),
                "status": str(raw.get("status") or "").strip(),
                "language": raw.get("language"),
                "error": raw.get("error"),
                "duration_seconds": raw.get("duration_seconds") or raw.get("duration") or "",
            }
        )
    return videos
