#!/usr/bin/env python3
"""Wrapper for the Predictive History two-phase comment rollout."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from grace_mar.predictive_history_comment_rollout import main


if __name__ == "__main__":
    raise SystemExit(main())
