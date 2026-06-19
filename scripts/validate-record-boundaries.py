#!/usr/bin/env python3
"""Optional YAML frontmatter on *.md — only files with --- block are checked."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ALLOWED = frozenset({"core-truth", "operational", "transient", "archive/placeholders/evidence"})
REQUIRED = frozenset({"category", "intent", "last-reviewed"})
ROOT = Path(__file__).resolve().parent.parent
FM = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL | re.MULTILINE)


def parse_yamlish(blob: str) -> dict[str, str]:
    d: dict[str, str] = {}
    for line in blob.splitlines():
        if ":" not in line or line.strip().startswith("#"):
            continue
        k, _, rest = line.partition(":")
        d[k.strip()] = rest.strip().strip('"\'')
    return d


def read_markdown_utf8(path: Path) -> tuple[str | None, str | None]:
    try:
        return path.read_text(encoding="utf-8"), None
    except UnicodeDecodeError as exc:
        return None, f"not valid utf-8 ({exc})"
    except OSError as exc:
        return None, f"cannot read ({exc})"


def main() -> int:
    errors: list[str] = []
    for md in ROOT.rglob("*.md"):
        if "archive" in md.parts:
            continue
        if "node_modules" in md.parts:
            continue
        rel = md.relative_to(ROOT)
        text, read_error = read_markdown_utf8(md)
        if read_error:
            errors.append(f"{rel}: {read_error}")
            continue
        m = FM.match(text)
        if not m:
            continue
        data = parse_yamlish(m.group(1))
        cat = data.get("category")
        if cat not in ALLOWED:
            errors.append(f"{rel}: bad category {cat!r}")
        miss = sorted(REQUIRED - set(data.keys()))
        if miss:
            errors.append(f"{rel}: missing {miss}")
    if errors:
        print("\n".join(errors))
        return 1
    print("validate-record-boundaries: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
