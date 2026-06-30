#!/usr/bin/env python3
"""Validate WORK-only speaker state sets.

Raw input remains the provenance chain. Speaker folders and their linked
ledgers/maps are compact state: they must stay link-valid, source-backed, and
shape-consistent where a source set or guest matrix declares exactness.
"""

from __future__ import annotations

import argparse
import re
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTERED_SPEAKER_SLUGS = ("pape", "crooke", "ritter", "parsi", "daniel-davis", "diesen")
DEFAULT_VOICES_DIR = REPO_ROOT / "statecraft" / "voices"
DEFAULT_CHANNELS_DIR = REPO_ROOT / "statecraft" / "channels"
# Folder names under statecraft/channels/ (channel-index slugs + legacy alias keys)
HOST_SLUGS = frozenset({"daniel-davis", "judging-freedom", "dialogue-works"})
CHANNEL_OBJECT_PREFIX = {
    "daniel-davis": "davis",
    "judging-freedom": "napolitano",
    "dialogue-works": "nima",
}

HEADING_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
HTTP_RE = re.compile(r"^[a-z][a-z0-9+.-]*:", re.IGNORECASE)
DATE_NAMED_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-")
WINDOWS_DRIVE_RE = re.compile(r"^[A-Za-z]:[\\/]")

BOUNDARY_MARKERS = (
        "WORK-only strategy-codex analysis. This is not Record material.",
)

OBVIOUS_STATE_NAME_RE = re.compile(
    r"(^README\.md$|speaker-object|cross-host-note|helix|routing|"
    r"host-wiring|interview-appearances|forecast-ledger)",
    re.IGNORECASE,
)

@dataclass(frozen=True)
class SourceSetSpec:
    file: str
    expected_count: int
    required_prefixes: tuple[str, ...] = ()
    excluded_patterns: tuple[str, ...] = ()

@dataclass(frozen=True)
class GuestMatrixSpec:
    file: str
    arc_glob: str
    expected_count: int

@dataclass(frozen=True)
class SpeakerSpec:
    slug: str
    manifest_file: str
    compact_state_files: tuple[str, ...]
    provenance_roots: tuple[str, ...]
    source_sets: tuple[SourceSetSpec, ...] = ()
    guest_matrices: tuple[GuestMatrixSpec, ...] = ()

def repo_rel(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()

def normalize_manifest_rel(raw: str) -> str:
    return raw.replace("\\", "/").strip()

def validate_repo_relative(value: object, field: str, manifest_rel: str) -> tuple[str | None, str | None]:
    if not isinstance(value, str) or not value.strip():
        return None, f"{manifest_rel}: `{field}` must be a non-empty string"
    normalized = normalize_manifest_rel(value)
    parts = normalized.split("/")
    if (
        normalized.startswith("/")
        or WINDOWS_DRIVE_RE.match(normalized)
        or any(part in ("", ".", "..") for part in parts)
    ):
        return None, f"{manifest_rel}: `{field}` must be a repo-relative path: {value!r}"
    return normalized, None

def string_list(value: object, field: str, manifest_rel: str) -> tuple[tuple[str, ...], list[str]]:
    if not isinstance(value, list):
        return (), [f"{manifest_rel}: `{field}` must be a list of strings"]
    out: list[str] = []
    errors: list[str] = []
    for idx, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            errors.append(f"{manifest_rel}: `{field}[{idx}]` must be a non-empty string")
        else:
            out.append(item.strip())
    return tuple(out), errors

def section_text(text: str, heading: str) -> str:
    target = heading.casefold()
    for match in HEADING_RE.finditer(text):
        if match.group(1).strip().casefold() != target:
            continue
        start = match.end()
        next_match = HEADING_RE.search(text, start)
        end = next_match.start() if next_match else len(text)
        return text[start:end]
    return ""

def has_work_boundary(text: str) -> bool:
    return any(marker in text for marker in BOUNDARY_MARKERS)

def is_compatibility_pointer(text: str) -> bool:
    lowered = text.casefold()
    return (
        (
            lowered.startswith("# compatibility pointer")
            and "canonical statecraft-relevant surface now lives at" in lowered
        )
        or (
            "compatibility note:" in lowered
            and "canonical" in lowered
            and "compatibility residue only" in lowered
        )
    )

def strip_link_target(raw: str) -> str:
    target = raw.strip()
    if " " in target and not target.startswith("<"):
        # Drop optional markdown title: [x](path "title").
        target = target.split(" ", 1)[0].strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1].strip()
    return target

