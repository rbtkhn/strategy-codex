#!/usr/bin/env python3
"""Auto-file Freeman prediction notes from scored capture hooks (no manifest audit)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REPORT = REPO_ROOT / "runtime" / "artifacts" / "freeman-prediction-auto-file-report.json"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from freeman_prediction_auto_file import (  # noqa: E402
    build_report_payload,
    collect_auto_file_candidates,
    load_auto_file_config,
    note_path_for,
    prune_stale_auto_file_notes,
    render_auto_file_note,
)
from prediction_lib import render_json  # noqa: E402

def auto_materialize(
    *,
    dry_run: bool = False,
    force: bool = False,
    prune: bool = False,
    event_id_filter: str | None = None,
    report_path: Path,
) -> tuple[int, int, int, int]:
    auto_cfg = load_auto_file_config()
    pruned = 0
    if prune:
        removed, _ = prune_stale_auto_file_notes(dry_run=dry_run, event_id_filter=event_id_filter)
        pruned = len(removed)

    candidates = collect_auto_file_candidates(auto_cfg=auto_cfg, event_id_filter=event_id_filter)
    written = skipped = 0

    for candidate in candidates:
        path = note_path_for(candidate)
        rel = path.relative_to(REPO_ROOT).as_posix()
        if path.is_file() and not force:
            skipped += 1
            if dry_run:
                print(f"[dry-run] skip existing {rel}")
            continue
        if dry_run:
            print(
                f"[dry-run] would write {rel} score={candidate.score} "
                f"({', '.join(candidate.reasons)})"
            )
            written += 1
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_auto_file_note(candidate), encoding="utf-8")
        written += 1
        print(f"[ok] wrote {rel} score={candidate.score}")

    report = build_report_payload(candidates)
    if not dry_run:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(render_json(report), encoding="utf-8")

    return written, skipped, len(candidates), pruned

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true", help="Overwrite existing note files")
    ap.add_argument(
        "--prune",
        action="store_true",
        help="Delete stale auto_file notes before materializing",
    )
    ap.add_argument("--event-id", default=None, help="Limit to one pilot event_id")
    ap.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = ap.parse_args()

    written, skipped, total, pruned = auto_materialize(
        dry_run=args.dry_run,
        force=args.force,
        prune=args.prune,
        event_id_filter=args.event_id,
        report_path=args.report,
    )
    mode = "dry-run" if args.dry_run else "wrote"
    print(
        f"[ok] auto_materialize_freeman_predictions: {mode} {written} note(s), "
        f"pruned {pruned}, skipped {skipped} existing, {total} candidate(s) scored above threshold"
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
