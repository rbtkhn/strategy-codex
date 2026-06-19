#!/usr/bin/env python3
"""Repo-local wrapper for the public Predictive History intake command."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = SRC_DIR
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))
from repo_io import SRC_DIR

from grace_mar.predictive_history import main


if __name__ == "__main__":
    raise SystemExit(main())
