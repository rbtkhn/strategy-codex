from __future__ import annotations

from typing import Any

from .contract import ARTIFACT_CLASSES_BY_SUBSURFACE, FAMILY_BY_SUBSURFACE, INTENT_SUBSURFACE_MAP

INTENT_REGISTRY: dict[str, dict[str, Any]] = {
    "briefing": {"n_slides": 10},
    "lesson": {"n_slides": 12},
    "summary": {"n_slides": 8},
    "roadmap": {"n_slides": 9},
    "comparison": {"n_slides": 10},
}

DEFAULT_SECTIONS: dict[str, dict[str, list[str]]] = {
    "ce-civ": {
        "briefing": [
            "Civilization Frame",
            "Institutional Pattern",
            "Evidence",
            "Application",
            "Next Moves",
        ],
        "lesson": [
            "Civilization Frame",
            "Institutional Pattern",
            "Evidence",
            "Application",
            "Study Questions",
        ],
        "summary": ["Summary", "Institutional Pattern", "Evidence", "Application"],
        "comparison": [
            "Comparison Frame",
            "Civilization Side A",
            "Civilization Side B",
            "Institutional Tensions",
            "Synthesis",
        ],
    },
    "ce-emp": {
        "briefing": [
            "Executive Summary",
            "Statecraft Use",
            "Counterweights",
            "Decision Points",
            "Next Moves",
        ],
        "summary": ["Summary", "Statecraft Use", "Counterweights", "Appendix"],
        "roadmap": [
            "Roadmap Thesis",
            "Current Position",
            "Workstreams",
            "Risks and Counterweights",
            "Decision Points",
        ],
        "comparison": [
            "Comparison Frame",
            "Statecraft Side A",
            "Statecraft Side B",
            "Counterweights",
            "Synthesis",
        ],
    },
    "ce-mus": {
        "lesson": [
            "Exhibit Frame",
            "Object Sequence",
            "Interpretation",
            "Operational Relevance",
            "Cautions",
        ],
        "summary": [
            "Exhibit Summary",
            "Object Sequence",
            "Operational Relevance",
            "Cautions",
        ],
        "comparison": [
            "Comparison Frame",
            "Object Sequence A",
            "Object Sequence B",
            "Interpretive Tensions",
            "Synthesis",
        ],
    },
    "ph-civ": {
        "lesson": [
            "Opening Thesis",
            "Reader Orientation",
            "Pattern",
            "Evidence",
            "Study Questions",
        ],
        "summary": ["Summary", "Pattern", "Evidence", "Reader Return Path"],
        "comparison": [
            "Comparison Frame",
            "Pattern Side A",
            "Pattern Side B",
            "Tensions",
            "Synthesis",
        ],
    },
    "ph-apo": {
        "lesson": [
            "Crisis Frame",
            "Pressure System",
            "Evidence",
            "Caveats",
            "Implications",
        ],
        "summary": ["Summary", "Pressure System", "Evidence", "Implications"],
        "comparison": [
            "Comparison Frame",
            "Pressure System A",
            "Pressure System B",
            "Caveats",
            "Synthesis",
        ],
    },
}

