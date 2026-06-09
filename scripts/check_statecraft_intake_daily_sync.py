#!/usr/bin/env python3
"""Compare statecraft archive day truth vs daily synthesis listing for one pub_date.

Read-only. Exit 0 when in sync or when no daily exists; exit 1 on DESYNC.

Usage:
    python3 scripts/check_statecraft_intake_daily_sync.py --day 2026-06-08
    python3 scripts/check_statecraft_intake_daily_sync.py --latest
    python3 scripts/check_statecraft_intake_daily_sync.py --all
    python3 scripts/check_statecraft_intake_daily_sync.py --day 2026-06-08 --json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from statecraft_day_archive import DEFAULT_ROOT, iter_all_day_dirs, summarize_day_dir  # noqa: E402

DAILY_DIR = REPO_ROOT / "statecraft" / "daily"
ARCHIVE_CHECKPOINT_RE = re.compile(
    r"Archive checkpoint:\s*\*\*(\d+)\*\*",
    re.IGNORECASE,
)
DAILY_SOURCE_LINK_RE = re.compile(
    r"source-archive/statecraft/(\d{4}-\d{2}-\d{2})/(source-[^)\s`]+\.md)",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class SyncReport:
    day: str
    status: str  # ok | desync | no_daily | no_archive
    archive_count: int
    daily_checkpoint_count: int | None
    archive_only: tuple[str, ...]
    daily_only: tuple[str, ...]
    daily_path: str | None
    archive_day_dir: str | None

    @property
    def exit_code(self) -> int:
        if self.status in {"ok", "no_daily", "no_archive"}:
            return 0
        return 1


def _parse_daily_checkpoint(text: str) -> int | None:
    match = ARCHIVE_CHECKPOINT_RE.search(text)
    if not match:
        return None
    return int(match.group(1))


def _parse_daily_source_slugs(text: str, day: str) -> set[str]:
    slugs: set[str] = set()
    for link_day, slug in DAILY_SOURCE_LINK_RE.findall(text):
        if link_day == day:
            slugs.add(slug)
    return slugs


def build_sync_report(day: str, *, root: Path = DEFAULT_ROOT, daily_dir: Path = DAILY_DIR) -> SyncReport:
    day_dir = root / day
    daily_path = daily_dir / f"{day}.md"

    if not day_dir.is_dir():
        return SyncReport(
            day=day,
            status="no_archive",
            archive_count=0,
            daily_checkpoint_count=None,
            archive_only=(),
            daily_only=(),
            daily_path=str(daily_path.relative_to(REPO_ROOT)) if daily_path.is_file() else None,
            archive_day_dir=None,
        )

    summary = summarize_day_dir(day_dir)
    archive_slugs = set(summary.file_names)

    if not daily_path.is_file():
        return SyncReport(
            day=day,
            status="no_daily",
            archive_count=summary.source_count,
            daily_checkpoint_count=None,
            archive_only=tuple(sorted(archive_slugs)),
            daily_only=(),
            daily_path=None,
            archive_day_dir=str(day_dir.relative_to(REPO_ROOT)),
        )

    daily_text = daily_path.read_text(encoding="utf-8-sig", errors="replace")
    daily_slugs = _parse_daily_source_slugs(daily_text, day)
    checkpoint = _parse_daily_checkpoint(daily_text)

    archive_only = tuple(sorted(archive_slugs - daily_slugs))
    daily_only = tuple(sorted(daily_slugs - archive_slugs))

    count_mismatch = checkpoint is not None and checkpoint != summary.source_count
    slug_mismatch = bool(archive_only or daily_only)
    status = "desync" if count_mismatch or slug_mismatch else "ok"

    return SyncReport(
        day=day,
        status=status,
        archive_count=summary.source_count,
        daily_checkpoint_count=checkpoint,
        archive_only=archive_only,
        daily_only=daily_only,
        daily_path=str(daily_path.relative_to(REPO_ROOT)),
        archive_day_dir=str(day_dir.relative_to(REPO_ROOT)),
    )


def format_human(report: SyncReport) -> str:
    lines = [
        f"statecraft intake/daily sync — {report.day}",
        f"status: {report.status.upper()}",
        f"archive_count: {report.archive_count}",
    ]
    if report.daily_checkpoint_count is not None:
        lines.append(f"daily_checkpoint_count: {report.daily_checkpoint_count}")
    if report.archive_day_dir:
        lines.append(f"archive_day_dir: {report.archive_day_dir}")
    if report.daily_path:
        lines.append(f"daily_path: {report.daily_path}")

    if report.status == "no_daily":
        lines.append("note: daily synthesis missing — intake-only day is ok")
        if report.archive_only:
            lines.append(f"archive_sources ({len(report.archive_only)}): {', '.join(report.archive_only)}")
        return "\n".join(lines)

    if report.status == "no_archive":
        lines.append("note: archive day folder missing")
        return "\n".join(lines)

    if report.archive_only:
        lines.append(f"archive_only ({len(report.archive_only)}):")
        for slug in report.archive_only:
            lines.append(f"  - {slug}")
    if report.daily_only:
        lines.append(f"daily_only ({len(report.daily_only)}):")
        for slug in report.daily_only:
            lines.append(f"  - {slug}")
    if report.status == "ok":
        lines.append("ok: archive and daily source lists align")
    else:
        lines.append(
            "action: run statecraft daily synthesis or wire missing captures into "
            f"statecraft/daily/{report.day}.md before treating the day as current"
        )
    return "\n".join(lines)


def iter_captured_days(*, root: Path = DEFAULT_ROOT) -> list[str]:
    """All YYYY-MM-DD archive days with at least one source file, oldest first."""
    root = root.resolve()
    if not root.is_dir():
        return []
    days: list[str] = []
    for day_dir in iter_all_day_dirs(root):
        if summarize_day_dir(day_dir).source_count > 0:
            days.append(day_dir.name)
    return days


def build_batch_reports(
    *,
    root: Path = DEFAULT_ROOT,
    daily_dir: Path = DAILY_DIR,
    from_day: str | None = None,
    to_day: str | None = None,
) -> list[SyncReport]:
    reports: list[SyncReport] = []
    for day in iter_captured_days(root=root):
        if from_day and day < from_day:
            continue
        if to_day and day > to_day:
            continue
        reports.append(build_sync_report(day, root=root, daily_dir=daily_dir))
    return reports


def batch_exit_code(reports: list[SyncReport]) -> int:
    return 1 if any(report.status == "desync" for report in reports) else 0


def format_batch_human(reports: list[SyncReport], *, desync_only: bool = False) -> str:
    if not reports:
        return "statecraft intake/daily sync — batch audit\nno captured archive days found"

    counts = {"ok": 0, "desync": 0, "no_daily": 0, "no_archive": 0}
    for report in reports:
        counts[report.status] = counts.get(report.status, 0) + 1

    lines = [
        "statecraft intake/daily sync — batch audit",
        f"days_checked: {len(reports)}",
        f"ok: {counts['ok']} · desync: {counts['desync']} · no_daily: {counts['no_daily']}",
        "",
        "day          status    archive  daily_cp  archive_only",
        "-----------  --------  -------  --------  ------------",
    ]
    table_rows = [r for r in reports if r.status == "desync"] if desync_only else reports
    for report in table_rows:
        checkpoint = (
            str(report.daily_checkpoint_count)
            if report.daily_checkpoint_count is not None
            else "-"
        )
        if report.status == "desync":
            only_n = len(report.archive_only)
            flag = f"{only_n}" if only_n else "count"
        else:
            flag = "-"
        lines.append(
            f"{report.day}  {report.status:8}  {report.archive_count:7}  {checkpoint:>8}  {flag}"
        )

    desyncs = [r for r in reports if r.status == "desync"]
    if desyncs:
        lines.extend(["", "desync detail:"])
        for report in desyncs:
            lines.append(f"- {report.day}:")
            if report.archive_only:
                for slug in report.archive_only:
                    lines.append(f"    archive_only: {slug}")
            if report.daily_only:
                for slug in report.daily_only:
                    lines.append(f"    daily_only: {slug}")
            if (
                report.daily_checkpoint_count is not None
                and report.daily_checkpoint_count != report.archive_count
            ):
                lines.append(
                    f"    count_mismatch: archive={report.archive_count} "
                    f"daily_checkpoint={report.daily_checkpoint_count}"
                )
        lines.extend(
            [
                "",
                "action: wire missing captures or run statecraft daily synthesis per desync day",
            ]
        )
    else:
        lines.extend(["", "ok: no desync across captured archive days"])

    return "\n".join(lines)


def resolve_latest_captured_day(*, root: Path = DEFAULT_ROOT) -> str | None:
    """Return the newest YYYY-MM-DD archive day with at least one source file."""
    days = iter_captured_days(root=root)
    return days[-1] if days else None


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=__doc__)
    day_group = ap.add_mutually_exclusive_group(required=True)
    day_group.add_argument("--day", help="Publication date YYYY-MM-DD")
    day_group.add_argument(
        "--latest",
        action="store_true",
        help="Use the newest archive day folder with at least one source file",
    )
    day_group.add_argument(
        "--all",
        action="store_true",
        help="Audit every captured archive day (backlog desync scan)",
    )
    ap.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    ap.add_argument(
        "--desync-only",
        action="store_true",
        help="With --all, print only desync rows in the table (summary still full)",
    )
    ap.add_argument(
        "--from-day",
        metavar="YYYY-MM-DD",
        help="With --all, earliest pub_date to include",
    )
    ap.add_argument(
        "--to-day",
        metavar="YYYY-MM-DD",
        help="With --all, latest pub_date to include",
    )
    ap.add_argument(
        "--root",
        type=Path,
        default=DEFAULT_ROOT,
        help="Statecraft source-archive root",
    )
    return ap.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    if args.all:
        reports = build_batch_reports(root=root, from_day=args.from_day, to_day=args.to_day)
        if args.json:
            payload = {
                "mode": "batch",
                "days_checked": len(reports),
                "desync_count": sum(1 for r in reports if r.status == "desync"),
                "reports": [asdict(r) for r in reports],
            }
            print(json.dumps(payload, indent=2))
        else:
            print(format_batch_human(reports, desync_only=args.desync_only))
        return batch_exit_code(reports)

    if args.latest:
        day = resolve_latest_captured_day(root=root)
        if day is None:
            if args.json:
                print(json.dumps({"status": "no_capture_days", "day": None}))
            else:
                print("statecraft intake/daily sync — no captured archive days found")
            return 0
    else:
        day = args.day.strip()
    report = build_sync_report(day, root=root)
    if args.json:
        print(json.dumps(asdict(report), indent=2))
    else:
        print(format_human(report))
    return report.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
