"""Minimal EIC pipeline smoke test."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from prediction.epistemic_intelligence_core import build_eic_payload  # noqa: E402


def test_eic_pipeline() -> None:
    mvel_path = REPO / "runtime" / "artifacts" / "multivoice-extracted-dataset.json"
    assert mvel_path.is_file()
    mvel = json.loads(mvel_path.read_text(encoding="utf-8"))
    bundle = build_eic_payload(mvel_dataset=mvel, semantic_scores={})
    assert bundle["object_count"] == len(bundle["core"]["objects"])
    assert bundle["events_rollup"]["interpretation"] == "epistemic_intelligence_events"
