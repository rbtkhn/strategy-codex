#!/usr/bin/env python3
"""Refresh or verify generated statecraft source-archive navigation indices.

Composes existing builders (day README, month rollup, year/thread/stale-audit) without
editing authoritative capture files under ``source-archive/statecraft/<pub_date>/``.

Usage:
    python3 scripts/refresh_statecraft_archive_indices.py
    python3 scripts/refresh_statecraft_archive_indices.py --check
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import build_statecraft_archive_navigation as nav  # noqa: E402
import build_statecraft_day_indices as day_idx  # noqa: E402
import build_statecraft_month_indices as month_idx  # noqa: E402
from statecraft_day_archive import DEFAULT_ROOT, iter_day_dirs  # noqa: E402


def _metadata_semantically_changed(path: Path, payload: dict[str, object]) -> bool:
    """Ignore volatile ``generated_at`` when comparing routing metadata."""
    import json

    rendered = json.dumps(payload, indent=2, ensure_ascii=True) + "\n"
    if not path.exists():
        return True
    existing = json.loads(path.read_text(encoding="utf-8"))
    fresh = json.loads(rendered)
    for blob in (existing, fresh):
        blob.pop("generated_at", None)
    return existing != fresh


def refresh_or_check(root: Path, *, check: bool) -> tuple[int, list[Path]]:
    """Return (stale_count, changed_paths)."""
    changed_paths: list[Path] = []
    years = nav.list_years(root)
    if not years:
        print(f"ok 0 years under {root}")
        return 0, changed_paths

    for year in years:
        for day_dir in iter_day_dirs(root, year):
            out_path, changed = day_idx.write_day_index(day_dir, check=check)
            if changed:
                changed_paths.append(out_path)
                if check:
                    print(f"stale {out_path}")

    all_groups: dict[str, list[Path]] = {}
    for year in years:
        all_groups.update(month_idx.group_day_dirs_by_month(root, year))

    routing_registry = month_idx.load_routing_registry()
    for month, day_dirs in sorted(all_groups.items()):
        out_path, changed = month_idx.write_month_index(root, month, day_dirs, check=check)
        if changed:
            changed_paths.append(out_path)
            if check:
                print(f"stale {out_path}")

    metadata_payload = month_idx.build_month_metadata(all_groups, routing_registry)
    metadata_path = month_idx.ROUTING_METADATA_PATH
    if check:
        metadata_changed = _metadata_semantically_changed(metadata_path, metadata_payload)
    else:
        _, metadata_changed = month_idx.write_json_payload(
            metadata_path,
            metadata_payload,
            check=False,
        )
    if metadata_changed:
        changed_paths.append(metadata_path)
        if check:
            print(f"stale {metadata_path}")

    for year in years:
        path, changed = nav.write_rendered(
            root / f"{year}.md",
            nav.build_year_index(root, year),
            check=check,
        )
        if changed:
            changed_paths.append(path)
            if check:
                print(f"stale {path}")

    thread_path, thread_changed = nav.write_rendered(
        root / "thread-index.md",
        nav.build_thread_index(root),
        check=check,
    )
    if thread_changed:
        changed_paths.append(thread_path)
        if check:
            print(f"stale {thread_path}")

    audit_path, audit_changed = nav.write_rendered(
        root / "stale-index-audit.md",
        nav.build_stale_index_audit(root),
        check=check,
    )
    if audit_changed:
        changed_paths.append(audit_path)
        if check:
            print(f"stale {audit_path}")

    return len(changed_paths), changed_paths


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="Statecraft source-archive root.")
    ap.add_argument(
        "--check",
        action="store_true",
        help="Compare generated indices without writing; exit 1 if any are stale or missing.",
    )
    return ap.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        print(f"archive root not found: {root}", file=sys.stderr)
        return 2

    stale_count, _ = refresh_or_check(root, check=args.check)
    if args.check:
        if stale_count == 0:
            print(f"ok 0 stale archive navigation files under {root}")
            return 0
        print(f"stale {stale_count} archive navigation files under {root}")
        return 1

    if stale_count == 0:
        print(f"unchanged 0 archive navigation files under {root}")
        return 0
    print(f"wrote {stale_count} archive navigation files under {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