def normalize_link_target(raw: str, base_file: Path, repo_root: Path) -> Path | None:
    target = strip_link_target(raw)
    if not target or target.startswith("#"):
        return None
    if "#" in target:
        target = target.split("#", 1)[0]
    if "?" in target:
        target = target.split("?", 1)[0]
    if not target:
        return None
    if HTTP_RE.match(target) and not WINDOWS_DRIVE_RE.match(target):
        return None

    target = target.replace("\\", "/")
    if re.match(r"^/[A-Za-z]:/", target):
        target = target[1:]

    path = Path(target)
    if not path.is_absolute():
        path = base_file.parent / path
    return path.resolve()

def migrated_source_target(path: Path, repo_root: Path) -> Path:
    """Map legacy codex source links onto currently tracked targets when applicable."""
    try:
        rel = path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.resolve()
    match = re.search(
        r"codex/years/(\d{4})/(?:raw-input|provenance)/(\d{4}-\d{2}-\d{2})/(.+\.md)$",
        rel,
    )
    if not match:
        return path.resolve()
    year, date_dir, filename = match.groups()
    candidates = (
        repo_root / "source-archive" / "statecraft" / date_dir / filename,
        repo_root / "codex" / "years" / year / "raw-input" / date_dir / filename,
    )
    for candidate in candidates:
        resolved = candidate.resolve()
        if resolved.exists():
            return resolved
    return path.resolve()

def markdown_links(text: str, base_file: Path, repo_root: Path) -> list[tuple[str, Path]]:
    out: list[tuple[str, Path]] = []
    for match in MARKDOWN_LINK_RE.finditer(text):
        raw = match.group(1)
        normalized = normalize_link_target(raw, base_file, repo_root)
        if normalized is not None:
            out.append((raw, normalized))
    return out

def source_links(
    text: str,
    base_file: Path,
    repo_root: Path,
    provenance_roots: tuple[Path, ...] = (),
) -> list[tuple[str, Path]]:
    links: list[tuple[str, Path]] = []
    for raw, path in markdown_links(text, base_file, repo_root):
        if path.suffix != ".md":
            continue
        rel = repo_rel(path, repo_root)
        under_legacy_root = any(
            needle in f"/{rel}"
            for needle in ("/raw-input/", "/provenance/", "/source-archive/statecraft/")
        )
        if provenance_roots:
            if is_under_any(path, provenance_roots) or under_legacy_root:
                links.append((raw, path))
        elif under_legacy_root:
            links.append((raw, path))
        else:
            links.append((raw, path))
    return links

def pattern_matches(pattern: str, basename: str, raw: str, rel: str) -> bool:
    if pattern.startswith("date-named-"):
        slug = pattern.removeprefix("date-named-")
        return DATE_NAMED_RE.match(basename) is not None and basename.endswith(f"-{slug}.md")
    return pattern in basename or pattern in raw or pattern in rel

def is_under_any(path: Path, roots: tuple[Path, ...]) -> bool:
    resolved = path.resolve()
    for root in roots:
        try:
            resolved.relative_to(root.resolve())
        except ValueError:
            continue
        return True
    return False

def speaker_shelf_dir(slug: str, voices_dir: Path, hosts_dir: Path) -> Path:
    if slug in HOST_SLUGS:
        return hosts_dir / slug
    return voices_dir / slug

