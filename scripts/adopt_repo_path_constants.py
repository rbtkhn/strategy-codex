#!/usr/bin/env python3
"""Replace hardcoded consolidated paths with repo_io constants in scripts/."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

REPLACEMENTS: list[tuple[str, str]] = [
    ('REPO_ROOT / "runtime/artifacts"', "ARTIFACTS_DIR"),
    ("REPO_ROOT / 'runtime/artifacts'", "ARTIFACTS_DIR"),
    ('repo_root / "runtime/artifacts"', "ARTIFACTS_DIR"),
    ('root / "runtime/artifacts"', "ARTIFACTS_DIR"),
    ('REPO_ROOT / "platform/src"', "SRC_DIR"),
    ("REPO_ROOT / 'platform/src'", "SRC_DIR"),
    ('REPO_ROOT / "runtime/prepared-context"', "PREPARED_CONTEXT_DIR"),
    ('repo_root / "runtime/prepared-context"', "PREPARED_CONTEXT_DIR"),
    ('root / "runtime/prepared-context"', "PREPARED_CONTEXT_DIR"),
    ('REPO_ROOT / "skills"', "SKILLS_DIR"),
    ('REPO_ROOT / "platform/apps"', "APPS_DIR"),
    ('REPO_ROOT / "archive/grace-mar-instance/bot"', "BOT_DIR"),
    ('REPO_ROOT / "schemas/registry"', "SCHEMA_REGISTRY_DIR"),
    ('_SRC = REPO_ROOT / "platform/src"', "_SRC = SRC_DIR"),
    ('ARTIFACT_ROOT / "runtime/artifacts"', "ARTIFACTS_DIR"),
]

IMPORT_FROM_RE = re.compile(r"^from repo_io import (.+)$", re.MULTILINE)

GRACE_MAR_CONSTANTS = frozenset({"BOT_DIR"})

def ensure_imports(text: str, constants: set[str]) -> str:
    if not constants:
        return text
    repo_io_names = sorted(c for c in constants if c not in GRACE_MAR_CONSTANTS)
    grace_mar_names = sorted(c for c in constants if c in GRACE_MAR_CONSTANTS)
    if repo_io_names:
        text = _ensure_repo_io_imports(text, repo_io_names)
    if grace_mar_names:
        text = _ensure_grace_mar_imports(text, grace_mar_names)
    return text

def _ensure_repo_io_imports(text: str, needed: list[str]) -> str:
    match = IMPORT_FROM_RE.search(text)
    if match:
        existing = [x.strip() for x in match.group(1).split(",")]
        merged = existing[:]
        for name in needed:
            if name not in merged:
                merged.append(name)
        new_import = "from repo_io import " + ", ".join(merged)
        return text[: match.start()] + new_import + text[match.end() :]
    anchor = "sys.path.insert(0,"
    idx = text.find(anchor)
    if idx == -1:
        anchor2 = 'if str(_SCRIPTS) not in sys.path:'
        idx = text.find(anchor2)
    if idx == -1:
        insert_at = 0
        for line in text.splitlines(True):
            if line.startswith("import ") or line.startswith("from "):
                insert_at += len(line)
            else:
                break
        block = "from repo_io import " + ", ".join(needed) + "\n"
        return text[:insert_at] + block + text[insert_at:]
    line_end = text.find("\n", idx)
    insert = line_end + 1 if line_end != -1 else len(text)
    block = "from repo_io import " + ", ".join(needed) + "\n"
    if block.strip() in text:
        return text
    return text[:insert] + block + text[insert:]

def _ensure_grace_mar_imports(text: str, needed: list[str]) -> str:
    marker = "from grace_mar_compat_paths import "
    if marker in text:
        return text
    anchor = "sys.path.insert(0,"
    idx = text.find(anchor)
    if idx == -1:
        anchor2 = 'if str(_SCRIPTS) not in sys.path:'
        idx = text.find(anchor2)
    if idx == -1:
        insert_at = 0
        for line in text.splitlines(True):
            if line.startswith("import ") or line.startswith("from "):
                insert_at += len(line)
            else:
                break
        block = "from grace_mar_compat_paths import " + ", ".join(needed) + "\n"
        return text[:insert_at] + block + text[insert_at:]
    line_end = text.find("\n", idx)
    insert = line_end + 1 if line_end != -1 else len(text)
    block = "from grace_mar_compat_paths import " + ", ".join(needed) + "\n"
    return text[:insert] + block + text[insert:]

def patch_file(path: Path, *, dry_run: bool) -> bool:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    new = text
    used: set[str] = set()
    for old, const in REPLACEMENTS:
        if old in new:
            new = new.replace(old, const)
            used.add(const)
    if used:
        new = ensure_imports(new, used)
    if new == text:
        return False
    rel = path.relative_to(REPO_ROOT)
    if dry_run:
        print(f"would update {rel} (+{', '.join(sorted(used))})")
    else:
        path.write_text(new, encoding="utf-8")
        print(f"updated {rel} (+{', '.join(sorted(used))})")
    return True

def main() -> int:
    parser = argparse.ArgumentParser(description="Adopt repo_io path constants")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    if not args.dry_run and not args.apply:
        parser.error("Specify --dry-run or --apply")
    changed = 0
    for path in sorted((REPO_ROOT / "scripts").rglob("*.py")):
        if path.name in {
            "adopt_repo_path_constants.py",
            "apply_root_path_rewrites.py",
            "check_repo_path_adoption.py",
        }:
            continue
        if patch_file(path, dry_run=args.dry_run):
            changed += 1
    print(f"{'would update' if args.dry_run else 'updated'} {changed} files")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
