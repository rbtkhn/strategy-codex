from __future__ import annotations

import json
from pathlib import Path

import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import build_statecraft_archive_navigation as nav  # noqa: E402
import build_statecraft_day_indices as day_idx  # noqa: E402
import build_statecraft_month_indices as month_idx  # noqa: E402


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def test_build_year_index_rolls_up_months_and_links(tmp_path: Path) -> None:
    root = tmp_path / "source-archive" / "statecraft"
    day_one = root / "2026-05-26"
    day_two = root / "2026-05-27"
    _write(
        day_one / "transcript-napolitano-hoh-why-the-pentagon-lies-2026-05-26.md",
        (
            "---\n"
            'title: "Matt Hoh: Why the Pentagon Lies"\n'
            "show: Judging Freedom\n"
            "host: Judge Andrew Napolitano\n"
            "guest: Matt Hoh\n"
            "thread: hoh\n"
            "---\n\n"
            "Body.\n"
        ),
    )
    _write(
        day_two / "youtube-daniel-davis-deep-dive-us-must-stop-the-siege-of-iran-2026-05-27.md",
        (
            "---\n"
            'title: "US Must Stop the Siege of Iran"\n'
            "show: Daniel Davis Deep Dive\n"
            "host: Daniel Davis\n"
            "guest: Seyed M. Marandi\n"
            "thread: iran\n"
            "---\n\n"
            "Body.\n"
        ),
    )

    rendered = nav.build_year_index(root, "2026")

    assert "# Statecraft Archive - 2026" in rendered
    assert "- Captured months: `1`" in rendered
    assert "- Captured days: `2`" in rendered
    assert "`Judging Freedom` (1)" in rendered
    assert "`Daniel Davis Deep Dive` (1)" in rendered
    assert "| `2026-05` | 2 | 2 |" in rendered
    assert "[open](statecraft/synthesis/month/2026-05.md)" in rendered


def test_build_thread_index_rolls_up_threads_across_days(tmp_path: Path) -> None:
    root = tmp_path / "source-archive" / "statecraft"
    day_one = root / "2026-05-26"
    day_two = root / "2026-05-27"
    _write(
        day_one / "transcript-napolitano-hoh-why-the-pentagon-lies-2026-05-26.md",
        (
            "---\n"
            'title: "Matt Hoh: Why the Pentagon Lies"\n'
            "show: Judging Freedom\n"
            "host: Judge Andrew Napolitano\n"
            "guest: Matt Hoh\n"
            "thread: hoh\n"
            "---\n\n"
            "Body.\n"
        ),
    )
    _write(
        day_two / "transcript-napolitano-hoh-us-foreign-policy-2026-05-27.md",
        (
            "---\n"
            'title: "Matt Hoh: US Foreign Policy"\n'
            "show: Judging Freedom\n"
            "host: Judge Andrew Napolitano\n"
            "guest: Matt Hoh\n"
            "thread: hoh\n"
            "---\n\n"
            "Body.\n"
        ),
    )

    rendered = nav.build_thread_index(root)

    assert "# Statecraft Archive - Thread Index" in rendered
    assert "- Distinct threads: `1`" in rendered
    assert "- Thread-linked source files: `2`" in rendered
    assert "| `hoh` | 2 | 2 | 1 |" in rendered
    assert "`2026-05-26` | `2026-05-27`" in rendered


