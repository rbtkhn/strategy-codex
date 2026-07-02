"""Append-only event registry changelog + compile to event-registry.json."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SCRIPTS = _REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from registry_pipeline.contracts import (  # noqa: E402
    ISRAEL_CHILD_IDS,
    fingerprint_gate_errors,
    normalize_event_v4,
    upsert_fingerprint_collision,
)
from registry_pipeline.falsifier_validator import validate_falsifiers, validate_trajectory_v4  # noqa: E402

REGISTRY_PATH = _REPO_ROOT / "statecraft" / "data" / "event-registry.json"
CHANGELOG_PATH = _REPO_ROOT / "statecraft" / "data" / "event-registry-changelog.jsonl"

class RegistryGateError(Exception):
    """Compile or changelog upsert rejected by semantic gatekeeper."""

    def __init__(self, errors: list[str]) -> None:
        self.errors = errors
        super().__init__("\n".join(errors))

def load_registry(path: Path | None = None) -> dict[str, Any]:
    target = path or REGISTRY_PATH
    return json.loads(target.read_text(encoding="utf-8"))

def load_changelog(path: Path | None = None) -> list[dict[str, Any]]:
    target = path or CHANGELOG_PATH
    if not target.exists():
        return []
    entries: list[dict[str, Any]] = []
    for line in target.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            entries.append(json.loads(line))
    return entries

def expand_changelog_ops(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Flatten nested baseline bundles into executable ops."""
    ops: list[dict[str, Any]] = []
    for entry in entries:
        op = str(entry.get("op") or "")
        nested = entry.get("ops")
        if op == "baseline_v4" and isinstance(nested, list):
            ops.extend(nested)
        elif op in {
            "upsert_event",
            "delete_event",
            "migrate_israel_dimensions",
            "normalize_all_v4",
        }:
            ops.append(entry)
    return ops

def validate_registry_gate(events: dict[str, dict[str, Any]]) -> tuple[list[str], list[str]]:
    """Semantic gatekeeper — falsifier/model, trajectory v4, fingerprint anti-splitting."""
    errors: list[str] = []
    fals_errors, fals_warnings, high_entropy = validate_falsifiers(events, strict=True)
    errors.extend(fals_errors)
    errors.extend(validate_trajectory_v4(events))
    errors.extend(fingerprint_gate_errors(events))
    warnings = list(fals_warnings)
    for eid in high_entropy:
        warnings.append(f"{eid}: high-entropy inferred falsifier_model — operator review")
    return errors, warnings

def validate_upsert_gate(
    event_id: str,
    event: dict[str, Any],
    registry: dict[str, dict[str, Any]],
    *,
    run_infer: bool = True,
) -> tuple[list[str], list[str]]:
    """Gate a single changelog upsert before append."""
    from registry_pipeline.probabilistic_falsifier_engine import enrich_event_falsifiers

    candidate = dict(event)
    if run_infer:
        candidate, _ = enrich_event_falsifiers(event_id, candidate)
    normalized = normalize_event_v4(event_id, candidate)
    errors, warnings = validate_registry_gate({event_id: normalized})
    errors.extend(upsert_fingerprint_collision(event_id, candidate, registry))
    return errors, warnings

def append_changelog(
    op: str,
    payload: dict[str, Any],
    *,
    note: str = "",
    path: Path | None = None,
    skip_gate: bool = False,
) -> dict[str, Any]:
    target = path or CHANGELOG_PATH
    if op == "upsert_event" and not skip_gate:
        event_id = str(payload.get("event_id") or "")
        event = dict(payload.get("event") or {})
        if not event_id:
            raise RegistryGateError(["upsert_event missing event_id"])
        registry = load_registry() if REGISTRY_PATH.is_file() else {}
        upsert_errors, _ = validate_upsert_gate(event_id, event, registry)
        if upsert_errors:
            raise RegistryGateError(upsert_errors)
    target.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "op": op,
        "note": note,
        **payload,
    }
    with target.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry

