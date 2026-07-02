"""Tests for check_capture_map_epistemic advisory WARNs."""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import check_capture_map_epistemic as checker  # noqa: E402

def test_collect_warnings_high_entropy() -> None:
    objects = [
        {
            "voice": "freeman",
            "timestamp": "2025-01-14",
            "capture": "source-archive/statecraft/2025-01-14/source-example.md",
            "capture_map_event_id": "us_israel_iran_war_preparation_2025",
            "alignment_entropy": 1.41,
            "regime": {"label": "fragmentation"},
            "primary_event_id": "us_israel_iran_war_preparation_2025",
            "stance": "yes",
            "quote_speaker": "host",
            "public_display": True,
        }
    ]
    warnings = checker.collect_warnings(objects, row_index={})
    assert any("high binding ambiguity" in w for w in warnings)
    assert any("fragmentation regime" in w for w in warnings)
    assert any("excerpt/speaker may not support stance" in w for w in warnings)
    assert any("source-example.md" in w for w in warnings)

def test_collect_warnings_clean_row() -> None:
    objects = [
        {
            "voice": "freeman",
            "timestamp": "2025-02-01",
            "capture": "source-archive/statecraft/2025-02-01/source-clean.md",
            "capture_map_event_id": "evt_a",
            "alignment_entropy": 0.2,
            "regime": {"label": "stabilization"},
            "primary_event_id": "evt_a",
            "stance": "yes",
            "quote_speaker": "freeman",
            "public_display": True,
        }
    ]
    warnings = checker.collect_warnings(objects, row_index={})
    assert warnings == []
