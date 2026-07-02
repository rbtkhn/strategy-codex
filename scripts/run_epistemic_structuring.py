#!/usr/bin/env python3
"""Operator entry — run epistemic structuring layer (PR3)."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
EPISTEMIC_ROOT = REPO_ROOT / "statecraft" / "epistemic"

if str(EPISTEMIC_ROOT) not in sys.path:
    sys.path.insert(0, str(EPISTEMIC_ROOT))

from pipeline.run_pipeline import run_structuring_layer  # noqa: E402
from structuring.normalize import DEFAULT_REGISTRY, DEFAULT_STRUCTURED_OUT  # noqa: E402

def main() -> int:
    structured = run_structuring_layer(
        registry_path=DEFAULT_REGISTRY,
        out_path=DEFAULT_STRUCTURED_OUT,
        write=True,
    )
    print(f"structured_predictions: {len(structured)} -> {DEFAULT_STRUCTURED_OUT}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
