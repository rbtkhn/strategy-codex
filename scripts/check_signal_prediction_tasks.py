#!/usr/bin/env python3
"""Validate signal-prediction-tasks.json shape — advisory only (never blocks)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PATH = REPO_ROOT / "runtime" / "artifacts" / "signal-prediction-tasks.json"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from build_signal_prediction_tasks import check_artifact as check_fresh  # noqa: E402
from prediction.signal_prediction_tasks import (  # noqa: E402
    LOW_N_ADVISORY_THRESHOLD,
    SIGNAL_VECTOR_DIMENSIONS,
    TASKS,
)


def validate_payload(payload: dict) -> list[str]:
    issues: list[str] = []
    if payload.get("interpretation") != "supervised_task_space":
        issues.append("top-level interpretation must be supervised_task_space")

    meta = payload.get("_meta")
    if not isinstance(meta, dict):
        issues.append("missing _meta object")
    else:
        if meta.get("task_source") != "heuristic_v1":
            issues.append("_meta.task_source must be heuristic_v1")
        dims = meta.get("signal_vector_dimensions")
        if dims != list(SIGNAL_VECTOR_DIMENSIONS):
            issues.append("_meta.signal_vector_dimensions mismatch")

    tasks = payload.get("tasks")
    if tasks != list(TASKS):
        issues.append("tasks list must match regime_shift, delta, convergence")

    examples = payload.get("examples")
    if not isinstance(examples, list):
        issues.append("examples must be a list")
        return issues

    for idx, example in enumerate(examples):
        if not isinstance(example, dict):
            issues.append(f"examples[{idx}]: must be an object")
            continue
        if example.get("interpretation") != "supervised_task_example":
            issues.append(f"examples[{idx}]: interpretation must be supervised_task_example")
        for field in ("event_id", "task", "anchor_date", "time_offset", "signal_vector", "future_outcome"):
            if field not in example:
                issues.append(f"examples[{idx}]: missing {field}")
        vec = example.get("signal_vector")
        if isinstance(vec, list) and len(vec) != len(SIGNAL_VECTOR_DIMENSIONS):
            issues.append(f"examples[{idx}]: signal_vector must have {len(SIGNAL_VECTOR_DIMENSIONS)} dims")
        if example.get("task") not in TASKS:
            issues.append(f"examples[{idx}]: invalid task {example.get('task')!r}")

    return issues


def run_check(*, path: Path | None = None, advisory: bool = False) -> int:
    target = path or DEFAULT_PATH
    if not target.is_file():
        msg = f"missing {target.relative_to(REPO_ROOT)}"
        if advisory:
            print(f"WARN: {msg}", file=sys.stderr)
            return 0
        print(f"error: {msg}", file=sys.stderr)
        return 1

    payload = json.loads(target.read_text(encoding="utf-8"))
    issues = validate_payload(payload)
    if issues:
        for line in issues:
            if advisory:
                print(f"WARN: {line}", file=sys.stderr)
            else:
                print(line, file=sys.stderr)
        return 0 if advisory else 1

    scope = (payload.get("_meta") or {}).get("task_scope") or {}
    if isinstance(scope, dict) and scope.get("low_n_advisory"):
        count = scope.get("example_count", 0)
        print(
            f"WARN: low task example count ({count} < {LOW_N_ADVISORY_THRESHOLD}); advisory only",
            file=sys.stderr,
        )

    fresh_rc = check_fresh(output_path=target)
    if fresh_rc != 0:
        msg = f"{target.relative_to(REPO_ROOT)} is out of date; run build_signal_prediction_tasks.py"
        if advisory:
            print(f"WARN: {msg}", file=sys.stderr)
            return 0
        print(f"error: {msg}", file=sys.stderr)
        return 1

    print("[ok] signal prediction tasks valid (advisory)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--path", type=Path, default=DEFAULT_PATH)
    ap.add_argument(
        "--advisory",
        action="store_true",
        help="Never block exit code; emit WARN lines only (check_repo_health)",
    )
    args = ap.parse_args()
    return run_check(path=args.path, advisory=args.advisory)


if __name__ == "__main__":
    raise SystemExit(main())