def load_manifest(slug: str, repo_root: Path, voices_dir: Path, hosts_dir: Path) -> tuple[SpeakerSpec | None, list[str]]:
    manifest_path = speaker_shelf_dir(slug, voices_dir, hosts_dir) / "state-set.toml"
    manifest_rel = repo_rel(manifest_path, repo_root)
    if not manifest_path.exists():
        return None, [f"{manifest_rel}: registered speaker manifest is missing"]

    try:
        with manifest_path.open("rb") as fh:
            data = tomllib.load(fh)
    except tomllib.TOMLDecodeError as exc:
        return None, [f"{manifest_rel}: invalid TOML: {exc}"]

    errors: list[str] = []
    if data.get("version") != 1:
        errors.append(f"{manifest_rel}: `version` must be 1")
    if data.get("slug") != slug:
        errors.append(f"{manifest_rel}: `slug` must be `{slug}`")

    raw_compact_state_files = data.get("compact_state_files")
    raw_provenance_roots = data.get("provenance_roots")
    compact_state_files, compact_errors = string_list(
        raw_compact_state_files, "compact_state_files", manifest_rel
    )
    provenance_roots, provenance_errors = string_list(
        raw_provenance_roots, "provenance_roots", manifest_rel
    )
    errors.extend(compact_errors)
    errors.extend(provenance_errors)

    compact_state_files = tuple(
        validated
        for idx, item in enumerate(compact_state_files)
        for validated, error in [validate_repo_relative(item, f"compact_state_files[{idx}]", manifest_rel)]
        if not error
    )
    provenance_roots = tuple(
        validated
        for idx, item in enumerate(provenance_roots)
        for validated, error in [validate_repo_relative(item, f"provenance_roots[{idx}]", manifest_rel)]
        if not error
    )

    for idx, item in enumerate(raw_compact_state_files if isinstance(raw_compact_state_files, list) else []):
        _validated, error = validate_repo_relative(item, f"compact_state_files[{idx}]", manifest_rel)
        if error:
            errors.append(error)
    for idx, item in enumerate(raw_provenance_roots if isinstance(raw_provenance_roots, list) else []):
        validated, error = validate_repo_relative(item, f"provenance_roots[{idx}]", manifest_rel)
        if error:
            errors.append(error)

    source_sets, source_errors = parse_source_sets(data.get("source_sets", []), manifest_rel)
    guest_matrices, matrix_errors = parse_guest_matrices(data.get("guest_matrices", []), manifest_rel)
    errors.extend(source_errors)
    errors.extend(matrix_errors)

    if errors:
        return None, errors

    return (
        SpeakerSpec(
            slug=slug,
            manifest_file=manifest_rel,
            compact_state_files=compact_state_files,
            provenance_roots=provenance_roots,
            source_sets=source_sets,
            guest_matrices=guest_matrices,
        ),
        [],
    )

def parse_source_sets(value: object, manifest_rel: str) -> tuple[tuple[SourceSetSpec, ...], list[str]]:
    if value is None:
        return (), []
    if not isinstance(value, list):
        return (), [f"{manifest_rel}: `source_sets` must be a list of tables"]
    specs: list[SourceSetSpec] = []
    errors: list[str] = []
    for idx, item in enumerate(value):
        if not isinstance(item, dict):
            errors.append(f"{manifest_rel}: `source_sets[{idx}]` must be a table")
            continue
        path, path_error = validate_repo_relative(item.get("file"), f"source_sets[{idx}].file", manifest_rel)
        if path_error:
            errors.append(path_error)
        expected = item.get("expected_count")
        if not isinstance(expected, int) or expected < 0:
            errors.append(f"{manifest_rel}: `source_sets[{idx}].expected_count` must be a non-negative integer")
        required, required_errors = string_list(
            item.get("required_prefixes", []), f"source_sets[{idx}].required_prefixes", manifest_rel
        )
        excluded, excluded_errors = string_list(
            item.get("excluded_patterns", []), f"source_sets[{idx}].excluded_patterns", manifest_rel
        )
        errors.extend(required_errors)
        errors.extend(excluded_errors)
        if path_error or not isinstance(expected, int) or expected < 0:
            continue
        specs.append(
            SourceSetSpec(
                file=path,
                expected_count=expected,
                required_prefixes=required,
                excluded_patterns=excluded,
            )
        )
    return tuple(specs), errors

