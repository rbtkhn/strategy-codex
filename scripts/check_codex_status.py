#!/usr/bin/env python3
"""Legacy wrapper — prefer check_continuity_status.py."""

from __future__ import annotations

import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from check_continuity_status import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
