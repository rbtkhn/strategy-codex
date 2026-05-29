#!/usr/bin/env python3
"""Build generated root-level navigation indices for the statecraft source archive."""

from __future__ import annotations

import argparse
import errno
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from build_statecraft_month_indices import build_month_readme, group_day_dirs_by_month, month_key_from_day
from statecraft_day_archive import (
    DEFAULT_ROOT,
    ArchiveFile,
    DaySummary,
    build_day_readme,
    collect_archive_file,
    fmt_counter,
    iter_day_dirs,
    iter_source_files,
    summarize_day_dir,
)


@dataclass
class ThreadStats:
    file_count: int = 0
    days: set[str] = field(default_factory=set)
    months: set[str] = field(default_factory=set)
    channels: Counter[str] = field(default_factory=Counter)
    hosts: Counter[str] = field(default_factory=Counter)
    guests: Counter[str] = field(default_factory=Counter)
    first_day: str | None = None
    last_day: str | None = None


def iter_all_day_dirs(root: Path) -> list[Path]:
    return sorted(
        [path for path in root.iterdir() if path.is_dir() and len(path.name) == 10 and path.name[4] == "-" and path.name[7] == "-"],
        key=lambda path: path.name,
    )


def list_years(root: Path) -> list[str]:
    return sorted({day_dir.name[:4] for day_dir in iter_all_day_dirs(root)})


def merge_counter(days: list[DaySummary], attr: str) -> Counter[str]:
    counter: Counter[str] = Counter()
    for day in days:
        counter.update(getattr(day, attr))
    return counter


def top_counter_text(counter: Counter[str], limit: int = 3) -> str:
    if not counter:
        return "(none)"
    return ", ".join(f"`{name}` ({count})" for name, count in counter.most_common(limit))


def build_year_index(root: Path, year: str) -> str:
    month_groups = group_day_dirs_by_month(root, year)
    month_summaries: list[tuple[str, list[DaySummary]]] = []
    for month, day_dirs in month_groups.items():
        month_summaries.append((month, [summarize_day_dir(day_dir) for day_dir in day_dirs]))

    all_days = [summary for _, summaries in month_summaries for summary in summaries]
    source_total = sum(day.source_count for day in all_days)
    channel_counter = merge_counter(all_days, "channel_counter")
    host_counter = merge_counter(all_days, "host_counter")
    guest_counter = merge_counter(all_days, "guest_counter")
    thread_counter = merge_counter(all_days, "thread_counter")
    fallback_counter = merge_counter(all_days, "fallback_counter")

    lines = [
        f"# Statecraft Archive - {year}",
        "",
        "_Generated inventory note. Rebuild with `python scripts/build_statecraft_archive_navigation.py`._",
        "",
        "## Stats",
        "",
        f"- Captured months: `{len(month_summaries)}`",
        f"- Captured days: `{len(all_days)}`",
        f"- Source files: `{source_total}`",
        f"- Distinct channels/shows: `{len(channel_counter)}`",
        f"- Distinct hosts: `{len(host_counter)}`",
        f"- Distinct guests: `{len(guest_counter)}`",
        f"- Distinct threads: `{len(thread_counter)}`",
        "",
        "## Rollups",
        "",
        f"- Channels/shows: {fmt_counter(channel_counter)}",
        f"- Hosts: {fmt_counter(host_counter)}",
        f"- Guests: {fmt_counter(guest_counter)}",
        f"- Threads: {fmt_counter(thread_counter)}",
        f"- Filename-family fallbacks: {fmt_counter(fallback_counter)}",
        "",
        "## Months",
        "",
        "| Month | Days | Files | Top channels/shows | Top threads | Index |",
        "| --- | ---: | ---: | --- | --- | --- |",
    ]

    for month, summaries in month_summaries:
        month_source_total = sum(day.source_count for day in summaries)
        month_channel_counter = merge_counter(summaries, "channel_counter")
        month_thread_counter = merge_counter(summaries, "thread_counter")
        lines.append(
            f"| `{month}` | {len(summaries)} | {month_source_total} | "
            f"{top_counter_text(month_channel_counter)} | "
            f"{top_counter_text(month_thread_counter)} | "
            f"[open](./{month}.md) |"
        )

    lines.extend(
        [
            "",
            "## Return",
            "",
            "- Root archive: [source-archive/statecraft/README.md](./README.md)",
            "",
        ]
    )
    return "\n".join(lines)


def collect_thread_stats(root: Path) -> dict[str, ThreadStats]:
    stats: dict[str, ThreadStats] = {}
    for day_dir in iter_all_day_dirs(root):
        day = day_dir.name
        month = month_key_from_day(day)
        for path in iter_source_files(day_dir):
            record = collect_archive_file(path)
            for thread in record.thread_values:
                entry = stats.setdefault(thread, ThreadStats())
                entry.file_count += 1
                entry.days.add(day)
                entry.months.add(month)
                entry.channels.update(record.channel_values)
                entry.hosts.update(record.host_values)
                entry.guests.update(record.guest_values)
                entry.first_day = day if entry.first_day is None else min(entry.first_day, day)
                entry.last_day = day if entry.last_day is None else max(entry.last_day, day)
    return dict(sorted(stats.items()))


