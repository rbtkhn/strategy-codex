from __future__ import annotations

from datetime import date
import sys

import backfill_substack_raw_input as substack
import backfill_crooke_substack_raw_input as crooke
import backfill_pape_substack_raw_input as pape
import backfill_ritter_site_raw_input as ritter_site
import backfill_ritter_substack_raw_input as ritter

def test_slug_from_substack_url() -> None:
    assert (
        substack._slug_from_url("https://example.substack.com/p/the-post-title")
        == "the-post-title"
    )

def test_run_targets_urls_without_archive_scan(tmp_path, monkeypatch) -> None:
    calls: list[str] = []

    def fake_fetch_json(url: str, *, timeout: int = 60) -> object:
        calls.append(url)
        assert "/api/v1/archive" not in url
        return {
            "post_date": "2026-04-17T12:00:00Z",
            "title": "A Real-Time Test",
            "canonical_url": "https://escalationtrap.substack.com/p/a-real-time-test",
            "slug": "a-real-time-test",
            "id": 123,
            "subtitle": "A teaser",
            "body_html": "<p>Body text.</p>",
        }

    monkeypatch.setattr(substack, "_fetch_json", fake_fetch_json)

    assert (
        substack.run(
            hostname="escalationtrap.substack.com",
            year=2026,
            raw_root=tmp_path,
            ingest_date=date(2026, 5, 10),
            thread="pape",
            apply=True,
            limit=50,
            urls=["https://escalationtrap.substack.com/p/a-real-time-test"],
            publication_slug="pape",
        )
        == 0
    )

    written = tmp_path / "2026-04-17" / "substack-pape-a-real-time-test-2026-04-17.md"
    assert written.exists()
    text = written.read_text(encoding="utf-8")
    assert "source_url: https://escalationtrap.substack.com/p/a-real-time-test" in text
    assert "thread: pape" in text
    assert calls == ["https://escalationtrap.substack.com/api/v1/posts/a-real-time-test"]

def test_pape_wrapper_refuses_broad_archive_scan_by_default(monkeypatch, capsys) -> None:
    monkeypatch.setattr(sys, "argv", ["backfill_pape_substack_raw_input.py"])

    assert pape.main() == 2
    err = capsys.readouterr().err
    assert "Refusing broad Pape archive scan by default" in err
    assert "not raw-input backlog" in err

def test_ritter_wrappers_refuse_broad_archive_scan_by_default(monkeypatch, capsys) -> None:
    monkeypatch.setattr(sys, "argv", ["backfill_ritter_substack_raw_input.py"])
    assert ritter.main() == 2
    assert "Refusing broad Ritter archive scan by default" in capsys.readouterr().err

    monkeypatch.setattr(sys, "argv", ["backfill_ritter_site_raw_input.py"])
    assert ritter_site.main() == 2
    assert "Refusing broad Ritter archive scan by default" in capsys.readouterr().err

def test_crooke_wrapper_refuses_broad_archive_scan_by_default(monkeypatch, capsys) -> None:
    monkeypatch.setattr(sys, "argv", ["backfill_crooke_substack_raw_input.py"])

    assert crooke.main() == 2
    err = capsys.readouterr().err
    assert "Refusing broad Crooke archive scan by default" in err
    assert "not raw-input backlog" in err
