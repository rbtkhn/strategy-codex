#!/usr/bin/env python3
"""Validate runtime/artifacts/prediction-timeline.json shape."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PATH = REPO_ROOT / "runtime" / "artifacts" / "prediction-timeline.json"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from prediction_lib import SHIFT_TYPES  # noqa: E402

SHIFT_REQUIRED = ("type", "from", "to", "from_date", "to_date", "from_file", "to_file")


def validate_timeline(payload: dict) -> list[str]:
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
        for section in ("entries", "latest_by_speaker", "shifts"):
            if section not in block:
                issues.append(f"{label}: missing `{section}`")

        entries = block.get("entries")
        if isinstance(entries, list):
            dates = [str(row.get("date") or "") for row in entries if isinstance(row, dict)]
            if dates != sorted(dates):
                issues.append(f"{label}.entries: must be sorted by date")
        else:
            issues.append(f"{label}.entries: must be a list")

        shifts = block.get("shifts")
        if isinstance(shifts, dict):
            for speaker, speaker_shifts in shifts.items():
                if not isinstance(speaker_shifts, list):
                    issues.append(f"{label}.shifts.{speaker}: must be a list")
                    continue
                for idx, shift in enumerate(speaker_shifts):
                    shift_label = f"{label}.shifts.{speaker}[{idx}]"
                    if not isinstance(shift, dict):
                        issues.append(f"{shift_label}: must be an object")
                        continue
                    for field in SHIFT_REQUIRED:
                        if field not in shift:
                            issues.append(f"{shift_label}: missing `{field}`")
                    shift_type = shift.get("type")
                    if shift_type not in SHIFT_TYPES:
                        issues.append(f"{shift_label}: invalid type `{shift_type}`")

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
        print("error: timeline payload must be a JSON object", file=sys.stderr)
        return 1

    issues = validate_timeline(payload)
    if issues:
        for line in issues:
            print(line, file=sys.stderr)
        print(f"check_prediction_timeline: {len(issues)} violation(s)", file=sys.stderr)
        return 1

    print("[ok] prediction timeline valid")
    return 0


def main() -> int:
    return run_check()


if __name__ == "__main__":
    raise SystemExit(main())
