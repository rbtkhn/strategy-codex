from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from integrations.scenario_lab.export_to_scenario import build_markdown_report, build_packet
from integrations.scenario_lab.run_gated_simulation import (
    build_run_markdown,
    build_run_report,
)
from integrations.scenario_lab.visualize_simulation import (
    build_bundle,
    build_mermaid_tree,
    build_visualization_markdown,
)


class ScenarioLabBridgeTests(unittest.TestCase):
    def test_build_packet_collects_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            evidence_path = Path(tmpdir) / "evidence.md"
            evidence_path.write_text("# Evidence\n\nA singularity-facing note.", encoding="utf-8")
            packet = build_packet(
                scenario="Agent control futures",
                domain="company-action",
                evidence_paths=[evidence_path],
                assumptions=["Local checkout exists"],
                scenario_lab_root=Path(tmpdir) / "scenario-lab",
                forecast_root=Path(tmpdir) / ".forecast",
            )
            self.assertEqual(packet["routing_surface"], "singularity-academy")
            self.assertEqual(packet["domain"], "company-action")
            self.assertEqual(packet["assumptions"], ["Local checkout exists"])
            self.assertEqual(len(packet["evidence_items"]), 1)
            report = build_markdown_report(packet)
            self.assertIn("WORK-only", report)
            self.assertIn("Evidence", report)

    def test_failure_report_stays_advisory(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            packet_path = Path(tmpdir) / "packet.json"
            packet_path.write_text("{}", encoding="utf-8")
            report = build_run_report(
                packet={"scenario": "Agent control futures", "domain": "company-action", "assumptions": []},
                packet_path=packet_path,
                run_dir=Path(tmpdir),
                scenario_lab_root=Path(tmpdir) / "scenario-lab",
                scenario_lab_cmd=["scenario-lab"],
                runner_status="runner_unavailable",
                error_message="Scenario Lab checkout not found",
                raw_payload=None,
            )
            markdown = build_run_markdown(report)
            self.assertEqual(report["governance"]["record_authority"], "none")
            self.assertEqual(report["result"]["status"], "failed")
            self.assertIn("bounded failure artifact", markdown)

    def test_visualization_bundle_validates(self) -> None:
        report = {
            "scenario": "Agent control futures",
            "domain": "company-action",
            "packet_sha256": "abc123",
            "result": {
                "ranked_scenarios": [
                    {
                        "name": "Contained local-first loop",
                        "probability": 0.62,
                        "summary": "Local control planes stay governable.",
                        "actors": ["operator"],
                    }
                ],
                "actor_pressures": [{"actor": "operator", "pressure": 0.71, "note": "review pressure"}],
            },
        }
        packet = {
            "assumptions": ["Local-first infrastructure remains cheaper than expected."],
            "evidence_items": [{"source_path": "singularity/workshop/sheets/agent-control-plane.md"}],
        }
        mermaid = build_mermaid_tree(report)
        self.assertIn("Contained local-first loop", mermaid)
        markdown = build_visualization_markdown(report, packet)
        self.assertIn("Assumptions vs Evidence", markdown)
        bundle = build_bundle(report, packet, Path("artifacts/simulations/agent-control/report.json"))
        self.assertEqual(bundle["family"], "civ-emp")
        self.assertEqual(bundle["subsurface"], "ce-emp")
        self.assertEqual(bundle["intent"], "briefing")


if __name__ == "__main__":
    unittest.main()
