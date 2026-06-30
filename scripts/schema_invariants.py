#!/usr/bin/env python3
"""Cross-object lifecycle invariants for prediction/event surfaces."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from prediction_lib import (  # noqa: E402
    EVENT_REGISTRY_PATH,
    collect_prediction_notes,
    load_event_registry,
    parse_frontmatter_dict,
    prediction_status_for_event,
    repo_relative,
    validate_event,
    validate_prediction_fields,
)

def run_prediction_invariants(
    *,
    events_path: Path | None = None,
) -> list[str]:
    """Return human-readable violation lines."""
    issues: list[str] = []
    path = events_path or EVENT_REGISTRY_PATH

    try:
        events = load_event_registry(path)
    except (FileNotFoundError, ValueError) as exc:
        return [str(exc)]

    for event_id, event in events.items():
        issues.extend(validate_event(event_id, event))

    event_ids = set(events.keys())
    for note in collect_prediction_notes():
        if note.event_id and note.event_id not in event_ids:
            issues.append(f"{note.file}: unknown event_id `{note.event_id}`")

        text = note.path.read_text(encoding="utf-8", errors="replace")
        data = parse_frontmatter_dict(text, feature=note.file)
        issues.extend(validate_prediction_fields(data, note.file, events=events))

    return issues

def run_check(*, events_path: Path | None = None) -> int:
    issues = run_prediction_invariants(events_path=events_path)
    if issues:
        for line in issues:
            print(line, file=sys.stderr)
        print(f"schema_invariants: {len(issues)} violation(s)", file=sys.stderr)
        return 1
    print("[ok] schema invariants valid")
    return 0

def main() -> int:
    return run_check()

if __name__ == "__main__":
    raise SystemExit(main())
