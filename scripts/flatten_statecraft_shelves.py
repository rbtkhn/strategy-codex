#!/usr/bin/env python3
"""Flatten stream/ and themes/ subfolders under statecraft/voices and statecraft/channels.

Usage:
    python scripts/flatten_statecraft_shelves.py --dry-run
    python scripts/flatten_statecraft_shelves.py --apply
    python scripts/flatten_statecraft_shelves.py --rewrite-links
    python scripts/flatten_statecraft_shelves.py --rewrite-visible-labels [--dry-run]
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
NOTES_DIR = REPO_ROOT / "statecraft" / "notes"
RECEIPT_PATH = REPO_ROOT / "runtime" / "artifacts" / "flat-shelf-migrate-receipt.json"
VISIBLE_LABELS_RECEIPT = (
    REPO_ROOT / "runtime" / "artifacts" / "flat-shelf-visible-labels-receipt.json"
)

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
PROMOTE_STREAM_OVER_PARENT = frozenset({"arc-mercouris-continuity.md"})

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

def _notes_arc_names() -> frozenset[str]:
    if not NOTES_DIR.is_dir():
        return frozenset()
    return frozenset(p.name for p in NOTES_DIR.glob("arc-*.md"))

def _arc_stub_map(shelf_root: Path) -> dict[str, str]:
    """Map canonical arc basename -> local compat stub basename."""
    mapping: dict[str, str] = {}
    for path in shelf_root.glob("*-arc.md"):
        try:
            head = path.read_text(encoding="utf-8", errors="ignore")[:400]
        except OSError:
            continue
        m = re.search(r"^#\s+(arc-[^\s(]+)", head, re.MULTILINE)
        if m:
            mapping[f"{m.group(1)}.md"] = path.name
    return mapping

def _resolve_broken_href(shelf_root: Path, href: str, notes_arcs: frozenset[str]) -> str:
    """Fix href when target file missing at shelf root."""
    if not href or href.startswith(("http://", "https://", "#", "/")):
        return href
    if "://" in href or href.startswith("mailto:"):
        return href
    # Strip anchor
    base, _, anchor = href.partition("#")
    if (shelf_root / base).is_file():
        return href

    stub_map = _arc_stub_map(shelf_root)
    if base in stub_map and (shelf_root / stub_map[base]).is_file():
        resolved = stub_map[base]
        return f"{resolved}#{anchor}" if anchor else resolved

    if base in notes_arcs:
        resolved = f"../../notes/{base}"
        return f"{resolved}#{anchor}" if anchor else resolved

    slug = shelf_root.name
    # Flatten rename: stream/README -> {slug}-monthly-shelves.md
    if base == "README.md":
        monthly = f"{slug}-monthly-shelves.md"
        if (shelf_root / monthly).is_file():
            return f"{monthly}#{anchor}" if anchor else monthly
        themes = f"{slug}-themes.md"
        if (shelf_root / themes).is_file():
            return f"{themes}#{anchor}" if anchor else themes

    # arc-{slug}-continuity-threads.md -> {slug}-arc-threads.md
    alt = f"{slug}-arc-threads.md"
    if base.startswith("arc-") and base.endswith("-threads.md") and (shelf_root / alt).is_file():
        return f"{alt}#{anchor}" if anchor else alt

    return href

def rewrite_visible_labels_in_text(text: str, shelf_root: Path, notes_arcs: frozenset[str]) -> tuple[str, int]:
    """Fix stale stream/themes link labels and broken hrefs in one shelf markdown file."""
    slug = shelf_root.name
    changes = 0
    monthly = f"{slug}-monthly-shelves.md"
    themes = f"{slug}-themes.md"

    def repl_stream_label(m: re.Match[str]) -> str:
        nonlocal changes
        inner = m.group(1)
        href = m.group(2)
        new_href = _resolve_broken_href(shelf_root, href, notes_arcs)
        if new_href != href:
            changes += 1
        changes += 1
        return f"[{inner}]({new_href})"

    # [stream/foo](href) -> [foo](href)
    text, n = re.subn(r"\[stream/([^\]]+)\]\(([^)]+)\)", repl_stream_label, text)
    changes += n

    def repl_themes_label(m: re.Match[str]) -> str:
        nonlocal changes
        inner = m.group(1)
        href = m.group(2)
        if inner == "README.md" and (shelf_root / themes).is_file():
            changes += 1
            return f"[{themes}]({themes})"
        new_href = _resolve_broken_href(shelf_root, href, notes_arcs)
        if new_href != href:
            changes += 1
        changes += 1
        return f"[{inner}]({new_href})"

    text, n = re.subn(r"\[themes/([^\]]+)\]\(([^)]+)\)", repl_themes_label, text)
    changes += n

    # [stream/README.md](...) -> monthly-shelves
    if (shelf_root / monthly).is_file():

        def repl_stream_readme(m: re.Match[str]) -> str:
            nonlocal changes
            changes += 1
            return f"[{monthly}]({monthly})"

        text, n = re.subn(
            r"\[stream/README\.md\]\([^)]+\)",
            repl_stream_readme,
            text,
        )
        changes += n

    # [themes/README.md](README.md) or any href
    if (shelf_root / themes).is_file():

        def repl_themes_readme(m: re.Match[str]) -> str:
            nonlocal changes
            changes += 1
            return f"[{themes}]({themes})"

        text, n = re.subn(
            r"\[themes/README\.md\]\([^)]+\)",
            repl_themes_readme,
            text,
        )
        changes += n

    # Prose historical-themes links pointing at speaker README
    if (shelf_root / themes).is_file():

        def repl_historical_themes(m: re.Match[str]) -> str:
            nonlocal changes
            changes += 1
            return f"{m.group(1)}[{m.group(2)}]({themes})"

        text, n = re.subn(
            r"(?i)(\[)([^\]]*(?:historical themes|theme)[^\]]*)\]\(README\.md\)",
            repl_historical_themes,
            text,
        )
        changes += n

    # Remaining arc hrefs without stream/ prefix
    def repl_md_link(m: re.Match[str]) -> str:
        nonlocal changes
        label = m.group(1)
        href = m.group(2)
        if label.startswith(("stream/", "themes/")):
            return m.group(0)
        new_href = _resolve_broken_href(shelf_root, href, notes_arcs)
        if new_href == href:
            return m.group(0)
        changes += 1
        return f"[{label}]({new_href})"

    text, n = re.subn(r"\[([^\]]+\.md)\]\(([^)]+\.md)\)", repl_md_link, text)
    changes += n

    # Prose monthly-shelf links that still point README at itself
    if (shelf_root / monthly).is_file():

        def repl_readme_monthly(m: re.Match[str]) -> str:
            nonlocal changes
            changes += 1
            return f"[{monthly}]({monthly})"

        text, n = re.subn(
            r"\[README\.md\]\(README\.md\)"
            r"(?=[^\n]*(?:monthly|month ladder|month-level|bounded monthly|month synthesis))",
            repl_readme_monthly,
            text,
            flags=re.IGNORECASE,
        )
        changes += n

    # Broken empty stream/ placeholders from prior link rewrite
    if (shelf_root / monthly).is_file():

        def repl_empty_stream(m: re.Match[str]) -> str:
            nonlocal changes
            changes += 1
            return f"[{monthly}]({monthly})"

        text, n = re.subn(r"\[stream/\]\(\)", repl_empty_stream, text)
        changes += n

    # stream/ label with absolute or relative path in href (channels)
    text, n = re.subn(
        r"\[stream/\]\(([^)]+)\)",
        lambda m: f"[{shelf_root.name} shelf]({m.group(1)})",
        text,
    )
    if n:
        changes += n

    return text, changes

def rewrite_visible_labels(*, dry_run: bool = False) -> int:
    notes_arcs = _notes_arc_names()
    changed_files = 0
    receipt: list[dict[str, str | int]] = []

    for base, meta in ((VOICES_DIR, VOICES_META_DIRS), (CHANNELS_DIR, frozenset())):
        if not base.is_dir():
            continue
        for shelf in sorted(base.iterdir()):
            if not shelf.is_dir() or shelf.name in meta:
                continue
            for path in sorted(shelf.glob("*.md")):
                try:
                    text = path.read_text(encoding="utf-8")
                except (UnicodeDecodeError, OSError):
                    continue
                new_text, n = rewrite_visible_labels_in_text(text, shelf, notes_arcs)
                if n and new_text != text:
                    rel = _rel(path)
                    receipt.append({"path": rel, "changes": n})
                    if dry_run:
                        print(f"would rewrite {rel} ({n} edits)")
                    else:
                        path.write_text(new_text, encoding="utf-8", newline="\n")
                        print(f"rewrite {rel} ({n} edits)")
                    changed_files += 1

    if not dry_run:
        VISIBLE_LABELS_RECEIPT.parent.mkdir(parents=True, exist_ok=True)
        VISIBLE_LABELS_RECEIPT.write_text(
            json.dumps(receipt, indent=2) + "\n", encoding="utf-8"
        )
        print(f"receipt: {_rel(VISIBLE_LABELS_RECEIPT)} ({len(receipt)} files)")
    else:
        print(f"dry-run: {changed_files} file(s) would change")
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
    parser.add_argument("--rewrite-visible-labels", action="store_true")
    parser.add_argument(
        "--dry-run-labels",
        action="store_true",
        help="with --rewrite-visible-labels, print only",
    )
    args = parser.parse_args()

    if not any(
        (args.dry_run, args.apply, args.rewrite_links, args.rewrite_visible_labels)
    ):
        parser.error(
            "specify --dry-run, --apply, --rewrite-links, and/or --rewrite-visible-labels"
        )

    if args.dry_run or args.apply:
        plans = collect_all_moves()
        if args.dry_run:
            dry_run(plans)
        if args.apply:
            apply_moves(plans)

    if args.rewrite_links:
        n = rewrite_links()
        print(f"rewrote {n} files")

    if args.rewrite_visible_labels:
        n = rewrite_visible_labels(dry_run=args.dry_run_labels)
        print(f"visible-label pass: {n} file(s)")

    return 0

if __name__ == "__main__":
    sys.exit(main())
