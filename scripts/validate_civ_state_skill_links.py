#!/usr/bin/env python3
"""Verify public/civ-state markdown links in civ-state CURSOR_APPENDIX resolve."""

from __future__ import annotations

import re
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent
_APPENDIX = _REPO / ".cursor" / "skills" / "civ-state" / "CURSOR_APPENDIX.md"
_PUBLIC = _REPO / "public" / "civ-state"

def _extract_public_links(text: str) -> list[str]:
    pattern = re.compile(r"\]\(([^)]+)\)")
    links: list[str] = []
    for raw in pattern.findall(text):
        if "public/civ-state" not in raw.replace("\\", "/"):
            continue
        clean = raw.split("#")[0].strip()
        if not clean:
            continue
        links.append(clean.replace("\\", "/"))
    return links

def main() -> int:
    if not _APPENDIX.is_file():
        print(f"Missing {_APPENDIX}", file=sys.stderr)
        return 1
    text = _APPENDIX.read_text(encoding="utf-8")
    errors: list[str] = []
    for link in _extract_public_links(text):
        # Resolve relative to appendix dir
        target = (_APPENDIX.parent / link).resolve()
        try:
            target.relative_to(_PUBLIC.resolve())
        except ValueError:
            errors.append(f"link escapes public/civ-state: {link}")
            continue
        if not target.exists():
            errors.append(f"missing: {link}")
    if errors:
        for err in errors:
            print(err, file=sys.stderr)
        return 1
    print("validate_civ_state_skill_links: OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
