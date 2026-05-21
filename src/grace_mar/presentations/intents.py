from __future__ import annotations

from typing import Any

from .contract import INTENT_SUBSURFACE_MAP

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
    "ph-mus": {
        "lesson": [
            "Museum Orientation",
            "Visitor Path",
            "Key Artifacts",
            "What To Notice",
            "Cautions",
        ],
        "summary": [
            "Museum Summary",
            "Visitor Path",
            "Key Artifacts",
            "Cautions",
        ],
        "comparison": [
            "Comparison Frame",
            "Exhibit Side A",
            "Exhibit Side B",
            "What To Notice",
            "Cautions",
        ],
    },
}

TEMPLATE_MAP: dict[tuple[str, str], str] = {
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
    ("ph-mus", "lesson"): "ph-mus-lesson",
    ("ph-mus", "summary"): "ph-mus-summary",
    ("ph-mus", "comparison"): "ph-mus-comparison",
}


def get_template_key(family: str, subsurface: str, intent: str) -> str:
    del family
    return TEMPLATE_MAP[(subsurface, intent)]


def default_sections_for(subsurface: str, intent: str) -> list[str]:
    return list(DEFAULT_SECTIONS[subsurface][intent])


def list_intents() -> list[dict[str, Any]]:
    rows = []
    for name in INTENT_REGISTRY:
        rows.append(
            {
                "intent": name,
                "allowed_targets": [
                    {"family": "ph-civ" if target.startswith("ph-") else "civ-emp", "subsurface": target}
                    for target in INTENT_SUBSURFACE_MAP[name]
                ],
            }
        )
    return rows


def list_templates() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for intent, targets in INTENT_SUBSURFACE_MAP.items():
        for subsurface in targets:
            rows.append(
                {
                    "family": "ph-civ" if subsurface.startswith("ph-") else "civ-emp",
                    "subsurface": subsurface,
                    "intent": intent,
                    "template": get_template_key(
                        "ph-civ" if subsurface.startswith("ph-") else "civ-emp",
                        subsurface,
                        intent,
                    ),
                }
            )
    return rows


def build_presenton_markdown(bundle: dict[str, Any]) -> str:
    intent = bundle["intent"]
    family = bundle["family"]
    subsurface = bundle["subsurface"]
    section_order = bundle["presentation_hints"]["section_order"]
    sections = (
        list(section_order)
        if section_order
        else default_sections_for(subsurface, intent)
    )
    lines = [
        f"# {bundle['title']}",
        "",
        f"Family: {family}",
        f"Subsurface: {subsurface}",
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
