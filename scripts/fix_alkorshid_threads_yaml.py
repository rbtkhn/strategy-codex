#!/usr/bin/env python3
"""Fix duplicate threads blocks and normalize nima -> alkorshid in DW cluster YAML."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ARCHIVE = REPO / "source-archive" / "statecraft"
FM_RE = re.compile(r"\A(---\n.*?\n---\n)(.*)", re.DOTALL)


def normalize_frontmatter(fm: str) -> str:
    lines = fm.splitlines()
    out: list[str] = []
    seen_threads = False
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("threads:"):
            if seen_threads:
                i += 1
                while i < len(lines) and lines[i].startswith("  -"):
                    i += 1
                continue
            seen_threads = True
            items: list[str] = []
            i += 1
            while i < len(lines) and lines[i].startswith("  -"):
                val = lines[i].split("-", 1)[1].strip()
                if val == "nima":
                    val = "alkorshid"
                if val and val not in items:
                    items.append(val)
                i += 1
            if "alkorshid" not in items:
                items.insert(0, "alkorshid")
            out.append("threads:")
            for item in items:
                out.append(f"  - {item}")
            continue
        if line.startswith("thread:"):
            val = line.split(":", 1)[1].strip()
            if val == "nima":
                out.append("thread: alkorshid")
            else:
                out.append(line)
            i += 1
            continue
        out.append(line)
        i += 1
    return "\n".join(out) + "\n"


def patch_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8-sig")
    m = FM_RE.match(text)
    if not m:
        return False
    new_fm = normalize_frontmatter(m.group(1))
    new_text = new_fm + m.group(2)
    if new_text == text:
        return False
    path.write_text(new_text, encoding="utf-8")
    return True


def main() -> int:
    patterns = ("source-dialogue-works-*", "source-daniel-davis-alkorshid-*", "source-nawfal-alkorshid-*")
    n = 0
    for pat in patterns:
        for path in ARCHIVE.rglob(pat):
            if path.suffix == ".md" and patch_file(path):
                n += 1
    print(f"patched {n} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
