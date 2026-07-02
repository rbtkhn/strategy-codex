from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from integrations.codegraph.common import (
    DEFAULT_OUTPUT_ROOT,
    REPO_ROOT,
    relative_to_repo,
    resolve_codegraph_cmd,
    run_codegraph_json,
    utc_now_iso,
    write_json,
    write_text,
)

def _safe_node_id(value: Any, fallback: str) -> str:
    text = str(value or "").strip()
    if not text:
        text = fallback
    return text.replace(":", "_").replace("/", "_").replace("\\", "_").replace(" ", "_")

def _symbol_match_node(match: Any) -> dict[str, Any]:
    if isinstance(match, dict) and isinstance(match.get("node"), dict):
        return match["node"]
    if isinstance(match, dict):
        return match
    return {}

def build_mermaid_graph(context_payload: dict[str, Any], max_edges: int = 20) -> str:
    nodes = context_payload.get("nodes", [])
    edges = context_payload.get("edges", [])
    if not nodes:
        return "graph TD\n  empty[\"No indexed nodes returned\"]"

    lines = ["graph TD"]
    seen_nodes: set[str] = set()
    id_map: dict[str, str] = {}
    for idx, node in enumerate(nodes):
        raw_id = str(node.get("id") or node.get("name") or f"node_{idx}")
        mermaid_id = _safe_node_id(raw_id, f"node_{idx}")
        id_map[raw_id] = mermaid_id
        if mermaid_id in seen_nodes:
            continue
        seen_nodes.add(mermaid_id)
        label = str(node.get("displayName") or node.get("name") or raw_id).replace('"', "'")
        lines.append(f'  {mermaid_id}["{label}"]')

    for idx, edge in enumerate(edges[:max_edges]):
        source = id_map.get(str(edge.get("from") or edge.get("source") or ""))
        target = id_map.get(str(edge.get("to") or edge.get("target") or ""))
        if not source or not target:
            continue
        label = str(edge.get("type") or edge.get("kind") or edge.get("label") or f"edge_{idx}").replace('"', "'")
        lines.append(f'  {source} -->|"{label}"| {target}')

    if len(lines) == 1:
        return "graph TD\n  empty[\"No graph edges returned\"]"
    return "\n".join(lines)

