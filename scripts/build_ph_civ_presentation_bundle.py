#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "src"))

from integrations.presentations.common import write_bundle
from integrations.presentations.ph_civ_adapter import build_ph_civ_bundle, build_ph_mus_packet_bundle


def main() -> int:
    ap = argparse.ArgumentParser(description="Build a PH-CIV presentation bundle from explicit public packets.")
    ap.add_argument("--intent", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--audience", required=True)
    ap.add_argument("--subsurface", default="ph-civ", choices=["ph-civ", "ph-apo", "ph-mus"])
    ap.add_argument("--source-path", action="append", default=[])
    ap.add_argument("--packet-json", type=Path)
    ap.add_argument("--public-id", action="append", default=[])
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()

    out = args.output if args.output.is_absolute() else (REPO_ROOT / args.output)
    if args.subsurface == "ph-mus":
        if not args.packet_json:
            raise SystemExit("--packet-json is required for ph-mus bundles")
        packet_path = args.packet_json if args.packet_json.is_absolute() else (REPO_ROOT / args.packet_json)
        bundle = build_ph_mus_packet_bundle(
            intent=args.intent,
            title=args.title,
            audience=args.audience,
            packet_path=packet_path,
        )
    else:
        if not args.source_path:
            raise SystemExit("--source-path is required for ph-civ and ph-apo bundles")
        paths = [Path(p) if Path(p).is_absolute() else (REPO_ROOT / p) for p in args.source_path]
        bundle = build_ph_civ_bundle(
            intent=args.intent,
            title=args.title,
            audience=args.audience,
            source_paths=paths,
            public_ids=args.public_id,
            subsurface=args.subsurface,
        )
    write_bundle(bundle, out)
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