def parse_guest_matrices(value: object, manifest_rel: str) -> tuple[tuple[GuestMatrixSpec, ...], list[str]]:
    if value is None:
        return (), []
    if not isinstance(value, list):
        return (), [f"{manifest_rel}: `guest_matrices` must be a list of tables"]
    specs: list[GuestMatrixSpec] = []
    errors: list[str] = []
    for idx, item in enumerate(value):
        if not isinstance(item, dict):
            errors.append(f"{manifest_rel}: `guest_matrices[{idx}]` must be a table")
            continue
        path, path_error = validate_repo_relative(item.get("file"), f"guest_matrices[{idx}].file", manifest_rel)
        glob, glob_error = validate_repo_relative(
            item.get("arc_glob"), f"guest_matrices[{idx}].arc_glob", manifest_rel
        )
        expected = item.get("expected_count")
        if not isinstance(expected, int) or expected < 0:
            errors.append(f"{manifest_rel}: `guest_matrices[{idx}].expected_count` must be a non-negative integer")
        for error in (path_error, glob_error):
            if error:
                errors.append(error)
        if path_error or glob_error or not isinstance(expected, int) or expected < 0:
            continue
        specs.append(GuestMatrixSpec(file=path, arc_glob=glob, expected_count=expected))
    return tuple(specs), errors

def validate_compact_state_file(path: Path, repo_root: Path) -> list[str]:
    if not path.exists():
        return [f"{repo_rel(path, repo_root)}: registered compact state file is missing"]
    text = path.read_text(encoding="utf-8")
    if is_compatibility_pointer(text):
        return []
    if not has_work_boundary(text):
        return [f"{repo_rel(path, repo_root)}: missing WORK-only state boundary"]
    return []

def validate_source_set(
    spec: SourceSetSpec,
    repo_root: Path,
    provenance_roots: tuple[Path, ...] = (),
) -> list[str]:
    path = repo_root / spec.file
    errors: list[str] = []
    if not path.exists():
        return [f"{spec.file}: source set file is missing"]

    text = path.read_text(encoding="utf-8")
    if is_compatibility_pointer(text):
        return []
    section = section_text(text, "Source Set")
    if not section:
        return [f"{spec.file}: missing `## Source Set` section"]

    links = source_links(section, path, repo_root, provenance_roots)
    if len(links) != spec.expected_count:
        errors.append(
            f"{spec.file}: Source Set has {len(links)} source link(s); "
            f"expected {spec.expected_count}"
        )

    seen: dict[str, int] = {}
    for raw, target in links:
        resolved_target = target
        if not resolved_target.exists():
            migrated = migrated_source_target(resolved_target, repo_root)
            if migrated.exists():
                resolved_target = migrated
        rel = repo_rel(resolved_target, repo_root)
        basename = resolved_target.name
        seen[rel] = seen.get(rel, 0) + 1
        if provenance_roots and not is_under_any(resolved_target, provenance_roots):
            roots = ", ".join(repo_rel(root, repo_root) for root in provenance_roots)
            errors.append(f"{spec.file}: Source Set target `{rel}` is outside provenance roots: {roots}")
        if not resolved_target.exists():
            errors.append(f"{spec.file}: missing Source Set target `{rel}`")
        if spec.required_prefixes and not basename.startswith(spec.required_prefixes):
            prefixes = ", ".join(spec.required_prefixes)
            errors.append(
                f"{spec.file}: Source Set target `{basename}` does not match "
                f"required prefix(es): {prefixes}"
            )
        for pattern in spec.excluded_patterns:
            if pattern_matches(pattern, basename, raw, rel):
                errors.append(f"{spec.file}: excluded source class `{pattern}` appears in `{rel}`")

    duplicates = sorted(rel for rel, count in seen.items() if count > 1)
    for rel in duplicates:
        errors.append(f"{spec.file}: duplicate Source Set target `{rel}`")

    return errors

