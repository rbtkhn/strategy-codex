"""Tests for scripts/backfill_x_shortform_bundle_raw_input.py."""

from __future__ import annotations

from pathlib import Path

import scripts.backfill_x_shortform_bundle_raw_input as module


def test_default_profile_url_strips_at_prefix() -> None:
    assert module._default_profile_url("@Example") == "https://x.com/Example"


def test_main_pins_x_platform(monkeypatch, tmp_path: Path) -> None:
    body = tmp_path / "ocr.md"
    body.write_text("One\n\nTwo", encoding="utf-8")

    captured: dict[str, object] = {}

    def fake_run(**kwargs):
        captured.update(kwargs)
        return tmp_path / "out.md"

    monkeypatch.setattr(module, "run", fake_run)
    monkeypatch.setattr(
        "sys.argv",
        [
            "backfill_x_shortform_bundle_raw_input.py",
            "--account",
            "@example",
            "--pub-date",
            "2026-05-07",
            "--body-file",
            str(body),
        ],
    )

    assert module.main() == 0
    assert captured["source_platform"] == "x"
    assert captured["account_author"] == "@example"
    assert captured["source_url_profile"] == "https://x.com/example"
    assert captured["pub_date"].isoformat() == "2026-05-07"

