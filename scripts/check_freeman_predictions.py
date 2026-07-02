#!/usr/bin/env python3
"""Validate Freeman predictions — compatibility wrapper for check_voice_predictions.py."""

from __future__ import annotations

import sys

from check_voice_predictions import main

def _ensure_speaker() -> None:
    if "--speaker" not in sys.argv:
        sys.argv.extend(["--speaker", "freeman"])

if __name__ == "__main__":
    _ensure_speaker()
    raise SystemExit(main())
