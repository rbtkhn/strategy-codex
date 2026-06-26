#!/usr/bin/env python3
"""Bulk-normalize solo hub show labels (WORK only).

For `source-alexander-mercouris-*` with `channel_slug` not `the-duran` and
`show: Mercouris`, set `show: Alexander Mercouris`.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ARCHIVE_ROOT = REPO_ROOT / "source-archive" / "statecraft"
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
SHOW_RE = re.compile(
    r"^(show:\s*)(?:Mercouris|\"Mercouris\"|'Mercouris')\s*$",
    re.M,
)


def parse_scalar(block: str, key: str) -> str | None:
    m = re.search(rf"^{re.escape(key)}:\s*(.+)$", block, re.M)
    if not m:
        return None
    val = m.group(1).strip().strip('"').strip("'")
    return val or None


def collect_targets(root: Path) -> list[Path]:
    targets: list[Path] = []
    for path in sorted(root.rglob("source-alexander-mercouris-*.md")):
        text = path.read_text(encoding="utf-8")
        m = FRONTMATTER_RE.match(text)
        if not m:
            continue
        block = m.group(1)
        if parse_scalar(block, "show") != "Mercouris":
            continue
        slug = (parse_scalar(block, "channel_slug") or "alexander-mercouris").lower()
        if slug == "the-duran":
            continue
        targets.append(path)
    return targets


def apply_show(path: Path, dry_run: bool) -> bool:
    text = path.read_text(encoding="utf-8")
    new_text, n = SHOW_RE.subn(r"\1Alexander Mercouris", text, count=1)
    if n != 1 or new_text == text:
        return False
    if not dry_run:
        path.write_text(new_text, encoding="utf-8", newline="\n")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    if args.apply == args.dry_run:
        parser.error("Specify exactly one of --dry-run or --apply")

    targets = collect_targets(ARCHIVE_ROOT)
    changed = 0
    for path in targets:
        if apply_show(path, dry_run=args.dry_run):
            changed += 1
            rel = path.relative_to(REPO_ROOT)
            print(f"{'would_patch' if args.dry_run else 'patched'} {rel}")
    print(f"total={changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
