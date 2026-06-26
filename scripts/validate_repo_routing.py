#!/usr/bin/env python3
"""Validate LLM routing surfaces: repo-map, voices INDEX, source-index registry, links."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from yaml_compat import safe_load_path

VOICES = REPO_ROOT / "statecraft" / "voices"
CHANNELS = REPO_ROOT / "statecraft" / "channels"
REPO_MAP_PATH = REPO_ROOT / "repo-map.yaml"
SCHEMA_PATH = REPO_ROOT / "schemas" / "repo_map.schema.json"
LLM_ROUTING = REPO_ROOT / "LLM-ROUTING.md"
VOICES_INDEX = VOICES / "INDEX.md"

ABS_PATTERNS = (
    re.compile(r"/C:/", re.I),
    re.compile(r"C:\\", re.I),
    re.compile(r"/Users/", re.I),
    re.compile(r"/home/", re.I),
)

MD_LINK = re.compile(r"\]\(([^)]+)\)")


def _err(errors: list[str], msg: str) -> None:
    errors.append(msg)


def discover_source_indexes() -> list[Path]:
    return sorted(VOICES.glob("**/*-source-index.md"))


def discover_host_shelves() -> list[Path]:
    if not CHANNELS.is_dir():
        return []
    return sorted(CHANNELS.glob("*/README.md"))


def host_shelf_route_id(slug: str) -> str:
    return f"{slug}-host-shelf"


CATEGORY_ENUM = frozenset({"source", "work", "generated", "archive"})


def _route_path(route: dict[str, Any]) -> str:
    return str(route.get("path") or route.get("path_pattern") or "").replace("\\", "/")


def _is_verbatim_source_capture_path(path: str) -> bool:
    if not path.startswith("source-archive/statecraft/"):
        return False
    if "source-*.md" in path:
        return True
    basename = path.rsplit("/", 1)[-1]
    return basename.startswith("source-") and basename.endswith(".md")


def expected_route_category(route: dict[str, Any]) -> str:
    """Path-first authority category (four-way model)."""
    path = _route_path(route)
    kind = str(route.get("kind", ""))
    if _is_verbatim_source_capture_path(path):
        return "source"
    if kind == "source_capture":
        return "source"
    if path.startswith(("docs/archive/", "archive/grace-mar-")):
        return "archive"
    if path.startswith("runtime/artifacts/"):
        return "generated"
    if kind in {"generated_inventory", "generated_dashboard"}:
        return "generated"
    if route.get("id") == "llm-routing":
        return "generated"
    return "work"


def validate_route_categories(
    data: dict[str, Any], errors: list[str], *, strict: bool
) -> None:
    seen_categories: set[str] = set()
    for route in data.get("routes", []):
        route_id = route.get("id", "?")
        declared = route.get("category")
        expected = expected_route_category(route)
        kind = str(route.get("kind", ""))
        path = _route_path(route)

        if declared is None:
            if strict:
                _err(errors, f"repo-map missing category on {route_id}")
            else:
                print(
                    f"warning: repo-map missing category on {route_id} "
                    f"(expected {expected})",
                    file=sys.stderr,
                )
            continue

        if declared not in CATEGORY_ENUM:
            _err(errors, f"repo-map invalid category on {route_id}: {declared}")
            continue

        if declared != expected:
            _err(
                errors,
                f"repo-map category mismatch on {route_id}: "
                f"declared={declared} expected={expected} (kind={kind}, path={path})",
            )

        if "generated" in kind and kind != "source_capture" and declared != "generated":
            _err(
                errors,
                f"repo-map kind/category mismatch on {route_id}: kind={kind} requires generated",
            )

        seen_categories.add(str(declared))

    missing_quadrants = CATEGORY_ENUM - seen_categories
    if missing_quadrants:
        _err(
            errors,
            f"repo-map missing category quadrant(s): {', '.join(sorted(missing_quadrants))}",
        )


def load_repo_map() -> dict[str, Any]:
    return safe_load_path(REPO_MAP_PATH, feature="validate_repo_routing.py")


def validate_schema(data: dict[str, Any], errors: list[str]) -> None:
    try:
        import jsonschema
    except ImportError:
        _err(errors, "jsonschema required")
        return
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    try:
        jsonschema.Draft202012Validator(schema).validate(data)
    except jsonschema.ValidationError as exc:
        _err(errors, f"repo-map.yaml schema: {exc.message}")


def validate_required_files(errors: list[str]) -> None:
    for p in (LLM_ROUTING, REPO_MAP_PATH, VOICES_INDEX):
        if not p.is_file():
            _err(errors, f"missing required file: {p.relative_to(REPO_ROOT)}")


def validate_route_paths(data: dict[str, Any], errors: list[str]) -> dict[str, dict[str, Any]]:
    by_path: dict[str, dict[str, Any]] = {}
    for route in data.get("routes", []):
        path_pattern = route.get("path_pattern")
        path = str(route.get("path") or "")
        if path_pattern and not path:
            continue
        if not path:
            _err(errors, f"repo-map route missing path: {route.get('id')}")
            continue
        full = REPO_ROOT / path.replace("\\", "/")
        if not full.is_file():
            _err(errors, f"repo-map path missing: {path}")
        canon = route.get("canonical_source")
        if canon:
            canon_full = REPO_ROOT / str(canon).replace("\\", "/")
            if not canon_full.is_file():
                _err(errors, f"repo-map canonical_source missing: {canon}")
        by_path[path.replace("\\", "/")] = route
    return by_path


def validate_source_index_registry(
    data: dict[str, Any],
    index_text: str,
    errors: list[str],
    *,
    generate_hints: bool,
) -> None:
    routes = data.get("routes", [])
    route_paths = {
        str(r.get("path", "")).replace("\\", "/")
        for r in routes
        if r.get("kind") == "source_index"
    }
    discovered = discover_source_indexes()
    for si in discovered:
        rel = si.relative_to(REPO_ROOT).as_posix()
        rel_from_index = f"{si.parent.name}/{si.name}"
        if rel not in index_text and rel_from_index not in index_text and si.name not in index_text:
            _err(errors, f"INDEX.md missing source-index: {rel}")
        if rel not in route_paths:
            _err(errors, f"repo-map missing source_index route: {rel}")
            if generate_hints:
                slug = si.parent.name
                print(
                    f"  - id: {slug}-source-index\n"
                    f"    title: {slug.title()} source index\n"
                    f"    path: {rel}\n"
                    f"    kind: source_index\n"
                    f"    authority: work_only\n"
                    f"    tags: [{slug}, source-index, statecraft, voices]\n"
                    f"    search_hints: [{slug.title()} index, {slug} source index]",
                    file=sys.stderr,
                )

    for rel in sorted(route_paths):
        full = REPO_ROOT / rel
        if full.is_file() and "*-source-index" not in rel and not rel.endswith("-source-index.md"):
            continue
        if rel.endswith("-source-index.md") and not full.is_file():
            _err(errors, f"repo-map source_index points to missing file: {rel}")


def validate_host_shelf_registry(
    data: dict[str, Any],
    errors: list[str],
    *,
    generate_hints: bool,
) -> None:
    routes = data.get("routes", [])
    host_routes_by_id = {
        str(r.get("id", "")): r
        for r in routes
        if str(r.get("id", "")).endswith("-host-shelf")
    }
    discovered = discover_host_shelves()
    discovered_paths = {p.relative_to(REPO_ROOT).as_posix() for p in discovered}

    for shelf in discovered:
        slug = shelf.parent.name
        expected_id = host_shelf_route_id(slug)
        expected_path = shelf.relative_to(REPO_ROOT).as_posix()
        route = host_routes_by_id.get(expected_id)
        if route is None:
            _err(errors, f"repo-map missing host_shelf route: {expected_id}")
            if generate_hints:
                title = slug.replace("-", " ").title()
                print(
                    f"  - id: {expected_id}\n"
                    f"    title: {title} host shelf\n"
                    f"    path: {expected_path}\n"
                    f"    kind: routing_aid\n"
                    f"    authority: work_only\n"
                    f"    tags: [{slug}, host-shelf, statecraft]\n"
                    f"    search_hints: [{title} host, {slug} profile]",
                    file=sys.stderr,
                )
            continue
        rel = str(route.get("path", "")).replace("\\", "/")
        if rel != expected_path:
            _err(
                errors,
                f"repo-map host_shelf path mismatch for {expected_id}: {rel} != {expected_path}",
            )
        if route.get("kind") != "routing_aid":
            _err(errors, f"repo-map host_shelf {expected_id} must have kind routing_aid")
        full = REPO_ROOT / rel
        if not full.is_file():
            _err(errors, f"repo-map host_shelf points to missing file: {rel}")

    for route_id, route in host_routes_by_id.items():
        rel = str(route.get("path", "")).replace("\\", "/")
        if rel not in discovered_paths:
            _err(errors, f"repo-map host_shelf orphan route (no disk shelf): {route_id}")


def validate_required_routes(data: dict[str, Any], errors: list[str]) -> None:
    ids = {r.get("id") for r in data.get("routes", [])}
    for req in (
        "llm-routing",
        "voices-index",
        "source-lattice-doctrine",
        "ph-civ-source-lattice",
        "barnes-source-index",
    ):
        if req not in ids:
            _err(errors, f"repo-map missing required route id: {req}")


def validate_routing_doc_links(errors: list[str]) -> None:
    text = LLM_ROUTING.read_text(encoding="utf-8")
    if "source-lattice-beyond-the-repo.md" not in text:
        _err(errors, "LLM-ROUTING.md must link to docs/source-lattice-beyond-the-repo.md")
    if "statecraft/voices/INDEX.md" not in text:
        _err(errors, "LLM-ROUTING.md must reference statecraft/voices/INDEX.md")


def validate_index_lattice_section(errors: list[str]) -> None:
    text = VOICES_INDEX.read_text(encoding="utf-8")
    if "source-lattice" not in text.lower():
        _err(errors, "voices/INDEX.md must mention source-lattice disambiguation")


def has_absolute_path(text: str) -> bool:
    return any(p.search(text) for p in ABS_PATTERNS)


def resolve_md_link(from_file: Path, target: str) -> Path | None:
    target = target.strip()
    if not target or target.startswith(("http://", "https://", "mailto:")):
        return None
    if target.startswith("#"):
        return from_file
    if target.startswith("/"):
        return None
    dest = (from_file.parent / target).resolve()
    return dest


def validate_markdown_links(
    files: list[Path],
    errors: list[str],
    *,
    strict: bool,
) -> None:
    if not strict:
        return
    for fp in files:
        text = fp.read_text(encoding="utf-8")
        for match in MD_LINK.finditer(text):
            target = match.group(1)
            dest = resolve_md_link(fp, target)
            if dest is None:
                continue
            if dest.is_file() or dest == fp:
                continue
            if dest.is_dir():
                continue
            if target.rstrip("/").endswith("/") or target.endswith("/"):
                parent = (fp.parent / target.rstrip("/")).resolve()
                if parent.is_dir():
                    continue
            _err(
                errors,
                f"broken link in {fp.relative_to(REPO_ROOT)}: {target}",
            )


def validate_absolute_paths(
    files: list[Path],
    errors: list[str],
    *,
    allow: bool,
) -> None:
    if allow:
        return
    for fp in files:
        text = fp.read_text(encoding="utf-8")
        if has_absolute_path(text):
            _err(
                errors,
                f"absolute path in {fp.relative_to(REPO_ROOT)}",
            )


def _index_lists_source_index(rel: str, index_text: str, basename: str) -> bool:
    parent_name = Path(rel).parent.name
    rel_from_index = f"{parent_name}/{basename}"
    return rel in index_text or rel_from_index in index_text or basename in index_text


def collect_routing_metrics(*, strict: bool = False) -> dict[str, Any]:
    """Lightweight coverage counters for routing surfaces (read-only)."""
    data = load_repo_map() if REPO_MAP_PATH.is_file() else {"routes": []}
    routes = data.get("routes", [])
    source_indexes = discover_source_indexes()
    index_text = VOICES_INDEX.read_text(encoding="utf-8") if VOICES_INDEX.is_file() else ""

    route_paths = {
        str(r.get("path", "")).replace("\\", "/")
        for r in routes
        if r.get("kind") == "source_index"
    }
    discovered = {p.relative_to(REPO_ROOT).as_posix() for p in source_indexes}
    host_shelves = discover_host_shelves()
    host_shelf_paths = {p.relative_to(REPO_ROOT).as_posix() for p in host_shelves}
    host_shelf_route_paths = {
        str(r.get("path", "")).replace("\\", "/")
        for r in routes
        if str(r.get("id", "")).endswith("-host-shelf")
    }

    link_files = list(source_indexes)
    if VOICES_INDEX.is_file():
        link_files.append(VOICES_INDEX)
    markdown_links = 0
    absolute_path_violations = 0
    for fp in link_files:
        text = fp.read_text(encoding="utf-8")
        markdown_links += len(MD_LINK.findall(text))
        if has_absolute_path(text):
            absolute_path_violations += 1

    index_listed = sum(
        1 for rel in discovered if _index_lists_source_index(rel, index_text, Path(rel).name)
    )
    repo_map_listed = sum(1 for rel in discovered if rel in route_paths)
    host_shelf_repo_map_listed = sum(
        1 for rel in host_shelf_paths if rel in host_shelf_route_paths
    )

    broken_link_count = 0
    if strict:
        link_errors: list[str] = []
        validate_markdown_links(link_files, link_errors, strict=True)
        broken_link_count = len(link_errors)

    kinds: dict[str, int] = {}
    for route in routes:
        kind = str(route.get("kind", "unknown"))
        kinds[kind] = kinds.get(kind, 0) + 1

    coverage_denominator = len(discovered) or 1
    registry_coverage_pct = round(
        100.0 * min(index_listed, repo_map_listed) / coverage_denominator,
        1,
    )

    host_denominator = len(host_shelf_paths) or 1
    host_shelf_coverage_pct = round(
        100.0 * host_shelf_repo_map_listed / host_denominator,
        1,
    )

    return {
        "source_index_count": len(discovered),
        "host_shelf_count": len(host_shelf_paths),
        "markdown_link_count": markdown_links,
        "repo_map_routes_total": len(routes),
        "repo_map_routes_by_kind": kinds,
        "repo_map_source_index_routes": len(route_paths),
        "repo_map_host_shelf_routes": len(host_shelf_route_paths),
        "registry_index_listed": index_listed,
        "registry_repo_map_listed": repo_map_listed,
        "registry_coverage_pct": registry_coverage_pct,
        "host_shelf_repo_map_listed": host_shelf_repo_map_listed,
        "host_shelf_coverage_pct": host_shelf_coverage_pct,
        "absolute_path_violations": absolute_path_violations,
        "broken_link_count": broken_link_count,
        "required_surfaces_present": all(
            p.is_file() for p in (LLM_ROUTING, REPO_MAP_PATH, VOICES_INDEX)
        ),
    }


def format_routing_report(metrics: dict[str, Any]) -> str:
    kinds = metrics.get("repo_map_routes_by_kind") or {}
    kind_line = ", ".join(f"{k}={v}" for k, v in sorted(kinds.items()))
    lines = [
        "## Repo routing metrics",
        "",
        f"- source indexes (disk): {metrics['source_index_count']}",
        f"- host shelves (disk): {metrics['host_shelf_count']}",
        f"- markdown links (INDEX + source-index files): {metrics['markdown_link_count']}",
        f"- repo-map routes: {metrics['repo_map_routes_total']} ({kind_line})",
        f"- source_index routes in repo-map: {metrics['repo_map_source_index_routes']}",
        f"- host_shelf routes in repo-map: {metrics['repo_map_host_shelf_routes']}",
        f"- registry: INDEX lists {metrics['registry_index_listed']}/{metrics['source_index_count']}, "
        f"repo-map lists {metrics['registry_repo_map_listed']}/{metrics['source_index_count']} "
        f"({metrics['registry_coverage_pct']}% bijection when both match)",
        f"- host shelves: repo-map lists {metrics['host_shelf_repo_map_listed']}/{metrics['host_shelf_count']} "
        f"({metrics['host_shelf_coverage_pct']}%)",
        f"- absolute path violations (INDEX + source-index): {metrics['absolute_path_violations']}",
        f"- broken links (--strict resolution): {metrics['broken_link_count']}",
        f"- required surfaces present: {metrics['required_surfaces_present']}",
    ]
    return "\n".join(lines)


def validate_all(
    *,
    strict: bool,
    allow_absolute_paths: bool,
    scope_all_civ_lens: bool,
    generate_hints: bool,
) -> list[str]:
    errors: list[str] = []
    validate_required_files(errors)
    if not REPO_MAP_PATH.is_file():
        return errors

    data = load_repo_map()
    validate_schema(data, errors)
    validate_route_categories(data, errors, strict=strict)
    validate_route_paths(data, errors)
    validate_required_routes(data, errors)

    index_text = VOICES_INDEX.read_text(encoding="utf-8") if VOICES_INDEX.is_file() else ""
    validate_source_index_registry(
        data, index_text, errors, generate_hints=generate_hints
    )
    validate_host_shelf_registry(data, errors, generate_hints=generate_hints)

    validate_routing_doc_links(errors)
    validate_index_lattice_section(errors)

    source_indexes = discover_source_indexes()
    abs_files: list[Path] = list(source_indexes)
    if VOICES_INDEX.is_file():
        abs_files.append(VOICES_INDEX)
    if scope_all_civ_lens:
        abs_files = sorted(VOICES.rglob("*.md"))

    validate_absolute_paths(abs_files, errors, allow=allow_absolute_paths)

    link_files = list(source_indexes)
    if VOICES_INDEX.is_file():
        link_files.append(VOICES_INDEX)
    validate_markdown_links(link_files, errors, strict=strict)

    return errors


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--strict",
        action="store_true",
        help="Fail on broken markdown links in INDEX and source-index files",
    )
    ap.add_argument(
        "--allow-absolute-paths",
        action="store_true",
        help="Skip absolute path ban (local use before link normalization)",
    )
    ap.add_argument(
        "--scope",
        choices=("source-index", "all-civ-lens"),
        default="source-index",
        help="Which files receive absolute-path checks",
    )
    ap.add_argument(
        "--generate-repo-map-hints",
        action="store_true",
        help="Print YAML stubs for missing source_index and host_shelf routes to stderr",
    )
    ap.add_argument(
        "--report",
        action="store_true",
        help="Print routing coverage metrics to stdout (runs validation too)",
    )
    ap.add_argument(
        "--report-json",
        action="store_true",
        help="Print routing metrics as JSON to stdout (runs validation too)",
    )
    args = ap.parse_args()

    if args.generate_repo_map_hints:
        print("# repo-map hints for missing source_index / host_shelf routes", file=sys.stderr)

    if args.report or args.report_json:
        metrics = collect_routing_metrics(strict=args.strict)
        if args.report_json:
            print(json.dumps(metrics, indent=2, sort_keys=True))
        if args.report:
            print(format_routing_report(metrics))

    errors = validate_all(
        strict=args.strict,
        allow_absolute_paths=args.allow_absolute_paths,
        scope_all_civ_lens=args.scope == "all-civ-lens",
        generate_hints=args.generate_repo_map_hints,
    )
    if errors:
        for e in errors:
            print(f"error: {e}", file=sys.stderr)
        return 1
    print("ok: repo routing validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
