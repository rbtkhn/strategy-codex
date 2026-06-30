#!/usr/bin/env python3
"""
Generate skill inventory artifacts for strategy-codex consolidation.

Usage:
  python3 scripts/generate_skill_inventory.py
  python3 scripts/generate_skill_inventory.py --json-only
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from repo_io import SKILLS_DIR

from skill_consolidation_maps import CATEGORY_MAP, REPLACEMENT_MAP, STATUS_MAP  # noqa: E402
from validate_skills import (  # noqa: E402
    MANIFEST_FILE,
    REPO_ROOT,
    _draft_skill_paths,
    _has_verification_section,
    _load_manifest_entries,
    _split_frontmatter,
)

OUTPUT_MD = REPO_ROOT / "runtime" / "artifacts" / "skill-inventory.md"
OUTPUT_JSON = REPO_ROOT / "runtime" / "artifacts" / "skill-inventory.json"

NOTES_MAP: dict[str, str] = {
    "coffee": "External host skill (~/.continuity/skills/coffee/); not in repo manifest",
    "academy-mirror-sync": "Candidate archived unless operator confirms active mirror",
    "strategy-notebook-lane-split": "Review: likely runbook or archived",
    "lane-survey": "Review: likely runbook or archived",
    "pros-and-cons": "Review: likely runbook or archived",
}

def _git_mtime(path: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI", "--", str(path)],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()[:10]
    except (OSError, subprocess.SubprocessError):
        pass
    try:
        ts = path.stat().st_mtime
        return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d")
    except OSError:
        return None

def _read_skill(path: Path) -> tuple[dict[str, Any] | None, str]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None, ""
    fm, body = _split_frontmatter(text)
    return fm, body

def _location(name: str, has_portable: bool, has_cursor: bool, is_draft: bool) -> str:
    if is_draft:
        return "draft"
    if has_portable and has_cursor:
        return "both"
    if has_portable:
        return "portable"
    if has_cursor:
        return "cursor-only"
    return "unknown"

def build_inventory() -> list[dict[str, Any]]:
    manifest = _load_manifest_entries()
    manifest_names = set(manifest.keys())

    portable_dirs = {
        d.name: d / "SKILL.md"
        for d in (SKILLS_DIR).iterdir()
        if d.is_dir() and not d.name.startswith("_") and d.name != "runbooks" and (d / "SKILL.md").is_file()
    }
    cursor_dirs = {
        d.name: d / "SKILL.md"
        for d in (REPO_ROOT / ".cursor" / "skills").iterdir()
        if d.is_dir() and (d / "SKILL.md").is_file()
    }
    draft_paths = {p.parent.name: p for p in _draft_skill_paths()}

    all_names = sorted(set(portable_dirs) | set(cursor_dirs) | set(draft_paths) | {"coffee"})

    rows: list[dict[str, Any]] = []
    for name in all_names:
        is_draft = name in draft_paths and name not in portable_dirs
        has_portable = name in portable_dirs
        has_cursor = name in cursor_dirs
        primary = draft_paths.get(name) or portable_dirs.get(name) or cursor_dirs.get(name)

        fm: dict[str, Any] | None = None
        body = ""
        if primary and primary.is_file():
            fm, body = _read_skill(primary)

        category = (fm or {}).get("category") or CATEGORY_MAP.get(name, "")
        status = (fm or {}).get("status") or STATUS_MAP.get(name, "active" if not is_draft else "draft")
        replacement = (fm or {}).get("replacement") or REPLACEMENT_MAP.get(name, "")
        activation = (
            (fm or {}).get("activation")
            or (fm or {}).get("preferred_activation")
            or ""
        )

        if body and _has_verification_section(body):
            proof = "present"
        elif is_draft or name == "coffee":
            proof = "n/a"
        else:
            proof = "missing"

        last_mod = _git_mtime(primary) if primary and primary.is_file() else None

        entry = manifest.get(name, {})
        target = entry.get("target", f".cursor/skills/{name}/SKILL.md" if has_cursor else "")
        source = entry.get("source", f"skills/{name}/SKILL.md" if has_portable else "")

        notes = NOTES_MAP.get(name, "")
        if name in manifest_names and manifest.get(name):
            manifest_text = (REPO_ROOT / MANIFEST_FILE).read_text(encoding="utf-8")
            # crude: find comment line before name entry
            if f"# Legacy" in manifest_text and name in ("wire-verify", "check-streams", "cognition-streams"):
                notes = (notes + "; manifest legacy comment").strip("; ")

        rows.append({
            "name": name,
            "location": _location(name, has_portable, has_cursor, is_draft),
            "manifest_listed": name in manifest_names,
            "cursor_target": target if has_cursor else "",
            "portable_source": source if has_portable else "",
            "category": category,
            "status": status,
            "replacement_or_parent": replacement,
            "activation_trigger": activation,
            "proof_standard": proof,
            "last_modified": last_mod or "",
            "notes": notes,
        })

    return rows

def _md_table(rows: list[dict[str, Any]]) -> str:
    headers = [
        "name", "location", "manifest_listed", "cursor_target", "portable_source",
        "category", "status", "replacement_or_parent", "activation_trigger",
        "proof_standard", "last_modified", "notes",
    ]
    lines = [
        "# Skill inventory (generated)",
        "",
        f"Generated: `{datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}`",
        "",
        "Regenerate: `python3 scripts/generate_skill_inventory.py`",
        "",
        f"Total rows: **{len(rows)}**",
        "",
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        cells = [str(row.get(h, "")).replace("|", "\\|") for h in headers]
        lines.append("| " + " | ".join(cells) + " |")
    lines.append("")
    return "\n".join(lines)

def main() -> int:
    parser = argparse.ArgumentParser(description="Generate skill inventory artifacts.")
    parser.add_argument("--json-only", action="store_true")
    args = parser.parse_args()

    rows = build_inventory()
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "row_count": len(rows),
        "skills": rows,
    }
    OUTPUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    if not args.json_only:
        OUTPUT_MD.write_text(_md_table(rows), encoding="utf-8")
        print(f"Wrote {OUTPUT_MD.relative_to(REPO_ROOT)} ({len(rows)} rows)")
    print(f"Wrote {OUTPUT_JSON.relative_to(REPO_ROOT)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
