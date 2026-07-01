"""Tests for build_epistemic_intelligence_core.py drift gate."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from prediction.epistemic_intelligence_core import build_eic_payload  # noqa: E402


def test_build_eic_payload_object_count() -> None:
    mvel_path = REPO / "runtime" / "artifacts" / "multivoice-extracted-dataset.json"
    if not mvel_path.is_file():
        return
    mvel = json.loads(mvel_path.read_text(encoding="utf-8"))
    bundle = build_eic_payload(mvel_dataset=mvel, semantic_scores={})
    assert bundle["object_count"] >= 1
    assert bundle["core"]["_meta"]["registry_mutation"] is False


def test_build_epistemic_intelligence_core_check() -> None:
    build = subprocess.run(
        [sys.executable, "scripts/build_epistemic_intelligence_core.py"],
        cwd=REPO,
        capture_output=True,
        text=True,
    )
    assert build.returncode == 0, build.stderr

    check = subprocess.run(
        [sys.executable, "scripts/build_epistemic_intelligence_core.py", "--check"],
        cwd=REPO,
        capture_output=True,
        text=True,
    )
    assert check.returncode == 0, check.stderr

    core = REPO / "runtime" / "artifacts" / "epistemic-intelligence-core.json"
    payload = json.loads(core.read_text(encoding="utf-8"))
    assert payload.get("interpretation") == "epistemic_intelligence_core"
