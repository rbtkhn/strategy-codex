#!/usr/bin/env python3
"""Shared helpers for statecraft day archive indexing and dashboards."""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ROOT = REPO_ROOT / "source-archive" / "statecraft"
DEFAULT_YEAR = "2026"
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", re.DOTALL)
HONORIFIC_RE = re.compile(
    r"^(?:judge|amb\.?|ambassador|col\.?|colonel|lt\.?\s*col\.?|lt\.?\s*colonel|"
    r"prof\.?|professor|cpt\.?)\s+",
    re.IGNORECASE,
)

# Longest-first so more specific families win.
KNOWN_FAMILY_PREFIXES = (
    "youtube-daniel-davis-deep-dive-",
    "youtube-alex-mercouris-",
    "youtube-glenn-diesen-",
    "youtube-dialogue-works-",
    "transcript-napolitano-",
    "transcript-alkorshid-",
    "transcript-duran-",
    "transcript-wilkerson-judging-freedom-",
    "judging-freedom-",
    "youtube-hoh-dialogue-works-",
    "youtube-blumenthal-judging-freedom-",
    "substack-",
    "transcript-",
    "youtube-",
)


@dataclass(frozen=True)
class ArchiveFile:
    path: Path
    name: str
    title: str
    show: str
    host_values: tuple[str, ...]
    guest_values: tuple[str, ...]
    thread_values: tuple[str, ...]
    channel_values: tuple[str, ...]
    source_type: str
    type_label: str
    fallback_family: str
    has_frontmatter: bool


@dataclass(frozen=True)
class DaySummary:
    date: str
    source_count: int
    type_counter: Counter[str]
    channel_counter: Counter[str]
    host_counter: Counter[str]
    guest_counter: Counter[str]
    thread_counter: Counter[str]
    fallback_counter: Counter[str]
    file_names: tuple[str, ...]
    has_readme: bool = False
    readme_parse_ok: bool = False


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def parse_frontmatter(path: Path) -> dict[str, Any]:
    text = read_text(path)
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    return parse_simple_frontmatter_block(match.group(1))


def parse_simple_frontmatter_block(block: str) -> dict[str, Any]:
    """Parse the narrow YAML subset used by source-archive frontmatter."""
    data: dict[str, Any] = {}
    current_list_key: str | None = None
    for raw_line in block.splitlines():
        line = raw_line.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        list_match = re.match(r"^\s*-\s*(.+?)\s*$", line)
        if list_match and current_list_key:
            data.setdefault(current_list_key, [])
            data[current_list_key].append(parse_scalar(list_match.group(1)))
            continue
        current_list_key = None
        field_match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):(?:\s*(.*))?$", line)
        if not field_match:
            continue
        key = field_match.group(1)
        raw_value = field_match.group(2) or ""
        if raw_value == "":
            data[key] = []
            current_list_key = key
            continue
        data[key] = parse_scalar(raw_value)
    return data


def parse_scalar(raw: str) -> str:
    text = raw.strip()
    if len(text) >= 2 and text[0] == text[-1] and text[0] in {'"', "'"}:
        return text[1:-1]
    return text


def norm_scalar(value: Any) -> str:
    return " ".join(str(value or "").split()).strip()


def as_values(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, (list, tuple)):
        out: list[str] = []
        for item in value:
            text = norm_scalar(item)
            if text and text not in out:
                out.append(text)
        return tuple(out)
    text = norm_scalar(value)
    return (text,) if text else ()


def normalize_person_label(value: str) -> str:
    text = norm_scalar(value)
    while True:
        updated = HONORIFIC_RE.sub("", text).strip()
        if updated == text:
            break
        text = updated
    return text


def normalize_channel_label(value: str) -> str:
    text = norm_scalar(value)
    if "-" in text and " " not in text and text.lower() == text:
        return text.replace("-", " ").title()
    return text


def type_label(name: str) -> str:
    stem = name[:-3] if name.endswith(".md") else name
    return stem.split("-", 1)[0] if "-" in stem else stem


