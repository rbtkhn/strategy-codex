#!/usr/bin/env python3
"""Build generated inventory-style month indices for statecraft source archives."""

from __future__ import annotations

import argparse
import errno
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from statecraft_day_archive import (
    DEFAULT_ROOT,
    REPO_ROOT,
    DaySummary,
    collect_archive_file,
    fmt_counter,
    iter_day_dirs,
    iter_source_files,
    summarize_day_dir,
)

ROUTING_REGISTRY_PATH = REPO_ROOT / "statecraft" / "data" / "month-maturity-routing-registry.json"
ROUTING_METADATA_PATH = REPO_ROOT / "statecraft" / "data" / "month-routing-metadata.json"
REGISTRY_NOTE_DIR = REPO_ROOT / "statecraft" / "notes"
MONTH_NAME_MAP = {
    "01": "january",
    "02": "february",
    "03": "march",
    "04": "april",
    "05": "may",
    "06": "june",
    "07": "july",
    "08": "august",
    "09": "september",
    "10": "october",
    "11": "november",
    "12": "december",
}
ROUTE_CLASS_BENCHMARK = "benchmark"
ROUTE_CLASS_WATCHLIST = "watchlist"
ROUTE_CLASS_CLOSURE_AUDIT = "closure-audit"

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

def month_note_slug(month: str) -> str:
    year, month_num = month.split("-")
    month_name = MONTH_NAME_MAP.get(month_num, month_num)
    return f"{month_name}-{year}"

def iter_month_records(day_dirs: list[Path]) -> list:
    records = []
    for day_dir in day_dirs:
        for path in iter_source_files(day_dir):
            records.append(collect_archive_file(path))
    return records

def guess_month_note_surfaces(month: str) -> list[str]:
    slug = month_note_slug(month)
    surfaces = []
    if not REGISTRY_NOTE_DIR.exists():
        return surfaces
    for path in sorted(REGISTRY_NOTE_DIR.glob(f"*{slug}*.md")):
        surfaces.append(path.as_posix().split("/", 3)[-1])
    return surfaces

def surname_signature(label: str) -> str:
    tokens = re.findall(r"[a-z0-9]+", label.lower())
    return tokens[-1] if tokens else ""

def looks_like_person_label(label: str) -> bool:
    if any(sep in label for sep in ("&", ";", "|", "/", ":")):
        return False
    tokens = re.findall(r"[A-Za-z0-9]+", label)
    if not (1 <= len(tokens) <= 4):
        return False
    lowered = [token.lower() for token in tokens]
    banned = {
        "breaking",
        "live",
        "update",
        "war",
        "showdown",
        "offensive",
        "peace",
        "talks",
        "ceasefire",
        "the",
        "and",
        "with",
        "w",
        "vs",
        "v",
        "on",
        "in",
        "at",
        "for",
        "its",
        "over",
        "from",
        "just",
        "now",
        "new",
        "full",
    }
    return not any(token in banned for token in lowered)

def build_guest_label_variants(records: list) -> list[dict[str, object]]:
    buckets: dict[str, Counter[str]] = defaultdict(Counter)
    for record in records:
        for label in record.guest_values:
            if not looks_like_person_label(label):
                continue
            signature = surname_signature(label)
            if signature:
                buckets[signature][label] += 1

    variants: list[dict[str, object]] = []
    for signature, counter in sorted(buckets.items()):
        if len(counter) < 2:
            continue
        variants.append(
            {
                "signature": signature,
                "labels": [
                    {"label": label, "count": count}
                    for label, count in sorted(counter.items(), key=lambda item: (-item[1], item[0]))
                ],
            }
        )
    return variants

def load_routing_registry(path: Path = ROUTING_REGISTRY_PATH) -> dict[str, dict[str, object]]:
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    months = payload.get("months", [])
    out: dict[str, dict[str, object]] = {}
    for entry in months:
        month = entry.get("month")
        if isinstance(month, str):
            out[month] = entry
    return out

def build_month_metadata(all_groups: dict[str, list[Path]], routing_registry: dict[str, dict[str, object]]) -> dict[str, object]:
    months: dict[str, object] = {}
    for month, day_dirs in sorted(all_groups.items()):
        day_summaries = [summarize_day_dir(day_dir) for day_dir in day_dirs]
        records = iter_month_records(day_dirs)
        source_total = sum(day.source_count for day in day_summaries)
        channel_counter = merge_counter(day_summaries, "channel_counter")
        host_counter = merge_counter(day_summaries, "host_counter")
        guest_counter = merge_counter(day_summaries, "guest_counter")
        thread_counter = merge_counter(day_summaries, "thread_counter")
        registry_entry = routing_registry.get(month, {})
        existing_month_surfaces = registry_entry.get("primary_surfaces") or guess_month_note_surfaces(month)
        route_class = registry_entry.get("route_class")
        months[month] = {
            "captured_days": len(day_summaries),
            "source_count": source_total,
            "thread_count": len(thread_counter),
            "channel_or_show_count": len(channel_counter),
            "host_count": len(host_counter),
            "guest_count": len(guest_counter),
            "guest_label_variants": build_guest_label_variants(records),
            "existing_month_surface_count": len(existing_month_surfaces),
            "existing_month_surfaces": existing_month_surfaces,
            "is_dense_month": len(day_summaries) >= 20 or source_total >= 75,
            "has_finite_queue": bool(registry_entry.get("has_finite_queue", False)),
            "has_existing_benchmark_surfaces": route_class == ROUTE_CLASS_BENCHMARK,
            "needs_label_normalization": bool(build_guest_label_variants(records)),
        }

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "generated_by": "scripts/build_statecraft_month_indices.py",
        "registry_path": ROUTING_REGISTRY_PATH.as_posix().split("/", 3)[-1],
        "months": months,
    }

