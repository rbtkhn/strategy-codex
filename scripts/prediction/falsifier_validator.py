"""Hard falsifier gate — extends check_event_registry for Phase 3."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SCRIPTS = _REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from check_event_registry import check_registry  # noqa: E402
from prediction.contracts import infer_prediction_type  # noqa: E402
from prediction_lib import load_event_registry  # noqa: E402


def validate_falsifiers(
    events: dict[str, dict[str, Any]],
    *,
    strict: bool = True,
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    for event_id, event in sorted(events.items()):
        pred_type = infer_prediction_type(event)
        has_falsifier = bool(str(event.get("falsifier") or "").strip())
        if pred_type == "not_falsifiable":
            continue
        if not has_falsifier:
            msg = f"{event_id}: missing falsifier (prediction_type={pred_type})"
            if strict:
                errors.append(msg)
            else:
                warnings.append(msg)
        dims = event.get("dimensions") or []
        if dims:
            for dim in dims:
                dim_id = str(dim.get("id") or "?")
                if not str(dim.get("falsifier") or "").strip():
                    msg = f"{event_id}: dimension {dim_id} missing falsifier"
                    if strict:
                        errors.append(msg)
                    else:
                        warnings.append(msg)
    return errors, warnings


def validate_trajectory_v4(events: dict[str, dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    for event_id, event in sorted(events.items()):
        if event.get("parent_event_id"):
            errors.append(f"{event_id}: parent_event_id deprecated in v4")
        children = event.get("child_event_ids") or []
        if children:
            errors.append(f"{event_id}: child_event_ids deprecated in v4 ({len(children)} refs)")
        if str(event.get("event_type") or "") == "trajectory":
            dims = event.get("dimensions") or []
            if not dims:
                errors.append(f"{event_id}: trajectory missing dimensions[]")
    return errors


def run_falsifier_validator(
    *,
    registry_path: Path | None = None,
    strict: bool = True,
) -> tuple[list[str], list[str]]:
    events = load_event_registry(registry_path)
    reg_errors, reg_warnings, _ = check_registry(events, strict_enrolled=strict)
    fals_errors, fals_warnings = validate_falsifiers(events, strict=strict)
    traj_errors = validate_trajectory_v4(events)
    errors = reg_errors + fals_errors + traj_errors
    warnings = reg_warnings + fals_warnings
    return errors, warnings


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=None)
    parser.add_argument("--warn-only", action="store_true")
    args = parser.parse_args()

    errors, warnings = run_falsifier_validator(
        registry_path=args.registry,
        strict=not args.warn_only,
    )
    for w in warnings:
        print(f"WARN: {w}", file=sys.stderr)
    for e in errors:
        print(f"ERROR: {e}", file=sys.stderr)
    if errors:
        return 1
    print(f"[ok] falsifier validator passed ({len(warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
