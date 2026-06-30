#!/usr/bin/env python3
"""Validate runtime/artifacts/prediction-registry.json shape and references."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REGISTRY = REPO_ROOT / "runtime" / "artifacts" / "prediction-registry.json"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from prediction_lib import (  # noqa: E402
    REGISTRY_PREDICTION_FIELDS,
    STANCES,
    load_event_registry,
)


def validate_registry(payload: dict) -> list[str]:
    issues: list[str] = []
    if "_meta" not in payload:
        issues.append("missing top-level `_meta`")
    if "predictions" not in payload:
        issues.append("missing top-level `predictions`")
        return issues

    predictions = payload.get("predictions")
    if not isinstance(predictions, list):
        issues.append("`predictions` must be a list")
        return issues

    try:
        events = load_event_registry()
    except (FileNotFoundError, ValueError) as exc:
        issues.append(str(exc))
        events = {}

    for idx, row in enumerate(predictions):
        label = f"predictions[{idx}]"
        if not isinstance(row, dict):
            issues.append(f"{label}: must be an object")
            continue
        for field in REGISTRY_PREDICTION_FIELDS:
            if field not in row:
                issues.append(f"{label}: missing `{field}`")
        stance = str(row.get("stance") or "")
        if stance and stance not in STANCES:
            issues.append(f"{label}: invalid stance `{stance}`")
        event_id = str(row.get("event_id") or "")
        if event_id and event_id not in events:
            issues.append(f"{label}: unknown event_id `{event_id}`")

    return issues


def run_check(*, registry_path: Path | None = None) -> int:
    path = registry_path or DEFAULT_REGISTRY
    if not path.is_file():
        print(f"error: missing {path.relative_to(REPO_ROOT)}", file=sys.stderr)
        return 1
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"error: invalid JSON in {path.relative_to(REPO_ROOT)}: {exc}", file=sys.stderr)
        return 1
    if not isinstance(payload, dict):
        print("error: registry must be a JSON object", file=sys.stderr)
        return 1

    issues = validate_registry(payload)
    if issues:
        for line in issues:
            print(line, file=sys.stderr)
        print(f"check_prediction_registry: {len(issues)} violation(s)", file=sys.stderr)
        return 1

    print("[ok] prediction registry valid")
    return 0


def main() -> int:
    return run_check()


if __name__ == "__main__":
    raise SystemExit(main())
