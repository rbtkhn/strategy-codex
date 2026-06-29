#!/usr/bin/env python3
"""Audit statecraft archive index surfaces (day → month/year inventory → global navigation).

Usage:
    python scripts/audit_statecraft_archive_index.py --day 2026-06-28
    python scripts/audit_statecraft_archive_index.py --day 2026-06-28 --table
    python scripts/audit_statecraft_archive_index.py --month 2026-06 --table-only
    python scripts/audit_statecraft_archive_index.py --global
    python scripts/audit_statecraft_archive_index.py --channel-index --table
    python scripts/audit_statecraft_archive_index.py --writer-index --table
    python scripts/audit_statecraft_archive_index.py --voice-index --table
    python scripts/audit_statecraft_archive_index.py --shelf-index parsi --table
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Literal

REPO_ROOT = Path(__file__).resolve().parents[1]
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import build_statecraft_archive_navigation as nav  # noqa: E402
import build_statecraft_day_indices as day_idx  # noqa: E402
import shelf_index_utils as shelf_utils  # noqa: E402
import statecraft_writer_index as writer_idx  # noqa: E402
import validate_repo_routing as routing_val  # noqa: E402
from quantify_section_nav import extract_transcript  # noqa: E402
from statecraft_day_archive import (  # noqa: E402
    CHANNEL_INDEX_DIR,
    DAY_INDEX_FILENAME,
    DEFAULT_ROOT,
    build_day_index,
    build_day_readme_stub,
    classify_day_captures,
    is_youtube_capture,
    iter_day_dirs,
    iter_source_files,
    norm_scalar,
    parse_day_readme,
    parse_frontmatter,
    read_text,
    summarize_day_dir,
)

from statecraft_youtube_discovery import is_daily_watchlist_slug, load_daily_watchlist_keys  # noqa: E402

Bucket = Literal["channel", "writer", "other"]
SortKey = Literal["date", "words", "title", "bucket"]
ChannelSortKey = Literal["files", "slug", "label", "last_day"]

DEFAULT_MONTH_YEAR_TABLE_LIMIT = 50

VOICES_DIR = REPO_ROOT / "statecraft" / "voices"
VOICES_META_DIRS = frozenset({"_templates", "_scratch", "map", "relations"})


@dataclass(frozen=True)
class InventoryRow:
    day_folder: str
    pub_date: str
    filename: str
    title: str
    source_url: str
    words: int
    bucket: Bucket
    kind: str
    sections: int | None

    def sort_date(self) -> str:
        return self.pub_date or self.day_folder


@dataclass
class AuditFinding:
    level: Literal["pass", "fail", "warn"]
    code: str
    message: str


@dataclass(frozen=True)
class ChannelIndexRow:
    slug: str
    label: str
    files: int
    days: int
    watchlist: bool
    channel_url: str
    first_day: str
    last_day: str
    explicit_slug: bool


@dataclass(frozen=True)
class WriterIndexRow:
    slug: str
    label: str
    files: int
    days: int
    thread: str
    feed_url: str
    first_day: str
    last_day: str


@dataclass(frozen=True)
class VoiceIndexRow:
    slug: str
    label: str
    primary_index: str
    listed: bool
    profile: bool
    index_kind: str


@dataclass(frozen=True)
class ShelfCaptureRow:
    pub_date: str
    title: str
    capture_path: str
    on_disk: bool

    def sort_date(self) -> str:
        return self.pub_date


MD_LINK_PAIR = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")


def word_count_capture(path: Path) -> int:
    text = read_text(path)
    body = text.split("---", 2)[2] if text.startswith("---") else text
    transcript = extract_transcript(body)
    return len(re.findall(r"\b\w+\b", transcript))


def section_count_capture(path: Path, meta: dict[str, Any]) -> int | None:
    curation = norm_scalar(meta.get("transcript_curation"))
    if curation != "curated_sectioned":
        return None
    text = read_text(path)
    body = text.split("---", 2)[2] if text.startswith("---") else text
    transcript = extract_transcript(body)
    count = len(re.findall(r"^### .+$", transcript, re.MULTILINE))
    return count if count else None


def inventory_row_for_capture(path: Path, day_dir: Path) -> InventoryRow:
    meta = parse_frontmatter(path)
    record_bucket: Bucket = "other"
    for entry in classify_day_captures(day_dir):
        if entry.path == path:
            record_bucket = entry.bucket
            break
    title = norm_scalar(meta.get("title")) or path.stem.removeprefix("source-")
    pub_date = norm_scalar(meta.get("pub_date")) or day_dir.name
    kind = norm_scalar(meta.get("kind")) or norm_scalar(meta.get("source_form")) or "—"
    url = norm_scalar(meta.get("source_url")) or "—"
    return InventoryRow(
        day_folder=day_dir.name,
        pub_date=pub_date,
        filename=path.name,
        title=title,
        source_url=url,
        words=word_count_capture(path),
        bucket=record_bucket,
        kind=kind,
        sections=section_count_capture(path, meta),
    )


def collect_inventory_rows(day_dirs: list[Path]) -> list[InventoryRow]:
    rows: list[InventoryRow] = []
    for day_dir in day_dirs:
        for path in iter_source_files(day_dir):
            rows.append(inventory_row_for_capture(path, day_dir))
    return rows


def sort_inventory_rows(rows: list[InventoryRow], sort_key: SortKey) -> list[InventoryRow]:
    if sort_key == "words":
        return sorted(rows, key=lambda r: (-r.words, r.sort_date(), r.filename))
    if sort_key == "title":
        return sorted(rows, key=lambda r: (r.title.casefold(), r.sort_date(), r.filename))
    if sort_key == "bucket":
        return sorted(rows, key=lambda r: (r.bucket, r.sort_date(), r.filename))
    return sorted(rows, key=lambda r: (r.sort_date(), r.filename))


def apply_table_limit(
    rows: list[InventoryRow],
    limit: int | None,
) -> tuple[list[InventoryRow], int]:
    if limit is None or limit <= 0 or len(rows) <= limit:
        return rows, 0
    return rows[:limit], len(rows) - limit


def default_table_limit(scope: str) -> int | None:
    if scope in ("day", "channel-index", "writer-index", "voice-index", "shelf-index"):
        return None
    return DEFAULT_MONTH_YEAR_TABLE_LIMIT


def capture_hygiene_warnings(path: Path, meta: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    host_scalar = norm_scalar(meta.get("host"))
    host_people = meta.get("host_people")
    if host_scalar and not host_people:
        warnings.append(f"{path.name}: host scalar set but host_people empty")
    thread_scalar = norm_scalar(meta.get("thread"))
    threads = meta.get("threads")
    if thread_scalar and not threads:
        warnings.append(f"{path.name}: thread scalar set but threads empty")
    if is_youtube_capture(meta) and not norm_scalar(meta.get("source_url")):
        warnings.append(f"{path.name}: YouTube capture missing source_url")
    return warnings


def _channel_surface_status(path: Path, rendered: str) -> str:
    return nav._render_compare_status(path, rendered)


def collect_channel_index_rows(root: Path, *, misc: bool = False) -> list[ChannelIndexRow]:
    watchlist_keys = load_daily_watchlist_keys()
    if misc:
        all_stats = nav.collect_channel_stats(root)
        misc_slugs = nav.load_channel_index_misc_slugs()
        _, stats = nav._partition_channel_stats(all_stats, misc_slugs)
    else:
        stats = nav.collect_main_channel_stats(root)
    rows: list[ChannelIndexRow] = []
    for entry in stats.values():
        url = entry.channel_url or ""
        if url and not url.startswith("http"):
            url = f"https://{url}"
        rows.append(
            ChannelIndexRow(
                slug=entry.slug,
                label=entry.label,
                files=entry.file_count,
                days=len(entry.days),
                watchlist=is_daily_watchlist_slug(entry.slug, watchlist_keys),
                channel_url=url,
                first_day=entry.first_day or "",
                last_day=entry.last_day or "",
                explicit_slug=entry.explicit_slug,
            )
        )
    return rows


def sort_channel_index_rows(rows: list[ChannelIndexRow], sort_key: ChannelSortKey) -> list[ChannelIndexRow]:
    if sort_key == "slug":
        return sorted(rows, key=lambda r: (r.slug, -r.files))
    if sort_key == "label":
        return sorted(rows, key=lambda r: (r.label.casefold(), -r.files))
    if sort_key == "last_day":
        return sorted(rows, key=lambda r: (r.last_day, -r.files, r.slug))
    return sorted(rows, key=lambda r: (-r.files, r.slug))


def map_channel_table_sort(sort_key: SortKey) -> ChannelSortKey:
    if sort_key == "title":
        return "label"
    if sort_key == "bucket":
        return "slug"
    if sort_key == "date":
        return "files"
    return "files"


def audit_channel_index(root: Path) -> list[AuditFinding]:
    findings: list[AuditFinding] = []
    surfaces = [
        ("channel-index.md", CHANNEL_INDEX_DIR / "channel-index.md", nav.build_channel_index(root)),
        (
            "channel-index-misc.md",
            CHANNEL_INDEX_DIR / "channel-index-misc.md",
            nav.build_channel_index_misc(root),
        ),
    ]
    for name, path, rendered in surfaces:
        status = _channel_surface_status(path, rendered)
        if status == "ok":
            findings.append(AuditFinding("pass", "channel_md", f"{name} matches builder"))
        elif status == "missing":
            findings.append(AuditFinding("fail", "missing_channel_md", f"{name} missing"))
        else:
            findings.append(AuditFinding("fail", "stale_channel_md", f"{name} stale vs recomputed build"))

    json_path = CHANNEL_INDEX_DIR / "channel-index.json"
    json_stale = nav._json_payload_semantically_changed(json_path, nav.build_channel_index_json(root))
    if not json_path.is_file():
        findings.append(AuditFinding("fail", "missing_channel_json", "channel-index.json missing"))
    elif json_stale:
        findings.append(AuditFinding("fail", "stale_channel_json", "channel-index.json stale vs recomputed build"))
    else:
        findings.append(AuditFinding("pass", "channel_json", "channel-index.json matches builder"))

    live_main = nav.collect_main_channel_stats(root)
    live_files = sum(entry.file_count for entry in live_main.values())
    if json_path.is_file() and not json_stale:
        try:
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            indexed_files = int(payload.get("stats", {}).get("youtube_source_files", -1))
            if indexed_files >= 0 and indexed_files != live_files:
                findings.append(
                    AuditFinding(
                        "warn",
                        "stats_drift",
                        f"channel-index.json youtube_source_files {indexed_files} vs live {live_files}",
                    )
                )
        except (json.JSONDecodeError, TypeError, ValueError):
            findings.append(AuditFinding("warn", "channel_json_parse", "channel-index.json stats unreadable"))

    for entry in live_main.values():
        if not entry.explicit_slug:
            findings.append(
                AuditFinding(
                    "warn",
                    "hygiene",
                    f"{entry.slug}: derived channel slug (no explicit channel_slug in captures)",
                )
            )
        if not entry.channel_url:
            findings.append(
                AuditFinding("warn", "hygiene", f"{entry.slug}: missing channel URL on roster row")
            )

    return findings


def format_channel_index_table(
    scope_label: str,
    rows: list[ChannelIndexRow],
    *,
    truncated: int,
    sort_key: ChannelSortKey,
) -> str:
    lines = [
        f"## Channel index inventory — {scope_label}",
        "",
        f"_Sorted by `{sort_key}`; main roster (misc excluded)._",
        "",
        "| Slug | Label | Files | Days | Watchlist | Last day | URL |",
        "| --- | --- | ---: | ---: | --- | --- | --- |",
    ]
    for row in rows:
        label = row.label.replace("|", "\\|")
        if len(label) > 48:
            label = label[:45] + "..."
        url = row.channel_url or "—"
        if len(url) > 48 and url != "—":
            url = url[:45] + "..."
        watch = "yes" if row.watchlist else ""
        slug_cell = row.slug if row.explicit_slug else f"{row.slug} *"
        lines.append(
            f"| `{slug_cell}` | {label} | {row.files} | {row.days} | {watch} | {row.last_day} | {url} |"
        )
    if truncated:
        lines.append("")
        lines.append(f"_… and {truncated} more row(s); use `--table-limit 0` for full list._")
    lines.append("")
    lines.append(f"rows shown: {len(rows)}")
    return "\n".join(lines)


def run_fix_channel_index(root: Path) -> None:
    nav.write_rendered(CHANNEL_INDEX_DIR / "channel-index.md", nav.build_channel_index(root), check=False)
    nav.write_channel_index_json(CHANNEL_INDEX_DIR / "channel-index.json", root, check=False)
    nav.write_rendered(
        CHANNEL_INDEX_DIR / "channel-index-misc.md",
        nav.build_channel_index_misc(root),
        check=False,
    )


def collect_writer_index_rows(root: Path) -> list[WriterIndexRow]:
    rows: list[WriterIndexRow] = []
    for entry in writer_idx.collect_writer_stats(root).values():
        url = entry.feed_url.rstrip("/")
        rows.append(
            WriterIndexRow(
                slug=entry.slug,
                label=entry.label,
                files=entry.file_count,
                days=len(entry.days),
                thread=entry.thread,
                feed_url=url,
                first_day=entry.first_day or "",
                last_day=entry.last_day or "",
            )
        )
    return rows


def sort_writer_index_rows(rows: list[WriterIndexRow], sort_key: ChannelSortKey) -> list[WriterIndexRow]:
    if sort_key == "slug":
        return sorted(rows, key=lambda r: (r.slug, -r.files))
    if sort_key == "label":
        return sorted(rows, key=lambda r: (r.label.casefold(), -r.files))
    if sort_key == "last_day":
        return sorted(rows, key=lambda r: (r.last_day, -r.files, r.slug))
    return sorted(rows, key=lambda r: (-r.files, r.slug))


def audit_writer_index(root: Path) -> list[AuditFinding]:
    findings: list[AuditFinding] = []
    md_path = root / "writer-index.md"
    rendered = writer_idx.build_writer_index(root)
    status = _channel_surface_status(md_path, rendered)
    if status == "ok":
        findings.append(AuditFinding("pass", "writer_md", "writer-index.md matches builder"))
    elif status == "missing":
        findings.append(AuditFinding("fail", "missing_writer_md", "writer-index.md missing"))
    else:
        findings.append(AuditFinding("fail", "stale_writer_md", "writer-index.md stale vs recomputed build"))

    json_path = root / "writer-index.json"
    json_stale = nav._json_payload_semantically_changed(json_path, writer_idx.build_writer_index_json(root))
    if not json_path.is_file():
        findings.append(AuditFinding("fail", "missing_writer_json", "writer-index.json missing"))
    elif json_stale:
        findings.append(AuditFinding("fail", "stale_writer_json", "writer-index.json stale vs recomputed build"))
    else:
        findings.append(AuditFinding("pass", "writer_json", "writer-index.json matches builder"))

    live_stats = writer_idx.collect_writer_stats(root)
    live_files = sum(entry.file_count for entry in live_stats.values())
    if json_path.is_file() and not json_stale:
        try:
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            indexed_files = int(payload.get("stats", {}).get("file_count", -1))
            if indexed_files >= 0 and indexed_files != live_files:
                findings.append(
                    AuditFinding(
                        "warn",
                        "stats_drift",
                        f"writer-index.json file_count {indexed_files} vs live {live_files}",
                    )
                )
        except (json.JSONDecodeError, TypeError, ValueError):
            findings.append(AuditFinding("warn", "writer_json_parse", "writer-index.json stats unreadable"))

    for entry in live_stats.values():
        if entry.file_count == 0:
            findings.append(
                AuditFinding(
                    "warn",
                    "hygiene",
                    f"{entry.slug}: configured writer with zero archive files",
                )
            )

    return findings


def format_writer_index_table(
    scope_label: str,
    rows: list[WriterIndexRow],
    *,
    truncated: int,
    sort_key: ChannelSortKey,
) -> str:
    lines = [
        f"## Writer index inventory — {scope_label}",
        "",
        f"_Sorted by `{sort_key}`; configured prose roster only (YouTube excluded)._",
        "",
        "| Slug | Label | Files | Days | Thread | Last day | Feed URL |",
        "| --- | --- | ---: | ---: | --- | --- | --- |",
    ]
    for row in rows:
        label = row.label.replace("|", "\\|")
        if len(label) > 48:
            label = label[:45] + "..."
        url = row.feed_url or "—"
        if len(url) > 48 and url != "—":
            url = url[:45] + "..."
        lines.append(
            f"| `{row.slug}` | {label} | {row.files} | {row.days} | `{row.thread}` | {row.last_day} | {url} |"
        )
    if truncated:
        lines.append("")
        lines.append(f"_… and {truncated} more row(s); use `--table-limit 0` for full list._")
    lines.append("")
    lines.append(f"rows shown: {len(rows)}")
    return "\n".join(lines)


def run_fix_writer_index(root: Path) -> None:
    nav.write_rendered(root / "writer-index.md", writer_idx.build_writer_index(root), check=False)
    nav.write_writer_index_json(root / "writer-index.json", root, check=False)


def _voice_index_lists_path(rel_posix: str, index_text: str, basename: str) -> bool:
    return routing_val._index_lists_source_index(rel_posix, index_text, basename)


def _posix_rel(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def discover_voice_primary_indexes(voices_dir: Path | None = None) -> list[tuple[str, Path, str]]:
    base = voices_dir or VOICES_DIR
    rows: list[tuple[str, Path, str]] = []
    if not base.is_dir():
        return rows
    for shelf in sorted(base.iterdir()):
        if not shelf.is_dir() or shelf.name in VOICES_META_DIRS:
            continue
        slug = shelf.name
        primary = shelf / f"{slug}-index.md"
        if primary.is_file():
            rows.append((slug, primary, "primary"))
            continue
        legacy = shelf / f"{slug}-source-index.md"
        if legacy.is_file():
            rows.append((slug, legacy, "legacy-source"))
    return rows


def collect_voice_index_rows(voices_dir: Path | None = None) -> list[VoiceIndexRow]:
    index_path = (voices_dir or VOICES_DIR) / "voice-index.md"
    index_text = read_text(index_path) if index_path.is_file() else ""
    rows: list[VoiceIndexRow] = []
    for slug, path, kind in discover_voice_primary_indexes(voices_dir):
        rel = _posix_rel(path)
        profile_path = path.parent / f"{slug}-profile.md"
        label = slug.replace("-", " ").title()
        rows.append(
            VoiceIndexRow(
                slug=slug,
                label=label,
                primary_index=rel,
                listed=_voice_index_lists_path(rel, index_text, path.name),
                profile=profile_path.is_file(),
                index_kind=kind,
            )
        )
    return rows


def sort_voice_index_rows(rows: list[VoiceIndexRow], sort_key: ChannelSortKey) -> list[VoiceIndexRow]:
    if sort_key == "label":
        return sorted(rows, key=lambda r: (r.label.casefold(), r.slug))
    if sort_key == "slug":
        return sorted(rows, key=lambda r: r.slug)
    if sort_key == "last_day":
        return sorted(rows, key=lambda r: (not r.listed, r.slug))
    return sorted(rows, key=lambda r: (not r.listed, r.slug))


def audit_voice_index(voices_dir: Path | None = None) -> list[AuditFinding]:
    findings: list[AuditFinding] = []
    base = voices_dir or VOICES_DIR
    index_path = base / "voice-index.md"
    if not index_path.is_file():
        findings.append(AuditFinding("fail", "missing_voice_index", "voice-index.md missing"))
        return findings

    index_text = read_text(index_path)
    if "source-lattice" not in index_text.casefold():
        findings.append(
            AuditFinding("fail", "voice_index_doctrine", "voice-index.md missing source-lattice disambiguation")
        )
    else:
        findings.append(
            AuditFinding("pass", "voice_index_doctrine", "voice-index.md includes source-lattice disambiguation")
        )

    link_errors: list[str] = []
    routing_val.validate_markdown_links([index_path], link_errors, strict=True)
    if link_errors:
        for msg in link_errors[:10]:
            findings.append(AuditFinding("fail", "broken_link", msg))
        if len(link_errors) > 10:
            findings.append(
                AuditFinding(
                    "fail",
                    "broken_link",
                    f"… and {len(link_errors) - 10} more broken link(s) in voice-index.md",
                )
            )
    else:
        findings.append(AuditFinding("pass", "links_ok", "voice-index.md links resolve on disk"))

    primary = discover_voice_primary_indexes(base)
    unlisted = [
        _posix_rel(path)
        for _slug, path, _kind in primary
        if not _voice_index_lists_path(_posix_rel(path), index_text, path.name)
    ]
    if unlisted:
        for rel in unlisted:
            findings.append(AuditFinding("fail", "registry_gap", f"voice-index.md missing primary shelf: {rel}"))
    else:
        findings.append(
            AuditFinding(
                "pass",
                "registry_parity",
                f"voice-index.md lists all {len(primary)} primary voice shelves",
            )
        )

    for path in sorted(base.glob("**/*-source-index.md")) if base.is_dir() else []:
        slug = path.parent.name
        promoted = base / slug / f"{slug}-index.md"
        if promoted.is_file():
            continue
        rel = _posix_rel(path)
        if not _voice_index_lists_path(rel, index_text, path.name):
            findings.append(
                AuditFinding("warn", "hygiene", f"legacy source-index not listed in voice-index.md: {rel}")
            )

    shelves_without_index = []
    if base.is_dir():
        for shelf in sorted(base.iterdir()):
            if not shelf.is_dir() or shelf.name in VOICES_META_DIRS:
                continue
            if not any(shelf / name for name in (f"{shelf.name}-index.md", f"{shelf.name}-source-index.md")):
                shelves_without_index.append(shelf.name)
    for slug in shelves_without_index:
        findings.append(
            AuditFinding("warn", "hygiene", f"{slug}: voice shelf missing primary or legacy source-index file")
        )

    return findings


def format_voice_index_table(
    scope_label: str,
    rows: list[VoiceIndexRow],
    *,
    truncated: int,
    sort_key: ChannelSortKey,
) -> str:
    lines = [
        f"## Voice index inventory — {scope_label}",
        "",
        f"_Sorted by `{sort_key}`; curated registry (not generated)._",
        "",
        "| Slug | Label | Primary index | Listed | Profile | Kind |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        label = row.label.replace("|", "\\|")
        listed = "yes" if row.listed else "no"
        profile = "yes" if row.profile else ""
        idx = f"{row.slug}/{Path(row.primary_index).name}"
        lines.append(
            f"| `{row.slug}` | {label} | `{idx}` | {listed} | {profile} | {row.index_kind} |"
        )
    if truncated:
        lines.append("")
        lines.append(f"_… and {truncated} more row(s); use `--table-limit 0` for full list._")
    lines.append("")
    lines.append(f"rows shown: {len(rows)}")
    return "\n".join(lines)


def shelf_index_path(slug: str, voices_dir: Path | None = None) -> Path:
    base = voices_dir or VOICES_DIR
    return base / slug / f"{slug}-index.md"


def parse_shelf_index_links(index_path: Path) -> list[tuple[str, str, Path | None]]:
    text = read_text(index_path)
    rows: list[tuple[str, str, Path | None]] = []
    seen: set[str] = set()
    for match in MD_LINK_PAIR.finditer(text):
        title = match.group(1).strip()
        target = match.group(2).strip().split("#", 1)[0]
        if not target or target.startswith(("http://", "https://", "mailto:")):
            continue
        dest = routing_val.resolve_md_link(index_path, target)
        if dest is None:
            continue
        try:
            rel = _posix_rel(dest)
        except Exception:
            rel = str(dest)
        if rel in seen:
            continue
        seen.add(rel)
        if dest.name.startswith("source-") and "source-archive/statecraft" in rel.replace("\\", "/"):
            rows.append((title, rel, dest if dest.is_file() else None))
    return rows


def iter_archive_captures_for_shelf(slug: str, root: Path) -> list[Path]:
    if not root.is_dir():
        return []
    paths: list[Path] = []
    for day_dir in writer_idx.iter_all_day_dirs(root):
        for path in iter_source_files(day_dir):
            meta = parse_frontmatter(path)
            body_snip = read_text(path)[:8000] if path.is_file() else ""
            if shelf_utils.capture_matches_shelf(slug, path, meta, body_snip):
                paths.append(path)
    return sorted(paths, key=lambda p: (p.parent.name, p.name))


def collect_shelf_capture_rows(
    slug: str,
    *,
    archive_root: Path,
    index_path: Path | None = None,
) -> list[ShelfCaptureRow]:
    index_path = index_path or shelf_index_path(slug)
    rows: list[ShelfCaptureRow] = []
    for title, rel, dest in parse_shelf_index_links(index_path):
        pub_date = ""
        parts = rel.split("/")
        for part in parts:
            if len(part) == 10 and part[4] == "-" and part[7] == "-":
                pub_date = part
                break
        rows.append(
            ShelfCaptureRow(
                pub_date=pub_date,
                title=title or Path(rel).name,
                capture_path=rel,
                on_disk=bool(dest and dest.is_file()),
            )
        )
    return rows


def sort_shelf_capture_rows(rows: list[ShelfCaptureRow], sort_key: SortKey) -> list[ShelfCaptureRow]:
    if sort_key == "title":
        return sorted(rows, key=lambda r: (r.title.casefold(), r.pub_date))
    if sort_key == "words":
        return sorted(rows, key=lambda r: (not r.on_disk, r.pub_date, r.title))
    return sorted(rows, key=lambda r: (r.pub_date, r.title))


def audit_shelf_index(
    slug: str,
    *,
    archive_root: Path,
    voices_dir: Path | None = None,
) -> list[AuditFinding]:
    findings: list[AuditFinding] = []
    base = voices_dir or VOICES_DIR
    index_path = shelf_index_path(slug, base)
    if not index_path.is_file():
        findings.append(
            AuditFinding("fail", "missing_shelf_index", f"missing {slug}/{slug}-index.md")
        )
        return findings

    voice_registry = base / "voice-index.md"
    if voice_registry.is_file():
        reg_text = read_text(voice_registry)
        primary_rel = _posix_rel(index_path)
        if _voice_index_lists_path(primary_rel, reg_text, index_path.name):
            findings.append(
                AuditFinding("pass", "voice_registry", f"{slug} listed in voice-index.md")
            )
        else:
            findings.append(
                AuditFinding("fail", "voice_registry", f"{slug} not listed in voice-index.md")
            )

    link_errors: list[str] = []
    routing_val.validate_markdown_links([index_path], link_errors, strict=True)
    if link_errors:
        for msg in link_errors[:10]:
            findings.append(AuditFinding("fail", "broken_link", msg))
        if len(link_errors) > 10:
            findings.append(
                AuditFinding(
                    "fail",
                    "broken_link",
                    f"… and {len(link_errors) - 10} more broken link(s) in {slug}-index.md",
                )
            )
    else:
        findings.append(
            AuditFinding("pass", "links_ok", f"{slug}-index.md links resolve on disk")
        )

    for companion_path in shelf_utils.companion_paths(slug, base):
        findings.append(AuditFinding("pass", "companion_route", companion_path.name))
    index_body = read_text(index_path)
    for pattern in (f"{slug}-forecast-ledger", f"{slug}-interview-appearances"):
        if pattern.replace("-", " ") in index_body.lower() or pattern in index_body:
            if not shelf_utils.companion_paths(slug, base):
                findings.append(
                    AuditFinding("warn", "companion_missing", f"referenced but missing: {pattern}*.md")
                )
                break

    shelf_links = parse_shelf_index_links(index_path)
    missing_captures = [rel for _title, rel, dest in shelf_links if dest is None]
    if missing_captures:
        for rel in missing_captures:
            findings.append(AuditFinding("fail", "capture_missing", f"index links missing capture: {rel}"))
    else:
        findings.append(
            AuditFinding(
                "pass",
                "capture_links",
                f"{len(shelf_links)} archive capture link(s) resolve on disk",
            )
        )

    index_text = read_text(index_path)
    disk_captures = iter_archive_captures_for_shelf(slug, archive_root)
    eligible_count = 0
    unlisted = []
    for path in disk_captures:
        meta = parse_frontmatter(path)
        body_snip = read_text(path)[:8000] if path.is_file() else ""
        if shelf_utils.shelf_capture_excluded(slug, path, meta, body_snip):
            continue
        eligible_count += 1
        rel = _posix_rel(path)
        if path.name not in index_text and rel not in index_text:
            unlisted.append(rel)
    if unlisted:
        for rel in unlisted[:15]:
            findings.append(
                AuditFinding("warn", "archive_unlisted", f"archive capture not cited in {slug}-index.md: {rel}")
            )
        if len(unlisted) > 15:
            findings.append(
                AuditFinding(
                    "warn",
                    "archive_unlisted",
                    f"… and {len(unlisted) - 15} more {slug} archive capture(s) not cited",
                )
            )
    else:
        findings.append(
            AuditFinding(
                "pass",
                "archive_parity",
                f"all {eligible_count} eligible archive captures cited in index",
            )
        )

    return findings


def format_shelf_capture_table(
    scope_label: str,
    rows: list[ShelfCaptureRow],
    *,
    truncated: int,
    sort_key: SortKey,
) -> str:
    lines = [
        f"## Shelf capture inventory — {scope_label}",
        "",
        f"_Sorted by `{sort_key}`; links from `{scope_label}-index.md` to archive captures._",
        "",
        "| Date | Title | Capture | On disk |",
        "| --- | --- | --- | --- |",
    ]
    for row in rows:
        title = row.title.replace("|", "\\|")
        if len(title) > 56:
            title = title[:53] + "..."
        cap = row.capture_path
        if len(cap) > 52:
            cap = "…" + cap[-49:]
        disk = "yes" if row.on_disk else "no"
        lines.append(f"| {row.pub_date} | {title} | `{cap}` | {disk} |")
    if truncated:
        lines.append("")
        lines.append(f"_… and {truncated} more row(s); use `--table-limit 0` for full list._")
    lines.append("")
    lines.append(f"rows shown: {len(rows)}")
    return "\n".join(lines)


def audit_day_dir(day_dir: Path) -> list[AuditFinding]:
    findings: list[AuditFinding] = []
    if not day_dir.is_dir():
        findings.append(AuditFinding("fail", "missing_day", f"day directory not found: {day_dir}"))
        return findings

    disk_files = {p.name for p in iter_source_files(day_dir)}
    index_path = day_dir / DAY_INDEX_FILENAME
    parsed = None
    if not index_path.is_file():
        findings.append(AuditFinding("fail", "missing_index", f"missing {DAY_INDEX_FILENAME}"))
        indexed_files: set[str] = set()
    else:
        parsed = parse_day_readme(day_dir)
        indexed_files = set(parsed.file_names) if parsed else set()
        rendered = build_day_index(day_dir)
        existing = read_text(index_path)
        if existing != rendered:
            findings.append(
                AuditFinding("fail", "stale_index", f"{DAY_INDEX_FILENAME} stale vs recomputed build")
            )
        else:
            findings.append(AuditFinding("pass", "index_fresh", f"{DAY_INDEX_FILENAME} matches builder"))

    if disk_files != indexed_files:
        only_disk = sorted(disk_files - indexed_files)
        only_index = sorted(indexed_files - disk_files)
        parts: list[str] = []
        if only_disk:
            parts.append(f"on disk only: {', '.join(only_disk)}")
        if only_index:
            parts.append(f"in index only: {', '.join(only_index)}")
        findings.append(AuditFinding("fail", "parity", "; ".join(parts)))
    else:
        findings.append(AuditFinding("pass", "parity", f"Files list matches disk ({len(disk_files)} sources)"))

    readme_path = day_dir / "README.md"
    stub_expected = build_day_readme_stub(day_dir)
    if not readme_path.is_file():
        findings.append(AuditFinding("fail", "readme_stub", "README.md missing"))
    else:
        readme_text = read_text(readme_path)
        if readme_text != stub_expected:
            findings.append(AuditFinding("fail", "readme_stub", "README.md not day-index stub"))
        else:
            findings.append(AuditFinding("pass", "readme_stub", "README.md stub ok"))

    if parsed:
        live = summarize_day_dir(day_dir)
        if parsed.source_count != live.source_count:
            findings.append(
                AuditFinding(
                    "warn",
                    "stats_drift",
                    f"index source_count {parsed.source_count} vs live {live.source_count}",
                )
            )

    for path in iter_source_files(day_dir):
        meta = parse_frontmatter(path)
        for msg in capture_hygiene_warnings(path, meta):
            findings.append(AuditFinding("warn", "hygiene", msg))

    return findings


def audit_global(root: Path) -> list[AuditFinding]:
    findings: list[AuditFinding] = []
    import io
    from contextlib import redirect_stdout

    old_argv = sys.argv
    sys.argv = ["build_statecraft_archive_navigation.py", "--root", str(root), "--check"]
    buf = io.StringIO()
    try:
        with redirect_stdout(buf):
            code = nav.main()
    finally:
        sys.argv = old_argv
    output = buf.getvalue().strip()
    if code == 0:
        findings.append(
            AuditFinding("pass", "global_nav", output or "global navigation indices ok")
        )
    else:
        findings.append(
            AuditFinding("fail", "global_nav", output or "global navigation indices stale")
        )
    return findings


def format_findings(scope_label: str, findings: list[AuditFinding]) -> str:
    lines = [f"## Index audit — {scope_label}", ""]
    for level in ("pass", "fail", "warn"):
        bucket = [f for f in findings if f.level == level]
        if not bucket:
            continue
        label = level.upper()
        for item in bucket:
            lines.append(f"{label} [{item.code}] {item.message}")
    fails = sum(1 for f in findings if f.level == "fail")
    lines.append("")
    lines.append(f"exit {'1' if fails else '0'}")
    return "\n".join(lines)


def format_inventory_table(
    scope_label: str,
    rows: list[InventoryRow],
    *,
    truncated: int,
    sort_key: SortKey,
) -> str:
    lines = [
        f"## Index inventory — {scope_label}",
        "",
        f"_Sorted by `{sort_key}`; word count is transcript/body words (not comparable across kinds)._",
        "",
        "| Date | Title | URL | Words | Bucket | Kind | § |",
        "| --- | --- | --- | ---: | --- | --- | ---: |",
    ]
    for row in rows:
        title = row.title.replace("|", "\\|")
        if len(title) > 72:
            title = title[:69] + "..."
        url = row.source_url if row.source_url != "—" else "—"
        if len(url) > 48 and url != "—":
            url = url[:45] + "..."
        sec = str(row.sections) if row.sections is not None else "—"
        lines.append(
            f"| {row.pub_date} | {title} | {url} | {row.words} | {row.bucket} | {row.kind} | {sec} |"
        )
    if truncated:
        lines.append("")
        lines.append(f"_… and {truncated} more row(s); use `--table-limit 0` for full list._")
    lines.append("")
    lines.append(f"rows shown: {len(rows)}")
    return "\n".join(lines)


def resolve_day_dirs(root: Path, args: argparse.Namespace) -> tuple[list[Path], str]:
    if args.day:
        day_dir = root / args.day
        return [day_dir], args.day
    if args.month:
        day_dirs = day_idx.iter_day_dirs_for_scope(root, year=args.month[:4], month=args.month)
        return day_dirs, args.month
    if args.year:
        day_dirs = iter_day_dirs(root, args.year)
        return day_dirs, args.year
    return [], ""


def resolve_scope_name(args: argparse.Namespace) -> str:
    if args.global_audit:
        return "global"
    if args.channel_index:
        return "channel-index"
    if args.writer_index:
        return "writer-index"
    if args.voice_index:
        return "voice-index"
    if args.shelf_index:
        return "shelf-index"
    if args.day:
        return "day"
    if args.month:
        return "month"
    if args.year:
        return "year"
    return ""


def run_fix(root: Path, args: argparse.Namespace, day_dirs: list[Path]) -> None:
    if args.channel_index:
        run_fix_channel_index(root)
    elif args.writer_index:
        run_fix_writer_index(root)
    elif args.global_audit or args.month or args.year:
        old_argv = sys.argv
        sys.argv = ["build_statecraft_archive_navigation.py", "--root", str(root)]
        try:
            nav.main()
        finally:
            sys.argv = old_argv
    for day_dir in day_dirs:
        if day_dir.is_dir():
            day_idx.write_day_index(day_dir, check=False)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    scope = parser.add_mutually_exclusive_group()
    scope.add_argument("--day", metavar="YYYY-MM-DD", help="Audit one calendar day folder.")
    scope.add_argument("--month", metavar="YYYY-MM", help="Audit each day in month + inventory scope.")
    scope.add_argument("--year", metavar="YYYY", help="Inventory / audit all days in year.")
    scope.add_argument("--global", dest="global_audit", action="store_true", help="Global navigation stale check.")
    scope.add_argument(
        "--channel-index",
        action="store_true",
        help="Audit channel-index.md/json (+ misc) stale vs live YouTube captures.",
    )
    scope.add_argument(
        "--writer-index",
        action="store_true",
        help="Audit writer-index.md/json stale vs live prose captures.",
    )
    scope.add_argument(
        "--voice-index",
        action="store_true",
        help="Audit voice-index.md registry parity, links, and shelf coverage.",
    )
    scope.add_argument(
        "--shelf-index",
        metavar="SLUG",
        help="Audit curated voice shelf bench (e.g. parsi-index.md) vs archive captures.",
    )
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="Statecraft archive root.")
    parser.add_argument("--table", action="store_true", help="Append inventory table to output.")
    parser.add_argument("--table-only", action="store_true", help="Inventory table only; skip audit checks.")
    parser.add_argument(
        "--table-limit",
        type=int,
        default=None,
        help="Max table rows (0 = unlimited). Default: unlimited for --day, 50 for month/year.",
    )
    parser.add_argument(
        "--table-sort",
        choices=("date", "words", "title", "bucket"),
        default="date",
        help="Inventory row sort (default: date).",
    )
    parser.add_argument("--section", action="store_true", help="Run quantify_section_nav per day (audit mode).")
    parser.add_argument("--daily-sync", metavar="YYYY-MM-DD", help="Run intake vs daily synthesis sync.")
    parser.add_argument("--fix", action="store_true", help="Rebuild stale day-index / global navigation.")
    parser.add_argument("--json", action="store_true", help="JSON receipt.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    root = args.root.resolve()

    if (
        not args.global_audit
        and not args.channel_index
        and not args.writer_index
        and not args.voice_index
        and not args.shelf_index
        and not args.day
        and not args.month
        and not args.year
    ):
        print(
            "error: specify --day, --month, --year, --channel-index, --writer-index, "
            "--voice-index, --shelf-index SLUG, or --global",
            file=sys.stderr,
        )
        return 2

    day_dirs, scope_label = resolve_day_dirs(root, args)
    scope_kind = resolve_scope_name(args)

    if args.fix:
        if args.voice_index or args.shelf_index:
            curated = "voice-index.md" if args.voice_index else f"{args.shelf_index}-index.md"
            print(
                f"note: {curated} is curated; --fix skipped (edit manually)",
                file=sys.stderr,
            )
        else:
            run_fix(root, args, day_dirs)

    findings: list[AuditFinding] = []

    if args.channel_index:
        findings.extend(audit_channel_index(root))
        if not scope_label:
            scope_label = "channel-index (main roster)"

    if args.writer_index:
        findings.extend(audit_writer_index(root))
        if not scope_label:
            scope_label = "writer-index"

    if args.voice_index:
        findings.extend(audit_voice_index())
        if not scope_label:
            scope_label = "voice-index"

    if args.shelf_index:
        slug = args.shelf_index.strip().casefold()
        findings.extend(audit_shelf_index(slug, archive_root=root))
        if not scope_label:
            scope_label = f"{slug} shelf-index"

    if args.global_audit:
        findings.extend(audit_global(root))
        if not scope_label:
            scope_label = "global navigation"

    if not args.table_only and day_dirs:
        for day_dir in day_dirs:
            findings.extend(audit_day_dir(day_dir))

    if args.section and args.day:
        import quantify_section_nav as qsn

        qsn.main(["--day", args.day])

    if args.daily_sync:
        import check_statecraft_intake_daily_sync as daily_sync

        report = daily_sync.build_sync_report(args.daily_sync.strip(), root=root)
        if report.status == "desync":
            findings.append(
                AuditFinding("fail", "daily_sync", f"daily synthesis desync for {args.daily_sync}")
            )
        elif report.status == "ok":
            findings.append(AuditFinding("pass", "daily_sync", f"daily synthesis ok for {args.daily_sync}"))

    table_rows: list[InventoryRow] = []
    channel_table_rows: list[ChannelIndexRow] = []
    writer_table_rows: list[WriterIndexRow] = []
    voice_table_rows: list[VoiceIndexRow] = []
    shelf_table_rows: list[ShelfCaptureRow] = []
    truncated = 0
    roster_sort = map_channel_table_sort(args.table_sort)
    if (args.table or args.table_only) and args.channel_index:
        all_channel_rows = collect_channel_index_rows(root, misc=False)
        channel_table_rows = sort_channel_index_rows(all_channel_rows, roster_sort)
        limit = args.table_limit
        if limit is None:
            limit = default_table_limit(scope_kind) if scope_kind else DEFAULT_MONTH_YEAR_TABLE_LIMIT
        channel_table_rows, truncated = apply_table_limit(channel_table_rows, limit)
    elif (args.table or args.table_only) and args.writer_index:
        all_writer_rows = collect_writer_index_rows(root)
        writer_table_rows = sort_writer_index_rows(all_writer_rows, roster_sort)
        limit = args.table_limit
        if limit is None:
            limit = default_table_limit(scope_kind) if scope_kind else DEFAULT_MONTH_YEAR_TABLE_LIMIT
        writer_table_rows, truncated = apply_table_limit(writer_table_rows, limit)
    elif (args.table or args.table_only) and args.voice_index:
        all_voice_rows = collect_voice_index_rows()
        voice_table_rows = sort_voice_index_rows(all_voice_rows, roster_sort)
        limit = args.table_limit
        if limit is None:
            limit = default_table_limit(scope_kind) if scope_kind else DEFAULT_MONTH_YEAR_TABLE_LIMIT
        voice_table_rows, truncated = apply_table_limit(voice_table_rows, limit)
    elif (args.table or args.table_only) and args.shelf_index:
        slug = args.shelf_index.strip().casefold()
        all_shelf_rows = collect_shelf_capture_rows(slug, archive_root=root)
        shelf_table_rows = sort_shelf_capture_rows(all_shelf_rows, args.table_sort)
        limit = args.table_limit
        if limit is None:
            limit = default_table_limit(scope_kind) if scope_kind else DEFAULT_MONTH_YEAR_TABLE_LIMIT
        shelf_table_rows, truncated = apply_table_limit(shelf_table_rows, limit)
    elif (args.table or args.table_only) and day_dirs:
        all_rows = collect_inventory_rows(day_dirs)
        table_rows = sort_inventory_rows(all_rows, args.table_sort)
        limit = args.table_limit
        if limit is None:
            limit = default_table_limit(scope_kind) if scope_kind else DEFAULT_MONTH_YEAR_TABLE_LIMIT
        table_rows, truncated = apply_table_limit(table_rows, limit)
        if scope_kind == "year" and len(all_rows) > 200:
            findings.append(
                AuditFinding(
                    "warn",
                    "table_large",
                    "year scope exceeds 200 captures; prefer --month or raise --table-limit",
                )
            )

    exit_code = 1 if any(f.level == "fail" for f in findings) else 0

    if args.json:
        payload: dict[str, Any] = {
            "scope": scope_label,
            "exit_code": exit_code,
            "findings": [asdict(f) for f in findings],
            "table": [asdict(r) for r in table_rows],
            "channel_table": [asdict(r) for r in channel_table_rows],
            "writer_table": [asdict(r) for r in writer_table_rows],
            "voice_table": [asdict(r) for r in voice_table_rows],
            "shelf_table": [asdict(r) for r in shelf_table_rows],
            "table_truncated": truncated,
            "table_sort": args.table_sort,
        }
        print(json.dumps(payload, indent=2))
        return exit_code

    parts: list[str] = []
    if not args.table_only:
        parts.append(format_findings(scope_label, findings))
    if (args.table or args.table_only) and channel_table_rows:
        parts.append(
            format_channel_index_table(
                scope_label or "channel-index",
                channel_table_rows,
                truncated=truncated,
                sort_key=roster_sort,
            )
        )
    elif (args.table or args.table_only) and writer_table_rows:
        parts.append(
            format_writer_index_table(
                scope_label or "writer-index",
                writer_table_rows,
                truncated=truncated,
                sort_key=roster_sort,
            )
        )
    elif (args.table or args.table_only) and voice_table_rows:
        parts.append(
            format_voice_index_table(
                scope_label or "voice-index",
                voice_table_rows,
                truncated=truncated,
                sort_key=roster_sort,
            )
        )
    elif (args.table or args.table_only) and shelf_table_rows:
        slug = args.shelf_index.strip().casefold() if args.shelf_index else "shelf"
        parts.append(
            format_shelf_capture_table(
                slug,
                shelf_table_rows,
                truncated=truncated,
                sort_key=args.table_sort,
            )
        )
    elif args.table or args.table_only:
        inv_label = scope_label or "inventory"
        parts.append(format_inventory_table(inv_label, table_rows, truncated=truncated, sort_key=args.table_sort))
    print("\n\n".join(p for p in parts if p))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
