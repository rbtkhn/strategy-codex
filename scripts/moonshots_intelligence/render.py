"""Render intelligence JSON to markdown using template shape."""

from __future__ import annotations

from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_PATH = (
    REPO_ROOT
    / "research"
    / "singularity-science"
    / "moonshots"
    / "moonshots-intelligence-template.md"
)

def render_markdown(document: dict[str, Any]) -> str:
    prov = document.get("provenance") or {}
    lines: list[str] = [
        f"# Moonshots Intelligence — {prov.get('output_basename', 'episode')}",
        "",
        "## Provenance",
        "",
        f"- Archive: `{prov.get('archive_path', '')}`",
        f"- Episode: {prov.get('episode_number', 'n/a')}",
        f"- Source: {prov.get('source_url', 'n/a')}",
        f"- Compiler: {prov.get('compiler_version', '')} · prompt `{prov.get('prompt_id', '')}` · model `{prov.get('model', '')}`",
        f"- Generated: {prov.get('generated_at', '')}",
        "",
        "## I. Core Thesis",
        "",
        str(document.get("core_thesis") or ""),
        "",
        "## II. Dual-Layer Bullets",
        "",
    ]
    for i, bullet in enumerate(document.get("bullets") or [], start=1):
        lines.extend(
            [
                f"### Bullet {i} ({bullet.get('evidence_ref', '')})",
                "",
                f"- **Claim:** {bullet.get('claim', '')}",
                f"- **Mechanism:** {bullet.get('mechanism', '')}",
                f"- **Implication:** {bullet.get('implication', '')}",
                "",
                "**Evidence (verbatim):**",
                "",
                f"> {bullet.get('evidence', '')}",
                "",
            ]
        )
    lines.extend(
        [
            "## III. Concept Primitives",
            "",
        ]
    )
    for item in document.get("concept_primitives") or []:
        lines.append(f"- {item}")
    loops = document.get("feedback_loops") or {}
    lines.extend(["", "## IV. Feedback Loops", "", "### Reinforcing", ""])
    for item in loops.get("reinforcing") or []:
        lines.append(f"- {item}")
    lines.extend(["", "### Balancing", ""])
    for item in loops.get("balancing") or []:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## V. Meta-Insight Layer",
            "",
            str(document.get("meta_insight") or ""),
            "",
        ]
    )
    if document.get("nst_mapping"):
        lines.extend(["## VI. NST Mapping (optional)", ""])
        for entry in document["nst_mapping"]:
            lines.append(
                f"- `{entry.get('evidence_ref', '')}`: object={entry.get('object_claim', '')[:80]}…"
            )
        lines.append("")
    return "\n".join(lines)
