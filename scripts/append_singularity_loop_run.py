#!/usr/bin/env python3
"""Append a Singularity loop run receipt."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUT = REPO_ROOT / "runtime" / "operator-events" / "singularity-loop-runs.jsonl"
SCHEMA_PATH = REPO_ROOT / "schemas" / "runtime" / "singularity-loop-run.schema.json"

VALID_STATUSES = {"planned", "done", "blocked", "skipped", "revised", "rejected"}

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from mcp_receipt_lib import validate_json_schema  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--loop-id", required=True)
    ap.add_argument("--status", required=True, choices=sorted(VALID_STATUSES))
    ap.add_argument("--action-card", required=True)
    ap.add_argument("--proof-artifact")
    ap.add_argument("--blocked-reason")
    ap.add_argument("--next-loop-id", action="append", default=[])
    ap.add_argument("--notes")
    ap.add_argument("--source", default="scripts/append_singularity_loop_run.py")
    ap.add_argument("--output", type=Path, default=DEFAULT_OUT)
    ap.add_argument(
        "--skip-schema",
        action="store_true",
        help="Skip JSON Schema validation before append (not recommended)",
    )
    args = ap.parse_args()

    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "loop_id": args.loop_id,
        "status": args.status,
        "action_card": args.action_card,
        "proof_artifact": args.proof_artifact,
        "blocked_reason": args.blocked_reason,
        "next_loop_ids": args.next_loop_id,
        "notes": args.notes,
        "source": args.source,
    }

    if not args.skip_schema:
        try:
            validate_json_schema(payload, SCHEMA_PATH)
        except Exception as exc:
            print(f"error: receipt failed schema validation: {exc}", file=sys.stderr)
            return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")

    print(f"[ok] appended loop run receipt for {args.loop_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
