#!/usr/bin/env python3
"""Validate audience / authority / record_status markers on high-traffic docs."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_DOCS = (
    "README.md",
    "docs/public-orientation.md",
    "docs/start-here.md",
    "AGENTS.md",
    "LLM-ROUTING.md",
    "docs/archive/grace-mar.md",
    "docs/root-directory-map.md",
    "docs/harness-architecture-map.md",
    "docs/work-membrane-v2.md",
    "essays/README.md",
)

ALLOWED = {
    "audience": {"public", "operator", "archive", "generated"},
    "authority": {
        "source",
        "synthesis",
        "note",
        "transaction",
        "routing_aid",
        "archive",
        "doctrine",
    },
    "record_status": {"none", "frozen", "fork_revive_only"},
}

FRONTMATTER_RE = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL | re.MULTILINE)
FIELD_RE = re.compile(r"^(audience|authority|record_status):\s*(\S+)\s*$", re.MULTILINE)
RECORD_TOPIC_RE = re.compile(
    r"Grace-Mar|\bRecord\b|recursion-gate|fork revive|fork-revive",
    re.I,
)
FROZEN_RE = re.compile(r"frozen|fork[- ]revive|reference-only|archive only", re.I)


def parse_frontmatter(text: str) -> dict[str, str]:
    text = text.lstrip("\ufeff").replace("\r\n", "\n")
    head = "\n".join(text.splitlines()[:50])
    match = FRONTMATTER_RE.search(head)
    if not match:
        return {}
    block = match.group(1)
    return {m.group(1): m.group(2) for m in FIELD_RE.finditer(block)}


def validate_file(path: Path) -> list[str]:
    rel = path.relative_to(REPO_ROOT).as_posix()
    text = path.read_text(encoding="utf-8", errors="replace")
    fields = parse_frontmatter(text)
    issues: list[str] = []

    for key in ("audience", "authority", "record_status"):
        if key not in fields:
            issues.append(f"{rel}: missing frontmatter `{key}`")
            continue
        if fields[key] not in ALLOWED[key]:
            issues.append(f"{rel}: invalid `{key}: {fields[key]}`")

    if fields.get("audience") == "public" and RECORD_TOPIC_RE.search(text):
        if not FROZEN_RE.search(text):
            issues.append(
                f"{rel}: public doc mentions Record/Grace-Mar without frozen/fork-revive framing"
            )

    if fields.get("record_status") in {"frozen", "fork_revive_only"}:
        if not RECORD_TOPIC_RE.search(text) and rel != "docs/archive/grace-mar.md":
            issues.append(f"{rel}: record_status set but no Record topic anchor in body")

    return issues


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--path", action="append", dest="paths", help="Extra doc to check")
    args = ap.parse_args()

    targets: list[Path] = []
    for rel in REQUIRED_DOCS:
        path = REPO_ROOT / rel
        if path.is_file():
            targets.append(path)
    for rel in args.paths or []:
        path = (REPO_ROOT / rel).resolve()
        if path.is_file():
            targets.append(path)

    issues: list[str] = []
    for path in sorted(set(targets)):
        issues.extend(validate_file(path))

    if issues:
        for line in issues:
            print(line, file=sys.stderr)
        print(f"check_doc_authority_markers: {len(issues)} issue(s)", file=sys.stderr)
        return 1

    print(f"check_doc_authority_markers: ok ({len(targets)} doc(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
