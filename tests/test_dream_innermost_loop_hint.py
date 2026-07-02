from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import dream_innermost_loop_hint as hint

RSS_FIXTURE = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>The Innermost Loop</title>
    <item>
      <title>Older Post</title>
      <link>https://theinnermostloop.substack.com/p/older</link>
      <pubDate>Fri, 08 May 2026 12:00:00 GMT</pubDate>
      <description>This body should not be retained.</description>
    </item>
    <item>
      <title>Latest &amp; Sharper &lt;script&gt;bad&lt;/script&gt;</title>
      <link>https://theinnermostloop.substack.com/p/latest</link>
      <pubDate>Sat, 09 May 2026 12:30:00 GMT</pubDate>
      <description>This body should not be retained either.</description>
    </item>
  </channel>
</rss>
"""

def test_parse_latest_post_selects_newest_and_sanitizes_title():
    latest = hint.parse_latest_post(RSS_FIXTURE)

    assert latest["url"] == "https://theinnermostloop.substack.com/p/latest"
    assert latest["published_at"] == "2026-05-09T12:30:00+00:00"
    assert "<script>" not in latest["title"]
    assert latest["title"] == "Latest & Sharper bad"

def test_build_frontier_source_hint_is_metadata_only():
    result = hint.build_frontier_source_hint(
        feed_xml=RSS_FIXTURE,
        now=datetime(2026, 5, 9, 13, 0, tzinfo=timezone.utc),
    )

    assert result["status"] == "ok"
    assert result["source_id"] == "the-innermost-loop"
    assert result["source_mode"] == "live_lookup"
    assert result["title"] == "Latest & Sharper bad"
    assert result["url"] == "https://theinnermostloop.substack.com/p/latest"
    assert result["fetched_at"] == "2026-05-09T13:00:00+00:00"
    assert "guidance" in result
    assert "description" not in result
    assert "body" not in result
    assert "This body should not be retained" not in str(result)

def test_build_frontier_source_hint_failure_is_non_blocking():
    result = hint.build_frontier_source_hint(feed_xml="<not xml")

    assert result["status"] == "unavailable"
    assert result["source_name"] == "The Innermost Loop"
    assert result["source_mode"] == "live_lookup"
    assert "error" in result

def test_format_frontier_source_followup_only_for_ok_hint():
    ok = hint.build_frontier_source_hint(feed_xml=RSS_FIXTURE)
    unavailable = hint.build_frontier_source_hint(feed_xml="<not xml")

    followup = hint.format_frontier_source_followup(ok)

    assert followup is not None
    assert "AI frontier watch" in followup
    assert "explicit source hygiene" in followup
    assert hint.format_frontier_source_followup(unavailable) is None
