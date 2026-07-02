from __future__ import annotations

from grace_mar.presentations.intents import build_presenton_markdown, get_template_key, list_intents, list_templates

def test_intent_and_template_indexes_cover_required_examples() -> None:
    intents = {row["intent"]: row for row in list_intents()}
    templates = {
        (row["family"], row["subsurface"], row["artifact_class"], row["intent"]): row["template"]
        for row in list_templates()
    }
    assert "briefing" in intents
    assert "lesson" in intents
    assert templates[("civ-emp", "ce-emp", "statecraft_brief", "briefing")] == "ce-emp-statecraft-brief-briefing"
    assert templates[("ph-civ", "ph-civ", "chapter_packet", "lesson")] == "ph-civ-chapter-packet-lesson"
    assert get_template_key("ph-civ", "ph-civ", "lesson", "chapter_packet") == "ph-civ-chapter-packet-lesson"
    assert get_template_key("ph-civ", "ph-civ", "summary") == "ph-civ-summary"

def test_build_presenton_markdown_contains_sources_and_constraints() -> None:
    bundle = {
        "bundle_type": "single_bundle",
        "family": "ph-civ",
        "subsurface": "ph-civ",
        "artifact_class": "chapter_packet",
        "intent": "lesson",
        "title": "Civ-07 lesson",
        "audience": "Public readers",
        "source_items": [
            {
                "id": "civ-07",
                "title": "Civ 07",
                "text": "Source text",
                "citation": "public packet",
            }
        ],
        "presentation_hints": {
            "section_order": ["Opening Thesis", "Reader Orientation"],
            "visual_notes": ["Keep ids visible"],
            "chart_candidates": [],
        },
    }
    out = build_presenton_markdown(bundle)
    assert "# Civ-07 lesson" in out
    assert "Family: ph-civ" in out
    assert "Subsurface: ph-civ" in out
    assert "Artifact class: chapter_packet" in out
    assert "Source material:" in out
    assert "Civ 07 [civ-07]" in out
    assert "Do not invent facts" in out
