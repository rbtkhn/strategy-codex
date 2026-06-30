#!/usr/bin/env python3
"""One-time migration: voice slug alkorshid -> alkhorshid (folder, files, routing)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

SKIP_DIR_NAMES = frozenset(
    {".git", ".git-local", ".git-ssh", "node_modules", "__pycache__", ".venv", "venv"}
)
TEXT_SUFFIXES = frozenset(
    {
        ".md",
        ".py",
        ".yaml",
        ".yml",
        ".json",
        ".jsonl",
        ".csv",
        ".txt",
        ".mdc",
    }
)

# Path renames (old relative -> new relative), deepest paths first.
PATH_RENAMES: list[tuple[str, str]] = [
    (
        "runtime/artifacts/host-shelf-quality/2026/alkorshid",
        "runtime/artifacts/host-shelf-quality/2026/alkhorshid",
    ),
    (
        "runtime/artifacts/host-shelf-quality/2025/alkorshid",
        "runtime/artifacts/host-shelf-quality/2025/alkhorshid",
    ),
    (
        "statecraft/voices/alkorshid/alkorshid-index.md",
        "statecraft/voices/alkhorshid/alkhorshid-index.md",
    ),
    (
        "statecraft/voices/alkorshid/alkorshid-profile.md",
        "statecraft/voices/alkhorshid/alkhorshid-profile.md",
    ),
    ("statecraft/voices/alkorshid", "statecraft/voices/alkhorshid"),
    ("continuity/experts/alkorshid", "continuity/experts/alkhorshid"),
    (
        "scripts/audit_dialogue_works_alkorshid.py",
        "scripts/audit_dialogue_works_alkhorshid.py",
    ),
    (
        "scripts/sweep_alkorshid_archive_links.py",
        "scripts/sweep_alkhorshid_archive_links.py",
    ),
    (
        "scripts/apply_dialogue_works_alkorshid_migration.py",
        "scripts/apply_dialogue_works_alkhorshid_migration.py",
    ),
    (
        "scripts/backfill_alkorshid_youtube_raw_input.py",
        "scripts/backfill_alkhorshid_youtube_raw_input.py",
    ),
    ("continuity/profiles/alkorshid-profile.md", "continuity/profiles/alkhorshid-profile.md"),
    (
        "statecraft/audits/dialogue-works-alkorshid-audit-2026-06-24.md",
        "statecraft/audits/dialogue-works-alkhorshid-audit-2026-06-24.md",
    ),
    (
        "statecraft/audits/dialogue-works-alkorshid-audit-2026-06-24-post.md",
        "statecraft/audits/dialogue-works-alkhorshid-audit-2026-06-24-post.md",
    ),
    (
        "statecraft/audits/dialogue-works-alkorshid-audit-2026-06-24.csv",
        "statecraft/audits/dialogue-works-alkhorshid-audit-2026-06-24.csv",
    ),
    (
        "statecraft/audits/dialogue-works-alkorshid-audit-2026-06-24-post.csv",
        "statecraft/audits/dialogue-works-alkhorshid-audit-2026-06-24-post.csv",
    ),
    (
        "statecraft/sheets/source-archive-residue/2026-04-28/2026-04-28-alkorshid.md",
        "statecraft/sheets/source-archive-residue/2026-04-28/2026-04-28-alkhorshid.md",
    ),
]

# Content replacements (order matters — longer/specific first).
CONTENT_REPLACEMENTS: list[tuple[str, str]] = [
    ("statecraft/voices/alkorshid/alkorshid-index.md", "statecraft/voices/alkhorshid/alkhorshid-index.md"),
    ("statecraft/voices/alkorshid/alkorshid-profile.md", "statecraft/voices/alkhorshid/alkhorshid-profile.md"),
    ("statecraft/voices/alkorshid/", "statecraft/voices/alkhorshid/"),
    ("statecraft/voices/alkorshid", "statecraft/voices/alkhorshid"),
    ("voices/alkorshid/alkorshid-", "voices/alkhorshid/alkhorshid-"),
    ("alkorshid/alkorshid-", "alkhorshid/alkhorshid-"),
    ("continuity/experts/alkorshid/", "continuity/experts/alkhorshid/"),
    ("continuity/experts/alkorshid", "continuity/experts/alkhorshid"),
    ("host-shelf-quality/2026/alkorshid", "host-shelf-quality/2026/alkhorshid"),
    ("host-shelf-quality/2025/alkorshid", "host-shelf-quality/2025/alkhorshid"),
    ("id: alkorshid-", "id: alkhorshid-"),
    ("alkorshid-index.md", "alkhorshid-index.md"),
    ("alkorshid-profile.md", "alkhorshid-profile.md"),
    ("alkorshid-index", "alkhorshid-index"),
    ("alkorshid-profile", "alkhorshid-profile"),
    ("dialogue-works-alkorshid-audit", "dialogue-works-alkhorshid-audit"),
    ("fix_alkorshid_threads_yaml", "fix_alkhorshid_threads_yaml"),
    ("fix_alkorshid_threads", "fix_alkhorshid_threads"),
    ("audit_dialogue_works_alkorshid", "audit_dialogue_works_alkhorshid"),
    ("Alkorshid index", "Alkhorshid index"),
    ("Alkorshid profile", "Alkhorshid profile"),
    ("Alkorshid guest", "Alkhorshid guest"),
    ("Nima Alkorshid", "Nima Alkhorshid"),
    ("Alkorshid /", "Alkhorshid /"),
    ("Alkorshid (", "Alkhorshid ("),
    ("Alkorshid voice", "Alkhorshid voice"),
    ("title: Alkorshid", "title: Alkhorshid"),
    ("`alkorshid`", "`alkhorshid`"),
    ('"alkorshid"', '"alkhorshid"'),
    ("- alkorshid\n", "- alkhorshid\n"),
    ("thread: alkorshid", "thread: alkhorshid"),
    ("thread:alkorshid", "thread:alkhorshid"),
    ("DEFAULT_THREAD = \"alkorshid\"", "DEFAULT_THREAD = \"alkhorshid\""),
    ('"alkorshid",', '"alkhorshid",'),
    ('"alkorshid"', '"alkhorshid"'),
    ("frozenset({\"alkorshid\"})", "frozenset({\"alkhorshid\"})"),
    ("SKIP_DIRS = frozenset({\"alkorshid\"})", "SKIP_DIRS = frozenset({\"alkhorshid\"})"),
    ("host_thread\": \"thread:alkorshid\"", "host_thread\": \"thread:alkhorshid\""),
    ("{nima, alkorshid,", "{nima, alkhorshid,"),
    ("nima alkorshid", "nima alkhorshid"),
    ("sweep_alkorshid_archive_links", "sweep_alkhorshid_archive_links"),
    ("apply_dialogue_works_alkorshid_migration", "apply_dialogue_works_alkhorshid_migration"),
    ("backfill_alkorshid_youtube_raw_input", "backfill_alkhorshid_youtube_raw_input"),
    ("2026-04-28-alkorshid.md", "2026-04-28-alkhorshid.md"),
    ("legacy slug/path **`alkorshid`** (missing `h`) pending rename to `alkhorshid`.", "slug **`alkhorshid`** (legacy capture filenames may still contain `alkorshid`)."),
    ("legacy slug **`alkorshid`** was renamed to **`alkhorshid`**", "slug **`alkhorshid`** (legacy capture filenames may still contain `alkorshid`)"),
]

THREAD_LINE_RE = re.compile(r"^(thread:\s*)alkorshid(\s*)$", re.M)
THREADS_ITEM_RE = re.compile(r"^(\s+-\s*)alkorshid(\s*)$", re.M)

def _should_skip(path: Path) -> bool:
    return any(part in SKIP_DIR_NAMES for part in path.parts)

def rename_paths() -> list[str]:
    logs: list[str] = []
    for old_rel, new_rel in PATH_RENAMES:
        old = REPO / old_rel
        new = REPO / new_rel
        if not old.exists():
            if new.exists():
                continue
            logs.append(f"skip missing: {old_rel}")
            continue
        if new.exists():
            if old.is_dir() and new.is_dir():
                for child in old.iterdir():
                    dest = new / child.name
                    if dest.exists():
                        logs.append(f"skip existing child: {dest.relative_to(REPO)}")
                        continue
                    child.rename(dest)
                    logs.append(f"merged: {child.relative_to(REPO)} -> {dest.relative_to(REPO)}")
                try:
                    old.rmdir()
                    logs.append(f"removed empty: {old_rel}")
                except OSError:
                    logs.append(f"left non-empty: {old_rel}")
                continue
            logs.append(f"skip target exists: {new_rel}")
            continue
        new.parent.mkdir(parents=True, exist_ok=True)
        old.rename(new)
        logs.append(f"renamed: {old_rel} -> {new_rel}")
    return logs

def patch_text(text: str) -> str:
    out = text
    for old, new in CONTENT_REPLACEMENTS:
        out = out.replace(old, new)
    out = THREAD_LINE_RE.sub(r"\1alkhorshid\2", out)
    out = THREADS_ITEM_RE.sub(r"\1alkhorshid\2", out)
    return out

def patch_files() -> list[str]:
    logs: list[str] = []
    for path in sorted(REPO.rglob("*")):
        if not path.is_file() or _should_skip(path):
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in {
            "repo-map.yaml",
            "LLM-ROUTING.md",
        }:
            continue
        if "rename_alkorshid_to_alkhorshid.py" in str(path):
            continue
        try:
            original = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if "alkorshid" not in original and "Alkorshid" not in original:
            continue
        updated = patch_text(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8", newline="\n")
            logs.append(str(path.relative_to(REPO)))
    return logs

def main() -> int:
    print("=== path renames ===")
    for line in rename_paths():
        print(line)
    print("=== content patches ===")
    patched = patch_files()
    print(f"patched {len(patched)} files")
    for rel in patched[:40]:
        print(f"  {rel}")
    if len(patched) > 40:
        print(f"  ... and {len(patched) - 40} more")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
