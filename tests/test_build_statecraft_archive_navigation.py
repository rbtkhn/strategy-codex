from __future__ import annotations

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
    assert "[open](./2026-05.md)" in rendered


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
    assert slug == "alexander-mercouris"
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
