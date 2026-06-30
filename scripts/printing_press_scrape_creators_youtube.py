#!/usr/bin/env python3
"""Admit Printing Press scrape-creators YouTube transcript output.

V1 is a governed WORK-layer acquisition adapter. It accepts public YouTube
transcript/video metadata from a captured scrape-creators JSON payload, writes
the existing youtube-channel transcript layout, and emits a receipt. It does
not use credentials, cookies, comments, DMs, or Record surfaces.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
from repo_io import ARTIFACTS_DIR

from fetch_strategy_raw_input import _slugify  # noqa: E402
from youtube_transcripts.hashing import compute_content_hash  # noqa: E402

PIPELINE_VERSION = "printing-press-scrape-creators-v1"
DEFAULT_ARTIFACT_ROOT = ARTIFACTS_DIR / "printing-press" / "scrape-creators"
DEFAULT_CHANNEL_ROOT = REPO_ROOT / "research" / "external" / "youtube-channels"
INSTALL_HINT = (
    "Printing Press scrape-creators CLI not found. Install/review first, for example: "
    "npx -y @mvanhorn/printing-press install scrape-creators"
)
COMMENT_KEYS = {"comment", "comments", "replies", "reply_count", "comment_count"}
AUTH_KEYS = {
    "cookie",
    "cookies",
    "session",
    "session_cookie",
    "authenticated",
    "auth",
    "credential",
    "credentials",
    "token",
}

class AdmissionError(ValueError):
    """Unsafe or unsupported acquisition input."""

@dataclass(frozen=True)
class YouTubeTranscriptRecord:
    video_id: str
    title: str
    url: str
    transcript: str
    upload_date: str
    duration_seconds: float | None
    language: str
    fetched_at_utc: str

def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def find_scrape_creators_binary() -> str | None:
    explicit = os.environ.get("SCRAPE_CREATORS_BIN", "").strip()
    if explicit:
        return explicit if shutil.which(explicit) or Path(explicit).exists() else None
    for name in ("scrape-creators", "scrape-creators-pp-cli", "pp-scrape-creators"):
        found = shutil.which(name)
        if found:
            return found
    return None

def run_scrape_creators_fetch(url: str) -> dict[str, Any]:
    binary = find_scrape_creators_binary()
    if not binary:
        raise FileNotFoundError(INSTALL_HINT)
    template = os.environ.get(
        "SCRAPE_CREATORS_COMMAND_TEMPLATE",
        "{bin} youtube transcript --url {url} --json",
    )
    cmd = [part.format(bin=binary, url=url) for part in template.split()]
    proc = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or "scrape-creators failed")
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError("scrape-creators returned non-JSON output") from exc
    if not isinstance(data, dict):
        raise RuntimeError("scrape-creators JSON root must be an object")
    return data

def load_payload(path: Path | None, fetch_url: str | None) -> dict[str, Any]:
    if path and fetch_url:
        raise AdmissionError("Use only one of --input-json or --fetch-url")
    if path:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        if not isinstance(data, dict):
            raise AdmissionError("input JSON root must be an object")
        return data
    if fetch_url:
        return run_scrape_creators_fetch(fetch_url)
    raise AdmissionError("Provide --input-json or --fetch-url")

def iter_payload_items(payload: dict[str, Any]) -> list[dict[str, Any]]:
    for key in ("videos", "items", "results", "transcripts", "data"):
        value = payload.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
    return [payload]

def _string(item: dict[str, Any], *keys: str) -> str:
    for key in keys:
        value = item.get(key)
        if value is None:
            continue
        text = str(value).strip()
        if text:
            return text
    return ""

def _number(item: dict[str, Any], *keys: str) -> float | None:
    for key in keys:
        value = item.get(key)
        if value in (None, ""):
            continue
        try:
            return float(value)
        except (TypeError, ValueError):
            continue
    return None

def _transcript(item: dict[str, Any]) -> str:
    for key in ("transcript", "transcript_text", "caption_text", "captions", "text", "body"):
        value = item.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
        if isinstance(value, list):
            lines: list[str] = []
            for part in value:
                if isinstance(part, str):
                    lines.append(part.strip())
                elif isinstance(part, dict):
                    lines.append(str(part.get("text") or "").strip())
            text = "\n".join(line for line in lines if line)
            if text:
                return text
    return ""

def extract_video_id(item: dict[str, Any]) -> str:
    direct = _string(item, "video_id", "youtube_id", "id")
    if re.fullmatch(r"[A-Za-z0-9_-]{6,}", direct):
        return direct
    url = _string(item, "url", "source_url", "watch_url", "webpage_url")
    patterns = (
        r"[?&]v=([A-Za-z0-9_-]{6,})",
        r"youtu\.be/([A-Za-z0-9_-]{6,})",
        r"/shorts/([A-Za-z0-9_-]{6,})",
        r"/embed/([A-Za-z0-9_-]{6,})",
    )
    for pattern in patterns:
        m = re.search(pattern, url)
        if m:
            return m.group(1)
    raise AdmissionError("missing YouTube video_id")

def normalize_upload_date(raw: str, fallback: str) -> str:
    text = raw.strip()
    if re.fullmatch(r"\d{8}", text):
        return text
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        return text.replace("-", "")
    if text:
        try:
            return datetime.fromisoformat(text.replace("Z", "+00:00")).strftime("%Y%m%d")
        except ValueError:
            pass
    return fallback[:10].replace("-", "")

def _walk_has_key(obj: Any, keys: set[str]) -> bool:
    if isinstance(obj, dict):
        for key, value in obj.items():
            if str(key).lower() in keys and value not in (None, "", [], {}, False, 0):
                return True
            if _walk_has_key(value, keys):
                return True
    elif isinstance(obj, list):
        return any(_walk_has_key(item, keys) for item in obj)
    return False

def validate_public_youtube_only(item: dict[str, Any]) -> None:
    platform = _string(item, "platform", "source_platform", "service").lower()
    if platform and platform not in {"youtube", "yt"}:
        raise AdmissionError(f"unsupported platform for v1: {platform}")
    url = _string(item, "url", "source_url", "watch_url", "webpage_url")
    if url and "youtube.com" not in url and "youtu.be" not in url:
        raise AdmissionError("v1 accepts YouTube URLs only")
    kind = _string(item, "kind", "type", "content_type").lower()
    if "comment" in kind:
        raise AdmissionError("comments are excluded from v1")
    if _walk_has_key(item, COMMENT_KEYS):
        raise AdmissionError("comments/replies are excluded from v1")
    if _walk_has_key(item, AUTH_KEYS):
        raise AdmissionError("credentialed/cookie/session scraping is excluded from v1")

def normalize_record(item: dict[str, Any], *, fetched_at_utc: str) -> YouTubeTranscriptRecord:
    validate_public_youtube_only(item)
    video_id = extract_video_id(item)
    title = _string(item, "title", "name") or video_id
    url = _string(item, "url", "source_url", "watch_url", "webpage_url") or f"https://www.youtube.com/watch?v={video_id}"
    transcript = _transcript(item)
    if not transcript:
        raise AdmissionError(f"{video_id}: missing transcript text")
    language = _string(item, "language", "lang", "transcript_language") or "unknown"
    upload_date = normalize_upload_date(
        _string(item, "upload_date", "published_at", "published", "date"),
        fetched_at_utc,
    )
    return YouTubeTranscriptRecord(
        video_id=video_id,
        title=title,
        url=url,
        transcript=transcript,
        upload_date=upload_date,
        duration_seconds=_number(item, "duration_seconds", "duration", "length_seconds"),
        language=language,
        fetched_at_utc=fetched_at_utc,
    )

def normalize_payload(payload: dict[str, Any]) -> list[YouTubeTranscriptRecord]:
    fetched_at = _string(payload, "fetched_at_utc", "generated_at_utc") or utc_now()
    records = [normalize_record(item, fetched_at_utc=fetched_at) for item in iter_payload_items(payload)]
    if not records:
        raise AdmissionError("payload contained no video records")
    return records

def transcript_filename(record: YouTubeTranscriptRecord) -> str:
    return f"{record.video_id}_{_slugify(record.title, max_len=72)}.txt"

def transcript_text(record: YouTubeTranscriptRecord) -> str:
    header = [
        f"# source_url: {record.url}",
        f"# video_id: {record.video_id}",
        f"# title: {record.title}",
        f"# fetched_at_utc: {record.fetched_at_utc}",
        "# source_tier: printing_press_scrape_creators_public_youtube",
        "# pipeline_version: printing-press-scrape-creators-v1",
        "",
    ]
    return "\n".join(header) + record.transcript.strip() + "\n"

def index_row(record: YouTubeTranscriptRecord, transcript_rel: str) -> dict[str, Any]:
    body = transcript_text(record)
    return {
        "video_id": record.video_id,
        "title": record.title,
        "upload_date": record.upload_date,
        "duration_seconds": record.duration_seconds,
        "url": record.url,
        "transcript_file": transcript_rel,
        "status": "ok",
        "language": record.language,
        "error": None,
        "metadata_source": "printing-press/scrape-creators",
        "content_hash": compute_content_hash(record.video_id, body, PIPELINE_VERSION),
        "pipeline_version": PIPELINE_VERSION,
        "source_tier": "printing_press_scrape_creators_public_youtube",
        "quality": None,
        "fetched_at_utc": record.fetched_at_utc,
        "last_listing_seen_at": record.fetched_at_utc,
    }

def build_outputs(records: list[YouTubeTranscriptRecord], *, channel_slug: str, channel_url: str) -> tuple[dict[str, Any], dict[str, Any], list[tuple[str, str]]]:
    generated = utc_now()
    transcript_files: list[tuple[str, str]] = []
    rows: list[dict[str, Any]] = []
    manifest_videos: dict[str, Any] = {}
    for record in records:
        name = transcript_filename(record)
        rel = f"transcripts/{name}"
        body = transcript_text(record)
        row = index_row(record, rel)
        transcript_files.append((rel, body))
        rows.append(row)
        manifest_videos[record.video_id] = {
            "content_hash": row["content_hash"],
            "source_tier": row["source_tier"],
            "quality": row["quality"],
            "status": row["status"],
            "error": None,
            "last_updated_utc": generated,
            "last_successful_fetch_at_utc": record.fetched_at_utc,
        }
    index = {
        "channel_url": channel_url,
        "input_urls": sorted({record.url for record in records}),
        "pipeline_version": PIPELINE_VERSION,
        "generated_at_utc": generated,
        "video_count": len(rows),
        "transcripts_attempted": len(rows),
        "channel_slug": channel_slug,
        "source": "printing-press/scrape-creators",
        "videos": rows,
    }
    manifest = {
        "manifest_version": 1,
        "pipeline_version": PIPELINE_VERSION,
        "last_run_utc": generated,
        "videos": manifest_videos,
    }
    return index, manifest, transcript_files

def merge_existing_outputs(output_dir: Path, index: dict[str, Any], manifest: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    index_path = output_dir / "index.json"
    if index_path.exists():
        try:
            existing = json.loads(index_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            existing = {}
        old_videos = existing.get("videos") if isinstance(existing, dict) else None
        if isinstance(old_videos, list):
            by_id = {
                str(row.get("video_id") or ""): row
                for row in old_videos
                if isinstance(row, dict) and row.get("video_id")
            }
            for row in index["videos"]:
                by_id[str(row["video_id"])] = row
            index["videos"] = list(by_id.values())
            index["video_count"] = len(index["videos"])
            index["transcripts_attempted"] = len(index["videos"])
            old_inputs = existing.get("input_urls") if isinstance(existing, dict) else None
            if isinstance(old_inputs, list):
                index["input_urls"] = sorted(set(str(x) for x in old_inputs) | set(index["input_urls"]))

    manifest_path = output_dir / "transcript_manifest.json"
    if manifest_path.exists():
        try:
            existing_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            existing_manifest = {}
        old_manifest_videos = existing_manifest.get("videos") if isinstance(existing_manifest, dict) else None
        if isinstance(old_manifest_videos, dict):
            merged = dict(old_manifest_videos)
            merged.update(manifest["videos"])
            manifest["videos"] = merged
    return index, manifest

def write_outputs(
    records: list[YouTubeTranscriptRecord],
    *,
    channel_slug: str,
    channel_url: str,
    output_dir: Path,
    receipt_dir: Path,
    apply: bool,
) -> list[Path]:
    index, manifest, transcript_files = build_outputs(records, channel_slug=channel_slug, channel_url=channel_url)
    index, manifest = merge_existing_outputs(output_dir, index, manifest)
    changed: list[Path] = []
    planned: list[tuple[Path, str]] = [
        (output_dir / "index.json", json.dumps(index, indent=2, ensure_ascii=True) + "\n"),
        (output_dir / "transcript_manifest.json", json.dumps(manifest, indent=2, ensure_ascii=True) + "\n"),
    ]
    for rel, body in transcript_files:
        planned.append((output_dir / rel, body))
    receipt = {
        "receipt_type": "printing_press_scrape_creators_youtube_v1",
        "generated_at_utc": utc_now(),
        "channel_slug": channel_slug,
        "channel_url": channel_url,
        "record_count": len(records),
        "output_dir": str(output_dir.relative_to(REPO_ROOT) if output_dir.is_relative_to(REPO_ROOT) else output_dir),
        "guardrails": {
            "public_youtube_only": True,
            "comments": "excluded",
            "credentials_cookies_sessions": "excluded",
            "record_merge": "excluded",
        },
    }
    planned.append((receipt_dir / f"{channel_slug}-{receipt['generated_at_utc'].replace(':', '')}.json", json.dumps(receipt, indent=2, ensure_ascii=True) + "\n"))
    for path, content in planned:
        changed.append(path)
        if not apply:
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return changed

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input-json", type=Path, help="Captured scrape-creators JSON payload")
    ap.add_argument("--fetch-url", help="Public YouTube URL to fetch via installed scrape-creators CLI")
    ap.add_argument("--channel-slug", required=True)
    ap.add_argument("--channel-url", default="", help="Source channel URL; defaults to first record URL")
    ap.add_argument("--output-dir", type=Path, default=None)
    ap.add_argument("--receipt-dir", type=Path, default=DEFAULT_ARTIFACT_ROOT)
    ap.add_argument("--apply", action="store_true", help="Write files. Default is dry-run.")
    ap.add_argument("--include-comments", action="store_true", help=argparse.SUPPRESS)
    ap.add_argument("--use-cookies", action="store_true", help=argparse.SUPPRESS)
    ap.add_argument("--credentialed", action="store_true", help=argparse.SUPPRESS)
    return ap.parse_args(argv)

def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.include_comments:
        print("comments are excluded from v1", file=sys.stderr)
        return 2
    if args.use_cookies or args.credentialed:
        print("credentialed/cookie scraping is excluded from v1", file=sys.stderr)
        return 2
    try:
        payload = load_payload(args.input_json, args.fetch_url)
        records = normalize_payload(payload)
        channel_url = args.channel_url or records[0].url
        output_dir = args.output_dir or (DEFAULT_CHANNEL_ROOT / args.channel_slug)
        paths = write_outputs(
            records,
            channel_slug=args.channel_slug,
            channel_url=channel_url,
            output_dir=output_dir,
            receipt_dir=args.receipt_dir,
            apply=args.apply,
        )
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 127
    except AdmissionError as exc:
        print(f"admission rejected: {exc}", file=sys.stderr)
        return 2
    except (OSError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"scrape-creators adapter failed: {exc}", file=sys.stderr)
        return 1
    verb = "wrote" if args.apply else "would write"
    for path in paths:
        rel = path.relative_to(REPO_ROOT) if path.is_relative_to(REPO_ROOT) else path
        print(f"{verb}: {rel}")
    if not args.apply:
        print("dry-run only; pass --apply to write files")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
