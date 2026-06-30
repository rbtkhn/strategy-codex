#!/usr/bin/env python3
"""Apply operator Israel-catalog audit pass to freeman-prediction-crawl.json."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST = REPO_ROOT / "runtime" / "artifacts" / "freeman-prediction-crawl.json"
EVENT_ID = "israel_self_destruction_trajectory"
JAN_PREFIX = "2025-01-"

# Title-approved rows: optional speech_act override (default restated).
TITLE_SPEECH_ACT: dict[str, str] = {
    "2025-10-07": "iterated",
    "2025-10-31": "iterated",
    "2025-12-05": "iterated",
    "2026-05-01": "iterated",
    "2026-05-26": "iterated",
}

JAN_BODY_SPEECH_ACT: dict[str, str] = {
    "2025-01-14": "restated",
    "2025-01-17": "restated",
    "2025-01-21": "iterated",
}

REJECT_BODY = "body_keyword outside Jan 2025 window; incidental thesis hit — defer to title/register pass"


def should_approve(row: dict) -> bool:
    if row.get("event_id") != EVENT_ID:
        return False
    method = str(row.get("match_method") or "")
    pub = str(row.get("pub_date") or "")
    if method == "title" or method == "register":
        return True
    if method == "body_keyword" and pub.startswith(JAN_PREFIX):
        return True
    return False


def speech_act_for(row: dict) -> str:
    pub = str(row.get("pub_date") or "")
    method = str(row.get("match_method") or "")
    suggested = row.get("suggested_speech_act")
    if suggested in {"restated", "iterated"}:
        return str(suggested)
    if method == "body_keyword" and pub in JAN_BODY_SPEECH_ACT:
        return JAN_BODY_SPEECH_ACT[pub]
    if method == "title" and pub in TITLE_SPEECH_ACT:
        return TITLE_SPEECH_ACT[pub]
    return "restated"


def apply_audit(payload: dict) -> tuple[int, int]:
    approved = rejected = 0
    for row in payload.get("rows") or []:
        if row.get("event_id") != EVENT_ID:
            continue
        if should_approve(row):
            row["audit_status"] = "approved"
            row["audit_stance"] = "yes"
            row["audit_speech_act"] = speech_act_for(row)
            row["reject_reason"] = None
            row["needs_human"] = False
            approved += 1
        else:
            row["audit_status"] = "rejected"
            row["audit_stance"] = None
            row["audit_speech_act"] = None
            row["reject_reason"] = REJECT_BODY
            row["needs_human"] = False
            rejected += 1
    return approved, rejected


def main() -> int:
    if not MANIFEST.is_file():
        print(f"error: missing {MANIFEST.relative_to(REPO_ROOT)}", file=sys.stderr)
        return 1
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    approved, rejected = apply_audit(payload)
    MANIFEST.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        f"[ok] Israel catalog audit: {approved} approved, {rejected} rejected "
        f"({MANIFEST.relative_to(REPO_ROOT)})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
