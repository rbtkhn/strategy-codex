#!/usr/bin/env python3
"""Check notes-lane enrollment for voice prediction shelves."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TIMELINE = REPO_ROOT / "runtime" / "artifacts" / "prediction-timeline.json"
DEFAULT_QUEUE = REPO_ROOT / "runtime" / "artifacts" / "prediction-review-queue.json"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from voice_prediction_pilot import VOICE_REGISTRY, get_voice_config  # noqa: E402

def load_timeline(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {"events": {}}
    return json.loads(path.read_text(encoding="utf-8"))

def check_speaker_enrollment(
    speaker: str,
    *,
    timeline: dict[str, Any],
) -> list[str]:
    config = get_voice_config(speaker)
    issues: list[str] = []
    events_block = timeline.get("events") or {}

    for event_id in config.pilot_event_order:
        block = events_block.get(event_id) or {}
        speaker_shifts = (block.get("shifts") or {}).get(speaker) or []
        speaker_reviews = (block.get("reviews") or {}).get(speaker) or []
        latest = (block.get("latest_by_speaker") or {}).get(speaker)
        if not latest and not speaker_shifts and not speaker_reviews:
            issues.append(
                f"{speaker}/{event_id}: missing notes-lane timeline entry "
                "(latest_by_speaker, shift, or review)"
            )
    return issues

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--speaker", action="append", default=[])
    ap.add_argument("--timeline", type=Path, default=DEFAULT_TIMELINE)
    ap.add_argument("--emit-review-queue", action="store_true")
    ap.add_argument("--queue-output", type=Path, default=DEFAULT_QUEUE)
    args = ap.parse_args()

    speakers = args.speaker or sorted(VOICE_REGISTRY.keys())
    timeline = load_timeline(args.timeline)
    all_issues: list[str] = []
    queue_items: list[dict[str, Any]] = []

    for speaker in speakers:
        for issue in check_speaker_enrollment(speaker, timeline=timeline):
            all_issues.append(issue)
            queue_items.append(
                {
                    "type": "shelf_without_notes_lane",
                    "speaker": speaker,
                    "message": issue,
                }
            )

    for issue in all_issues:
        print(f"WARN: {issue}", file=sys.stderr)

    if args.emit_review_queue and queue_items:
        existing: list[dict[str, Any]] = []
        if args.queue_output.is_file():
            existing = json.loads(args.queue_output.read_text(encoding="utf-8")).get("items") or []
        merged = existing + queue_items
        payload = {
            "_meta": {
                "generated": True,
                "source": "scripts/check_voice_enrollment.py",
            },
            "items": merged,
        }
        args.queue_output.parent.mkdir(parents=True, exist_ok=True)
        args.queue_output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"[ok] appended {len(queue_items)} item(s) to review queue")

    if all_issues:
        print(f"[warn] {len(all_issues)} enrollment warning(s)")
        return 0
    print("[ok] notes-lane enrollment check passed")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