def build_markdown_report(
    export_payload: dict[str, Any],
    *,
    task: str,
    project_path: Path | None,
) -> str:
    context_payload = export_payload["context"]
    status_payload = export_payload["status"]
    lines: list[str] = []
    lines.append(f"# CodeGraph Context Export: {task}")
    lines.append("")
    lines.append("## Pilot Frame")
    lines.append(
        "Bounded WORK-only pilot export for code exploration, pre-edit impact review, and "
        "Presenton-oriented architecture prep. This artifact is rebuildable and not governed state."
    )
    lines.append("")
    lines.append("## Index Status")
    lines.append(f"- Project path: `{project_path or 'unknown'}`")
    lines.append(f"- Indexed files: `{status_payload.get('fileCount', 'unknown')}`")
    lines.append(f"- Indexed nodes: `{status_payload.get('nodeCount', 'unknown')}`")
    lines.append(f"- Indexed edges: `{status_payload.get('edgeCount', 'unknown')}`")
    lines.append(f"- Languages: `{', '.join(status_payload.get('languages', []))}`")
    lines.append("")
    lines.append("## Query Summary")
    lines.append(str(context_payload.get("summary") or "No summary returned."))
    lines.append("")

    entry_points = context_payload.get("entryPoints", [])
    if entry_points:
        lines.append("## Entry Points")
        for entry in entry_points:
            if isinstance(entry, dict):
                name = entry.get("qualifiedName") or entry.get("name") or entry.get("id") or "unknown"
                kind = entry.get("kind") or "unknown"
                path_text = entry.get("filePath") or entry.get("path") or ""
                path_suffix = f" - `{path_text}`" if path_text else ""
                lines.append(f"- `{kind}` `{name}`{path_suffix}")
            else:
                lines.append(f"- `{entry}`")
        lines.append("")

    lines.append("## Relationship Graph")
    lines.append("```mermaid")
    lines.append(build_mermaid_graph(context_payload))
    lines.append("```")
    lines.append("")

    nodes = context_payload.get("nodes", [])
    if nodes:
        lines.append("## Top Nodes")
        for node in nodes[:10]:
            name = node.get("displayName") or node.get("name") or node.get("id") or "unknown"
            kind = node.get("kind") or "unknown"
            path_text = node.get("filePath") or node.get("path") or ""
            path_suffix = f" - `{path_text}`" if path_text else ""
            lines.append(f"- `{kind}` `{name}`{path_suffix}")
        lines.append("")

    code_blocks = context_payload.get("codeBlocks", [])
    if code_blocks:
        lines.append("## Code Blocks")
        for idx, block in enumerate(code_blocks, start=1):
            title = block.get("title") or block.get("path") or f"block-{idx}"
            title = block.get("title") or block.get("filePath") or block.get("path") or f"block-{idx}"
            language = block.get("language") or ""
            code = str(block.get("code") or block.get("content") or "").rstrip()
            if not code:
                continue
            lines.append(f"### {title}")
            lines.append(f"```{language}")
            lines.append(code)
            lines.append("```")
            lines.append("")

    symbol_queries = export_payload.get("symbol_queries", [])
    if symbol_queries:
        lines.append("## Symbol Queries")
        for item in symbol_queries:
            lines.append(f"### `{item['symbol']}`")
            payload = item["payload"]
            if isinstance(payload, dict):
                summary = payload.get("summary") or "No symbol summary returned."
                matches = payload.get("results", [])
            elif isinstance(payload, list):
                summary = f"Returned {len(payload)} symbol matches."
                matches = payload
            else:
                summary = "No symbol summary returned."
                matches = []
            lines.append(summary)
            if matches:
                for match in matches[:5]:
                    node = _symbol_match_node(match)
                    label = node.get("displayName") or node.get("qualifiedName") or node.get("name") or node.get("id") or "unknown"
                    kind = node.get("kind") or "unknown"
                    path_text = node.get("filePath") or node.get("path") or ""
                    path_suffix = f" - `{path_text}`" if path_text else ""
                    lines.append(f"- `{kind}` `{label}`{path_suffix}")
            lines.append("")

    affected_runs = export_payload.get("affected", [])
    if affected_runs:
        lines.append("## Affected Analysis")
        for run in affected_runs:
            lines.append(f"### `{run['changed_file']}`")
            payload = run["payload"]
            if isinstance(payload, dict):
                tests = payload.get("testFiles") or payload.get("tests") or []
                files = payload.get("files") or payload.get("affectedFiles") or []
                if files:
                    lines.append("- Affected files:")
                    for path_text in files[:10]:
                        lines.append(f"  - `{path_text}`")
                if tests:
                    lines.append("- Suggested tests:")
                    for test_path in tests[:10]:
                        lines.append(f"  - `{test_path}`")
                if not files and not tests:
                    lines.append("- No affected files or tests returned.")
            else:
                lines.append(f"- `{payload}`")
            lines.append("")

    related_files = context_payload.get("relatedFiles", [])
    if related_files:
        lines.append("## Related Files")
        for path_text in related_files[:15]:
            rel = relative_to_repo(Path(path_text)) if path_text else path_text
            lines.append(f"- `{rel}`")
        lines.append("")

    lines.append("## Provenance")
    lines.append(f"- Generated at: `{export_payload['generated_at']}`")
    lines.append("- Source mode: `strategy-codex-codegraph-pilot`")
    return "\n".join(lines)

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Export bounded CodeGraph context for pilot workflows.")
    parser.add_argument("--task", required=True, help="Natural-language task or architecture query.")
    parser.add_argument("--output", type=Path, required=True, help="Path to the JSON export artifact.")
    parser.add_argument("--markdown-output", type=Path, help="Optional Markdown companion report path.")
    parser.add_argument("--project-path", type=Path, default=REPO_ROOT, help="Project path to analyze.")
    parser.add_argument("--max-nodes", type=int, default=12, help="Maximum nodes to request from CodeGraph.")
    parser.add_argument("--max-code", type=int, default=4, help="Maximum code blocks to request from CodeGraph.")
    parser.add_argument("--symbol", action="append", default=[], help="Optional symbol query to resolve.")
    parser.add_argument("--query-limit", type=int, default=5, help="Maximum matches per symbol query.")
    parser.add_argument(
        "--changed-file",
        action="append",
        default=[],
        help="Optional changed file path for affected analysis.",
    )
    parser.add_argument(
        "--affected-depth",
        type=int,
        default=2,
        help="Depth to use for `codegraph affected` runs.",
    )
    parser.add_argument(
        "--codegraph-cmd",
        help="Optional command override, e.g. 'npx @colbymchenry/codegraph'.",
    )
    return parser

def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    codegraph_cmd = resolve_codegraph_cmd(args.codegraph_cmd)
    project_path = args.project_path.resolve()

    status_payload = run_codegraph_json(["status", "-j"], cwd=project_path, codegraph_cmd=codegraph_cmd)
    context_payload = run_codegraph_json(
        [
            "context",
            "--path",
            str(project_path),
            "--format",
            "json",
            "--max-nodes",
            str(args.max_nodes),
            "--max-code",
            str(args.max_code),
            args.task,
        ],
        cwd=project_path,
        codegraph_cmd=codegraph_cmd,
    )

    symbol_queries: list[dict[str, Any]] = []
    for symbol in args.symbol:
        payload = run_codegraph_json(
            ["query", symbol, "--json", "--limit", str(args.query_limit)],
            cwd=project_path,
            codegraph_cmd=codegraph_cmd,
        )
        symbol_queries.append({"symbol": symbol, "payload": payload})

    affected_runs: list[dict[str, Any]] = []
    for changed_file in args.changed_file:
        payload = run_codegraph_json(
            ["affected", changed_file, "--json", "--depth", str(args.affected_depth)],
            cwd=project_path,
            codegraph_cmd=codegraph_cmd,
        )
        affected_runs.append({"changed_file": changed_file, "payload": payload})

    export_payload = {
        "schema_version": "strategy-codex-codegraph-pilot.v1",
        "generated_at": utc_now_iso(),
        "project_path": str(project_path),
        "task": args.task,
        "status": status_payload,
        "context": context_payload,
        "symbol_queries": symbol_queries,
        "affected": affected_runs,
    }
    output_path = args.output
    if not output_path.is_absolute():
        output_path = DEFAULT_OUTPUT_ROOT / output_path
    write_json(output_path, export_payload)

    markdown_path = args.markdown_output
    if markdown_path:
        if not markdown_path.is_absolute():
            markdown_path = DEFAULT_OUTPUT_ROOT / markdown_path
        markdown = build_markdown_report(export_payload, task=args.task, project_path=project_path)
        write_text(markdown_path, markdown)

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
