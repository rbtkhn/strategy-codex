#!/usr/bin/env python3
"""Build generated root-level navigation indices for the statecraft source archive."""

from __future__ import annotations

import argparse
import errno
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from build_statecraft_month_indices import build_month_readme, group_day_dirs_by_month, month_key_from_day
from statecraft_day_archive import (
    DEFAULT_ROOT,
    REPO_ROOT,
    ArchiveFile,
    DaySummary,
    build_day_readme,
    collect_archive_file,
    fmt_counter,
    iter_day_dirs,
    iter_source_files,
    norm_scalar,
    parse_frontmatter,
    summarize_day_dir,
)
from statecraft_youtube_discovery import (  # noqa: E402
    canonical_channel_index_slug,
    is_daily_watchlist_slug,
    load_canonical_channel_labels,
    load_canonical_channel_urls,
    load_daily_watchlist_keys,
    load_index_slug_canonical,
    resolve_host_index_slug,
    resolve_filename_prefix_index_slug,
)

_SLUG_RE = re.compile(r"[^a-z0-9]+")


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


@dataclass
class ChannelStats:
    slug: str
    label: str
    file_count: int = 0
    youtube_count: int = 0
    days: set[str] = field(default_factory=set)
    months: set[str] = field(default_factory=set)
    shows: Counter[str] = field(default_factory=Counter)
    hosts: Counter[str] = field(default_factory=Counter)
    channel_url: str = ""
    explicit_slug: bool = True
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
    kind_counter = merge_counter(all_days, "kind_counter")
    source_form_counter = merge_counter(all_days, "source_form_counter")
    channel_counter = merge_counter(all_days, "channel_counter")
    host_counter = merge_counter(all_days, "host_counter")
    guest_counter = merge_counter(all_days, "guest_counter")
    thread_counter = merge_counter(all_days, "thread_counter")

    lines = [
        f"# Statecraft Archive - {year}",
        "",
        "_Generated inventory note. Rebuild with `python scripts/refresh_statecraft_archive_indices.py`._",
        "",
        "## Stats",
        "",
        f"- Captured months: `{len(month_summaries)}`",
        f"- Captured days: `{len(all_days)}`",
        f"- Source files: `{source_total}`",
        f"- Body kind mix: {fmt_counter(kind_counter)}",
        f"- Source form mix: {fmt_counter(source_form_counter)}",
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


def _slugify_channel_key(text: str) -> str:
    key = _SLUG_RE.sub("-", norm_scalar(text).lower()).strip("-")
    return key or "unknown"


def _is_youtube_capture(meta: dict[str, Any]) -> bool:
    if norm_scalar(meta.get("source_type")).casefold() == "youtube":
        return True
    if norm_scalar(meta.get("youtube_id")):
        return True
    url = norm_scalar(meta.get("source_url")).casefold()
    return "youtube.com" in url or "youtu.be" in url


def _channel_registry_key(meta: dict[str, Any], filename: str = "") -> tuple[str, str, bool]:
    slug = norm_scalar(meta.get("channel_slug"))
    label = (
        norm_scalar(meta.get("channel_name"))
        or norm_scalar(meta.get("show_title"))
        or norm_scalar(meta.get("show"))
    )
    if slug:
        return slug, label or slug.replace("-", " ").title(), True
    if label:
        return _slugify_channel_key(label), label, False
    host = norm_scalar(meta.get("host"))
    if host:
        host_slug = resolve_host_index_slug(host)
        if host_slug:
            return host_slug, host, False
    if filename:
        prefix_slug = resolve_filename_prefix_index_slug(filename)
        if prefix_slug:
            return prefix_slug, prefix_slug.replace("-", " ").title(), False
    return "unknown", "(none)", False


def collect_channel_stats(root: Path) -> dict[str, ChannelStats]:
    canonical_map = load_index_slug_canonical()
    canonical_labels = load_canonical_channel_labels()
    canonical_urls = load_canonical_channel_urls()
    stats: dict[str, ChannelStats] = {}
    for day_dir in iter_all_day_dirs(root):
        day = day_dir.name
        month = month_key_from_day(day)
        for path in iter_source_files(day_dir):
            meta = parse_frontmatter(path)
            if not _is_youtube_capture(meta):
                continue
            slug, label, explicit_slug = _channel_registry_key(meta, path.name)
            index_slug = canonical_channel_index_slug(slug, canonical_map)
            if index_slug in canonical_labels:
                label = canonical_labels[index_slug]
            entry = stats.get(index_slug)
            if entry is None:
                entry = ChannelStats(
                    slug=index_slug,
                    label=label,
                    explicit_slug=explicit_slug or index_slug in canonical_labels,
                    channel_url=canonical_urls.get(index_slug, ""),
                )
                stats[index_slug] = entry
            elif label and entry.label in {"", "(none)"}:
                entry.label = label
            if explicit_slug or index_slug in canonical_labels:
                entry.explicit_slug = True
            entry.file_count += 1
            entry.youtube_count += 1
            entry.days.add(day)
            entry.months.add(month)
            show = norm_scalar(meta.get("show_title")) or norm_scalar(meta.get("show"))
            if show:
                entry.shows[show] += 1
            host = norm_scalar(meta.get("host"))
            if host:
                entry.hosts[host] += 1
            channel_url = norm_scalar(meta.get("channel_url"))
            if channel_url and not entry.channel_url:
                entry.channel_url = channel_url
            if not entry.channel_url and index_slug in canonical_urls:
                entry.channel_url = canonical_urls[index_slug]
            entry.first_day = day if entry.first_day is None else min(entry.first_day, day)
            entry.last_day = day if entry.last_day is None else max(entry.last_day, day)
    return dict(sorted(stats.items()))


def build_channel_index(root: Path) -> str:
    channel_stats = collect_channel_stats(root)
    watchlist_keys = load_daily_watchlist_keys()
    total_files = sum(entry.file_count for entry in channel_stats.values())
    explicit_slug_count = sum(1 for entry in channel_stats.values() if entry.explicit_slug)

    lines = [
        "# Statecraft Archive - YouTube Channel Index",
        "",
        "_Generated inventory note. Rebuild with `python scripts/refresh_statecraft_archive_indices.py`._",
        "",
        "Flat registry of **YouTube channels** seen in `source-*.md` captures (`source_type: youtube`,",
        "`youtube_id`, or YouTube `source_url`). Articles, Substack, and other non-YouTube surfaces are excluded.",
        "Primary key: YAML `channel_slug` when present; otherwise derived from `channel_name` / `show`,",
        "or configured `host` / filename prefix when listed in discovery config.",
        "",
        "Curated daily watchlist (subset): "
        "[statecraft_youtube_discovery.json](../../platform/config/statecraft_youtube_discovery.json) · "
        "[youtube-transcript-queue.md](../../statecraft/sheets/source-archive-control/youtube-transcript-queue.md) · "
        "Legacy: [COGNITION-STREAMS-WATCHLIST-DEPRECATED.md](../../docs/skill-work/work-strategy/COGNITION-STREAMS-WATCHLIST-DEPRECATED.md)",
        "",
        "## Stats",
        "",
        f"- Distinct YouTube channel keys: `{len(channel_stats)}`",
        f"- YouTube source files mapped: `{total_files}`",
        f"- Rows with explicit `channel_slug`: `{explicit_slug_count}`",
        f"- Watchlist channels (matched): `{sum(1 for e in channel_stats.values() if is_daily_watchlist_slug(e.slug, watchlist_keys))}`",
        "",
        "## Channels",
        "",
        "| Channel slug | Label | Files | Days | Watchlist | Channel URL | First day | Last day |",
        "| --- | --- | ---: | ---: | --- | --- | --- | --- |",
    ]

    for entry in sorted(channel_stats.values(), key=lambda item: (-item.file_count, item.slug)):
        url = entry.channel_url or ""
        if url and not url.startswith("http"):
            url = f"https://{url}"
        url_cell = f"[open]({url})" if url.startswith("http") else ""
        watchlist_cell = "yes" if is_daily_watchlist_slug(entry.slug, watchlist_keys) else ""
        slug_note = "" if entry.explicit_slug else " *"
        lines.append(
            f"| `{entry.slug}`{slug_note} | {entry.label} | {entry.file_count} | "
            f"{len(entry.days)} | {watchlist_cell} | {url_cell} | `{entry.first_day or ''}` | `{entry.last_day or ''}` |"
        )

    lines.extend(
        [
            "",
            "_`*` = slug derived from label; no explicit `channel_slug` in frontmatter._",
            "",
            "## Return",
            "",
            "- Root archive: [source-archive/statecraft/README.md](./README.md)",
            "- Thread index: [thread-index.md](./thread-index.md)",
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
        "_Generated inventory note. Rebuild with `python scripts/refresh_statecraft_archive_indices.py`._",
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
    channel_path = root / "channel-index.md"
    channel_status = _render_compare_status(channel_path, build_channel_index(root))

    day_counter = Counter(status for _, status in day_rows)
    month_counter = Counter(status for _, status in month_rows)
    year_counter = Counter(status for _, status in year_rows)

    lines = [
        "# Statecraft Archive - Stale Index Audit",
        "",
        "_Generated inventory note. Rebuild with `python scripts/refresh_statecraft_archive_indices.py`._",
        "",
        "## Stats",
        "",
        f"- Day indices: {fmt_counter(day_counter)}",
        f"- Month indices: {fmt_counter(month_counter)}",
        f"- Year indices: {fmt_counter(year_counter)}",
        f"- Thread index: `{thread_status}`",
        f"- Channel index: `{channel_status}`",
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
            f"- `channel-index.md`: `{channel_status}`",
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

    channel_path, channel_changed = write_rendered(root / "channel-index.md", build_channel_index(root), check=args.check)
    if channel_changed:
        changed_paths.append(channel_path)
        if args.check:
            print(f"stale {channel_path}")

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
