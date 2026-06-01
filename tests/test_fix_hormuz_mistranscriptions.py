from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import fix_hormuz_mistranscriptions as fix  # noqa: E402


def test_apply_replacements_fixes_first_wave_family() -> None:
    text = (
        "They discussed the straight of hormones.\n"
        "Others pointed to the straight of humus.\n"
        "Others talked about the trade of hormones.\n"
        "And the trade of humus mattered too.\n"
        "Managed passage through the street of Ormuz continued.\n"
        "And the straight of\n"
        "Hormos was reopened.\n"
        "The straits of Homus stayed contested.\n"
    )

    updated, counts = fix.apply_replacements(text)

    assert "straight of hormones" not in updated
    assert "straight of humus" not in updated
    assert "trade of hormones" not in updated
    assert "trade of humus" not in updated
    assert "street of Ormuz" not in updated
    assert "straight of\nHormos" not in updated
    assert "straits of Homus" not in updated
    assert "Strait of Hormuz" in updated
    assert "Straits of Hormuz" in updated
    assert counts["straight_of_hormones"] == 1
    assert counts["straight_of_humus"] == 1
    assert counts["trade_of_hormones"] == 1
    assert counts["trade_of_humus"] == 1
    assert counts["street_of_ormuz"] == 1
    assert counts["straight_of_hormos"] + counts["split_straight_of_hormos"] == 1
    assert counts["straits_of_homus"] == 1


def test_fix_paths_only_touches_high_confidence_files(tmp_path: Path) -> None:
    transcript = tmp_path / "source-archive" / "statecraft" / "2026-02-17" / "transcript-example.md"
    transcript.parent.mkdir(parents=True)
    transcript.write_text("the straight of hormones stayed closed\n", encoding="utf-8")
    audit_json = tmp_path / "audit.json"
    audit_json.write_text(
        json.dumps(
            {
                "findings": [
                    {
                        "path": str(transcript.relative_to(tmp_path)).replace("\\", "/"),
                        "tier": "high_confidence",
                        "match_text": "straight of hormones",
                    },
                    {
                        "path": str(transcript.relative_to(tmp_path)).replace("\\", "/"),
                        "tier": "context_only",
                        "match_text": "",
                    },
                ]
            }
        ),
        encoding="utf-8",
    )

    original_root = fix.REPO_ROOT
    fix.REPO_ROOT = tmp_path
    try:
        paths = fix.load_target_paths(audit_json)
        result = fix.fix_paths(paths, write=True)
    finally:
        fix.REPO_ROOT = original_root

    assert result["changed_files"] == 1
    assert transcript.read_text(encoding="utf-8") == "the Strait of Hormuz stayed closed\n"


def test_apply_replacements_fixes_second_wave_family() -> None:
    text = (
        "The state of armus is contested.\n"
        "Managed passage through the street of armors continued.\n"
        "Another guest said the straight of armus and the strait of armus.\n"
        "Reports mentioned the straight of Armoose.\n"
        "Others warned about the straight of foremost, the trade of foremost, and the trade of formos.\n"
        "A policy note mentioned the state of formos.\n"
        "One transcript even said the straight of Barmuz.\n"
        "Plural references to the straits of Armoose also showed up.\n"
    )

    updated, counts = fix.apply_replacements(text)

    assert "state of armus" not in updated
    assert "street of armors" not in updated
    assert "straight of armus" not in updated
    assert "strait of armus" not in updated
    assert "straight of Armoose" not in updated
    assert "straight of foremost" not in updated
    assert "trade of foremost" not in updated
    assert "trade of formos" not in updated
    assert "state of formos" not in updated
    assert "straight of Barmuz" not in updated
    assert "straits of Armoose" not in updated
    assert updated.count("Strait of Hormuz") == 10
    assert updated.count("Straits of Hormuz") == 1
    assert counts["state_of_armus"] == 1
    assert counts["street_of_armors"] == 1
    assert counts["straight_of_armus"] == 1
    assert counts["strait_of_armus"] == 1
    assert counts["straight_of_armoose"] == 1
    assert counts["straight_of_foremost"] == 1
    assert counts["trade_of_foremost"] == 1
    assert counts["trade_of_formos"] == 1
    assert counts["state_of_formos"] == 1
    assert counts["straight_of_barmuz"] == 1
    assert counts["straits_of_armoose"] == 1


def test_apply_replacements_fixes_hermuz_and_hormuse_family() -> None:
    text = (
        "The Straits of Hermuz remain blocked.\n"
        "Another report said the straits of Hormuse were closed.\n"
        "One guest warned the straight of Hormuse could break the market.\n"
        "Another said the straight of Hermuz and the straight of Hermus were decisive.\n"
        "Shipping also mentioned the trade of Hermuz and the street of Hermuz.\n"
        "A malformed line referred to the street Hermuz and the strait of Hermuz.\n"
    )

    updated, counts = fix.apply_replacements(text)

    assert "Straits of Hermuz" not in updated
    assert "straits of Hormuse" not in updated
    assert "straight of Hormuse" not in updated
    assert "straight of Hermuz" not in updated
    assert "straight of Hermus" not in updated
    assert "trade of Hermuz" not in updated
    assert "street of Hermuz" not in updated
    assert "street Hermuz" not in updated
    assert "strait of Hermuz" not in updated
    assert updated.count("Straits of Hormuz") == 2
    assert updated.count("Strait of Hormuz") == 7
    assert counts["straits_of_hermuz"] == 1
    assert counts["straits_of_hormuse"] == 1
    assert counts["straight_of_hormuse"] == 1
    assert counts["straight_of_hermuz"] == 1
    assert counts["straight_of_hermus"] == 1
    assert counts["trade_of_hermuz"] == 1
    assert counts["street_of_hermuz"] == 1
    assert counts["street_hermuz"] == 1
    assert counts["strait_of_hermuz"] == 1
