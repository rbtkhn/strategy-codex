#!/usr/bin/env python3
"""Bounded slug ref patch: alkorshid -> alkhorshid (excludes archive capture bodies)."""
from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

PATCH_ROOTS = [
    REPO / "statecraft" / "voices",
    REPO / "statecraft" / "channels",
    REPO / "statecraft" / "sheets",
    REPO / "statecraft" / "audits",
    REPO / "codex",
    REPO / "scripts",
    REPO / "tests",
    REPO / "runtime" / "artifacts",
    REPO / "docs",
]
ROOT_FILES = [
    REPO / "repo-map.yaml",
    REPO / "generated-manifest.yaml",
    REPO / "AGENTS.md",
    REPO / "LLM-ROUTING.md",
]

SKIP_NAMES = frozenset({"rename_alkorshid_to_alkhorshid.py", "patch_alkhorshid_slug_refs.py"})
TEXT_SUFFIXES = frozenset({".md", ".py", ".yaml", ".yml", ".json", ".mdc", ".csv"})

REPLACEMENTS = [
    ("statecraft/voices/alkorshid/alkorshid-index.md", "statecraft/voices/alkhorshid/alkhorshid-index.md"),
    ("statecraft/voices/alkorshid/alkorshid-profile.md", "statecraft/voices/alkhorshid/alkhorshid-profile.md"),
    ("statecraft/voices/alkorshid/", "statecraft/voices/alkhorshid/"),
    ("voices/alkorshid/alkorshid-", "voices/alkhorshid/alkhorshid-"),
    ("alkorshid/alkorshid-", "alkhorshid/alkhorshid-"),
    ("codex/experts/alkorshid", "codex/experts/alkhorshid"),
    ("id: alkorshid-", "id: alkhorshid-"),
    ("alkorshid-index.md", "alkhorshid-index.md"),
    ("alkorshid-profile.md", "alkhorshid-profile.md"),
    ("alkorshid-index", "alkhorshid-index"),
    ("alkorshid-profile", "alkhorshid-profile"),
    ("dialogue-works-alkorshid-audit", "dialogue-works-alkhorshid-audit"),
    ("fix_alkorshid_threads_yaml", "fix_alkhorshid_threads_yaml"),
    ("audit_dialogue_works_alkorshid", "audit_dialogue_works_alkhorshid"),
    ("sweep_alkorshid_archive_links", "sweep_alkhorshid_archive_links"),
    ("apply_dialogue_works_alkorshid_migration", "apply_dialogue_works_alkhorshid_migration"),
    ("backfill_alkorshid_youtube_raw_input", "backfill_alkhorshid_youtube_raw_input"),
    ("2026-04-28-alkorshid.md", "2026-04-28-alkhorshid.md"),
    ("Alkorshid index", "Alkhorshid index"),
    ("Alkorshid profile", "Alkhorshid profile"),
    ("(`alkorshid`)", "(`alkhorshid`)"),
    ("`alkorshid`", "`alkhorshid`"),
    ('"thread": "alkorshid"', '"thread": "alkhorshid"'),
    ('"speaker": "alkorshid"', '"speaker": "alkhorshid"'),
    ("| alkorshid |", "| alkhorshid |"),
    ("- `alkorshid`", "- `alkhorshid`"),
    ("--shelf-index alkorshid", "--shelf-index alkhorshid"),
    ("--voice alkorshid", "--voice alkhorshid"),
    ("thread:alkorshid", "thread:alkhorshid"),
    ("thread: alkorshid", "thread: alkhorshid"),
    ("- alkorshid\n", "- alkhorshid\n"),
    ('"alkorshid":', '"alkhorshid":'),
    ("legacy slug/path **`alkorshid`** (missing `h`) pending rename to `alkhorshid`.", "slug **`alkhorshid`** (legacy capture filenames may still contain `alkorshid`)."),
    ("# Alkhorshid voice shelf (`alkorshid`)", "# Alkhorshid voice shelf (`alkhorshid`)"),
    ("# Alkhorshid index (`alkorshid`)", "# Alkhorshid index (`alkhorshid`)"),
]

THREAD_LINE_RE = re.compile(r"^(thread:\s*)alkorshid(\s*)$", re.M)
THREADS_ITEM_RE = re.compile(r"^(\s+-\s*)alkorshid(\s*)$", re.M)

def patch_text(text: str) -> str:
    if "shelf_index_utils.py" in text and '"alkhorshid": ("alkorshid",)' in text:
        return text
    out = text
    for old, new in REPLACEMENTS:
        out = out.replace(old, new)
    out = THREAD_LINE_RE.sub(r"\1alkhorshid\2", out)
    out = THREADS_ITEM_RE.sub(r"\1alkhorshid\2", out)
    return out

def iter_files():
    for root in PATCH_ROOTS:
        if not root.exists():
            continue
        if root.is_file():
            yield root
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if path.name in SKIP_NAMES:
                continue
            if "source-archive" in path.parts:
                continue
            if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in {"repo-map.yaml", "LLM-ROUTING.md"}:
                continue
            yield path
    for path in ROOT_FILES:
        if path.is_file():
            yield path

def patch_archive_frontmatter() -> int:
    archive = REPO / "source-archive" / "statecraft"
    fm_re = re.compile(r"\A(---\n.*?\n---\n)", re.DOTALL)
    n = 0
    for path in archive.rglob("*.md"):
        try:
            text = path.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeDecodeError):
            continue
        if "alkorshid" not in text[:800]:
            continue
        m = fm_re.match(text)
        if not m:
            continue
        new_fm = patch_text(m.group(1))
        if new_fm == m.group(1):
            continue
        path.write_text(new_fm + text[m.end() :], encoding="utf-8")
        n += 1
    return n

def main() -> int:
    patched: list[str] = []
    for path in iter_files():
        try:
            original = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if "alkorshid" not in original and "Alkorshid" not in original:
            continue
        if path.name == "shelf_index_utils.py":
            continue
        updated = patch_text(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8", newline="\n")
            patched.append(str(path.relative_to(REPO)))
    fm_n = patch_archive_frontmatter()
    print(f"patched {len(patched)} repo files; {fm_n} archive frontmatter files")
    for rel in patched[:50]:
        print(f"  {rel}")
    if len(patched) > 50:
        print(f"  ... and {len(patched) - 50} more")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
