from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from grace_mar.presentations.contract import validate_bundle
from integrations.presentations.common import current_git_ref, write_bundle
from integrations.scenario_lab.common import REPO_ROOT, load_json, relative_to_repo, utc_now_iso, write_text


def build_mermaid_tree(report: dict[str, Any]) -> str:
    lines = ["graph TD", '  root["Scenario Lab Run"]']
    ranked = report.get("result", {}).get("ranked_scenarios", [])
    if not ranked:
        lines.append('  root --> empty["No scenario families returned"]')
        return "\n".join(lines)
    for idx, item in enumerate(ranked[:6], start=1):
        node = f"scenario_{idx}"
        probability = (
            f"{round(item['probability'] * 100, 1)}%" if item.get("probability") is not None else "unknown"
        )
        label = f"{item.get('name', f'Scenario {idx}')} ({probability})".replace('"', "'")
        lines.append(f'  root --> {node}["{label}"]')
    return "\n".join(lines)


def build_visualization_markdown(report: dict[str, Any], packet: dict[str, Any] | None) -> str:
    lines: list[str] = []
    lines.append(f"# Scenario Lab Visualization: {report['scenario']}")
    lines.append("")
    lines.append("## Governance")
    lines.append(
        "Derived simulation artifact for singularity-academy. WORK-only, advisory, and non-Record."
    )
    lines.append("")
    lines.append("## Scenario Tree")
    lines.append("```mermaid")
    lines.append(build_mermaid_tree(report))
    lines.append("```")
    lines.append("")
    ranked = report.get("result", {}).get("ranked_scenarios", [])
    if ranked:
        lines.append("## Scenario Families")
        for item in ranked:
            probability = (
                f"{round(item['probability'] * 100, 1)}%" if item.get("probability") is not None else "unknown"
            )
            lines.append(f"- `{item['name']}` - `{probability}`")
            if item.get("summary"):
                lines.append(f"  {item['summary']}")
        lines.append("")
    pressures = report.get("result", {}).get("actor_pressures", [])
    if pressures:
        lines.append("## Actor Pressure")
        for item in pressures:
            pressure = (
                f"{round(item['pressure'] * 100, 1)}%" if item.get("pressure") is not None else "unknown"
            )
            lines.append(f"- `{item['actor']}` - `{pressure}`")
        lines.append("")
    if packet:
        lines.append("## Assumptions vs Evidence")
        assumptions = packet.get("assumptions", [])
        if assumptions:
            lines.append("### Assumptions")
            for item in assumptions:
                lines.append(f"- {item}")
            lines.append("")
        evidence_items = packet.get("evidence_items", [])
        if evidence_items:
            lines.append("### Evidence")
            for item in evidence_items:
                lines.append(f"- `{item['source_path']}`")
            lines.append("")
    return "\n".join(lines)


def build_bundle(report: dict[str, Any], packet: dict[str, Any] | None, report_path: Path) -> dict[str, Any]:
    markdown = build_visualization_markdown(report, packet)
    assumptions_text = ""
    if packet and packet.get("assumptions"):
        assumptions_text = "\n".join(f"- {item}" for item in packet["assumptions"])
    evidence_text = ""
    if packet and packet.get("evidence_items"):
        evidence_text = "\n".join(f"- {item['source_path']}" for item in packet["evidence_items"])
    bundle = {
        "family": "civ-emp",
        "subsurface": "ce-emp",
        "intent": "briefing",
        "title": f"Scenario Lab Pilot - {report['scenario']}",
        "audience": "operator",
        "source_items": [
            {
                "id": "scenario-summary",
                "title": "Scenario family summary",
                "text": "\n".join(
                    f"- {item['name']}: {round(item['probability'] * 100, 1) if item.get('probability') is not None else 'unknown'}%"
                    for item in report.get("result", {}).get("ranked_scenarios", [])
                )
                or "No scenario families returned.",
                "citation": f"{relative_to_repo(report_path)} :: Scenario Lab pilot run report",
                "kind": "section",
                "source_path": relative_to_repo(report_path),
                "public": False,
            },
            {
                "id": "scenario-tree",
                "title": "Scenario tree",
                "text": f"```mermaid\n{build_mermaid_tree(report)}\n```",
                "citation": f"{relative_to_repo(report_path)} :: Scenario Lab pilot run report",
                "kind": "diagram",
                "source_path": relative_to_repo(report_path),
                "public": False,
            },
            {
                "id": "assumptions-evidence",
                "title": "Assumptions vs evidence",
                "text": f"Assumptions\n{assumptions_text or '- none listed'}\n\nEvidence\n{evidence_text or '- no evidence packet linked'}",
                "citation": f"{relative_to_repo(report_path)} :: Scenario Lab pilot packet linkage",
                "kind": "section",
                "source_path": relative_to_repo(report_path),
                "public": False,
            },
        ],
        "policy": {
            "classification": "work_public_safe",
            "approved_for_render": True,
            "allowed_outputs": ["pptx", "web"],
            "source_mode": "strategy-codex-scenario-lab-pilot",
        },
        "provenance": {
            "source_repo": "strategy-codex",
            "source_ref": current_git_ref(),
            "bundle_created_at": utc_now_iso(),
            "content_hashes": {
                "scenario_report": report.get("packet_sha256", "unknown"),
            },
        },
        "presentation_hints": {
            "section_order": ["scenario-summary", "scenario-tree", "assumptions-evidence"],
            "chart_candidates": ["scenario tree", "actor pressure", "assumption matrix"],
            "visual_notes": [
                "Use clear branching diagrams rather than dense node clouds.",
                "Keep the governance boundary visible: simulation is advisory, not approved truth.",
            ],
            "template_key": "grace-mar-strategy",
        },
    }
    return validate_bundle(bundle)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Visualize a Scenario Lab pilot run for markdown and Presenton.")
    parser.add_argument("--input", type=Path, required=True, help="Path to report.json from run_gated_simulation.")
    parser.add_argument("--output", type=Path, required=True, help="Markdown output path.")
    parser.add_argument("--bundle-output", type=Path, help="Optional presentation bundle output path.")
    parser.add_argument("--packet", type=Path, help="Optional packet.json path; defaults to sibling packet.json.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    report = load_json(args.input)
    packet_path = args.packet or args.input.with_name("packet.json")
    packet = load_json(packet_path) if packet_path.exists() else None
    output_path = args.output
    if not output_path.is_absolute():
        output_path = REPO_ROOT / output_path
    write_text(output_path, build_visualization_markdown(report, packet))
    if args.bundle_output:
        bundle_path = args.bundle_output
        if not bundle_path.is_absolute():
            bundle_path = REPO_ROOT / bundle_path
        write_bundle(build_bundle(report, packet, args.input), bundle_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
