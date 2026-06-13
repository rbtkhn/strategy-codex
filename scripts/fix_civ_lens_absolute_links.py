#!/usr/bin/env python3
"""Replace absolute /C:/dev/strategy-codex/ markdown links with repo-relative paths."""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ROOT = REPO_ROOT / "statecraft" / "voices"

ABS_PREFIX = re.compile(
    r"/C:/dev/strategy-codex/(?P<rest>[^\s\)\>\"']+)",
    re.IGNORECASE,
)


def relative_repo_path(from_file: Path, target_under_root: str) -> str:
    """Return markdown-safe relative path from from_file to repo-root target."""
    from_dir = from_file.parent.resolve()
    target = (REPO_ROOT / target_under_root.replace("\\", "/")).resolve()
    return os.path.relpath(target, from_dir).replace("\\", "/")


def fix_content(text: str, file_path: Path) -> tuple[str, int]:
    count = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal count
        rest = match.group("rest")
        trailing = ""
        while rest and rest[-1] in ".,;":
            trailing = rest[-1] + trailing
            rest = rest[:-1]
        rel = relative_repo_path(file_path, rest)
        count += 1
        return rel + trailing

    return ABS_PREFIX.sub(repl, text), count


def iter_markdown_files(root: Path) -> list[Path]:
    if root.is_file():
        return [root] if root.suffix.lower() == ".md" else []
    return sorted(root.rglob("*.md"))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--paths",
        nargs="*",
        type=Path,
        default=[DEFAULT_ROOT],
        help="Files or directories to scan (default: statecraft/voices)",
    )
    ap.add_argument(
        "--apply",
        action="store_true",
        help="Write changes (default: dry-run report only)",
    )
    args = ap.parse_args()

    files: list[Path] = []
    for p in args.paths:
        p = p if p.is_absolute() else REPO_ROOT / p
        files.extend(iter_markdown_files(p))

    total = 0
    changed_files = 0
    for fp in files:
        try:
            text = fp.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            print(f"skip (encoding): {fp.relative_to(REPO_ROOT)}", file=sys.stderr)
            continue
        new_text, n = fix_content(text, fp)
        if n:
            total += n
            changed_files += 1
            rel = fp.relative_to(REPO_ROOT)
            mode = "apply" if args.apply else "dry-run"
            print(f"{mode}: {rel} ({n} link(s))")
            if args.apply:
                fp.write_text(new_text, encoding="utf-8")

    print(f"done: {total} replacement(s) in {changed_files} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
