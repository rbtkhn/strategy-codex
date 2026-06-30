#!/usr/bin/env python3
"""Validate runtime/artifacts/prediction-registry.json shape and references."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REGISTRY = REPO_ROOT / "runtime" / "artifacts" / "prediction-registry.json"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from validate_all_schemas import load_registry, validate_entry  # noqa: E402

def run_check(*, registry_path: Path | None = None) -> int:
    path = registry_path or DEFAULT_REGISTRY
    if not path.is_file():
        print(f"error: missing {path.relative_to(REPO_ROOT)}", file=sys.stderr)
        return 1

    manifest = load_registry()
    entry = manifest["schemas"]["prediction_registry"]
    entry = dict(entry)
    entry["applies_to"] = str(path.relative_to(REPO_ROOT)).replace("\\", "/")

    lines, failed = validate_entry("prediction_registry", entry)
    for line in lines:
        print(line)
    if failed:
        print("check_prediction_registry: validation failed", file=sys.stderr)
        return 1
    print("[ok] prediction registry valid")
    return 0

def main() -> int:
    return run_check()

if __name__ == "__main__":
    raise SystemExit(main())