DEFAULT_SECTIONS_BY_ARTIFACT_CLASS: dict[str, dict[str, list[str]]] = {
    "chapter_packet": {
        "lesson": ["Opening Thesis", "Reader Orientation", "Pattern", "Evidence", "Study Questions"],
        "summary": ["Summary", "Pattern", "Evidence", "Reader Return Path"],
        "comparison": ["Comparison Frame", "Pattern Side A", "Pattern Side B", "Tensions", "Synthesis"],
    },
    "route_comparison": {
        "summary": ["Comparison Summary", "Route Side A", "Route Side B", "Shared Pattern", "Reader Return Path"],
        "comparison": ["Comparison Frame", "Route Side A", "Route Side B", "Tensions", "Synthesis"],
    },
    "civilization_pattern_packet": {
        "briefing": ["Civilization Frame", "Institutional Pattern", "Evidence", "Application", "Next Moves"],
        "lesson": ["Civilization Frame", "Institutional Pattern", "Evidence", "Application", "Study Questions"],
        "summary": ["Summary", "Institutional Pattern", "Evidence", "Application"],
        "comparison": ["Comparison Frame", "Civilization Side A", "Civilization Side B", "Institutional Tensions", "Synthesis"],
    },
    "statecraft_brief": {
        "briefing": ["Executive Summary", "Statecraft Use", "Counterweights", "Decision Points", "Next Moves"],
        "summary": ["Summary", "Statecraft Use", "Counterweights", "Appendix"],
        "roadmap": ["Roadmap Thesis", "Current Position", "Workstreams", "Risks and Counterweights", "Decision Points"],
    },
    "strategic_exhibit": {
        "lesson": ["Exhibit Frame", "Object Sequence", "Interpretation", "Operational Relevance", "Cautions"],
        "summary": ["Exhibit Summary", "Object Sequence", "Operational Relevance", "Cautions"],
        "comparison": ["Comparison Frame", "Object Sequence A", "Object Sequence B", "Interpretive Tensions", "Synthesis"],
    },
    "decision_comparison": {
        "briefing": ["Executive Summary", "Decision Options", "Counterweights", "Implications", "Next Moves"],
        "comparison": ["Comparison Frame", "Decision Side A", "Decision Side B", "Counterweights", "Synthesis"],
    },
}

TEMPLATE_MAP: dict[tuple[str, str, str], str] = {
    ("ce-civ", "civilization_pattern_packet", "briefing"): "ce-civ-civilization-pattern-packet-briefing",
    ("ce-civ", "civilization_pattern_packet", "lesson"): "ce-civ-civilization-pattern-packet-lesson",
    ("ce-civ", "civilization_pattern_packet", "summary"): "ce-civ-civilization-pattern-packet-summary",
    ("ce-civ", "civilization_pattern_packet", "comparison"): "ce-civ-civilization-pattern-packet-comparison",
    ("ce-emp", "statecraft_brief", "briefing"): "ce-emp-statecraft-brief-briefing",
    ("ce-emp", "statecraft_brief", "summary"): "ce-emp-statecraft-brief-summary",
    ("ce-emp", "statecraft_brief", "roadmap"): "ce-emp-statecraft-brief-roadmap",
    ("ce-emp", "decision_comparison", "briefing"): "ce-emp-decision-comparison-briefing",
    ("ce-emp", "decision_comparison", "comparison"): "ce-emp-decision-comparison-comparison",
    ("ce-mus", "strategic_exhibit", "lesson"): "ce-mus-strategic-exhibit-lesson",
    ("ce-mus", "strategic_exhibit", "summary"): "ce-mus-strategic-exhibit-summary",
    ("ce-mus", "strategic_exhibit", "comparison"): "ce-mus-strategic-exhibit-comparison",
    ("ph-civ", "chapter_packet", "lesson"): "ph-civ-chapter-packet-lesson",
    ("ph-civ", "chapter_packet", "summary"): "ph-civ-chapter-packet-summary",
    ("ph-civ", "chapter_packet", "comparison"): "ph-civ-chapter-packet-comparison",
    ("ph-civ", "route_comparison", "summary"): "ph-civ-route-comparison-summary",
    ("ph-civ", "route_comparison", "comparison"): "ph-civ-route-comparison-comparison",
    ("ph-apo", "chapter_packet", "lesson"): "ph-apo-chapter-packet-lesson",
    ("ph-apo", "chapter_packet", "summary"): "ph-apo-chapter-packet-summary",
    ("ph-apo", "chapter_packet", "comparison"): "ph-apo-chapter-packet-comparison",
    ("ph-apo", "route_comparison", "summary"): "ph-apo-route-comparison-summary",
    ("ph-apo", "route_comparison", "comparison"): "ph-apo-route-comparison-comparison",
}

