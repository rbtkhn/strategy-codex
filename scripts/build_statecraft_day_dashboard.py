#!/usr/bin/env python3
"""Build an aggregate statecraft day dashboard from day indices."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from statecraft_day_archive import (
    DEFAULT_ROOT,
    DaySummary,
    counter_to_list,
    fmt_counter,
    iter_day_dirs,
    parse_day_readme,
    summarize_day_dir,
)


REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = REPO_ROOT / "artifacts" / "statecraft"
OUT_MD = OUT_DIR / "day-dashboard.md"
OUT_JSON = OUT_DIR / "day-dashboard.json"
SCHEMA_VERSION = "1.0.0-statecraft-day-dashboard"


@dataclass(frozen=True)
class DashboardArgs:
    root: Path
    year: str | None
    from_day: str | None
    to_day: str | None


def parse_args() -> DashboardArgs:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="Statecraft source-archive root.")
    ap.add_argument("--year", type=str, default=None, help="Only include YYYY day folders for this year.")
    ap.add_argument("--from", dest="from_day", type=str, default=None, help="Lower date bound YYYY-MM-DD.")
    ap.add_argument("--to", dest="to_day", type=str, default=None, help="Upper date bound YYYY-MM-DD.")
    args = ap.parse_args()
    return DashboardArgs(
        root=args.root.resolve(),
        year=args.year,
        from_day=args.from_day,
        to_day=args.to_day,
    )


def _all_day_dirs(root: Path) -> list[Path]:
    day_dirs: list[Path] = []
    for year_dir in sorted(path for path in root.iterdir() if path.is_dir()):
        name = year_dir.name
        if len(name) == 10 and name[4] == "-" and name[7] == "-":
            day_dirs.append(year_dir)
    return sorted(day_dirs, key=lambda path: path.name)


def _select_day_dirs(root: Path, year: str | None, from_day: str | None, to_day: str | None) -> list[Path]:
    if year:
        day_dirs = iter_day_dirs(root, year)
    else:
        day_dirs = _all_day_dirs(root)
    if from_day:
        day_dirs = [path for path in day_dirs if path.name >= from_day]
    if to_day:
        day_dirs = [path for path in day_dirs if path.name <= to_day]
    return day_dirs


def load_day_summary(day_dir: Path) -> DaySummary:
    parsed = parse_day_readme(day_dir)
    if parsed is not None:
        return parsed
    return summarize_day_dir(day_dir, has_readme=(day_dir / "README.md").is_file(), readme_parse_ok=False)


def _merge_counter(days: list[DaySummary], attr: str) -> Counter[str]:
    counter: Counter[str] = Counter()
    for day in days:
        counter.update(getattr(day, attr))
    return counter


def _top_names(counter: Counter[str], limit: int = 3) -> str:
    if not counter:
        return "(none)"
    return ", ".join(name for name, _ in sorted(counter.items(), key=lambda item: (-item[1], item[0]))[:limit])


def _format_day_link(root: Path, date: str) -> str:
    readme_path = (root / date / "README.md").resolve()
    return f"[{date}]({readme_path.as_posix()})"


def build_dashboard_payload(root: Path, days: list[DaySummary]) -> dict:
    total_sources = sum(day.source_count for day in days)
    aggregate_channels = _merge_counter(days, "channel_counter")
    aggregate_hosts = _merge_counter(days, "host_counter")
    aggregate_guests = _merge_counter(days, "guest_counter")
    aggregate_threads = _merge_counter(days, "thread_counter")
    aggregate_fallbacks = _merge_counter(days, "fallback_counter")

    top_days = sorted(days, key=lambda day: (-day.source_count, day.date))[:10]
    quiet_days = [day for day in days if day.source_count <= 2][:10]
    fallback_heavy = sorted(
        [day for day in days if sum(day.fallback_counter.values()) > 0],
        key=lambda day: (-sum(day.fallback_counter.values()), day.date),
    )[:10]
    missing_hosts_or_guests = [
        day
        for day in days
        if not day.host_counter or not day.guest_counter
    ][:10]
    missing_readmes = [day for day in days if not day.has_readme][:10]

    return {
        "schemaVersion": SCHEMA_VERSION,
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "root": str(root),
        "coverage": {
            "dayCount": len(days),
            "sourceFileCount": total_sources,
            "firstDay": days[0].date if days else None,
            "lastDay": days[-1].date if days else None,
        },
        "aggregates": {
            "topDays": [
                {"date": day.date, "sourceCount": day.source_count}
                for day in top_days
            ],
            "quietDays": [
                {"date": day.date, "sourceCount": day.source_count}
                for day in quiet_days
            ],
            "channels": counter_to_list(aggregate_channels),
            "hosts": counter_to_list(aggregate_hosts),
            "guests": counter_to_list(aggregate_guests),
            "threads": counter_to_list(aggregate_threads),
            "fallbackFamilies": counter_to_list(aggregate_fallbacks),
        },
        "anomalies": {
            "fallbackHeavyDays": [
                {"date": day.date, "fallbackCount": sum(day.fallback_counter.values())}
                for day in fallback_heavy
            ],
            "missingHostOrGuestDays": [
                {
                    "date": day.date,
                    "hasHosts": bool(day.host_counter),
                    "hasGuests": bool(day.guest_counter),
                }
                for day in missing_hosts_or_guests
            ],
            "missingReadmes": [day.date for day in missing_readmes],
        },
        "days": [
            {
                "date": day.date,
                "fileCount": day.source_count,
                "channels": counter_to_list(day.channel_counter),
                "shows": counter_to_list(day.channel_counter),
                "hosts": counter_to_list(day.host_counter),
                "guests": counter_to_list(day.guest_counter),
                "threads": counter_to_list(day.thread_counter),
                "fallbackFamilies": counter_to_list(day.fallback_counter),
                "fileNames": list(day.file_names),
                "hasReadme": day.has_readme,
                "readmeParseOk": day.readme_parse_ok,
            }
            for day in days
        ],
    }


def _render_counter_table(counter: Counter[str], header: str, limit: int = 10) -> list[str]:
    rows = sorted(counter.items(), key=lambda item: (-item[1], item[0]))[:limit]
    lines = [f"## {header}", "", "| Name | Count |", "| --- | ---: |"]
    for name, count in rows:
        lines.append(f"| `{name}` | {count} |")
    if not rows:
        lines.append("| `(none)` | 0 |")
    lines.append("")
    return lines


def render_dashboard_markdown(root: Path, payload: dict) -> str:
    coverage = payload["coverage"]
    aggregate_channels = Counter({item["name"]: item["count"] for item in payload["aggregates"]["channels"]})
    aggregate_hosts = Counter({item["name"]: item["count"] for item in payload["aggregates"]["hosts"]})
    aggregate_guests = Counter({item["name"]: item["count"] for item in payload["aggregates"]["guests"]})
    aggregate_threads = Counter({item["name"]: item["count"] for item in payload["aggregates"]["threads"]})

    lines = [
        "# Statecraft Day Dashboard",
        "",
        "_Generated observability artifact. Rebuild with `python scripts/build_statecraft_day_dashboard.py`._",
        "",
        f"- Generated: `{payload['generatedAt']}`",
        f"- Root: `{payload['root']}`",
        f"- Indexed days: `{coverage['dayCount']}`",
        f"- Source files: `{coverage['sourceFileCount']}`",
        f"- Covered span: `{coverage['firstDay']}` to `{coverage['lastDay']}`",
        "",
        "## Heaviest Days",
        "",
        "| Day | Source files |",
        "| --- | ---: |",
    ]
    for item in payload["aggregates"]["topDays"]:
        lines.append(f"| {_format_day_link(root, item['date'])} | {item['sourceCount']} |")
    if not payload["aggregates"]["topDays"]:
        lines.append("| `(none)` | 0 |")
    lines.extend(
        [
            "",
            "## Quiet Days (1-2 files)",
            "",
            "| Day | Source files |",
            "| --- | ---: |",
        ]
    )
    for item in payload["aggregates"]["quietDays"]:
        lines.append(f"| {_format_day_link(root, item['date'])} | {item['sourceCount']} |")
    if not payload["aggregates"]["quietDays"]:
        lines.append("| `(none)` | 0 |")
    lines.append("")
    lines.extend(_render_counter_table(aggregate_channels, "Channel / Show Leaderboard"))
    lines.extend(_render_counter_table(aggregate_hosts, "Host Leaderboard"))
    lines.extend(_render_counter_table(aggregate_guests, "Guest Leaderboard"))
    lines.extend(_render_counter_table(aggregate_threads, "Thread Leaderboard"))

    lines.extend(
        [
            "## Anomalies / Gaps",
            "",
            f"- Fallback-heavy days: {fmt_counter(Counter({item['date']: item['fallbackCount'] for item in payload['anomalies']['fallbackHeavyDays']}))}",
            f"- Missing host or guest coverage: {fmt_counter(Counter({item['date']: 1 for item in payload['anomalies']['missingHostOrGuestDays']}))}",
            f"- Missing local READMEs: {fmt_counter(Counter({date: 1 for date in payload['anomalies']['missingReadmes']}))}",
            "",
            "## Day Ledger",
            "",
            "| Day | Files | Top channels/shows | Threads | Fallback families | README |",
            "| --- | ---: | --- | ---: | ---: | --- |",
        ]
    )
    for day in payload["days"]:
        lines.append(
            "| "
            f"{_format_day_link(root, day['date'])} | "
            f"{day['fileCount']} | "
            f"{_top_names(Counter({item['name']: item['count'] for item in day['channels']}))} | "
            f"{len(day['threads'])} | "
            f"{sum(item['count'] for item in day['fallbackFamilies'])} | "
            f"{'yes' if day['hasReadme'] else 'no'} |"
        )
    if not payload["days"]:
        lines.append("| `(none)` | 0 | `(none)` | 0 | 0 | no |")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    day_dirs = _select_day_dirs(args.root, args.year, args.from_day, args.to_day)
    day_summaries = [load_day_summary(day_dir) for day_dir in day_dirs]
    payload = build_dashboard_payload(args.root, day_summaries)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8", newline="\n")
    OUT_MD.write_text(render_dashboard_markdown(args.root, payload), encoding="utf-8", newline="\n")
    print(f"wrote {OUT_MD}")
    print(f"wrote {OUT_JSON}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
