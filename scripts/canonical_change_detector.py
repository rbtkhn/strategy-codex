#!/usr/bin/env python3
"""Detect changed repo paths and map them to derived rebuild targets."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from derived_regeneration import (
    REPO_ROOT,
    TARGETS,
    detect_git_changed_paths,
    expand_with_downstream,
    matched_paths_for_target,
    normalize_rel_path,
    select_targets_for_paths,
    topologically_sort_targets,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--paths",
        action="append",
        default=None,
        metavar="PATH",
        help="repo-relative changed path (repeat or comma-separated); default: detect from git status",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="emit machine-readable JSON",
    )
    parser.add_argument(
        "--incremental",
        action="store_true",
        help="include downstream targets and report them in dependency order",
    )
    return parser


def _expand(values: list[str] | None) -> list[str]:
    if not values:
        return []
    out: list[str] = []
    for value in values:
        for part in value.split(","):
            stripped = part.strip()
            if stripped:
                out.append(normalize_rel_path(stripped))
    return out


def main() -> int:
    args = build_parser().parse_args()
    changed_paths = _expand(args.paths) or detect_git_changed_paths(REPO_ROOT)
    directly_selected = select_targets_for_paths(changed_paths)
    selected = (
        topologically_sort_targets(expand_with_downstream(directly_selected))
        if args.incremental
        else directly_selected
    )
    direct_ids = {target.target_id for target in directly_selected}

    payload = {
        "repoRoot": str(REPO_ROOT),
        "changedPaths": changed_paths,
        "selectionMode": "incremental" if args.incremental else "direct",
        "targets": [
            {
                "targetId": target.target_id,
                "description": target.description,
                "selectionReason": "direct" if target.target_id in direct_ids else "downstream",
                "matchedPaths": matched_paths_for_target(changed_paths, target),
                "outputs": list(target.outputs),
            }
            for target in selected
        ],
        "knownTargets": [target.target_id for target in TARGETS],
    }

    if args.json:
        print(json.dumps(payload, indent=2))
        return 0

    print("# Canonical change detector")
    print()
    if changed_paths:
        print("Changed paths:")
        for path in changed_paths:
            print(f"- `{path}`")
    else:
        print("No changed paths detected.")
    print()
    if selected:
        label = "Impacted derived targets"
        if args.incremental:
            label += " (incremental order)"
        print(f"{label}:")
        for target in selected:
            matched = matched_paths_for_target(changed_paths, target)
            reason = "direct" if target.target_id in direct_ids else "downstream"
            print(f"- `{target.target_id}` ({reason}) - {target.description}")
            for path in matched:
                print(f"  - `{path}`")
    else:
        print("No derived rebuild targets matched.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
