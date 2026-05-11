#!/usr/bin/env python3
"""
Append one JSON line per video per run to a .jsonl file for longitudinal tracking
(views, likes, comment counts, channel subscribers). Uses yt-dlp metadata only;
does not download video or full comment threads.

  python3 scripts/snapshot_youtube_video_metrics.py --video-id lkKrZq4YdqY \\
    --jsonl codex/predictive-history/influence-tracking/snapshots/video-metrics.jsonl
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from youtube_transcripts.ytdlp_adapter import YtDlpError, fetch_video_metadata_subprocess, get_version

REPO_ROOT = Path(__file__).resolve().parent.parent


def _watch_url(video_id: str) -> str:
    vid = video_id.strip()
    if not vid or len(vid) < 6:
        raise ValueError(f"bad video_id: {video_id!r}")
    return f"https://www.youtube.com/watch?v={vid}"


def _fetch_metadata(url: str) -> dict:
    try:
        return fetch_video_metadata_subprocess(url, mode="binary")
    except YtDlpError as exc:
        raise RuntimeError(str(exc)) from exc


def _snapshot_record(d: dict, *, tool_version: str) -> dict:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    vid = d.get("id") or ""
    return {
        "captured_at_utc": ts,
        "video_id": vid,
        "url": d.get("webpage_url") or _watch_url(vid),
        "title": d.get("title"),
        "channel": d.get("channel"),
        "channel_id": d.get("channel_id"),
        "channel_follower_count": d.get("channel_follower_count"),
        "view_count": d.get("view_count"),
        "like_count": d.get("like_count"),
        "comment_count": d.get("comment_count"),
        "upload_date": d.get("upload_date"),
        "duration": d.get("duration"),
        "tool": "yt-dlp",
        "tool_version": tool_version,
    }


def _yt_dlp_version() -> str:
    return get_version(mode="binary")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Append YouTube public metrics to JSONL.")
    p.add_argument(
        "--video-id",
        nargs="+",
        required=True,
        help="One or more 11-character YouTube video IDs",
    )
    p.add_argument(
        "--jsonl",
        required=True,
        type=Path,
        help="Append-only JSONL path (e.g. influence-tracking/snapshots/video-metrics.jsonl)",
    )
    args = p.parse_args(argv)
    out = args.jsonl
    if not out.is_absolute():
        out = REPO_ROOT / out
    out.parent.mkdir(parents=True, exist_ok=True)
    ver = _yt_dlp_version()

    for raw_id in args.video_id:
        vid = raw_id.strip()
        url = _watch_url(vid)
        try:
            meta = _fetch_metadata(url)
        except Exception as e:
            print(f"ERROR {vid}: {e}", file=sys.stderr)
            return 1
        rec = _snapshot_record(meta, tool_version=ver)
        with open(out, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=True) + "\n")
        print(json.dumps(rec, indent=2, ensure_ascii=True))
    print(f"Appended to {out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