def test_stale_index_audit_marks_ok_stale_and_missing(tmp_path: Path) -> None:
    root = tmp_path / "source-archive" / "statecraft"
    day_ok = root / "2026-05-26"
    day_stale = root / "2026-05-27"
    day_missing = root / "2026-05-28"
    _write(
        day_ok / "transcript-napolitano-hoh-why-the-pentagon-lies-2026-05-26.md",
        (
            "---\n"
            'title: "Matt Hoh: Why the Pentagon Lies"\n'
            "show: Judging Freedom\n"
            "host: Judge Andrew Napolitano\n"
            "guest: Matt Hoh\n"
            "thread: hoh\n"
            "---\n\n"
            "Body.\n"
        ),
    )
    _write(
        day_stale / "transcript-napolitano-marandi-iran-standoff-2026-05-27.md",
        (
            "---\n"
            'title: "Iran Standoff"\n'
            "show: Judging Freedom\n"
            "host: Judge Andrew Napolitano\n"
            "guest: Seyed M. Marandi\n"
            "thread: marandi\n"
            "---\n\n"
            "Body.\n"
        ),
    )
    _write(
        day_missing / "youtube-daniel-davis-deep-dive-us-must-stop-the-siege-of-iran-2026-05-28.md",
        (
            "---\n"
            'title: "US Must Stop the Siege of Iran"\n'
            "show: Daniel Davis Deep Dive\n"
            "host: Daniel Davis\n"
            "guest: Seyed M. Marandi\n"
            "thread: iran\n"
            "---\n\n"
            "Body.\n"
        ),
    )

    day_idx.write_day_index(day_ok)
    _write(day_stale / "README.md", "# stale\n")
    month_groups = month_idx.group_day_dirs_by_month(root, "2026")
    month_idx.write_month_index(root, "2026-05", month_groups["2026-05"])
    nav.write_rendered(root / "2026.md", nav.build_year_index(root, "2026"))
    nav.write_rendered(root / "thread-index.md", nav.build_thread_index(root))

    rendered = nav.build_stale_index_audit(root)

    assert "- Day indices:" in rendered
    assert "`ok` (1)" in rendered
    assert "`stale` (1)" in rendered
    assert "`missing` (1)" in rendered
    assert "| `2026-05-26` | `ok` |" in rendered
    assert "| `2026-05-27` | `stale` |" in rendered
    assert "| `2026-05-28` | `missing` |" in rendered
    assert "- Month indices: `ok` (1)" in rendered
    assert "- Year indices: `ok` (1)" in rendered
    assert "- Thread index: `ok`" in rendered


def test_channel_registry_key_routes_configured_host_only_davis_captures() -> None:
    davis_meta = {
        "source_type": "youtube",
        "youtube_id": "abc123",
        "host": "Daniel Davis / Deep Dive",
    }
    slug, label, explicit = nav._channel_registry_key(davis_meta)
    assert slug == "daniel-davis"
    assert label == "Daniel Davis / Deep Dive"
    assert explicit is False

    napolitano_meta = {
        "source_type": "youtube",
        "youtube_id": "xyz789",
        "host": "Judge Andrew Napolitano",
    }
    slug, _, _ = nav._channel_registry_key(napolitano_meta)
    assert slug == "judging-freedom"

    diesen_fname_meta = {
        "source_type": "youtube",
        "youtube_id": "def456",
    }
    slug, _, _ = nav._channel_registry_key(
        diesen_fname_meta,
        "source-diesen-wilkerson-ceasefire-fails-2026-04-10.md",
    )
    assert slug == "glenn-diesen"


def test_channel_registry_key_routes_configured_series_values() -> None:
    duran_meta = {
        "source_url": "https://www.youtube.com/watch?v=abc123",
        "series": "The Duran",
    }
    slug, label, explicit = nav._channel_registry_key(duran_meta)
    assert slug == "the-duran"
    assert label == "The Duran"
    assert explicit is False

    jf_meta = {
        "source_url": "https://www.youtube.com/watch?v=def456",
        "series": "Judging Freedom",
    }
    slug, _, _ = nav._channel_registry_key(jf_meta)
    assert slug == "judging-freedom"

    ritter_meta = {
        "source_url": "https://www.youtube.com/watch?v=7pXI52jKcOU",
        "series": "Ritter's Rant",
    }
    slug, label, explicit = nav._channel_registry_key(ritter_meta)
    assert slug == "scott-ritter"
    assert label == "Ritter's Rant"
    assert explicit is False

    kiriakou_meta = {
        "source_type": "youtube",
        "source_url": "https://www.youtube.com/watch?v=DuZALiYzcmA",
    }
    slug, _, _ = nav._channel_registry_key(
        kiriakou_meta,
        "source-kiriakou-anthony-aguilar-gaza-whistleblower-death-by-design-2026-02-27.md",
    )
    assert slug == "john-kiriakou"


def test_channel_index_excludes_misc_slugs_from_main_index() -> None:
    root = REPO_ROOT / "source-archive" / "statecraft"
    rendered = nav.build_channel_index(root)
    misc = nav.build_channel_index_misc(root)
    assert "jeffrey-sachs" not in rendered
    assert "jeffrey-sachs" in misc
    assert "john-kiriakou" in misc
    assert "scott-ritter" in misc
    assert "`unknown`" not in rendered
    assert "channel-index-misc.md" in rendered
    assert "channel-index.json" in rendered


def test_build_channel_index_json_main_roster_excludes_misc() -> None:
    root = REPO_ROOT / "source-archive" / "statecraft"
    payload = nav.build_channel_index_json(root)
    slugs = {row["slug"] for row in payload["channels"]}

    assert payload["check_sources_scope"] == "main"
    assert payload["stats"]["main_channel_count"] == len(payload["channels"])
    assert "jeffrey-sachs" not in slugs
    assert "john-kiriakou" not in slugs
    assert "scott-ritter" not in slugs
    assert all(row["check_sources"] is True for row in payload["channels"])
    assert payload["stats"]["watchlist_count"] == sum(1 for row in payload["channels"] if row["watchlist"])
    assert payload["stats"]["discoverable_count"] == 15
    assert all(row["discoverable"] for row in payload["channels"])


