#!/usr/bin/env python3
"""Shared helpers for statecraft day archive indexing and dashboards."""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import build_speaker_routing_queue as speaker_routing


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ROOT = REPO_ROOT / "source-archive" / "statecraft"
DEFAULT_YEAR = "2026"
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", re.DOTALL)
HONORIFIC_RE = re.compile(
    r"^(?:judge|amb\.?|ambassador|col\.?|colonel|lt\.?\s*col\.?|lt\.?\s*colonel|"
    r"prof\.?|professor|cpt\.?)\s+",
    re.IGNORECASE,
)

CANONICAL_SOURCE_PREFIX = "source-"


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
    source_form: str
    kind_label: str
    has_frontmatter: bool


@dataclass(frozen=True)
class DaySummary:
    date: str
    source_count: int
    kind_counter: Counter[str]
    source_form_counter: Counter[str]
    channel_counter: Counter[str]
    host_counter: Counter[str]
    guest_counter: Counter[str]
    thread_counter: Counter[str]
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


def parse_scalar(raw: str) -> Any:
    text = raw.strip()
    if text.startswith("[") and text.endswith("]"):
        inner = text[1:-1].strip()
        if not inner:
            return []
        return [parse_scalar(part) for part in inner.split(",")]
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


def guest_meta_values(meta: dict[str, Any]) -> tuple[str, ...]:
    out: list[str] = []
    for key in ("guest", "guests", "speaker", "speakers", "participants"):
        raw_values = list(as_values(meta.get(key)))
        expanded_values: list[str] = []
        for value in raw_values:
            if key in {"speakers", "participants"} and "," in value:
                expanded_values.extend(part.strip() for part in value.split(","))
            else:
                expanded_values.append(value)
        for value in expanded_values:
            normalized = normalize_person_label(value)
            if normalized and normalized not in out:
                out.append(normalized)
    for key, raw_value in meta.items():
        if not re.fullmatch(r"guest_\d+", str(key)):
            continue
        for value in as_values(raw_value):
            normalized = normalize_person_label(value)
            if normalized and normalized not in out:
                out.append(normalized)
    return tuple(out)


@lru_cache(maxsize=1)
def _speaker_inventory() -> speaker_routing.SpeakerInventory:
    return speaker_routing._discover_inventory(speaker_routing.DEFAULT_SPEAKERS_DIR, DEFAULT_ROOT)  # noqa: SLF001


def explicit_thread_values(meta: dict[str, Any]) -> tuple[str, ...]:
    out: list[str] = []
    for value in as_values(meta.get("thread")) + as_values(meta.get("threads")):
        normalized = norm_scalar(value)
        if normalized and normalized not in out:
            out.append(normalized)
    for key, raw_value in meta.items():
        if not re.fullmatch(r"thread_\d+", str(key)):
            continue
        for value in as_values(raw_value):
            normalized = norm_scalar(value)
            if normalized and normalized not in out:
                out.append(normalized)
    return tuple(out)


def derive_thread_values(meta: dict[str, Any], guest_values: tuple[str, ...]) -> tuple[str, ...]:
    out = list(explicit_thread_values(meta))

    inventory = _speaker_inventory()

    host_slug = speaker_routing._canonical_host_slug(meta)  # noqa: SLF001
    if host_slug and host_slug in inventory.speaker_folders and host_slug not in out:
        out.append(host_slug)

    for guest in guest_values:
        guest_slug = speaker_routing._match_speaker(guest, inventory)  # noqa: SLF001
        if guest_slug and guest_slug not in out:
            out.append(guest_slug)

    return tuple(out)


def type_label(name: str) -> str:
    stem = name[:-3] if name.endswith(".md") else name
    return stem.split("-", 1)[0] if "-" in stem else stem