def build_thread_index(root: Path) -> str:
    thread_stats = collect_thread_stats(root)
    total_files = sum(entry.file_count for entry in thread_stats.values())
    total_days = len({day for entry in thread_stats.values() for day in entry.days})
    total_months = len({month for entry in thread_stats.values() for month in entry.months})

    lines = [
        "# Statecraft Archive - Thread Index",
        "",
        "_Generated inventory note. Rebuild with `python scripts/build_statecraft_archive_navigation.py`._",
        "",
        "## Stats",
        "",
        f"- Distinct threads: `{len(thread_stats)}`",
        f"- Thread-linked source files: `{total_files}`",
        f"- Covered days: `{total_days}`",
        f"- Covered months: `{total_months}`",
        "",
        "## Threads",
        "",
        "| Thread | Files | Days | Months | Top channels/shows | Top hosts | First day | Last day |",
        "| --- | ---: | ---: | ---: | --- | --- | --- | --- |",
    ]

    for thread, entry in sorted(thread_stats.items(), key=lambda item: (-item[1].file_count, item[0])):
        lines.append(
            f"| `{thread}` | {entry.file_count} | {len(entry.days)} | {len(entry.months)} | "
            f"{top_counter_text(entry.channels)} | "
            f"{top_counter_text(entry.hosts)} | "
            f"`{entry.first_day or ''}` | "
            f"`{entry.last_day or ''}` |"
        )

    lines.extend(
        [
            "",
            "## Return",
            "",
            "- Root archive: [source-archive/statecraft/README.md](./README.md)",
            "",
        ]
    )
    return "\n".join(lines)


def _render_compare_status(path: Path, rendered: str) -> str:
    if not path.exists():
        return "missing"
    existing = path.read_text(encoding="utf-8", errors="replace")
    return "ok" if existing == rendered else "stale"


def build_stale_index_audit(root: Path) -> str:
    day_rows: list[tuple[str, str]] = []
    month_rows: list[tuple[str, str]] = []
    year_rows: list[tuple[str, str]] = []

    for day_dir in iter_all_day_dirs(root):
        path = day_dir / "README.md"
        rendered = build_day_readme(day_dir)
        day_rows.append((day_dir.name, _render_compare_status(path, rendered)))

    for year in list_years(root):
        month_groups = group_day_dirs_by_month(root, year)
        for month, day_dirs in month_groups.items():
            path = root / f"{month}.md"
            rendered = build_month_readme(root, month, day_dirs)
            month_rows.append((month, _render_compare_status(path, rendered)))
        year_path = root / f"{year}.md"
        year_rendered = build_year_index(root, year)
        year_rows.append((year, _render_compare_status(year_path, year_rendered)))

    thread_path = root / "thread-index.md"
    thread_status = _render_compare_status(thread_path, build_thread_index(root))

    day_counter = Counter(status for _, status in day_rows)
    month_counter = Counter(status for _, status in month_rows)
    year_counter = Counter(status for _, status in year_rows)

    lines = [
        "# Statecraft Archive - Stale Index Audit",
        "",
        "_Generated inventory note. Rebuild with `python scripts/build_statecraft_archive_navigation.py`._",
        "",
        "## Stats",
        "",
        f"- Day indices: {fmt_counter(day_counter)}",
        f"- Month indices: {fmt_counter(month_counter)}",
        f"- Year indices: {fmt_counter(year_counter)}",
        f"- Thread index: `{thread_status}`",
        "",
        "## Day Index Status",
        "",
        "| Day | Status |",
        "| --- | --- |",
    ]
    lines.extend(f"| `{day}` | `{status}` |" for day, status in day_rows)
    lines.extend(
        [
            "",
            "## Month Index Status",
            "",
            "| Month | Status |",
            "| --- | --- |",
        ]
    )
    lines.extend(f"| `{month}` | `{status}` |" for month, status in month_rows)
    lines.extend(
        [
            "",
            "## Year Index Status",
            "",
            "| Year | Status |",
            "| --- | --- |",
        ]
    )
    lines.extend(f"| `{year}` | `{status}` |" for year, status in year_rows)
    lines.extend(
        [
            "",
            "## Root Navigation Status",
            "",
            f"- `thread-index.md`: `{thread_status}`",
            "",
            "## Return",
            "",
            "- Root archive: [source-archive/statecraft/README.md](./README.md)",
            "",
        ]
    )
    return "\n".join(lines)


def write_rendered(path: Path, rendered: str, *, check: bool = False) -> tuple[Path, bool]:
    existing = path.read_text(encoding="utf-8") if path.exists() else None
    changed = existing != rendered
    if changed and not check:
        try:
            path.write_text(rendered, encoding="utf-8", newline="\n")
        except PermissionError as exc:
            if exc.errno == errno.EACCES:
                raise PermissionError(
                    f"permission denied writing {path}; run with --check first to detect stale archive navigation, "
                    "then rerun the specific write in an unsandboxed shell"
                ) from exc
            raise
    return path, changed


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="Statecraft source-archive root.")
    ap.add_argument("--check", action="store_true", help="Read and compare generated archive-navigation files without writing them.")
    return ap.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()

    changed_paths: list[Path] = []
    for year in list_years(root):
        path, changed = write_rendered(root / f"{year}.md", build_year_index(root, year), check=args.check)
        if changed:
            changed_paths.append(path)
            if args.check:
                print(f"stale {path}")

    thread_path, thread_changed = write_rendered(root / "thread-index.md", build_thread_index(root), check=args.check)
    if thread_changed:
        changed_paths.append(thread_path)
        if args.check:
            print(f"stale {thread_path}")

    audit_path, audit_changed = write_rendered(root / "stale-index-audit.md", build_stale_index_audit(root), check=args.check)
    if audit_changed:
        changed_paths.append(audit_path)
        if args.check:
            print(f"stale {audit_path}")

    if args.check:
        if not changed_paths:
            print(f"ok 0 archive navigation files under {root}")
            return 0
        print(f"stale {len(changed_paths)} archive navigation files under {root}")
        return 1

    if not changed_paths:
        print(f"unchanged 0 archive navigation files under {root}")
        return 0
    print(f"wrote {len(changed_paths)} archive navigation files under {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
