"""Per-video metadata via yt-dlp full extract; optional YouTube Data API v3."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request

from youtube_transcripts.ytdlp_adapter import (
    caption_language_fields,
    fetch_video_metadata_import_with_auth,
    normalize_duration_seconds,
    normalize_title,
)


def fetch_metadata_ytdlp(
    video_id: str,
    *,
    max_attempts: int = 4,
    cookies: str | None = None,
    cookies_from_browser: str | None = None,
) -> dict[str, object]:
    """Full extract_info for one video (not flat)."""
    try:
        return fetch_video_metadata_import_with_auth(
            video_id,
            max_attempts=max_attempts,
            cookies=cookies,
            cookies_from_browser=cookies_from_browser,
        )
    except Exception:
        return {}


def ytdlp_to_record(info: dict[str, object]) -> dict[str, object]:
    """Normalize yt-dlp info dict for manifest."""
    captions = caption_language_fields(info)
    return {
        "duration_seconds": normalize_duration_seconds(info.get("duration")),
        "upload_date": (info.get("upload_date") or "") or None,
        "title": normalize_title(info.get("title")) or None,
        "channel": normalize_title(info.get("channel") or info.get("uploader")) or None,
        "was_live": bool(info.get("was_live") or info.get("is_live")),
        "availability": (info.get("availability") or "") or None,
        "metadata_source": "yt-dlp",
        "caption_manual_langs": captions["caption_manual_langs"],
        "caption_auto_langs": captions["caption_auto_langs"],
    }


def fetch_metadata_youtube_api(video_id: str) -> dict[str, object] | None:
    """Optional snippet + contentDetails; requires GOOGLE_API_KEY."""
    key = (os.environ.get("GOOGLE_API_KEY") or os.environ.get("YOUTUBE_DATA_API_KEY") or "").strip()
    if not key:
        return None
    q = urllib.parse.urlencode(
        {
            "part": "snippet,contentDetails",
            "id": video_id,
            "key": key,
        }
    )
    url = f"https://www.googleapis.com/youtube/v3/videos?{q}"
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            raw = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return None
    items = raw.get("items") or []
    if not items:
        return None
    it = items[0]
    sn = it.get("snippet") or {}
    cd = it.get("contentDetails") or {}
    iso_dur = cd.get("duration") or ""
    return {
        "published_at": sn.get("publishedAt"),
        "title_api": sn.get("title"),
        "duration_iso8601": iso_dur,
        "metadata_source_api": "youtube_data_v3",
    }
