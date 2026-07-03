#!/usr/bin/env python3
"""Refresh a Diesen guest-stream ledger from YouTube URLs.

This is an input-workflow helper for the Glenn Diesen scaffold in strategy-notebook.
It canonicalizes YouTube URLs, fetches exact metadata with yt-dlp, dedupes by
video ID across the Diesen profile, and refreshes the ledger section in place.

"""

from __future__ import annotations

import argparse
import html
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable
from urllib.parse import parse_qs, urlparse

from youtube_transcripts.ytdlp_adapter import YtDlpError, fetch_video_metadata_subprocess

REPO_ROOT = Path(__file__).resolve().parent.parent
NOTEBOOK_ROOT = REPO_ROOT / "docs/archive/skill-work-legacy/work-strategy/strategy-notebook"
DEFAULT_PROFILE = NOTEBOOK_ROOT / "experts" / "diesen" / "profile.md"

WATCH_URL_RE = re.compile(r"https?://(?:www\.)?youtube\.com/watch\?v=[A-Za-z0-9_-]{6,}")
YOUTUBE_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")
LINK_RE = re.compile(r"https?://[^\s)\]]+")
MARKER_START_RE = re.compile(r"<!--\s*diesen-ledger:([a-z0-9_-]+):start\s*-->", re.I)
MARKER_END_RE = re.compile(r"<!--\s*diesen-ledger:([a-z0-9_-]+):end\s*-->", re.I)

@dataclass(frozen=True)
class LedgerRow:
    pub_date: str
    title: str
    url: str
    raw_input: str
    video_id: str

def extract_video_id(value: str) -> str | None:
    text = value.strip()
    if not text:
        return None
    if YOUTUBE_ID_RE.fullmatch(text):
        return text
    parsed = urlparse(text)
    host = (parsed.netloc or "").lower()
    path = parsed.path or ""
    if "youtu.be" in host:
        candidate = path.strip("/").split("/", 1)[0]
        return candidate if YOUTUBE_ID_RE.fullmatch(candidate) else None
    if "youtube.com" in host:
        if path.startswith("/watch"):
            q = parse_qs(parsed.query)
            candidate = (q.get("v") or [""])[0]
            return candidate if YOUTUBE_ID_RE.fullmatch(candidate) else None
        if path.startswith("/shorts/"):
            candidate = path.split("/shorts/", 1)[1].split("/", 1)[0]
            return candidate if YOUTUBE_ID_RE.fullmatch(candidate) else None
    m = WATCH_URL_RE.search(text)
    if m:
        return m.group(0).split("v=", 1)[1].split("&", 1)[0]
    return None

def canonical_watch_url(value: str) -> str:
    video_id = extract_video_id(value)
    if not video_id:
        raise ValueError(f"could not parse YouTube video id from: {value!r}")
    return f"https://www.youtube.com/watch?v={video_id}"

def normalize_text(text: str) -> str:
    text = html.unescape(text or "")
    text = " ".join(text.split())
    return text.strip()

def normalize_cell(text: str) -> str:
    return normalize_text(text).replace("\\|", "|").replace("\\\\", "\\")

def escape_cell(text: str) -> str:
    return normalize_text(text).replace("\\", "\\\\").replace("|", "\\|")

def normalize_pub_date(value: str | None) -> str | None:
    text = normalize_text(value or "")
    if not text:
        return None
    if re.fullmatch(r"\d{8}", text):
        return f"{text[:4]}-{text[4:6]}-{text[6:8]}"
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        return text
    return None

def fetch_youtube_metadata(video_id: str) -> dict | None:
    try:
        data = fetch_video_metadata_subprocess(
            video_id,
            mode="module",
            python_cmd=sys.executable,
        )
    except YtDlpError:
        return None
    title = normalize_text(str(data.get("title") or ""))
    pub_date = normalize_pub_date(str(data.get("upload_date") or ""))
    if not title or not pub_date:
        return None
    return {
        "title": title,
        "pub_date": pub_date,
        "url": canonical_watch_url(video_id),
    }

def raw_input_status(notebook_root: Path, video_id: str, canonical_url: str) -> str:
    raw_root = notebook_root / "raw-input"
    needles = {video_id, canonical_url}
    for path in raw_root.rglob("*.md"):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if any(needle in text for needle in needles):
            return "mirrored"
    return "needs capture"

def split_table_cells(line: str) -> list[str]:
    inner = line.strip().strip("|")
    parts = re.split(r"(?<!\\)\|", inner)
    return [normalize_cell(p) for p in parts]

def parse_rows_from_section(section_text: str) -> list[LedgerRow]:
    rows: list[LedgerRow] = []
    for line in section_text.splitlines():
        if not line.startswith("|"):
            continue
        cells = split_table_cells(line)
        if len(cells) < 4 or cells[0] == "pub_date" or cells[0].startswith("-"):
            continue
        pub_date, title_cell, url_cell, status = cells[:4]
        pub_date = normalize_pub_date(pub_date) or ""
        if not pub_date:
            continue
        match = LINK_RE.search(url_cell)
        if not match:
            continue
        url = canonical_watch_url(match.group(0))
        video_id = extract_video_id(url)
        if not video_id:
            continue
        rows.append(
            LedgerRow(
                pub_date=pub_date,
                title=normalize_text(title_cell),
                url=url,
                raw_input=status if status in {"mirrored", "needs capture"} else "needs capture",
                video_id=video_id,
            )
        )
    return rows