def infer_family_label(name: str) -> str:
    stem = name[:-3] if name.endswith(".md") else name
    stem = re.sub(r"-\d{4}-\d{2}-\d{2}$", "", stem)
    for prefix in KNOWN_FAMILY_PREFIXES:
        if stem.startswith(prefix):
            return f"{prefix}*"
    if "-" not in stem:
        return stem
    head = stem.split("-")
    return "-".join(head[:2]) + "-*"


def collect_archive_file(path: Path) -> ArchiveFile:
    meta = parse_frontmatter(path)
    host_values = tuple(
        filter(
            None,
            (
                normalize_person_label(v)
                for v in (as_values(meta.get("host")) or as_values(meta.get("hosts")))
            ),
        )
    )
    guest_values = (
        as_values(meta.get("guest"))
        or as_values(meta.get("guests"))
        or as_values(meta.get("speaker"))
        or as_values(meta.get("speakers"))
        or as_values(meta.get("participants"))
    )
    guest_values = tuple(filter(None, (normalize_person_label(v) for v in guest_values)))
    channel_values = (
        as_values(meta.get("show"))
        or as_values(meta.get("channel_slug"))
        or as_values(meta.get("publication"))
    )
    channel_values = tuple(filter(None, (normalize_channel_label(v) for v in channel_values)))
    thread_values = as_values(meta.get("thread")) or as_values(meta.get("threads"))
    return ArchiveFile(
        path=path,
        name=path.name,
        title=norm_scalar(meta.get("title")),
        show=norm_scalar(meta.get("show")),
        host_values=host_values,
        guest_values=guest_values,
        thread_values=thread_values,
        channel_values=channel_values,
        source_type=norm_scalar(meta.get("source_type")),
        type_label=type_label(path.name),
        fallback_family=infer_family_label(path.name),
        has_frontmatter=bool(meta),
    )


def iter_source_files(day_dir: Path) -> list[Path]:
    return sorted(
        [path for path in day_dir.glob("*.md") if path.name != "README.md"],
        key=lambda path: path.name,
    )


def rollup_values(records: list[ArchiveFile], attr: str) -> Counter[str]:
    counter: Counter[str] = Counter()
    for record in records:
        for value in getattr(record, attr):
            counter[value] += 1
    return counter


def fallback_counter(records: list[ArchiveFile]) -> Counter[str]:
    counter: Counter[str] = Counter()
    for record in records:
        if record.channel_values and record.host_values and record.guest_values and record.thread_values:
            continue
        counter[record.fallback_family] += 1
    return counter


def summarize_records(date: str, records: list[ArchiveFile], *, has_readme: bool = False, readme_parse_ok: bool = False) -> DaySummary:
    return DaySummary(
        date=date,
        source_count=len(records),
        type_counter=Counter(record.type_label for record in records),
        channel_counter=rollup_values(records, "channel_values"),
        host_counter=rollup_values(records, "host_values"),
        guest_counter=rollup_values(records, "guest_values"),
        thread_counter=rollup_values(records, "thread_values"),
        fallback_counter=fallback_counter(records),
        file_names=tuple(record.name for record in records),
        has_readme=has_readme,
        readme_parse_ok=readme_parse_ok,
    )


def summarize_day_dir(day_dir: Path, *, has_readme: bool | None = None, readme_parse_ok: bool = False) -> DaySummary:
    records = [collect_archive_file(path) for path in iter_source_files(day_dir)]
    return summarize_records(
        day_dir.name,
        records,
        has_readme=(day_dir / "README.md").is_file() if has_readme is None else has_readme,
        readme_parse_ok=readme_parse_ok,
    )


def fmt_counter(counter: Counter[str]) -> str:
    if not counter:
        return "(none)"
    parts = [
        f"`{name}` ({count})"
        for name, count in sorted(counter.items(), key=lambda item: (-item[1], item[0]))
    ]
    return ", ".join(parts)


def counter_to_list(counter: Counter[str]) -> list[dict[str, int | str]]:
    return [
        {"name": name, "count": count}
        for name, count in sorted(counter.items(), key=lambda item: (-item[1], item[0]))
    ]


