#!/usr/bin/env python3
"""Validate runtime/artifacts/prediction-metrics.json shape and invariants."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_METRICS = REPO_ROOT / "runtime" / "artifacts" / "prediction-metrics.json"


def validate_metrics(payload: dict) -> list[str]:
    issues: list[str] = []
    if "_meta" not in payload:
        issues.append("missing top-level `_meta`")
    if "voices" not in payload:
        issues.append("missing top-level `voices`")
        return issues

    voices = payload.get("voices")
    if not isinstance(voices, dict):
        issues.append("`voices` must be an object")
        return issues

    for speaker, bucket in voices.items():
        label = f"voices.{speaker}"
        if not isinstance(bucket, dict):
            issues.append(f"{label}: must be an object")
            continue
        for field in ("total", "resolved", "scorable", "correct", "incorrect", "unscored", "accuracy"):
            if field not in bucket:
                issues.append(f"{label}: missing `{field}`")
        accuracy = bucket.get("accuracy")
        if accuracy is not None:
            if not isinstance(accuracy, (int, float)) or accuracy < 0 or accuracy > 1:
                issues.append(f"{label}: accuracy must be null or between 0 and 1")
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
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"error: invalid JSON: {exc}", file=sys.stderr)
        return 1
    if not isinstance(payload, dict):
        print("error: metrics must be a JSON object", file=sys.stderr)
        return 1

    issues = validate_metrics(payload)
    if issues:
        for line in issues:
            print(line, file=sys.stderr)
        print(f"check_prediction_metrics: {len(issues)} violation(s)", file=sys.stderr)
        return 1

    print("[ok] prediction metrics valid")
    return 0


def main() -> int:
    return run_check()


if __name__ == "__main__":
    raise SystemExit(main())