def test_main_roster_slugs_have_full_discovery_rows() -> None:
    import statecraft_youtube_discovery as discovery

    roster = discovery.load_check_sources_roster(rebuild=True)
    by_key = discovery.load_discovery_channel_rows_by_key()
    slugs = {row["slug"] for row in roster}
    assert len(slugs) == 15
    for slug in slugs:
        assert slug in by_key, slug
        assert str(by_key[slug].get("channel_id") or "").startswith("UC"), slug
        assert str(by_key[slug].get("handle_url") or "").startswith("http"), slug


def test_load_check_sources_roster_reads_json_or_rebuilds(tmp_path: Path) -> None:
    import statecraft_youtube_discovery as discovery

    archive_root = tmp_path / "source-archive" / "statecraft"
    day_dir = archive_root / "2026-05-26"
    _write(
        day_dir / "transcript-napolitano-hoh-why-the-pentagon-lies-2026-05-26.md",
        (
            "---\n"
            'title: "Matt Hoh: Why the Pentagon Lies"\n'
            "source_type: youtube\n"
            "youtube_id: abc123\n"
            "show: Judging Freedom\n"
            "host: Judge Andrew Napolitano\n"
            "---\n\n"
            "Body.\n"
        ),
    )
    _write(
        day_dir / "source-kiriakou-anthony-aguilar-gaza-whistleblower-death-by-design-2026-02-27.md",
        (
            "---\n"
            'title: "Gaza whistleblower"\n'
            "source_type: youtube\n"
            "youtube_id: def456\n"
            "---\n\n"
            "Body.\n"
        ),
    )

    payload = nav.build_channel_index_json(archive_root)
    json_path = archive_root / "channel-index.json"
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    roster = discovery.load_check_sources_roster(root=archive_root)
    slugs = {row["slug"] for row in roster}
    assert "judging-freedom" in slugs
    assert "john-kiriakou" not in slugs

    rebuilt = discovery.load_check_sources_roster(root=archive_root, rebuild=True)
    assert {row["slug"] for row in rebuilt} == slugs


