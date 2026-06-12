#!/usr/bin/env python3
"""Validate LLM routing surfaces: repo-map, civ-lens INDEX, source-index registry, links."""

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

CIV_LENS = REPO_ROOT / "statecraft" / "civ-lens"
REPO_MAP_PATH = REPO_ROOT / "repo-map.yaml"
SCHEMA_PATH = REPO_ROOT / "schemas" / "repo_map.schema.json"
LLM_ROUTING = REPO_ROOT / "LLM-ROUTING.md"
CIV_INDEX = CIV_LENS / "INDEX.md"

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
    return sorted(CIV_LENS.glob("**/*-source-index.md"))


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
    for p in (LLM_ROUTING, REPO_MAP_PATH, CIV_INDEX):
        if not p.is_file():
            _err(errors, f"missing required file: {p.relative_to(REPO_ROOT)}")


def validate_route_paths(data: dict[str, Any], errors: list[str]) -> dict[str, dict[str, Any]]:
    by_path: dict[str, dict[str, Any]] = {}
    for route in data.get("routes", []):
        path = route.get("path", "")
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
                    f"    tags: [{slug}, source-index, statecraft, civ-lens]\n"
                    f"    search_hints: [{slug.title()} index, {slug} source index]",
                    file=sys.stderr,
                )

    for rel in sorted(route_paths):
        full = REPO_ROOT / rel
        if full.is_file() and "*-source-index" not in rel and not rel.endswith("-source-index.md"):
            continue
        if rel.endswith("-source-index.md") and not full.is_file():
            _err(errors, f"repo-map source_index points to missing file: {rel}")


def validate_required_routes(data: dict[str, Any], errors: list[str]) -> None:
    ids = {r.get("id") for r in data.get("routes", [])}
    for req in (
        "llm-routing",
        "civ-lens-index",
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
    if "statecraft/civ-lens/INDEX.md" not in text:
        _err(errors, "LLM-ROUTING.md must reference statecraft/civ-lens/INDEX.md")


def validate_index_lattice_section(errors: list[str]) -> None:
    text = CIV_INDEX.read_text(encoding="utf-8")
    if "source-lattice" not in text.lower():
        _err(errors, "civ-lens/INDEX.md must mention source-lattice disambiguation")


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
    validate_route_paths(data, errors)
    validate_required_routes(data, errors)

    index_text = CIV_INDEX.read_text(encoding="utf-8") if CIV_INDEX.is_file() else ""
    validate_source_index_registry(
        data, index_text, errors, generate_hints=generate_hints
    )

    validate_routing_doc_links(errors)
    validate_index_lattice_section(errors)

    source_indexes = discover_source_indexes()
    abs_files: list[Path] = list(source_indexes)
    if CIV_INDEX.is_file():
        abs_files.append(CIV_INDEX)
    if scope_all_civ_lens:
        abs_files = sorted(CIV_LENS.rglob("*.md"))

    validate_absolute_paths(abs_files, errors, allow=allow_absolute_paths)

    link_files = list(source_indexes)
    if CIV_INDEX.is_file():
        link_files.append(CIV_INDEX)
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
        help="Print YAML stubs for missing source_index routes to stderr",
    )
    args = ap.parse_args()

    if args.generate_repo_map_hints:
        print("# repo-map hints for missing source_index routes", file=sys.stderr)

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
