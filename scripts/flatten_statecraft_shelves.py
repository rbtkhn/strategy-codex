#!/usr/bin/env python3
"""Flatten stream/ and themes/ subfolders under statecraft/voices and statecraft/channels.

Usage:
    python scripts/flatten_statecraft_shelves.py --dry-run
    python scripts/flatten_statecraft_shelves.py --apply
    python scripts/flatten_statecraft_shelves.py --rewrite-links
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VOICES_DIR = REPO_ROOT / "statecraft" / "voices"
CHANNELS_DIR = REPO_ROOT / "statecraft" / "channels"
RECEIPT_PATH = REPO_ROOT / "runtime" / "artifacts" / "flat-shelf-migrate-receipt.json"

VOICES_META_DIRS = frozenset({"_scratch", "_templates", "map", "relations"})
NESTED_SHELF_DIRS = ("stream", "themes")

REWRITE_SCAN_DIRS = (
    "statecraft",
    "docs",
    ".cursor",
    "skills",
    "tests",
    "scripts",
    "codex",
    "LLM-ROUTING.md",
    "README.md",
    "AGENTS.md",
)
REWRITE_EXCLUDE_PREFIXES = (
    "runtime/artifacts/benchmarks/",
    ".cursor/plans/",
    "public/predictive-history/",
)

# Parent stub replaced by stream canonical body
PROMOTE_STREAM_OVER_PARENT = frozenset({"mercouris-arc.md"})


@dataclass(frozen=True)
class MovePlan:
    src: Path
    dest: Path
    action: str  # move | delete_stub | skip


def _rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT)).replace("\\", "/")


def _speaker_slug(shelf_root: Path) -> str:
    return shelf_root.name


def _target_name(shelf_root: Path, subdir: str, src: Path) -> tuple[str, str]:
    """Return (dest_basename, action_note)."""
    slug = _speaker_slug(shelf_root)
    name = src.name

    if subdir == "stream" and name == "README.md":
        return f"{slug}-monthly-shelves.md", "stream README -> monthly-shelves"
    if subdir == "themes" and name == "README.md":
        return f"{slug}-themes.md", "themes README -> themes index"
    return name, "direct"


def collect_moves_for_shelf(shelf_root: Path) -> list[MovePlan]:
    plans: list[MovePlan] = []
    for subdir in NESTED_SHELF_DIRS:
        nested = shelf_root / subdir
        if not nested.is_dir():
            continue
        for src in sorted(nested.rglob("*")):
            if not src.is_file():
                continue
            dest_name, _ = _target_name(shelf_root, subdir, src)
            dest = shelf_root / dest_name
            if dest_name in PROMOTE_STREAM_OVER_PARENT and (shelf_root / dest_name).is_file():
                plans.append(MovePlan(shelf_root / dest_name, dest, "delete_stub"))
            if dest.exists() and dest.resolve() != src.resolve():
                if dest_name in PROMOTE_STREAM_OVER_PARENT:
                    pass  # stub removed above
                else:
                    print(
                        f"collision: {_rel(src)} -> {_rel(dest)} (dest exists)",
                        file=sys.stderr,
                    )
                    sys.exit(1)
            plans.append(MovePlan(src, dest, "move"))
    return plans


def collect_all_moves() -> list[MovePlan]:
    plans: list[MovePlan] = []
    if VOICES_DIR.is_dir():
        for shelf in sorted(VOICES_DIR.iterdir()):
            if not shelf.is_dir() or shelf.name in VOICES_META_DIRS:
                continue
            plans.extend(collect_moves_for_shelf(shelf))
    if CHANNELS_DIR.is_dir():
        for shelf in sorted(CHANNELS_DIR.iterdir()):
            if not shelf.is_dir():
                continue
            plans.extend(collect_moves_for_shelf(shelf))
    return plans


def fix_relative_depth_in_moved_files(receipt: list[dict[str, str]]) -> int:
    """Remove one ../ prefix from relative markdown links in files moved out of stream/."""
    paths = {entry["to"] for entry in receipt if entry.get("action") == "move"}
    fixed = 0
    for rel in sorted(paths):
        path = REPO_ROOT / rel
        if not path.is_file() or path.suffix not in {".md", ".yaml", ".yml"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = path.read_text(encoding="utf-8", errors="replace")
        new_text = re.sub(
            r"\((\.\./[^)]+)\)",
            lambda m: "(" + m.group(1)[3:] + ")"
            if m.group(1).startswith("../")
            else m.group(0),
            text,
        )
        if new_text != text:
            path.write_text(new_text, encoding="utf-8", newline="\n")
            fixed += 1
    return fixed


def apply_moves(plans: list[MovePlan]) -> None:
    receipt: list[dict[str, str]] = []
    deleted: set[Path] = set()
    for plan in plans:
        if plan.action == "delete_stub" and plan.src not in deleted:
            print(f"rm stub {_rel(plan.src)}")
            plan.src.unlink()
            deleted.add(plan.src)
            receipt.append({"action": "delete_stub", "path": _rel(plan.src)})
        if plan.action != "move":
            continue
        if plan.src.resolve() == plan.dest.resolve():
            continue
        print(f"mv {_rel(plan.src)} -> {_rel(plan.dest)}")
        plan.dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(plan.src), str(plan.dest))
        receipt.append({"action": "move", "from": _rel(plan.src), "to": _rel(plan.dest)})

    for shelf in list(VOICES_DIR.iterdir()) + list(CHANNELS_DIR.iterdir()):
        if not shelf.is_dir():
            continue
        for subdir in NESTED_SHELF_DIRS:
            nested = shelf / subdir
            if nested.is_dir() and not any(nested.rglob("*")):
                print(f"rmdir {_rel(nested)}")
                nested.rmdir()
            elif nested.is_dir():
                remaining = list(nested.rglob("*"))
                if remaining:
                    print(f"warn: non-empty after move: {_rel(nested)} ({len(remaining)} items)", file=sys.stderr)

    RECEIPT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT_PATH.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(f"receipt: {_rel(RECEIPT_PATH)} ({len(receipt)} entries)")
    n = fix_relative_depth_in_moved_files(receipt)
    print(f"fixed relative link depth in {n} moved files")


def should_rewrite(path: Path) -> bool:
    rel = _rel(path)
    for prefix in REWRITE_EXCLUDE_PREFIXES:
        if rel.startswith(prefix) or f"/{prefix}" in rel:
            return False
    if path.suffix not in {".md", ".mdc", ".py", ".yaml", ".yml", ".json", ".toml"}:
        return False
    return True


def rewrite_text(text: str) -> tuple[str, int]:
    """Return (new_text, change_count)."""
    original = text
    n = 0

    def subn(pattern: str, repl: str, s: str) -> str:
        nonlocal n
        s2, count = re.subn(pattern, repl, s)
        n += count
        return s2

    # Absolute repo paths (forward and backslash)
    text = subn(
        r"statecraft/voices/([a-z0-9-]+)/stream/",
        r"statecraft/voices/\1/",
        text,
    )
    text = subn(
        r"statecraft/voices/([a-z0-9-]+)/themes/",
        r"statecraft/voices/\1/",
        text,
    )
    text = subn(
        r"statecraft\\voices\\([a-z0-9-]+)\\stream\\",
        r"statecraft/voices/\1/",
        text,
    )
    text = subn(
        r"statecraft\\voices\\([a-z0-9-]+)\\themes\\",
        r"statecraft/voices/\1/",
        text,
    )
    text = subn(
        r"statecraft/channels/([a-z0-9-]+)/stream/",
        r"statecraft/channels/\1/",
        text,
    )
    text = subn(
        r"statecraft\\channels\\([a-z0-9-]+)\\stream\\",
        r"statecraft/channels/\1/",
        text,
    )

    # Windows absolute paths embedded in markdown
    text = subn(
        r"([A-Za-z]:[/\\]dev[/\\]strategy-codex[/\\])statecraft[/\\]voices[/\\]([a-z0-9-]+)[/\\]stream[/\\]",
        r"\1statecraft/voices/\2/",
        text,
    )
    text = subn(
        r"([A-Za-z]:[/\\][^)\s]+[/\\]strategy-codex[/\\])statecraft[/\\]voices[/\\]([a-z0-9-]+)[/\\]stream[/\\]",
        r"\1statecraft/voices/\2/",
        text,
    )
    text = subn(
        r"([A-Za-z]:[/\\]dev[/\\]strategy-codex[/\\])statecraft[/\\]channels[/\\]([a-z0-9-]+)[/\\]stream[/\\]",
        r"\1statecraft/channels/\2/",
        text,
    )

    # Shorthand channel aliases used in cross-shelf relative links
    text = subn(r"\.\./\.\./davis/", "../../channels/daniel-davis/", text)
    text = subn(r"\.\./davis/", "../../channels/daniel-davis/", text)
    text = subn(r"\.\./\.\./nima/", "../../channels/dialogue-works/", text)
    text = subn(r"\.\./nima/", "../../channels/dialogue-works/", text)
    text = subn(r"\.\./\.\./napolitano/", "../../channels/judging-freedom/", text)
    text = subn(r"\.\./napolitano/", "../../channels/judging-freedom/", text)
    text = subn(r"\.\./\.\./channels/([a-z0-9-]+)/stream/", r"../../channels/\1/", text)
    text = subn(r"\.\./channels/([a-z0-9-]+)/stream/", r"../channels/\1/", text)

    # Any remaining speaker/channel segment before stream/
    text = subn(r"/([a-z0-9-]+)/stream/", r"/\1/", text)
    text = subn(r"\\([a-z0-9-]+)\\stream\\", r"/\1/", text)

    # Relative markdown links: stream/foo -> foo, ../stream/ -> sibling at shelf root
    text = subn(r"\(\s*stream/", "(", text)
    text = subn(r"\(\s*\./stream/", "(", text)
    text = subn(r"\(\s*\.\./stream/", "(", text)
    text = subn(r"\(\s*\.\./\.\./stream/", "(../../", text)
    text = subn(r"\(\s*\.\./\.\./\.\./stream/", "(../../../", text)
    text = subn(r"\(\s*\.\./\.\./\.\./\.\./stream/", "(../../../../", text)
    text = subn(r"\(\s*themes/", "(", text)
    text = subn(r"\(\s*\./themes/", "(", text)
    text = subn(r"\(\s*\.\./themes/", "(", text)

    # Monthly-shelves / themes README renames in links
    for slug in (
        "ritter",
        "crooke",
        "mercouris",
        "freeman",
        "johnson",
        "macgregor",
        "marandi",
        "mearsheimer",
        "parsi",
    ):
        text = subn(
            rf"({slug}/)stream/README\.md",
            rf"\1{slug}-monthly-shelves.md",
            text,
        )
        text = subn(
            rf"({slug}/)themes/README\.md",
            rf"\1{slug}-themes.md",
            text,
        )
        text = subn(
            rf"\(({slug}/)stream/README\.md\)",
            rf"(\1{slug}-monthly-shelves.md)",
            text,
        )
        text = subn(
            rf"\(({slug}/)themes/README\.md\)",
            rf"(\1{slug}-themes.md)",
            text,
        )

    if text != original:
        return text, max(1, n)
    return text, 0


def rewrite_links() -> int:
    changed_files = 0
    targets: list[Path] = []
    for item in REWRITE_SCAN_DIRS:
        p = REPO_ROOT / item
        if p.is_file():
            targets.append(p)
        elif p.is_dir():
            targets.extend(p.rglob("*"))

    seen: set[Path] = set()
    for path in sorted(targets):
        if not path.is_file() or path in seen or not should_rewrite(path):
            continue
        seen.add(path)
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        new_text, n = rewrite_text(text)
        if n and new_text != text:
            path.write_text(new_text, encoding="utf-8", newline="\n")
            print(f"rewrite {_rel(path)}")
            changed_files += 1
    return changed_files


def dry_run(plans: list[MovePlan]) -> None:
    for plan in plans:
        if plan.action == "delete_stub":
            print(f"DELETE STUB {_rel(plan.src)}")
        elif plan.action == "move":
            print(f"MOVE {_rel(plan.src)} -> {_rel(plan.dest)}")
    print(f"total plans: {len(plans)}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--rewrite-links", action="store_true")
    args = parser.parse_args()

    if not any((args.dry_run, args.apply, args.rewrite_links)):
        parser.error("specify --dry-run, --apply, and/or --rewrite-links")

    if args.dry_run or args.apply:
        plans = collect_all_moves()
        if args.dry_run:
            dry_run(plans)
        if args.apply:
            apply_moves(plans)

    if args.rewrite_links:
        n = rewrite_links()
        print(f"rewrote {n} files")

    return 0


if __name__ == "__main__":
    sys.exit(main())
