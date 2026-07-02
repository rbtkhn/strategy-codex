"""Tests for the Diesen ledger input helper."""

from __future__ import annotations

import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from update_diesen_ledger import (  # noqa: E402
    canonical_watch_url,
    extract_video_id,
    rebuild_ledger_section,
)

def test_video_id_parsing_normalizes_common_youtube_forms() -> None:
    vid = "abc123DEF45"
    assert extract_video_id(vid) == vid
    assert extract_video_id(f"https://www.youtube.com/watch?v={vid}&t=1s") == vid
    assert extract_video_id(f"https://youtu.be/{vid}") == vid
    assert canonical_watch_url(f"https://youtu.be/{vid}") == f"https://www.youtube.com/watch?v={vid}"

def test_rebuild_ledger_section_canonicalizes_dedupes_and_marks_mirror_status(tmp_path: Path) -> None:
    notebook_root = tmp_path / "strategy-notebook"
    raw_root = notebook_root / "raw-input"
    raw_root.mkdir(parents=True, exist_ok=True)

    mirrored = raw_root / "2026-01-10" / "diesen-new.md"
    mirrored.parent.mkdir(parents=True, exist_ok=True)
    mirrored.write_text(
        "---\nsource_url: \"https://www.youtube.com/watch?v=zyxwvutsrqp\"\n---\n",
        encoding="utf-8",
    )

    profile_text = """# Diesen profile

## Mearsheimer ledger
<!-- diesen-ledger:mearsheimer:start -->

| pub_date | Title | URL | raw-input |
|----------|-------|-----|-----------|
| 2026-01-01 | John Mearsheimer: Existing Row | [https://www.youtube.com/watch?v=abcdefghijk](https://www.youtube.com/watch?v=abcdefghijk) | needs capture |

<!-- diesen-ledger:mearsheimer:end -->

## Sachs ledger
<!-- diesen-ledger:sachs:start -->

| pub_date | Title | URL | raw-input |
|----------|-------|-----|-----------|
| 2026-01-20 | Jeffrey Sachs: Existing Row | [https://www.youtube.com/watch?v=lmnopqrstuv](https://www.youtube.com/watch?v=lmnopqrstuv) | needs capture |

<!-- diesen-ledger:sachs:end -->
"""

    metadata = {
        "lmnopqrstuv": {
            "title": "Jeffrey Sachs: Existing Row",
            "pub_date": "2026-01-20",
            "url": "https://www.youtube.com/watch?v=lmnopqrstuv",
        },
        "zyxwvutsrqp": {
            "title": "Jeffrey Sachs: New Row | With Pipes",
            "pub_date": "2026-01-10",
            "url": "https://www.youtube.com/watch?v=zyxwvutsrqp",
        },
        "abcdefghijk": {
            "title": "John Mearsheimer: Existing Row",
            "pub_date": "2026-01-01",
            "url": "https://www.youtube.com/watch?v=abcdefghijk",
        },
    }

    def fake_fetch(video_id: str) -> dict | None:
        return metadata.get(video_id)

    updated, added = rebuild_ledger_section(
        profile_text=profile_text,
        ledger_key="sachs",
        urls=[
            "https://www.youtube.com/watch?v=zyxwvutsrqp&t=1s",
            "https://www.youtube.com/watch?v=abcdefghijk",
        ],
        notebook_root=notebook_root,
        metadata_fetcher=fake_fetch,
    )

    assert added == ["zyxwvutsrqp"]
    assert updated.count("watch?v=abcdefghijk") == 2
    assert "[https://www.youtube.com/watch?v=zyxwvutsrqp](https://www.youtube.com/watch?v=zyxwvutsrqp)" in updated
    assert r"Jeffrey Sachs: New Row \| With Pipes" in updated
    assert "2026-01-10 | Jeffrey Sachs: New Row \\| With Pipes" in updated
    assert "mirrored" in updated
    assert "needs capture" in updated
    assert "https://www.youtube.com/watch?v=lmnopqrstuv" in updated

def test_rebuild_ledger_section_offline_reflows_existing_rows(tmp_path: Path) -> None:
    notebook_root = tmp_path / "strategy-notebook"
    raw_root = notebook_root / "raw-input"
    raw_root.mkdir(parents=True, exist_ok=True)

    profile_text = """# Diesen profile

## Sachs ledger
<!-- diesen-ledger:sachs:start -->

| pub_date | Title | URL | raw-input |
|----------|-------|-----|-----------|
| 2026-01-20 | Jeffrey Sachs: Existing Row | [https://www.youtube.com/watch?v=lmnopqrstuv](https://www.youtube.com/watch?v=lmnopqrstuv) | needs capture |
| 2026-01-10 | Jeffrey Sachs: New Row | [https://www.youtube.com/watch?v=zyxwvutsrqp](https://www.youtube.com/watch?v=zyxwvutsrqp) | needs capture |

<!-- diesen-ledger:sachs:end -->
"""

    (raw_root / "2026-01-10").mkdir(parents=True, exist_ok=True)

    updated, added = rebuild_ledger_section(
        profile_text=profile_text,
        ledger_key="sachs",
        urls=[],
        notebook_root=notebook_root,
        metadata_fetcher=None,
    )

    assert added == []
    assert "2026-01-10" in updated.splitlines()[7]
    assert "2026-01-20" in updated
