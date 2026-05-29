#!/usr/bin/env python3
"""Build generated inventory-style month indices for statecraft source archives."""

from __future__ import annotations

import argparse
import errno
from collections import Counter, defaultdict
from pathlib import Path

from statecraft_day_archive import DEFAULT_ROOT, DaySummary, fmt_counter, iter_day_dirs, summarize_day_dir


def month_key_from_day(day_name: str) -> str:
    return day_name[:7]


def group_day_dirs_by_month(root: Path, year: str) -> dict[str, list[Path]]:
    grouped: dict[str, list[Path]] = defaultdict(list)
    for day_dir in iter_day_dirs(root, year):
        grouped[month_key_from_day(day_dir.name)].append(day_dir)
    return dict(sorted(grouped.items()))


def merge_counter(days: list[DaySummary], attr: str) -> Counter[str]:
    counter: Counter[str] = Counter()
    for day in days:
        counter.update(getattr(day, attr))
    return counter


def top_counter_text(counter: Counter[str], limit: int = 3) -> str:
    if not counter:
        return "(none)"
    parts = [f"`{name}` ({count})" for name, count in counter.most_common(limit)]
    return ", ".join(parts)


def build_month_readme(root: Path, month: str, day_dirs: list[Path]) -> str:
    day_summaries = [summarize_day_dir(day_dir) for day_dir in day_dirs]
    source_total = sum(day.source_count for day in day_summaries)
    type_counter = merge_counter(day_summaries, "type_counter")
    channel_counter = merge_counter(day_summaries, "channel_counter")
    host_counter = merge_counter(day_summaries, "host_counter")
    guest_counter = merge_counter(day_summaries, "guest_counter")
    thread_counter = merge_counter(day_summaries, "thread_counter")
    fallback_counter = merge_counter(day_summaries, "fallback_counter")

    lines = [
        f"# Statecraft Archive - {month}",
        "",
        "_Generated inventory note. Rebuild with `python scripts/build_statecraft_month_indices.py`._",
        "",
        "## Stats",
        "",
        f"- Captured days: `{len(day_summaries)}`",
        f"- Source files: `{source_total}`",
        f"- Type mix: {fmt_counter(type_counter)}",
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
        "## Days",
        "",
        "| Day | Files | Top channels/shows | Top threads | README |",
        "| --- | ---: | --- | --- | --- |",
    ]

    for day_dir, summary in zip(day_dirs, day_summaries, strict=True):
        day_name = day_dir.name
        readme_rel = f"./{day_name}/README.md"
        lines.append(
            f"| `{day_name}` | {summary.source_count} | "
            f"{top_counter_text(summary.channel_counter)} | "
            f"{top_counter_text(summary.thread_counter)} | "
            f"[open]({readme_rel}) |"
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


def write_month_index(root: Path, month: str, day_dirs: list[Path], *, check: bool = False) -> tuple[Path, bool]:
    out_path = root / f"{month}.md"
    rendered = build_month_readme(root, month, day_dirs)
    existing = out_path.read_text(encoding="utf-8") if out_path.exists() else None
    changed = existing != rendered
    if changed and not check:
        try:
            out_path.write_text(rendered, encoding="utf-8", newline="\n")
        except PermissionError as exc:
            if exc.errno == errno.EACCES:
                raise PermissionError(
                    f"permission denied writing {out_path}; run with --check first to detect stale month indices, "
                    "then rerun the specific --month or --year write in an unsandboxed shell"
                ) from exc
            raise
    return out_path, changed


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="Statecraft source-archive root.")
    ap.add_argument("--year", type=str, default="all", help="Year prefix to index, or `all`.")
    ap.add_argument("--month", type=str, default=None, help="Specific YYYY-MM month to rebuild.")
    ap.add_argument("--check", action="store_true", help="Read and compare generated month indices without writing them.")
    return ap.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    all_groups: dict[str, list[Path]] = {}
    if args.month:
        target_year = args.month[:4]
        all_groups = group_day_dirs_by_month(root, target_year)
        if args.month not in all_groups:
            raise SystemExit(f"month not found: {args.month}")
        out_path, changed = write_month_index(root, args.month, all_groups[args.month], check=args.check)
        if args.check:
            print(f"{'stale' if changed else 'ok'} {out_path}")
            return 1 if changed else 0
        print(f"{'wrote' if changed else 'unchanged'} {out_path}")
        return 0

    if args.year == "all":
        years = sorted({p.name[:4] for p in root.iterdir() if p.is_dir() and len(p.name) >= 10 and p.name[4] == "-"})
        for year in years:
            all_groups.update(group_day_dirs_by_month(root, year))
    else:
        all_groups = group_day_dirs_by_month(root, args.year)

    changed_paths: list[Path] = []
    for month, day_dirs in all_groups.items():
        out_path, changed = write_month_index(root, month, day_dirs, check=args.check)
        if changed:
            changed_paths.append(out_path)
            if args.check:
                print(f"stale {out_path}")
    if args.check:
        if not changed_paths:
            print(f"ok 0 month indices under {root}")
            return 0
        print(f"stale {len(changed_paths)} month indices under {root}")
        return 1
    if not changed_paths:
        print(f"unchanged 0 month indices under {root}")
        return 0
    print(f"wrote {len(changed_paths)} month indices under {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
