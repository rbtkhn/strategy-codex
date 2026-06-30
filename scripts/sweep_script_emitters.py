#!/usr/bin/env python3
"""Remove deprecated WORK/Record banner strings from script emitters."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"

REPLACEMENTS: tuple[tuple[str, str], ...] = (
    ('"WORK only; not Record.",\n', ""),
    ("'WORK only; not Record.',\n", ""),
    ('"WORK only; not Record.\\n\\n"\n', ""),
    ('"""WORK only; not Record.\n\n', '"""\n\n'),
    ('HEADER = """WORK only; not Record.\n\n', 'HEADER = """\n\n'),
    ('COMPAT_TEMPLATE = """WORK only; not Record.\n\n', 'COMPAT_TEMPLATE = """\n\n'),
    ('WORK_BOUNDARY = "WORK only; not Record."\n', 'WORK_BOUNDARY = ""\n'),
    ('lines.append("WORK only; not Record.")\n', ""),
    (
        '"# Sibling term page (template stub)\\n\\nWORK only; not Record.\\n",\n',
        '"# Sibling term page (template stub)\\n\\n",\n',
    ),
)


def main() -> int:
    changed = 0
    for path in sorted(SCRIPTS.glob("*.py")):
        if path.name == "check_work_record_doctrine.py":
            continue
        text = path.read_text(encoding="utf-8")
        original = text
        for old, new in REPLACEMENTS:
            text = text.replace(old, new)
        if text != original:
            path.write_text(text, encoding="utf-8", newline="\n")
            changed += 1
            print(f"[apply] {path.relative_to(REPO_ROOT).as_posix()}")
    print(f"sweep_script_emitters: changed={changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