def validate_guest_matrix(spec: GuestMatrixSpec, repo_root: Path) -> list[str]:
    path = repo_root / spec.file
    errors: list[str] = []
    if not path.exists():
        return [f"{spec.file}: guest matrix file is missing"]

    text = path.read_text(encoding="utf-8")
    section = section_text(text, "Guest Transformation Matrix")
    if not section:
        return [f"{spec.file}: missing `## Guest Transformation Matrix` section"]

    expected = sorted(repo_root.glob(spec.arc_glob))
    if len(expected) != spec.expected_count:
        errors.append(
            f"{spec.file}: discovered {len(expected)} guest arc file(s); "
            f"expected {spec.expected_count}"
        )

    expected_names = {p.name for p in expected}
    for arc in expected:
        count = section.count(arc.name)
        if count != 1:
            errors.append(
                f"{spec.file}: guest matrix references `{arc.name}` {count} time(s); "
                "expected exactly once"
            )

    linked_arc_names: set[str] = set()
    for _raw, target in markdown_links(section, path, repo_root):
        if target.name.endswith("-speaker-arc.md"):
            linked_arc_names.add(target.name)
            if target.name not in expected_names:
                errors.append(f"{spec.file}: guest matrix links unexpected arc `{repo_rel(target, repo_root)}`")
            elif not target.exists():
                errors.append(f"{spec.file}: missing guest matrix target `{repo_rel(target, repo_root)}`")

    missing_linked = sorted(expected_names - linked_arc_names)
    for name in missing_linked:
        errors.append(f"{spec.file}: guest matrix does not link expected arc `{name}`")

    return errors

