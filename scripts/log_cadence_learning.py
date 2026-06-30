#!/usr/bin/env python3
"""Append a WORK-only cadence learning event."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from cadence_learning import append_learning_event
from repo_io import DEFAULT_PROFILE_ID

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-u", "--user", default=DEFAULT_PROFILE_ID)
    parser.add_argument("--event-type", required=True, choices=("dream_stage", "coffee_choice", "coffee_resolution"))
    parser.add_argument("--payload-json", required=True, help="JSON object payload for the learning event")
    parser.add_argument("--ledger", type=Path, default=None)
    args = parser.parse_args()

    payload = json.loads(args.payload_json)
    path = append_learning_event(args.user, args.event_type, payload, ledger_path=args.ledger)
    print(path)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
