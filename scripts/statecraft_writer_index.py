#!/usr/bin/env python3
"""Writer-index roster and archive stats for configured Substack / prose outlets."""

from __future__ import annotations

import json
import re
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from statecraft_day_archive import DEFAULT_ROOT, is_youtube_capture, iter_source_files, norm_scalar, parse_frontmatter

REPO_ROOT = Path(__file__).resolve().parent.parent
WRITER_DISCOVERY_CONFIG_PATH = REPO_ROOT / "platform" / "config" / "statecraft_writer_discovery.json"

WRITER_SOURCE_TYPE_WHITELIST = frozenset(
    {
        "substack",
        "substack-post",
        "article",
        "rss-item",
        "web-page",
        "institutional-primary",
        "paste-bundle",
        "mixed",
        "x-post-text",
        "x-post-bundle",
        "verbatim-sidecar",
    }
)
WRITER_KIND_WHITELIST = frozenset(
    {
        "substack-post",
        "rss-item",
        "paste-bundle",
        "article",
        "mixed",
        "x-post-text",
        "x-post-bundle",
        "verbatim-sidecar",
    }
)
WRITER_SOURCE_FORM_PROSE = frozenset(
    {
        "newsletter",
        "essay",
        "article",
        "institutional-statement",
        "op-ed",
        "wire",
    }
)
VIDEO_SOURCE_FORMS = frozenset({"solo", "interview", "panel", "livestream"})
VIDEO_KINDS = frozenset({"transcript", "operator-transcript", "cleaned-transcript"})

_FILENAME_DATE_RE = re.compile(r"^(?P<body>.+)-(\d{4}-\d{2}-\d{2})$")
_SLUG_RE = re.compile(r"[^a-z0-9]+")


def iter_all_day_dirs(root: Path) -> list[Path]:
    return sorted(
        [
            path
            for path in root.iterdir()
            if path.is_dir() and len(path.name) == 10 and path.name[4] == "-" and path.name[7] == "-"
        ],
        key=lambda path: path.name,
    )


def _slugify_channel_key(text: str) -> str:
    key = _SLUG_RE.sub("-", norm_scalar(text).lower()).strip("-")
    return key or "unknown"


def load_writer_discovery_payload(path: Path | None = None) -> dict[str, Any]:
    config_path = path or WRITER_DISCOVERY_CONFIG_PATH
    return json.loads(config_path.read_text(encoding="utf-8"))


def load_writer_slug_aliases(payload: dict[str, Any] | None = None) -> dict[str, str]:
    data = payload or load_writer_discovery_payload()
    raw = data.get("writer_slug_aliases") or {}
    return {str(key): str(value) for key, value in raw.items()}


def load_writer_index_misc_slugs(payload: dict[str, Any] | None = None) -> set[str]:
    data = payload or load_writer_discovery_payload()
    raw = data.get("writer_index_misc_slugs") or []
    return {str(slug) for slug in raw}


def canonical_writer_slug(slug: str, aliases: dict[str, str] | None = None) -> str:
    mapping = aliases or load_writer_slug_aliases()
    current = slug
    seen: set[str] = set()
    while current in mapping and current not in seen:
        seen.add(current)
        current = mapping[current]
    return current


def load_writer_roster(path: Path | None = None) -> list[dict[str, Any]]:
    payload = load_writer_discovery_payload(path)
    return list(payload.get("writers") or [])


def load_writer_rows_by_slug(path: Path | None = None) -> dict[str, dict[str, Any]]:
    return {str(row["writer_slug"]): row for row in load_writer_roster(path) if row.get("writer_slug")}


def is_hard_excluded_writer(meta: dict[str, Any]) -> bool:
    if is_youtube_capture(meta):
        return True
    source_form = norm_scalar(meta.get("source_form")).casefold()
    kind = norm_scalar(meta.get("kind")).casefold()
    if source_form in VIDEO_SOURCE_FORMS and kind in VIDEO_KINDS:
        if source_form not in WRITER_SOURCE_FORM_PROSE:
            return True
    return False


def is_writer_index_eligible(meta: dict[str, Any]) -> bool:
    if is_hard_excluded_writer(meta):
        return False
    source_type = norm_scalar(meta.get("source_type")).casefold()
    kind = norm_scalar(meta.get("kind")).casefold()
    source_form = norm_scalar(meta.get("source_form")).casefold()
    if source_type in WRITER_SOURCE_TYPE_WHITELIST:
        return True
    if kind in WRITER_KIND_WHITELIST:
        return True
    if source_form in WRITER_SOURCE_FORM_PROSE:
        return True
    if norm_scalar(meta.get("writer_slug")) or norm_scalar(meta.get("publication_slug")):
        return True
    return False


def _filename_prefix(filename: str) -> str:
    name = filename
    if not name.startswith("source-") or not name.endswith(".md"):
        return ""
    rest = name[len("source-") : -len(".md")]
    match = _FILENAME_DATE_RE.match(rest)
    if not match:
        return ""
    return match.group("body").split("-")[0]


