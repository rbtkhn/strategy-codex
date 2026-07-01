#!/usr/bin/env python3
"""Operator entry — run epistemic temporal scaffolding layer (PR5)."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
EPISTEMIC_ROOT = REPO_ROOT / "statecraft" / "epistemic"

if str(EPISTEMIC_ROOT) not in sys.path:
    sys.path.insert(0, str(EPISTEMIC_ROOT))

from pipeline.run_pipeline import run_temporal_layer  # noqa: E402
from temporal.temporal_engine import (  # noqa: E402
    DEFAULT_OBSERVATIONS_IN,
    DEFAULT_STRUCTURED_IN,
    DEFAULT_TEMPORAL_OUT,
)


def main() -> int:
    temporal_by_event, summary = run_temporal_layer(
        structured_path=DEFAULT_STRUCTURED_IN,
        observations_path=DEFAULT_OBSERVATIONS_IN,
        out_path=DEFAULT_TEMPORAL_OUT,
        write=True,
    )
    print(
        f"temporal: events={len(temporal_by_event)} "
        f"ordering_confidence_avg={summary['ordering_confidence_avg']} "
        f"-> {DEFAULT_TEMPORAL_OUT}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
