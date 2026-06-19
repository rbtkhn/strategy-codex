from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from integrations.scenario_lab.common import (
    DEFAULT_OUTPUT_ROOT,
    append_jsonl,
    file_sha256,
    load_json,
    relative_to_repo,
    resolve_forecast_root,
    resolve_scenario_lab_cmd,
    resolve_output_path,
    resolve_scenario_lab_root,
    run_scenario_lab,
    slugify,
    utc_now_iso,
    write_json,
    write_text,
)
from integrations.scenario_lab.export_to_scenario import build_markdown_report, build_packet


def _coerce_probability(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if number > 1:
        return round(number / 100.0, 4)
    return round(number, 4)


def normalize_runner_payload(payload: dict[str, Any]) -> dict[str, Any]:
    ranked_input = payload.get("ranked_scenarios") or payload.get("scenario_families") or []
    ranked_scenarios: list[dict[str, Any]] = []
    for idx, item in enumerate(ranked_input):
        if not isinstance(item, dict):
            continue
        ranked_scenarios.append(
            {
                "id": str(item.get("id") or f"scenario-{idx + 1}"),
                "name": str(item.get("name") or item.get("label") or f"Scenario {idx + 1}"),
                "probability": _coerce_probability(
                    item.get("probability") or item.get("confidence") or item.get("score")
                ),
                "summary": str(item.get("summary") or item.get("description") or "").strip(),
                "actors": list(item.get("actors") or item.get("actor_ids") or []),
            }
        )
    actor_input = payload.get("actor_pressures") or payload.get("actor_metrics") or []
    actor_pressures: list[dict[str, Any]] = []
    for item in actor_input:
        if not isinstance(item, dict):
            continue
        actor_pressures.append(
            {
                "actor": str(item.get("actor") or item.get("name") or "unknown"),
                "pressure": _coerce_probability(item.get("pressure") or item.get("score") or item.get("value")),
                "note": str(item.get("note") or item.get("summary") or "").strip(),
            }
        )
    assumptions = [str(x).strip() for x in payload.get("assumptions", []) if str(x).strip()]
    return {
        "ranked_scenarios": ranked_scenarios,
        "actor_pressures": actor_pressures,
        "assumptions": assumptions,
    }


def build_run_report(
    *,
    packet: dict[str, Any],
    packet_path: Path,
    run_dir: Path,
    scenario_lab_root: Path,
    scenario_lab_cmd: list[str],
    runner_status: str,
    error_message: str = "",
    raw_payload: dict[str, Any] | None = None,
    stdout: str = "",
    stderr: str = "",
) -> dict[str, Any]:
    normalized = normalize_runner_payload(raw_payload or {})
    return {
        "schema_version": "strategy-codex-scenario-lab-run.v1",
        "generated_at": utc_now_iso(),
        "routing_surface": "singularity-academy",
        "scenario": packet["scenario"],
        "domain": packet["domain"],
        "governance": {
            "mode": "work_only",
            "simulation_only": True,
            "record_authority": "none",
            "gate_effect": "none",
            "advisory_note": "Scenario Lab pilot outputs are derived/advisory and do not imply approval.",
        },
        "packet_path": relative_to_repo(packet_path),
        "packet_sha256": file_sha256(packet_path),
        "run_dir": relative_to_repo(run_dir),
        "scenario_lab": {
            "root": str(scenario_lab_root),
            "command": scenario_lab_cmd,
            "runner_status": runner_status,
            "error_message": error_message,
        },
        "result": {
            "status": "succeeded" if runner_status == "succeeded" else "failed",
            "ranked_scenarios": normalized["ranked_scenarios"],
            "actor_pressures": normalized["actor_pressures"],
            "assumptions": normalized["assumptions"] or packet.get("assumptions", []),
            "stdout_excerpt": stdout[:1200],
            "stderr_excerpt": stderr[:1200],
        },
    }


def build_run_markdown(report: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append(f"# Scenario Lab Run: {report['scenario']}")
    lines.append("")
    lines.append("## Governance")
    lines.append(
        "WORK-only simulation artifact. Advisory, derived, and non-Record. No approval semantics are implied by this run."
    )
    lines.append("")
    lines.append("## Run Status")
    lines.append(f"- domain: `{report['domain']}`")
    lines.append(f"- runner status: `{report['scenario_lab']['runner_status']}`")
    if report["scenario_lab"]["error_message"]:
        lines.append(f"- error: {report['scenario_lab']['error_message']}")
    lines.append("")
    result = report["result"]
    if result["status"] != "succeeded":
        lines.append("## Failure Posture")
        lines.append(
            "The pilot wrote a bounded failure artifact instead of pretending the simulation succeeded."
        )
        lines.append("")
        if result["stderr_excerpt"]:
            lines.append("```text")
            lines.append(result["stderr_excerpt"])
            lines.append("```")
        return "\n".join(lines)

    lines.append("## Ranked Scenario Families")
    for item in result["ranked_scenarios"]:
        probability = (
            f"{round(item['probability'] * 100, 1)}%" if item.get("probability") is not None else "unknown"
        )
        lines.append(f"- `{item['name']}` - probability `{probability}`")
        if item.get("summary"):
            lines.append(f"  {item['summary']}")
    lines.append("")
    if result["actor_pressures"]:
        lines.append("## Actor Pressure")
        for item in result["actor_pressures"]:
            pressure = (
                f"{round(item['pressure'] * 100, 1)}%" if item.get("pressure") is not None else "unknown"
            )
            note = f" - {item['note']}" if item.get("note") else ""
            lines.append(f"- `{item['actor']}` - `{pressure}`{note}")
        lines.append("")
    if result["assumptions"]:
        lines.append("## Assumptions")
        for item in result["assumptions"]:
            lines.append(f"- {item}")
        lines.append("")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a bounded Scenario Lab pilot simulation.")
    parser.add_argument("--scenario", required=True, help="Scenario question or title.")
    parser.add_argument("--domain", required=True, help="Scenario Lab domain pack name.")
    parser.add_argument("--evidence-path", action="append", required=True, help="Repo-local evidence path.")
    parser.add_argument("--assumption", action="append", default=[], help="Explicit run assumption.")
    parser.add_argument("--output-dir", type=Path, help="Optional output run directory.")
    parser.add_argument("--scenario-lab-root", help="Optional Scenario Lab checkout path.")
    parser.add_argument("--scenario-lab-cmd", help="Optional Scenario Lab command override.")
    parser.add_argument("--forecast-root", help="Optional .forecast root override.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    scenario_lab_root = resolve_scenario_lab_root(args.scenario_lab_root)
    scenario_lab_cmd = resolve_scenario_lab_cmd(args.scenario_lab_cmd)
    forecast_root = resolve_forecast_root(args.forecast_root)
    slug = slugify(args.scenario)
    run_dir = resolve_output_path(args.output_dir or Path(slug), default_root=DEFAULT_OUTPUT_ROOT)
    run_dir.mkdir(parents=True, exist_ok=True)

    evidence_paths = [Path.cwd() / path for path in args.evidence_path]
    packet = build_packet(
        scenario=args.scenario,
        domain=args.domain,
        evidence_paths=evidence_paths,
        assumptions=args.assumption,
        scenario_lab_root=scenario_lab_root,
        forecast_root=forecast_root,
    )
    packet_path = write_json(run_dir / "packet.json", packet)
    write_text(run_dir / "packet.md", build_markdown_report(packet))
    raw_output_path = run_dir / "raw-scenario-lab-output.json"

    runner_status = "runner_unavailable"
    error_message = ""
    raw_payload: dict[str, Any] | None = None
    stdout = ""
    stderr = ""

    if not scenario_lab_root.exists():
        error_message = f"Scenario Lab checkout not found at {scenario_lab_root}"
    else:
        completed = run_scenario_lab(
            [
                "simulate",
                "--root",
                str(forecast_root),
                "--domain",
                args.domain,
                "--intake",
                str(packet_path),
                "--output",
                str(raw_output_path),
            ],
            cwd=scenario_lab_root,
            scenario_lab_cmd=scenario_lab_cmd,
        )
        stdout = completed.stdout
        stderr = completed.stderr
        if completed.returncode != 0:
            runner_status = "runner_failed"
            error_message = stderr.strip() or f"Scenario Lab exited with code {completed.returncode}"
        elif raw_output_path.exists():
            runner_status = "succeeded"
            raw_payload = load_json(raw_output_path)
        else:
            runner_status = "runner_failed"
            error_message = "Scenario Lab exited without writing the expected output file."

    report = build_run_report(
        packet=packet,
        packet_path=packet_path,
        run_dir=run_dir,
        scenario_lab_root=scenario_lab_root,
        scenario_lab_cmd=scenario_lab_cmd,
        runner_status=runner_status,
        error_message=error_message,
        raw_payload=raw_payload,
        stdout=stdout,
        stderr=stderr,
    )
    report_path = write_json(run_dir / "report.json", report)
    write_text(run_dir / "report.md", build_run_markdown(report))
    append_jsonl(
        DEFAULT_OUTPUT_ROOT / "manifest.jsonl",
        {
            "generated_at": report["generated_at"],
            "scenario": report["scenario"],
            "domain": report["domain"],
            "report_path": relative_to_repo(report_path),
            "packet_path": report["packet_path"],
            "runner_status": report["scenario_lab"]["runner_status"],
            "packet_sha256": report["packet_sha256"],
        },
    )
    return 0 if runner_status == "succeeded" else 1


if __name__ == "__main__":
    raise SystemExit(main())
