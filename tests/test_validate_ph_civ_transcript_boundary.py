from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from validate_ph_civ_transcript_boundary import (  # noqa: E402
    classify_paths,
    format_violation_message,
    is_protected_transcript_path,
)


def test_blocks_mirror_prefixed_transcript_paths() -> None:
    blocked, allowed = classify_paths(
        [
            "public/ph-civ/book/volume-ii/civ-07/civ-07-transcript.md",
            "public/ph-civ/book/volume-ii/civ-07/civ-07-commentary.md",
        ]
    )

    assert blocked == [
        "public/ph-civ/book/volume-ii/civ-07/civ-07-transcript.md"
    ]
    assert allowed == [
        "public/ph-civ/book/volume-ii/civ-07/civ-07-commentary.md"
    ]


def test_blocks_submodule_relative_transcript_paths() -> None:
    blocked, allowed = classify_paths(
        [
            "book/volume-v/gb-03/gb-03-transcript.md",
            "data/cards/gb-03.md",
        ]
    )

    assert blocked == ["book/volume-v/gb-03/gb-03-transcript.md"]
    assert allowed == ["data/cards/gb-03.md"]


def test_normalizes_windows_paths() -> None:
    assert is_protected_transcript_path(
        r"public\ph-civ\book\volume-ii\civ-10\civ-10-transcript.md"
    )


def test_allows_boundary_maintenance_paths() -> None:
    blocked, allowed = classify_paths(
        [
            "scripts/validate_ph_civ_transcript_boundary.py",
            ".cursor/rules/ph-civ-transcript-immutability.mdc",
        ]
    )

    assert blocked == []
    assert len(allowed) == 2


def test_violation_message_documents_escape_hatch() -> None:
    message = format_violation_message(
        ["public/ph-civ/book/volume-ii/civ-09/civ-09-transcript.md"]
    )

    assert "PH-CIV transcript boundary violation" in message
    assert "PH_CIV_TRANSCRIPT_EDIT=1" in message
    assert "PH-TRANSCRIPT-EDIT:" in message
    assert "civ-09-transcript.md" in message
