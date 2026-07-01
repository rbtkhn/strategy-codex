#!/usr/bin/env python3
"""Phase 3 CI orchestrator — orphan events, falsifiers, trajectory v4, shift lint."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REGISTRY = REPO_ROOT / "statecraft" / "data" / "event-registry.json"
DEFAULT_REGISTRY_ARTIFACT = REPO_ROOT / "runtime" / "artifacts" / "prediction-registry.json"
DEFAULT_TIMELINE = REPO_ROOT / "runtime" / "artifacts" / "prediction-timeline.json"
DEFAULT_QUEUE = REPO_ROOT / "runtime" / "artifacts" / "prediction-review-queue.json"
PREDICTIONS_DIR = REPO_ROOT / "statecraft" / "notes" / "predictions"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from prediction.contracts import fingerprint_gate_errors  # noqa: E402
from prediction.contracts import predictive_fingerprint  # noqa: E402
from prediction.falsifier_validator import (  # noqa: E402
    run_falsifier_validator,
    validate_trajectory_v4,
)
from prediction_lib import collect_prediction_notes, load_event_registry  # noqa: E402
from voice_prediction_pilot import VOICE_REGISTRY, load_capture_map  # noqa: E402


def collect_referenced_event_ids() -> set[str]:
    refs: set[str] = set()
    for note in collect_prediction_notes():
        refs.add(note.event_id)
    for cfg in VOICE_REGISTRY.values():
        cap_path = cfg.capture_map_path
        if not cap_path.is_file():
            continue
        for row in load_capture_map(cap_path, guest_speaker=cfg.speaker):
            refs.add(str(row.get("event_id") or ""))
    return {r for r in refs if r}


def check_orphan_events(events: dict[str, dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    for event_id in sorted(collect_referenced_event_ids()):
        if event_id not in events:
            errors.append(f"orphan event_id {event_id!r} referenced but not in registry")
    return errors


def check_fake_shifts(timeline: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    for event_id, block in (timeline.get("events") or {}).items():
        for speaker, shifts in (block.get("shifts") or {}).items():
            for shift in shifts:
                shift_type = str(shift.get("type") or "")
                if shift_type not in {
                    "stance_shift",
                    "mechanism_shift",
                    "horizon_shift",
                    "contradiction",
                    "flip",
                    "qualification_shift",
                    "certainty_shift",
                    "stance_change",
                }:
                    warnings.append(
                        f"{event_id}/{speaker}: unknown shift type {shift_type!r}"
                    )
                from_stance = str(shift.get("from") or shift.get("from_stance") or "")
                to_stance = str(shift.get("to") or shift.get("to_stance") or "")
                if shift_type in {"stance_shift", "flip", "contradiction"} and from_stance == to_stance:
                    warnings.append(
                        f"{event_id}/{speaker}: fake stance shift — same stance {from_stance!r}"
                    )
    return warnings


def check_event_inflation(events: dict[str, dict[str, Any]]) -> list[str]:
    return fingerprint_gate_errors(events)


def check_renderer_ssot(events: dict[str, dict[str, Any]]) -> list[str]:
    warnings: list[str] = []
    for speaker, cfg in VOICE_REGISTRY.items():
        json_path = cfg.predictions_json_path
        if not json_path.is_file():
            continue
        payload = json.loads(json_path.read_text(encoding="utf-8"))
        for ev in payload.get("events") or []:
            event_id = str(ev.get("event_id") or "")
            if event_id not in events:
                warnings.append(f"{speaker}: shelf event {event_id!r} not in registry")
            if ev.get("child_event_ids"):
                warnings.append(f"{speaker}/{event_id}: shelf still exposes child_event_ids")
    return warnings


def run_phase3_checks(
    *,
    registry_path: Path | None = None,
    timeline_path: Path | None = None,
    strict_shifts: bool = False,
) -> tuple[list[str], list[str], list[dict[str, Any]]]:
    events = load_event_registry(registry_path)
    errors: list[str] = []
    warnings: list[str] = []
    queue: list[dict[str, Any]] = []

    errors.extend(check_orphan_events(events))
    fals_errors, fals_warnings = run_falsifier_validator(registry_path=registry_path, strict=True)
    errors.extend(f for f in fals_errors if "missing falsifier" in f or "deprecated" in f or "trajectory" in f)
    warnings.extend(fals_warnings)

    tl_path = timeline_path or DEFAULT_TIMELINE
    if tl_path.is_file():
        timeline = json.loads(tl_path.read_text(encoding="utf-8"))
        shift_issues = check_fake_shifts(timeline)
        if strict_shifts:
            errors.extend(shift_issues)
        else:
            warnings.extend(shift_issues)
            for msg in shift_issues:
                queue.append({"type": "fake_shift", "message": msg})

    inflation = check_event_inflation(events)
    if strict_shifts:
        errors.extend(inflation)
    else:
        warnings.extend(inflation)
        for msg in inflation:
            queue.append({"type": "event_inflation", "message": msg})

    warnings.extend(check_renderer_ssot(events))

    return errors, warnings, queue


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    ap.add_argument("--timeline", type=Path, default=DEFAULT_TIMELINE)
    ap.add_argument(
        "--strict-shifts",
        action="store_true",
        help="checks 4-5 are ERROR (Phase 3b default)",
    )
    ap.add_argument("--emit-review-queue", action="store_true")
    ap.add_argument("--queue-output", type=Path, default=DEFAULT_QUEUE)
    args = ap.parse_args()

    errors, warnings, queue = run_phase3_checks(
        registry_path=args.registry,
        timeline_path=args.timeline,
        strict_shifts=args.strict_shifts,
    )

    for w in warnings:
        print(f"WARN: {w}", file=sys.stderr)
    for e in errors:
        print(f"ERROR: {e}", file=sys.stderr)

    if args.emit_review_queue and queue:
        payload = {
            "_meta": {
                "generated": True,
                "source": "scripts/check_phase3.py",
                "description": "Phase 3 review queue",
            },
            "items": queue,
        }
        args.queue_output.parent.mkdir(parents=True, exist_ok=True)
        args.queue_output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"[ok] wrote {args.queue_output.relative_to(REPO_ROOT)}")

    if errors:
        print(f"[fail] {len(errors)} error(s), {len(warnings)} warning(s)", file=sys.stderr)
        return 1
    print(f"[ok] check_phase3 passed ({len(warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
