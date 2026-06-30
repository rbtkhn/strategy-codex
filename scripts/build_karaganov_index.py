#!/usr/bin/env python3
"""Parity gate for manual-curated karaganov-index.md."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_manual_voice_index_gate import gate_main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(gate_main("karaganov"))
