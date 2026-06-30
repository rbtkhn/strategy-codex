#!/usr/bin/env python3
"""Backfill statecraft archive filenames to match channel_slug (non-authoritative).

Renames:
  source-napolitano-*     -> source-judging-freedom-*   (channel_slug: judging-freedom)
  source-nawfal-*         -> source-mario-nawfal-*      (channel_slug: mario-nawfal)
  source-{guest}-carlson-* -> source-tucker-carlson-{guest}-* (channel_slug: tucker-carlson)
  source-alex-mercouris-* -> source-alexander-mercouris-* (Mercouris solo channel)
  source-mercouris-*      -> source-alexander-mercouris-* (solo hub only; skips panels/guest lanes)
  source-mercouris-*      -> source-duran-mercouris-*     (The Duran channel; channel_slug/show)
  source-alex-mercouris-*  -> source-duran-mercouris-*     (when channel_slug: the-duran)

Then rewrites repo references (basename swap) and optionally rebuilds indices.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ARCHIVE_ROOT = REPO_ROOT / "source-archive" / "statecraft"
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
GUEST_CARLSON_RE = re.compile(r"^source-([a-z0-9][a-z0-9-]*)-carlson-(.+)$", re.I)
JUDGING_FREEDOM_SLUGS = {
    "judging-freedom",
    "napolitano",
    "judge-napolitano-judging-freedom",
    "",
}
MARIO_NAWFAL_SLUGS = {"mario-nawfal", "nawfal", ""}
MERCOURIS_CHANNEL_SLUGS = {
    "alexander-mercouris",
    "alex-mercouris",
    "mercouris",
    "",
}
DURAN_CHANNEL_SLUGS = {"the-duran", ""}
DURAN_SHOWS = {"the duran"}
SKIP_LINK_DIRS = {
    ".git",
    ".git-ssh",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
}
LINK_SUFFIXES = {".md", ".py", ".json", ".jsonl", ".yaml", ".yml", ".toml", ".txt"}

def parse_scalar(block: str, key: str) -> str | None:
    m = re.search(rf"^{re.escape(key)}:\s*(.+)$", block, re.M)
    if not m:
        return None
    val = m.group(1).strip().strip('"').strip("'")
    return val or None

def read_frontmatter_block(path: Path) -> str | None:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    return m.group(1)

def read_channel_slug(path: Path) -> str | None:
    block = read_frontmatter_block(path)
    if not block:
        return None
    return parse_scalar(block, "channel_slug")

def is_duran_capture(path: Path) -> bool:
    block = read_frontmatter_block(path)
    if not block:
        return False
    slug = (parse_scalar(block, "channel_slug") or "").lower()
    if slug == "the-duran":
        return True
    show = (parse_scalar(block, "show") or "").strip().lower()
    if show in DURAN_SHOWS:
        return True
    return False

def is_mercouris_solo_hub(path: Path) -> bool:
    block = read_frontmatter_block(path)
    if not block:
        return False
    source_form = (parse_scalar(block, "source_form") or "").lower()
    if source_form not in {"solo", ""}:
        return False
    thread = (parse_scalar(block, "thread") or "").lower()
    slug = (parse_scalar(block, "channel_slug") or "").lower()
    if thread == "mercouris":
        return True
    return slug in MERCOURIS_CHANNEL_SLUGS and source_form == "solo"

def proposed_basename(name: str, channel_slug: str | None, path: Path) -> str | None:
    slug = (channel_slug or "").strip().lower()
    lower = name.lower()

    if lower.startswith("source-napolitano-"):
        if slug and slug not in JUDGING_FREEDOM_SLUGS:
            return None
        return "source-judging-freedom-" + name[len("source-napolitano-") :]

    if lower.startswith("source-nawfal-"):
        if slug and slug not in MARIO_NAWFAL_SLUGS:
            return None
        return "source-mario-nawfal-" + name[len("source-nawfal-") :]

    if lower.startswith("source-tucker-carlson-"):
        return None

    m = GUEST_CARLSON_RE.match(name)
    if m and slug == "tucker-carlson":
        guest = m.group(1).lower()
        if guest in ("tucker-carlson", "dialogue-works"):
            return None
        return f"source-tucker-carlson-{guest}-" + m.group(2)

    if lower.startswith("source-alex-mercouris-"):
        if slug == "the-duran":
            return "source-duran-mercouris-" + name[len("source-alex-mercouris-") :]
        if slug and slug not in MERCOURIS_CHANNEL_SLUGS:
            return None
        return "source-alexander-mercouris-" + name[len("source-alex-mercouris-") :]

    if lower.startswith("source-mercouris-"):
        if is_duran_capture(path):
            return "source-duran-mercouris-" + name[len("source-mercouris-") :]
        if not is_mercouris_solo_hub(path):
            return None
        if slug and slug not in MERCOURIS_CHANNEL_SLUGS:
            return None
        return "source-alexander-mercouris-" + name[len("source-mercouris-") :]

    return None

def normalize_mercouris_channel_slug(path: Path) -> bool:
    block = read_frontmatter_block(path)
    if not block:
        return False
    slug = parse_scalar(block, "channel_slug")
    if slug not in ("alex-mercouris", "mercouris"):
        return False
    text = path.read_text(encoding="utf-8")
    updated = re.sub(
        r'^(channel_slug:\s*)(?:"(?:alex-mercouris|mercouris)"|(?:alex-mercouris|mercouris))\s*$',
        r"\1alexander-mercouris",
        text,
        count=1,
        flags=re.M,
    )
    if updated == text:
        return False
    path.write_text(updated, encoding="utf-8", newline="\n")
    return True

def patch_legacy_mercouris_slugs(root: Path) -> int:
    changed = 0
    for path in sorted(root.rglob("source-*.md")):
        if not path.is_file():
            continue
        if normalize_mercouris_channel_slug(path):
            changed += 1
    return changed

def collect_renames(root: Path) -> list[tuple[Path, Path]]:
    pairs: list[tuple[Path, Path]] = []
    for path in sorted(root.rglob("source-*.md")):
        if not path.is_file():
            continue
        new_name = proposed_basename(path.name, read_channel_slug(path), path)
        if not new_name or new_name == path.name:
            continue
        dest = path.with_name(new_name)
        if dest.exists() and dest.resolve() != path.resolve():
            raise SystemExit(f"collision: {path} -> {dest} (target exists)")
        pairs.append((path, dest))
    return pairs

def git_mv(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    rel_src = src.relative_to(REPO_ROOT)
    rel_dest = dest.relative_to(REPO_ROOT)
    proc = subprocess.run(
        ["git", "mv", str(rel_src), str(rel_dest)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    if proc.returncode == 0:
        return
    if "not under version control" in (proc.stderr or ""):
        shutil.move(src, dest)
        subprocess.run(["git", "add", str(rel_dest)], cwd=REPO_ROOT, check=True)
        return
    raise subprocess.CalledProcessError(proc.returncode, proc.args, proc.stdout, proc.stderr)

def git_rename_map() -> dict[str, str]:
    """Build old->new basename map from git rename detection."""
    mapping: dict[str, str] = {}
    for cmd in (
        ["git", "diff", "--name-status", "-M", "--diff-filter=R"],
        ["git", "diff", "--cached", "--name-status", "-M", "--diff-filter=R"],
    ):
        proc = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True, check=True)
        for line in proc.stdout.splitlines():
            parts = line.split("\t")
            if len(parts) != 3 or not parts[0].startswith("R"):
                continue
            old_path = Path(parts[1])
            new_path = Path(parts[2])
            if old_path.name != new_path.name:
                mapping[old_path.name] = new_path.name
    return mapping

def rewrite_links(renames: dict[str, str]) -> int:
    if not renames:
        return 0
    ordered = sorted(renames.items(), key=lambda kv: len(kv[0]), reverse=True)
    changed_files = 0
    for path in REPO_ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_LINK_DIRS for part in path.parts):
            continue
        if path.suffix.lower() not in LINK_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        original = text
        for old, new in ordered:
            if old in text:
                text = text.replace(old, new)
        if text != original:
            path.write_text(text, encoding="utf-8", newline="\n")
            changed_files += 1
    return changed_files

def rebuild_indices() -> None:
    subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "raw_input_master_index.py"), "--apply"],
        cwd=REPO_ROOT,
        check=True,
    )
    for year in ("2025", "2026"):
        subprocess.run(
            [
                sys.executable,
                str(REPO_ROOT / "scripts" / "build_statecraft_day_indices.py"),
                "--year",
                year,
            ],
            cwd=REPO_ROOT,
            check=True,
        )

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true", help="Print planned renames only.")
    ap.add_argument("--apply", action="store_true", help="Rename files and rewrite links.")
    ap.add_argument("--skip-indices", action="store_true", help="Skip index rebuild after apply.")
    ap.add_argument("--links-only", action="store_true", help="Rewrite links from git rename status only.")
    args = ap.parse_args()
    if not args.dry_run and not args.apply and not args.links_only:
        ap.error("Specify --dry-run, --apply, or --links-only")

    if args.links_only:
        mapping = git_rename_map()
        n = rewrite_links(mapping)
        print(f"link_files_updated={n} rename_pairs={len(mapping)}")
        if not args.skip_indices:
            rebuild_indices()
            print("indices_rebuilt")
        return 0

    pairs = collect_renames(ARCHIVE_ROOT)
    print(f"planned_renames={len(pairs)}")
    for src, dest in pairs:
        print(f"  {src.relative_to(REPO_ROOT)} -> {dest.name}")

    if args.dry_run:
        return 0

    for src, dest in pairs:
        git_mv(src, dest)

    slug_patched = patch_legacy_mercouris_slugs(ARCHIVE_ROOT)
    print(f"channel_slug_patched={slug_patched}")

    mapping = {src.name: dest.name for src, dest in pairs}
    n = rewrite_links(mapping)
    print(f"link_files_updated={n}")

    if not args.skip_indices:
        rebuild_indices()
        print("indices_rebuilt")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
