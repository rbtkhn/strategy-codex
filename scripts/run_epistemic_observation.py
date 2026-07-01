#!/usr/bin/env python3
"""Operator entry — run epistemic observation layer (PR2)."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
EPISTEMIC_ROOT = REPO_ROOT / "statecraft" / "epistemic"

if str(EPISTEMIC_ROOT) not in sys.path:
    sys.path.insert(0, str(EPISTEMIC_ROOT))

from pipeline.run_pipeline import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