def test_build_writer_index_counts_configured_substack_feeds(tmp_path: Path, monkeypatch) -> None:
    import statecraft_writer_index as writer_index

    root = tmp_path / "source-archive" / "statecraft"
    day = root / "2026-06-18"
    _write(
        day / "source-crooke-israel-picking-up-pieces-2026-06-18.md",
        (
            "---\n"
            "kind: substack-post\n"
            "source_form: newsletter\n"
            "source_type: substack\n"
            "thread: crooke\n"
            'source_url: "https://conflictsforum.substack.com/p/israel-picking-up-the-pieces-of-its"\n'
            "author: Alastair Crooke\n"
            "---\n\n"
            "Body.\n"
        ),
    )
    _write(
        day / "source-pape-stage-iv-begins-2026-06-17.md",
        (
            "---\n"
            "kind: substack-post\n"
            "source_type: substack-post\n"
            "thread: pape\n"
            'source_url: "https://escalationtrap.substack.com/p/stage-iv-begins"\n'
            "---\n\n"
            "Body.\n"
        ),
    )

    config = tmp_path / "writers.json"
    config.write_text(
        json.dumps(
            {
                "writer_slug_aliases": {},
                "writers": [
                    {
                        "writer_slug": "crooke",
                        "label": "Alastair Crooke",
                        "thread": "crooke",
                        "feed_url": "https://conflictsforum.substack.com/",
                        "feed_host": "conflictsforum.substack.com",
                        "check_written": True,
                    },
                    {
                        "writer_slug": "pape",
                        "label": "Prof Robert Pape",
                        "thread": "pape",
                        "feed_url": "https://escalationtrap.substack.com/",
                        "feed_host": "escalationtrap.substack.com",
                        "check_written": True,
                    },
                ],
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(writer_index, "WRITER_DISCOVERY_CONFIG_PATH", config)

    payload = writer_index.build_writer_index_json(root, config)
    by_slug = {row["writer_slug"]: row for row in payload["writers"]}
    assert payload["stats"]["writer_count"] == 2
    assert by_slug["crooke"]["file_count"] == 1
    assert by_slug["pape"]["file_count"] == 1

    rendered = writer_index.build_writer_index(root, config)
    assert "# Statecraft Archive - Writer Index" in rendered
    assert "`crooke`" in rendered
    assert "`pape`" in rendered


def test_is_youtube_capture_shared_membrane_helper() -> None:
    from statecraft_day_archive import is_youtube_capture

    assert is_youtube_capture({"source_type": "youtube"}) is True
    assert is_youtube_capture({"youtube_id": "abc123"}) is True
    assert is_youtube_capture({"source_url": "https://www.youtube.com/watch?v=abc"}) is True
    assert is_youtube_capture({"source_url": "https://youtu.be/abc"}) is True
    assert is_youtube_capture({"source_type": "substack", "source_url": "https://conflictsforum.substack.com/p/x"}) is False


def test_writer_index_includes_ritter_prose_on_transcript(tmp_path: Path, monkeypatch) -> None:
    import statecraft_writer_index as writer_index

    root = tmp_path / "source-archive" / "statecraft"
    day = root / "2026-06-18"
    _write(
        day / "source-ritter-essay-on-geneva-2026-06-18.md",
        (
            "---\n"
            "kind: operator-transcript\n"
            "source_form: newsletter\n"
            "source_type: substack\n"
            "thread: ritter\n"
            'source_url: "https://scottritter.substack.com/p/geneva"\n'
            "---\n\n"
            "Body.\n"
        ),
    )
    config = tmp_path / "writers.json"
    config.write_text(
        json.dumps(
            {
                "writer_slug_aliases": {},
                "writers": [
                    {
                        "writer_slug": "ritter",
                        "label": "Scott Ritter",
                        "thread": "ritter",
                        "feed_url": "https://scottritter.substack.com/",
                        "feed_host": "scottritter.substack.com",
                        "check_written": True,
                        "require_substack_signal": True,
                    },
                ],
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(writer_index, "WRITER_DISCOVERY_CONFIG_PATH", config)

    payload = writer_index.build_writer_index_json(root, config)
    by_slug = {row["writer_slug"]: row for row in payload["writers"]}
    assert by_slug["ritter"]["file_count"] == 1


def test_load_check_written_roster_reads_json_or_rebuilds(tmp_path: Path, monkeypatch) -> None:
    import statecraft_writer_index as writer_index

    archive_root = tmp_path / "source-archive" / "statecraft"
    day = archive_root / "2026-06-18"
    _write(
        day / "source-crooke-israel-picking-up-pieces-2026-06-18.md",
        (
            "---\n"
            "kind: substack-post\n"
            "source_form: newsletter\n"
            "source_type: substack\n"
            "thread: crooke\n"
            'source_url: "https://conflictsforum.substack.com/p/israel-picking-up-the-pieces-of-its"\n'
            "---\n\n"
            "Body.\n"
        ),
    )
    config = tmp_path / "writers.json"
    config.write_text(
        json.dumps(
            {
                "writer_slug_aliases": {},
                "writer_index_misc_slugs": ["one-off"],
                "writers": [
                    {
                        "writer_slug": "crooke",
                        "label": "Alastair Crooke",
                        "thread": "crooke",
                        "feed_url": "https://conflictsforum.substack.com/",
                        "feed_host": "conflictsforum.substack.com",
                        "check_written": True,
                    },
                    {
                        "writer_slug": "one-off",
                        "label": "One-off outlet",
                        "thread": "one-off",
                        "feed_url": "https://example.substack.com/",
                        "feed_host": "example.substack.com",
                        "check_written": True,
                    },
                ],
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(writer_index, "WRITER_DISCOVERY_CONFIG_PATH", config)

    payload = writer_index.build_writer_index_json(archive_root, config)
    json_path = archive_root / "writer-index.json"
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    roster = writer_index.load_check_written_roster(root=archive_root, config_path=config)
    slugs = {row["writer_slug"] for row in roster}
    assert slugs == {"crooke"}

    rebuilt = writer_index.load_check_written_roster(root=archive_root, config_path=config, rebuild=True)
    assert {row["writer_slug"] for row in rebuilt} == slugs


def test_configured_writer_roster_slugs_have_discovery_rows() -> None:
    import statecraft_writer_index as writer_index

    roster = writer_index.load_check_written_roster(rebuild=True)
    by_slug = writer_index.load_writer_rows_by_slug()
    slugs = {row["writer_slug"] for row in roster}
    assert len(slugs) == 6
    for slug in slugs:
        assert slug in by_slug, slug
        assert str(by_slug[slug].get("feed_url") or "").startswith("http"), slug
        assert str(by_slug[slug].get("feed_host") or ""), slug
