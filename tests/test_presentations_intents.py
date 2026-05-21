from __future__ import annotations

from grace_mar.presentations.intents import build_presenton_markdown, get_template_key, list_intents, list_templates


def test_intent_and_template_indexes_cover_required_examples() -> None:
    intents = {row["intent"]: row for row in list_intents()}
    templates = {
        (row["family"], row["subsurface"], row["intent"]): row["template"]
        for row in list_templates()
    }
    assert "briefing" in intents
    assert "lesson" in intents
    assert templates[("civ-emp", "ce-emp", "briefing")] == "ce-emp-briefing"
    assert templates[("ph-civ", "ph-mus", "lesson")] == "ph-mus-lesson"
    assert get_template_key("ph-civ", "ph-civ", "summary") == "ph-civ-summary"


def test_build_presenton_markdown_contains_sources_and_constraints() -> None:
    bundle = {
        "family": "ph-civ",
        "subsurface": "ph-mus",
        "intent": "lesson",
        "title": "GT-16 museum lesson",
        "audience": "Public readers",
        "source_items": [
            {
                "id": "gt-16",
                "title": "GT 16",
                "text": "Source text",
                "citation": "public packet",
            }
        ],
        "presentation_hints": {
            "section_order": ["Museum Orientation", "Visitor Path"],
            "visual_notes": ["Keep ids visible"],
            "chart_candidates": [],
        },
    }
    out = build_presenton_markdown(bundle)
    assert "# GT-16 museum lesson" in out
    assert "Family: ph-civ" in out
    assert "Subsurface: ph-mus" in out
    assert "Source material:" in out
    assert "GT 16 [gt-16]" in out
    assert "Do not invent facts" in out
