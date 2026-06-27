#!/usr/bin/env python3
"""Deprecated: use build_voice_routing_queue.py."""

from __future__ import annotations

import sys

from build_voice_routing_queue import *  # noqa: F403
from build_voice_routing_queue import main

if __name__ == "__main__":
    print(
        "warning: build_speaker_routing_queue.py is deprecated; use build_voice_routing_queue.py",
        file=sys.stderr,
    )
    raise SystemExit(main())
