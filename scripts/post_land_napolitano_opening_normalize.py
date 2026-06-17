#!/usr/bin/env python3
"""Post-land hook: Napolitano opening scaffold normalize for statecraft captures.

Intake calls this immediately after landing a Judging Freedom / Napolitano object
under ``source-archive/statecraft/``. Default applies conservative trims in place;
use ``--dry-run`` to preview only.

Usage:
    python scripts/post_land_napolitano_opening_normalize.py --path <landed-file>
    python scripts/post_land_napolitano_opening_normalize.py --path <landed-file> --dry-run
    python scripts/post_land_napolitano_opening_normalize.py --day 2026-06-16 --dry-run
    python scripts/post_land_napolitano_opening_normalize.py --month 2026-06 --dry-run
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from normalize_napolitano_opening_scaffold import (  # noqa: E402
    ARCHIVE_ROOT,
    is_napolitano_capture,
    normalize_text,
    split_frontmatter,
)

DAY_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
MONTH_RE = re.compile(r"^\d{4}-\d{2}$")


@dataclass(frozen=True)
class PostLandResult:
    path: Path
    status: str
    applied: bool
    flags: str
    opening_tier: str


@dataclass(frozen=True)
class BatchSummary:
    scanned: int
    would_change: int
    applied: int
    no_op: int
    skipped: int


def _resolve_landed_path(path: Path) -> Path:
    resolved = (REPO_ROOT / path).resolve() if not path.is_absolute() else path.resolve()
    if not resolved.is_file():
        raise FileNotFoundError(f"landed file not found: {resolved}")
    try:
        resolved.relative_to(ARCHIVE_ROOT.resolve())
    except ValueError as exc:
        raise ValueError(
            f"path must be under {ARCHIVE_ROOT.relative_to(REPO_ROOT).as_posix()}: {resolved}"
        ) from exc
    return resolved


def _napolitano_capture_paths(folder: Path) -> list[Path]:
    if not folder.is_dir():
        return []
    paths = sorted(
        p
        for p in folder.glob("source-napolitano-*.md")
        if p.is_file() and ".cleaned." not in p.name
    )
    return paths


def collect_batch_paths(
    *,
    paths: list[Path] | None = None,
    day: str | None = None,
    month: str | None = None,
) -> list[Path]:
    """Resolve Napolitano capture paths for single-file, day, or month batch runs."""
    explicit = paths or []
    if explicit:
        return sorted({_resolve_landed_path(path) for path in explicit})

    if day:
        if not DAY_RE.match(day):
            raise ValueError(f"--day must be YYYY-MM-DD, got: {day}")
        return _napolitano_capture_paths(ARCHIVE_ROOT / day)

    if month:
        if not MONTH_RE.match(month):
            raise ValueError(f"--month must be YYYY-MM, got: {month}")
        collected: list[Path] = []
        for folder in sorted(ARCHIVE_ROOT.glob(f"{month}-*")):
            collected.extend(_napolitano_capture_paths(folder))
        return sorted(set(collected))

    raise ValueError("provide --path, --day YYYY-MM-DD, or --month YYYY-MM")


def post_land_napolitano_opening_normalize(
    path: Path,
    *,
    dry_run: bool = False,
    tag_only: bool = False,
) -> PostLandResult:
    """Normalize one landed Napolitano capture; apply unless ``dry_run``."""
    landed = _resolve_landed_path(path)
    text = landed.read_text(encoding="utf-8")
    meta, _ = split_frontmatter(text)
    if not is_napolitano_capture(meta, landed):
        return PostLandResult(
            path=landed,
            status="skipped-not-napolitano",
            applied=False,
            flags="",
            opening_tier=str(meta.get("opening_tier") or ""),
        )

    changed, new_text, file_change = normalize_text(landed, text, tag_only=tag_only)
    if file_change is None or not changed:
        tier = str(meta.get("opening_tier") or (file_change.opening_tier if file_change else ""))
        return PostLandResult(
            path=landed,
            status="no-op",
            applied=False,
            flags="",
            opening_tier=tier,
        )

    flags: list[str] = []
    if file_change.cold_open_trimmed:
        flags.append("cold_open")
    if file_change.sponsor_trimmed:
        flags.append("sponsor")
    if file_change.close_promo_trimmed:
        flags.append("close_promo")
    if file_change.paragraphs_removed:
        flags.append(f"-{file_change.paragraphs_removed}p")
    joined = ", ".join(flags) if flags else "metadata"

    if not dry_run:
        landed.write_text(new_text, encoding="utf-8")

    return PostLandResult(
        path=landed,
        status="dry-run" if dry_run else "applied",
        applied=not dry_run,
        flags=joined,
        opening_tier=file_change.opening_tier,
    )


def _format_flags(result: PostLandResult) -> str:
    rel = result.path.relative_to(REPO_ROOT).as_posix()
    if result.status == "skipped-not-napolitano":
        return f"skip {rel} (not Judging Freedom / Napolitano)"
    if result.status == "no-op":
        tier = f" tier={result.opening_tier}" if result.opening_tier else ""
        return f"no-op {rel}{tier}"
    mode = "would-change" if result.status == "dry-run" else "applied"
    return f"{mode} {rel} [{result.flags}] tier={result.opening_tier}"


def run_batch(
    paths: list[Path],
    *,
    dry_run: bool = False,
    tag_only: bool = False,
    stream: bool = True,
) -> tuple[list[PostLandResult], BatchSummary]:
    """Run post-land normalize on many captures in one process; print progress as you go."""
    results: list[PostLandResult] = []
    would_change = 0
    applied = 0
    no_op = 0
    skipped = 0

    for path in paths:
        try:
            result = post_land_napolitano_opening_normalize(
                path,
                dry_run=dry_run,
                tag_only=tag_only,
            )
        except (FileNotFoundError, ValueError) as exc:
            if stream:
                print(f"error {path}: {exc}", flush=True)
            raise
        results.append(result)
        if result.status == "skipped-not-napolitano":
            skipped += 1
        elif result.status == "no-op":
            no_op += 1
        elif result.status == "dry-run":
            would_change += 1
        elif result.status == "applied":
            applied += 1
        if stream:
            print(_format_flags(result), flush=True)

    summary = BatchSummary(
        scanned=len(results),
        would_change=would_change,
        applied=applied,
        no_op=no_op,
        skipped=skipped,
    )
    return results, summary


def _format_batch_summary(summary: BatchSummary, *, dry_run: bool) -> str:
    mode = "dry-run" if dry_run else "apply"
    sep = " | "
    if dry_run:
        return (
            f"Batch {mode}:{sep}{summary.scanned} scanned{sep}"
            f"{summary.would_change} would-change{sep}{summary.no_op} no-op{sep}{summary.skipped} skipped"
        )
    return (
        f"Batch {mode}:{sep}{summary.scanned} scanned{sep}"
        f"{summary.applied} applied{sep}{summary.no_op} no-op{sep}{summary.skipped} skipped"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--path",
        type=Path,
        action="append",
        default=[],
        help="Landed capture under source-archive/statecraft/ (repeatable).",
    )
    parser.add_argument(
        "--day",
        type=str,
        help="All Napolitano captures for one archive day (YYYY-MM-DD).",
    )
    parser.add_argument(
        "--month",
        type=str,
        help="All Napolitano captures for one archive month (YYYY-MM).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview trim only; do not write.",
    )
    parser.add_argument(
        "--tag-only",
        action="store_true",
        help="Only set opening_tier metadata; do not trim body.",
    )
    args = parser.parse_args()

    if not args.path and not args.day and not args.month:
        parser.error("provide --path, --day YYYY-MM-DD, or --month YYYY-MM")

    selectors = sum(bool(x) for x in (args.path, args.day, args.month))
    if selectors > 1:
        parser.error("use only one of --path, --day, or --month")

    try:
        paths = collect_batch_paths(paths=args.path or None, day=args.day, month=args.month)
    except (FileNotFoundError, ValueError) as exc:
        print(exc, file=sys.stderr)
        return 1

    if not paths:
        scope = args.day or args.month or "selection"
        print(f"no Napolitano captures found for {scope}", file=sys.stderr)
        return 0

    _, summary = run_batch(paths, dry_run=args.dry_run, tag_only=args.tag_only, stream=True)
    print(_format_batch_summary(summary, dry_run=args.dry_run), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
