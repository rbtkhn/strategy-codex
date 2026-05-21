from __future__ import annotations

import json
from pathlib import Path
from unittest import mock
import unittest

from integrations.codegraph import common
from integrations.codegraph.export_code_context import (
    build_markdown_report,
    build_mermaid_graph,
)
from integrations.codegraph.generate_architecture_bundle import build_bundle


class CodeGraphBridgeTests(unittest.TestCase):
    def test_resolve_codegraph_cmd_prefers_local_windows_binary(self) -> None:
        fake_binary = Path(
            "C:/dev/strategy-codex/.codex-tmp/npm-cache/_npx/demo/node_modules/"
            "@colbymchenry/codegraph-win32-x64/bin/codegraph.cmd"
        )
        with mock.patch.object(common, "find_local_codegraph_cmd", return_value=[str(fake_binary)]), mock.patch.dict(
            common.os.environ,
            {},
            clear=True,
        ):
            cmd = common.resolve_codegraph_cmd()

        self.assertEqual(cmd, [str(fake_binary)])

    def test_build_mermaid_graph_includes_edge_labels(self) -> None:
        graph = build_mermaid_graph(
            {
                "nodes": [
                    {"id": "a", "displayName": "Alpha"},
                    {"id": "b", "displayName": "Beta"},
                ],
                "edges": [{"from": "a", "to": "b", "type": "calls"}],
            }
        )
        self.assertIn('a["Alpha"]', graph)
        self.assertIn('-->|"calls"| b', graph)

    def test_build_markdown_report_includes_pilot_sections(self) -> None:
        payload = {
            "generated_at": "2026-05-21T00:00:00+00:00",
            "status": {
                "fileCount": 10,
                "nodeCount": 20,
                "edgeCount": 30,
                "languages": ["python"],
            },
            "context": {
                "summary": "Presentation code is clustered around one service.",
                "entryPoints": [
                    {
                        "qualifiedName": "PresentationService",
                        "kind": "class",
                        "filePath": "src/grace_mar/presentations/service.py",
                    }
                ],
                "nodes": [{"id": "svc", "displayName": "PresentationService", "kind": "class"}],
                "edges": [],
                "codeBlocks": [
                    {
                        "filePath": "src/grace_mar/presentations/service.py",
                        "language": "python",
                        "content": "class X:\n    pass",
                    }
                ],
                "relatedFiles": ["src/grace_mar/presentations/service.py"],
            },
            "symbol_queries": [{"symbol": "PresentationService", "payload": []}],
            "affected": [],
        }
        report = build_markdown_report(
            payload,
            task="presentation service architecture",
            project_path=None,
        )
        self.assertIn("## Pilot Frame", report)
        self.assertIn("## Relationship Graph", report)
        self.assertIn("## Code Blocks", report)
        self.assertIn("strategy-codex-codegraph-pilot", report)

    def test_build_bundle_validates_contract(self) -> None:
        export_payload = {
            "task": "presentation service architecture",
            "export_path": "artifacts/codegraph/service-architecture.json",
            "export_sha256": "abc123",
            "markdown_report": "## Relationship Graph\n```mermaid\ngraph TD\n  A-->B\n```",
            "context": {
                "summary": "The presentation service coordinates intents and rendering.",
                "codeBlocks": [
                    {
                        "filePath": "src/grace_mar/presentations/service.py",
                        "language": "python",
                        "content": "class PresentationService:\n    pass",
                    }
                ],
            },
        }
        bundle = build_bundle(
            export_payload,
            title="Strategy-Codex Presentation Service Architecture",
            audience="operator",
        )
        self.assertEqual(bundle["family"], "civ-emp")
        self.assertEqual(bundle["subsurface"], "ce-emp")
        self.assertEqual(bundle["intent"], "roadmap")
        self.assertEqual(bundle["policy"]["source_mode"], "strategy-codex-codegraph-pilot")
        self.assertTrue(json.dumps(bundle))


if __name__ == "__main__":
    unittest.main()
