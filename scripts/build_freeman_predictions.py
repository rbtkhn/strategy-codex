#!/usr/bin/env python3
"""Build Freeman prediction record — compatibility wrapper for build_voice_predictions.py."""

from __future__ import annotations

import sys

from build_voice_predictions import main

def _ensure_speaker() -> None:
    if "--speaker" not in sys.argv:
        sys.argv.extend(["--speaker", "freeman"])

if __name__ == "__main__":
    _ensure_speaker()
    raise SystemExit(main())
