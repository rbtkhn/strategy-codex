#!/usr/bin/env python3
"""Validate event-registry.json — falsifiers, resolved closure, parent/child consistency."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REGISTRY = REPO_ROOT / "statecraft" / "data" / "event-registry.json"
DEFAULT_QUEUE = REPO_ROOT / "runtime" / "artifacts" / "prediction-review-queue.json"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from prediction_lib import EVENT_STATUSES, load_event_registry  # noqa: E402
from voice_prediction_pilot import VOICE_REGISTRY  # noqa: E402

# Voices with generated shelves on manifest (strict falsifier gate in Phase 3+)
ENROLLED_PILOT_EVENTS: frozenset[str] = frozenset(
    eid for cfg in VOICE_REGISTRY.values() for eid in cfg.pilot_event_order
)


def event_id_to_wire_stub_slug(event_id: str) -> str:
    return str(event_id).replace("_", "-")


def wire_stub_path(event_id: str) -> Path:
    slug = event_id_to_wire_stub_slug(event_id)
    return REPO_ROOT / "statecraft" / "notes" / "wire" / f"prediction-resolution-{slug}.md"


def check_registry(
    events: dict[str, dict[str, Any]],
    *,
    strict_enrolled: bool = False,
) -> tuple[list[str], list[str], list[dict[str, Any]]]:
    errors: list[str] = []
    warnings: list[str] = []
    queue_items: list[dict[str, Any]] = []

    for event_id, event in sorted(events.items()):
        status = str(event.get("status") or "")
        if status and status not in EVENT_STATUSES:
            errors.append(f"{event_id}: invalid status {status!r}")

        if status == "resolved":
            if not event.get("resolved_date"):
                errors.append(f"{event_id}: resolved event missing resolved_date")
            if not event.get("resolution_source"):
                errors.append(f"{event_id}: resolved event missing resolution_source")
            stub = wire_stub_path(event_id)
            if not stub.is_file():
                msg = f"{event_id}: resolved without wire stub {stub.relative_to(REPO_ROOT).as_posix()}"
                warnings.append(msg)
                queue_items.append(
                    {"type": "resolved_without_wire_stub", "event_id": event_id, "message": msg}
                )

        has_falsifier = bool(str(event.get("falsifier") or "").strip())
        not_falsifiable = event.get("not_falsifiable") is True
        if not has_falsifier and not not_falsifiable:
            msg = f"{event_id}: missing falsifier (set falsifier or not_falsifiable: true)"
            if strict_enrolled and event_id in ENROLLED_PILOT_EVENTS:
                errors.append(msg)
            else:
                warnings.append(msg)
            queue_items.append({"type": "needs_falsifier", "event_id": event_id, "message": msg})

        parent = event.get("parent_event_id")
        if parent is not None and str(parent).strip():
            msg = f"{event_id}: parent_event_id deprecated in v4 — use dimensions[] on trajectory"
            errors.append(msg)

        children = event.get("child_event_ids") or []
        if isinstance(children, list) and children:
            errors.append(
                f"{event_id}: child_event_ids deprecated in v4 ({len(children)} refs) — use dimensions[]"
            )

        event_type = str(event.get("event_type") or "")
        dims = event.get("dimensions") or []
        if event_type == "trajectory" or "trajectory" in event_id:
            if not dims:
                msg = f"{event_id}: trajectory missing dimensions[]"
                errors.append(msg)

    return errors, warnings, queue_items


def emit_review_queue(items: list[dict[str, Any]], *, output_path: Path) -> None:
    payload = {
        "_meta": {
            "generated": True,
            "source": "scripts/check_event_registry.py",
            "description": "Operator prediction review queue",
        },
        "items": items,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    ap.add_argument(
        "--strict-enrolled",
        action="store_true",
        help="missing falsifier on enrolled pilot events is ERROR (Phase 3+)",
    )
    ap.add_argument(
        "--emit-review-queue",
        action="store_true",
        help=f"write queue items to {DEFAULT_QUEUE.relative_to(REPO_ROOT)}",
    )
    ap.add_argument("--queue-output", type=Path, default=DEFAULT_QUEUE)
    args = ap.parse_args()

    events = load_event_registry(args.registry)
    errors, warnings, queue_items = check_registry(events, strict_enrolled=args.strict_enrolled)

    for warning in warnings:
        print(f"WARN: {warning}", file=sys.stderr)
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)

    if args.emit_review_queue:
        emit_review_queue(queue_items, output_path=args.queue_output)
        print(f"[ok] wrote {args.queue_output.relative_to(REPO_ROOT)}")

    if errors:
        print(f"[fail] {len(errors)} error(s), {len(warnings)} warning(s)", file=sys.stderr)
        return 1
    print(f"[ok] event registry check passed ({len(warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
