#!/usr/bin/env python3
"""Hybrid generator for LLM-ROUTING.md from repo-map.yaml + curated prose template."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from validate_repo_routing import (  # noqa: E402
    collect_routing_metrics,
    discover_host_shelves,
    discover_source_indexes,
    format_routing_report,
    load_repo_map,
)

TEMPLATE_PATH = REPO_ROOT / "docs" / "templates" / "llm-routing-prose.md"
OUTPUT_PATH = REPO_ROOT / "LLM-ROUTING.md"
GENERATED_MARKER = "<!-- GENERATED:sections -->"
GENERATED_HEADER = """<!-- GENERATED FILE. DO NOT EDIT DIRECTLY.
Source: repo-map.yaml + docs/templates/llm-routing-prose.md
Regenerate: python3 scripts/generate_llm_routing.py
-->

---
audience: operator
authority: routing_aid
record_status: none
---

"""

def _hints(route: dict[str, Any], limit: int = 3) -> str:
    hints = route.get("search_hints") or []
    if not hints:
        return "—"
    shown = hints[:limit]
    text = ", ".join(str(h) for h in shown)
    if len(hints) > limit:
        text += ", …"
    return text

def _path_cell(route: dict[str, Any]) -> str:
    path = str(route.get("path") or route.get("path_pattern") or "")
    if not path:
        return "—"
    if path.endswith(".md") and " " not in path and not path.startswith("`"):
        return f"[{path}]({path})"
    return f"`{path}`"

def render_route_registry(routes: list[dict[str, Any]]) -> str:
    lines = [
        "## Route registry (generated from repo-map.yaml)",
        "",
        "| id | kind | category | path | search hints |",
        "|---|---|---|---|---|",
    ]
    for route in sorted(routes, key=lambda r: str(r.get("id", ""))):
        category = route.get("category")
        if not category:
            raise ValueError(f"route missing category: {route.get('id')}")
        lines.append(
            "| {id} | {kind} | {category} | {path} | {hints} |".format(
                id=route.get("id", ""),
                kind=route.get("kind", ""),
                category=category,
                path=_path_cell(route),
                hints=_hints(route),
            )
        )
    return "\n".join(lines)

def render_source_index_registry(routes: list[dict[str, Any]]) -> str:
    discovered = discover_source_indexes()
    route_by_path = {
        str(r.get("path", "")).replace("\\", "/"): r
        for r in routes
        if r.get("kind") == "source_index" and r.get("path")
    }
    lines = [
        "",
        "## Source index registry (generated)",
        "",
        "| speaker | path | repo-map id |",
        "|---|---|---|",
    ]
    for path in discovered:
        speaker = path.parent.name
        primary = path.parent / f"{speaker}-index.md"
        if primary.is_file():
            rel = primary.relative_to(REPO_ROOT).as_posix()
        else:
            rel = path.relative_to(REPO_ROOT).as_posix()
        route = route_by_path.get(rel)
        route_id = route.get("id", "—") if route else "—"
        lines.append(f"| {speaker} | [{rel}]({rel}) | {route_id} |")
    return "\n".join(lines)

def render_host_shelf_registry(routes: list[dict[str, Any]]) -> str:
    shelves = discover_host_shelves()
    route_by_path = {
        str(r.get("path", "")).replace("\\", "/"): r
        for r in routes
        if str(r.get("id", "")).endswith("-host-shelf")
    }
    lines = [
        "",
        "## Host shelf registry (generated)",
        "",
        "| host | path | repo-map id |",
        "|---|---|---|",
    ]
    for path in shelves:
        rel = path.relative_to(REPO_ROOT).as_posix()
        host = path.parent.name
        route = route_by_path.get(rel)
        route_id = route.get("id", "—") if route else "—"
        lines.append(f"| {host} | [{rel}]({rel}) | {route_id} |")
    return "\n".join(lines)

def render_generated_sections(routes: list[dict[str, Any]]) -> str:
    metrics = collect_routing_metrics(strict=False)
    parts = [
        render_route_registry(routes),
        render_source_index_registry(routes),
        render_host_shelf_registry(routes),
        "",
        format_routing_report(metrics),
    ]
    return "\n".join(parts)

def normalize_root_links(text: str) -> str:
    """Template lives under docs/templates; output is repo-root LLM-ROUTING.md."""
    replacements = [
        ("../../AGENTS.md", "AGENTS.md"),
        ("../../docs/", "docs/"),
        ("../../statecraft/", "statecraft/"),
        ("../../source-archive/", "source-archive/"),
        ("../../archive/", "archive/"),
        ("../../continuity/", "continuity/"),
        ("../../essays/", "essays/"),
        ("../../singularity/", "singularity/"),
        ("../../repo-map.yaml", "repo-map.yaml"),
        ("../../runtime/", "runtime/"),
        ("../operator-dashboards.md", "docs/operator-dashboards.md"),
        ("../start-here.md", "docs/start-here.md"),
        ("../routing-reference.md", "docs/routing-reference.md"),
        ("../prose-index.md", "docs/prose-index.md"),
        ("../source-lattice-beyond-the-repo.md", "docs/source-lattice-beyond-the-repo.md"),
        ("../archive/", "docs/archive/"),
        ("README.md](README.md)", "README.md](README.md)"),  # no-op anchor
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    text = text.replace("](../../statecraft)", "](statecraft)")
    text = text.replace("](../../singularity)", "](singularity)")
    text = text.replace("](../../source-archive/", "](source-archive/")
    return text

def build_document() -> str:
    if not TEMPLATE_PATH.is_file():
        raise FileNotFoundError(f"missing template: {TEMPLATE_PATH.relative_to(REPO_ROOT)}")
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    if GENERATED_MARKER not in template:
        raise ValueError(f"template missing marker {GENERATED_MARKER}")

    data = load_repo_map()
    routes = data.get("routes") or []
    generated = render_generated_sections(routes)
    body = template.replace(GENERATED_MARKER, generated, 1)
    body = normalize_root_links(body)
    return GENERATED_HEADER + body

def write_output(text: str) -> None:
    OUTPUT_PATH.write_text(text, encoding="utf-8", newline="\n")

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit 1 if LLM-ROUTING.md differs from generated output",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write LLM-ROUTING.md (default when neither --check nor --write)",
    )
    args = parser.parse_args()

    generated = build_document()
    if args.check:
        if not OUTPUT_PATH.is_file():
            print(f"error: missing {OUTPUT_PATH.relative_to(REPO_ROOT)}", file=sys.stderr)
            return 1
        current = OUTPUT_PATH.read_text(encoding="utf-8")
        if current != generated:
            print("error: LLM-ROUTING.md is out of date; run generate_llm_routing.py", file=sys.stderr)
            return 1
        print("ok: LLM-ROUTING.md matches generator output")
        return 0

    if args.write or not args.check:
        write_output(generated)
        print(f"wrote {OUTPUT_PATH.relative_to(REPO_ROOT)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
