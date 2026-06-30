from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from validate_predictive_history_boundary import classify_paths, format_violation_message


def test_allows_boundary_maintenance_paths() -> None:
    blocked, allowed = classify_paths(
        [
            "continuity/predictive-history/README.md",
            "research/external/youtube-channels/predictive-history/README.md",
        ]
    )

    assert blocked == []
    assert allowed == [
        "continuity/predictive-history/README.md",
        "research/external/youtube-channels/predictive-history/README.md",
    ]


def test_blocks_frozen_predictive_history_content_paths() -> None:
    blocked, allowed = classify_paths(
        [
            "continuity/predictive-history/lectures/game-theory-21-world-war-trump.md",
            "research/external/youtube-channels/predictive-history/index.json",
        ]
    )

    assert blocked == [
        "continuity/predictive-history/lectures/game-theory-21-world-war-trump.md",
        "research/external/youtube-channels/predictive-history/index.json",
    ]
    assert allowed == []


def test_normalizes_windows_paths() -> None:
    blocked, allowed = classify_paths(
        [r".\codex\predictive-history\BOOK-ARCHITECTURE.md"]
    )

    assert blocked == ["continuity/predictive-history/BOOK-ARCHITECTURE.md"]
    assert allowed == []


def test_violation_message_points_to_external_repo() -> None:
    message = format_violation_message(
        ["continuity/predictive-history/STATUS.md"],
        ["continuity/predictive-history/README.md"],
    )

    assert "canonical public Predictive History repo" in message
    assert "public ph-civ source_id, pattern_id, and route references" in message
    assert "Move canonical public Predictive History edits to `rbtkhn/predictive-history` instead." in message
    assert "continuity/predictive-history/STATUS.md" in message
