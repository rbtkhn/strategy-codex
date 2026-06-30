#!/usr/bin/env python3
"""Validate runtime/artifacts/prediction-disagreement.json shape."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PATH = REPO_ROOT / "runtime" / "artifacts" / "prediction-disagreement.json"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from prediction_lib import STANCE_KEYS  # noqa: E402

def _score_in_range(value: object, label: str) -> list[str]:
    issues: list[str] = []
    if not isinstance(value, (int, float)):
        issues.append(f"{label}: score must be numeric")
        return issues
    if value < 0 or value > 1:
        issues.append(f"{label}: score must be between 0 and 1")
    return issues

def validate_disagreement(payload: dict) -> list[str]:
    issues: list[str] = []
    if "_meta" not in payload:
        issues.append("missing top-level `_meta`")
    if "events" not in payload:
        issues.append("missing top-level `events`")
        return issues

    events = payload.get("events")
    if not isinstance(events, dict):
        issues.append("`events` must be an object")
        return issues

    for event_id, block in events.items():
        label = f"events.{event_id}"
        if not isinstance(block, dict):
            issues.append(f"{label}: must be an object")
            continue
        for mode in ("prediction_level", "latest_voice_level"):
            if mode not in block:
                issues.append(f"{label}: missing `{mode}`")
                continue
            section = block[mode]
            if not isinstance(section, dict):
                issues.append(f"{label}.{mode}: must be an object")
                continue
            dist = section.get("distribution")
            if not isinstance(dist, dict):
                issues.append(f"{label}.{mode}: missing distribution object")
            else:
                for key in STANCE_KEYS:
                    if key not in dist:
                        issues.append(f"{label}.{mode}.distribution: missing `{key}`")
            issues.extend(_score_in_range(section.get("disagreement_score_raw"), f"{label}.{mode}.raw"))
            issues.extend(
                _score_in_range(section.get("disagreement_score_normalized"), f"{label}.{mode}.normalized")
            )

    return issues

def run_check(*, path: Path | None = None) -> int:
    target = path or DEFAULT_PATH
    if not target.is_file():
        print(f"error: missing {target.relative_to(REPO_ROOT)}", file=sys.stderr)
        return 1
    try:
        payload = json.loads(target.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"error: invalid JSON: {exc}", file=sys.stderr)
        return 1
    if not isinstance(payload, dict):
        print("error: disagreement payload must be a JSON object", file=sys.stderr)
        return 1

    issues = validate_disagreement(payload)
    if issues:
        for line in issues:
            print(line, file=sys.stderr)
        print(f"check_prediction_disagreement: {len(issues)} violation(s)", file=sys.stderr)
        return 1

    print("[ok] prediction disagreement valid")
    return 0

def main() -> int:
    return run_check()

if __name__ == "__main__":
    raise SystemExit(main())
