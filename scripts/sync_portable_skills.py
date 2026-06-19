#!/usr/bin/env python3
"""
Assemble .cursor/skills/*/SKILL.md from skills/*/SKILL.md + optional CURSOR_APPENDIX.md.

Usage:
    python3 scripts/sync_portable_skills.py
    python3 scripts/sync_portable_skills.py --dry-run
    python3 scripts/sync_portable_skills.py --verify
    python3 scripts/sync_portable_skills.py --skill politics-massie
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from yaml_compat import safe_dump, safe_load_path, safe_load_text

_MANIFEST = _REPO / "skills" / "manifest.yaml"
_GENERATOR = "sync_portable_skills.py"


def _reject_unsupported_yaml_subset(text: str) -> None:
    unsupported_patterns = (
        (r"(?m)^\s*[^#\n][^:\n]*:\s*[>|]", "block scalars"),
        (r"(?m)^\s*-\s*[>|]", "block scalars"),
        (r"(?m)^\s*[^#\n].*:\s*(\[[^\]]*\]|\{[^}]*\})\s*$", "inline collections"),
        (r"(?m)^\s*-\s*(\[[^\]]*\]|\{[^}]*\})\s*$", "inline collections"),
        (r"(?m)^\s*[^#\n].*:\s*[&*][^\s#]+", "anchors or aliases"),
        (r"(?m)^\s*-\s*[&*][^\s#]+", "anchors or aliases"),
        (r"(?m)^\s*<<\s*:", "merge keys"),
        (r"(?m)^\s*[^#\n].*:\s*null\s*$", "null scalars"),
    )
    for pattern, label in unsupported_patterns:
        if re.search(pattern, text):
            raise ValueError(
                f"Unsupported YAML subset for sync_portable_skills.py: {label}. "
                "Use plain scalars, nested maps, and nested lists only."
            )


def _parse_scalar(value: str):
    value = value.strip()
    if not value:
        return ""
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    low = value.lower()
    if low == "true":
        return True
    if low == "false":
        return False
    return value


def _parse_yaml_subset(text: str):
    _reject_unsupported_yaml_subset(text)
    lines = text.splitlines()

    def nonempty(idx: int) -> bool:
        if idx >= len(lines):
            return False
        stripped = lines[idx].strip()
        return bool(stripped) and not stripped.startswith("#")

    def indent_of(idx: int) -> int:
        return len(lines[idx]) - len(lines[idx].lstrip(" "))

    def next_significant(idx: int) -> int | None:
        j = idx
        while j < len(lines):
            if nonempty(j):
                return j
            j += 1
        return None

    def parse_block(idx: int, indent: int):
        start = next_significant(idx)
        if start is None or indent_of(start) < indent:
            return {}, start if start is not None else len(lines)
        if lines[start].lstrip().startswith("- "):
            return parse_list(start, indent)
        return parse_map(start, indent)

    def parse_list(idx: int, indent: int):
        out = []
        i = idx
        while True:
            i = next_significant(i)
            if i is None:
                return out, len(lines)
            current_indent = indent_of(i)
            if current_indent < indent:
                return out, i
            if current_indent != indent or not lines[i].lstrip().startswith("- "):
                return out, i
            rest = lines[i].lstrip()[2:].strip()
            i += 1
            if not rest:
                child, i = parse_block(i, indent + 2)
                out.append(child)
                continue
            if ":" in rest:
                key, sep, value = rest.partition(":")
                key = key.strip()
                item = {}
                if value.strip():
                    item[key] = _parse_scalar(value.strip())
                else:
                    child, i = parse_block(i, indent + 2)
                    item[key] = child
                nxt = next_significant(i)
                if nxt is not None and indent_of(nxt) >= indent + 2:
                    child, i = parse_map(nxt, indent + 2)
                    if isinstance(child, dict):
                        item.update(child)
                out.append(item)
                continue
            out.append(_parse_scalar(rest))

    def parse_map(idx: int, indent: int):
        out = {}
        i = idx
        while True:
            i = next_significant(i)
            if i is None:
                return out, len(lines)
            current_indent = indent_of(i)
            if current_indent < indent:
                return out, i
            if current_indent != indent:
                return out, i
            stripped = lines[i].strip()
            key, sep, value = stripped.partition(":")
            if not sep:
                raise ValueError(f"Unsupported YAML line: {stripped!r}")
            key = key.strip()
            value = value.strip()
            i += 1
            if value:
                out[key] = _parse_scalar(value)
                continue
            nxt = next_significant(i)
            if nxt is None or indent_of(nxt) <= indent:
                out[key] = {}
                continue
            child, i = parse_block(nxt, indent + 2)
            out[key] = child

    parsed, _ = parse_block(0, 0)
    return parsed


def _dump_yaml_subset(data, *, indent: int = 0) -> str:
    def format_scalar(value):
        if isinstance(value, bool):
            return "true" if value else "false"
        if value is None:
            return '""'
        if isinstance(value, (int, float)):
            return str(value)
        text = str(value).replace("\\", "\\\\").replace('"', '\\"')
        return f'"{text}"'

    lines: list[str] = []
    pad = " " * indent
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, list):
                lines.append(f"{pad}{key}:")
                lines.append(_dump_yaml_subset(value, indent=indent + 2))
            elif isinstance(value, dict):
                lines.append(f"{pad}{key}:")
                nested = _dump_yaml_subset(value, indent=indent + 2)
                if nested:
                    lines.append(nested)
            else:
                lines.append(f"{pad}{key}: {format_scalar(value)}")
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                keys = list(item.keys())
                if not keys:
                    lines.append(f"{pad}- {{}}")
                    continue
                first = keys[0]
                first_value = item[first]
                if isinstance(first_value, (dict, list)):
                    lines.append(f"{pad}- {first}:")
                    nested = _dump_yaml_subset(first_value, indent=indent + 4)
                    if nested:
                        lines.append(nested)
                else:
                    lines.append(f"{pad}- {first}: {format_scalar(first_value)}")
                for key in keys[1:]:
                    value = item[key]
                    if isinstance(value, list):
                        lines.append(f"{pad}  {key}:")
                        nested = _dump_yaml_subset(value, indent=indent + 4)
                        if nested:
                            lines.append(nested)
                    elif isinstance(value, dict):
                        lines.append(f"{pad}  {key}:")
                        nested = _dump_yaml_subset(value, indent=indent + 4)
                        if nested:
                            lines.append(nested)
                    else:
                        lines.append(f"{pad}  {key}: {format_scalar(value)}")
            elif isinstance(item, list):
                lines.append(f"{pad}-")
                nested = _dump_yaml_subset(item, indent=indent + 2)
                if nested:
                    lines.append(nested)
            else:
                lines.append(f"{pad}- {format_scalar(item)}")
    return "\n".join(lines)


def _load_yaml(path: Path) -> dict:
    def _is_manifest_shape(data: object) -> bool:
        if not isinstance(data, dict):
            return False
        skills = data.get("skills")
        if skills is None:
            return True
        return isinstance(skills, list) and all(isinstance(item, dict) for item in skills)

    try:
        data = safe_load_path(path, feature="sync_portable_skills.py")
        if not _is_manifest_shape(data):
            data = _parse_yaml_subset(path.read_text(encoding="utf-8"))
    except RuntimeError as e:
        if "PyYAML is required" not in str(e):
            raise
        data = _parse_yaml_subset(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def _split_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return {}, text
    raw = m.group(1)
    body = text[m.end() :]
    try:
        try:
            meta = safe_load_text(raw, feature="sync_portable_skills.py")
        except RuntimeError as e:
            if "PyYAML is required" not in str(e):
                raise
            meta = _parse_yaml_subset(raw)
        return (meta if isinstance(meta, dict) else {}), body
    except Exception as e:
        print(f"YAML frontmatter parse error: {e}", file=sys.stderr)
        sys.exit(1)


def _dump_frontmatter(meta: dict) -> str:
    # Wide width so `description` stays one physical line (hosts break on wrapped YAML).
    try:
        s = safe_dump(
            meta,
            feature="sync_portable_skills.py",
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
            width=2000,
        ).rstrip()
    except RuntimeError as e:
        if "PyYAML is required" not in str(e):
            raise
        s = _dump_yaml_subset(meta).rstrip()
    return f"---\n{s}\n---\n"


def _verify_skill(portable_body: str, forbidden: list[str], skill_name: str) -> list[str]:
    errs: list[str] = []
    for sub in forbidden:
        if sub in portable_body:
            errs.append(f"{skill_name}: portable body must not contain {sub!r}")
    return errs


def _verify_description_one_line(meta: dict, skill_name: str) -> list[str]:
    errs: list[str] = []
    d = meta.get("description")
    if d is None:
        return [f"{skill_name}: missing description"]
    if not isinstance(d, str):
        return [f"{skill_name}: description must be a string"]
    if "\n" in d:
        errs.append(f"{skill_name}: description must be a single line (contains newline)")
    return errs


def sync_one(
    entry: dict,
    *,
    dry_run: bool,
    verify_only: bool,
) -> tuple[str, list[str]]:
    """Returns (status, errors). status in ok, skip, write."""
    name = entry.get("name")
    src_rel = entry.get("source")
    tgt_rel = entry.get("target")
    apx_rel = entry.get("appendix")
    forbidden = entry.get("verify_forbidden_substrings") or []

    if not name or not src_rel or not tgt_rel:
        return "skip", [f"bad manifest entry: {entry!r}"]

    src = _REPO / "skills" / src_rel
    tgt = _REPO / tgt_rel
    apx = _REPO / apx_rel if apx_rel else None

    if not src.is_file():
        return "skip", [f"missing source {src}"]

    raw = src.read_text(encoding="utf-8")
    meta, body = _split_frontmatter(raw)
    errs = _verify_description_one_line(meta, name)
    errs += _verify_skill(body, forbidden, name)
    if meta.get("portable") is not True:
        errs.append(f"{name}: portable: true required in source frontmatter")

    if verify_only:
        return ("ok" if not errs else "error"), errs

    if errs:
        return "error", errs

    meta_out = dict(meta)
    meta_out["portable_source"] = f"skills/{src_rel}"
    meta_out["synced_by"] = _GENERATOR

    appendix_block = ""
    if apx and apx.is_file():
        apx_text = apx.read_text(encoding="utf-8").strip()
        appendix_block = f"\n\n## Cursor / grace-mar instance\n\n{apx_text}\n"
    elif apx_rel:
        appendix_block = f"\n\n## Cursor / grace-mar instance\n\n_(appendix missing: {apx_rel})_\n"

    out = _dump_frontmatter(meta_out) + body.lstrip("\n") + appendix_block

    if dry_run:
        print(f"[dry-run] would write {tgt} ({len(out)} bytes)")
        return "ok", []

    tgt.parent.mkdir(parents=True, exist_ok=True)
    tgt.write_text(out, encoding="utf-8")
    print(f"Wrote {tgt}")
    return "ok", []


def main() -> int:
    p = argparse.ArgumentParser(description="Assemble Cursor skills from skills/.")
    p.add_argument("--dry-run", action="store_true", help="Print actions only")
    p.add_argument("--verify", action="store_true", help="Validate only; no writes")
    p.add_argument("--skill", metavar="NAME", help="Sync a single manifest name")
    args = p.parse_args()

    if not _MANIFEST.is_file():
        print(f"Missing {_MANIFEST}", file=sys.stderr)
        return 1

    data = _load_yaml(_MANIFEST)
    skills = data.get("skills") or []
    if not isinstance(skills, list):
        print("manifest skills: must be a list", file=sys.stderr)
        return 1

    all_errs: list[str] = []
    for entry in skills:
        if not isinstance(entry, dict):
            continue
        if args.skill and entry.get("name") != args.skill:
            continue
        status, errs = sync_one(entry, dry_run=args.dry_run, verify_only=args.verify)
        all_errs.extend(errs)
        if status == "error":
            for e in errs:
                print(e, file=sys.stderr)

    if all_errs:
        return 1
    if args.verify:
        print("verify: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
