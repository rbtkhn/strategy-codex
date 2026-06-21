from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import build_statecraft_day_indices as idx  # noqa: E402
import statecraft_day_source_index as day_source  # noqa: E402


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def test_build_day_index_uses_frontmatter_rollups_and_partitions_channel_sources(tmp_path: Path) -> None:
    day = tmp_path / "source-archive" / "statecraft" / "2026-05-26"
    _write(
        day / "transcript-napolitano-hoh-why-the-pentagon-lies-2026-05-26.md",
        (
            "---\n"
            'title: "Matt Hoh: Why the Pentagon Lies"\n'
            "show: Judging Freedom\n"
            "host: Judge Andrew Napolitano\n"
            "guest: Matt Hoh\n"
            "thread: hoh\n"
            "source_type: operator-pasted-youtube-transcript\n"
            "youtube_id: abc123test\n"
            "source_url: https://www.youtube.com/watch?v=abc123test\n"
            "---\n\n"
            "# Matt Hoh: Why the Pentagon Lies\n"
        ),
    )
    _write(
        day / "youtube-daniel-davis-deep-dive-us-must-stop-the-siege-of-iran-2026-05-26.md",
        (
            "---\n"
            'title: "US Must Stop the Siege of Iran"\n'
            "show: Daniel Davis Deep Dive\n"
            "host: Daniel Davis\n"
            "guests:\n"
            "  - Seyed M. Marandi\n"
            "  - Daniel Davis\n"
            "thread: davis\n"
            "source_type: youtube\n"
            "---\n\n"
            "# US Must Stop the Siege of Iran\n"
        ),
    )
    _write(day / "README.md", "# old\n")

    text = idx.build_day_index(day)

    assert "# Statecraft Archive - Day Index - 2026-05-26" in text
    assert "- Source files: `2`" in text
    assert "- Channel sources: `2`" in text
    assert "- Writer sources: `0`" in text
    assert "`transcript` (1)" in text and "`youtube` (1)" in text
    assert "## Channel sources" in text
    assert "## Writer sources" in text
    assert "## Other sources" in text
    assert "Matt Hoh" not in text or "abc123test" in text
    assert "[abc123test](https://www.youtube.com/watch?v=abc123test)" in text
    assert "- `README.md`" not in text
    assert "- `transcript-napolitano-hoh-why-the-pentagon-lies-2026-05-26.md`" in text
    assert "- `youtube-daniel-davis-deep-dive-us-must-stop-the-siege-of-iran-2026-05-26.md`" in text


def test_build_day_index_partitions_writer_and_channel_without_overlap(
    tmp_path: Path, monkeypatch
) -> None:
    import statecraft_writer_index as writer_index

    day = tmp_path / "source-archive" / "statecraft" / "2026-06-18"
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
    _write(
        day / "source-alex-mercouris-sample-2026-06-18.md",
        (
            "---\n"
            'title: "Mercouris sample"\n'
            "source_type: youtube\n"
            "youtube_id: abc123\n"
            "thread: mercouris\n"
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
                ],
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(writer_index, "WRITER_DISCOVERY_CONFIG_PATH", config)

    text = idx.build_day_index(day)

    assert "- Channel sources: `1`" in text
    assert "- Writer sources: `1`" in text
    assert "`crooke`" in text
    assert "conflictsforum.substack.com" in text
    assert "`mercouris`" in text or "abc123" in text


def test_build_day_readme_stub_points_at_day_index(tmp_path: Path) -> None:
    day = tmp_path / "source-archive" / "statecraft" / "2026-06-18"
    day.mkdir(parents=True)
    stub = idx.build_day_readme_stub(day)
    assert "[day-index.md](./day-index.md)" in stub


def test_write_day_index_writes_day_index_and_readme_stub(tmp_path: Path) -> None:
    day = tmp_path / "source-archive" / "statecraft" / "2026-03-16"
    _write(
        day / "substack-pape-irans-new-battlefield-the-global-2026-03-16.md",
        (
            "---\n"
            'title: "Iran\'s New Battlefield"\n'
            "publication: Substack\n"
            "author: Robert Pape\n"
            "thread: pape\n"
            "---\n\n"
            "Body.\n"
        ),
    )
    _write(day / "README.md", "placeholder\n")

    out_path, _changed = idx.write_day_index(day)
    index_text = (day / "day-index.md").read_text(encoding="utf-8")
    stub_text = (day / "README.md").read_text(encoding="utf-8")

    assert out_path == day / "day-index.md"
    assert "# Statecraft Archive - Day Index - 2026-03-16" in index_text
    assert "placeholder" not in stub_text
    assert "[day-index.md](./day-index.md)" in stub_text


def test_statecraft_day_source_index_reads_day_index_file(tmp_path: Path) -> None:
    day = tmp_path / "source-archive" / "statecraft" / "2026-06-17"
    _write(day / "day-index.md", "# Statecraft Archive - Day Index - 2026-06-17\n")
    path, text = day_source.load_day_index("2026-06-17", root=tmp_path / "source-archive" / "statecraft")
    assert path.name == "day-index.md"
    assert "Day Index" in text


def test_iter_day_dirs_filters_to_requested_year(tmp_path: Path) -> None:
    root = tmp_path / "source-archive" / "statecraft"
    (root / "2026-01-01").mkdir(parents=True)
    (root / "2026-02-01").mkdir()
    (root / "2025-12-31").mkdir()
    (root / "_aired-pending").mkdir()

    got = idx._iter_day_dirs(root, "2026")

    assert [p.name for p in got] == ["2026-01-01", "2026-02-01"]


def test_iter_day_dirs_for_scope_filters_month(tmp_path: Path) -> None:
    root = tmp_path / "source-archive" / "statecraft"
    (root / "2026-05-31").mkdir(parents=True)
    (root / "2026-06-01").mkdir()
    (root / "2026-06-02").mkdir()
    (root / "2026-07-01").mkdir()

    got = idx.iter_day_dirs_for_scope(root, year="2026", month="2026-06")

    assert [p.name for p in got] == ["2026-06-01", "2026-06-02"]