def apply_ops(registry: dict[str, Any], ops: list[dict[str, Any]]) -> dict[str, Any]:
    out = dict(registry)
    for entry in ops:
        op = str(entry.get("op") or "")
        if op == "upsert_event":
            event_id = str(entry["event_id"])
            event = dict(entry.get("event") or {})
            out[event_id] = normalize_event_v4(event_id, event)
        elif op == "delete_event":
            out.pop(str(entry["event_id"]), None)
        elif op == "migrate_israel_dimensions":
            parent_id = "israel_self_destruction_trajectory"
            parent = dict(out.get(parent_id) or {})
            existing_dims = parent.get("dimensions") or []
            has_children = any(child_id in out for child_id in ISRAEL_CHILD_IDS)
            if existing_dims and not has_children:
                continue
            dimensions: list[dict[str, Any]] = []
            for child_id in ISRAEL_CHILD_IDS:
                child = out.pop(child_id, None)
                if not child:
                    continue
                dimensions.append(
                    {
                        "id": child_id,
                        "label": str(child.get("question") or child_id),
                        "falsifier": child.get("falsifier") or "",
                        "confirmation_criteria": child.get("confirmation_criteria") or "",
                    }
                )
            parent["dimensions"] = dimensions
            parent.pop("child_event_ids", None)
            parent.pop("parent_event_id", None)
            out[parent_id] = normalize_event_v4(parent_id, parent)
            for child_id in ISRAEL_CHILD_IDS:
                out.pop(child_id, None)
        elif op == "normalize_all_v4":
            out = {
                eid: normalize_event_v4(eid, ev)
                for eid, ev in sorted(out.items())
            }
    return out

def compile_registry(
    *,
    registry_path: Path | None = None,
    changelog_path: Path | None = None,
    write: bool = True,
    skip_gate: bool = False,
    run_infer: bool = True,
) -> dict[str, Any]:
    from registry_pipeline.probabilistic_falsifier_engine import enrich_registry

    reg_path = registry_path or REGISTRY_PATH
    log_path = changelog_path or CHANGELOG_PATH
    base = load_registry(reg_path) if reg_path.exists() else {}
    ops = expand_changelog_ops(load_changelog(log_path))
    compiled = apply_ops(base, ops)
    if run_infer:
        compiled, _ = enrich_registry(compiled)
    if not skip_gate:
        gate_errors, _ = validate_registry_gate(compiled)
        if gate_errors:
            raise RegistryGateError(gate_errors)
    if write:
        reg_path.write_text(
            json.dumps(compiled, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    return compiled

def seed_v4_migration(*, write_changelog: bool = True) -> dict[str, Any]:
    registry = load_registry()
    ops = [
        {"op": "migrate_israel_dimensions"},
        {"op": "normalize_all_v4"},
    ]
    if write_changelog and not CHANGELOG_PATH.exists():
        append_changelog(
            "baseline_v4",
            {"ops": ops},
            note="Phase 3: Israel dimensions collapse + v4 field normalization",
        )
    return apply_ops(registry, ops)

def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Event registry changelog writer")
    sub = parser.add_subparsers(dest="command", required=True)
    compile_parser = sub.add_parser("compile", help="Apply changelog and write event-registry.json")
    compile_parser.add_argument("--no-infer", action="store_true", help="Skip probabilistic falsifier inference")
    seed = sub.add_parser("seed-v4", help="One-time Israel dimensions migration")
    seed.add_argument("--write", action="store_true", help="Write registry + changelog")
    args = parser.parse_args()

    if args.command == "compile":
        try:
            compile_registry(run_infer=not args.no_infer)
        except RegistryGateError as exc:
            for err in exc.errors:
                print(f"ERROR: {err}", file=sys.stderr)
            print(f"[fail] compile blocked by gatekeeper ({len(exc.errors)} error(s))", file=sys.stderr)
            return 1
        print(f"Compiled {REGISTRY_PATH}")
        return 0

    compiled = seed_v4_migration(write_changelog=args.write)
    if args.write:
        REGISTRY_PATH.write_text(
            json.dumps(compiled, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"Wrote {REGISTRY_PATH} ({len(compiled)} events)")
    else:
        print(json.dumps({"event_count": len(compiled)}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
