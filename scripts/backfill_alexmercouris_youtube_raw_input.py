#!/usr/bin/env python3
"""Backfill Alex Mercouris YouTube channel listings into raw-input/.

"""

from __future__ import annotations

import sys
from pathlib import Path

from backfill_youtube_channel_raw_input import main as youtube_main

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CHANNEL_URL = "https://www.youtube.com/@AlexMercouris/videos"
DEFAULT_SHOW = "Alex Mercouris"
DEFAULT_HOST = "Alexander Mercouris"

def main() -> int:
    return youtube_main(
        [
            "--channel-url",
            DEFAULT_CHANNEL_URL,
            "--channel-slug",
            "alex-mercouris",
            "--show",
            DEFAULT_SHOW,
            "--host",
            DEFAULT_HOST,
            "--thread",
            "mercouris",
            "--file-prefix",
            "youtube-alex-mercouris",
            "--source-note",
            "Automated YouTube index mirror for Alex Mercouris hub capture.",
            "--work-dir",
            str(REPO_ROOT / ".codex-tmp" / "youtube-alex-mercouris-index"),
            "--notebook-root",
            str(REPO_ROOT / "docs/skill-work/work-strategy/strategy-notebook"),
            "--limit",
            "500",
            "--sleep",
            "0.25",
            "--stop-before-date",
            "2025-01-01",
            "--index-only",
            "--infer-guest",
            *sys.argv[1:],
        ]
    )

if __name__ == "__main__":
    raise SystemExit(main())