def resolve_writer_slug(meta: dict[str, Any], filename: str = "", *, aliases: dict[str, str] | None = None) -> str:
    mapping = aliases or load_writer_slug_aliases()
    for field_name in ("writer_slug", "publication_slug", "thread"):
        value = norm_scalar(meta.get(field_name))
        if value:
            return canonical_writer_slug(value, mapping)
    author = norm_scalar(meta.get("author"))
    if author:
        return canonical_writer_slug(_slugify_channel_key(author), mapping)
    publication = norm_scalar(meta.get("publication"))
    if publication:
        return canonical_writer_slug(_slugify_channel_key(publication), mapping)
    prefix = _filename_prefix(filename)
    if prefix:
        return canonical_writer_slug(prefix, mapping)
    return ""


def _has_substack_signal(meta: dict[str, Any]) -> bool:
    source_type = norm_scalar(meta.get("source_type")).casefold()
    kind = norm_scalar(meta.get("kind")).casefold()
    if source_type in {"substack", "substack-post"} or kind == "substack-post":
        return True
    url = norm_scalar(meta.get("source_url")).casefold()
    return "substack.com" in url


def match_configured_writer_slug(
    meta: dict[str, Any],
    filename: str,
    *,
    roster: list[dict[str, Any]] | None = None,
    aliases: dict[str, str] | None = None,
) -> str:
    rows = roster if roster is not None else load_writer_roster()
    mapping = aliases if aliases is not None else load_writer_slug_aliases()
    for row in rows:
        if capture_matches_writer(meta, filename, row, aliases=mapping):
            return str(row.get("writer_slug") or "")
    return ""


def capture_matches_writer(
    meta: dict[str, Any],
    filename: str,
    writer_row: dict[str, Any],
    *,
    aliases: dict[str, str] | None = None,
) -> bool:
    if not is_writer_index_eligible(meta):
        return False
    slug = str(writer_row.get("writer_slug") or "")
    if writer_row.get("require_substack_signal") and not _has_substack_signal(meta):
        return False

    resolved = resolve_writer_slug(meta, filename, aliases=aliases)
    if resolved == slug:
        return True

    thread = norm_scalar(meta.get("thread"))
    if thread and canonical_writer_slug(thread, aliases or load_writer_slug_aliases()) == slug:
        feed_host = str(writer_row.get("feed_host") or "").casefold()
        url = norm_scalar(meta.get("source_url")).casefold()
        channel_name = norm_scalar(meta.get("channel_name")).casefold()
        if feed_host and (feed_host in url or feed_host in channel_name):
            return True
        prefixes = writer_row.get("filename_prefixes") or []
        prefix = _filename_prefix(filename)
        if prefix and prefix in prefixes:
            return True
        if not writer_row.get("filename_prefixes") and not writer_row.get("require_substack_signal"):
            return True
        return False

    feed_host = str(writer_row.get("feed_host") or "").casefold()
    if feed_host:
        haystacks = (
            norm_scalar(meta.get("source_url")),
            norm_scalar(meta.get("channel_name")),
            norm_scalar(meta.get("publication")),
        )
        if any(feed_host in value.casefold() for value in haystacks if value):
            return True

    prefixes = writer_row.get("filename_prefixes") or []
    prefix = _filename_prefix(filename)
    if prefix and prefix in prefixes:
        return True
    return False


@dataclass
class WriterStats:
    slug: str
    label: str
    feed_url: str
    thread: str
    file_count: int = 0
    days: set[str] = field(default_factory=set)
    months: set[str] = field(default_factory=set)
    source_types: Counter[str] = field(default_factory=Counter)
    first_day: str | None = None
    last_day: str | None = None
    check_written: bool = True
    discoverable: bool = False


def collect_writer_stats(root: Path, config_path: Path | None = None) -> dict[str, WriterStats]:
    payload = load_writer_discovery_payload(config_path)
    aliases = load_writer_slug_aliases(payload)
    roster = load_writer_roster(config_path)
    stats: dict[str, WriterStats] = {}
    for row in roster:
        slug = str(row.get("writer_slug") or "")
        if not slug:
            continue
        stats[slug] = WriterStats(
            slug=slug,
            label=str(row.get("label") or slug),
            feed_url=str(row.get("feed_url") or ""),
            thread=str(row.get("thread") or slug),
            check_written=bool(row.get("check_written", True)),
            discoverable=bool(row.get("discoverable", False)),
        )

    for day_dir in iter_all_day_dirs(root):
        day = day_dir.name
        month = day[:7]
        for path in iter_source_files(day_dir):
            meta = parse_frontmatter(path)
            for slug, entry in stats.items():
                row = next(item for item in roster if item.get("writer_slug") == slug)
                if not capture_matches_writer(meta, path.name, row, aliases=aliases):
                    continue
                entry.file_count += 1
                entry.days.add(day)
                entry.months.add(month)
                source_type = norm_scalar(meta.get("source_type")) or norm_scalar(meta.get("kind")) or "(none)"
                entry.source_types[source_type] += 1
                entry.first_day = day if entry.first_day is None else min(entry.first_day, day)
                entry.last_day = day if entry.last_day is None else max(entry.last_day, day)
                break
    return stats


