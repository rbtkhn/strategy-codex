"""Tests for scripts/validate_statecraft_daily_synthesis.py."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from validate_statecraft_daily_synthesis import (
    FIVE_VOLUME_ORDER,
    validate_daily_file,
    validate_monthly_file,
    validate_quote_anchor_line,
)

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_quote_anchor_line_rejects_short_quote() -> None:
    err = validate_quote_anchor_line('Quote anchor: "too short to clear this floor."')
    assert err is not None
    assert "requires at least 12" in err


def test_quote_anchor_line_accepts_long_quote() -> None:
    err = validate_quote_anchor_line(
        'Quote anchor: "we have to see the Americans actually implement its side of the bargain."'
    )
    assert err is None


def test_validate_daily_file_rejects_wrong_five_volume_order(tmp_path: Path) -> None:
    path = tmp_path / "2026-06-01.md"
    path.write_text(
        """## Source Base

## Executive Read

## Dominant Themes

## Lane Read

## Five-Volume CIV-STATE Read

- `Persia`: x
- `China`: x
- `Rome`: x
- `Russia`: x
- `America`: x

## Speaker Value From This Batch

- `demo`: Quote anchor: "this quote has enough words to satisfy the floor cleanly today."

## Tensions And Falsifiers

- demo

## Best Next Moves

1. demo
""",
        encoding="utf-8",
    )
    errors = validate_daily_file(path)
    assert any("Five-Volume CIV-STATE Read labels mismatch" in e for e in errors)


def test_validate_monthly_file_rejects_invalid_function_label(tmp_path: Path) -> None:
    path = tmp_path / "2026-06.md"
    path.write_text(
        """## Source Base

## Executive Read

## Functional Convergence

- `trap`: valid
- `myth`: invalid

## Month Arcs

## Lane Ownership Across The Month

## Five-Volume CIV-STATE Read

"""
        + "\n".join(f"- `{label}`: x" for label in FIVE_VOLUME_ORDER)
        + """

## Best Re-entry Days

## What The Month Clarified

## What The Month Still Did Not Settle

## Best Next Companion Notes
""",
        encoding="utf-8",
    )
    errors = validate_monthly_file(path)
    assert any("invalid labels" in e for e in errors)


def test_repo_validator_smoke() -> None:
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "validate_statecraft_daily_synthesis.py")],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout

