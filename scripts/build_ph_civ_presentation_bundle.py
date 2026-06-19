#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
from repo_io import SRC_DIR
sys.path.insert(0, str(SRC_DIR))

from integrations.presentations.common import write_bundle
from integrations.presentations.ph_civ_adapter import build_ph_civ_bundle, build_ph_mus_packet_bundle


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Build a ph-civ family deck bundle for ph-civ, ph-apo, or ph-mus."
    )
    ap.add_argument("--intent", required=True, help="Deck job such as lesson, summary, or comparison.")
    ap.add_argument("--title", required=True, help="Deck title shown to readers or operators.")
    ap.add_argument("--audience", required=True, help="Audience label used to frame the deck.")
    ap.add_argument(
        "--subsurface",
        default="ph-civ",
        choices=["ph-civ", "ph-apo", "ph-mus"],
        help="PH lane to render: civilization, apocalypse, or museum/exhibit.",
    )
    ap.add_argument(
        "--source-path",
        action="append",
        default=[],
        help="Explicit public packet JSON path. Use for ph-civ or ph-apo packet-driven builds.",
    )
    ap.add_argument(
        "--packet-json",
        type=Path,
        help="Prepared museum packet JSON. Required for ph-mus.",
    )
    ap.add_argument(
        "--public-id",
        action="append",
        default=[],
        help="Public source id to echo in labels when building ph-civ or ph-apo decks.",
    )
    ap.add_argument("--output", type=Path, required=True, help="Bundle JSON path to write.")
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
            raise SystemExit("--source-path is required for ph-civ and ph-apo public packet bundles")
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