def validate_registered_speaker(
    slug: str,
    repo_root: Path,
    voices_dir: Path,
    hosts_dir: Path,
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    spec, manifest_errors = load_manifest(slug, repo_root, voices_dir, hosts_dir)
    if manifest_errors:
        return manifest_errors, warnings
    assert spec is not None

    for state_file in spec.compact_state_files:
        errors.extend(validate_compact_state_file(repo_root / state_file, repo_root))
    provenance_roots = tuple((repo_root / root).resolve() for root in spec.provenance_roots)
    for source_set in spec.source_sets:
        errors.extend(validate_source_set(source_set, repo_root, provenance_roots))
    for guest_matrix in spec.guest_matrices:
        errors.extend(validate_guest_matrix(guest_matrix, repo_root))
    return errors, warnings

def is_inside_codex(path: Path, repo_root: Path) -> bool:
    try:
        path.resolve().relative_to((repo_root / "codex").resolve())
    except ValueError:
        return False
    return True

def obvious_state_files(speaker_dir: Path) -> list[Path]:
    return sorted(
        path
        for path in speaker_dir.glob("*.md")
        if OBVIOUS_STATE_NAME_RE.search(path.name)
    )

def validate_unregistered_speaker(speaker_dir: Path, repo_root: Path) -> list[str]:
    slug = speaker_dir.name
    warnings: list[str] = []
    if slug.startswith("_"):
        return warnings

    if not (speaker_dir / "README.md").exists():
        warnings.append(f"{repo_rel(speaker_dir, repo_root)}: no README.md")
    if not (speaker_dir / f"{slug}-speaker-object.md").exists():
        warnings.append(f"{repo_rel(speaker_dir, repo_root)}: no `{slug}-speaker-object.md`")

    for path in obvious_state_files(speaker_dir):
        text = path.read_text(encoding="utf-8")
        if not has_work_boundary(text):
            warnings.append(f"{repo_rel(path, repo_root)}: missing WORK-only state boundary")
        for raw, target in markdown_links(text, path, repo_root):
            if is_inside_codex(target, repo_root) and not target.exists():
                warnings.append(f"{repo_rel(path, repo_root)}: broken codex link `{strip_link_target(raw)}`")

    return warnings

def validate_all(
    repo_root: Path,
    voices_dir: Path,
    hosts_dir: Path,
    speaker: str | None = None,
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if speaker:
        slug = speaker.strip().lower()
        if slug in REGISTERED_SPEAKER_SLUGS:
            speaker_errors, speaker_warnings = validate_registered_speaker(
                slug, repo_root, voices_dir, hosts_dir
            )
            errors.extend(speaker_errors)
            warnings.extend(speaker_warnings)
        else:
            speaker_dir = speaker_shelf_dir(slug, voices_dir, hosts_dir)
            if not speaker_dir.exists():
                errors.append(f"unknown speaker `{slug}` and no folder at {repo_rel(speaker_dir, repo_root)}")
            else:
                warnings.extend(validate_unregistered_speaker(speaker_dir, repo_root))
        return errors, warnings

    for slug in REGISTERED_SPEAKER_SLUGS:
        speaker_errors, speaker_warnings = validate_registered_speaker(
            slug, repo_root, voices_dir, hosts_dir
        )
        errors.extend(speaker_errors)
        warnings.extend(speaker_warnings)

    if voices_dir.exists():
        for speaker_dir in sorted(path for path in voices_dir.iterdir() if path.is_dir()):
            if speaker_dir.name.lower() not in REGISTERED_SPEAKER_SLUGS:
                warnings.extend(validate_unregistered_speaker(speaker_dir, repo_root))

    return errors, warnings

def list_registered(repo_root: Path, voices_dir: Path, hosts_dir: Path) -> None:
    for slug in REGISTERED_SPEAKER_SLUGS:
        print(slug)
        spec, errors = load_manifest(slug, repo_root, voices_dir, hosts_dir)
        if errors:
            for error in errors:
                print(f"  manifest error: {error}")
            continue
        assert spec is not None
        print(f"  manifest: {spec.manifest_file}")
        for state_file in spec.compact_state_files:
            print(f"  state set: {state_file}")
        for provenance_root in spec.provenance_roots:
            print(f"  provenance root: {provenance_root}")
        for source_set in spec.source_sets:
            print(f"  source set: {source_set.file} (expected {source_set.expected_count})")
        for matrix in spec.guest_matrices:
            print(f"  guest matrix: {matrix.file} (expected {matrix.expected_count})")

def promote_state_boundary_warnings(warnings: list[str]) -> tuple[list[str], list[str]]:
    promoted: list[str] = []
    remaining: list[str] = []
    for warning in warnings:
        if "missing WORK-only state boundary" in warning:
            promoted.append(warning)
        else:
            remaining.append(warning)
    return promoted, remaining

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--speaker", help="Validate one registered speaker slug.")
    parser.add_argument("--list", action="store_true", help="List registered speakers.")
    parser.add_argument(
        "--strict-warnings",
        action="store_true",
        help="Promote compact-state warnings to failures.",
    )
    parser.add_argument(
        "--strict-state-boundary",
        action="store_true",
        help="Promote compact-state boundary warnings to failures.",
    )
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT, help=argparse.SUPPRESS)
    parser.add_argument("--speakers-dir", type=Path, help=argparse.SUPPRESS)
    return parser.parse_args(argv)

def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = args.repo_root.resolve()
    voices_dir = (
        args.speakers_dir.resolve()
        if args.speakers_dir
        else repo_root / "statecraft" / "voices"
    )
    hosts_dir = DEFAULT_CHANNELS_DIR

    if args.list:
        list_registered(repo_root, voices_dir, hosts_dir)
        return 0

    errors, warnings = validate_all(repo_root, voices_dir, hosts_dir, speaker=args.speaker)
    if args.strict_state_boundary:
        promoted, warnings = promote_state_boundary_warnings(warnings)
        errors.extend(promoted)

    for warning in warnings:
        print(f"WARNING: {warning}", file=sys.stderr)
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)

    if errors:
        print(
            f"validate_speaker_state_sets: failed "
            f"({len(errors)} error(s), {len(warnings)} warning(s))",
            file=sys.stderr,
        )
        return 1
    if args.strict_warnings and warnings:
        print(
            f"validate_speaker_state_sets: failed "
            f"(0 error(s), {len(warnings)} warning(s) promoted)",
            file=sys.stderr,
        )
        return 1

    if warnings:
        print(f"validate_speaker_state_sets: OK ({len(warnings)} warning(s))", file=sys.stderr)
    else:
        print("validate_speaker_state_sets: OK", file=sys.stderr)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
