#!/usr/bin/env python3
"""Validate runtime/artifacts/prediction-metrics.json shape and invariants."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_METRICS = REPO_ROOT / "runtime" / "artifacts" / "prediction-metrics.json"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from validate_all_schemas import load_registry, validate_entry  # noqa: E402

def validate_metrics_arithmetic(payload: dict) -> list[str]:
    issues: list[str] = []
    voices = payload.get("voices")
    if not isinstance(voices, dict):
        return issues
    for speaker, bucket in voices.items():
        if not isinstance(bucket, dict):
            continue
        label = f"voices.{speaker}"
        correct = int(bucket.get("correct") or 0)
        incorrect = int(bucket.get("incorrect") or 0)
        scorable = int(bucket.get("scorable") or 0)
        resolved = int(bucket.get("resolved") or 0)
        if correct + incorrect != scorable:
            issues.append(f"{label}: correct + incorrect must equal scorable")
        if resolved < scorable:
            issues.append(f"{label}: resolved must be >= scorable")
    return issues

def run_check(*, metrics_path: Path | None = None) -> int:
    path = metrics_path or DEFAULT_METRICS
    if not path.is_file():
        print(f"error: missing {path.relative_to(REPO_ROOT)}", file=sys.stderr)
        return 1

    manifest = load_registry()
    entry = dict(manifest["schemas"]["prediction_metrics"])
    entry["applies_to"] = str(path.relative_to(REPO_ROOT)).replace("\\", "/")
    lines, failed = validate_entry("prediction_metrics", entry)
    for line in lines:
        print(line)

    import json

    payload = json.loads(path.read_text(encoding="utf-8"))
    arithmetic = validate_metrics_arithmetic(payload)
    if arithmetic:
        failed = True
        for line in arithmetic:
            print(line, file=sys.stderr)

    if failed:
        print("check_prediction_metrics: validation failed", file=sys.stderr)
        return 1
    print("[ok] prediction metrics valid")
    return 0

def main() -> int:
    return run_check()

if __name__ == "__main__":
    raise SystemExit(main())
