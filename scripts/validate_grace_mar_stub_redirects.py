#!/usr/bin/env python3
"""Validate Grace-Mar quarantine stubs: YAML moved_to resolves and body is short."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DOCS = REPO / "docs"
MAX_STUB_LINES = 15
MOVED_RE = re.compile(r"^moved_to:\s*(.+)$", re.MULTILINE)
ARCHIVED_RE = re.compile(r"^archived:\s*true\s*$", re.MULTILINE)


def parse_stub(path: Path) -> tuple[bool, str | None]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return False, None
    end = text.find("---", 3)
    if end == -1:
        return False, None
    front = text[3:end]
    if not ARCHIVED_RE.search(front):
        return False, None
    m = MOVED_RE.search(front)
    if not m:
        return False, None
    return True, m.group(1).strip()


def main() -> int:
    errors: list[str] = []
    checked = 0
    for path in sorted(DOCS.glob("*.md")):
        is_stub, moved_to = parse_stub(path)
        if not is_stub:
            continue
        checked += 1
        line_count = len(path.read_text(encoding="utf-8").splitlines())
        if line_count > MAX_STUB_LINES:
            errors.append(f"{path.relative_to(REPO)}: stub has {line_count} lines (max {MAX_STUB_LINES})")
        dest = REPO / moved_to.replace("/", "\\") if sys.platform == "win32" else REPO / moved_to
        if not dest.is_file():
            errors.append(f"{path.relative_to(REPO)}: moved_to missing: {moved_to}")

    if checked == 0:
        print("warn: no archived stubs found under docs/", file=sys.stderr)

    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1

    print(f"ok: {checked} stub(s) validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
