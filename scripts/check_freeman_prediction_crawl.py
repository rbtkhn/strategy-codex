#!/usr/bin/env python3
"""Validate freeman-prediction-crawl.json manifest shape."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PATH = REPO_ROOT / "runtime" / "artifacts" / "freeman-prediction-crawl.json"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from freeman_prediction_pilot import load_thesis_map  # noqa: E402
from prediction_lib import STANCES  # noqa: E402

AUDIT_STATUSES = frozenset({"pending", "approved", "rejected", "defer"})

def validate_manifest(payload: dict) -> list[str]:
    issues: list[str] = []
    if "_meta" not in payload:
        issues.append("missing `_meta`")
    rows = payload.get("rows")
    if not isinstance(rows, list):
        issues.append("`rows` must be a list")
        return issues
    thesis = load_thesis_map()
    seen: set[tuple[str, str]] = set()
    by_event: dict[str, list[str]] = {}
    for idx, row in enumerate(rows):
        label = f"rows[{idx}]"
        if not isinstance(row, dict):
            issues.append(f"{label}: must be object")
            continue
        for field in ("source", "pub_date", "event_id", "match_method", "needs_human", "audit_status"):
            if field not in row:
                issues.append(f"{label}: missing `{field}`")
        event_id = str(row.get("event_id") or "")
        if event_id not in thesis:
            issues.append(f"{label}: unknown event_id `{event_id}`")
        source = str(row.get("source") or "")
        if source and not (REPO_ROOT / source.replace("\\", "/")).is_file():
            issues.append(f"{label}: missing source `{source}`")
        key = (source, event_id)
        if key in seen:
            issues.append(f"{label}: duplicate (source, event_id)")
        seen.add(key)
        status = str(row.get("audit_status") or "")
        if status and status not in AUDIT_STATUSES:
            issues.append(f"{label}: invalid audit_status `{status}`")
        if status == "approved":
            stance = str(row.get("audit_stance") or "")
            if stance not in STANCES:
                issues.append(f"{label}: approved row missing valid audit_stance")
            if not row.get("audit_speech_act"):
                issues.append(f"{label}: approved row missing audit_speech_act")
        pub = str(row.get("pub_date") or "")
        by_event.setdefault(event_id, []).append(pub)
    for event_id, dates in by_event.items():
        if dates != sorted(dates):
            issues.append(f"event {event_id}: pub_date not non-decreasing")
    return issues

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--manifest", type=Path, default=DEFAULT_PATH)
    args = ap.parse_args()
    if not args.manifest.is_file():
        print(f"error: missing {args.manifest.relative_to(REPO_ROOT)}", file=sys.stderr)
        return 1
    payload = json.loads(args.manifest.read_text(encoding="utf-8"))
    issues = validate_manifest(payload)
    if issues:
        for line in issues:
            print(line, file=sys.stderr)
        print(f"check_freeman_prediction_crawl: {len(issues)} violation(s)", file=sys.stderr)
        return 1
    print("[ok] freeman-prediction-crawl manifest valid")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
