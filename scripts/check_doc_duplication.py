#!/usr/bin/env python3
"""Detect duplicated doctrine, routing tables, and generated prose in primary docs."""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

PRIMARY_GLOBS = (
    "README.md",
    "AGENTS.md",
    "contributing.md",
    "instance-doctrine.md",
    "docs/start-here.md",
    "docs/product-identity.md",
    "docs/harness-architecture-map.md",
    "docs/root-directory-map.md",
    "docs/routing-reference.md",
    "docs/architecture.md",
)

SKIP_PREFIXES = (
    "docs/archive/",
    "archive/",
    "docs/templates/",
)

GENERATED_MARKERS = (
    "Route registry (generated from repo-map.yaml)",
    "<!-- GENERATED FILE",
    "_Generated inventory note",
    "<!-- GENERATED — run:",
)

GRACE_MAR_DUP_RE = re.compile(
    r"Grace-Mar|grace-mar|fork revive|companion-self|recursion-gate",
    re.I,
)

MIN_DUP_PARAGRAPH_CHARS = 160
MIN_GRACE_MAR_DUP_CHARS = 80

def _iter_primary_files() -> list[Path]:
    out: set[Path] = set()
    for pattern in PRIMARY_GLOBS:
        for path in REPO_ROOT.glob(pattern):
            if not path.is_file():
                continue
            rel = path.relative_to(REPO_ROOT).as_posix()
            if any(rel.startswith(prefix) for prefix in SKIP_PREFIXES):
                continue
            out.add(path)
    return sorted(out)

def _normalize_paragraph(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())

def _paragraphs(text: str) -> list[str]:
    chunks = re.split(r"\n\s*\n", text)
    return [_normalize_paragraph(c) for c in chunks if len(_normalize_paragraph(c)) >= MIN_GRACE_MAR_DUP_CHARS]

def _table_header_key(block: str) -> str | None:
    lines = [ln.strip() for ln in block.splitlines() if ln.strip()]
    if len(lines) < 2:
        return None
    if not lines[0].startswith("|") or not lines[1].startswith("|"):
        return None
    if not re.match(r"^\|[-:\s|]+\|$", lines[1]):
        return None
    header = _normalize_paragraph(lines[0].lower())
    if header.count("|") < 2:
        return None
    return header

def _extract_markdown_tables(text: str) -> list[str]:
    tables: list[str] = []
    lines = text.splitlines()
    i = 0
    while i < len(lines) - 1:
        if lines[i].strip().startswith("|") and re.match(r"^\|[-:\s|]+\|$", lines[i + 1].strip()):
            start = i
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                i += 1
            tables.append("\n".join(lines[start:i]))
            continue
        i += 1
    return tables

def _hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]

def collect_issues(*, min_paragraph_chars: int) -> list[str]:
    issues: list[str] = []
    files = _iter_primary_files()

    paragraph_hits: dict[str, list[str]] = defaultdict(list)
    grace_mar_hits: dict[str, list[str]] = defaultdict(list)
    table_hits: dict[str, list[str]] = defaultdict(list)

    for path in files:
        rel = path.relative_to(REPO_ROOT).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")

        for marker in GENERATED_MARKERS:
            if marker in text:
                issues.append(f"{rel}: contains generated-surface marker {marker!r}")

        for para in _paragraphs(text):
            if len(para) >= min_paragraph_chars:
                key = _hash_text(para.lower())
                paragraph_hits[key].append(rel)
            if GRACE_MAR_DUP_RE.search(para):
                gkey = _hash_text(para.lower())
                grace_mar_hits[gkey].append(rel)

        for table in _extract_markdown_tables(text):
            header = _table_header_key(table)
            if not header:
                continue
            if "user asks" in header or "pick |" in header or "need |" in header:
                table_hits[header].append(rel)

    for key, paths in paragraph_hits.items():
        uniq = sorted(set(paths))
        if len(uniq) > 1:
            issues.append(
                f"duplicate paragraph ({min_paragraph_chars}+ chars) in: {', '.join(uniq)}"
            )

    for key, paths in grace_mar_hits.items():
        uniq = sorted(set(paths))
        if len(uniq) > 1:
            issues.append(f"duplicate Grace-Mar paragraph block in: {', '.join(uniq)}")

    route_like = [
        (header, sorted(set(paths)))
        for header, paths in table_hits.items()
        if len(set(paths)) > 1
        and ("route" in header or "path" in header or "kind |" in header or "analyst" in header)
    ]
    for header, paths in route_like[:20]:
        preview = header[:72] + ("…" if len(header) > 72 else "")
        issues.append(f"duplicate route-like table header in {', '.join(paths)}: {preview}")

    choose_path_tables = [
        sorted(set(paths))
        for header, paths in table_hits.items()
        if "pick |" in header or "you are" in header
    ]
    if len(choose_path_tables) > 1 or (
        choose_path_tables and len(choose_path_tables[0]) > 1
    ):
        flat = sorted({p for group in choose_path_tables for p in group})
        if len(flat) > 1:
            issues.append(f"duplicate choose-your-path table in: {', '.join(flat)}")

    return issues

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 when any duplication issue is found",
    )
    parser.add_argument(
        "--min-paragraph-chars",
        type=int,
        default=MIN_DUP_PARAGRAPH_CHARS,
        help="Minimum paragraph size for generic duplicate detection",
    )
    args = parser.parse_args()

    issues = collect_issues(min_paragraph_chars=args.min_paragraph_chars)
    if issues:
        for issue in issues:
            print(f"doc-duplication: {issue}", file=sys.stderr)
        print(f"doc-duplication: {len(issues)} issue(s)", file=sys.stderr)
        return 1 if args.strict else 0

    print("ok: doc duplication check passed")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
