#!/usr/bin/env python3
"""Backfill Dialogue Works YouTube transcripts into strategy-notebook raw-input/.

This wrapper fetches the public Dialogue Works YouTube channel into a temporary
transcript corpus, then mirrors the transcript text into raw-input markdown with
Dialogue Works frontmatter. Host-side capture is the primary goal; guest lanes
can still be mirrored separately when needed.
WORK only; not Record.
"""

from __future__ import annotations

import sys
from pathlib import Path

from backfill_youtube_channel_raw_input import main as youtube_main

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CHANNEL_URL = "https://www.youtube.com/@dialogueworks01/videos"
DEFAULT_THREAD = "nima"
DEFAULT_SHOW = "Dialogue Works"
DEFAULT_HOST = "Nima Alkhorshid"


def main() -> int:
    return youtube_main(
        [
            "--channel-url",
            DEFAULT_CHANNEL_URL,
            "--channel-slug",
            "dialogue-works",
            "--show",
            DEFAULT_SHOW,
            "--host",
            DEFAULT_HOST,
            "--thread",
            DEFAULT_THREAD,
            "--file-prefix",
            "transcript-dialogue-works",
            "--source-note",
            "Automated YouTube transcript fetch for Dialogue Works host capture.",
            "--work-dir",
            str(REPO_ROOT / ".codex-tmp" / "nima-dialogue-works"),
            "--notebook-root",
            str(REPO_ROOT / "docs/skill-work/work-strategy/strategy-notebook"),
            "--limit",
            "20",
            "--sleep",
            "0.25",
            "--infer-guest",
            *sys.argv[1:],
        ]
    )


if __name__ == "__main__":
    raise SystemExit(main())
