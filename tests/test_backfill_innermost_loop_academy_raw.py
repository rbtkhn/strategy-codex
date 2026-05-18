from __future__ import annotations

from datetime import date

import backfill_innermost_loop_academy_raw as raw


def test_title_or_slug_date_wins_over_published_date() -> None:
    assert raw._date_from_title_or_slug(
        "Welcome to May 15, 2026",
        "",
        date(2026, 5, 16),
    ) == date(2026, 5, 15)
    assert raw._date_from_title_or_slug(
        "Untitled",
        "welcome-to-may-14-2026",
        date(2026, 5, 15),
    ) == date(2026, 5, 14)


def test_run_writes_full_local_captures_and_indexes_them(tmp_path, monkeypatch) -> None:
    raw_root = tmp_path / "codex/academy/singularity/workshop/raw-input/innermost-loop"
    workshop_readme = tmp_path / "codex/academy/singularity/workshop/README.md"
    shelf_readme = tmp_path / "codex/academy/singularity/README.md"
    workshop_readme.parent.mkdir(parents=True, exist_ok=True)
    shelf_readme.parent.mkdir(parents=True, exist_ok=True)
    workshop_readme.write_text(
        "# Singularity Workshop\n\n## First Instruments To Build\n\n- One\n",
        encoding="utf-8",
    )
    shelf_readme.write_text("# Singularity\n\nWORK only; not Record.\n", encoding="utf-8")

    def fake_fetch_json(url: str, *, timeout: int = 60) -> object:
        if "/api/v1/archive" in url and "offset=0" in url:
            return [
                {
                    "slug": "welcome-to-may-17-2026",
                    "post_date": "2026-05-17T10:00:00Z",
                },
                {
                    "slug": "welcome-to-may-15-2026",
                    "post_date": "2026-05-16T01:00:00Z",
                },
            ]
        if "/api/v1/archive" in url:
            return []
        slug = url.rsplit("/", 1)[-1]
        day = "17" if slug.endswith("17-2026") else "15"
        published = "2026-05-17T10:00:00Z" if day == "17" else "2026-05-16T01:00:00Z"
        return {
            "id": int(day),
            "slug": slug,
            "title": f"Welcome to May {day}, 2026",
            "subtitle": f"Teaser for May {day}",
            "canonical_url": f"https://theinnermostloop.substack.com/p/{slug}",
            "post_date": published,
            "body_html": (
                "<p>First full paragraph with a distinctive raw-capture phrase.</p>"
                "<p>Second paragraph should also be preserved.</p>"
            ),
        }

    monkeypatch.setattr(raw, "_fetch_json", fake_fetch_json)

    assert (
        raw.run(
            host="theinnermostloop.substack.com",
            raw_root=raw_root,
            workshop_readme=workshop_readme,
            shelf_readme=shelf_readme,
            today=date(2026, 5, 18),
            days=14,
            apply=True,
            overwrite=False,
            page_size=30,
        )
        == 0
    )

    may15 = raw_root / "innermost-loop-2026-05-15.md"
    may17 = raw_root / "innermost-loop-2026-05-17.md"
    assert may15.exists()
    assert may17.exists()
    text = may15.read_text(encoding="utf-8")
    assert "title_date: 2026-05-15" in text
    assert "published_date: 2026-05-16" in text
    assert "distinctive raw-capture phrase" in text
    assert "Second paragraph should also be preserved." in text

    workshop = workshop_readme.read_text(encoding="utf-8")
    assert "## Raw Captures" in workshop
    assert "raw-input/innermost-loop/innermost-loop-2026-05-15.md" in workshop
    assert "## First Instruments To Build" in workshop
    shelf = shelf_readme.read_text(encoding="utf-8")
    assert "## Raw Capture Backfill" in shelf
    assert "workshop/raw-input/innermost-loop/innermost-loop-2026-05-17.md" in shelf


def test_existing_capture_is_not_overwritten_without_flag(tmp_path, monkeypatch) -> None:
    raw_root = tmp_path / "raw"
    raw_root.mkdir()
    dest = raw_root / "innermost-loop-2026-05-17.md"
    dest.write_text("manual capture", encoding="utf-8")
    workshop_readme = tmp_path / "workshop.md"
    shelf_readme = tmp_path / "shelf.md"
    workshop_readme.write_text("# Workshop\n", encoding="utf-8")
    shelf_readme.write_text("# Shelf\n", encoding="utf-8")

    def fake_fetch_json(url: str, *, timeout: int = 60) -> object:
        if "/api/v1/archive" in url and "offset=0" in url:
            return [{"slug": "welcome-to-may-17-2026", "post_date": "2026-05-17T10:00:00Z"}]
        if "/api/v1/archive" in url:
            return []
        return {
            "slug": "welcome-to-may-17-2026",
            "title": "Welcome to May 17, 2026",
            "canonical_url": "https://theinnermostloop.substack.com/p/welcome-to-may-17-2026",
            "post_date": "2026-05-17T10:00:00Z",
            "body_html": "<p>new capture</p>",
        }

    monkeypatch.setattr(raw, "_fetch_json", fake_fetch_json)

    raw.run(
        host="theinnermostloop.substack.com",
        raw_root=raw_root,
        workshop_readme=workshop_readme,
        shelf_readme=shelf_readme,
        today=date(2026, 5, 18),
        days=14,
        apply=True,
        overwrite=False,
        page_size=30,
    )

    assert dest.read_text(encoding="utf-8") == "manual capture"
