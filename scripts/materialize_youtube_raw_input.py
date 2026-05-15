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
DEFAULT_NOTEBOOK_ROOT = REPO_ROOT / "codex" / str(date.today().year)
DEFAULT_RECEIPT_ROOT = REPO_ROOT / ".codex-tmp" / "youtube-raw-input"
DEFAULT_ROUTING_OUT = REPO_ROOT / "artifacts" / "speaker-routing"
DEFAULT_ACTION_OUT = REPO_ROOT / "artifacts" / "speaker-memory-actions"
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


def infer_guest_from_title(title: str, notebook_root: Path) -> tuple[str | None, str | None]:
    speakers_dir = notebook_root / "speakers"
    if not speakers_dir.is_dir():
        return None, None
    title_text = f" {title.casefold()} "
    matches: list[str] = []
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
    unique = sorted(set(matches))
    if len(unique) == 1:
        return unique[0].replace("-", " ").title(), "exact-title-match"
    return None, None


def fetch_metadata(url: str) -> tuple[str | None, dict[str, Any], str | None]:
    video_id = extract_video_id(url)
    if not video_id:
        return None, {}, "missing YouTube video id"
    info = fetch_metadata_ytdlp(video_id)
    if not info:
        for mode in ("binary", "module"):
            try:
                info = fetch_video_metadata_subprocess(url, mode=mode)
                break
            except Exception:
                info = {}
    if not info:
        return video_id, {}, "metadata fetch failed"
    return video_id, dict(info), None


def fetch_caption_text(video_id: str) -> tuple[str | None, str | None, str | None, str | None]:
    for langs in (PRIMARY_LANGS, FALLBACK_LANGS):
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
        "source_note": "Auto-captions extracted with yt_dlp from YouTube subtitles. Not human-verified verbatim.",
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


def materialize_one(
    item: ApprovedUrl,
    *,
    notebook_root: Path,
    ingest_date: str,
    apply: bool,
    watchlist: dict[str, WatchlistSpec],
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

    video_id, info, metadata_error = fetch_metadata(item.url)
    if not video_id or metadata_error:
        return {
            "url": item.url,
            "status": "failed-fetch",
            "output_path": "",
            "verification_ok": False,
            "verification_reason": metadata_error or "metadata fetch failed",
            "body_word_count": 0,
            "body_chars": 0,
        }

    spec = infer_watchlist_spec(info, watchlist)
    title = item.title or str(info.get("title") or video_id).strip()
    pub_date = item.pub_date or normalize_upload_date(str(info.get("upload_date") or ""))
    if not pub_date:
        return {
            "url": canonical_watch_url(item.url),
            "youtube_id": video_id,
            "title": title,
            "status": "failed-fetch",
            "output_path": "",
            "verification_ok": False,
            "verification_reason": "missing upload date",
            "body_word_count": 0,
            "body_chars": 0,
        }

    captions, caption_kind, caption_lang, caption_error = fetch_caption_text(video_id)
    if not captions:
        return {
            "url": canonical_watch_url(item.url),
            "youtube_id": video_id,
            "title": title,
            "pub_date": pub_date,
            "status": "failed-fetch",
            "output_path": "",
            "verification_ok": False,
            "verification_reason": caption_error or "subtitle fetch failed",
            "body_word_count": 0,
            "body_chars": 0,
        }

    transcript_type = "manual_subtitles_vtt" if caption_kind == "manual" else "auto_subtitles_vtt"
    source_url = canonical_watch_url(str(info.get("webpage_url") or info.get("url") or item.url))
    file_prefix = item.file_prefix or (spec.file_prefix if spec else f"youtube-{item.channel_slug or slugify(str(info.get('channel') or 'outside'))}")
    out_path = output_path_for(notebook_root, pub_date, file_prefix, title)
    inferred_guest, guest_inference = (None, None) if item.guest else infer_guest_from_title(title, notebook_root)
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
        "verification_ok": verification.ok,
        "verification_reason": verification.reason,
        "body_word_count": verification.word_count,
        "body_chars": verification.body_chars,
        "caption_language": caption_lang,
        "caption_kind": caption_kind,
    }


def _successful_output_paths(rows: list[dict[str, Any]]) -> list[Path]:
    out: list[Path] = []
    for row in rows:
        if row.get("status") not in {"materialized", "already-present-valid"}:
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
    return {
        "url": source_url,
        "status": "already-present-valid" if verification.ok else "failed-verification",
        "output_path": str(path),
        "verification_ok": verification.ok,
        "verification_reason": verification.reason,
        "body_word_count": verification.word_count,
        "body_chars": verification.body_chars,
        "title": str(verification.frontmatter.get("title") or path.stem),
        "pub_date": str(verification.frontmatter.get("pub_date") or path.parent.name),
        "existing_raw_input": True,
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
    inventory = speaker_routing._discover_inventory(notebook_root / "speakers", notebook_root)
    routing_rows = speaker_routing.build_rows(raw_paths, inventory, notebook_root)
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
    return {
        "speaker_routing_jsonl": routing_written["jsonl"],
        "speaker_routing_markdown": routing_written["markdown"],
        "appearance_ledger": routing_written["appearance_ledger"],
        "appearance_rollup_json": action_written["appearance_rollup_json"],
        "appearance_rollup_markdown": action_written["appearance_rollup_markdown"],
        "memory_action_queue_jsonl": action_written["memory_action_queue_jsonl"],
        "memory_action_queue_markdown": action_written["memory_action_queue_markdown"],
        "appearance_count": str(len(routing_rows)),
        "action_count": str(len(actions)),
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
    ]
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
            if key.endswith("_count"):
                continue
            lines.append(f"- `{key}`: `{value}`")
    summary.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return {"successful_raw_inputs": str(successful), "capture_summary": str(summary)}


def write_receipts(
    rows: list[dict[str, Any]],
    receipt_dir: Path,
    *,
    purpose: str = "one-off",
    tranche_label: str = "",
    artifact_paths: dict[str, str] | None = None,
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
    parser.add_argument("--with-appearances", action="store_true", help="Build appearance, routing, and action artifacts for successful raw-inputs.")
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
    rows = [
        materialize_one(
            item,
            notebook_root=args.notebook_root,
            ingest_date=args.ingest_date,
            apply=args.apply,
            watchlist=watchlist,
        )
        for item in items
    ]
    rows.extend(materialize_existing_raw_input(path if path.is_absolute() else REPO_ROOT / path) for path in raw_input_paths)
    run_id = args.run_id or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    receipt_dir = args.receipt_root / run_id
    artifact_paths: dict[str, str] = {}
    if args.with_appearances:
        artifact_paths = build_appearance_artifacts(
            raw_paths=_successful_output_paths(rows),
            notebook_root=args.notebook_root.resolve(),
            run_id=run_id,
            include_no_action=args.include_no_action,
        )
    paths = write_receipts(
        rows,
        receipt_dir,
        purpose=args.purpose,
        tranche_label=args.tranche_label,
        artifact_paths=artifact_paths,
    )
    print(json.dumps({"rows": rows, "receipts": paths}, indent=2, ensure_ascii=True))
    failed = [row for row in rows if row.get("status") in {"failed-fetch", "failed-verification"}]
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
