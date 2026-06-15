#!/usr/bin/env python3
"""
Validate exported Civilizational Statecraft public book.

Usage:
  python scripts/validate_civilizational_statecraft_public.py
  python scripts/validate_civilizational_statecraft_public.py path/to/export
  python scripts/validate_civilizational_statecraft_public.py --json
  python scripts/validate_civilizational_statecraft_public.py path/to/publish-clone
  python scripts/validate_civilizational_statecraft_public.py --exclude archive path/to/publish-clone
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / "config" / "civilizational_statecraft_public_export.yaml"
DEFAULT_EXPORT = REPO_ROOT / "artifacts" / "civilizational-statecraft-public"

REQUIRED_ROOT = [
    "README.md",
    "table-of-contents.md",
    "reader-guide.md",
    "source-lattice.md",
    "glossary.md",
    "manifest.yaml",
    "LICENSE",
    "CONTRIBUTING.md",
    "FOUNDING-PROVENANCE.md",
    "EXPORT-RECEIPT.md",
]

REQUIRED_FRAMEWORK = [
    "framework/civilization-empire-faith-science-memory-desire.md",
    "framework/era-law.md",
    "comparative/continuity-mechanism.md",
    "comparative/pattern-library/README.md",
]

VOLUME_ESSAYS = ["civilization", "empire"]


def load_manifest() -> dict:
    if yaml is None:
        raise SystemExit("PyYAML required")
    with MANIFEST_PATH.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def normalize_exclude_prefixes(prefixes: list[str]) -> tuple[str, ...]:
    out: list[str] = []
    for raw in prefixes:
        p = raw.strip().strip("/\\").replace("\\", "/")
        if p:
            out.append(p)
    return tuple(out)


def is_excluded(rel: Path, exclude_prefixes: tuple[str, ...]) -> bool:
    if not exclude_prefixes:
        return False
    rel_posix = rel.as_posix()
    parts = rel_posix.split("/")
    if parts and parts[0] in exclude_prefixes:
        return True
    return any(rel_posix.startswith(f"{p}/") for p in exclude_prefixes)


def iter_markdown(export: Path, exclude_prefixes: tuple[str, ...]) -> list[Path]:
    paths: list[Path] = []
    for path in export.rglob("*.md"):
        rel = path.relative_to(export)
        if is_excluded(rel, exclude_prefixes):
            continue
        paths.append(path)
    return paths


def check_forbidden(
    export: Path, patterns: list[str], exclude_prefixes: tuple[str, ...]
) -> list[str]:
    errors: list[str] = []
    for path in iter_markdown(export, exclude_prefixes):
        text = path.read_text(encoding="utf-8")
        rel = str(path.relative_to(export))
        for pat in patterns:
            if pat.lower() in text.lower():
                errors.append(f"forbidden `{pat}` in {rel}")
    return errors


def check_required(export: Path, paths: list[str]) -> list[str]:
    return [f"missing required file: {p}" for p in paths if not (export / p).is_file()]


def check_volume(export: Path, slug: str, eras: list[str], stub: bool) -> list[str]:
    errors: list[str] = []
    base = export / "volumes" / slug
    for name in ["README.md", "introduction.md", "sacred-grammar.md", "shelf-reader.md", "bibliography.md"]:
        if not (base / name).is_file():
            errors.append(f"volumes/{slug}: missing {name}")
    for legacy in base.glob("statecraft-*.md"):
        errors.append(f"volumes/{slug}: legacy statecraft essay must not export: {legacy.name}")
    for part in VOLUME_ESSAYS:
        matches = list(base.glob(f"{part}-*.md"))
        if not matches and not stub:
            errors.append(f"volumes/{slug}: missing {part} essay")
    for era in eras:
        primary = base / "sources" / "primary" / f"{era}.md"
        if not primary.is_file():
            errors.append(f"volumes/{slug}: missing sources/primary/{era}.md")
    return errors


def check_internal_links(export: Path, exclude_prefixes: tuple[str, ...]) -> list[str]:
    errors: list[str] = []
    link_re = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for path in iter_markdown(export, exclude_prefixes):
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(export)
        for target in link_re.findall(text):
            if target.startswith("http") or target.startswith("#"):
                continue
            clean = target.split("#")[0]
            if not clean:
                continue
            dest = (path.parent / clean).resolve()
            try:
                dest.relative_to(export.resolve())
            except ValueError:
                errors.append(f"link escapes export root in {rel}: {target}")
                continue
            if not dest.exists():
                errors.append(f"broken link in {rel}: {target}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("export_dir", nargs="?", type=Path, default=DEFAULT_EXPORT)
    parser.add_argument("--json", action="store_true")
    parser.add_argument(
        "--exclude",
        action="append",
        default=None,
        metavar="PREFIX",
        help="Top-level path prefix to skip (repeatable). Default: manifest validation_exclude_prefixes.",
    )
    parser.add_argument(
        "--no-default-exclude",
        action="store_true",
        help="Validate every markdown file; ignore manifest validation_exclude_prefixes.",
    )
    args = parser.parse_args()

    export = args.export_dir.resolve()
    if not export.is_dir():
        print(f"Export directory not found: {export}", file=sys.stderr)
        return 1

    manifest = load_manifest()
    if args.no_default_exclude:
        exclude_prefixes: tuple[str, ...] = ()
    elif args.exclude is not None:
        exclude_prefixes = normalize_exclude_prefixes(args.exclude)
    else:
        exclude_prefixes = normalize_exclude_prefixes(
            manifest.get("validation_exclude_prefixes", [])
        )

    errors: list[str] = []
    errors.extend(check_required(export, REQUIRED_ROOT))
    errors.extend(check_required(export, REQUIRED_FRAMEWORK))
    errors.extend(check_forbidden(export, manifest.get("forbidden_patterns", []), exclude_prefixes))

    era_spine = manifest.get("era_spine", {})
    stubs = manifest.get("volume_stubs", {})
    for folder, slug in manifest.get("volume_slugs", {}).items():
        eras = era_spine.get(slug, [])
        stub = stubs.get(slug, {}).get("preview", False)
        errors.extend(check_volume(export, slug, eras, stub))

    errors.extend(check_internal_links(export, exclude_prefixes))

    result = {
        "export_dir": str(export),
        "exclude_prefixes": list(exclude_prefixes),
        "ok": len(errors) == 0,
        "error_count": len(errors),
        "errors": errors,
    }

    if args.json:
        print(json.dumps(result, indent=2))
    elif errors:
        print(f"VALIDATION FAILED ({len(errors)} errors):", file=sys.stderr)
        if exclude_prefixes:
            print(f"  (excluding: {', '.join(exclude_prefixes)})", file=sys.stderr)
        for err in errors[:50]:
            print(f"  {err}", file=sys.stderr)
    else:
        scope = f" (excluding: {', '.join(exclude_prefixes)})" if exclude_prefixes else ""
        print(f"OK: {export}{scope}")

    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
