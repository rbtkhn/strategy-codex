#!/usr/bin/env python3
"""Validate event registry and prediction note event_id references."""

from __future__ import annotations

import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from schema_invariants import run_prediction_invariants  # noqa: E402
from validate_all_schemas import run_validation  # noqa: E402

def run_check(*, registry_path: Path | None = None) -> int:
    del registry_path  # compatibility; path fixed in registry manifest
    schema_rc = run_validation(scope="prediction", include_invariants=False)
    if schema_rc != 0:
        return schema_rc
    issues = run_prediction_invariants()
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