LEGACY_TEMPLATE_MAP: dict[tuple[str, str], str] = {
    ("ce-civ", "briefing"): "ce-civ-briefing",
    ("ce-civ", "lesson"): "ce-civ-lesson",
    ("ce-civ", "summary"): "ce-civ-summary",
    ("ce-civ", "comparison"): "ce-civ-comparison",
    ("ce-emp", "briefing"): "ce-emp-briefing",
    ("ce-emp", "summary"): "ce-emp-summary",
    ("ce-emp", "roadmap"): "ce-emp-roadmap",
    ("ce-emp", "comparison"): "ce-emp-comparison",
    ("ce-mus", "lesson"): "ce-mus-lesson",
    ("ce-mus", "summary"): "ce-mus-summary",
    ("ce-mus", "comparison"): "ce-mus-comparison",
    ("ph-civ", "lesson"): "ph-civ-lesson",
    ("ph-civ", "summary"): "ph-civ-summary",
    ("ph-civ", "comparison"): "ph-civ-comparison",
    ("ph-apo", "lesson"): "ph-apo-lesson",
    ("ph-apo", "summary"): "ph-apo-summary",
    ("ph-apo", "comparison"): "ph-apo-comparison",
}


def get_template_key(
    family: str,
    subsurface: str,
    intent: str,
    artifact_class: str = "",
) -> str:
    if artifact_class:
        template = TEMPLATE_MAP.get((subsurface, artifact_class, intent))
        if template:
            return template
    if family != FAMILY_BY_SUBSURFACE[subsurface]:
        raise KeyError(f"family {family!r} does not match subsurface {subsurface!r}")
    return LEGACY_TEMPLATE_MAP[(subsurface, intent)]


def default_sections_for(subsurface: str, intent: str, artifact_class: str = "") -> list[str]:
    if artifact_class:
        section_map = DEFAULT_SECTIONS_BY_ARTIFACT_CLASS.get(artifact_class, {})
        if intent in section_map:
            return list(section_map[intent])
    return list(DEFAULT_SECTIONS[subsurface][intent])


def list_intents() -> list[dict[str, Any]]:
    rows = []
    for name in INTENT_REGISTRY:
        rows.append(
            {
                "intent": name,
                "allowed_targets": [
                    {
                        "family": FAMILY_BY_SUBSURFACE[target],
                        "subsurface": target,
                        "artifact_classes": [
                            artifact_class
                            for artifact_class in ARTIFACT_CLASSES_BY_SUBSURFACE[target]
                            if (target, artifact_class, name) in TEMPLATE_MAP
                        ],
                    }
                    for target in INTENT_SUBSURFACE_MAP[name]
                ],
            }
        )
    return rows


def list_templates() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for (subsurface, artifact_class, intent), template in TEMPLATE_MAP.items():
        rows.append(
            {
                "family": FAMILY_BY_SUBSURFACE[subsurface],
                "subsurface": subsurface,
                "artifact_class": artifact_class,
                "intent": intent,
                "template": template,
            }
        )
    return rows


def build_presenton_markdown(bundle: dict[str, Any]) -> str:
    intent = bundle["intent"]
    family = bundle["family"]
    subsurface = bundle["subsurface"]
    artifact_class = str(bundle.get("artifact_class") or "")
    section_order = bundle["presentation_hints"]["section_order"]
    sections = (
        list(section_order)
        if section_order
        else default_sections_for(subsurface, intent, artifact_class)
    )
    lines = [
        f"# {bundle['title']}",
        "",
        f"Family: {family}",
        f"Subsurface: {subsurface}",
        f"Artifact class: {artifact_class or 'legacy'}",
        f"Intent: {intent}",
        f"Audience: {bundle['audience']}",
        "",
        "Use the following sections in order.",
        "",
    ]
    for idx, section in enumerate(sections, start=1):
        lines.append(f"{idx}. {section}")
    lines.extend(["", "Source material:", ""])
    for item in bundle["source_items"]:
        lines.extend(
            [
                f"## {item['title']} [{item['id']}]",
                f"Citation: {item['citation']}",
                item["text"],
                "",
            ]
        )
    if bundle["presentation_hints"]["visual_notes"]:
        lines.append("Visual notes:")
        for note in bundle["presentation_hints"]["visual_notes"]:
            lines.append(f"- {note}")
        lines.append("")
    if bundle["presentation_hints"]["chart_candidates"]:
        lines.append("Chart candidates:")
        for note in bundle["presentation_hints"]["chart_candidates"]:
            lines.append(f"- {note}")
        lines.append("")
    lines.extend(
        [
            "Constraints:",
            "- Keep source traceability visible through citations or source ids.",
            "- Do not invent facts outside the source material.",
            "- Favor concise slide text with clear structure.",
        ]
    )
    return "\n".join(lines).strip() + "\n"
