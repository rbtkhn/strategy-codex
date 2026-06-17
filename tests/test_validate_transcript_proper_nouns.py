from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from validate_transcript_proper_nouns import (  # noqa: E402
    line_hits,
    transcript_body,
)

BLOCKLIST = (
    REPO_ROOT
    / "public/ph-civ/data/asr-blocklist/volume-ii-pilot.json"
)


def test_transcript_body_splits_on_part_i_marker() -> None:
    text = "---\n---\n\n## Part I: Full transcript\n\nbronch age here\n"
    assert "bronch age" in transcript_body(text)
    assert "---" not in transcript_body(text)


def test_line_hits_finds_known_mangling() -> None:
    payload = json.loads(BLOCKLIST.read_text(encoding="utf-8"))
    body = "we talked about the bronch age and trade.\n"
    path = Path("book/volume-ii/civ-08/civ-08-transcript.md")
    hits = line_hits(path, body, payload["entries"], set())
    assert any(hit.literal == "bronch age" for hit in hits)


def test_allowed_residual_suppresses_hit() -> None:
    payload = json.loads(BLOCKLIST.read_text(encoding="utf-8"))
    body = "normally effing goes well in our forest.\n"
    path = Path("book/volume-ii/civ-03/civ-03-transcript.md")
    allowed = {item["literal"] for item in payload["allowed_residuals"]}
    hits = line_hits(path, body, payload["entries"], allowed)
    assert hits == []


def test_blocklist_has_pilot_scope_metadata() -> None:
    payload = json.loads(BLOCKLIST.read_text(encoding="utf-8"))
    assert payload["scope"] == "volume-ii civ-01..18"
    assert len(payload["entries"]) >= 100
    assert any(entry["literal"] == "hedgemon" for entry in payload["entries"])
