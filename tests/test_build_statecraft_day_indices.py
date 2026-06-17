from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import build_statecraft_day_indices as idx  # noqa: E402


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def test_build_day_readme_uses_frontmatter_rollups_and_excludes_readme(tmp_path: Path) -> None:
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

    text = idx.build_day_readme(day)

    assert "# Statecraft Archive - 2026-05-26" in text
    assert "- Source files: `2`" in text
    assert "`transcript` (1)" in text and "`youtube` (1)" in text
    assert "`Judging Freedom` (1)" in text and "`Daniel Davis Deep Dive` (1)" in text
    assert "Hosts:" in text and "`Andrew Napolitano` (1)" in text and "`Daniel Davis` (1)" in text
    assert (
        "Guests:" in text
        and "`Daniel Davis` (1)" in text
        and "`Matt Hoh` (1)" in text
        and "`Seyed M. Marandi` (1)" in text
    )
    assert "Threads:" in text and "`davis` (1)" in text and "`hoh` (1)" in text
    assert "## Ingest register" in text
    assert "Not the speaker source bench" in text
    assert "Matt Hoh" in text and "[abc123test](https://www.youtube.com/watch?v=abc123test)" in text
    assert "- `README.md`" not in text
    assert "- `transcript-napolitano-hoh-why-the-pentagon-lies-2026-05-26.md`" in text
    assert "- `youtube-daniel-davis-deep-dive-us-must-stop-the-siege-of-iran-2026-05-26.md`" in text


def test_build_day_readme_uses_family_fallback_for_metadata_thin_files(tmp_path: Path) -> None:
    day = tmp_path / "source-archive" / "statecraft" / "2026-01-12"
    _write(
        day / "transcript-napolitano-johnson-is-the-cia-fueling-irans-chaos-2026-01-12.md",
        (
            "---\n"
            'title: "Larry Johnson: Is the CIA Fueling Iran\'s Chaos?"\n'
            "host: Judge Andrew Napolitano\n"
            "thread: johnson\n"
            "---\n\n"
            "Summary body.\n"
        ),
    )
    _write(
        day / "youtube-alex-mercouris-russia-10-kms-from-zaporozhzhye-city-evacuations-begin-putin-returns-ira-2026-01-12.md",
        "No frontmatter here.\n",
    )

    text = idx.build_day_readme(day)

    assert "## Filename Family Fallbacks" in text
    assert "`transcript-napolitano-*` (1)" in text
    assert "`youtube-alex-mercouris-*` (1)" in text
    assert "Hosts: `Andrew Napolitano` (1)" in text
    assert "Threads: `johnson` (1)" in text


def test_write_day_index_overwrites_existing_readme_deterministically(tmp_path: Path) -> None:
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

    out_path = idx.write_day_index(day)
    first = out_path.read_text(encoding="utf-8")
    second_path = idx.write_day_index(day)
    second = second_path.read_text(encoding="utf-8")

    assert out_path == day / "README.md"
    assert first == second
    assert "placeholder" not in first
    assert "# Statecraft Archive - 2026-03-16" in first


def test_iter_day_dirs_filters_to_requested_year(tmp_path: Path) -> None:
    root = tmp_path / "source-archive" / "statecraft"
    (root / "2026-01-01").mkdir(parents=True)
    (root / "2026-02-01").mkdir()
    (root / "2025-12-31").mkdir()
    (root / "_aired-pending").mkdir()

    got = idx._iter_day_dirs(root, "2026")

    assert [p.name for p in got] == ["2026-01-01", "2026-02-01"]
