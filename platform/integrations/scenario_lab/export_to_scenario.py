from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from integrations.scenario_lab.common import (
    DEFAULT_OUTPUT_ROOT,
    REPO_ROOT,
    file_sha256,
    markdown_excerpt,
    relative_to_repo,
    resolve_forecast_root,
    resolve_output_path,
    resolve_scenario_lab_root,
    utc_now_iso,
    write_json,
    write_text,
)

def build_evidence_items(paths: list[Path]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for path in paths:
        resolved = path.resolve()
        items.append(
            {
                "id": relative_to_repo(resolved).replace("/", "__"),
                "title": resolved.stem.replace("-", " ").replace("_", " "),
                "source_path": relative_to_repo(resolved),
                "sha256": file_sha256(resolved),
                "excerpt": markdown_excerpt(resolved),
            }
        )
    return items

def build_packet(
    *,
    scenario: str,
    domain: str,
    evidence_paths: list[Path],
    assumptions: list[str],
    scenario_lab_root: Path,
    forecast_root: Path,
) -> dict[str, Any]:
    return {
        "schema_version": "strategy-codex-scenario-lab-pilot.v1",
        "generated_at": utc_now_iso(),
        "routing_surface": "singularity-academy",
        "governance": {
            "mode": "work_only",
            "simulation_only": True,
            "record_authority": "none",
            "gate_effect": "none",
            "advisory_note": "Scenario Lab pilot packets are derived WORK artifacts, not approved truth.",
        },
        "scenario": scenario,
        "domain": domain,
        "scenario_lab_root": str(scenario_lab_root),
        "forecast_root": str(forecast_root),
        "assumptions": assumptions,
        "evidence_items": build_evidence_items(evidence_paths),
    }

def build_markdown_report(packet: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append(f"# Scenario Lab Intake: {packet['scenario']}")
    lines.append("")
    lines.append("## Pilot Frame")
    lines.append(
        "Bounded singularity-academy pilot packet for structured future branching, actor pressure, "
        "and ranked scenario-family work. This packet is WORK-only and not governed truth."
    )
    lines.append("")
    lines.append("## Routing")
    lines.append(f"- surface: `{packet['routing_surface']}`")
    lines.append(f"- domain: `{packet['domain']}`")
    lines.append(f"- forecast root: `{packet['forecast_root']}`")
    lines.append("")
    lines.append("## Governance")
    lines.append(
        "- simulation only: `true`; derived/advisory artifact, not evidence, not approval, not Record."
    )
    lines.append("- no automatic recursion-gate routing is part of this pilot.")
    lines.append("")
    assumptions = packet.get("assumptions", [])
    if assumptions:
        lines.append("## Explicit Assumptions")
        for item in assumptions:
            lines.append(f"- {item}")
        lines.append("")
    lines.append("## Evidence Packet")
    for item in packet.get("evidence_items", []):
        lines.append(f"### {item['title']}")
        lines.append(f"- source: `{item['source_path']}`")
        lines.append(f"- sha256: `{item['sha256']}`")
        lines.append("")
        lines.append(item["excerpt"])
        lines.append("")
    return "\n".join(lines)

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build a Scenario Lab pilot intake packet from local surfaces.")
    parser.add_argument("--scenario", required=True, help="Scenario question or title.")
    parser.add_argument("--domain", required=True, help="Scenario Lab domain pack name.")
    parser.add_argument(
        "--evidence-path",
        action="append",
        required=True,
        help="Repo-local evidence path to include in the packet.",
    )
    parser.add_argument(
        "--assumption",
        action="append",
        default=[],
        help="Explicit assumption to carry into the run.",
    )
    parser.add_argument("--output", type=Path, required=True, help="Output JSON path.")
    parser.add_argument("--markdown-output", type=Path, help="Optional Markdown report path.")
    parser.add_argument("--scenario-lab-root", help="Optional Scenario Lab checkout path.")
    parser.add_argument("--forecast-root", help="Optional .forecast root override.")
    return parser

def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    evidence_paths = [REPO_ROOT / path for path in args.evidence_path]
    packet = build_packet(
        scenario=args.scenario,
        domain=args.domain,
        evidence_paths=evidence_paths,
        assumptions=args.assumption,
        scenario_lab_root=resolve_scenario_lab_root(args.scenario_lab_root),
        forecast_root=resolve_forecast_root(args.forecast_root),
    )
    output_path = resolve_output_path(args.output, default_root=DEFAULT_OUTPUT_ROOT)
    write_json(output_path, packet)
    if args.markdown_output:
        markdown_path = resolve_output_path(args.markdown_output, default_root=DEFAULT_OUTPUT_ROOT)
        write_text(markdown_path, build_markdown_report(packet))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
