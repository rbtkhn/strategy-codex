"""Offline tests for scripts/backfill_shortform_bundle_raw_input.py."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from scripts.backfill_shortform_bundle_raw_input import _build_doc, run

def test_build_doc_uses_shortform_bundle_kind() -> None:
    doc = _build_doc(
        ingest_date=date(2026, 5, 7),
        pub_date=date(2026, 5, 7),
        source_platform="x",
        account_author="@example",
        source_url_profile="https://x.com/example",
        source_url=None,
        thread="example",
        title="Example short-form bundle",
        body_text="Post one\n\nPost two",
        screenshot_refs=["shot-1.png", "shot-2.png"],
    )
    assert "kind: shortform-bundle" in doc
    assert "source_platform: x" in doc
    assert "account_author: @example" in doc
    assert "screenshot_count: 2" in doc
    assert "## Screenshot provenance" in doc
    assert "shot-1.png" in doc
    assert "Post one" in doc

def test_run_writes_daily_shortform_bundle(tmp_path: Path) -> None:
    body = tmp_path / "ocr.md"
    body.write_text("First post\n\nSecond post", encoding="utf-8")

    dest = run(
        raw_root=tmp_path / "raw-input",
        ingest_date=date(2026, 5, 7),
        pub_date=date(2026, 5, 7),
        source_platform="threads",
        account_author="@example",
        source_url_profile="https://threads.net/@example",
        source_url=None,
        thread="example",
        title=None,
        body_file=body,
        screenshot_refs=["a.png", "b.png"],
        output=None,
        apply=True,
    )
    assert dest.name.startswith("shortform-bundle-threads-example-2026-05-07")
    text = dest.read_text(encoding="utf-8")
    assert "kind: shortform-bundle" in text
    assert "source_platform: threads" in text
    assert "account_author: @example" in text
    assert "First post" in text
    assert "Second post" in text
    assert "a.png" in text and "b.png" in text
