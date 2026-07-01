"""Hard falsifier gate — extends check_event_registry for Phase 3 / 3.5."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SCRIPTS = _REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from check_event_registry import check_registry  # noqa: E402
from registry_pipeline.contracts import (  # noqa: E402
    HIGH_ENTROPY_THRESHOLD,
    has_falsifier_coverage,
    infer_prediction_type,
    validate_falsifier_model,
)
from prediction_lib import load_event_registry  # noqa: E402


def validate_falsifiers(
    events: dict[str, dict[str, Any]],
    *,
    strict: bool = True,
) -> tuple[list[str], list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    high_entropy: list[str] = []
    for event_id, event in sorted(events.items()):
        pred_type = infer_prediction_type(event)
        if pred_type == "not_falsifiable" or event.get("not_falsifiable") is True:
            continue

        model = event.get("falsifier_model")
        if model is not None:
            model_errors = validate_falsifier_model(model)
            for err in model_errors:
                msg = f"{event_id}: falsifier_model {err}"
                if strict:
                    errors.append(msg)
                else:
                    warnings.append(msg)
            if isinstance(model, dict) and not model_errors:
                entropy = model.get("entropy")
                if isinstance(entropy, (int, float)) and float(entropy) >= HIGH_ENTROPY_THRESHOLD:
                    if str(model.get("inference_source") or "") == "heuristic_v1":
                        high_entropy.append(event_id)

        if not has_falsifier_coverage(event):
            msg = f"{event_id}: missing falsifier and falsifier_model (prediction_type={pred_type})"
            if strict:
                errors.append(msg)
            else:
                warnings.append(msg)

        dims = event.get("dimensions") or []
        if dims:
            for dim in dims:
                dim_id = str(dim.get("id") or "?")
                if not has_falsifier_coverage(dim):
                    msg = f"{event_id}: dimension {dim_id} missing falsifier and falsifier_model"
                    if strict:
                        errors.append(msg)
                    else:
                        warnings.append(msg)
                dim_model = dim.get("falsifier_model")
                if dim_model is not None:
                    for err in validate_falsifier_model(dim_model):
                        msg = f"{event_id}: dimension {dim_id} falsifier_model {err}"
                        if strict:
                            errors.append(msg)
                        else:
                            warnings.append(msg)
    return errors, warnings, high_entropy


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
) -> tuple[list[str], list[str], list[str]]:
    events = load_event_registry(registry_path)
    reg_errors, reg_warnings, _ = check_registry(events, strict_enrolled=strict)
    fals_errors, fals_warnings, high_entropy = validate_falsifiers(events, strict=strict)
    traj_errors = validate_trajectory_v4(events)
    errors = reg_errors + fals_errors + traj_errors
    warnings = reg_warnings + fals_warnings
    return errors, warnings, high_entropy


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=None)
    parser.add_argument("--warn-only", action="store_true")
    args = parser.parse_args()

    errors, warnings, high_entropy = run_falsifier_validator(
        registry_path=args.registry,
        strict=not args.warn_only,
    )
    for w in warnings:
        print(f"WARN: {w}", file=sys.stderr)
    for eid in high_entropy:
        print(f"WARN: {eid}: high-entropy inferred falsifier_model", file=sys.stderr)
    for e in errors:
        print(f"ERROR: {e}", file=sys.stderr)
    if errors:
        return 1
    print(f"[ok] falsifier validator passed ({len(warnings)} warning(s), {len(high_entropy)} high-entropy)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
