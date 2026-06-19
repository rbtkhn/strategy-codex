from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from grace_mar.presentations.contract import validate_bundle
from integrations.codegraph.common import REPO_ROOT, relative_to_repo, utc_now_iso
from integrations.presentations.common import current_git_ref, write_bundle


def _markdown_citation(path: str, task: str) -> str:
    rel = relative_to_repo(Path(path))
    return f"{rel} :: CodeGraph pilot export for task '{task}'"


def _extract_mermaid(markdown_report: str) -> str:
    fence = "```mermaid"
    if fence not in markdown_report:
        return ""
    _, after = markdown_report.split(fence, 1)
    return after.split("```", 1)[0].strip()


def build_bundle(
    export_payload: dict[str, Any],
    *,
    title: str,
    audience: str,
) -> dict[str, Any]:
    export_path = export_payload.get("export_path") or "runtime/artifacts/codegraph/export.json"
    task = str(export_payload.get("task") or "architecture analysis")
    context_payload = export_payload.get("context", {})
    summary = str(context_payload.get("summary") or "No CodeGraph summary returned.")
    source_items: list[dict[str, Any]] = [
        {
            "id": "overview",
            "title": "CodeGraph summary",
            "text": summary,
            "citation": _markdown_citation(export_path, task),
            "kind": "section",
            "source_path": export_path,
            "public": False,
        }
    ]

    mermaid = _extract_mermaid(str(export_payload.get("markdown_report") or ""))
    if mermaid:
        source_items.append(
            {
                "id": "relationship-graph",
                "title": "Relationship graph",
                "text": f"```mermaid\n{mermaid}\n```",
                "citation": _markdown_citation(export_path, task),
                "kind": "diagram",
                "source_path": export_path,
                "public": False,
            }
        )

    for idx, block in enumerate(context_payload.get("codeBlocks", [])[:3], start=1):
        code = str(block.get("code") or block.get("content") or "").strip()
        if not code:
            continue
        language = block.get("language") or ""
        block_title = block.get("title") or block.get("filePath") or block.get("path") or f"Code block {idx}"
        source_path = block.get("filePath") or block.get("path") or export_path
        source_items.append(
            {
                "id": f"code-block-{idx}",
                "title": str(block_title),
                "text": f"```{language}\n{code}\n```",
                "citation": _markdown_citation(str(source_path), task),
                "kind": "code",
                "source_path": str(source_path),
                "public": False,
            }
        )

    export_hash = export_payload.get("export_sha256")
    if not export_hash:
        export_hash = hashlib.sha256(
            json.dumps(export_payload, ensure_ascii=True, sort_keys=True).encode("utf-8")
        ).hexdigest()

    bundle = {
        "family": "civ-emp",
        "subsurface": "ce-emp",
        "intent": "roadmap",
        "title": title,
        "audience": audience,
        "source_items": source_items,
        "policy": {
            "classification": "work_public_safe",
            "approved_for_render": True,
            "allowed_outputs": ["pptx", "web"],
            "source_mode": "strategy-codex-codegraph-pilot",
        },
        "provenance": {
            "source_repo": "strategy-codex",
            "source_ref": current_git_ref(),
            "bundle_created_at": utc_now_iso(),
            "content_hashes": {
                "codegraph_export": export_hash,
            },
        },
        "presentation_hints": {
            "section_order": ["overview", "relationship-graph", "code-block-1", "code-block-2"],
            "chart_candidates": ["relationship graph", "module flow", "impact surface"],
            "visual_notes": [
                "Clean tech styling with architecture-first diagrams.",
                "Prefer legible module groupings over dense all-node graphs.",
            ],
            "template_key": "grace-mar-strategy",
        },
    }
    return validate_bundle(bundle)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build a Presenton bundle from a CodeGraph pilot export.")
    parser.add_argument("--input", type=Path, required=True, help="Path to CodeGraph export JSON.")
    parser.add_argument("--output", type=Path, required=True, help="Path to presentation bundle JSON.")
    parser.add_argument(
        "--title",
        default="Strategy-Codex Architecture Review",
        help="Presentation title.",
    )
    parser.add_argument(
        "--audience",
        default="operator",
        help="Presentation audience label for the bundle contract.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    payload["export_path"] = str(args.input)
    markdown_path = args.input.with_suffix(".md")
    if markdown_path.exists():
        payload["markdown_report"] = markdown_path.read_text(encoding="utf-8")
    bundle = build_bundle(payload, title=args.title, audience=args.audience)
    output_path = args.output
    if not output_path.is_absolute():
        output_path = REPO_ROOT / output_path
    write_bundle(bundle, output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
