"""Tests for scripts/statecraft_situation_brief_delta.py."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from statecraft_situation_brief_delta import (  # noqa: E402
    build_delta_block,
    grade_from_row,
    parse_fork_grades,
    parse_iso_date,
)

SAMPLE_MATRIX = """
| ID | Claim | Lane | Lang | Verdict | Cite |
| --- | --- | --- | --- | --- | --- |
| **J14-1** | Trump: MoU signed Sunday | America | en | **Contradicted** (for Sunday sign) | cite |
| **J14-2** | Iran FM: not signed Sunday | Persia | en | **Supported** | cite |
| **J14-3** | Trump: Deal complete | America | en | **Supported** | cite |
"""

SAMPLE_MATRIX_DAY2 = """
| ID | Claim | Lane | Lang | Verdict | Cite |
| --- | --- | --- | --- | --- | --- |
| **J14-1** | Trump: MoU signed Sunday | America | en | **Supported** | cite |
| **J14-2** | Iran FM: not signed Sunday | Persia | en | **Contested** | cite |
| **J14-3** | Trump: Deal complete | America | en | **Supported** | cite |
| **J16-K1** | Live strikes Lebanon | Adjacent | en | **Supported** | cite |
"""


def test_parse_iso_date() -> None:
    assert parse_iso_date("2026-06-16").isoformat() == "2026-06-16"


def test_grade_from_row_picks_strongest_verdict() -> None:
    row = ["**J14-15**", "claim", "lane", "en", "**Contradicted / absent**", "cite"]
    assert grade_from_row(row) == "Contradicted"


def test_parse_fork_grades_extracts_j_ids() -> None:
    grades = parse_fork_grades(SAMPLE_MATRIX, "fixture.md")
    assert set(grades) == {"J14-1", "J14-2", "J14-3"}
    assert grades["J14-1"].grade == "Contradicted"
    assert grades["J14-2"].grade == "Supported"


def test_build_delta_block_reports_changes() -> None:
    prior = parse_fork_grades(SAMPLE_MATRIX, "prior.md")
    current = parse_fork_grades(SAMPLE_MATRIX_DAY2, "current.md")
    block = build_delta_block(
        prior_day=parse_iso_date("2026-06-14"),
        current_day=parse_iso_date("2026-06-16"),
        prior_grades=prior,
        current_grades=current,
        prior_source="2026-06-14-wire-verify-matrix.md",
        current_source="2026-06-16-wire-verify-matrix.md",
    )
    assert "## Situation Brief — changes since 2026-06-14" in block
    assert "**J14-1** | Contradicted | Supported | changed" in block
    assert "**J16-K1**" in block
    assert "Governed brief with source receipts" in block


def test_live_repo_matrix_pair() -> None:
    daily_dir = REPO_ROOT / "statecraft" / "daily"
    prior_path = daily_dir / "2026-06-14-wire-verify-matrix.md"
    today_path = daily_dir / "2026-06-16-wire-verify-matrix.md"
    if not prior_path.is_file() or not today_path.is_file():
        return
    prior = parse_fork_grades(prior_path.read_text(encoding="utf-8"), prior_path.name)
    current = parse_fork_grades(today_path.read_text(encoding="utf-8"), today_path.name)
    assert "J14-1" in prior
    assert any(k.startswith("J16-") for k in current)
