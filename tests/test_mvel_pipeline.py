"""Minimal MVEL pipeline smoke test."""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from prediction.run_multivoice_extraction import run_mvel  # noqa: E402


def test_mvel_pipeline() -> None:
    result = run_mvel(semantic_scores={}, disagreement={})
    assert result["status"] == "ok"
