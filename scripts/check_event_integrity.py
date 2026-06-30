#!/usr/bin/env python3
"""Validate event registry and prediction note event_id references."""

from __future__ import annotations

import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from prediction_lib import (  # noqa: E402
    EVENT_REGISTRY_PATH,
    collect_prediction_notes,
    load_event_registry,
    parse_frontmatter_dict,
    repo_relative,
    validate_event,
    validate_prediction_fields,
)


def run_check(*, registry_path: Path | None = None) -> int:
    path = registry_path or EVENT_REGISTRY_PATH
    issues: list[str] = []

    try:
        events = load_event_registry(path)
    except (FileNotFoundError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    for event_id, event in events.items():
        issues.extend(validate_event(event_id, event))

    event_ids = set(events.keys())
    for note in collect_prediction_notes():
        if note.event_id and note.event_id not in event_ids:
            issues.append(f"{note.file}: unknown event_id `{note.event_id}`")

        text = note.path.read_text(encoding="utf-8", errors="replace")
        data = parse_frontmatter_dict(text, feature=note.file)
        issues.extend(validate_prediction_fields(data, note.file))

    if issues:
        for line in issues:
            print(line, file=sys.stderr)
        print(f"check_event_integrity: {len(issues)} violation(s)", file=sys.stderr)
        return 1

    print("[ok] event integrity valid")
    return 0


def main() -> int:
    return run_check()


if __name__ == "__main__":
    raise SystemExit(main())
