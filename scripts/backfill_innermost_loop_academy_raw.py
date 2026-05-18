#!/usr/bin/env python3
"""Backfill The Innermost Loop into the academy singularity workshop.

Uses Substack's public JSON endpoints:
  GET https://theinnermostloop.substack.com/api/v1/archive?sort=new&offset=N&limit=50
  GET https://theinnermostloop.substack.com/api/v1/posts/{slug}

Writes one full, local, plain-text raw capture per newsletter under:
  codex/2026/academy/singularity/workshop/raw-input/innermost-loop/

WORK only; not Record.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from html import unescape
import json
from pathlib import Path
import re
import sys
from typing import Iterable
import urllib.error
import urllib.request

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_HOST = "theinnermostloop.substack.com"
DEFAULT_RAW_ROOT = (
    REPO_ROOT
    / "codex/2026/academy/singularity/workshop/raw-input/innermost-loop"
)
DEFAULT_WORKSHOP_README = REPO_ROOT / "codex/2026/academy/singularity/workshop/README.md"
DEFAULT_SHELF_README = REPO_ROOT / "codex/2026/academy/singularity/README.md"
USER_AGENT = "strategy-codex-innermost-loop-backfill/1.0 (+local academy singularity)"

MONTHS = {
    "jan": 1,
    "january": 1,
    "feb": 2,
    "february": 2,
    "mar": 3,
    "march": 3,
    "apr": 4,
    "april": 4,
    "may": 5,
    "jun": 6,
    "june": 6,
    "jul": 7,
    "july": 7,
    "aug": 8,
    "august": 8,
    "sep": 9,
    "sept": 9,
    "september": 9,
    "oct": 10,
    "october": 10,
    "nov": 11,
    "november": 11,
    "dec": 12,
    "december": 12,
}


@dataclass(frozen=True)
class CaptureResult:
    day: date
    path: Path
    title: str
    url: str
    status: str


def _relative(path: Path, root: Path = REPO_ROOT) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve())).replace("\\", "/")
    except ValueError:
        return str(path)


def _fetch_json(url: str, *, timeout: int = 60) -> object:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _post_day_utc(iso_z: str) -> date:
    if not iso_z:
        raise ValueError("missing post_date")
    if iso_z.endswith("Z"):
        iso_z = iso_z[:-1] + "+00:00"
    dt = datetime.fromisoformat(iso_z)
    if dt.tzinfo is not None:
        dt = dt.astimezone(timezone.utc)
    return dt.date()


def _strip_html(html: str) -> str:
    if not html:
        return ""
    text = re.sub(r"(?is)<script[^>]*>.*?</script>", " ", html)
    text = re.sub(r"(?is)<style[^>]*>.*?</style>", " ", text)
    text = re.sub(r"(?i)<br\s*/?>", "\n", text)
    text = re.sub(r"(?i)</(p|div|section|article|h[1-6]|blockquote)\s*>", "\n\n", text)
    text = re.sub(r"(?i)<li[^>]*>", "\n- ", text)
    text = re.sub(r"(?i)</li\s*>", "\n", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = unescape(text)
    lines = [re.sub(r"[ \t\r\f\v]+", " ", line).strip() for line in text.splitlines()]
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _date_from_title_or_slug(title: str, slug: str, published: date) -> date:
    combined = f"{title} {slug}".lower()
    m = re.search(
        r"\b("
        + "|".join(sorted(MONTHS, key=len, reverse=True))
        + r")[-\s]+(\d{1,2})(?:st|nd|rd|th)?(?:,)?[-\s]+(\d{4})\b",
        combined,
    )
    if not m:
        return published
    month = MONTHS[m.group(1)]
    return date(int(m.group(3)), month, int(m.group(2)))


def _canonical_url(post: dict, host: str) -> str:
    slug = str(post.get("slug") or "").strip()
    return str(post.get("canonical_url") or f"https://{host}/p/{slug}")


def _build_capture_doc(*, detail: dict, host: str, capture_date: date) -> tuple[date, str]:
    title = str(detail.get("title") or detail.get("slug") or "Untitled")
    slug = str(detail.get("slug") or "").strip()
    published = _post_day_utc(str(detail.get("post_date") or ""))
    title_day = _date_from_title_or_slug(title, slug, published)
    url = _canonical_url(detail, host)
    body_text = _strip_html(str(detail.get("body_html") or ""))
    subtitle = str(detail.get("subtitle") or detail.get("description") or "").strip()

    front = [
        "---",
        f"capture_date: {capture_date.isoformat()}",
        f"title_date: {title_day.isoformat()}",
        f"published_date: {published.isoformat()}",
        "kind: substack-newsletter-raw-capture",
        "source: the-innermost-loop",
        "publication: The Innermost Loop",
        "author: Dr. Alex Wissner-Gross",
        f"source_url: {url}",
        f"slug: {slug}",
    ]
    if detail.get("id") is not None:
        front.append(f"post_id: {detail.get('id')}")
    front.append("---")

    parts = [
        "\n".join(front),
        "",
        f"# The Innermost Loop - {title_day.isoformat()}",
        "",
        "WORK only; not Record.",
        "",
        "## Source",
        "",
        f"- Title: {title}",
        f"- URL: {url}",
        f"- Published: {published.isoformat()}",
        f"- Captured: {capture_date.isoformat()}",
        "- Capture mode: full local raw capture; HTML stripped to plain text.",
        "",
    ]
    if subtitle:
        parts.extend(["## Teaser", "", subtitle, ""])
    parts.extend(
        [
            "## Newsletter Text",
            "",
            body_text or "_(empty body from Substack API)_",
            "",
            "_Backfilled by `scripts/backfill_innermost_loop_academy_raw.py`; local WORK copy, not Record._",
            "",
        ]
    )
    return title_day, "\n".join(parts)


def _fetch_archive_posts(*, host: str, since: date, until: date, page_size: int) -> list[dict]:
    collected: dict[str, dict] = {}
    offset = 0
    stop_before = since - timedelta(days=2)
    while True:
        url = f"https://{host}/api/v1/archive?sort=new&offset={offset}&limit={page_size}"
        batch = _fetch_json(url)
        if not isinstance(batch, list) or not batch:
            break
        dated_batch: list[tuple[date, dict]] = []
        for item in batch:
            if not isinstance(item, dict) or not item.get("slug"):
                continue
            try:
                published = _post_day_utc(str(item.get("post_date") or ""))
            except ValueError:
                continue
            dated_batch.append((published, item))
            if stop_before <= published <= until + timedelta(days=2):
                collected[str(item["slug"])] = item
        if dated_batch and all(day < stop_before for day, _ in dated_batch):
            break
        offset += len(batch)
    return sorted(collected.values(), key=lambda x: str(x.get("post_date") or ""))


def _render_index_lines(results: Iterable[CaptureResult], *, link_prefix: str) -> list[str]:
    lines: list[str] = []
    for result in sorted(results, key=lambda r: r.day):
        rel = f"{link_prefix.rstrip('/')}/{result.path.name}"
        lines.append(
            f"- [The Innermost Loop raw - {result.day.isoformat()}]({rel}) - full newsletter capture."
        )
    return lines


def _replace_or_insert_section(text: str, heading: str, body: str, *, before_heading: str | None = None) -> str:
    pattern = re.compile(rf"(?ms)^## {re.escape(heading)}\n.*?(?=^## |\Z)")
    replacement = f"## {heading}\n\n{body.rstrip()}\n\n"
    if pattern.search(text):
        return pattern.sub(replacement, text)
    if before_heading and f"## {before_heading}" in text:
        idx = text.index(f"## {before_heading}")
        return (text[:idx].rstrip() + "\n\n" + replacement + text[idx:].lstrip()).rstrip() + "\n"
    return text.rstrip() + "\n\n" + replacement


def _update_readmes(
    *,
    raw_root: Path,
    workshop_readme: Path,
    shelf_readme: Path,
    apply: bool,
) -> None:
    files = sorted(raw_root.glob("innermost-loop-*.md"))
    results = []
    for path in files:
        m = re.search(r"(\d{4}-\d{2}-\d{2})", path.name)
        if not m:
            continue
        results.append(
            CaptureResult(
                day=datetime.strptime(m.group(1), "%Y-%m-%d").date(),
                path=path,
                title=f"The Innermost Loop raw - {m.group(1)}",
                url="",
                status="indexed",
            )
        )
    if not results:
        return

    workshop_body = (
        "Full local captures live here for close reading. Interpretive source sheets stay in "
        "`sheets/`; this folder preserves the newsletter text used to build them.\n\n"
        + "\n".join(_render_index_lines(results, link_prefix="raw-input/innermost-loop"))
    )
    shelf_body = (
        "Full local captures for the current Innermost Loop backfill live under "
        "`workshop/raw-input/innermost-loop/`.\n\n"
        + "\n".join(_render_index_lines(results, link_prefix="workshop/raw-input/innermost-loop"))
    )

    if workshop_readme.is_file():
        text = workshop_readme.read_text(encoding="utf-8")
        new_text = _replace_or_insert_section(
            text,
            "Raw Captures",
            workshop_body,
            before_heading="First Instruments To Build",
        )
        if new_text != text:
            if apply:
                workshop_readme.write_text(new_text, encoding="utf-8")
                print(f"updated: {_relative(workshop_readme)}")
            else:
                print(f"would update: {_relative(workshop_readme)}")

    if shelf_readme.is_file():
        text = shelf_readme.read_text(encoding="utf-8")
        new_text = _replace_or_insert_section(
            text,
            "Raw Capture Backfill",
            shelf_body,
            before_heading=None,
        )
        if new_text != text:
            if apply:
                shelf_readme.write_text(new_text, encoding="utf-8")
                print(f"updated: {_relative(shelf_readme)}")
            else:
                print(f"would update: {_relative(shelf_readme)}")


def run(
    *,
    host: str,
    raw_root: Path,
    workshop_readme: Path,
    shelf_readme: Path,
    today: date,
    days: int,
    apply: bool,
    overwrite: bool,
    page_size: int,
) -> int:
    since = today - timedelta(days=days)
    until = today
    host = host.strip().removeprefix("https://").rstrip("/")
    posts = _fetch_archive_posts(host=host, since=since, until=until, page_size=page_size)
    results: list[CaptureResult] = []

    for post in posts:
        slug = str(post.get("slug") or "")
        try:
            detail = _fetch_json(f"https://{host}/api/v1/posts/{slug}")
        except (urllib.error.URLError, json.JSONDecodeError, TimeoutError, ValueError) as e:
            print(f"skip {slug}: {e}", file=sys.stderr)
            continue
        if not isinstance(detail, dict):
            continue
        try:
            title_day, content = _build_capture_doc(
                detail=detail,
                host=host,
                capture_date=today,
            )
        except ValueError as e:
            print(f"skip {slug}: {e}", file=sys.stderr)
            continue
        if not (since <= title_day <= until):
            continue
        dest = raw_root / f"innermost-loop-{title_day.isoformat()}.md"
        title = str(detail.get("title") or slug)
        url = _canonical_url(detail, host)
        if dest.is_file() and not overwrite:
            print(f"skip existing: {_relative(dest)}")
            results.append(CaptureResult(title_day, dest, title, url, "existing"))
            continue
        if dest.is_file() and dest.read_text(encoding="utf-8") == content:
            print(f"skip unchanged: {_relative(dest)}")
            results.append(CaptureResult(title_day, dest, title, url, "unchanged"))
            continue
        existed_before = dest.is_file()
        if not apply:
            action = "would overwrite" if dest.is_file() else "would write"
            print(f"{action}: {_relative(dest)}")
            results.append(CaptureResult(title_day, dest, title, url, "planned"))
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content, encoding="utf-8")
        print(f"{'overwrote' if existed_before else 'wrote'}: {_relative(dest)}")
        results.append(CaptureResult(title_day, dest, title, url, "written"))

    if results:
        _update_readmes(
            raw_root=raw_root,
            workshop_readme=workshop_readme,
            shelf_readme=shelf_readme,
            apply=apply,
        )
    else:
        print(f"No Innermost Loop posts found from {since.isoformat()} through {until.isoformat()}.")

    if not apply:
        print("\nDry-run only. Pass --apply to write raw captures.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--host", default=DEFAULT_HOST)
    ap.add_argument("--root", type=Path, default=DEFAULT_RAW_ROOT)
    ap.add_argument("--workshop-readme", type=Path, default=DEFAULT_WORKSHOP_README)
    ap.add_argument("--shelf-readme", type=Path, default=DEFAULT_SHELF_README)
    ap.add_argument("--today", default=None, help="YYYY-MM-DD; default is local date")
    ap.add_argument("--days", type=int, default=14, help="look back this many days from --today")
    ap.add_argument("--page-size", type=int, default=30)
    ap.add_argument("--overwrite", action="store_true", help="replace existing raw captures")
    ap.add_argument("--apply", action="store_true", help="write files; default is dry-run")
    args = ap.parse_args()

    today = (
        datetime.strptime(args.today, "%Y-%m-%d").date()
        if args.today
        else date.today()
    )
    return run(
        host=args.host,
        raw_root=args.root,
        workshop_readme=args.workshop_readme,
        shelf_readme=args.shelf_readme,
        today=today,
        days=max(1, args.days),
        apply=args.apply,
        overwrite=args.overwrite,
        page_size=max(1, min(args.page_size, 50)),
    )


if __name__ == "__main__":
    raise SystemExit(main())
