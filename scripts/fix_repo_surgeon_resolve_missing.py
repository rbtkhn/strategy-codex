#!/usr/bin/env python3
"""Resolve broken markdown links when target basename is unique in the repo."""

from __future__ import annotations

import argparse
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from validate_structured_files import (  # noqa: E402
    collect_markdown_paths,
    iter_markdown_links,
    validate_markdown_links,
)

INLINE_LINK_RE = re.compile(r"(\[[^\]]*\]\()([^)]+)(\))")
SKIP_SUFFIXES = {".md", ".png", ".yaml", ".yml", ".json", ".pdf"}


def build_basename_index() -> dict[str, list[Path]]:
    index: dict[str, list[Path]] = defaultdict(list)
    for path in REPO_ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in SKIP_SUFFIXES:
            continue
        if any(part in {".git", ".venv", "node_modules"} for part in path.parts):
            continue
        index[path.name].append(path)
    return index


def pick_candidate(source: Path, basename: str, candidates: list[Path]) -> Path | None:
    if not candidates:
        return None
    if len(candidates) == 1:
        return candidates[0]

    def score(path: Path) -> int:
        rel = path.relative_to(REPO_ROOT).as_posix()
        value = 0
        if rel.startswith("source-archive/statecraft/"):
            value += 5
        if rel.startswith("statecraft/voices/"):
            value += 4
        if rel.startswith("codex/"):
            value += 3
        if rel.startswith("docs/skill-work/"):
            value += 2
        try:
            if source.relative_to(REPO_ROOT).parts[0] == path.relative_to(REPO_ROOT).parts[0]:
                value += 1
        except ValueError:
            pass
        return value

    ranked = sorted(((score(p), p) for p in candidates), reverse=True)
    if ranked[0][0] == 0:
        return None
    if len(ranked) == 1 or ranked[0][0] > ranked[1][0]:
        return ranked[0][1]
    return None


def replace_link_in_file(path: Path, old_target: str, new_target: str) -> bool:
    text = path.read_text(encoding="utf-8")
    needle = f"]({old_target})"
    repl = f"]({new_target})"
    if needle not in text:
        return False
    path.write_text(text.replace(needle, repl), encoding="utf-8", newline="\n")
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--scope", default="all", choices=("docs", "statecraft", "skills", "all"))
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    paths = [p for p in collect_markdown_paths(REPO_ROOT, args.scope) if p.suffix == ".md"]
    errors = validate_markdown_links(paths, REPO_ROOT)
    basename_index = build_basename_index()

    fixed = 0
    skipped = 0
    for err in errors:
        if ":->" not in err:
            continue
        left, detail = err.split(":->", 1)
        if ":" not in left:
            continue
        file_part, raw = left.rsplit(":", 1)
        source = (REPO_ROOT / file_part).resolve()
        if not source.is_file():
            continue
        target_part = raw.split("#", 1)[0].strip()
        frag = ""
        if "#" in raw:
            frag = "#" + raw.split("#", 1)[1]
        basename = Path(target_part.replace("\\", "/")).name
        if not basename:
            skipped += 1
            continue
        candidates = basename_index.get(basename, [])
        chosen = pick_candidate(source, basename, candidates)
        if chosen is None:
            skipped += 1
            continue
        new_rel = os.path.relpath(chosen, source.parent).replace("\\", "/") + frag
        if new_rel == raw.strip().lstrip("<").rstrip(">"):
            skipped += 1
            continue
        if args.apply:
            if replace_link_in_file(source, raw, new_rel):
                fixed += 1
                print(f"fixed: {file_part} {raw} -> {new_rel}")
        else:
            print(f"dry-run: {file_part} {raw} -> {new_rel}")
            fixed += 1

    print(f"done: {fixed} resolved, {skipped} skipped, {len(errors)} errors scanned")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
