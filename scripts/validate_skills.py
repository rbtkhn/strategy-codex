#!/usr/bin/env python3
"""
Validate skill metadata across .cursor/skills/, skills/, and skills/runbooks/.

Read-only unless --fix is used.

Usage:
  python3 scripts/validate_skills.py
  python3 scripts/validate_skills.py --json
  python3 scripts/validate_skills.py --strict-verification
  python3 scripts/validate_skills.py --strict-metadata
  python3 scripts/validate_skills.py --fix
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from yaml_compat import safe_load_path, safe_load_text

from skill_consolidation_maps import CATEGORY_VALUES, STATUS_VALUES  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FRONTMATTER = {"name", "description"}
PORTABLE_REQUIRED = {"portable", "version"}

CURSOR_SKILLS_DIR = ".cursor/skills"
PORTABLE_SKILLS_DIR = "skills"
RUNBOOKS_DIR = "skills/runbooks"
MANIFEST_FILE = "skills/manifest.yaml"
SYNC_MARKER = "sync_portable_skills.py"
DRAFT_MAX_AGE_DAYS = 30
GRACE_MAR_PATH = "archive/grace-mar-instance/"

REDIRECT_STATUSES = frozenset({"redirect", "deprecated", "merged"})
SPECIAL_REPLACEMENTS = frozenset({
    "fork-revive", "archive", "coffee",
    "strategy-codex-expert-cross-weave", "strategy-codex-guest-canon-note",
    "strategy-notebook-expert-cross-weave", "strategy-notebook-guest-canon-note",
    "periodic-statecraft-review",
    "civ-state-primary-text",
    "civ-state-volume-hardening",
    "domain-lane-survey",
})

SCOPE_CLASSES = frozenset({"personal", "project-local", "repo-governed", "public-portable"})
VERIFICATION_HEADING = "## Verification / Proof Standard"

RUNBOOK_REQUIRED_FRONTMATTER = {
    "name",
    "description",
    "portable",
    "version",
    "scope_class",
    "skills",
    "outputs",
    "authority",
}

RUNBOOK_REQUIRED_SECTIONS = [
    "purpose",
    "trigger",
    "skills composed",
    "inputs required",
    "workflow steps",
    "human approval points",
    "stop conditions",
    "verification / proof standard",
    "outputs",
    "return paths",
]

ADVISORY_AUTHORITY = frozenset({"advisory_only", "advisory-only", "advisory only"})

FORBIDDEN_AUTHORITY_PHRASES = [
    "auto-merge",
    "auto merge",
    "automatic merge",
    "silent merge",
    "auto-publish",
    "auto publish",
    "automatic publish",
    "canonize without",
    "canon authority",
    "merge authority",
]

WARN_DISPLAY_CAP = 5


def _split_frontmatter(text: str) -> tuple[dict[str, Any] | None, str]:
    if not text.startswith("---"):
        return None, text
    end = text.find("---", 3)
    if end < 0:
        return None, text
    block = text[3:end]
    body = text[end + 3 :].lstrip("\n")
    try:
        fm = safe_load_text(block, feature="validate_skills.py")
    except RuntimeError:
        fm = _parse_frontmatter_legacy(text)
        return fm, body
    if not isinstance(fm, dict):
        return None, body
    return fm, body


def _parse_frontmatter_legacy(path_or_text: str | Path) -> dict[str, Any] | None:
    if isinstance(path_or_text, Path):
        try:
            text = path_or_text.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            return None
    else:
        text = path_or_text

    if not text.startswith("---"):
        return None

    end = text.find("---", 3)
    if end < 0:
        return None

    block = text[3:end].strip()
    result: dict[str, Any] = {}
    for line in block.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip().strip("'\"")
        if val.startswith("[") and val.endswith("]"):
            items = [v.strip().strip("'\"") for v in val[1:-1].split(",") if v.strip()]
            result[key] = items
        elif val.lower() == "true":
            result[key] = True
        elif val.lower() == "false":
            result[key] = False
        else:
            result[key] = val
    return result


def _parse_frontmatter(path: Path) -> dict[str, Any] | None:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None
    fm, _ = _split_frontmatter(text)
    return fm


def _has_verification_section(body: str) -> bool:
    return VERIFICATION_HEADING.lower() in body.lower()


def _load_manifest_entries() -> dict[str, dict[str, Any]]:
    manifest_path = REPO_ROOT / MANIFEST_FILE
    if not manifest_path.exists():
        return {}
    try:
        data = safe_load_path(manifest_path, feature="validate_skills.py")
    except RuntimeError:
        names = _load_manifest_names_legacy()
        return {n: {"name": n} for n in names}
    if not isinstance(data, dict):
        return {}
    skills = data.get("skills") or []
    out: dict[str, dict[str, Any]] = {}
    if isinstance(skills, list):
        for entry in skills:
            if isinstance(entry, dict) and entry.get("name"):
                out[str(entry["name"])] = entry
    return out


def _load_manifest_names_legacy() -> set[str]:
    manifest_path = REPO_ROOT / MANIFEST_FILE
    if not manifest_path.exists():
        return set()
    text = manifest_path.read_text(encoding="utf-8")
    names: set[str] = set()
    for m in re.finditer(r"^\s*-\s*name:\s*(.+)$", text, re.MULTILINE):
        names.add(m.group(1).strip())
    return names


def _cursor_skill_dirs() -> list[Path]:
    base = REPO_ROOT / CURSOR_SKILLS_DIR
    if not base.exists():
        return []
    return sorted(d for d in base.iterdir() if d.is_dir() and (d / "SKILL.md").exists())


def _portable_skill_dirs() -> list[Path]:
    base = REPO_ROOT / PORTABLE_SKILLS_DIR
    if not base.exists():
        return []
    return sorted(
        d
        for d in base.iterdir()
        if d.is_dir() and not d.name.startswith("_") and d.name != "runbooks" and (d / "SKILL.md").exists()
    )


def _draft_skill_paths() -> list[Path]:
    base = REPO_ROOT / PORTABLE_SKILLS_DIR / "_drafts"
    if not base.exists():
        return []
    return sorted(p / "SKILL.md" for p in base.iterdir() if p.is_dir() and (p / "SKILL.md").exists())


def _all_cursor_skill_names() -> set[str]:
    base = REPO_ROOT / CURSOR_SKILLS_DIR
    if not base.exists():
        return set()
    return {d.name for d in base.iterdir() if d.is_dir() and (d / "SKILL.md").exists()}


def _skill_exists(name: str, manifest_names: set[str], cursor_names: set[str] | None = None) -> bool:
    if name in manifest_names:
        return True
    if cursor_names and name in cursor_names:
        return True
    return (REPO_ROOT / PORTABLE_SKILLS_DIR / name / "SKILL.md").is_file()


def _replacement_valid(name: str, manifest_names: set[str], cursor_names: set[str]) -> bool:
    if name in SPECIAL_REPLACEMENTS:
        return True
    return _skill_exists(name, manifest_names, cursor_names)


def _check_consolidation_metadata(
    errors: list[dict[str, str]],
    *,
    rel: str,
    fm: dict[str, Any],
    manifest_entry: dict[str, Any] | None,
    body: str,
    is_manifest_listed: bool,
    is_cursor_only: bool,
    strict_metadata: bool,
    manifest_names: set[str],
    cursor_names: set[str],
) -> None:
    level = "error" if strict_metadata else "warn"
    needs_category = is_manifest_listed or is_cursor_only

    category = fm.get("category")
    status = fm.get("status", "active")

    if needs_category and not category:
        errors.append({"path": rel, "level": level, "message": "Missing category frontmatter"})
    elif category and category not in CATEGORY_VALUES:
        errors.append({"path": rel, "level": "error", "message": f"Invalid category '{category}'"})

    if needs_category and not fm.get("status"):
        errors.append({"path": rel, "level": level, "message": "Missing status frontmatter"})
    elif status and status not in STATUS_VALUES:
        errors.append({"path": rel, "level": "error", "message": f"Invalid status '{status}'"})

    if status in REDIRECT_STATUSES:
        replacement = fm.get("replacement")
        if not replacement:
            errors.append({
                "path": rel,
                "level": level,
                "message": f"status '{status}' requires replacement frontmatter",
            })
        elif not _replacement_valid(str(replacement), manifest_names, cursor_names):
            errors.append({
                "path": rel,
                "level": "error",
                "message": f"replacement '{replacement}' not found among skills",
            })

    if manifest_entry:
        for key in ("category", "status", "replacement"):
            if manifest_entry.get(key) and fm.get(key) and manifest_entry[key] != fm.get(key):
                errors.append({
                    "path": rel,
                    "level": "warn",
                    "message": f"{key} '{fm.get(key)}' differs from manifest '{manifest_entry[key]}'",
                })

    if status == "active" and GRACE_MAR_PATH in body:
        if not fm.get("fork-revive-only") and not fm.get("review_date"):
            errors.append({
                "path": rel,
                "level": "warn",
                "message": f"active skill references {GRACE_MAR_PATH} without fork-revive-only or review_date",
            })

    if status == "active":
        combined = (body or "").lower()
        for phrase in FORBIDDEN_AUTHORITY_PHRASES:
            if phrase not in combined:
                continue
            excluded = False
            for line in combined.splitlines():
                if phrase in line and any(
                    token in line for token in ("no ", "not ", "without ", "never ", "does not ")
                ):
                    excluded = True
                    break
            if not excluded:
                errors.append({
                    "path": rel,
                    "level": "error",
                    "message": f"Active skill must not claim authority: contains {phrase!r}",
                })


def _check_synced_cursor_target(
    errors: list[dict[str, str]],
    *,
    name: str,
    entry: dict[str, Any],
    strict_metadata: bool,
) -> None:
    target = REPO_ROOT / str(entry.get("target", ""))
    if not target.is_file():
        return
    fm = _parse_frontmatter(target)
    if fm is None:
        return
    synced = str(fm.get("synced_by", ""))
    if SYNC_MARKER not in synced:
        errors.append({
            "path": str(target.relative_to(REPO_ROOT)),
            "level": "error" if strict_metadata else "warn",
            "message": f"Manifest skill '{name}' cursor target missing synced_by: {SYNC_MARKER}",
        })


def _check_draft_age(errors: list[dict[str, str]], path: Path) -> None:
    import datetime as dt

    rel = str(path.relative_to(REPO_ROOT))
    try:
        mtime = path.stat().st_mtime
    except OSError:
        return
    age_days = (dt.datetime.now(tz=dt.timezone.utc) - dt.datetime.fromtimestamp(mtime, tz=dt.timezone.utc)).days
    if age_days > DRAFT_MAX_AGE_DAYS:
        errors.append({
            "path": rel,
            "level": "info",
            "message": f"Draft older than {DRAFT_MAX_AGE_DAYS} days ({age_days}d) — promote, merge, archive, or renew",
        })


def _check_scope_class(
    errors: list[dict[str, str]],
    *,
    rel: str,
    fm: dict[str, Any],
    manifest_entry: dict[str, Any] | None,
    is_manifest_listed: bool,
    forbidden_substrings: list[str] | None,
    body: str,
) -> None:
    scope = fm.get("scope_class")
    if scope is not None and scope not in SCOPE_CLASSES:
        errors.append({
            "path": rel,
            "level": "error",
            "message": f"Invalid scope_class '{scope}' (allowed: {', '.join(sorted(SCOPE_CLASSES))})",
        })

    if is_manifest_listed and not scope:
        errors.append({
            "path": rel,
            "level": "warn",
            "message": "Missing scope_class (default implied: repo-governed)",
        })

    if manifest_entry and manifest_entry.get("scope_class") and scope:
        if manifest_entry["scope_class"] != scope:
            errors.append({
                "path": rel,
                "level": "warn",
                "message": f"scope_class '{scope}' differs from manifest '{manifest_entry['scope_class']}'",
            })

    if scope == "public-portable" and forbidden_substrings:
        for sub in forbidden_substrings:
            if sub in body:
                errors.append({
                    "path": rel,
                    "level": "warn",
                    "message": f"public-portable body contains forbidden substring {sub!r}",
                })


def _check_verification(
    errors: list[dict[str, str]],
    *,
    rel: str,
    body: str,
    level: str,
    strict_verification: bool,
) -> None:
    if _has_verification_section(body):
        return
    if level == "info":
        errors.append({
            "path": rel,
            "level": "info",
            "message": f"Missing {VERIFICATION_HEADING} section (draft)",
        })
        return
    if strict_verification and level == "promoted":
        errors.append({
            "path": rel,
            "level": "error",
            "message": f"Missing {VERIFICATION_HEADING} section (--strict-verification)",
        })
        return
    errors.append({
        "path": rel,
        "level": "warn",
        "message": f"Missing {VERIFICATION_HEADING} section",
    })


def _runbook_paths() -> list[Path]:
    base = REPO_ROOT / RUNBOOKS_DIR
    if not base.exists():
        return []
    return sorted(base.glob("*.runbook.md"))


def _section_headings(body: str) -> set[str]:
    headings: set[str] = set()
    for line in body.splitlines():
        m = re.match(r"^##+\s+(.+)$", line.strip())
        if m:
            headings.add(m.group(1).strip().lower())
    return headings


def validate_runbooks(
    errors: list[dict[str, str]],
    *,
    manifest_names: set[str],
    cursor_names: set[str],
) -> None:
    for path in _runbook_paths():
        rel = str(path.relative_to(REPO_ROOT))
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            errors.append({"path": rel, "level": "error", "message": "Unreadable runbook"})
            continue

        fm, body = _split_frontmatter(text)
        if fm is None:
            errors.append({"path": rel, "level": "error", "message": "Missing or unparseable frontmatter"})
            continue

        for field in RUNBOOK_REQUIRED_FRONTMATTER:
            if field not in fm or fm[field] in (None, "", []):
                errors.append({"path": rel, "level": "error", "message": f"Missing required runbook field: {field}"})

        scope = fm.get("scope_class")
        if scope and scope not in SCOPE_CLASSES:
            errors.append({
                "path": rel,
                "level": "error",
                "message": f"Invalid scope_class '{scope}'",
            })

        authority = str(fm.get("authority", "")).strip().lower()
        if authority and authority not in {a.lower() for a in ADVISORY_AUTHORITY}:
            errors.append({
                "path": rel,
                "level": "error",
                "message": f"authority must be advisory-only, got {fm.get('authority')!r}",
            })

        combined = text.lower()
        for phrase in FORBIDDEN_AUTHORITY_PHRASES:
            if phrase in combined:
                errors.append({
                    "path": rel,
                    "level": "error",
                    "message": f"Runbook must not claim authority: contains {phrase!r}",
                })

        skills = fm.get("skills")
        if isinstance(skills, list):
            for skill_name in skills:
                if not _skill_exists(str(skill_name), manifest_names, cursor_names):
                    errors.append({
                        "path": rel,
                        "level": "error",
                        "message": f"skills entry '{skill_name}' not found in manifest or skills/",
                    })

        surfaces = fm.get("surfaces")
        if isinstance(surfaces, list):
            for surface in surfaces:
                surface_path = REPO_ROOT / str(surface)
                if not surface_path.is_file():
                    errors.append({
                        "path": rel,
                        "level": "error",
                        "message": f"surfaces path does not exist: {surface}",
                    })

        headings = _section_headings(body)
        for section in RUNBOOK_REQUIRED_SECTIONS:
            if not any(section in h for h in headings):
                errors.append({
                    "path": rel,
                    "level": "error",
                    "message": f"Missing required section: {section.title()}",
                })


def validate(
    *,
    verbose: bool = False,
    strict_verification: bool = False,
    strict_metadata: bool = False,
) -> list[dict[str, str]]:
    """Run all checks. Returns list of {path, level, message} dicts."""
    errors: list[dict[str, str]] = []
    known_skill_names = _all_cursor_skill_names()
    manifest_entries = _load_manifest_entries()
    manifest_names = set(manifest_entries.keys())
    portable_names = {d.name for d in _portable_skill_dirs()}

    for skill_dir in _cursor_skill_dirs():
        skill_path = skill_dir / "SKILL.md"
        rel = str(skill_path.relative_to(REPO_ROOT))
        try:
            text = skill_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            errors.append({"path": rel, "level": "error", "message": "Unreadable skill file"})
            continue

        fm, body = _split_frontmatter(text)
        if fm is None:
            errors.append({"path": rel, "level": "error", "message": "Missing or unparseable frontmatter"})
            continue

        for field in REQUIRED_FRONTMATTER:
            if field not in fm or not fm[field]:
                errors.append({"path": rel, "level": "error", "message": f"Missing required field: {field}"})

        if fm.get("name") and fm["name"] != skill_dir.name:
            errors.append({
                "path": rel,
                "level": "warn",
                "message": f"name '{fm['name']}' does not match directory '{skill_dir.name}'",
            })

        is_cursor_only = skill_dir.name not in portable_names
        if is_cursor_only:
            _check_consolidation_metadata(
                errors,
                rel=rel,
                fm=fm,
                manifest_entry=manifest_entries.get(skill_dir.name),
                body=body,
                is_manifest_listed=skill_dir.name in manifest_names,
                is_cursor_only=True,
                strict_metadata=strict_metadata,
                manifest_names=manifest_names,
                cursor_names=known_skill_names,
            )

            if fm.get("status", "active") == "active":
                _check_verification(
                    errors,
                    rel=rel,
                    body=body,
                    level="promoted" if strict_verification else "listed",
                    strict_verification=strict_verification and fm.get("status") == "active",
                )

        requires = fm.get("requires")
        if isinstance(requires, list):
            for dep in requires:
                if dep not in known_skill_names:
                    errors.append({
                        "path": rel,
                        "level": "error",
                        "message": f"requires '{dep}' but no .cursor/skills/{dep}/ exists",
                    })

    for skill_dir in _portable_skill_dirs():
        skill_path = skill_dir / "SKILL.md"
        rel = str(skill_path.relative_to(REPO_ROOT))
        try:
            text = skill_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            errors.append({"path": rel, "level": "error", "message": "Unreadable skill file"})
            continue

        fm, body = _split_frontmatter(text)
        if fm is None:
            errors.append({"path": rel, "level": "error", "message": "Missing or unparseable frontmatter"})
            continue

        for field in REQUIRED_FRONTMATTER | PORTABLE_REQUIRED:
            if field not in fm or (fm[field] == "" if isinstance(fm[field], str) else fm[field] is None):
                errors.append({"path": rel, "level": "error", "message": f"Missing required portable field: {field}"})

        if fm.get("portable") is not True:
            errors.append({"path": rel, "level": "error", "message": "portable: must be true for skills in skills/"})

        is_listed = skill_dir.name in manifest_names
        if not is_listed:
            errors.append({"path": rel, "level": "warn", "message": f"'{skill_dir.name}' not listed in {MANIFEST_FILE}"})

        entry = manifest_entries.get(skill_dir.name)
        forbidden = list(entry.get("verify_forbidden_substrings") or []) if entry else []
        _check_scope_class(
            errors,
            rel=rel,
            fm=fm,
            manifest_entry=entry,
            is_manifest_listed=is_listed,
            forbidden_substrings=forbidden,
            body=body,
        )
        _check_consolidation_metadata(
            errors,
            rel=rel,
            fm=fm,
            manifest_entry=entry,
            body=body,
            is_manifest_listed=is_listed,
            is_cursor_only=False,
            strict_metadata=strict_metadata,
            manifest_names=manifest_names,
            cursor_names=known_skill_names,
        )
        verify_level = "promoted" if is_listed else "listed"
        if is_listed and fm.get("status") == "redirect":
            verify_level = "listed"
        _check_verification(
            errors,
            rel=rel,
            body=body,
            level=verify_level,
            strict_verification=strict_verification and is_listed and fm.get("status", "active") == "active",
        )

    for draft_path in _draft_skill_paths():
        rel = str(draft_path.relative_to(REPO_ROOT))
        try:
            text = draft_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        fm, body = _split_frontmatter(text)
        if fm:
            _check_consolidation_metadata(
                errors,
                rel=rel,
                fm=fm,
                manifest_entry=None,
                body=body,
                is_manifest_listed=False,
                is_cursor_only=False,
                strict_metadata=False,
                manifest_names=manifest_names,
                cursor_names=known_skill_names,
            )
        _check_verification(
            errors,
            rel=rel,
            body=body,
            level="info",
            strict_verification=strict_verification,
        )
        _check_draft_age(errors, draft_path)

    for name, entry in manifest_entries.items():
        source_dir = REPO_ROOT / PORTABLE_SKILLS_DIR / name
        if not (source_dir / "SKILL.md").exists():
            errors.append({
                "path": MANIFEST_FILE,
                "level": "error",
                "message": f"Manifest lists '{name}' but {PORTABLE_SKILLS_DIR}/{name}/SKILL.md does not exist",
            })
        if entry.get("target"):
            _check_synced_cursor_target(errors, name=name, entry=entry, strict_metadata=strict_metadata)

    validate_runbooks(errors, manifest_names=manifest_names, cursor_names=known_skill_names)

    if verbose:
        pass

    return errors


def _count_by_level(errors: list[dict[str, str]]) -> dict[str, int]:
    counts = {"error": 0, "warn": 0, "info": 0}
    for e in errors:
        level = e.get("level", "warn")
        if level in counts:
            counts[level] += 1
    return counts


def format_text(errors: list[dict[str, str]], *, cap: int = WARN_DISPLAY_CAP) -> str:
    if not errors:
        return "All skills valid."

    counts = _count_by_level(errors)
    lines: list[str] = []

    errors_only = [e for e in errors if e["level"] == "error"]
    warns = [e for e in errors if e["level"] == "warn"]
    infos = [e for e in errors if e["level"] == "info"]

    for e in errors_only:
        lines.append(f"[ERROR] {e['path']}: {e['message']}")

    shown_warns = 0
    for e in warns:
        if shown_warns >= cap:
            break
        lines.append(f"[WARN] {e['path']}: {e['message']}")
        shown_warns += 1
    if len(warns) > cap:
        lines.append(f"[WARN] ... and {len(warns) - cap} more warning(s)")

    if infos and shown_warns < cap:
        for e in infos[: max(0, cap - shown_warns)]:
            lines.append(f"[INFO] {e['path']}: {e['message']}")

    lines.append(
        f"\n{len(errors)} issue(s): {counts['error']} error(s), {counts['warn']} warn(s), {counts['info']} info(s)."
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate skill metadata.")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--strict-verification", action="store_true", help="Fail promoted skills missing verification")
    parser.add_argument("--strict-metadata", action="store_true", help="Fail missing category/status/replacement/sync markers")
    parser.add_argument("--fix", action="store_true", help="Interactive fix mode (not yet implemented)")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    if args.fix:
        print("--fix mode is not yet implemented. Run without --fix to see issues.")
        return 1

    errors = validate(
        verbose=args.verbose,
        strict_verification=args.strict_verification,
        strict_metadata=args.strict_metadata,
    )
    counts = _count_by_level(errors)

    if args.json:
        payload = {
            "issues": errors,
            "error_count": counts["error"],
            "warn_count": counts["warn"],
            "info_count": counts["info"],
            "total": len(errors),
        }
        print(json.dumps(payload, indent=2))
    else:
        print(format_text(errors))

    return 1 if counts["error"] > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
