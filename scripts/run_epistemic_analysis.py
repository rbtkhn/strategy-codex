#!/usr/bin/env python3
"""Operator entry — run epistemic analysis layer (PR4)."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
EPISTEMIC_ROOT = REPO_ROOT / "statecraft" / "epistemic"

if str(EPISTEMIC_ROOT) not in sys.path:
    sys.path.insert(0, str(EPISTEMIC_ROOT))

from analysis.engine import DEFAULT_ANALYSIS_OUT, DEFAULT_STRUCTURED_IN  # noqa: E402
from pipeline.run_pipeline import run_analysis_layer  # noqa: E402

def main() -> int:
    analysis_by_event, summary = run_analysis_layer(
        structured_path=DEFAULT_STRUCTURED_IN,
        out_path=DEFAULT_ANALYSIS_OUT,
        write=True,
    )
    print(
        f"analysis: events={len(analysis_by_event)} "
        f"divergence_events={len(summary['cross_voice_divergence'])} -> {DEFAULT_ANALYSIS_OUT}"
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
