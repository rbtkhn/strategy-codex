"""Static contract tests for the assistant-facing coffee hub."""

from __future__ import annotations

from pathlib import Path

from scripts.assess_session_load import assess_load, format_annotated_menu


REPO_ROOT = Path(__file__).resolve().parents[1]
COFFEE_SKILL = REPO_ROOT / ".cursor" / "skills" / "coffee" / "SKILL.md"


def test_coffee_completion_requires_hub_menu_after_step_one() -> None:
    text = COFFEE_SKILL.read_text(encoding="utf-8")

    assert "Script output is Step 1 context only" in text
    assert "not complete until" in text
    assert "Coffee Hub Menu - Reply A-D" in text
    assert "Do not end a `coffee` turn with only script output" in text


def test_coffee_hub_canonical_lines_are_a_through_d_only() -> None:
    text = COFFEE_SKILL.read_text(encoding="utf-8")

    assert "A. Steward" in text
    assert "B. Engineer" in text
    assert "C. Strategist" in text
    assert "D. Capitalist" in text
    assert "Conductor is standalone" in text
    assert "E. Conductor" not in text


def test_assess_load_annotations_do_not_reintroduce_hub_e() -> None:
    result = assess_load("strategy-codex")
    assert set(result["option_weights"]) == {"A", "B", "C", "D"}

    menu = format_annotated_menu(result)
    assert "**A. Steward**" in menu
    assert "**B. Engineer**" in menu
    assert "**C. Strategist**" in menu
    assert "**D. Capitalist**" in menu
    assert "**E." not in menu
    assert "Conductor" not in menu
