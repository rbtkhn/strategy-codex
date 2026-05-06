from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any


def normalize_upload_date(raw: str | None) -> str | None:
    s = (raw or "").strip()
    if not s:
        return None
    if re.fullmatch(r"\d{8}", s):
        return f"{s[:4]}-{s[4:6]}-{s[6:8]}"
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        return s
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00")).date().isoformat()
    except ValueError:
        return None


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
