#!/usr/bin/env python3
"""One-off: strip ph-mus from public/predictive-history mirror (strategy-codex only)."""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MIRROR = REPO_ROOT / "public" / "ph-civ"

DELETE_PATHS = [
    MIRROR / "ph-mus",
    MIRROR / "data" / "museum",
    MIRROR / "schemas" / "museum-exhibit.schema.json",
    MIRROR / "schemas" / "museum-artifact.schema.json",
    MIRROR / "docs" / "media-inventory-guide.md",
    MIRROR / "docs" / "media-curator-bounty.md",
    MIRROR / "schemas" / "media-inventory-item.schema.json",
    MIRROR / "examples" / "media-inventory-row.json",
]

MUSEUM_HOOKS_RE = re.compile(
    r"\n### Museum Hooks\n.*?(?=\n### |\n---|\Z)",
    re.DOTALL,
)

CHECKLIST_RE = re.compile(
    r"routes, patterns, or museum rooms",
    re.IGNORECASE,
)


def strip_choreography(path: Path) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    for route in data.get("routes", []):
        route.pop("museum_status", None)
        route.pop("museum_exhibit_path", None)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def strip_surfaces(path: Path) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    data.pop("museum", None)
    data.get("surfaces", {}).pop("ph-mus", None)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def strip_llm_experience(path: Path) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    data.get("public_surfaces", {}).pop("museum", None)
    template = data.get("first_response_contract", {}).get("template", [])
    if template:
        template[1] = (
            "ph-civ is the two-volume public Predictive History artifact: "
            "Volume I discovers the laws of history; Volume II applies them."
        )
        template[3] = (
            "Choose one: continue the first tour; study civ-07; or switch modes."
        )
    data["modes"] = [m for m in data.get("modes", []) if m.get("mode") != "museum_room"]
    for mode in data.get("modes", []):
        if mode.get("mode") == "first_tour":
            mode["instruction"] = (
                "Orient the reader to the two volumes and the 10-route seed before opening individual chapters."
            )
    guardrails = data.get("guardrails", [])
    data["guardrails"] = [g for g in guardrails if "ph-mus" not in g.lower()]
    data["do_not_claim"] = [
        d for d in data.get("do_not_claim", []) if "ph-mus" not in d.lower() and "museum artifact" not in d.lower()
    ]
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def strip_first_tour(path: Path) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    for stop in data.get("stops", []):
        action = stop.get("next_action", "")
        if "museum room" in action.lower():
            stop["next_action"] = action.replace("future museum room", "commentary canvas").replace(
                " and future museum room", ""
            )
            if "museum" in stop["next_action"].lower():
                stop["next_action"] = "Study through its card, transcript, and commentary canvas."
    data["closing_choices"] = [
        c for c in data.get("closing_choices", []) if "ph-mus" not in c.lower() and "museum" not in c.lower()
    ]
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def strip_growth_goals(path: Path) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    policy = data.get("agent_goal_policy", {})
    policy["required_completion_basis"] = [
        x for x in policy.get("required_completion_basis", []) if "museum" not in x.lower()
    ]
    for campaign in data.get("campaigns", []):
        wedge = campaign.get("first_live_wedge", {})
        wedge["scope"] = [s for s in wedge.get("scope", []) if "museum" not in s.lower()]
        campaign["measurable_agent_outputs"] = [
            o.replace(" and eventual ph-mus exhibit path", "")
            for o in campaign.get("measurable_agent_outputs", [])
            if "ph-mus" not in o.lower()
        ]
        campaign["measurable_agent_outputs"] = [
            o.replace("visual/museum assets", "visual assets")
            for o in campaign["measurable_agent_outputs"]
        ]
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def strip_markdown_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    text = MUSEUM_HOOKS_RE.sub("\n", text)
    text = CHECKLIST_RE.sub("routes or patterns", text)
    text = re.sub(r", or museum rooms", "", text, flags=re.IGNORECASE)
    text = re.sub(r"museum rooms after review", "patterns after review", text, flags=re.IGNORECASE)
    text = re.sub(r"Potential exhibit hooks.*?\n", "", text)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def strip_site_chapter_json(path: Path) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    changed = False
    for key in list(data.keys()):
        if "museum" in key.lower():
            del data[key]
            changed = True
    if changed:
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def replace_in_tree(glob: str, replacements: list[tuple[str, str]]) -> int:
    count = 0
    for path in MIRROR.glob(glob):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        original = text
        for old, new in replacements:
            text = text.replace(old, new)
        if text != original:
            path.write_text(text, encoding="utf-8")
            count += 1
    return count


def main() -> int:
    for rel in DELETE_PATHS:
        if rel.is_dir():
            shutil.rmtree(rel, ignore_errors=True)
        elif rel.exists():
            rel.unlink()

    archive = MIRROR / "docs" / "archive"
    archive.mkdir(parents=True, exist_ok=True)
    (archive / "ph-mus-retired.md").write_text(
        "# ph-mus retired\n\n"
        "The Predictive History Museum (`ph-mus`) layer was removed from the public ph-civ vision.\n\n"
        "Use **chapter study mode** instead: open a chapter folder's `README.md`, transcript, "
        "commentary canvas, and public card.\n\n"
        "See `START-HERE.md` and `docs/first-tour.md` for the two-volume reader flow.\n",
        encoding="utf-8",
    )

    strip_choreography(MIRROR / "data" / "routes" / "choreography.json")
    strip_surfaces(MIRROR / "data" / "surfaces.json")
    strip_llm_experience(MIRROR / "data" / "llm-experience.json")
    strip_first_tour(MIRROR / "data" / "routes" / "first-tour.json")
    strip_growth_goals(MIRROR / "data" / "growth-goals.json")

    md_count = 0
    for path in MIRROR.rglob("*.md"):
        if strip_markdown_file(path):
            md_count += 1

    json_count = 0
    for path in (MIRROR / "site" / "_data" / "chapters").glob("*.json"):
        strip_site_chapter_json(path)
        json_count += 1

    print(f"Deleted {len(DELETE_PATHS)} museum paths")
    print(f"Stripped {md_count} markdown files")
    print(f"Processed {json_count} site chapter JSON files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
