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

    assert "A. Confirm" in text
    assert "B. Test" in text
    assert "C. Deepen" in text
    assert "D. Reframe" in text
    assert "Conductor is compressed" in text or "CONDUCTOR-COMPRESSION-SPEC" in text
    assert "E. Conductor" not in text

def test_assess_load_annotations_do_not_reintroduce_hub_e() -> None:
    result = assess_load("strategy-codex")
    assert set(result["option_weights"]) == {"A", "B", "C", "D"}

    menu = format_annotated_menu(result)
    assert "**A. Confirm**" in menu
    assert "**B. Test**" in menu
    assert "**C. Deepen**" in menu
    assert "**D. Reframe**" in menu
    assert "**E." not in menu
    assert "Conductor" not in menu

def test_assess_load_includes_default_attention() -> None:
    result = assess_load("strategy-codex")
    assert result.get("default_attention_by_letter") == {
        "A": None,
        "B": "precision pass",
        "C": "hold tension",
        "D": "one object only",
    }
    menu = format_annotated_menu(result)
    rec = result.get("recommended")
    if rec == "D":
        assert "one object only" in menu
    elif rec == "B":
        assert "precision pass" in menu
