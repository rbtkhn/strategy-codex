#!/usr/bin/env python3
"""
Backfill category/status frontmatter on skills (Commit 2).

Usage:
  python3 scripts/backfill_skill_metadata.py
  python3 scripts/backfill_skill_metadata.py --dry-run
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from repo_io import SKILLS_DIR

from skill_consolidation_maps import (  # noqa: E402
    CATEGORY_MAP,
    REPLACEMENT_MAP,
    REVIEW_DATE_MAP,
    STATUS_MAP,
)
from validate_skills import REPO_ROOT, _load_manifest_entries, _split_frontmatter  # noqa: E402
from yaml_compat import safe_dump, safe_load_path  # noqa: E402


def _format_scalar(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, list):
        if not value:
            return "[]"
        return "\n".join(f"  - {item}" for item in value)
    text = str(value)
    if any(c in text for c in ':"\'\n#{}[]'):
        return f'"{text.replace(chr(34), chr(92) + chr(34))}"'
    return text


def _render_frontmatter(fm: dict[str, Any]) -> str:
    """Preserve key order: name, description, then consolidation fields, then rest."""
    priority = [
        "name", "description", "preferred_activation", "activation",
        "portable", "version", "category", "status", "replacement",
        "scope_class", "review_date", "tags", "requires",
        "portable_source", "synced_by", "deprecated", "see",
    ]
    ordered_keys: list[str] = []
    for key in priority:
        if key in fm and key not in ordered_keys:
            ordered_keys.append(key)
    for key in sorted(fm.keys()):
        if key not in ordered_keys:
            ordered_keys.append(key)

    lines = ["---"]
    for key in ordered_keys:
        value = fm[key]
        if isinstance(value, list) and value:
            lines.append(f"{key}:")
            for item in value:
                lines.append(f"  - {item}")
        else:
            lines.append(f"{key}: {_format_scalar(value)}")
    lines.append("---")
    return "\n".join(lines)


def _merge_metadata(name: str, fm: dict[str, Any], *, is_draft: bool) -> dict[str, Any]:
    out = dict(fm)
    if is_draft:
        out.setdefault("status", "draft")
        out.setdefault("category", CATEGORY_MAP.get(name, "domain-pack"))
        return out

    if name in CATEGORY_MAP:
        out["category"] = CATEGORY_MAP[name]
    if name in STATUS_MAP:
        out["status"] = STATUS_MAP[name]
    if name in REPLACEMENT_MAP and out.get("status") in ("redirect", "deprecated", "merged", None):
        if STATUS_MAP.get(name) == "redirect":
            out["replacement"] = REPLACEMENT_MAP[name]
    if name in REVIEW_DATE_MAP and out.get("status") == "redirect":
        out.setdefault("review_date", REVIEW_DATE_MAP[name])
    if out.get("preferred_activation") and not out.get("activation"):
        out["activation"] = out["preferred_activation"]
    if out.get("portable") is True or name in _load_manifest_entries():
        out.setdefault("scope_class", "repo-governed")
    elif not out.get("scope_class"):
        out.setdefault("scope_class", "repo-governed")
    return out


def _patch_file(path: Path, name: str, *, is_draft: bool, dry_run: bool) -> bool:
    text = path.read_text(encoding="utf-8")
    fm, body = _split_frontmatter(text)
    if fm is None:
        print(f"SKIP (no frontmatter): {path}")
        return False
    merged = _merge_metadata(name, fm, is_draft=is_draft)
    if merged == fm:
        return False
    new_text = _render_frontmatter(merged) + "\n" + body.lstrip("\n")
    if dry_run:
        print(f"WOULD UPDATE: {path.relative_to(REPO_ROOT)}")
        return True
    path.write_text(new_text, encoding="utf-8")
    print(f"UPDATED: {path.relative_to(REPO_ROOT)}")
    return True


def _patch_manifest(dry_run: bool) -> bool:
    manifest_path = SKILLS_DIR / "manifest.yaml"
    data = safe_load_path(manifest_path, feature="backfill_skill_metadata.py")
    changed = False
    for entry in data.get("skills", []):
        name = entry.get("name")
        if not name:
            continue
        if name in CATEGORY_MAP and entry.get("category") != CATEGORY_MAP[name]:
            entry["category"] = CATEGORY_MAP[name]
            changed = True
        if name in STATUS_MAP and entry.get("status") != STATUS_MAP[name]:
            entry["status"] = STATUS_MAP[name]
            changed = True
        if name in REPLACEMENT_MAP and STATUS_MAP.get(name) == "redirect":
            if entry.get("replacement") != REPLACEMENT_MAP[name]:
                entry["replacement"] = REPLACEMENT_MAP[name]
                changed = True
    if not changed:
        return False
    if dry_run:
        print("WOULD UPDATE: skills/manifest.yaml")
        return True
    from yaml_compat import safe_dump as dump  # noqa: WPS433

    manifest_path.write_text(dump(data, feature="backfill_skill_metadata.py", sort_keys=False), encoding="utf-8")
    print("UPDATED: skills/manifest.yaml")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    manifest = _load_manifest_entries()
    updated = 0

    skills_base = SKILLS_DIR
    for skill_dir in sorted(skills_base.iterdir()):
        if not skill_dir.is_dir() or skill_dir.name.startswith("_") or skill_dir.name == "runbooks":
            continue
        skill_path = skill_dir / "SKILL.md"
        if skill_path.is_file():
            if _patch_file(skill_path, skill_dir.name, is_draft=False, dry_run=args.dry_run):
                updated += 1

    drafts_base = skills_base / "_drafts"
    if drafts_base.is_dir():
        for draft_dir in sorted(drafts_base.iterdir()):
            skill_path = draft_dir / "SKILL.md"
            if skill_path.is_file():
                if _patch_file(skill_path, draft_dir.name, is_draft=True, dry_run=args.dry_run):
                    updated += 1

    cursor_base = REPO_ROOT / ".cursor" / "skills"
    portable_names = {
        d.name for d in skills_base.iterdir()
        if d.is_dir() and not d.name.startswith("_") and d.name != "runbooks" and (d / "SKILL.md").is_file()
    }
    for skill_dir in sorted(cursor_base.iterdir()):
        if not skill_dir.is_dir():
            continue
        name = skill_dir.name
        if name in portable_names:
            continue
        skill_path = skill_dir / "SKILL.md"
        if skill_path.is_file():
            if _patch_file(skill_path, name, is_draft=False, dry_run=args.dry_run):
                updated += 1

    if _patch_manifest(args.dry_run):
        updated += 1

    print(f"\n{updated} file(s) {'would be ' if args.dry_run else ''}updated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
