#!/usr/bin/env python3
"""Build generated inventory-style README indices for statecraft day archives."""

from __future__ import annotations

import argparse
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


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def _parse_frontmatter(path: Path) -> dict[str, Any]:
    text = _read_text(path)
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    return _parse_simple_frontmatter_block(match.group(1))


def _parse_simple_frontmatter_block(block: str) -> dict[str, Any]:
    """Parse the narrow YAML subset used by source-archive frontmatter.

    Supports top-level scalar values and top-level list fields of the form:
      key: value
      key:
        - item
        - item
    """
    data: dict[str, Any] = {}
    current_list_key: str | None = None
    for raw_line in block.splitlines():
        line = raw_line.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        list_match = re.match(r"^\s*-\s*(.+?)\s*$", line)
        if list_match and current_list_key:
            data.setdefault(current_list_key, [])
            data[current_list_key].append(_parse_scalar(list_match.group(1)))
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
        data[key] = _parse_scalar(raw_value)
    return data


def _parse_scalar(raw: str) -> str:
    text = raw.strip()
    if len(text) >= 2 and text[0] == text[-1] and text[0] in {'"', "'"}:
        return text[1:-1]
    return text


def _norm_scalar(value: Any) -> str:
    return " ".join(str(value or "").split()).strip()


def _as_values(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, (list, tuple)):
        out: list[str] = []
        for item in value:
            text = _norm_scalar(item)
            if text and text not in out:
                out.append(text)
        return tuple(out)
    text = _norm_scalar(value)
    return (text,) if text else ()


def _normalize_person_label(value: str) -> str:
    text = _norm_scalar(value)
    while True:
        updated = HONORIFIC_RE.sub("", text).strip()
        if updated == text:
            break
        text = updated
    return text


def _normalize_channel_label(value: str) -> str:
    text = _norm_scalar(value)
    if "-" in text and " " not in text and text.lower() == text:
        return text.replace("-", " ").title()
    return text


def _type_label(name: str) -> str:
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
    meta = _parse_frontmatter(path)
    host_values = tuple(
        filter(None, (_normalize_person_label(v) for v in (_as_values(meta.get("host")) or _as_values(meta.get("hosts")))))
    )
    guest_values = (
        _as_values(meta.get("guest"))
        or _as_values(meta.get("guests"))
        or _as_values(meta.get("speaker"))
        or _as_values(meta.get("speakers"))
        or _as_values(meta.get("participants"))
    )
    guest_values = tuple(filter(None, (_normalize_person_label(v) for v in guest_values)))
    channel_values = (
        _as_values(meta.get("show"))
        or _as_values(meta.get("channel_slug"))
        or _as_values(meta.get("publication"))
    )
    channel_values = tuple(filter(None, (_normalize_channel_label(v) for v in channel_values)))
    thread_values = _as_values(meta.get("thread")) or _as_values(meta.get("threads"))
    return ArchiveFile(
        path=path,
        name=path.name,
        title=_norm_scalar(meta.get("title")),
        show=_norm_scalar(meta.get("show")),
        host_values=host_values,
        guest_values=guest_values,
        thread_values=thread_values,
        channel_values=channel_values,
        source_type=_norm_scalar(meta.get("source_type")),
        type_label=_type_label(path.name),
        fallback_family=infer_family_label(path.name),
        has_frontmatter=bool(meta),
    )


def _fmt_counter(counter: Counter[str]) -> str:
    if not counter:
        return "(none)"
    parts = [f"`{name}` ({count})" for name, count in sorted(counter.items(), key=lambda item: (-item[1], item[0]))]
    return ", ".join(parts)


def _rollup_values(records: list[ArchiveFile], attr: str) -> Counter[str]:
    counter: Counter[str] = Counter()
    for record in records:
        for value in getattr(record, attr):
            counter[value] += 1
    return counter


def _fallback_counter(records: list[ArchiveFile]) -> Counter[str]:
    counter: Counter[str] = Counter()
    for record in records:
        if record.channel_values and record.host_values and record.guest_values and record.thread_values:
            continue
        counter[record.fallback_family] += 1
    return counter


def build_day_readme(day_dir: Path) -> str:
    files = sorted(
        [path for path in day_dir.glob("*.md") if path.name != "README.md"],
        key=lambda path: path.name,
    )
    records = [collect_archive_file(path) for path in files]

    type_counter = Counter(record.type_label for record in records)
    channel_counter = _rollup_values(records, "channel_values")
    host_counter = _rollup_values(records, "host_values")
    guest_counter = _rollup_values(records, "guest_values")
    thread_counter = _rollup_values(records, "thread_values")
    fallback_counter = _fallback_counter(records)

    stats = [
        f"- Source files: `{len(records)}`",
        f"- Type mix: {_fmt_counter(type_counter)}",
        f"- Distinct channels/shows: `{len(channel_counter)}`",
        f"- Distinct hosts: `{len(host_counter)}`",
        f"- Distinct guests: `{len(guest_counter)}`",
        f"- Distinct threads: `{len(thread_counter)}`",
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
        f"- { _fmt_counter(channel_counter) }",
        "",
        "## Host / Guest / Thread Rollup",
        "",
        f"- Hosts: { _fmt_counter(host_counter) }",
        f"- Guests: { _fmt_counter(guest_counter) }",
        f"- Threads: { _fmt_counter(thread_counter) }",
        "",
        "## Filename Family Fallbacks",
        "",
        f"- { _fmt_counter(fallback_counter) }",
        "",
        "## Files",
        "",
    ]
    lines.extend(f"- `{record.name}`" for record in records)
    lines.append("")
    return "\n".join(lines)


def _iter_day_dirs(root: Path, year: str) -> list[Path]:
    return sorted(
        [
            path
            for path in root.iterdir()
            if path.is_dir() and re.fullmatch(rf"{re.escape(year)}-\d{{2}}-\d{{2}}", path.name)
        ],
        key=lambda path: path.name,
    )


def write_day_index(day_dir: Path) -> Path:
    out_path = day_dir / "README.md"
    out_path.write_text(build_day_readme(day_dir), encoding="utf-8", newline="\n")
    return out_path


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="Statecraft source-archive root.")
    ap.add_argument("--year", type=str, default=DEFAULT_YEAR, help="Year prefix to index, default: 2026.")
    ap.add_argument("--day", type=str, default=None, help="Specific YYYY-MM-DD day to rebuild.")
    return ap.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    if args.day:
        day_dir = root / args.day
        if not day_dir.is_dir():
            raise SystemExit(f"day directory not found: {day_dir}")
        write_day_index(day_dir)
        print(f"wrote {day_dir / 'README.md'}")
        return 0

    day_dirs = _iter_day_dirs(root, args.year)
    for day_dir in day_dirs:
        write_day_index(day_dir)
    print(f"wrote {len(day_dirs)} day indices under {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
