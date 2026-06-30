#!/usr/bin/env python3
"""Generate runtime/artifacts/prediction-registry.json from prediction notes."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = REPO_ROOT / "runtime" / "artifacts" / "prediction-registry.json"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from prediction_lib import (  # noqa: E402
    build_registry_payload,
    render_json,
)


def check_artifact(*, output_path: Path) -> int:
    if not output_path.is_file():
        print(f"error: missing {output_path.relative_to(REPO_ROOT)}", file=sys.stderr)
        return 1
    expected = render_json(build_registry_payload())
    current = output_path.read_text(encoding="utf-8")
    if current != expected:
        print(
            f"error: {output_path.relative_to(REPO_ROOT)} is out of date; "
            "run build_prediction_registry.py",
            file=sys.stderr,
        )
        return 1
    print("[ok] prediction registry artifact matches generator output")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Registry JSON output path",
    )
    ap.add_argument(
        "--check",
        action="store_true",
        help="Exit 1 if committed artifact differs from freshly computed output",
    )
    args = ap.parse_args()

    if args.check:
        return check_artifact(output_path=args.output)

    try:
        payload = build_registry_payload()
    except (FileNotFoundError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    text = render_json(payload)
    args.output.write_text(text, encoding="utf-8")
    print(f"[ok] wrote {args.output.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
