#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
from repo_io import SRC_DIR
sys.path.insert(0, str(SRC_DIR))

from integrations.presentations.civ_emp_adapter import build_civ_emp_bundle, build_civ_emp_packet_bundle
from integrations.presentations.common import write_bundle

def main() -> int:
    ap = argparse.ArgumentParser(
        description="Build a civ-emp family deck bundle for ce-civ, ce-emp, or ce-mus."
    )
    ap.add_argument("--intent", required=True, help="Deck job such as briefing, summary, roadmap, or comparison.")
    ap.add_argument("--title", required=True, help="Deck title shown to the operator or audience.")
    ap.add_argument("--audience", required=True, help="Audience label used to frame the deck.")
    ap.add_argument(
        "--subsurface",
        default="ce-emp",
        choices=["ce-civ", "ce-emp", "ce-mus"],
        help="CIV-EMP lane to render: civilization, empire/statecraft, or museum/exhibit.",
    )
    ap.add_argument(
        "--source-path",
        action="append",
        default=[],
        help="WORK-safe source markdown path. Use for ce-civ or ce-emp when building from repo sources.",
    )
    ap.add_argument(
        "--packet-json",
        type=Path,
        help="Prepared packet JSON. Use for ce-mus and optional packet-driven ce-civ/ce-emp flows.",
    )
    ap.add_argument("--output", type=Path, required=True, help="Bundle JSON path to write.")
    args = ap.parse_args()

    out = args.output if args.output.is_absolute() else (REPO_ROOT / args.output)
    if args.subsurface == "ce-mus" and not args.packet_json:
        raise SystemExit("--packet-json is required for ce-mus bundles")
    if args.packet_json:
        packet_path = args.packet_json if args.packet_json.is_absolute() else (REPO_ROOT / args.packet_json)
        bundle = build_civ_emp_packet_bundle(
            intent=args.intent,
            title=args.title,
            audience=args.audience,
            subsurface=args.subsurface,
            packet_path=packet_path,
        )
    else:
        paths = [Path(p) if Path(p).is_absolute() else (REPO_ROOT / p) for p in args.source_path]
        bundle = build_civ_emp_bundle(
            intent=args.intent,
            title=args.title,
            audience=args.audience,
            subsurface=args.subsurface,
            source_paths=paths or None,
        )
    write_bundle(bundle, out)
    print(out)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
