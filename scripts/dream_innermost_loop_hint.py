#!/usr/bin/env python3
"""Metadata-only frontier hint for The Innermost Loop.

This helper is used by dream as an operational next-day signal. It reads only
RSS metadata and intentionally avoids storing post bodies or generated
summaries.
"""

from __future__ import annotations

import html
import re
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Any

SOURCE_ID = "the-innermost-loop"
SOURCE_NAME = "The Innermost Loop"
FEED_URL = "https://theinnermostloop.substack.com/feed"
SOURCE_MODE = "live_lookup"
DEFAULT_TIMEOUT_SECONDS = 5


def _clean_text(value: str | None) -> str:
    text = html.unescape(value or "")
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _parse_rss_datetime(value: str) -> datetime | None:
    try:
        dt = parsedate_to_datetime(value)
    except (TypeError, ValueError):
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _item_timestamp(item: ET.Element) -> datetime:
    for tag in ("pubDate", "updated", "published"):
        text = _clean_text(item.findtext(tag))
        if not text:
            continue
        parsed = _parse_rss_datetime(text)
        if parsed is not None:
            return parsed
    return datetime.min.replace(tzinfo=timezone.utc)


def parse_latest_post(feed_xml: str) -> dict[str, str]:
    """Parse RSS XML and return metadata for the newest item."""
    root = ET.fromstring(feed_xml)
    items = root.findall(".//item")
    if not items:
        raise ValueError("feed contained no RSS items")

    latest = max(items, key=_item_timestamp)
    title = _clean_text(latest.findtext("title"))
    url = _clean_text(latest.findtext("link"))
    published_raw = _clean_text(latest.findtext("pubDate"))
    published_dt = _parse_rss_datetime(published_raw)

    if not title:
        raise ValueError("latest RSS item is missing a title")
    if not url:
        raise ValueError("latest RSS item is missing a link")

    return {
        "title": title,
        "url": url,
        "published_at": published_dt.isoformat() if published_dt else published_raw,
    }


def fetch_feed_xml(*, feed_url: str = FEED_URL, timeout: int = DEFAULT_TIMEOUT_SECONDS) -> str:
    request = urllib.request.Request(
        feed_url,
        headers={
            "User-Agent": "strategy-codex-dream/1.0 (+metadata-only frontier watch)",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def build_frontier_source_hint(
    *,
    feed_xml: str | None = None,
    feed_url: str = FEED_URL,
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Return a metadata-only hint for the latest Innermost Loop post.

    Network and parser failures are intentionally represented as data so dream
    can continue without treating a source-watch miss as a failed night-close.
    """
    fetched_at = (now or datetime.now(timezone.utc)).astimezone(timezone.utc).isoformat()
    base: dict[str, Any] = {
        "source_id": SOURCE_ID,
        "source_name": SOURCE_NAME,
        "feed_url": feed_url,
        "source_mode": SOURCE_MODE,
        "fetched_at": fetched_at,
    }

    try:
        xml_text = feed_xml if feed_xml is not None else fetch_feed_xml(feed_url=feed_url, timeout=timeout)
        latest = parse_latest_post(xml_text)
    except (ET.ParseError, ValueError, urllib.error.URLError, TimeoutError, OSError) as exc:
        return {
            **base,
            "status": "unavailable",
            "error": f"{type(exc).__name__}: {_clean_text(str(exc))[:180]}",
        }

    title = latest["title"]
    published = latest.get("published_at") or "unknown date"
    guidance = (
        "AI frontier watch: latest The Innermost Loop post is "
        f"\"{title}\" ({published}); decide tomorrow whether it merits Coffee C source hygiene."
    )
    return {
        **base,
        "status": "ok",
        "title": title,
        "url": latest["url"],
        "published_at": published,
        "guidance": guidance,
    }


def format_frontier_source_followup(hint: dict[str, Any]) -> str | None:
    if hint.get("status") != "ok":
        return None
    title = _clean_text(str(hint.get("title") or "untitled"))[:120]
    return (
        f"AI frontier watch: The Innermost Loop latest - {title} - "
        "consider Coffee C source hygiene if relevant tomorrow"
    )


def main() -> int:
    import json

    print(json.dumps(build_frontier_source_hint(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
