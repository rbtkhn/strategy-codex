#!/usr/bin/env python3
"""Audit check-sources / YouTube channel coverage with durable receipts and scoreable ledgers.

Advisory automation only. Discovers channel uploads via the main channel-index roster
(``load_check_sources_roster``; misc excluded), reconciles against local
``source-archive/statecraft`` captures (and optional legacy ``raw-input``), classifies
each published object, and emits machine-readable completeness outputs. Never performs
ingest itself.

Legacy name: cognition-streams audit.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
from repo_io import ARTIFACTS_DIR

from youtube_transcripts.ytdlp_adapter import (  # noqa: E402
    fetch_video_metadata_import,
    fetch_video_metadata_subprocess,
    list_channel_entries_subprocess,
    normalize_duration_seconds,
    normalize_upload_date,
    watch_url,
)
from statecraft_youtube_discovery import (  # noqa: E402
    load_check_sources_roster,
    load_discovery_channels,
    resolve_discovery_config_path,
)
from statecraft_day_archive import (  # noqa: E402
    DEFAULT_ROOT as DEFAULT_ARCHIVE_ROOT,
    iter_all_day_dirs,
    iter_source_files,
    norm_scalar,
    parse_frontmatter,
)

DEFAULT_OUT_DIR = ARTIFACTS_DIR / "cognition-streams"
DEFAULT_NOTEBOOK_ROOT = REPO_ROOT / "codex" / str(date.today().year)
DEFAULT_RECEIPT_ROOT = REPO_ROOT / ".codex-tmp" / "cognition-streams"
MAIN_CLASSES = {"captured-main", "uncaptured-main", "deferred"}
PRIORITY_ORDER = {"must-capture": 0, "probably-capture": 1, "hide-default": 2, "none": 3}
DISCOVERY_SOURCE_ORDER = ["uploads_playlist", "channel_feed", "videos_page", "inventory_appendix"]
TOKEN_STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "from",
    "into",
    "after",
    "that",
    "this",
    "your",
    "their",
    "they",
    "have",
    "just",
    "will",
    "what",
    "when",
    "where",
    "iran",
    "war",
    "trump",
    "china",
    "live",
    "today",
    "deep",
    "dive",
    "dialogue",
    "works",
    "glenn",
    "diesen",
    "daniel",
    "davis",
    "alexander",
    "mercouris",
    "nima",
    "alkorshid",
}
NARROWER_CUES = {
    "today",
    "plans",
    "power",
    "fact",
    "debate",
    "pocketbooks",
    "visits",
    "ceasefire",
    "only",
    "hook",
    "blowing",
    "punch",
}
SHORT_TITLE_MARKERS = ("#short", " shorts", "shorts ", "(short", " clip", "snippet", "teaser")
BROAD_TOKEN_STOPWORDS = TOKEN_STOPWORDS - {"iran", "war", "trump", "china"}


@dataclass(frozen=True)
class ChannelSpec:
    channel_key: str
    channel_name: str
    channel_id: str
    uploads_playlist_id: str
    handle_url: str
    show: str
    host: str
    thread: str
    file_prefix: str
    discovery_priority: list[str]


def _parse_date(value: str) -> date:
    return date.fromisoformat(value)


def _window_slug(start: date, end: date) -> str:
    return f"{start.isoformat()}_to_{end.isoformat()}"


def _load_discovery_specs(path: Path | None = None) -> dict[str, ChannelSpec]:
    config_path = path or resolve_discovery_config_path()
    out: dict[str, ChannelSpec] = {}
    field_names = {field.name for field in ChannelSpec.__dataclass_fields__.values()}
    for row in load_discovery_channels(config_path):
        filtered = {key: row[key] for key in field_names if key in row}
        spec = ChannelSpec(**filtered)
        out[spec.channel_key] = spec
    return out


def _channel_id_from_url(url: str) -> str:
    match = re.search(r"/channel/(UC[\w-]+)", url or "")
    return match.group(1) if match else ""


def _normalize_handle_url(url: str) -> str:
    cleaned = (url or "").strip().rstrip("/")
    if cleaned.endswith("/videos"):
        return cleaned[: -len("/videos")]
    return cleaned


def _spec_from_roster_row(row: dict[str, Any], discovery: dict[str, ChannelSpec]) -> ChannelSpec | None:
    key = str(row.get("slug") or "").strip()
    if not key:
        return None
    if key in discovery:
        return discovery[key]
    handle_url = _normalize_handle_url(str(row.get("channel_url") or ""))
    channel_id = str(row.get("channel_id") or "").strip() or _channel_id_from_url(handle_url)
    if not handle_url and not channel_id:
        return None
    uploads = f"UU{channel_id[2:]}" if channel_id.startswith("UC") else ""
    label = str(row.get("label") or key)
    return ChannelSpec(
        channel_key=key,
        channel_name=label,
        channel_id=channel_id,
        uploads_playlist_id=uploads,
        handle_url=handle_url,
        show=label,
        host="",
        thread=key.replace("-", "_"),
        file_prefix=f"source-{key}",
        discovery_priority=list(DISCOVERY_SOURCE_ORDER),
    )


def _load_roster(
    *,
    archive_root: Path,
    watchlist_only: bool = False,
    discoverable_only: bool = True,
    watchlist_path: Path | None = None,
) -> dict[str, ChannelSpec]:
    """Build audit channel specs from check-sources roster + discovery config."""
    discovery = _load_discovery_specs(watchlist_path)
    json_path = archive_root / "channel-index.json"
    if not json_path.is_file():
        specs = discovery
        if watchlist_only:
            watchlist_keys = {
                str(row.get("channel_key") or "")
                for row in load_discovery_channels(watchlist_path)
                if row.get("daily_watchlist")
            }
            if watchlist_keys:
                specs = {key: spec for key, spec in specs.items() if key in watchlist_keys}
        return dict(sorted(specs.items()))

    roster_rows = load_check_sources_roster(root=archive_root, json_path=json_path)
    out: dict[str, ChannelSpec] = {}
    for row in roster_rows:
        if discoverable_only and not row.get("discoverable"):
            continue
        if watchlist_only and not row.get("watchlist"):
            continue
        spec = _spec_from_roster_row(row, discovery)
        if spec is not None:
            out[spec.channel_key] = spec
    return dict(sorted(out.items()))


def _load_watchlist(path: Path | None = None) -> dict[str, ChannelSpec]:
    """Daily watchlist subset (six ``daily_watchlist`` channels) via check-sources roster."""
    return _load_roster(
        archive_root=DEFAULT_ARCHIVE_ROOT,
        watchlist_only=True,
        watchlist_path=path,
    )


def _canonical_watch_url(value: str) -> str | None:
    raw = (value or "").strip()
    if not raw:
        return None
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", raw):
        return watch_url(raw)
    try:
        parsed = urllib.parse.urlparse(raw)
    except ValueError:
        return None
    host = parsed.netloc.lower()
    if "youtu.be" in host:
        vid = parsed.path.strip("/").split("/", 1)[0]
        return watch_url(vid) if re.fullmatch(r"[A-Za-z0-9_-]{11}", vid) else None
    if "youtube.com" in host:
        qs = urllib.parse.parse_qs(parsed.query)
        vid = (qs.get("v") or [""])[0]
        if re.fullmatch(r"[A-Za-z0-9_-]{11}", vid):
            return watch_url(vid)
    return raw.rstrip("/")


def _youtube_id_from_url(value: str) -> str | None:
    canonical = _canonical_watch_url(value)
    if not canonical:
        return None
    match = re.search(r"[?&]v=([A-Za-z0-9_-]{11})", canonical)
    return match.group(1) if match else None


def _parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    out: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" not in line:
            continue
        key, raw = line.split(":", 1)
        out[key.strip()] = raw.strip().strip("\"'")
    return out


def _scan_raw_input_index(notebook_root: Path) -> dict[str, list[str]]:
    raw_root = notebook_root / "raw-input"
    matches: dict[str, list[str]] = {}
    if not raw_root.is_dir():
        return matches
    for md in raw_root.rglob("*.md"):
        if md.name == "README.md":
            continue
        text = md.read_text(encoding="utf-8", errors="replace")
        fm = _parse_frontmatter(text)
        source_url = _canonical_watch_url(fm.get("source_url", ""))
        if source_url:
            matches.setdefault(source_url, []).append(str(md))
            video_id = _youtube_id_from_url(source_url)
            if video_id:
                matches.setdefault(video_id, []).append(str(md))
        raw_video_id = (fm.get("video_id") or "").strip()
        if raw_video_id:
            matches.setdefault(raw_video_id, []).append(str(md))
    return matches


def _scan_source_archive_index(archive_root: Path) -> dict[str, list[str]]:
    matches: dict[str, list[str]] = {}
    if not archive_root.is_dir():
        return matches
    for day_dir in iter_all_day_dirs(archive_root):
        for path in iter_source_files(day_dir):
            meta = parse_frontmatter(path)
            source_url = _canonical_watch_url(norm_scalar(meta.get("source_url")) or "")
            if source_url:
                matches.setdefault(source_url, []).append(str(path))
                video_id = _youtube_id_from_url(source_url)
                if video_id:
                    matches.setdefault(video_id, []).append(str(path))
            youtube_id = norm_scalar(meta.get("youtube_id")) or ""
            if youtube_id:
                matches.setdefault(youtube_id, []).append(str(path))
    return matches


def _merge_capture_indexes(*indexes: dict[str, list[str]]) -> dict[str, list[str]]:
    merged: dict[str, list[str]] = {}
    for index in indexes:
        for key, paths in index.items():
            merged.setdefault(key, []).extend(paths)
    for key, paths in merged.items():
        merged[key] = sorted({path for path in paths})
    return merged


def _guess_limit(start: date, end: date) -> int:
    days = max(1, (end - start).days + 1)
    return max(60, min(400, days * 25))


def _fetch_feed_entries(channel_id: str) -> list[dict[str, Any]]:
    feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    with urllib.request.urlopen(feed_url, timeout=20) as resp:
        xml_bytes = resp.read()
    root = ET.fromstring(xml_bytes)
    ns = {
        "atom": "http://www.w3.org/2005/Atom",
        "yt": "http://www.youtube.com/xml/schemas/2015",
    }
    rows: list[dict[str, Any]] = []
    for entry in root.findall("atom:entry", ns):
        video_id = (entry.findtext("yt:videoId", default="", namespaces=ns) or "").strip()
        title = (entry.findtext("atom:title", default="", namespaces=ns) or "").strip()
        published = (entry.findtext("atom:published", default="", namespaces=ns) or "").strip()
        rows.append(
            {
                "id": video_id,
                "title": title,
                "url": watch_url(video_id) if video_id else "",
                "upload_date": normalize_upload_date(published) or "",
                "duration_seconds": None,
                "live_status": "",
                "release_timestamp": None,
                "discovery_source": "channel_feed",
            }
        )
    return rows


def _fetch_metadata(video_id: str) -> dict[str, Any]:
    try:
        info = fetch_video_metadata_import(video_id)
    except Exception:
        try:
            info = fetch_video_metadata_subprocess(video_id, mode="binary")
        except Exception:
            info = fetch_video_metadata_subprocess(video_id, mode="module")
    upload_date = normalize_upload_date(str(info.get("upload_date") or "")) or ""
    duration = normalize_duration_seconds(info.get("duration"))
    timestamp = info.get("release_timestamp")
    release_timestamp = int(timestamp) if isinstance(timestamp, (int, float)) else None
    return {
        "id": video_id,
        "title": str(info.get("title") or video_id),
        "url": _canonical_watch_url(str(info.get("webpage_url") or info.get("url") or watch_url(video_id))) or watch_url(video_id),
        "upload_date": upload_date,
        "duration_seconds": duration,
        "live_status": str(info.get("live_status") or ""),
        "release_timestamp": release_timestamp,
        "is_live": bool(info.get("is_live")),
        "availability": str(info.get("availability") or ""),
    }


def _discover_channel_online(spec: ChannelSpec, start: date, end: date) -> dict[str, Any]:
    limit = _guess_limit(start, end)
    attempted: list[str] = []
    errors: list[dict[str, str]] = []
    base_rows: list[dict[str, Any]] = []
    used_source = ""

    playlist_url = f"https://www.youtube.com/playlist?list={spec.uploads_playlist_id}"
    try:
        attempted.append("uploads_playlist")
        playlist_rows = list_channel_entries_subprocess(playlist_url, limit=limit, cwd=REPO_ROOT)
        for row in playlist_rows:
            base_rows.append(
                {
                    "id": row["id"],
                    "title": row["title"],
                    "url": row["url"],
                    "upload_date": normalize_upload_date(row.get("upload_date") or "") or "",
                    "duration_seconds": normalize_duration_seconds(row.get("duration")),
                    "discovery_source": "uploads_playlist",
                }
            )
        used_source = "uploads_playlist"
    except Exception as exc:  # pragma: no cover
        errors.append({"source": "uploads_playlist", "error": str(exc)})

    if not base_rows:
        try:
            attempted.append("channel_feed")
            base_rows = _fetch_feed_entries(spec.channel_id)
            used_source = "channel_feed"
        except Exception as exc:  # pragma: no cover
            errors.append({"source": "channel_feed", "error": str(exc)})

    if not base_rows:
        try:
            attempted.append("videos_page")
            page_rows = list_channel_entries_subprocess(f"{spec.handle_url}/videos", limit=limit, cwd=REPO_ROOT)
            for row in page_rows:
                base_rows.append(
                    {
                        "id": row["id"],
                        "title": row["title"],
                        "url": row["url"],
                        "upload_date": normalize_upload_date(row.get("upload_date") or "") or "",
                        "duration_seconds": normalize_duration_seconds(row.get("duration")),
                        "discovery_source": "videos_page",
                    }
                )
            used_source = "videos_page"
        except Exception as exc:  # pragma: no cover
            errors.append({"source": "videos_page", "error": str(exc)})

    deduped: list[dict[str, Any]] = []
    seen: set[str] = set()
    for row in base_rows:
        video_id = (row.get("id") or "").strip()
        if not video_id or video_id in seen:
            continue
        seen.add(video_id)
        deduped.append(row)

    rows: list[dict[str, Any]] = []
    if deduped:
        with ThreadPoolExecutor(max_workers=8) as pool:
            futures = {pool.submit(_fetch_metadata, row["id"]): row for row in deduped}
            for fut in as_completed(futures):
                base = futures[fut]
                try:
                    meta = fut.result()
                except Exception as exc:  # pragma: no cover
                    errors.append({"source": used_source or base.get("discovery_source", ""), "error": f"{base['id']}: {exc}"})
                    meta = {
                        "id": base["id"],
                        "title": base["title"],
                        "url": base["url"],
                        "upload_date": base.get("upload_date") or "",
                        "duration_seconds": base.get("duration_seconds"),
                        "live_status": "",
                        "release_timestamp": None,
                        "is_live": False,
                        "availability": "",
                    }
                meta["discovery_source"] = base.get("discovery_source") or used_source or "uploads_playlist"
                rows.append(meta)

    def _row_date(row: dict[str, Any]) -> date | None:
        upload = normalize_upload_date(str(row.get("upload_date") or ""))
        if upload:
            return _parse_date(upload)
        ts = row.get("release_timestamp")
        if isinstance(ts, int) and ts > 0:
            return datetime.utcfromtimestamp(ts).date()
        return None

    filtered = []
    for row in rows:
        row_date = _row_date(row)
        if row_date and (row_date < start or row_date > end):
            continue
        row["date"] = row_date.isoformat() if row_date else ""
        filtered.append(row)

    filtered.sort(key=lambda item: (item.get("date") or "", item.get("id") or ""))
    return {
        "channel_key": spec.channel_key,
        "channel_name": spec.channel_name,
        "window": {"start": start.isoformat(), "end": end.isoformat()},
        "sources_attempted": attempted,
        "source_used": used_source,
        "errors": errors,
        "items": filtered,
    }


def _load_receipt(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def _tokenize_title(title: str) -> set[str]:
    words = re.findall(r"[a-z0-9]+", title.lower())
    return {w for w in words if len(w) >= 3 and w not in TOKEN_STOPWORDS}


def _lead_subject_tokens(title: str) -> set[str]:
    lead = re.split(r"[:|/\\-]", title, maxsplit=1)[0]
    return _tokenize_title(lead)


def _topic_tokens(title: str) -> set[str]:
    words = re.findall(r"[a-z0-9]+", title.lower())
    return {w for w in words if len(w) >= 3 and w not in BROAD_TOKEN_STOPWORDS}


def _is_hidden_short(row: dict[str, Any]) -> bool:
    title = str(row.get("title") or "").lower()
    duration = row.get("duration_seconds")
    if isinstance(duration, int) and duration < 180:
        return True
    return any(marker in title for marker in SHORT_TITLE_MARKERS)


def _is_upcoming(row: dict[str, Any]) -> bool:
    live_status = str(row.get("live_status") or "").lower()
    availability = str(row.get("availability") or "").lower()
    if live_status in {"is_upcoming", "is_live"}:
        return True
    if "upcoming" in availability:
        return True
    return False


def _find_companion_parent(row: dict[str, Any], peers: list[dict[str, Any]]) -> tuple[dict[str, Any] | None, str | None]:
    channel_key = str(row.get("channel_key") or "")
    if channel_key in {"glenn-diesen", "alexander-mercouris", "alex-mercouris"}:
        return None, None

    title = str(row.get("title") or "")
    tokens = _tokenize_title(title)
    lead_tokens = _lead_subject_tokens(title)
    duration = row.get("duration_seconds") or 0
    if not isinstance(duration, int):
        duration = 0

    best_parent: dict[str, Any] | None = None
    best_reason: str | None = None
    best_score = -1
    for candidate in peers:
        if candidate is row:
            continue
        cand_duration = candidate.get("duration_seconds") or 0
        if not isinstance(cand_duration, int):
            cand_duration = 0
        if cand_duration <= duration:
            continue
        if cand_duration < duration + 240 and cand_duration < int(duration * 1.2):
            continue

        cand_title = str(candidate.get("title") or "")
        cand_tokens = _tokenize_title(cand_title)
        cand_lead_tokens = _lead_subject_tokens(cand_title)
        topic_overlap = len(_topic_tokens(title) & _topic_tokens(cand_title))
        overlap = len(tokens & cand_tokens)
        lead_overlap = len(lead_tokens & cand_lead_tokens)
        narrower = len(tokens & NARROWER_CUES) > 0

        if channel_key in {"daniel-davis", "daniel-davis-deep-dive"}:
            if lead_overlap >= 1 and cand_duration >= duration + 300:
                score = 10 + lead_overlap + overlap
                if score > best_score:
                    best_parent = candidate
                    best_score = score
                    best_reason = "same-day guest overlap with longer Davis item"
                continue
            if topic_overlap >= 1 and narrower and cand_duration >= duration + 300:
                score = 6 + topic_overlap + overlap
                if score > best_score:
                    best_parent = candidate
                    best_score = score
                    best_reason = "same-day narrower Davis companion"
                continue
        else:
            if overlap >= 3 and narrower and cand_duration >= duration + 300:
                score = 5 + overlap
                if score > best_score:
                    best_parent = candidate
                    best_score = score
                    best_reason = "same-day shorter overlap companion"

    return best_parent, best_reason


def _classify_rows(
    discovered_rows: list[dict[str, Any]],
    raw_index: dict[str, list[str]],
    recent_start: date,
) -> list[dict[str, Any]]:
    by_day_channel: dict[tuple[str, str], list[dict[str, Any]]] = {}
    rows: list[dict[str, Any]] = []

    for row in discovered_rows:
        by_day_channel.setdefault((str(row.get("date") or ""), str(row.get("channel_key") or "")), []).append(row)

    for row in discovered_rows:
        date_str = str(row.get("date") or "")
        channel_key = str(row.get("channel_key") or "")
        url = _canonical_watch_url(str(row.get("url") or "")) or watch_url(str(row.get("youtube_id") or row.get("id") or ""))
        video_id = str(row.get("youtube_id") or row.get("id") or _youtube_id_from_url(url) or "")
        matched_paths = raw_index.get(video_id, []) + raw_index.get(url, [])
        deduped_paths = sorted({p for p in matched_paths})
        captured = 1 if deduped_paths else 0

        classification = ""
        confidence = "high"
        priority = "none"
        notes: list[str] = []
        same_day_parent_id = ""

        if _is_upcoming(row):
            classification = "upcoming"
            priority = "none"
            notes.append("scheduled live or not-yet-aired object")
        elif _is_hidden_short(row):
            classification = "hidden-short"
            priority = "hide-default"
            notes.append("short-form or clip-style object")
        else:
            peers = [
                peer
                for peer in by_day_channel.get((date_str, channel_key), [])
                if not _is_upcoming(peer) and not _is_hidden_short(peer)
            ]
            parent, reason = _find_companion_parent(row, peers)
            if parent is not None:
                classification = "hidden-companion"
                confidence = "high" if channel_key in {"daniel-davis", "daniel-davis-deep-dive"} else "medium"
                priority = "hide-default"
                same_day_parent_id = str(parent.get("youtube_id") or parent.get("id") or "")
                if reason:
                    notes.append(reason)
            else:
                classification = "captured-main" if captured else "uncaptured-main"
                is_recent = bool(date_str) and _parse_date(date_str) >= recent_start
                priority = "must-capture" if (classification == "uncaptured-main" and is_recent) else (
                    "probably-capture" if classification == "uncaptured-main" else "none"
                )
                notes.append("main upload present in capture index" if captured else "main upload missing from capture index")

        rows.append(
            {
                "date": date_str,
                "channel_key": channel_key,
                "channel_name": row.get("channel_name") or "",
                "youtube_id": video_id,
                "title": row.get("title") or "",
                "url": url,
                "duration_seconds": row.get("duration_seconds"),
                "discovery_source": row.get("discovery_source") or "",
                "classification": classification,
                "classification_confidence": confidence,
                "priority": priority,
                "captured": captured,
                "raw_input_path": deduped_paths[0] if deduped_paths else "",
                "raw_input_paths": deduped_paths,
                "same_day_parent_id": same_day_parent_id,
                "notes": "; ".join(notes),
            }
        )

    rows.sort(key=lambda item: (item["date"], item["channel_key"], item["youtube_id"]))
    return rows


def _bucket_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    main_rows = [row for row in rows if row["classification"] in MAIN_CLASSES]
    captured_main = [row for row in rows if row["classification"] == "captured-main"]
    return {
        "rows": len(rows),
        "main_total": len(main_rows),
        "captured_main": len(captured_main),
        "coverage_pct": round((len(captured_main) / len(main_rows)) if main_rows else 0.0, 4),
        "must_capture_remaining": sum(1 for row in rows if row["priority"] == "must-capture" and not row["captured"]),
    }


def _derive_status(overall_pct: float, recent_pct: float, must_capture_remaining: int) -> str:
    if overall_pct >= 0.70 and recent_pct >= 0.90 and must_capture_remaining == 0:
        return "complete"
    if overall_pct >= 0.70 and recent_pct >= 0.90:
        return "meets-overall-and-recent"
    if overall_pct >= 0.70:
        return "meets-overall-only"
    return "below-threshold"


def _derive_target_status(target: dict[str, Any]) -> str:
    if target["main_total"] == 0:
        return "no-target-items"
    if target["coverage_pct"] >= 0.90 and target["must_capture_remaining"] == 0:
        return "complete"
    if target["must_capture_remaining"] == 0:
        return "must-captures-clear"
    if target["coverage_pct"] >= 0.90:
        return "coverage-ok-with-must-captures"
    return "below-threshold"


def _row_date_in_window(row: dict[str, Any], start: date, end: date) -> bool:
    raw = str(row.get("date") or "").strip()
    if not raw:
        return False
    try:
        row_date = _parse_date(raw)
    except ValueError:
        return False
    return start <= row_date <= end


def _compute_summary(rows: list[dict[str, Any]], recent_start: date, target_start: date, target_end: date) -> dict[str, Any]:
    overall = _bucket_summary(rows)
    recent_rows = [row for row in rows if row["date"] and _parse_date(row["date"]) >= recent_start]
    recent = _bucket_summary(recent_rows)
    target_rows = [row for row in rows if _row_date_in_window(row, target_start, target_end)]
    target = _bucket_summary(target_rows)

    per_date: dict[str, list[dict[str, Any]]] = {}
    per_channel: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        per_date.setdefault(row["date"], []).append(row)
        per_channel.setdefault(row["channel_key"], []).append(row)

    summary = {
        "main_total": overall["main_total"],
        "captured_main": overall["captured_main"],
        "overall_pct": overall["coverage_pct"],
        "recent_main_total": recent["main_total"],
        "recent_captured_main": recent["captured_main"],
        "recent_pct": recent["coverage_pct"],
        "must_capture_remaining": overall["must_capture_remaining"],
        "benchmark": {
            "overall_pct_min": 0.70,
            "recent_pct_min": 0.90,
            "must_capture_remaining_max": 0,
        },
        "status": _derive_status(overall["coverage_pct"], recent["coverage_pct"], overall["must_capture_remaining"]),
        "overall_backlog_status": _derive_status(
            overall["coverage_pct"], recent["coverage_pct"], overall["must_capture_remaining"]
        ),
        "target_window": {
            "start": target_start.isoformat(),
            "end": target_end.isoformat(),
        },
        "target_window_status": _derive_target_status(target),
        "target_window_main_total": target["main_total"],
        "target_window_captured_main": target["captured_main"],
        "target_window_pct": target["coverage_pct"],
        "target_window_must_capture_remaining": target["must_capture_remaining"],
        "per_date": {key: _bucket_summary(bucket) for key, bucket in sorted(per_date.items())},
        "per_channel": {key: _bucket_summary(bucket) for key, bucket in sorted(per_channel.items())},
    }
    if target_start == target_end:
        summary.update(
            {
                "target_date": target_start.isoformat(),
                "target_date_status": summary["target_window_status"],
                "target_date_main_total": summary["target_window_main_total"],
                "target_date_captured_main": summary["target_window_captured_main"],
                "target_date_pct": summary["target_window_pct"],
                "target_date_must_capture_remaining": summary["target_window_must_capture_remaining"],
            }
        )
    return summary


def _render_queue_markdown(queue_groups: dict[str, list[dict[str, Any]]]) -> str:
    lines = ["# Check-sources repair queue", ""]
    for label in ("must-capture", "probably-capture"):
        rows = queue_groups.get(label, [])
        lines.append(f"## {label}")
        lines.append("")
        if not rows:
            lines.append("_None._")
            lines.append("")
            continue
        for row in rows:
            row_date = row["date"] or "undated"
            lines.append(
                f"- `{row_date}` `{row['channel_key']}` `{row['youtube_id']}` "
                f"[{row['title']}]({row['url']})"
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _write_ledger(rows: list[dict[str, Any]], output_dir: Path, fmt: str) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    written: dict[str, str] = {}

    jsonl_path = output_dir / "coverage-ledger.jsonl"
    with jsonl_path.open("w", encoding="utf-8", newline="") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=True) + "\n")
    written["jsonl"] = str(jsonl_path)

    if fmt == "csv":
        csv_path = output_dir / "coverage-ledger.csv"
        fieldnames = list(rows[0].keys()) if rows else [
            "date",
            "channel_key",
            "channel_name",
            "youtube_id",
            "title",
            "url",
            "duration_seconds",
            "discovery_source",
            "classification",
            "classification_confidence",
            "priority",
            "captured",
            "raw_input_path",
            "raw_input_paths",
            "same_day_parent_id",
            "notes",
        ]
        with csv_path.open("w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        written["format"] = str(csv_path)
    elif fmt == "md":
        md_path = output_dir / "coverage-ledger.md"
        header = [
            "| date | channel_key | youtube_id | classification | priority | captured | title |",
            "|---|---|---|---|---|---:|---|",
        ]
        body = [
            f"| {row['date']} | {row['channel_key']} | `{row['youtube_id']}` | {row['classification']} | {row['priority']} | {row['captured']} | {row['title']} |"
            for row in rows
        ]
        md_path.write_text("\n".join(header + body) + "\n", encoding="utf-8")
        written["format"] = str(md_path)
    else:
        written["format"] = str(jsonl_path)

    return written


def run_audit(
    *,
    start: date,
    end: date,
    recent_start: date,
    channel_keys: list[str] | None,
    out_dir: Path,
    archive_root: Path,
    notebook_root: Path,
    fmt: str,
    offline: bool,
    receipt_root: Path = DEFAULT_RECEIPT_ROOT,
    watchlist_path: Path | None = None,
    roster: str = "watchlist",
    capture_surface: str = "archive",
) -> dict[str, Any]:
    watchlist_only = roster == "watchlist"
    roster_specs = _load_roster(
        archive_root=archive_root,
        watchlist_only=watchlist_only,
        watchlist_path=watchlist_path,
    )
    if channel_keys:
        selected = [roster_specs[key] for key in channel_keys if key in roster_specs]
    else:
        selected = list(roster_specs.values())
    window = _window_slug(start, end)
    receipt_dir = receipt_root / window
    output_dir = out_dir / window

    capture_indexes: list[dict[str, list[str]]] = []
    if capture_surface in {"archive", "both"}:
        capture_indexes.append(_scan_source_archive_index(archive_root))
    if capture_surface in {"raw-input", "both"}:
        capture_indexes.append(_scan_raw_input_index(notebook_root))
    capture_index = _merge_capture_indexes(*capture_indexes) if capture_indexes else {}
    discovered_rows: list[dict[str, Any]] = []
    receipt_manifest: dict[str, str] = {}
    for spec in selected:
        receipt_path = receipt_dir / f"{spec.channel_key}.discovery.json"
        receipt = _load_receipt(receipt_path) if offline else _discover_channel_online(spec, start, end)
        if not offline:
            _write_json(receipt_path, receipt)
        receipt_manifest[spec.channel_key] = str(receipt_path)
        for item in receipt.get("items") or []:
            discovered_rows.append(
                {
                    "date": item.get("date") or item.get("upload_date") or "",
                    "channel_key": spec.channel_key,
                    "channel_name": spec.channel_name,
                    "youtube_id": item.get("id") or item.get("youtube_id") or "",
                    "title": item.get("title") or "",
                    "url": item.get("url") or "",
                    "duration_seconds": normalize_duration_seconds(item.get("duration_seconds")),
                    "discovery_source": item.get("discovery_source") or receipt.get("source_used") or "",
                    "live_status": item.get("live_status") or "",
                    "release_timestamp": item.get("release_timestamp"),
                    "availability": item.get("availability") or "",
                }
            )

    rows = _classify_rows(discovered_rows, capture_index, recent_start)
    summary = _compute_summary(rows, recent_start, start, end)
    summary["roster_scope"] = roster
    summary["roster_channel_count"] = len(selected)
    summary["capture_surface"] = capture_surface
    queue_rows = [row for row in rows if row["priority"] in {"must-capture", "probably-capture"} and not row["captured"]]
    queue_rows.sort(key=lambda row: (PRIORITY_ORDER[row["priority"]], row["date"], row["channel_key"], row["youtube_id"]))
    queue_groups = {
        "must-capture": [row for row in queue_rows if row["priority"] == "must-capture"],
        "probably-capture": [row for row in queue_rows if row["priority"] == "probably-capture"],
    }

    ledger_paths = _write_ledger(rows, output_dir, fmt)
    _write_json(output_dir / "summary.json", summary)
    _write_json(output_dir / "repair-queue.json", queue_groups)
    (output_dir / "repair-queue.md").write_text(_render_queue_markdown(queue_groups), encoding="utf-8")
    _write_json(output_dir / "receipt-manifest.json", receipt_manifest)

    return {
        "window": window,
        "receipt_dir": str(receipt_dir),
        "output_dir": str(output_dir),
        "ledger_paths": ledger_paths,
        "summary": summary,
        "queue_groups": queue_groups,
        "receipt_manifest": receipt_manifest,
        "roster_scope": roster,
        "roster_channel_keys": [spec.channel_key for spec in selected],
    }


def _build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--start", required=True, help="YYYY-MM-DD")
    ap.add_argument("--end", required=True, help="YYYY-MM-DD")
    ap.add_argument("--recent-start", required=True, help="YYYY-MM-DD")
    ap.add_argument("--channel", action="append", default=[], help="Repeatable channel_key filter")
    ap.add_argument(
        "--roster",
        choices=("watchlist", "main"),
        default="watchlist",
        help="Channel scope: daily watchlist (6) or full main channel-index roster (misc excluded)",
    )
    ap.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR, help="Durable output root")
    ap.add_argument(
        "--archive-root",
        type=Path,
        default=DEFAULT_ARCHIVE_ROOT,
        help="Statecraft source-archive root for roster + capture reconciliation",
    )
    ap.add_argument(
        "--notebook-root",
        type=Path,
        default=DEFAULT_NOTEBOOK_ROOT,
        help="Legacy strategy notebook root (raw-input when --capture-surface includes raw-input)",
    )
    ap.add_argument(
        "--capture-surface",
        choices=("archive", "raw-input", "both"),
        default="archive",
        help="Local capture truth: source-archive (default), legacy raw-input, or both",
    )
    ap.add_argument("--format", choices=("jsonl", "csv", "md"), default="jsonl", help="Ledger export format")
    ap.add_argument("--offline", action="store_true", help="Score from existing receipts without fetching discovery")
    return ap


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    result = run_audit(
        start=_parse_date(args.start),
        end=_parse_date(args.end),
        recent_start=_parse_date(args.recent_start),
        channel_keys=args.channel or None,
        out_dir=args.out_dir,
        archive_root=args.archive_root,
        notebook_root=args.notebook_root,
        fmt=args.format,
        offline=args.offline,
        roster=args.roster,
        capture_surface=args.capture_surface,
    )
    print(json.dumps(result["summary"], indent=2, ensure_ascii=True))
    print(f"Receipts: {result['receipt_dir']}", file=sys.stderr)
    print(f"Outputs: {result['output_dir']}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
