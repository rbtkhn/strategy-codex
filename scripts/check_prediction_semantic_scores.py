#!/usr/bin/env python3
"""Validate prediction-semantic-scores.json shape — advisory only (never blocks)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PATH = REPO_ROOT / "runtime" / "artifacts" / "prediction-semantic-scores.json"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from build_prediction_semantic_scores import build_semantic_scores_payload  # noqa: E402
from prediction_lib import load_event_registry, render_json  # noqa: E402

REQUIRED_EVENT_FIELDS = (
    "entropy_score",
    "falsifier_confidence",
    "inference_source",
    "compression_quality",
    "risk_of_overcollapse",
)


def validate_scores(payload: dict) -> list[str]:
    issues: list[str] = []
    if "_meta" not in payload:
        issues.append("missing top-level `_meta`")
    events = payload.get("events")
    if not isinstance(events, dict):
        issues.append("`events` must be an object")
        return issues
    for event_id, block in events.items():
        if not isinstance(block, dict):
            issues.append(f"events.{event_id}: must be an object")
            continue
        for field in REQUIRED_EVENT_FIELDS:
            if field not in block:
                issues.append(f"events.{event_id}: missing `{field}`")
    return issues


def run_check(*, path: Path | None = None, warn_high_entropy: bool = True, advisory: bool = False) -> int:
    target = path or DEFAULT_PATH
    if not target.is_file():
        msg = f"missing {target.relative_to(REPO_ROOT)}"
        if advisory:
            print(f"WARN: {msg}", file=sys.stderr)
            return 0
        print(f"error: {msg}", file=sys.stderr)
        return 1
    payload = json.loads(target.read_text(encoding="utf-8"))
    issues = validate_scores(payload)
    if issues:
        for line in issues:
            if advisory:
                print(f"WARN: {line}", file=sys.stderr)
            else:
                print(line, file=sys.stderr)
        return 0 if advisory else 1

    expected = render_json(build_semantic_scores_payload(load_event_registry()))
    current = target.read_text(encoding="utf-8")
    if current != expected:
        msg = (
            f"{target.relative_to(REPO_ROOT)} is out of date; "
            "run build_prediction_semantic_scores.py"
        )
        if advisory:
            print(f"WARN: {msg}", file=sys.stderr)
        else:
            print(f"error: {msg}", file=sys.stderr)
            return 1

    if warn_high_entropy:
        for event_id, block in (payload.get("events") or {}).items():
            if block.get("falsifier_confidence") == "low" and block.get("inference_source") == "heuristic_v1":
                print(
                    f"WARN: {event_id}: low falsifier_confidence (heuristic inference)",
                    file=sys.stderr,
                )

    print("[ok] prediction semantic scores valid (advisory)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--path", type=Path, default=DEFAULT_PATH)
    ap.add_argument("--check", action="store_true")
    ap.add_argument(
        "--advisory",
        action="store_true",
        help="Never block exit code; emit WARN lines only (check_repo_health)",
    )
    args = ap.parse_args()
    return run_check(path=args.path, advisory=args.advisory)


if __name__ == "__main__":
    raise SystemExit(main())
