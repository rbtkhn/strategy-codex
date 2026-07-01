#!/usr/bin/env python3
"""Phase 3 prediction pipeline orchestrator."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

STEPS: list[tuple[str, list[str]]] = [
    ("semantic_event_extractor", ["python3", "scripts/registry_pipeline/semantic_event_extractor.py"]),
    ("compression_engine", ["python3", "scripts/registry_pipeline/compression_engine.py", "--check"]),
    (
        "probabilistic_falsifier_engine",
        ["python3", "scripts/registry_pipeline/probabilistic_falsifier_engine.py", "--emit-review-queue"],
    ),
    ("falsifier_validator", ["python3", "scripts/registry_pipeline/falsifier_validator.py"]),
    ("registry_writer compile", ["python3", "scripts/registry_pipeline/registry_writer.py", "compile"]),
    ("build_prediction_registry", ["python3", "scripts/build_prediction_registry.py"]),
    ("build_prediction_timeline", ["python3", "scripts/build_prediction_timeline.py"]),
    ("build_prediction_disagreement", ["python3", "scripts/build_prediction_disagreement.py"]),
    ("build_prediction_semantic_scores", ["python3", "scripts/build_prediction_semantic_scores.py"]),
    ("episystem_run_pipeline", ["python3", "scripts/prediction/run_pipeline.py", "--write", "--with-plugins"]),
    (
        "check_epistemic_pipeline",
        ["python3", "scripts/check_epistemic_pipeline.py", "--advisory"],
    ),
    (
        "check_epistemic_plugins",
        ["python3", "scripts/check_epistemic_plugins.py", "--advisory"],
    ),
    (
        "check_capture_map_epistemic",
        ["python3", "scripts/check_capture_map_epistemic.py", "--advisory"],
    ),
    ("build_freeman_predictions", ["python3", "scripts/build_freeman_predictions.py"]),
    (
        "build_mercouris_predictions",
        ["python3", "scripts/build_voice_predictions.py", "--speaker", "mercouris"],
    ),
    (
        "build_macgregor_predictions",
        ["python3", "scripts/build_voice_predictions.py", "--speaker", "macgregor"],
    ),
    ("build_prediction_event_pages", ["python3", "scripts/build_prediction_event_pages.py"]),
    ("check_phase3", ["python3", "scripts/check_phase3.py", "--emit-review-queue"]),
    (
        "check_prediction_semantic_scores",
        ["python3", "scripts/check_prediction_semantic_scores.py", "--advisory"],
    ),
]


def run_step(name: str, cmd: list[str], *, stop_on_fail: bool = True) -> int:
    print(f"\n==> {name}")
    proc = subprocess.run(cmd, cwd=REPO_ROOT)
    if proc.returncode != 0 and stop_on_fail:
        print(f"[fail] {name} exited {proc.returncode}", file=sys.stderr)
        return proc.returncode
    return proc.returncode


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--from-step",
        type=int,
        default=1,
        help="1-based step index to start from",
    )
    parser.add_argument(
        "--continue-on-fail",
        action="store_true",
        help="run remaining steps even if one fails",
    )
    args = parser.parse_args()

    for idx, (name, cmd) in enumerate(STEPS, start=1):
        if idx < args.from_step:
            continue
        code = run_step(name, cmd, stop_on_fail=not args.continue_on_fail)
        if code != 0:
            return code
    print("\n[ok] prediction pipeline complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
