#!/usr/bin/env python3
"""Generate runtime/artifacts/prediction-metrics.json from registry and events."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REGISTRY = REPO_ROOT / "runtime" / "artifacts" / "prediction-registry.json"
DEFAULT_OUTPUT = REPO_ROOT / "runtime" / "artifacts" / "prediction-metrics.json"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from prediction_lib import (  # noqa: E402
    build_metrics_payload,
    load_event_registry,
    render_json,
)

def _load_registry(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))

def check_artifact(*, output_path: Path, registry_path: Path) -> int:
    if not output_path.is_file():
        print(f"error: missing {output_path.relative_to(REPO_ROOT)}", file=sys.stderr)
        return 1
    registry = _load_registry(registry_path)
    events = load_event_registry()
    expected = render_json(build_metrics_payload(registry, events))
    current = output_path.read_text(encoding="utf-8")
    if current != expected:
        print(
            f"error: {output_path.relative_to(REPO_ROOT)} is out of date; "
            "run build_prediction_metrics.py",
            file=sys.stderr,
        )
        return 1
    print("[ok] prediction metrics artifact matches generator output")
    return 0

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    ap.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    if args.check:
        return check_artifact(output_path=args.output, registry_path=args.registry)

    if not args.registry.is_file():
        print(f"error: missing {args.registry.relative_to(REPO_ROOT)}", file=sys.stderr)
        return 1

    registry = _load_registry(args.registry)
    events = load_event_registry()
    payload = build_metrics_payload(registry, events)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_json(payload), encoding="utf-8")
    print(f"[ok] wrote {args.output.relative_to(REPO_ROOT)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
