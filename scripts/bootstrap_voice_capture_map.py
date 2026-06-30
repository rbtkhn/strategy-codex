#!/usr/bin/env python3
"""Validate curated voice prediction capture map — generic --speaker entry point."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from voice_prediction_pilot import get_voice_config, validate_curated_capture_map  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--speaker",
        default="freeman",
        help="Voice slug (see voice_prediction_pilot.list_voice_speakers())",
    )
    ap.add_argument("--check", action="store_true", help="Validate curated capture map only")
    ap.add_argument("--capture-map", type=Path, default=None)
    ap.add_argument("--public-map", type=Path, default=None)
    args = ap.parse_args()

    if not args.check:
        print("error: only --check is supported; use bootstrap_<speaker>_capture_map for v1 rebuild", file=sys.stderr)
        return 2

    try:
        config = get_voice_config(args.speaker)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    issues, row_count = validate_curated_capture_map(
        config,
        capture_map_path=args.capture_map,
        public_map_path=args.public_map,
    )
    if issues:
        for line in issues:
            print(line, file=sys.stderr)
        print(
            f"bootstrap_voice_capture_map ({config.speaker}): {len(issues)} issue(s)",
            file=sys.stderr,
        )
        return 1
    print(f"[ok] {config.speaker} capture map valid ({row_count} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
