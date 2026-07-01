"""Fingerprint-based event compression — anti-splitting and Macgregor dedup."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SCRIPTS = _REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from prediction.contracts import find_duplicate_fingerprints  # noqa: E402
from prediction.registry_writer import REGISTRY_PATH, append_changelog, load_registry  # noqa: E402

MACGREGOR_MERGE_CANDIDATES: dict[str, str] = {
    "ukraine_western_aid_prolongs_war": "ukraine_escalation_russian_capitulation",
    "nato_strategic_exposure_ukraine": "ukraine_escalation_russian_capitulation",
}


def compression_report(
    events: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    registry = events or load_registry()
    dupes = find_duplicate_fingerprints(registry)
    merge_proposals: list[dict[str, Any]] = []
    for source_id, target_id in MACGREGOR_MERGE_CANDIDATES.items():
        if source_id in registry and target_id in registry:
            merge_proposals.append(
                {
                    "action": "review_merge",
                    "source_id": source_id,
                    "target_id": target_id,
                    "reason": "Macgregor seed overlap — operator review before deprecate",
                }
            )
    keep_ids = {
        "ukraine_escalation_russian_capitulation",
        "us_israel_iran_war_preparation_2025",
    }
    macgregor_only = [
        eid
        for eid, ev in registry.items()
        if "macgregor-seed" in (ev.get("tags") or [])
        and eid not in keep_ids
        and eid not in MACGREGOR_MERGE_CANDIDATES
    ]
    return {
        "event_count": len(registry),
        "duplicate_fingerprints": dupes,
        "macgregor_merge_proposals": merge_proposals,
        "macgregor_only_seeds": macgregor_only,
    }


def apply_macgregor_deprecations(
    *,
    event_ids: list[str] | None = None,
    dry_run: bool = True,
) -> list[str]:
    registry = load_registry()
    targets = event_ids or list(MACGREGOR_MERGE_CANDIDATES.keys())
    applied: list[str] = []
    for event_id in targets:
        if event_id not in registry:
            continue
        if dry_run:
            applied.append(event_id)
            continue
        append_changelog(
            "upsert_event",
            {
                "event_id": event_id,
                "event": {**registry[event_id], "status": "deprecated"},
            },
            note="compression_engine: merge candidate deprecated pending operator review",
        )
        applied.append(event_id)
    return applied


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Dry-run compression report")
    parser.add_argument("--apply", action="store_true", help="Apply Macgregor deprecations via changelog")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    if args.apply:
        applied = apply_macgregor_deprecations(dry_run=False)
        from prediction.registry_writer import RegistryGateError, compile_registry

        try:
            compile_registry()
        except RegistryGateError as exc:
            for err in exc.errors:
                print(f"ERROR: {err}", file=sys.stderr)
            return 1
        print(f"Deprecated {len(applied)} event(s) via changelog")
        return 0

    report = compression_report()
    if args.json or args.check:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"Events: {report['event_count']}")
        print(f"Duplicate fingerprints: {len(report['duplicate_fingerprints'])}")
        print(f"Macgregor merge proposals: {len(report['macgregor_merge_proposals'])}")
    return 1 if report["duplicate_fingerprints"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