def build_writer_index_json(root: Path, config_path: Path | None = None) -> dict[str, Any]:
    stats = collect_writer_stats(root, config_path)
    writers: list[dict[str, Any]] = []
    for entry in sorted(stats.values(), key=lambda item: (-item.file_count, item.slug)):
        writers.append(
            {
                "writer_slug": entry.slug,
                "label": entry.label,
                "thread": entry.thread,
                "feed_url": entry.feed_url,
                "file_count": entry.file_count,
                "day_count": len(entry.days),
                "source_types": dict(entry.source_types),
                "check_written": entry.check_written,
                "discoverable": entry.discoverable,
                "first_day": entry.first_day or "",
                "last_day": entry.last_day or "",
            }
        )
    return {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "check_written_scope": "configured_roster",
        "check_written_notes": "Writer-index v1 lists configured Substack feeds only; see statecraft_writer_discovery.json.",
        "source_markdown": "writer-index.md",
        "stats": {
            "writer_count": len(writers),
            "file_count": sum(item["file_count"] for item in writers),
        },
        "writers": writers,
    }


def build_writer_index(root: Path, config_path: Path | None = None) -> str:
    stats = collect_writer_stats(root, config_path)
    total_files = sum(entry.file_count for entry in stats.values())
    lines = [
        "# Statecraft Archive - Writer Index",
        "",
        "_Generated inventory note. Rebuild with `python scripts/refresh_statecraft_archive_indices.py`._",
        "",
        "Flat registry of **configured written-source outlets** (Substack feeds in v1). "
        "YouTube channels live in [channel-index.md](../../statecraft/channels/channel-index.md). "
        "Cross-modal speaker rollups: [thread-index.md](./thread-index.md).",
        "",
        "Inclusion law: [writer-index-spec.md](./writer-index-spec.md). "
        "Roster SSOT: [statecraft_writer_discovery.json](../../platform/config/statecraft_writer_discovery.json).",
        "",
        "## Stats",
        "",
        f"- Configured writers: `{len(stats)}`",
        f"- Archive files mapped: `{total_files}`",
        f"- Machine roster: [writer-index.json](./writer-index.json)",
        "",
        "## Writers",
        "",
        "| Writer slug | Label | Files | Days | Thread | Feed URL | First day | Last day |",
        "| --- | --- | ---: | ---: | --- | --- | --- | --- |",
    ]
    for entry in sorted(stats.values(), key=lambda item: (-item.file_count, item.slug)):
        url = entry.feed_url.rstrip("/")
        url_cell = f"[open]({url})" if url.startswith("http") else ""
        lines.append(
            f"| `{entry.slug}` | {entry.label} | {entry.file_count} | {len(entry.days)} | "
            f"`{entry.thread}` | {url_cell} | `{entry.first_day or ''}` | `{entry.last_day or ''}` |"
        )
    lines.extend(
        [
            "",
            "## Return",
            "",
            "- YouTube roster: [channel-index.md](../../statecraft/channels/channel-index.md)",
            "- Spec: [writer-index-spec.md](./writer-index-spec.md)",
            "- Root archive: [source-archive/statecraft/README.md](./README.md)",
            "",
        ]
    )
    return "\n".join(lines)


def writer_index_json_path(root: Path | None = None) -> Path:
    archive_root = (root or DEFAULT_ROOT).resolve()
    return archive_root / "writer-index.json"


def load_writer_index_json(path: Path | None = None) -> dict[str, Any]:
    json_path = path or writer_index_json_path()
    return json.loads(json_path.read_text(encoding="utf-8"))


def load_check_written_roster(
    *,
    root: Path | None = None,
    json_path: Path | None = None,
    config_path: Path | None = None,
    rebuild: bool = False,
) -> list[dict[str, Any]]:
    """Main writer-index roster for check-written (misc slugs excluded).

    Reads ``writer-index.json`` when present unless ``rebuild=True``.
    """
    misc_slugs = load_writer_index_misc_slugs(
        load_writer_discovery_payload(config_path) if config_path else None
    )
    archive_root = (root or DEFAULT_ROOT).resolve()

    if not rebuild:
        path = json_path or writer_index_json_path(archive_root)
        if path.is_file():
            payload = load_writer_index_json(path)
            writers = list(payload.get("writers") or [])
            return [
                row
                for row in writers
                if row.get("check_written", True) and str(row.get("writer_slug") or "") not in misc_slugs
            ]

    payload = build_writer_index_json(archive_root, config_path)
    writers = list(payload.get("writers") or [])
    return [
        row
        for row in writers
        if row.get("check_written", True) and str(row.get("writer_slug") or "") not in misc_slugs
    ]
