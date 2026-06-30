#!/usr/bin/env python3
"""Link sweep: source-alkorshid / source-nima-alkorshid -> source-dialogue-works paths."""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

SCAN_ROOTS = [
    REPO / "statecraft",
    REPO / "skills",
    REPO / "codex",
    REPO / ".cursor",
]

# Map old basename prefix to new (same guest slug tail).
OLD_PREFIXES = (
    "source-alkorshid-",
    "source-nima-alkorshid-",
)

def new_path_for_old(old_fragment: str) -> str | None:
    for prefix in OLD_PREFIXES:
        if prefix in old_fragment:
            return old_fragment.replace(prefix, "source-dialogue-works-", 1)
    # dialogue-works mis-file -> daniel-davis (2026-05-29 known)
    if "source-dialogue-works-iran-war-never-stops-while-israel-attacks-lebanon-nima-alkhorshid-lt-col-daniel-davis-2026-05-29" in old_fragment:
        return old_fragment.replace(
            "source-dialogue-works-iran-war-never-stops-while-israel-attacks-lebanon-nima-alkhorshid-lt-col-daniel-davis-2026-05-29",
            "source-daniel-davis-alkorshid-iran-war-never-stops-while-israel-attacks-lebanon-nima-alkhorshid-lt-col-daniel-davis",
        )
    return None

def sweep_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="replace")
    new = text
    for prefix in OLD_PREFIXES:
        if prefix not in new:
            continue
        for m in re.finditer(re.escape(prefix) + r"[^\s\)`\"']+", new):
            old = m.group(0)
            repl = new_path_for_old(old)
            if repl:
                new = new.replace(old, repl)
    # known davis rename
    old_davis = "source-dialogue-works-iran-war-never-stops-while-israel-attacks-lebanon-nima-alkhorshid-lt-col-daniel-davis-2026-05-29"
    new_davis = "source-daniel-davis-alkorshid-iran-war-never-stops-while-israel-attacks-lebanon-nima-alkhorshid-lt-col-daniel-davis-2026-05-29"
    new = new.replace(old_davis, new_davis)
    if new == text:
        return False
    path.write_text(new, encoding="utf-8")
    return True

def main() -> None:
    n = 0
    for root in SCAN_ROOTS:
        if not root.exists():
            continue
        for path in root.rglob("*.md"):
            if sweep_file(path):
                n += 1
                print(path.relative_to(REPO))
    print(f"updated {n} files")

if __name__ == "__main__":
    main()
