#!/usr/bin/env python3
"""Validate optional SID embargo frontmatter on statecraft daily and memo files.

When publishing Situation Brief or synthesis on the same day as public copy,
``embargo`` must be set explicitly on governed surfaces.

Allowed values: ``public-ok`` | ``client-only`` | ``internal-only``

WORK only; not Record.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ROOTS = (
    REPO_ROOT / "statecraft" / "daily",
    REPO_ROOT / "statecraft" / "templates",
)

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
EMBARGO_VALUES = frozenset({"public-ok", "client-only", "internal-only"})
DAILY_SYNTHESIS_RE = re.compile(r"^\d{4}-\d{2}-\d{2}\.md$")
SID_MEMO_MARKER = "sid_deliverable:"


def parse_frontmatter(text: str) -> dict[str, str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip().strip('"').strip("'")
    return fields


def files_to_check(roots: list[Path], require_embargo: bool) -> list[Path]:
    paths: list[Path] = []
    for root in roots:
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*.md")):
            name = path.name
            if DAILY_SYNTHESIS_RE.match(name):
                paths.append(path)
                continue
            text_head = path.read_text(encoding="utf-8")[:800]
            if SID_MEMO_MARKER in text_head or "embargo:" in text_head:
                paths.append(path)
            elif require_embargo and "sid-transaction-memo" in name:
                paths.append(path)
    return paths


def validate_file(path: Path, strict: bool) -> list[str]:
    text = path.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    errors: list[str] = []

    if not fm:
        if strict and (SID_MEMO_MARKER in text or "embargo:" in text[:400]):
            errors.append("embargo block present but frontmatter malformed")
        elif strict and path.name.endswith("-wire-verify-matrix.md"):
            return []
        elif strict and DAILY_SYNTHESIS_RE.match(path.name):
            errors.append("daily synthesis missing frontmatter with embargo (strict mode)")
        return errors

    embargo = fm.get("embargo")
    if embargo is None:
        if strict:
            errors.append("missing embargo field in frontmatter")
        return errors

    if embargo not in EMBARGO_VALUES:
        errors.append(f"invalid embargo {embargo!r}; use {sorted(EMBARGO_VALUES)}")
    return errors


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        action="append",
        help="Directory to scan (repeatable; default: statecraft/daily + templates)",
    )
    parser.add_argument(
        "--path",
        type=Path,
        help="Validate a single file instead of scanning roots",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Require embargo frontmatter on daily synthesis files",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.path:
        targets = [args.path.resolve()]
    else:
        roots = [p.resolve() for p in (args.root or DEFAULT_ROOTS)]
        targets = files_to_check(roots, require_embargo=args.strict)

    failures = 0
    checked = 0
    for path in targets:
        if not path.is_file():
            print(f"skip missing: {path}", file=sys.stderr)
            continue
        checked += 1
        errors = validate_file(path, strict=args.strict or bool(args.path))
        if errors:
            failures += 1
            for err in errors:
                print(f"FAIL {path.relative_to(REPO_ROOT)}: {err}", file=sys.stderr)

    if checked == 0:
        print("no files matched embargo scan")
        return 0
    if failures:
        print(f"embargo check: {failures} file(s) failed of {checked}", file=sys.stderr)
        return 1
    print(f"embargo check: OK ({checked} file(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
