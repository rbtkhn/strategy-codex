"""Tier 2: yt-dlp subtitle files (manual / automatic)."""

from __future__ import annotations

import re

from youtube_transcripts.ytdlp_adapter import YtDlpError, download_subtitles

def _vtt_to_plain(vtt: str) -> str:
    lines_out: list[str] = []
    for line in vtt.splitlines():
        s = line.strip()
        if not s or s.startswith("WEBVTT") or s.startswith("NOTE") or "-->" in s:
            continue
        if re.match(r"^\d+$", s):
            continue
        s = re.sub(r"<[^>]+>", "", s)
        if s:
            lines_out.append(s)
    return "\n".join(lines_out).strip()

def fetch_subtitles_ytdlp(
    video_id: str,
    languages: list[str],
    *,
    prefer_manual: bool = True,
    cookies: str | None = None,
    cookies_from_browser: str | None = None,
) -> tuple[str | None, str | None, str | None, str | None]:
    """
    Download subtitles via yt-dlp (skip video).
    Returns (plain_text, kind_manual_or_auto, language, error).
    """
    try:
        raw_text, kind, lang_guess = download_subtitles(
            video_id,
            languages,
            prefer_manual=prefer_manual,
            cookies=cookies,
            cookies_from_browser=cookies_from_browser,
        )
    except YtDlpError as exc:
        return None, None, None, str(exc)

    text = _vtt_to_plain(raw_text)
    if not text:
        return None, kind, None, "empty vtt after parse"
    return text, kind, lang_guess, None
