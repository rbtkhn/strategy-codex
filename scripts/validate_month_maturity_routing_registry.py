#!/usr/bin/env python3
"""
Validate statecraft/data/month-maturity-routing-registry.json.

Checks:
- required fields and allowed enum values
- unique month entries in YYYY-MM form
- primary supporting surfaces exist
- registered months exist in generated month-routing metadata
- metadata surface lists include the registry's primary surfaces
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = REPO_ROOT / "statecraft" / "data" / "month-maturity-routing-registry.json"
METADATA_PATH = REPO_ROOT / "statecraft" / "data" / "month-routing-metadata.json"

MONTH_RE = re.compile(r"^\d{4}-\d{2}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

ALLOWED_ROUTE_CLASSES = {"benchmark", "watchlist", "closure-audit"}
ALLOWED_STATUSES = {
    "open",
    "stable",
    "stable-with-live-seam",
    "audited-and-confirmed",
}
REQUIRED_MONTH_KEYS = {
    "month",
    "route_class",
    "maturity_label",
    "status",
    "primary_surfaces",
    "comparison_uses",
    "open_questions",
    "next_honest_move",
    "has_finite_queue",
    "updated_at",
}

def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))

def validate_month_maturity_routing_registry(
    repo_root: Path,
    *,
    registry_path: Path | None = None,
    metadata_path: Path | None = None,
) -> list[str]:
    errors: list[str] = []
    registry_path = registry_path or (repo_root / "statecraft" / "data" / "month-maturity-routing-registry.json")
    metadata_path = metadata_path or (repo_root / "statecraft" / "data" / "month-routing-metadata.json")

    if not registry_path.is_file():
        return [f"Missing {registry_path.relative_to(repo_root)}"]

    try:
        registry = _load_json(registry_path)
    except json.JSONDecodeError as exc:
        return [f"{registry_path.relative_to(repo_root)}: invalid JSON: {exc}"]

    months = registry.get("months")
    if not isinstance(months, list) or not months:
        return [f"{registry_path.relative_to(repo_root)}: months must be a non-empty array"]

    metadata_months: dict[str, dict] = {}
    if metadata_path.is_file():
        try:
            metadata = _load_json(metadata_path)
        except json.JSONDecodeError as exc:
            errors.append(f"{metadata_path.relative_to(repo_root)}: invalid JSON: {exc}")
            metadata = {}
        raw_metadata_months = metadata.get("months", {})
        if isinstance(raw_metadata_months, dict):
            metadata_months = {
                key: value
                for key, value in raw_metadata_months.items()
                if isinstance(key, str) and isinstance(value, dict)
            }
        else:
            errors.append(f"{metadata_path.relative_to(repo_root)}: months must be an object")
    else:
        errors.append(f"Missing {metadata_path.relative_to(repo_root)}")

    seen_months: set[str] = set()
    for idx, entry in enumerate(months, start=1):
        loc = f"months[{idx}]"
        if not isinstance(entry, dict):
            errors.append(f"{loc}: each entry must be an object")
            continue
        for key in REQUIRED_MONTH_KEYS:
            if key not in entry:
                errors.append(f"{loc}: missing required key {key!r}")

        month = entry.get("month")
        if not isinstance(month, str) or not MONTH_RE.match(month):
            errors.append(f"{loc}: month must match YYYY-MM")
            continue
        if month in seen_months:
            errors.append(f"{loc}: duplicate month entry {month}")
        seen_months.add(month)

        route_class = entry.get("route_class")
        if route_class not in ALLOWED_ROUTE_CLASSES:
            errors.append(
                f"{loc} ({month}): route_class must be one of {sorted(ALLOWED_ROUTE_CLASSES)}"
            )

        status = entry.get("status")
        if status not in ALLOWED_STATUSES:
            errors.append(f"{loc} ({month}): status must be one of {sorted(ALLOWED_STATUSES)}")

        maturity_label = entry.get("maturity_label")
        if not isinstance(maturity_label, str) or len(maturity_label.strip()) < 5:
            errors.append(f"{loc} ({month}): maturity_label too short or missing")

        next_move = entry.get("next_honest_move")
        if not isinstance(next_move, str) or len(next_move.strip()) < 10:
            errors.append(f"{loc} ({month}): next_honest_move too short or missing")

        updated_at = entry.get("updated_at")
        if not isinstance(updated_at, str) or not DATE_RE.match(updated_at):
            errors.append(f"{loc} ({month}): updated_at must match YYYY-MM-DD")

        has_finite_queue = entry.get("has_finite_queue")
        if not isinstance(has_finite_queue, bool):
            errors.append(f"{loc} ({month}): has_finite_queue must be a boolean")

        for key in ("primary_surfaces", "comparison_uses", "open_questions"):
            value = entry.get(key)
            if not isinstance(value, list) or not value:
                errors.append(f"{loc} ({month}): {key} must be a non-empty array")
                continue
            if not all(isinstance(item, str) and item.strip() for item in value):
                errors.append(f"{loc} ({month}): {key} entries must be non-empty strings")

        primary_surfaces = entry.get("primary_surfaces") or []
        for surface in primary_surfaces:
            if not isinstance(surface, str):
                continue
            surface_path = repo_root / surface
            if not surface_path.is_file():
                errors.append(f"{loc} ({month}): primary_surface not found: {surface}")

        metadata_entry = metadata_months.get(month)
        if metadata_months and metadata_entry is None:
            errors.append(f"{loc} ({month}): missing from month-routing metadata")
            continue
        if metadata_entry is None:
            continue

        existing_surfaces = metadata_entry.get("existing_month_surfaces")
        if not isinstance(existing_surfaces, list):
            errors.append(
                f"{metadata_path.relative_to(repo_root)}[{month!r}]: existing_month_surfaces must be an array"
            )
            continue
        existing_surface_set = {surface for surface in existing_surfaces if isinstance(surface, str)}
        for surface in primary_surfaces:
            if isinstance(surface, str) and surface not in existing_surface_set:
                errors.append(
                    f"{loc} ({month}): metadata missing primary surface {surface}"
                )

        if route_class == "benchmark":
            if metadata_entry.get("has_existing_benchmark_surfaces") is not True:
                errors.append(
                    f"{loc} ({month}): benchmark month should have has_existing_benchmark_surfaces=true in metadata"
                )
        else:
            if metadata_entry.get("has_existing_benchmark_surfaces") not in {False, None}:
                errors.append(
                    f"{loc} ({month}): non-benchmark month should not have has_existing_benchmark_surfaces=true"
                )

        if metadata_entry.get("has_finite_queue") != has_finite_queue:
            errors.append(
                f"{loc} ({month}): metadata has_finite_queue does not match registry"
            )

    return errors

def main() -> int:
    parser = argparse.ArgumentParser(description="Validate month maturity routing registry JSON.")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=REPO_ROOT,
        help="Repository root (default: parent of scripts/)",
    )
    args = parser.parse_args()
    repo_root = args.repo_root.resolve()
    errors = validate_month_maturity_routing_registry(repo_root)
    if errors:
        print("Month maturity routing registry validation FAILED:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1
    print("Month maturity routing registry: OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