def render_rows(rows: list[LedgerRow]) -> str:
    lines = [
        "| pub_date | Title | URL | raw-input |",
        "|----------|-------|-----|-----------|",
    ]
    for row in rows:
        url = canonical_watch_url(row.video_id)
        lines.append(
            f"| {row.pub_date} | {escape_cell(row.title)} | "
            f"[{url}]({url}) | {row.raw_input} |"
        )
    return "\n".join(lines)

def find_existing_video_ids(profile_text: str) -> set[str]:
    ids: set[str] = set()
    for match in LINK_RE.finditer(profile_text):
        video_id = extract_video_id(match.group(0))
        if video_id:
            ids.add(video_id)
    return ids

def find_section_block(profile_text: str, ledger_key: str) -> tuple[str, str, str]:
    start_tag = f"<!-- diesen-ledger:{ledger_key}:start -->"
    end_tag = f"<!-- diesen-ledger:{ledger_key}:end -->"
    start = profile_text.find(start_tag)
    end = profile_text.find(end_tag)
    if start < 0 or end < 0 or end <= start:
        raise ValueError(f"missing ledger markers for {ledger_key!r}")
    start_body = start + len(start_tag)
    before = profile_text[:start_body]
    body = profile_text[start_body:end]
    after = profile_text[end:]
    return before, body, after

def rebuild_ledger_section(
    *,
    profile_text: str,
    ledger_key: str,
    urls: list[str],
    notebook_root: Path,
    metadata_fetcher: Callable[[str], dict | None] | None = fetch_youtube_metadata,
) -> tuple[str, list[str]]:
    before, body, after = find_section_block(profile_text, ledger_key)
    current_rows = parse_rows_from_section(body)
    current_by_id = {row.video_id: row for row in current_rows}
    global_existing_ids = find_existing_video_ids(profile_text)

    input_ids: list[str] = []
    for raw in urls:
        video_id = extract_video_id(raw)
        if not video_id:
            continue
        input_ids.append(video_id)

    added: list[str] = []
    for video_id in input_ids:
        if video_id in current_by_id:
            continue
        if video_id in global_existing_ids:
            continue
        current_by_id[video_id] = LedgerRow(
            pub_date="",
            title="",
            url=canonical_watch_url(video_id),
            raw_input="needs capture",
            video_id=video_id,
        )
        added.append(video_id)

    refreshed: list[LedgerRow] = []
    seen: set[str] = set()
    for row in list(current_by_id.values()):
        if row.video_id in seen:
            continue
        seen.add(row.video_id)
        meta = metadata_fetcher(row.video_id) if metadata_fetcher else None
        if meta:
            title = meta["title"]
            pub_date = meta["pub_date"]
            url = meta["url"]
        else:
            title = row.title or row.video_id
            pub_date = row.pub_date
            url = row.url
        if not pub_date:
            continue
        status = raw_input_status(notebook_root, row.video_id, url)
        refreshed.append(
            LedgerRow(
                pub_date=pub_date,
                title=title,
                url=url,
                raw_input=status,
                video_id=row.video_id,
            )
        )

    refreshed.sort(key=lambda r: (r.pub_date, r.title.lower(), r.video_id))
    rendered = render_rows(refreshed)
    new_block = f"{before}\n\n{rendered}\n\n{after}"
    return new_block, added

def extract_urls_from_text(text: str) -> list[str]:
    out: list[str] = []
    for token in re.split(r"[\s;]+", text):
        token = token.strip().strip(",")
        if not token:
            continue
        if extract_video_id(token):
            out.append(token)
            continue
        if WATCH_URL_RE.search(token):
            out.append(token)
    return out

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--profile-path", type=Path, default=DEFAULT_PROFILE)
    ap.add_argument("--ledger-key", required=True, help="Ledger marker key, e.g. sachs or mearsheimer")
    ap.add_argument(
        "urls",
        nargs="*",
        help="YouTube URLs or video IDs. If omitted, stdin is scanned for URLs.",
    )
    ap.add_argument("--notebook-root", type=Path, default=NOTEBOOK_ROOT)
    ap.add_argument("--apply", action="store_true", help="Write the refreshed ledger section")
    ap.add_argument(
        "--offline",
        action="store_true",
        help="Do not fetch live YouTube metadata; reflow from the existing ledger rows only.",
    )
    args = ap.parse_args(argv)

    urls = list(args.urls)
    if not urls and not sys.stdin.isatty():
        urls = extract_urls_from_text(sys.stdin.read())

    profile_path = args.profile_path
    if not profile_path.is_absolute():
        profile_path = REPO_ROOT / profile_path

    notebook_root = args.notebook_root
    if not notebook_root.is_absolute():
        notebook_root = REPO_ROOT / notebook_root

    if not profile_path.is_file():
        print(f"missing profile: {profile_path}", file=sys.stderr)
        return 1

    profile_text = profile_path.read_text(encoding="utf-8")
    try:
        updated, added = rebuild_ledger_section(
            profile_text=profile_text,
            ledger_key=args.ledger_key,
            urls=urls,
            notebook_root=notebook_root,
            metadata_fetcher=None if args.offline else fetch_youtube_metadata,
        )
    except ValueError as e:
        print(str(e), file=sys.stderr)
        return 1

    if updated == profile_text:
        print("no ledger changes")
        return 0

    if not args.apply:
        print(updated)
        if added:
            print(f"\nWould add {len(added)} new video id(s): {', '.join(added)}", file=sys.stderr)
        else:
            print("\nDry run only. Pass --apply to write the profile.", file=sys.stderr)
        return 0

    profile_path.write_text(updated, encoding="utf-8")
    if added:
        print(f"updated {profile_path} ({len(added)} new video id(s))")
    else:
        print(f"refreshed {profile_path}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
