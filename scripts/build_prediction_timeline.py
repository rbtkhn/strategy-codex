#!/usr/bin/env python3
"""Generate runtime/artifacts/prediction-timeline.json from prediction registry."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REGISTRY = REPO_ROOT / "runtime" / "artifacts" / "prediction-registry.json"
DEFAULT_OUTPUT = REPO_ROOT / "runtime" / "artifacts" / "prediction-timeline.json"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from prediction_lib import build_timeline_payload, render_json  # noqa: E402

def check_artifact(*, output_path: Path, registry_path: Path) -> int:
    if not output_path.is_file():
        print(f"error: missing {output_path.relative_to(REPO_ROOT)}", file=sys.stderr)
        return 1
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    expected = render_json(build_timeline_payload(registry))
    current = output_path.read_text(encoding="utf-8")
    if current != expected:
        print(
            f"error: {output_path.relative_to(REPO_ROOT)} is out of date; "
            "run build_prediction_timeline.py",
            file=sys.stderr,
        )
        return 1
    print("[ok] prediction timeline artifact matches generator output")
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

    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    payload = build_timeline_payload(registry)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_json(payload), encoding="utf-8")
    print(f"[ok] wrote {args.output.relative_to(REPO_ROOT)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
