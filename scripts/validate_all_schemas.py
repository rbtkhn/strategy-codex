#!/usr/bin/env python3
"""Validate structured data against schemas/registry.yaml."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = REPO_ROOT / "schemas" / "registry.yaml"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from mcp_receipt_lib import validate_json_schema  # noqa: E402
from prediction_lib import normalize_prediction_frontmatter, parse_frontmatter_dict, repo_relative  # noqa: E402
from schema_invariants import run_prediction_invariants  # noqa: E402
from singularity_loop_invariants import run_singularity_loop_invariants  # noqa: E402
from yaml_compat import safe_load_path  # noqa: E402

SCOPE_ALL = frozenset({"all", "prediction", "runtime", "singularity"})

def load_registry() -> dict[str, Any]:
    data = safe_load_path(REGISTRY_PATH, feature="schemas/registry.yaml")
    if not isinstance(data, dict) or "schemas" not in data:
        raise ValueError("schemas/registry.yaml must contain top-level `schemas`")
    return data

def _load_schema(schema_path: Path) -> dict[str, Any]:
    return json.loads(schema_path.read_text(encoding="utf-8"))

def _validate_instance(instance: Any, schema_path: Path, *, label: str) -> str | None:
    try:
        validate_json_schema(instance, schema_path)
    except Exception as exc:
        return f"{label}: {exc}"
    return None

def _validate_json_file(file_path: Path, schema_path: Path, *, name: str) -> list[str]:
    rel = repo_relative(file_path)
    try:
        data = json.loads(file_path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        return [f"[fail] {name}: {rel} -> JSON parse error: {exc}"]
    err = _validate_instance(data, schema_path, label=rel)
    if err:
        return [f"[fail] {name}: {err}"]
    return [f"[ok] {name}: {rel}"]

def _validate_json_object_map(file_path: Path, schema_path: Path, *, name: str) -> list[str]:
    rel = repo_relative(file_path)
    try:
        data = json.loads(file_path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        return [f"[fail] {name}: {rel} -> JSON parse error: {exc}"]
    if not isinstance(data, dict):
        return [f"[fail] {name}: {rel} -> expected object map"]
    issues: list[str] = []
    for key, value in data.items():
        err = _validate_instance(value, schema_path, label=f"{rel}#{key}")
        if err:
            issues.append(f"[fail] {name}: {err}")
    if issues:
        return issues
    return [f"[ok] {name}: {rel} ({len(data)} entries)"]

def _validate_markdown_frontmatter(file_path: Path, schema_path: Path, *, name: str) -> list[str]:
    rel = repo_relative(file_path)
    text = file_path.read_text(encoding="utf-8", errors="replace")
    data = normalize_prediction_frontmatter(parse_frontmatter_dict(text, feature=rel))
    if not data:
        return [f"[fail] {name}: {rel} -> missing frontmatter"]
    err = _validate_instance(data, schema_path, label=rel)
    if err:
        return [f"[fail] {name}: {err}"]
    return [f"[ok] {name}: {rel}"]

def _validate_jsonl(file_path: Path, schema_path: Path, *, name: str) -> list[str]:
    rel = repo_relative(file_path)
    issues: list[str] = []
    line_no = 0
    ok_count = 0
    for raw in file_path.read_text(encoding="utf-8-sig", errors="replace").splitlines():
        line = raw.strip()
        if not line:
            continue
        line_no += 1
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            issues.append(f"[fail] {name}: {rel}:{line_no} -> JSON parse error: {exc}")
            continue
        err = _validate_instance(row, schema_path, label=f"{rel}:{line_no}")
        if err:
            issues.append(f"[fail] {name}: {err}")
        else:
            ok_count += 1
    if issues:
        return issues
    return [f"[ok] {name}: {rel} ({ok_count} lines)"]

def _validate_yaml_file(file_path: Path, schema_path: Path, *, name: str) -> list[str]:
    rel = repo_relative(file_path)
    try:
        data = safe_load_path(file_path, feature=rel)
    except Exception as exc:
        return [f"[fail] {name}: {rel} -> YAML parse error: {exc}"]
    err = _validate_instance(data, schema_path, label=rel)
    if err:
        return [f"[fail] {name}: {err}"]
    return [f"[ok] {name}: {rel}"]

def validate_entry(name: str, entry: dict[str, Any]) -> tuple[list[str], bool]:
    schema_path = REPO_ROOT / str(entry["path"])
    pattern = str(entry["applies_to"])
    fmt = str(entry.get("format") or "json")

    if not schema_path.is_file():
        return [f"[fail] {name}: missing schema {entry['path']}"], True

    targets = sorted(REPO_ROOT.glob(pattern))
    if not targets:
        return [f"[skip] {name}: no files match `{pattern}`"], False

    lines: list[str] = []
    failed = False
    for target in targets:
        if fmt == "json":
            batch = _validate_json_file(target, schema_path, name=name)
        elif fmt == "json_object_map":
            batch = _validate_json_object_map(target, schema_path, name=name)
        elif fmt == "markdown_frontmatter":
            batch = _validate_markdown_frontmatter(target, schema_path, name=name)
        elif fmt == "jsonl":
            batch = _validate_jsonl(target, schema_path, name=name)
        elif fmt == "yaml":
            batch = _validate_yaml_file(target, schema_path, name=name)
        else:
            return [f"[fail] {name}: unknown format `{fmt}`"], True
        for line in batch:
            lines.append(line)
            if line.startswith("[fail]"):
                failed = True
    return lines, failed

def run_validation(*, scope: str = "all", include_invariants: bool = True) -> int:
    if scope not in SCOPE_ALL:
        raise ValueError(f"invalid scope `{scope}`")

    registry = load_registry()
    schemas = registry.get("schemas") or {}
    failed = False

    for name, entry in schemas.items():
        if not isinstance(entry, dict):
            print(f"[fail] {name}: registry entry must be an object", file=sys.stderr)
            failed = True
            continue
        entry_scope = str(entry.get("scope") or "all")
        if scope != "all" and entry_scope not in {scope, "all"}:
            continue
        lines, entry_failed = validate_entry(name, entry)
        for line in lines:
            print(line)
        failed = failed or entry_failed

    if include_invariants and scope in {"all", "prediction"}:
        invariant_issues = run_prediction_invariants()
        if invariant_issues:
            failed = True
            for line in invariant_issues:
                print(f"[fail] invariants: {line}", file=sys.stderr)

    if include_invariants and scope in {"all", "singularity"}:
        try:
            from singularity_loop_lib import collect_loop_rows  # noqa: WPS433

            loop_rows = collect_loop_rows()
        except ValueError as exc:
            failed = True
            for line in str(exc).splitlines():
                print(f"[fail] singularity invariants: {line}", file=sys.stderr)
        else:
            loop_issues = run_singularity_loop_invariants(loop_rows)
            if loop_issues:
                failed = True
                for line in loop_issues:
                    print(f"[fail] singularity invariants: {line}", file=sys.stderr)

    if failed:
        print("validate_all_schemas: validation failed", file=sys.stderr)
        return 1
    print("[ok] validate_all_schemas passed")
    return 0

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--scope",
        choices=sorted(SCOPE_ALL),
        default="all",
        help="Which registry entries to validate (default: all)",
    )
    parser.add_argument(
        "--no-invariants",
        action="store_true",
        help="Skip cross-object prediction invariants",
    )
    args = parser.parse_args()
    return run_validation(scope=args.scope, include_invariants=not args.no_invariants)

if __name__ == "__main__":
    raise SystemExit(main())