def infer_source_form(meta: dict[str, Any], host_values: tuple[str, ...], guest_values: tuple[str, ...]) -> str:
    explicit = norm_scalar(meta.get("source_form"))
    if explicit:
        return explicit

    source_url = norm_scalar(meta.get("source_url")).casefold()
    publication = norm_scalar(meta.get("publication")).casefold()
    kind = norm_scalar(meta.get("kind")).casefold()
    source_type = norm_scalar(meta.get("source_type")).casefold()

    if "substack.com" in source_url or publication.endswith("substack.com") or kind == "substack-post":
        return "newsletter"
    if kind in {"article", "web-page"} or source_type == "web-transcript-derived-summary":
        return "article"
    if len(guest_values) >= 2:
        return "panel"
    if len(guest_values) == 1:
        return "interview"
    if host_values or norm_scalar(meta.get("show")) or source_url:
        return "solo"
    return "post"


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
    guest_values = guest_meta_values(meta)
    channel_values = (
        as_values(meta.get("show"))
        or as_values(meta.get("channel_slug"))
        or as_values(meta.get("publication"))
    )
    channel_values = tuple(filter(None, (normalize_channel_label(v) for v in channel_values)))
    thread_values = derive_thread_values(meta, guest_values)
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
        source_form=infer_source_form(meta, host_values, guest_values),
        kind_label=norm_scalar(meta.get("kind")) or type_label(path.name),
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


def summarize_records(date: str, records: list[ArchiveFile], *, has_readme: bool = False, readme_parse_ok: bool = False) -> DaySummary:
    return DaySummary(
        date=date,
        source_count=len(records),
        kind_counter=Counter(record.kind_label for record in records),
        source_form_counter=Counter(record.source_form for record in records),
        channel_counter=rollup_values(records, "channel_values"),
        host_counter=rollup_values(records, "host_values"),
        guest_counter=rollup_values(records, "guest_values"),
        thread_counter=rollup_values(records, "thread_values"),
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


def iter_all_day_dirs(root: Path) -> list[Path]:
    return sorted(
        [
            path
            for path in root.iterdir()
            if path.is_dir() and len(path.name) == 10 and path.name[4] == "-" and path.name[7] == "-"
        ],
        key=lambda path: path.name,
    )


def select_day_dirs(
    root: Path,
    year: str | None = None,
    from_day: str | None = None,
    to_day: str | None = None,
) -> list[Path]:
    day_dirs = iter_day_dirs(root, year) if year else iter_all_day_dirs(root)
    if from_day:
        day_dirs = [path for path in day_dirs if path.name >= from_day]
    if to_day:
        day_dirs = [path for path in day_dirs if path.name <= to_day]
    return day_dirs


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
        f"- Body kind mix: {fmt_counter(summary.kind_counter)}",
        f"- Source form mix: {fmt_counter(summary.source_form_counter)}",
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
    kind_match = re.search(r"^- Body kind mix: (.+)$", text, re.MULTILINE)
    source_form_match = re.search(r"^- Source form mix: (.+)$", text, re.MULTILINE)
    legacy_type_match = re.search(r"^- Type mix: (.+)$", text, re.MULTILINE)
    channel_block = _extract_section_block(text, "Channel / Show Rollup")
    hgt_block = _extract_section_block(text, "Host / Guest / Thread Rollup")
    files_block = _extract_section_block(text, "Files")
    if not (title_match and source_match and channel_block and hgt_block and files_block):
        return None
    channel_match = re.search(r"^- (.+)$", channel_block, re.MULTILINE)
    host_match = re.search(r"^- Hosts: (.+)$", hgt_block, re.MULTILINE)
    guest_match = re.search(r"^- Guests: (.+)$", hgt_block, re.MULTILINE)
    thread_match = re.search(r"^- Threads: (.+)$", hgt_block, re.MULTILINE)
    if not (channel_match and host_match and guest_match and thread_match):
        return None
    files = tuple(re.findall(r"^- `([^`]+\.md)`$", files_block, re.MULTILINE))

    return DaySummary(
        date=title_match.group(1),
        source_count=int(source_match.group(1)),
        kind_counter=parse_counter_text(kind_match.group(1)) if kind_match else Counter(),
        source_form_counter=parse_counter_text(source_form_match.group(1)) if source_form_match else parse_counter_text(legacy_type_match.group(1)) if legacy_type_match else Counter(),
        channel_counter=parse_counter_text(channel_match.group(1)),
        host_counter=parse_counter_text(host_match.group(1)),
        guest_counter=parse_counter_text(guest_match.group(1)),
        thread_counter=parse_counter_text(thread_match.group(1)),
        file_names=files,
        has_readme=True,
        readme_parse_ok=True,
    )


def load_day_summary(day_dir: Path) -> DaySummary:
    parsed = parse_day_readme(day_dir)
    if parsed is not None:
        if not parsed.kind_counter or not parsed.source_form_counter:
            return summarize_day_dir(day_dir, has_readme=True, readme_parse_ok=True)
        return parsed
    return summarize_day_dir(day_dir, has_readme=(day_dir / "README.md").is_file(), readme_parse_ok=False)