def write_json_payload(path: Path, payload: dict[str, object], *, check: bool = False) -> tuple[Path, bool]:
    rendered = json.dumps(payload, indent=2, ensure_ascii=True) + "\n"
    existing = path.read_text(encoding="utf-8") if path.exists() else None
    changed = existing != rendered
    if changed and not check:
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            path.write_text(rendered, encoding="utf-8", newline="\n")
        except PermissionError as exc:
            if exc.errno == errno.EACCES:
                raise PermissionError(
                    f"permission denied writing {path}; rerun with --check first to detect stale routing metadata, "
                    "then rerun the write in an unsandboxed shell"
                ) from exc
            raise
    return path, changed

def build_month_readme(root: Path, month: str, day_dirs: list[Path]) -> str:
    day_summaries = [summarize_day_dir(day_dir) for day_dir in day_dirs]
    source_total = sum(day.source_count for day in day_summaries)
    kind_counter = merge_counter(day_summaries, "kind_counter")
    source_form_counter = merge_counter(day_summaries, "source_form_counter")
    channel_counter = merge_counter(day_summaries, "channel_counter")
    host_counter = merge_counter(day_summaries, "host_counter")
    guest_counter = merge_counter(day_summaries, "guest_counter")
    thread_counter = merge_counter(day_summaries, "thread_counter")

    lines = [
        f"# Statecraft Archive - {month}",
        "",
        "_Generated inventory note. Rebuild with `python scripts/build_statecraft_month_indices.py` or `python scripts/refresh_statecraft_archive_indices.py`._",
        "",
        "_Month archive rollup — drill down via each day README **Ingest register**._",
        "",
        "## Stats",
        "",
        f"- Captured days: `{len(day_summaries)}`",
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
        "## Days",
        "",
        "| Day | Files | Top channels/shows | Top threads | Day index |",
        "| --- | ---: | --- | --- | --- |",
    ]

    for day_dir, summary in zip(day_dirs, day_summaries, strict=True):
        day_name = day_dir.name
        index_rel = f"./{day_name}/day-index.md"
        lines.append(
            f"| `{day_name}` | {summary.source_count} | "
            f"{top_counter_text(summary.channel_counter)} | "
            f"{top_counter_text(summary.thread_counter)} | "
            f"[open]({index_rel}) |"
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
    ap.add_argument(
        "--metadata-out",
        type=Path,
        default=ROUTING_METADATA_PATH,
        help="Path for generated month routing metadata JSON.",
    )
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
        routing_registry = load_routing_registry()
        if args.year == "all":
            all_metadata_groups: dict[str, list[Path]] = {}
            years = sorted({p.name[:4] for p in root.iterdir() if p.is_dir() and len(p.name) >= 10 and p.name[4] == "-"})
            for year in years:
                all_metadata_groups.update(group_day_dirs_by_month(root, year))
        else:
            all_metadata_groups = group_day_dirs_by_month(root, target_year)
        metadata_payload = build_month_metadata(all_metadata_groups, routing_registry)
        metadata_path, metadata_changed = write_json_payload(args.metadata_out, metadata_payload, check=args.check)
        if args.check:
            print(f"{'stale' if changed else 'ok'} {out_path}")
            print(f"{'stale' if metadata_changed else 'ok'} {metadata_path}")
            return 1 if changed or metadata_changed else 0
        print(f"{'wrote' if changed else 'unchanged'} {out_path}")
        print(f"{'wrote' if metadata_changed else 'unchanged'} {metadata_path}")
        return 0

    if args.year == "all":
        years = sorted({p.name[:4] for p in root.iterdir() if p.is_dir() and len(p.name) >= 10 and p.name[4] == "-"})
        for year in years:
            all_groups.update(group_day_dirs_by_month(root, year))
    else:
        all_groups = group_day_dirs_by_month(root, args.year)

    changed_paths: list[Path] = []
    routing_registry = load_routing_registry()
    for month, day_dirs in all_groups.items():
        out_path, changed = write_month_index(root, month, day_dirs, check=args.check)
        if changed:
            changed_paths.append(out_path)
            if args.check:
                print(f"stale {out_path}")
    metadata_payload = build_month_metadata(all_groups, routing_registry)
    metadata_path, metadata_changed = write_json_payload(args.metadata_out, metadata_payload, check=args.check)
    if args.check:
        if metadata_changed:
            print(f"stale {metadata_path}")
        if not changed_paths:
            print(f"{'ok' if not metadata_changed else 'stale'} 0 month indices under {root}")
            return 1 if metadata_changed else 0
        print(f"stale {len(changed_paths)} month indices under {root}")
        return 1
    if not changed_paths:
        print(f"unchanged 0 month indices under {root}")
        print(f"{'wrote' if metadata_changed else 'unchanged'} {metadata_path}")
        return 0
    print(f"wrote {len(changed_paths)} month indices under {root}")
    print(f"{'wrote' if metadata_changed else 'unchanged'} {metadata_path}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