def build_day_readme(day_dir: Path) -> str:
    summary = summarize_day_dir(day_dir)
    stats = [
        f"- Source files: `{summary.source_count}`",
        f"- Type mix: {fmt_counter(summary.type_counter)}",
        f"- Distinct channels/shows: `{len(summary.channel_counter)}`",
        f"- Distinct hosts: `{len(summary.host_counter)}`",
        f"- Distinct guests: `{len(summary.guest_counter)}`",
        f"- Distinct threads: `{len(summary.thread_counter)}`",
    ]

    lines = [
        f"# Statecraft Archive - {day_dir.name}",
        "",
        "_Generated inventory note. Rebuild with `python scripts/build_statecraft_day_indices.py`._",
        "",
        "## Stats",
        "",
        *stats,
        "",
        "## Channel / Show Rollup",
        "",
        f"- {fmt_counter(summary.channel_counter)}",
        "",
        "## Host / Guest / Thread Rollup",
        "",
        f"- Hosts: {fmt_counter(summary.host_counter)}",
        f"- Guests: {fmt_counter(summary.guest_counter)}",
        f"- Threads: {fmt_counter(summary.thread_counter)}",
        "",
        "## Filename Family Fallbacks",
        "",
        f"- {fmt_counter(summary.fallback_counter)}",
        "",
        "## Files",
        "",
    ]
    lines.extend(f"- `{name}`" for name in summary.file_names)
    lines.append("")
    return "\n".join(lines)


def iter_day_dirs(root: Path, year: str) -> list[Path]:
    return sorted(
        [
            path
            for path in root.iterdir()
            if path.is_dir() and re.fullmatch(rf"{re.escape(year)}-\d{{2}}-\d{{2}}", path.name)
        ],
        key=lambda path: path.name,
    )


def parse_counter_text(text: str) -> Counter[str]:
    counter: Counter[str] = Counter()
    stripped = text.strip()
    if not stripped or stripped == "(none)":
        return counter
    for name, count in re.findall(r"`([^`]+)` \((\d+)\)", stripped):
        counter[name] = int(count)
    return counter


def _extract_section_block(text: str, heading: str) -> str | None:
    match = re.search(
        rf"^## {re.escape(heading)}\s*$\n(.*?)(?=^## |\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if not match:
        return None
    return match.group(1).strip()


def parse_day_readme(day_dir: Path) -> DaySummary | None:
    readme_path = day_dir / "README.md"
    if not readme_path.is_file():
        return None
    text = readme_path.read_text(encoding="utf-8", errors="replace")

    title_match = re.search(r"^# Statecraft Archive - (\d{4}-\d{2}-\d{2})$", text, re.MULTILINE)
    source_match = re.search(r"^- Source files: `(\d+)`$", text, re.MULTILINE)
    type_match = re.search(r"^- Type mix: (.+)$", text, re.MULTILINE)
    channel_block = _extract_section_block(text, "Channel / Show Rollup")
    hgt_block = _extract_section_block(text, "Host / Guest / Thread Rollup")
    fallback_block = _extract_section_block(text, "Filename Family Fallbacks")
    files_block = _extract_section_block(text, "Files")
    if not (title_match and source_match and type_match and channel_block and hgt_block and fallback_block and files_block):
        return None
    channel_match = re.search(r"^- (.+)$", channel_block, re.MULTILINE)
    host_match = re.search(r"^- Hosts: (.+)$", hgt_block, re.MULTILINE)
    guest_match = re.search(r"^- Guests: (.+)$", hgt_block, re.MULTILINE)
    thread_match = re.search(r"^- Threads: (.+)$", hgt_block, re.MULTILINE)
    fallback_match = re.search(r"^- (.+)$", fallback_block, re.MULTILINE)
    if not (channel_match and host_match and guest_match and thread_match and fallback_match):
        return None
    files = tuple(re.findall(r"^- `([^`]+\.md)`$", files_block, re.MULTILINE))

    return DaySummary(
        date=title_match.group(1),
        source_count=int(source_match.group(1)),
        type_counter=parse_counter_text(type_match.group(1)),
        channel_counter=parse_counter_text(channel_match.group(1)),
        host_counter=parse_counter_text(host_match.group(1)),
        guest_counter=parse_counter_text(guest_match.group(1)),
        thread_counter=parse_counter_text(thread_match.group(1)),
        fallback_counter=parse_counter_text(fallback_match.group(1)),
        file_names=files,
        has_readme=True,
        readme_parse_ok=True,
    )
