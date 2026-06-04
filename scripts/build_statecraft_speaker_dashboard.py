#!/usr/bin/env python3
"""Build a speaker-centric statecraft dashboard and saved guest slices."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import build_statecraft_day_dashboard as daydash
from statecraft_day_archive import (
    DEFAULT_ROOT,
    ArchiveFile,
    collect_archive_file,
    counter_to_list,
    iter_source_files,
    load_day_summary,
    select_day_dirs,
)


REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = REPO_ROOT / "artifacts" / "statecraft" / "speakers"
SLICES_DIR = OUT_DIR / "slices"
OUT_MD = OUT_DIR / "speaker-dashboard.md"
OUT_JSON = OUT_DIR / "speaker-dashboard.json"
SCHEMA_VERSION = "1.0.0-statecraft-speaker-dashboard"


@dataclass(frozen=True)
class DashboardArgs:
    root: Path
    year: str | None
    from_day: str | None
    to_day: str | None
    top_speakers: int
    top_slices: int
    skip_slices: bool


@dataclass
class SpeakerStats:
    name: str
    file_count: int = 0
    day_set: set[str] | None = None
    day_counter: Counter[str] | None = None
    host_counter: Counter[str] | None = None
    channel_counter: Counter[str] | None = None
    thread_counter: Counter[str] | None = None
    source_form_counter: Counter[str] | None = None

    def __post_init__(self) -> None:
        self.day_set = set()
        self.day_counter = Counter()
        self.host_counter = Counter()
        self.channel_counter = Counter()
        self.thread_counter = Counter()
        self.source_form_counter = Counter()

    def add(self, date: str, record: ArchiveFile) -> None:
        self.file_count += 1
        self.day_set.add(date)
        self.day_counter[date] += 1
        self.host_counter.update(record.host_values)
        self.channel_counter.update(record.channel_values)
        self.thread_counter.update(record.thread_values)
        self.source_form_counter.update((record.source_form,))


def parse_args() -> DashboardArgs:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="Statecraft source-archive root.")
    ap.add_argument("--year", type=str, default=None, help="Only include YYYY day folders for this year.")
    ap.add_argument("--from", dest="from_day", type=str, default=None, help="Lower date bound YYYY-MM-DD.")
    ap.add_argument("--to", dest="to_day", type=str, default=None, help="Upper date bound YYYY-MM-DD.")
    ap.add_argument("--top-speakers", type=int, default=25, help="How many speakers to include in the aggregate leaderboard.")
    ap.add_argument("--top-slices", type=int, default=10, help="How many top recurring guests to materialize as saved slices.")
    ap.add_argument("--skip-slices", action="store_true", help="Do not build per-speaker saved slices.")
    args = ap.parse_args()
    return DashboardArgs(
        root=args.root.resolve(),
        year=args.year,
        from_day=args.from_day,
        to_day=args.to_day,
        top_speakers=max(1, args.top_speakers),
        top_slices=max(0, args.top_slices),
        skip_slices=bool(args.skip_slices),
    )

def _select_day_dirs(root: Path, year: str | None, from_day: str | None, to_day: str | None) -> list[Path]:
    return select_day_dirs(root, year=year, from_day=from_day, to_day=to_day)


def collect_speaker_stats(day_dirs: list[Path]) -> tuple[dict[str, SpeakerStats], int]:
    stats: dict[str, SpeakerStats] = {}
    total_files = 0
    for day_dir in day_dirs:
        date = day_dir.name
        for path in iter_source_files(day_dir):
            total_files += 1
            record = collect_archive_file(path)
            for guest in record.guest_values:
                stats.setdefault(guest, SpeakerStats(name=guest)).add(date, record)
    return stats, total_files


def _sorted_speakers(stats: dict[str, SpeakerStats]) -> list[SpeakerStats]:
    return sorted(
        stats.values(),
        key=lambda item: (-item.file_count, -len(item.day_set), item.name),
    )


def _counter_top(counter: Counter[str], limit: int = 3) -> str:
    if not counter:
        return "(none)"
    return ", ".join(name for name, _ in sorted(counter.items(), key=lambda item: (-item[1], item[0]))[:limit])


def _speaker_slug(name: str) -> str:
    return daydash._normalize_slug(name)


def build_speaker_dashboard_payload(root: Path, day_dirs: list[Path], stats: dict[str, SpeakerStats], *, top_speakers: int) -> dict:
    sorted_speakers = _sorted_speakers(stats)
    top = sorted_speakers[:top_speakers]
    distinct_days = [day_dir.name for day_dir in day_dirs]
    total_guest_appearances = sum(s.file_count for s in sorted_speakers)
    return {
        "schemaVersion": SCHEMA_VERSION,
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "root": str(root),
        "coverage": {
            "dayCount": len(day_dirs),
            "sourceFileCount": sum(len(iter_source_files(day_dir)) for day_dir in day_dirs),
            "guestAppearanceCount": total_guest_appearances,
            "distinctGuestCount": len(sorted_speakers),
            "firstDay": distinct_days[0] if distinct_days else None,
            "lastDay": distinct_days[-1] if distinct_days else None,
        },
        "aggregates": {
            "topSpeakers": [
                {
                    "name": speaker.name,
                    "slug": _speaker_slug(speaker.name),
                    "fileCount": speaker.file_count,
                    "dayCount": len(speaker.day_set),
                    "topHosts": counter_to_list(speaker.host_counter),
                    "topChannels": counter_to_list(speaker.channel_counter),
                    "topThreads": counter_to_list(speaker.thread_counter),
                    "firstDay": min(speaker.day_set) if speaker.day_set else None,
                    "lastDay": max(speaker.day_set) if speaker.day_set else None,
                    "peakDay": max(
                        speaker.day_counter.items(),
                        key=lambda item: (item[1], item[0]),
                    )[0]
                    if speaker.day_counter
                    else None,
                    "peakDayCount": max(speaker.day_counter.values()) if speaker.day_counter else 0,
                }
                for speaker in top
            ]
        },
    }


def render_speaker_dashboard_markdown(payload: dict, slice_names: list[str]) -> str:
    coverage = payload["coverage"]
    top = payload["aggregates"]["topSpeakers"]
    lines = [
        "# Statecraft Speaker Dashboard",
        "",
        "_Generated observability artifact. Rebuild with `python scripts/build_statecraft_speaker_dashboard.py`._",
        "",
        f"- Generated: `{payload['generatedAt']}`",
        f"- Root: `{payload['root']}`",
        f"- Indexed days: `{coverage['dayCount']}`",
        f"- Source files: `{coverage['sourceFileCount']}`",
        f"- Guest appearances: `{coverage['guestAppearanceCount']}`",
        f"- Distinct guests: `{coverage['distinctGuestCount']}`",
        f"- Covered span: `{coverage['firstDay']}` to `{coverage['lastDay']}`",
        "",
        "## Top Guests",
        "",
        "| Guest | Files | Days | Top hosts | Top channels | Top threads | Span | Peak day |",
        "| --- | ---: | ---: | --- | --- | --- | --- | --- |",
    ]
    for speaker in top:
        lines.append(
            "| "
            f"`{speaker['name']}` | "
            f"{speaker['fileCount']} | "
            f"{speaker['dayCount']} | "
            f"{_counter_top(Counter({item['name']: item['count'] for item in speaker['topHosts']}))} | "
            f"{_counter_top(Counter({item['name']: item['count'] for item in speaker['topChannels']}))} | "
            f"{_counter_top(Counter({item['name']: item['count'] for item in speaker['topThreads']}))} | "
            f"{speaker['firstDay']} to {speaker['lastDay']} | "
            f"{speaker['peakDay']} ({speaker['peakDayCount']}) |"
        )
    if not top:
        lines.append("| `(none)` | 0 | 0 | `(none)` | `(none)` | `(none)` | `(none)` | `(none)` |")
    lines.extend(
        [
            "",
            "## Saved Speaker Slices",
            "",
            f"- {', '.join(f'`{name}`' for name in slice_names) if slice_names else '(none)'}",
            "",
        ]
    )
    return "\n".join(lines)


def build_saved_speaker_slices(root: Path, day_dirs: list[Path], speaker_names: list[str]) -> list[str]:
    if not speaker_names:
        return []
    all_day_summaries = [load_day_summary(day_dir) for day_dir in day_dirs]
    built: list[str] = []
    for speaker_name in speaker_names:
        slug = _speaker_slug(speaker_name)
        filtered = daydash.filter_day_summaries(all_day_summaries, guests=(speaker_name,))
        payload = daydash.build_dashboard_payload(root, filtered, guests=(speaker_name,), slug=slug)
        out_md = SLICES_DIR / f"{slug}.md"
        out_json = SLICES_DIR / f"{slug}.json"
        out_md.parent.mkdir(parents=True, exist_ok=True)
        payload["artifacts"] = {"markdown": str(out_md), "json": str(out_json)}
        out_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8", newline="\n")
        out_md.write_text(daydash.render_dashboard_markdown(root, payload), encoding="utf-8", newline="\n")
        built.append(slug)
    return built


def main() -> int:
    args = parse_args()
    day_dirs = _select_day_dirs(args.root, args.year, args.from_day, args.to_day)
    speaker_stats, _ = collect_speaker_stats(day_dirs)
    payload = build_speaker_dashboard_payload(args.root, day_dirs, speaker_stats, top_speakers=args.top_speakers)

    sorted_speakers = _sorted_speakers(speaker_stats)
    slice_targets = [] if args.skip_slices else [speaker.name for speaker in sorted_speakers[: args.top_slices]]
    slice_names = build_saved_speaker_slices(args.root, day_dirs, slice_targets)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    payload["artifacts"] = {"markdown": str(OUT_MD), "json": str(OUT_JSON)}
    payload["savedSlices"] = slice_names
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8", newline="\n")
    OUT_MD.write_text(render_speaker_dashboard_markdown(payload, slice_names), encoding="utf-8", newline="\n")
    print(f"wrote {OUT_MD}")
    print(f"wrote {OUT_JSON}")
    if slice_names:
        print(f"wrote {len(slice_names)} speaker slices under {SLICES_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
