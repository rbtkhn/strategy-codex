#!/usr/bin/env python3
"""Atomically materialize approved YouTube URLs into strategy-codex raw-input.

WORK only; not Record. This script consumes operator-approved URLs. It does
not decide which stream items deserve capture.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from yaml_compat import safe_dump, safe_load_text  # noqa: E402
import build_speaker_memory_actions as speaker_actions  # noqa: E402
import build_speaker_routing_queue as speaker_routing  # noqa: E402
import host_shelf_quality  # noqa: E402
from youtube_transcripts.discovery import extract_video_id  # noqa: E402
from youtube_transcripts.metadata import fetch_metadata_ytdlp  # noqa: E402
from youtube_transcripts.subtitles_ytdlp import fetch_subtitles_ytdlp  # noqa: E402
from youtube_transcripts.ytdlp_adapter import (  # noqa: E402
    fetch_video_metadata_subprocess,
    normalize_upload_date,
    watch_url,
)

WATCHLIST_PATH = (
    REPO_ROOT
    / "docs"
    / "skill-work"
    / "work-strategy"
    / "cognition-streams-watchlist.json"
)
DEFAULT_NOTEBOOK_ROOT = REPO_ROOT / "codex" / "years" / str(date.today().year)
DEFAULT_RECEIPT_ROOT = REPO_ROOT / ".codex-tmp" / "youtube-raw-input"
DEFAULT_ROUTING_OUT = REPO_ROOT / "artifacts" / "speaker-routing"
DEFAULT_ACTION_OUT = REPO_ROOT / "artifacts" / "speaker-memory-actions"
DEFAULT_HOST_QUALITY_OUT = REPO_ROOT / "artifacts" / "host-shelf-quality"
MIN_BODY_WORDS = 75
MIN_BODY_CHARS = 400
PRIMARY_LANGS = ["en.*"]
FALLBACK_LANGS = ["en.*", "en", "en-US", "en-orig"]
PLACEHOLDER_PATTERNS = (
    "transcript pending",
    "caption pending",
    "body absent",
    "placeholder transcript",
    "stub transcript",
    "index-only",
    "listed_only",
    "todo: transcript",
    "no transcript available",
    "paste full transcript",
    "paste transcript body",
)


@dataclass(frozen=True)
class WatchlistSpec:
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


@dataclass(frozen=True)
class ApprovedUrl:
    url: str
    show: str | None = None
    host: str | None = None
    thread: str | None = None
    channel_slug: str | None = None
    file_prefix: str | None = None
    guest: str | None = None
    pub_date: str | None = None
    title: str | None = None


@dataclass(frozen=True)
class VerificationResult:
    ok: bool
    reason: str
    word_count: int
    body_chars: int
    frontmatter: dict[str, Any]


@dataclass(frozen=True)
class YtdlpAuth:
    cookies: Path | None = None
    cookies_from_browser: str | None = None


def slugify(text: str, *, max_len: int = 72) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower())
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug[:max_len].rstrip("-") or "youtube"


def canonical_watch_url(value: str) -> str:
    video_id = extract_video_id(value)
    return watch_url(video_id) if video_id else value.strip()


def load_watchlist(path: Path = WATCHLIST_PATH) -> dict[str, WatchlistSpec]:
    data = json.loads(path.read_text(encoding="utf-8"))
    out: dict[str, WatchlistSpec] = {}
    for row in data.get("channels") or []:
        spec = WatchlistSpec(**row)
        out[spec.channel_key] = spec
    return out


def _norm(value: object) -> str:
    return str(value or "").strip().lower()


def infer_watchlist_spec(info: dict[str, Any], watchlist: dict[str, WatchlistSpec]) -> WatchlistSpec | None:
    channel_id = _norm(info.get("channel_id") or info.get("uploader_id"))
    channel_url = _norm(info.get("channel_url") or info.get("uploader_url"))
    channel = _norm(info.get("channel") or info.get("uploader"))
    for spec in watchlist.values():
        if channel_id and channel_id == spec.channel_id.lower():
            return spec
        if channel_url and channel_url.rstrip("/") == spec.handle_url.lower().rstrip("/"):
            return spec
        if channel and channel in {spec.channel_name.lower(), spec.show.lower()}:
            return spec
    return None


def load_approved_urls(path: Path | None, urls: list[str]) -> list[ApprovedUrl]:
    items = [ApprovedUrl(url=url) for url in urls]
    if not path:
        return items
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("{"):
            data = json.loads(line)
            url = str(data.get("url") or data.get("source_url") or "").strip()
            if not url:
                raise ValueError(f"JSONL row missing url: {line}")
            items.append(
                ApprovedUrl(
                    url=url,
                    show=data.get("show"),
                    host=data.get("host"),
                    thread=data.get("thread"),
                    channel_slug=data.get("channel_slug"),
                    file_prefix=data.get("file_prefix"),
                    guest=data.get("guest"),
                    pub_date=data.get("pub_date"),
                    title=data.get("title"),
                )
            )
        else:
            items.append(ApprovedUrl(url=line))
    return items


def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    raw = text[4:end]
    body_start = end + len("\n---")
    if body_start < len(text) and text[body_start : body_start + 1] == "\n":
        body_start += 1
    try:
        parsed = safe_load_text(raw, feature="materialize_youtube_raw_input.py")
    except Exception:
        return {}, text[body_start:]
    return (parsed if isinstance(parsed, dict) else {}), text[body_start:]


def verify_raw_input_text(text: str) -> VerificationResult:
    frontmatter, body = split_frontmatter(text)
    body_stripped = effective_body_text(body)
    body_words = re.findall(r"\b[\w'-]+\b", body_stripped)
    body_lower = body_stripped.lower()

    required = ("source_url", "pub_date", "title")
    missing = [key for key in required if not str(frontmatter.get(key) or "").strip()]
    if missing:
        return VerificationResult(False, f"missing frontmatter: {', '.join(missing)}", len(body_words), len(body_stripped), frontmatter)
    if not (frontmatter.get("source_note") or frontmatter.get("editorial_note")):
        return VerificationResult(False, "missing provenance note", len(body_words), len(body_stripped), frontmatter)
    if not frontmatter.get("source_type"):
        return VerificationResult(False, "missing source_type", len(body_words), len(body_stripped), frontmatter)
    if not frontmatter.get("transcript_type"):
        return VerificationResult(False, "missing transcript_type", len(body_words), len(body_stripped), frontmatter)
    for pattern in PLACEHOLDER_PATTERNS:
        if pattern in body_lower:
            return VerificationResult(False, f"placeholder body: {pattern}", len(body_words), len(body_stripped), frontmatter)
    if len(body_words) < MIN_BODY_WORDS:
        return VerificationResult(False, f"body too short: {len(body_words)} words", len(body_words), len(body_stripped), frontmatter)
    if len(body_stripped) < MIN_BODY_CHARS:
        return VerificationResult(False, f"body too short: {len(body_stripped)} chars", len(body_words), len(body_stripped), frontmatter)
    return VerificationResult(True, "ok", len(body_words), len(body_stripped), frontmatter)


def verify_existing_raw_input_for_appearance(text: str) -> VerificationResult:
    strict = verify_raw_input_text(text)
    if strict.ok:
        return strict
    frontmatter, body = split_frontmatter(text)
    body_stripped = effective_body_text(body)
    body_words = re.findall(r"\b[\w'-]+\b", body_stripped)
    body_lower = body_stripped.lower()
    required = ("source_url", "pub_date", "title")
    missing = [key for key in required if not str(frontmatter.get(key) or "").strip()]
    if missing:
        return VerificationResult(False, f"missing frontmatter: {', '.join(missing)}", len(body_words), len(body_stripped), frontmatter)
    for pattern in PLACEHOLDER_PATTERNS:
        if pattern in body_lower:
            return VerificationResult(False, f"placeholder body: {pattern}", len(body_words), len(body_stripped), frontmatter)
    if len(body_words) < MIN_BODY_WORDS:
        return VerificationResult(False, f"body too short: {len(body_words)} words", len(body_words), len(body_stripped), frontmatter)
    if len(body_stripped) < MIN_BODY_CHARS:
        return VerificationResult(False, f"body too short: {len(body_stripped)} chars", len(body_words), len(body_stripped), frontmatter)
    return VerificationResult(
        True,
        f"appearance-eligible legacy raw-input ({strict.reason})",
        len(body_words),
        len(body_stripped),
        frontmatter,
    )


def effective_body_text(body: str) -> str:
    lines = body.splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and re.match(r"^\s{0,3}#{1,6}\s+", lines[0]):
        lines.pop(0)
        while lines and not lines[0].strip():
            lines.pop(0)
    return "\n".join(lines).strip()


def classify_evidence_grade(frontmatter: dict[str, Any], verification_reason: str = "") -> str:
    return speaker_routing.classify_evidence_grade(frontmatter, verification_reason)


def find_existing_valid_raw_input(notebook_root: Path, url: str) -> tuple[Path, VerificationResult] | None:
    raw_root = notebook_root / "raw-input"
    if not raw_root.is_dir():
        return None
    canonical = canonical_watch_url(url)
    video_id = extract_video_id(canonical)
    for md in raw_root.rglob("*.md"):
        if md.name == "README.md":
            continue
        text = md.read_text(encoding="utf-8", errors="replace")
        frontmatter, _body = split_frontmatter(text)
        source_url = canonical_watch_url(str(frontmatter.get("source_url") or ""))
        source_id = extract_video_id(source_url)
        if source_url != canonical and not (video_id and source_id == video_id):
            continue
        verification = verify_raw_input_text(text)
        if verification.ok:
            return md, verification
    return None


TITLE_GUEST_ALIASES: dict[str, str] = {
    "patrick henningsen": "Henningsen",
}


def _normalized_name(value: str | None) -> str:
    if not value:
        return ""
    return re.sub(r"[^a-z0-9]+", " ", value.casefold()).strip()


def _host_slug_candidates(host: str | None) -> set[str]:
    host_norm = _normalized_name(host)
    if not host_norm:
        return set()
    tokens = host_norm.split()
    candidates = {host_norm, host_norm.replace(" ", "-")}
    if tokens:
        candidates.add(tokens[-1])
    return candidates


def infer_guest_from_title(title: str, notebook_root: Path, host: str | None = None) -> tuple[str | None, str | None]:
    speakers_dir = speaker_routing.DEFAULT_SPEAKERS_DIR
    if not speakers_dir.is_dir():
        return None, None
    title_text = f" {title.casefold()} "
    matches: list[str] = []
    host_slugs = _host_slug_candidates(host)
    for folder in sorted(path for path in speakers_dir.iterdir() if path.is_dir()):
        slug = folder.name
        candidates = {slug, slug.replace("-", " ")}
        obj = folder / f"{slug}-speaker-object.md"
        if obj.exists():
            candidates.add(slug.replace("-", " "))
        for candidate in candidates:
            pattern = rf"(?<![a-z0-9]){re.escape(candidate.casefold())}(?![a-z0-9])"
            if re.search(pattern, title_text):
                matches.append(slug)
                break
    unique_all = sorted(set(matches))
    unique = sorted(slug for slug in unique_all if slug not in host_slugs)
    if len(unique) == 1:
        return unique[0].replace("-", " ").title(), "exact-title-match"
    if not unique:
        alias_matches = [
            guest
            for alias, guest in TITLE_GUEST_ALIASES.items()
            if re.search(rf"(?<![a-z0-9]){re.escape(alias)}(?![a-z0-9])", title_text)
        ]
        if len(alias_matches) == 1 and _normalized_name(alias_matches[0]) not in host_slugs:
            return alias_matches[0], "title-known-speaker-match"
    if unique_all and not unique:
        return None, "host-only-title-match"
    return None, None


def _is_host_only_guest_match(guest: str | None, host: str | None) -> bool:
    if not guest or not host:
        return False
    guest_norm = _normalized_name(guest)
    host_norm = _normalized_name(host)
    if not guest_norm or not host_norm:
        return False
    host_tokens = set(host_norm.split())
    guest_tokens = set(guest_norm.split())
    return guest_norm == host_norm or guest_tokens.issubset(host_tokens)


def _caption_source_note(caption_kind: str | None) -> str:
    if caption_kind == "manual":
        return "Manual YouTube subtitles extracted with yt_dlp. Not human-verified verbatim."
    if caption_kind == "auto":
        return "Auto-generated YouTube subtitles extracted with yt_dlp. Not human-verified verbatim."
    return "YouTube subtitles extracted with yt_dlp. Not human-verified verbatim."


def fetch_metadata(url: str, auth: YtdlpAuth | None = None) -> tuple[str | None, dict[str, Any], str | None]:
    video_id = extract_video_id(url)
    if not video_id:
        return None, {}, "missing YouTube video id"
    auth = auth or YtdlpAuth()
    try:
        info = fetch_metadata_ytdlp(
            video_id,
            cookies=str(auth.cookies) if auth.cookies else None,
            cookies_from_browser=auth.cookies_from_browser,
        )
    except TypeError:
        info = fetch_metadata_ytdlp(video_id)
    if not info:
        for mode in ("binary", "module"):
            try:
                info = fetch_video_metadata_subprocess(
                    url,
                    mode=mode,
                    cookies=auth.cookies,
                    cookies_from_browser=auth.cookies_from_browser,
                )
                break
            except Exception:
                info = {}
    if not info:
        return video_id, {}, "metadata fetch failed"
    return video_id, dict(info), None


def fetch_caption_text(video_id: str, auth: YtdlpAuth | None = None) -> tuple[str | None, str | None, str | None, str | None]:
    auth = auth or YtdlpAuth()
    for langs in (PRIMARY_LANGS, FALLBACK_LANGS):
        try:
            text, kind, lang, error = fetch_subtitles_ytdlp(
                video_id,
                langs,
                cookies=str(auth.cookies) if auth.cookies else None,
                cookies_from_browser=auth.cookies_from_browser,
            )
        except TypeError:
            text, kind, lang, error = fetch_subtitles_ytdlp(video_id, langs)
        if text:
            return text, kind, lang, None
        last_error = error
    return None, None, None, last_error or "subtitle fetch failed"


def clean_caption_text(text: str) -> str:
    lines: list[str] = []
    prev = ""
    for raw in text.splitlines():
        line = html.unescape(raw).strip()
        line = re.sub(r"\s+", " ", line)
        if not line or line == prev:
            continue
        lines.append(line)
        prev = line
    return "\n".join(lines).strip()


def build_frontmatter(
    *,
    ingest_date: str,
    pub_date: str,
    title: str,
    source_url: str,
    video_id: str,
    spec: WatchlistSpec | None,
    item: ApprovedUrl,
    info: dict[str, Any],
    transcript_type: str,
    caption_language: str | None,
    caption_kind: str | None,
    guest: str | None = None,
    guest_inference: str | None = None,
    body_word_count: int | None = None,
    body_chars: int | None = None,
    verification_ok: bool | None = None,
    verification_reason: str | None = None,
    evidence_grade: str | None = None,
) -> str:
    show = item.show or (spec.show if spec else None)
    host = item.host or (spec.host if spec else None)
    thread = item.thread or (spec.thread if spec else None)
    channel_slug = item.channel_slug or (spec.channel_key if spec else slugify(str(info.get("channel") or info.get("uploader") or "youtube")))
    payload: dict[str, Any] = {
        "ingest_date": ingest_date,
        "pub_date": pub_date,
        "kind": "transcript",
        "source_type": "youtube",
        "transcript_type": transcript_type,
        "title": title,
        "source_url": source_url,
        "youtube_id": video_id,
        "channel_slug": channel_slug,
        "source_note": _caption_source_note(caption_kind),
        "editorial_note": "Atomic materialization verified a non-stub subtitle body before success was reported.",
    }
    if show:
        payload["show"] = show
    if host:
        payload["host"] = host
    if guest:
        payload["guest"] = guest
    if guest_inference:
        payload["guest_inference"] = guest_inference
    if thread:
        payload["thread"] = thread
    channel_url = str(info.get("channel_url") or info.get("uploader_url") or (spec.handle_url if spec else "")).strip()
    if channel_url:
        payload["channel_url"] = channel_url
    if caption_language:
        payload["caption_language"] = caption_language
    if caption_kind:
        payload["caption_kind"] = caption_kind
    if body_word_count is not None:
        payload["body_word_count"] = body_word_count
    if body_chars is not None:
        payload["body_chars"] = body_chars
    if verification_ok is not None:
        payload["verification_ok"] = verification_ok
    if verification_reason:
        payload["verification_reason"] = verification_reason
    if evidence_grade:
        payload["evidence_grade"] = evidence_grade
    raw = safe_dump(
        payload,
        feature="materialize_youtube_raw_input.py",
        sort_keys=False,
        allow_unicode=True,
        width=2000,
    ).rstrip()
    return f"---\n{raw}\n---\n\n"


def output_path_for(notebook_root: Path, pub_date: str, file_prefix: str, title: str) -> Path:
    return notebook_root / "raw-input" / pub_date / f"{file_prefix}-{slugify(title)}-{pub_date}.md"


def manual_context(item: ApprovedUrl) -> dict[str, Any]:
    return {
        "title": item.title or "",
        "pub_date": item.pub_date or "",
        "show": item.show or "",
        "host": item.host or "",
        "thread": item.thread or "",
        "channel_slug": item.channel_slug or "",
        "file_prefix": item.file_prefix or "",
        "guest": item.guest or "",
    }


def has_operator_metadata_for_bypass(item: ApprovedUrl) -> bool:
    return bool(
        item.title
        and item.pub_date
        and (item.file_prefix or item.channel_slug)
    )


def materialize_one(
    item: ApprovedUrl,
    *,
    notebook_root: Path,
    ingest_date: str,
    apply: bool,
    watchlist: dict[str, WatchlistSpec],
    auth: YtdlpAuth | None = None,
) -> dict[str, Any]:
    existing = find_existing_valid_raw_input(notebook_root, item.url)
    if existing:
        path, verification = existing
        return {
            "url": canonical_watch_url(item.url),
            "status": "already-present-valid",
            "output_path": str(path),
            "verification_ok": True,
            "verification_reason": verification.reason,
            "body_word_count": verification.word_count,
            "body_chars": verification.body_chars,
        }

    video_id, info, metadata_error = fetch_metadata(item.url, auth)
    metadata_bypassed = False
    if not video_id:
        return {
            "url": item.url,
            "youtube_id": "",
            "status": "failed-fetch",
            "output_path": "",
            "verification_ok": False,
            "verification_reason": metadata_error or "missing YouTube video id",
            "body_word_count": 0,
            "body_chars": 0,
            **manual_context(item),
        }
    if metadata_error:
        if not has_operator_metadata_for_bypass(item):
            return {
                "url": item.url,
                "youtube_id": video_id,
                "status": "failed-fetch",
                "output_path": "",
                "verification_ok": False,
                "verification_reason": metadata_error or "metadata fetch failed",
                "body_word_count": 0,
                "body_chars": 0,
                **manual_context(item),
            }
        info = {}
        metadata_bypassed = True

    spec = infer_watchlist_spec(info, watchlist)
    title = item.title or str(info.get("title") or video_id).strip()
    pub_date = item.pub_date or normalize_upload_date(str(info.get("upload_date") or ""))
    if not pub_date:
        return {
            "url": canonical_watch_url(item.url),
            "youtube_id": video_id,
            "title": title,
            "show": item.show or (spec.show if spec else ""),
            "host": item.host or (spec.host if spec else ""),
            "thread": item.thread or (spec.thread if spec else ""),
            "channel_slug": item.channel_slug or (spec.channel_key if spec else ""),
            "file_prefix": item.file_prefix or (spec.file_prefix if spec else ""),
            "guest": item.guest or "",
            "status": "failed-fetch",
            "output_path": "",
            "verification_ok": False,
            "verification_reason": "missing upload date",
            "body_word_count": 0,
            "body_chars": 0,
        }

    captions, caption_kind, caption_lang, caption_error = fetch_caption_text(video_id, auth)
    if not captions:
        return {
            "url": canonical_watch_url(item.url),
            "youtube_id": video_id,
            "title": title,
            "pub_date": pub_date,
            "show": item.show or (spec.show if spec else ""),
            "host": item.host or (spec.host if spec else ""),
            "thread": item.thread or (spec.thread if spec else ""),
            "channel_slug": item.channel_slug or (spec.channel_key if spec else ""),
            "file_prefix": item.file_prefix or (spec.file_prefix if spec else ""),
            "guest": item.guest or "",
            "status": "failed-fetch",
            "output_path": "",
            "verification_ok": False,
            "verification_reason": caption_error or "subtitle fetch failed",
            "body_word_count": 0,
            "body_chars": 0,
            "metadata_bypassed": metadata_bypassed,
        }

    transcript_type = "manual_subtitles_vtt" if caption_kind == "manual" else "auto_subtitles_vtt"
    source_url = canonical_watch_url(str(info.get("webpage_url") or info.get("url") or item.url))
    file_prefix = item.file_prefix or (spec.file_prefix if spec else f"youtube-{item.channel_slug or slugify(str(info.get('channel') or 'outside'))}")
    out_path = output_path_for(notebook_root, pub_date, file_prefix, title)
    host = item.host or (spec.host if spec else "")
    inferred_guest, guest_inference = (None, None) if item.guest else infer_guest_from_title(title, notebook_root, host)
    if _is_host_only_guest_match(inferred_guest, host):
        inferred_guest, guest_inference = None, "host-only-title-match"
    guest = item.guest or inferred_guest
    body = f"# {title}\n\n{clean_caption_text(captions)}\n"
    content = build_frontmatter(
        ingest_date=ingest_date,
        pub_date=pub_date,
        title=title,
        source_url=source_url,
        video_id=video_id,
        spec=spec,
        item=item,
        info=info,
        transcript_type=transcript_type,
        caption_language=caption_lang,
        caption_kind=caption_kind,
        guest=guest,
        guest_inference=guest_inference,
    ) + body
    verification = verify_raw_input_text(content)
    if not verification.ok:
        return {
            "url": source_url,
            "youtube_id": video_id,
            "title": title,
            "pub_date": pub_date,
            "status": "failed-verification",
            "output_path": str(out_path),
            "verification_ok": False,
            "verification_reason": verification.reason,
            "body_word_count": verification.word_count,
            "body_chars": verification.body_chars,
        }
    evidence_grade = classify_evidence_grade(verification.frontmatter, verification.reason)
    content = build_frontmatter(
        ingest_date=ingest_date,
        pub_date=pub_date,
        title=title,
        source_url=source_url,
        video_id=video_id,
        spec=spec,
        item=item,
        info=info,
        transcript_type=transcript_type,
        caption_language=caption_lang,
        caption_kind=caption_kind,
        guest=guest,
        guest_inference=guest_inference,
        body_word_count=verification.word_count,
        body_chars=verification.body_chars,
        verification_ok=True,
        verification_reason=verification.reason,
        evidence_grade=evidence_grade,
    ) + body
    verification = verify_raw_input_text(content)

    status = "dry-run"
    if apply:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(content, encoding="utf-8")
        reread = out_path.read_text(encoding="utf-8", errors="replace")
        verification = verify_raw_input_text(reread)
        status = "materialized" if verification.ok else "failed-verification"

    return {
        "url": source_url,
        "youtube_id": video_id,
        "title": title,
        "pub_date": pub_date,
        "status": status,
        "output_path": str(out_path),
        "watchlist_channel": spec.channel_key if spec else "",
        "show": item.show or (spec.show if spec else ""),
        "host": item.host or (spec.host if spec else ""),
        "thread": item.thread or (spec.thread if spec else ""),
        "guest": guest or "",
        "guest_inference": guest_inference or "",
        "evidence_grade": classify_evidence_grade(verification.frontmatter, verification.reason),
        "verification_ok": verification.ok,
        "verification_reason": verification.reason,
        "body_word_count": verification.word_count,
        "body_chars": verification.body_chars,
        "caption_language": caption_lang,
        "caption_kind": caption_kind,
        "metadata_bypassed": metadata_bypassed,
    }


def _successful_output_paths(rows: list[dict[str, Any]]) -> list[Path]:
    out: list[Path] = []
    for row in rows:
        if row.get("status") not in {"materialized", "already-present-valid", "already-present-legacy"}:
            continue
        output_path = str(row.get("output_path") or "").strip()
        if output_path:
            out.append(Path(output_path))
    return out


def materialize_existing_raw_input(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {
            "url": "",
            "status": "failed-verification",
            "output_path": str(path),
            "verification_ok": False,
            "verification_reason": "raw-input path does not exist",
            "body_word_count": 0,
            "body_chars": 0,
        }
    text = path.read_text(encoding="utf-8", errors="replace")
    verification = verify_existing_raw_input_for_appearance(text)
    source_url = str(verification.frontmatter.get("source_url") or "")
    legacy_ok = verification.reason.startswith("appearance-eligible legacy raw-input")
    return {
        "url": source_url,
        "status": "already-present-legacy" if (verification.ok and legacy_ok) else ("already-present-valid" if verification.ok else "failed-verification"),
        "output_path": str(path),
        "verification_ok": verification.ok,
        "verification_reason": verification.reason,
        "body_word_count": verification.word_count,
        "body_chars": verification.body_chars,
        "title": str(verification.frontmatter.get("title") or path.stem),
        "pub_date": str(verification.frontmatter.get("pub_date") or path.parent.name),
        "existing_raw_input": True,
        "evidence_grade": classify_evidence_grade(verification.frontmatter, verification.reason),
    }


def _path_lines(paths: list[Path]) -> str:
    return "".join(f"{path}\n" for path in paths)


def build_appearance_artifacts(
    *,
    raw_paths: list[Path],
    notebook_root: Path,
    run_id: str,
    include_no_action: bool,
) -> dict[str, str]:
    raw_paths = speaker_routing.normalize_raw_input_paths(raw_paths)
    if not raw_paths:
        return {}
    start, end = speaker_routing.window_for_raw_paths(raw_paths)
    inventory = speaker_routing._discover_inventory(speaker_routing.DEFAULT_SPEAKERS_DIR, notebook_root)
    routing_rows = speaker_routing.build_rows(raw_paths, inventory, notebook_root)
    unresolved_rows = speaker_routing.build_unresolved_rows(raw_paths, inventory)
    paths = {
        "appearance_count": str(len(routing_rows)),
        "action_count": "0",
        "unresolved_capture_count": str(len(unresolved_rows)),
        "unresolved_capture_titles": " | ".join(
            f"{row['pub_date']}::{row['title']}" for row in unresolved_rows
        ),
    }
    if not routing_rows:
        return paths
    routing_written = speaker_routing.write_outputs(
        routing_rows,
        DEFAULT_ROUTING_OUT / run_id,
        start,
        end,
    )
    actions = speaker_actions.build_actions(routing_rows, include_no_action=include_no_action)
    action_written = speaker_actions.write_outputs(
        rows=routing_rows,
        actions=actions,
        output_dir=DEFAULT_ACTION_OUT / run_id,
        start=start,
        end=end,
    )
    paths.update(
        {
            "speaker_routing_jsonl": routing_written["jsonl"],
            "speaker_routing_markdown": routing_written["markdown"],
            "appearance_ledger": routing_written["appearance_ledger"],
            "appearance_rollup_json": action_written["appearance_rollup_json"],
            "appearance_rollup_markdown": action_written["appearance_rollup_markdown"],
            "memory_action_queue_jsonl": action_written["memory_action_queue_jsonl"],
            "memory_action_queue_markdown": action_written["memory_action_queue_markdown"],
            "action_count": str(len(actions)),
        }
    )
    return paths


def build_quality_artifacts(*, raw_paths: list[Path], notebook_root: Path) -> dict[str, str]:
    summaries = host_shelf_quality.write_quality_reports_for_paths(
        raw_paths,
        notebook_root=notebook_root,
        output_root=DEFAULT_HOST_QUALITY_OUT,
        expand_to_month=True,
    )
    if not summaries:
        return {}
    return {
        "host_quality_count": str(len(summaries)),
        "host_quality_scope": "full-host-month",
        "host_quality_reports": " | ".join(str(summary["json_path"]) for summary in summaries),
        "host_quality_markdown": " | ".join(str(summary["markdown_path"]) for summary in summaries),
        "host_quality_closeout": " || ".join(str(summary["closeout_line"]) for summary in summaries),
    }


def write_capture_summary(
    *,
    rows: list[dict[str, Any]],
    receipt_dir: Path,
    purpose: str,
    tranche_label: str,
    artifact_paths: dict[str, str],
) -> dict[str, str]:
    successful_paths = _successful_output_paths(rows)
    successful = receipt_dir / "successful-raw-inputs.txt"
    successful.write_text(_path_lines(successful_paths), encoding="utf-8")

    counts: dict[str, int] = {}
    for row in rows:
        status = str(row.get("status") or "unknown")
        counts[status] = counts.get(status, 0) + 1
    transcript_valid_successes = 0
    summary_grade_carries = 0
    legacy_carries = 0
    for row in rows:
        if str(row.get("status") or "") not in {"materialized", "already-present-valid", "already-present-legacy"}:
            continue
        grade = str(row.get("evidence_grade") or "")
        if grade in {"transcript-grade", "cleaned-transcript", "transcript-bearing"}:
            transcript_valid_successes += 1
        elif grade == "summary-grade":
            summary_grade_carries += 1
        elif grade == "legacy-appearance-only":
            legacy_carries += 1
    unresolved_count = int(artifact_paths.get("unresolved_capture_count", "0") or "0")
    summary = receipt_dir / "capture-summary.md"
    lines = [
        "# YouTube capture summary",
        "",
        "WORK only; not Record.",
        "",
        f"- purpose: `{purpose}`",
        f"- tranche: `{tranche_label or '_none_'}`",
        f"- approved rows: `{len(rows)}`",
        f"- successful raw-inputs: `{len(successful_paths)}`",
        f"- transcript-valid successes: `{transcript_valid_successes}`",
        f"- summary-grade carries: `{summary_grade_carries}`",
        f"- legacy appearance carries: `{legacy_carries}`",
        f"- unresolved speaker captures: `{unresolved_count}`",
    ]
    if artifact_paths.get("host_quality_closeout"):
        if artifact_paths.get("host_quality_scope"):
            lines.append(f"- quality scope: `{artifact_paths['host_quality_scope']}`")
        lines.append(f"- quality closeout: {artifact_paths['host_quality_closeout']}")
    for status, count in sorted(counts.items()):
        lines.append(f"- {status}: `{count}`")
    if artifact_paths:
        lines.extend(
            [
                f"- appearances: `{artifact_paths.get('appearance_count', '0')}`",
                f"- actions: `{artifact_paths.get('action_count', '0')}`",
                "",
                "## Artifacts",
                "",
            ]
        )
        for key, value in sorted(artifact_paths.items()):
            if key.endswith("_count") or key == "unresolved_capture_titles":
                continue
            lines.append(f"- `{key}`: `{value}`")
        if unresolved_count:
            lines.extend(["", "## Unresolved speaker captures", ""])
            for chunk in str(artifact_paths.get("unresolved_capture_titles") or "").split(" | "):
                if not chunk:
                    continue
                pub_date, _sep, title = chunk.partition("::")
                lines.append(f"- `{pub_date}` {title}")
    summary.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return {"successful_raw_inputs": str(successful), "capture_summary": str(summary)}


def _manual_scaffold_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        row
        for row in rows
        if row.get("status") in {"failed-fetch", "failed-verification"}
        and str(row.get("url") or row.get("source_url") or "").strip()
    ]


def _manual_target_path(row: dict[str, Any], notebook_root: Path | None) -> Path | None:
    if not notebook_root:
        return None
    pub_date = str(row.get("pub_date") or "").strip()
    title = str(row.get("title") or "").strip()
    file_prefix = str(row.get("file_prefix") or row.get("channel_slug") or "youtube").strip()
    if not (pub_date and title and file_prefix):
        return None
    return output_path_for(notebook_root, pub_date, file_prefix, title)


def _manual_frontmatter(row: dict[str, Any], *, ingest_date: str) -> dict[str, Any]:
    source_url = canonical_watch_url(str(row.get("url") or row.get("source_url") or ""))
    payload: dict[str, Any] = {
        "ingest_date": ingest_date,
        "pub_date": str(row.get("pub_date") or "YYYY-MM-DD"),
        "kind": "transcript",
        "source_type": "youtube",
        "transcript_type": "operator_pasted_transcript",
        "title": str(row.get("title") or "PASTE TITLE HERE"),
        "source_url": source_url,
        "source_note": "Transcript pasted manually by operator after automated yt-dlp fetch failed.",
        "editorial_note": "Manual scaffold generated in receipts only; save to canonical raw-input only after replacing the paste marker with a real transcript body.",
    }
    for key in ("youtube_id", "channel_slug", "show", "host", "guest", "thread"):
        value = str(row.get(key) or "").strip()
        if value:
            payload[key] = value
    return payload


def _manual_frontmatter_text(row: dict[str, Any], *, ingest_date: str) -> str:
    frontmatter = safe_dump(
        _manual_frontmatter(row, ingest_date=ingest_date),
        feature="materialize_youtube_raw_input.py",
        sort_keys=False,
        allow_unicode=True,
        width=2000,
    ).rstrip()
    return f"---\n{frontmatter}\n---\n"


def _manual_draft_text(row: dict[str, Any], *, ingest_date: str) -> str:
    title = str(row.get("title") or "PASTE TITLE HERE").strip()
    return (
        f"{_manual_frontmatter_text(row, ingest_date=ingest_date)}\n"
        f"# {title}\n\n"
        "[PASTE FULL TRANSCRIPT BODY HERE. Delete this line before saving canonical raw-input.]\n"
    )


def _manual_paste_body_text(row: dict[str, Any], *, target_path: Path | None) -> str:
    title = str(row.get("title") or "PASTE TITLE HERE").strip()
    target = str(target_path) if target_path else "Unknown until pub_date, title, and file_prefix are supplied."
    return (
        "Paste the transcript body below this line, then move it into the matching .draft.md file.\n"
        "Do not paste summaries, chapter lists, comments, or descriptions here.\n\n"
        f"title: {title}\n"
        f"target_raw_input: {target}\n\n"
        "--- PASTE FULL TRANSCRIPT BODY BELOW ---\n\n"
    )


def _manual_verify_command(target_path: Path | None) -> str:
    if not target_path:
        return "After saving the canonical raw-input, run the materializer with --raw-input <path> --with-appearances."
    return (
        f'python scripts\\materialize_youtube_raw_input.py --raw-input "{target_path}" '
        "--with-appearances --purpose one-off --tranche-label manual-transcript"
    )


def _manual_verify_script(command: str) -> str:
    return (
        "# Manual transcript verification helper.\n"
        "# Run from the strategy-codex repository root after saving the filled raw-input draft.\n"
        f"{command}\n"
    )


def _manual_scaffold_body(
    row: dict[str, Any],
    *,
    ingest_date: str,
    target_path: Path | None,
    draft_name: str,
    paste_name: str,
    verify_name: str,
) -> str:
    title = str(row.get("title") or "PASTE TITLE HERE").strip()
    target = str(target_path) if target_path else "Unknown until pub_date, title, and file_prefix are supplied."
    source_url = canonical_watch_url(str(row.get("url") or row.get("source_url") or ""))
    reason = str(row.get("verification_reason") or "manual transcript needed")
    verify_command = _manual_verify_command(target_path)
    return (
        "# Manual Transcript Scaffold\n\n"
        "WORK only; not Record. This receipt is a handoff aid, not a captured transcript.\n\n"
        "## Target\n\n"
        f"- canonical_raw_input: `{target}`\n"
        f"- source_url: {source_url}\n"
        f"- failed_reason: `{reason}`\n\n"
        "## Curator Files\n\n"
        f"- draft: [{draft_name}]({draft_name})\n"
        f"- paste body buffer: [{paste_name}]({paste_name})\n"
        f"- verification helper: [{verify_name}]({verify_name})\n\n"
        "## Human Steps\n\n"
        "1. Open the YouTube source in a browser.\n"
        "2. Copy the full transcript, not only a summary or chapter list.\n"
        "3. Paste into the `.paste-body.txt` buffer if you want a scratch step.\n"
        "4. Replace the paste marker in the `.draft.md` file with the transcript body.\n"
        "5. Save the filled draft to the canonical raw-input path above.\n"
        "6. Run the verification/routing command below before claiming capture.\n\n"
        "## Curator Notes\n\n"
        "- curator_note: \n"
        "- transcript_source: YouTube transcript panel / operator copy / other\n"
        "- transcript_completeness: full / partial / unknown\n"
        "- speaker_labels: original / operator-added / none\n"
        "- status: needs-paste\n\n"
        "## Ready-To-Fill Raw-Input Draft Preview\n\n"
        "```markdown\n"
        f"{_manual_draft_text(row, ingest_date=ingest_date)}"
        "```\n\n"
        "## Verification Command\n\n"
        "```powershell\n"
        f"{verify_command}\n"
        "```\n\n"
        "## Non-Stub Checklist\n\n"
        "- Frontmatter has `source_url`, `pub_date`, `title`, `source_type`, `transcript_type`, and a provenance note.\n"
        "- Body is at least 75 words and 400 characters after frontmatter.\n"
        "- Body is transcript text, not an index, placeholder, or summary shell.\n"
        "- Speaker/guest metadata is preserved when known.\n"
    )


def _manual_queue_body(entries: list[dict[str, str]]) -> str:
    lines = [
        "# Manual curation queue",
        "",
        "WORK only; not Record. Use this as the human transcript inbox for blocked materialization rows.",
        "",
        "| status | pub_date | title | guest | target | scaffold | draft | paste body | verify |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for entry in entries:
        lines.append(
            "| needs-paste "
            f"| {entry['pub_date']} "
            f"| {entry['title']} "
            f"| {entry['guest']} "
            f"| `{entry['target']}` "
            f"| [{entry['scaffold_name']}]({entry['scaffold_rel']}) "
            f"| [{entry['draft_name']}]({entry['draft_rel']}) "
            f"| [{entry['paste_name']}]({entry['paste_rel']}) "
            f"| [{entry['verify_name']}]({entry['verify_rel']}) |"
        )
    lines.extend(
        [
            "",
            "## Status Meaning",
            "",
            "- `needs-paste`: no human transcript body has been added yet.",
            "- `pasted-needs-verify`: body has been pasted into the draft but verification has not passed yet.",
            "- `verified`: canonical raw-input exists and the materializer accepted it.",
            "- `blocked`: human transcript source is unavailable or incomplete.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def write_manual_transcript_scaffolds(
    rows: list[dict[str, Any]],
    receipt_dir: Path,
    *,
    notebook_root: Path | None = None,
    ingest_date: str | None = None,
) -> dict[str, str]:
    scaffold_rows = _manual_scaffold_rows(rows)
    if not scaffold_rows:
        return {}
    out_dir = receipt_dir / "manual-transcript-scaffolds"
    out_dir.mkdir(parents=True, exist_ok=True)
    effective_ingest_date = ingest_date or date.today().isoformat()
    index_lines = [
        "# Manual transcript scaffolds",
        "",
        "WORK only; not Record. These files help humans fill transcripts later without creating canonical stubs.",
        "",
    ]
    queue_entries: list[dict[str, str]] = []
    for idx, row in enumerate(scaffold_rows, start=1):
        title = str(row.get("title") or row.get("youtube_id") or row.get("url") or f"row-{idx}")
        slug = slugify(title, max_len=48)
        path = out_dir / f"{idx:02d}-{slug}.md"
        draft = out_dir / f"{idx:02d}-{slug}.draft.md"
        paste_body = out_dir / f"{idx:02d}-{slug}.paste-body.txt"
        verify = out_dir / f"{idx:02d}-{slug}.verify.ps1"
        target_path = _manual_target_path(row, notebook_root)
        verify_command = _manual_verify_command(target_path)
        path.write_text(
            _manual_scaffold_body(
                row,
                ingest_date=effective_ingest_date,
                target_path=target_path,
                draft_name=draft.name,
                paste_name=paste_body.name,
                verify_name=verify.name,
            ),
            encoding="utf-8",
        )
        draft.write_text(_manual_draft_text(row, ingest_date=effective_ingest_date), encoding="utf-8")
        paste_body.write_text(_manual_paste_body_text(row, target_path=target_path), encoding="utf-8")
        verify.write_text(_manual_verify_script(verify_command), encoding="utf-8")
        index_lines.append(f"- [{path.name}](manual-transcript-scaffolds/{path.name})")
        queue_entries.append(
            {
                "pub_date": str(row.get("pub_date") or ""),
                "title": title.replace("|", "\\|"),
                "guest": str(row.get("guest") or "").replace("|", "\\|"),
                "target": str(target_path) if target_path else "",
                "scaffold_name": path.name,
                "scaffold_rel": f"manual-transcript-scaffolds/{path.name}",
                "draft_name": draft.name,
                "draft_rel": f"manual-transcript-scaffolds/{draft.name}",
                "paste_name": paste_body.name,
                "paste_rel": f"manual-transcript-scaffolds/{paste_body.name}",
                "verify_name": verify.name,
                "verify_rel": f"manual-transcript-scaffolds/{verify.name}",
            }
        )
    index = receipt_dir / "manual-transcript-scaffolds.md"
    index.write_text("\n".join(index_lines).rstrip() + "\n", encoding="utf-8")
    queue = receipt_dir / "manual-curation-queue.md"
    queue.write_text(_manual_queue_body(queue_entries), encoding="utf-8")
    return {
        "manual_scaffold_index": str(index),
        "manual_scaffold_dir": str(out_dir),
        "manual_scaffold_count": str(len(scaffold_rows)),
        "manual_curation_queue": str(queue),
    }


def write_receipts(
    rows: list[dict[str, Any]],
    receipt_dir: Path,
    *,
    purpose: str = "one-off",
    tranche_label: str = "",
    artifact_paths: dict[str, str] | None = None,
    notebook_root: Path | None = None,
    ingest_date: str | None = None,
) -> dict[str, str]:
    receipt_dir.mkdir(parents=True, exist_ok=True)
    ledger = receipt_dir / "materialization-ledger.jsonl"
    with ledger.open("w", encoding="utf-8", newline="") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=True) + "\n")

    summary = receipt_dir / "materialization-summary.md"
    lines = [
        "# YouTube raw-input materialization summary",
        "",
        "| status | verification | words | output | title |",
        "|---|---|---:|---|---|",
    ]
    for row in rows:
        output = row.get("output_path") or ""
        title = str(row.get("title") or row.get("url") or "").replace("|", "\\|")
        lines.append(
            f"| {row.get('status', '')} | {row.get('verification_reason', '')} | {row.get('body_word_count', 0)} | `{output}` | {title} |"
        )
    summary.write_text("\n".join(lines) + "\n", encoding="utf-8")
    paths = {"ledger": str(ledger), "summary": str(summary)}
    paths.update(
        write_manual_transcript_scaffolds(
            rows,
            receipt_dir,
            notebook_root=notebook_root,
            ingest_date=ingest_date,
        )
    )
    paths.update(
        write_capture_summary(
            rows=rows,
            receipt_dir=receipt_dir,
            purpose=purpose,
            tranche_label=tranche_label,
            artifact_paths=artifact_paths or {},
        )
    )
    return paths


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", action="append", default=[], help="Approved YouTube watch URL. Repeatable.")
    parser.add_argument("--input", type=Path, default=None, help="JSONL or plain-text approved URL list.")
    parser.add_argument("--notebook-root", type=Path, default=DEFAULT_NOTEBOOK_ROOT)
    parser.add_argument("--ingest-date", default=date.today().isoformat(), help="YYYY-MM-DD")
    parser.add_argument("--apply", action="store_true", help="Write canonical raw-input files.")
    parser.add_argument("--no-apply", action="store_false", dest="apply", help="Dry-run without canonical writes.")
    parser.add_argument("--receipt-root", type=Path, default=DEFAULT_RECEIPT_ROOT)
    parser.add_argument("--run-id", default="", help="Receipt subdirectory name. Defaults to UTC timestamp.")
    parser.add_argument("--cookies", type=Path, default=None, help="yt-dlp cookies.txt path for operator-approved authenticated fetches.")
    parser.add_argument("--cookies-from-browser", default="", help="yt-dlp browser cookie source, for example `chrome` or `chrome:Profile 1`.")
    parser.add_argument("--with-appearances", action="store_true", help="Build appearance, routing, and action artifacts for successful raw-inputs.")
    parser.add_argument("--no-quality-report", action="store_true", help="Skip host-shelf quality artifacts when --with-appearances --apply would normally write them.")
    parser.add_argument("--purpose", choices=["daily", "densification", "one-off"], default="one-off")
    parser.add_argument("--tranche-label", default="", help="Human label for a bounded capture/densification tranche.")
    parser.add_argument("--raw-input", action="append", type=Path, default=[], help="Existing raw-input path to route without refetching. Repeatable.")
    parser.add_argument("--raw-input-list", type=Path, default=None, help="Text file with one existing raw-input path per line.")
    parser.add_argument("--include-no-action", action="store_true", help="Include no-action rows in speaker-memory action queue.")
    parser.add_argument("--show", default="")
    parser.add_argument("--host", default="")
    parser.add_argument("--thread", default="")
    parser.add_argument("--channel-slug", default="")
    parser.add_argument("--file-prefix", default="")
    parser.add_argument("--guest", default="")
    parser.add_argument("--pub-date", default="")
    parser.add_argument("--title", default="")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    items = load_approved_urls(args.input, args.url)
    raw_input_paths = list(args.raw_input)
    if args.raw_input_list:
        raw_input_paths.extend(speaker_routing.load_raw_input_list(args.raw_input_list))
    if not items and not raw_input_paths:
        print("materialize_youtube_raw_input: provide --url, --input, --raw-input, or --raw-input-list", file=sys.stderr)
        return 2

    if any([args.show, args.host, args.thread, args.channel_slug, args.file_prefix, args.guest, args.pub_date, args.title]):
        items = [
            ApprovedUrl(
                url=item.url,
                show=item.show or args.show or None,
                host=item.host or args.host or None,
                thread=item.thread or args.thread or None,
                channel_slug=item.channel_slug or args.channel_slug or None,
                file_prefix=item.file_prefix or args.file_prefix or None,
                guest=item.guest or args.guest or None,
                pub_date=item.pub_date or args.pub_date or None,
                title=item.title or args.title or None,
            )
            for item in items
        ]

    watchlist = load_watchlist()
    auth = YtdlpAuth(cookies=args.cookies, cookies_from_browser=args.cookies_from_browser or None)
    rows = [
        materialize_one(
            item,
            notebook_root=args.notebook_root,
            ingest_date=args.ingest_date,
            apply=args.apply,
            watchlist=watchlist,
            auth=auth,
        )
        for item in items
    ]
    rows.extend(materialize_existing_raw_input(path if path.is_absolute() else REPO_ROOT / path) for path in raw_input_paths)
    run_id = args.run_id or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    receipt_dir = args.receipt_root / run_id
    artifact_paths: dict[str, str] = {}
    if args.with_appearances:
        successful_paths = _successful_output_paths(rows)
        artifact_paths = build_appearance_artifacts(
            raw_paths=successful_paths,
            notebook_root=args.notebook_root.resolve(),
            run_id=run_id,
            include_no_action=args.include_no_action,
        )
        if args.apply and not args.no_quality_report:
            artifact_paths.update(
                build_quality_artifacts(
                    raw_paths=successful_paths,
                    notebook_root=args.notebook_root.resolve(),
                )
            )
    paths = write_receipts(
        rows,
        receipt_dir,
        purpose=args.purpose,
        tranche_label=args.tranche_label,
        artifact_paths=artifact_paths,
        notebook_root=args.notebook_root.resolve(),
        ingest_date=args.ingest_date,
    )
    print(json.dumps({"rows": rows, "receipts": paths}, indent=2, ensure_ascii=True))
    failed = [row for row in rows if row.get("status") in {"failed-fetch", "failed-verification"}]
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
