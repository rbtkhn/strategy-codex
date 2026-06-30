#!/usr/bin/env python3
"""Verify generated surfaces listed in generated-manifest.yaml."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / "generated-manifest.yaml"

ORPHAN_HEADER_RE = re.compile(r"<!--\s*GENERATED FILE", re.I)

ORPHAN_SCAN_ROOTS = (
    REPO_ROOT,
    REPO_ROOT / "docs",
    REPO_ROOT / "runtime" / "artifacts",
    REPO_ROOT / "statecraft",
    REPO_ROOT / "source-archive",
)

ORPHAN_SKIP_PREFIXES = (
    ".git/",
    ".codex-tmp/",
    "research/",
    "public/predictive-history/",
    "docs/templates/",
    "scripts/",
)

# Deferred enrollments — orphan scan warns only, never strict-fails
ORPHAN_DEFER_PREFIXES = (
    "docs/skill-work/work-dev/generated/",
    "runtime/artifacts/work-dev/",
)

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore[assignment]

@dataclass(frozen=True)
class ManifestEntry:
    entry_id: str
    path: str
    generator: str
    check_args: tuple[str, ...]
    drift_group: str | None
    header_type: str | None
    header_patterns: tuple[str, ...]

def _load_manifest(path: Path = MANIFEST_PATH) -> list[ManifestEntry]:
    if yaml is None:
        raise RuntimeError("PyYAML required; install requirements-dev.txt")
    if not path.is_file():
        raise FileNotFoundError(f"missing manifest: {path.relative_to(REPO_ROOT)}")

    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("generated-manifest.yaml must be a mapping")
    entries = raw.get("entries")
    if not isinstance(entries, list) or not entries:
        raise ValueError("generated-manifest.yaml must define a non-empty entries list")

    out: list[ManifestEntry] = []
    seen_ids: set[str] = set()
    seen_paths: set[str] = set()
    for item in entries:
        if not isinstance(item, dict):
            raise ValueError("each manifest entry must be a mapping")
        entry_id = str(item.get("id") or "").strip()
        rel_path = str(item.get("path") or "").strip().replace("\\", "/")
        generator = str(item.get("generator") or "").strip().replace("\\", "/")
        if not entry_id or not rel_path or not generator:
            raise ValueError("manifest entries require id, path, and generator")
        if entry_id in seen_ids:
            raise ValueError(f"duplicate manifest id: {entry_id}")
        if rel_path in seen_paths:
            raise ValueError(f"duplicate manifest path: {rel_path}")
        seen_ids.add(entry_id)
        seen_paths.add(rel_path)

        check_args_raw = item.get("check_args") or []
        if not isinstance(check_args_raw, list):
            raise ValueError(f"{entry_id}: check_args must be a list")
        check_args = tuple(str(part) for part in check_args_raw)

        header = item.get("header") or {}
        header_type = None
        header_patterns: tuple[str, ...] = ()
        if isinstance(header, dict) and header:
            header_type = str(header.get("type") or "").strip()
            patterns = header.get("patterns") or []
            if not isinstance(patterns, list) or not patterns:
                raise ValueError(f"{entry_id}: header.patterns must be a non-empty list")
            header_patterns = tuple(str(p) for p in patterns)

        drift_group = item.get("drift_group")
        drift_group_s = str(drift_group).strip() if drift_group else None

        gen_path = REPO_ROOT / generator
        if not gen_path.is_file():
            raise ValueError(f"{entry_id}: generator missing: {generator}")

        out.append(
            ManifestEntry(
                entry_id=entry_id,
                path=rel_path,
                generator=generator,
                check_args=check_args,
                drift_group=drift_group_s,
                header_type=header_type,
                header_patterns=header_patterns,
            )
        )
    return out

def _read_head(path: Path, *, max_lines: int = 12) -> str:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError):
        return ""
    return "\n".join(lines[:max_lines])

def _header_ok(entry: ManifestEntry, path: Path) -> list[str]:
    if not entry.header_type:
        return []
    text = path.read_text(encoding="utf-8") if path.suffix == ".json" else _read_head(path)
    if not text:
        return [f"{entry.entry_id}: unreadable or empty file"]
    missing = [pat for pat in entry.header_patterns if pat not in text]
    if missing:
        return [
            f"{entry.entry_id}: header missing pattern(s) in {entry.path}: "
            + ", ".join(repr(p) for p in missing)
        ]
    head = _read_head(path, max_lines=5)
    if ORPHAN_HEADER_RE.search(head):
        gen_name = Path(entry.generator).name
        if gen_name not in head:
            return [
                f"{entry.entry_id}: GENERATED FILE header in {entry.path} "
                f"does not name generator {entry.generator!r}"
            ]
    return []

def _drift_key(entry: ManifestEntry) -> tuple[str, tuple[str, ...], str | None]:
    return (entry.generator, entry.check_args, entry.drift_group)

def _run_drift_check(entry: ManifestEntry) -> list[str]:
    if not entry.check_args:
        return [f"{entry.entry_id}: no check_args; cannot verify drift"]
    cmd = [sys.executable, str(REPO_ROOT / entry.generator), *entry.check_args]
    proc = subprocess.run(
        cmd,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    if proc.returncode == 0:
        return []
    detail = (proc.stderr or proc.stdout or "").strip().splitlines()
    tail = detail[-1] if detail else f"exit {proc.returncode}"
    return [f"{entry.entry_id}: drift check failed ({entry.generator}): {tail}"]

def _is_deferred_orphan(rel_posix: str) -> bool:
    return any(prefix in rel_posix for prefix in ORPHAN_DEFER_PREFIXES)

def _iter_orphan_candidates() -> list[Path]:
    paths: set[Path] = set()
    for root in ORPHAN_SCAN_ROOTS:
        if not root.is_dir():
            continue
        for path in root.rglob("*.md"):
            if not path.is_file():
                continue
            rel = path.relative_to(REPO_ROOT).as_posix()
            if rel.startswith(".git/") or "/node_modules/" in rel:
                continue
            if any(rel.startswith(prefix) for prefix in ORPHAN_SKIP_PREFIXES):
                continue
            paths.add(path)
    return sorted(paths)

def collect_orphan_issues(
    manifest_paths: set[str],
    *,
    strict_orphans: bool,
) -> list[str]:
    issues: list[str] = []
    for path in _iter_orphan_candidates():
        rel = path.relative_to(REPO_ROOT).as_posix()
        head = _read_head(path, max_lines=5)
        if not ORPHAN_HEADER_RE.search(head):
            continue
        if rel in manifest_paths:
            continue
        if _is_deferred_orphan(rel):
            issues.append(f"orphan (deferred): {rel} has GENERATED FILE header but not in manifest")
            continue
        issues.append(f"orphan: {rel} has GENERATED FILE header but not in manifest")
    if strict_orphans:
        return [i for i in issues if not i.startswith("orphan (deferred):")]
    return issues

def collect_issues(*, run_drift: bool, run_orphans: bool, strict_orphans: bool) -> list[str]:
    issues: list[str] = []
    entries = _load_manifest()
    manifest_paths = {entry.path for entry in entries}
    drift_ran: set[tuple[str, tuple[str, ...], str | None]] = set()

    for entry in entries:
        target = REPO_ROOT / entry.path
        if not target.is_file():
            issues.append(f"{entry.entry_id}: missing generated surface: {entry.path}")
            continue
        issues.extend(_header_ok(entry, target))

        if not run_drift:
            continue
        key = _drift_key(entry)
        if key in drift_ran:
            continue
        drift_ran.add(key)
        issues.extend(_run_drift_check(entry))

    if run_orphans:
        issues.extend(collect_orphan_issues(manifest_paths, strict_orphans=strict_orphans))

    return issues

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Run generator drift checks (default when neither --headers-only nor --manifest-only)",
    )
    parser.add_argument(
        "--headers-only",
        action="store_true",
        help="Verify manifest paths and header conventions only",
    )
    parser.add_argument(
        "--manifest-only",
        action="store_true",
        help="Validate manifest schema and generator paths only",
    )
    parser.add_argument(
        "--orphans-only",
        action="store_true",
        help="Scan for GENERATED FILE headers not listed in manifest",
    )
    parser.add_argument(
        "--strict-orphans",
        action="store_true",
        help="Exit 1 on undeclared GENERATED FILE headers (deferred paths still warn only)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 when any issue is found (default: warn on stderr, exit 0)",
    )
    args = parser.parse_args()

    if args.manifest_only:
        try:
            count = len(_load_manifest())
        except (OSError, ValueError, RuntimeError) as exc:
            print(f"generated-surfaces: {exc}", file=sys.stderr)
            return 1 if args.strict else 0
        print(f"ok: generated-manifest.yaml valid ({count} entries)")
        return 0

    if args.orphans_only:
        try:
            entries = _load_manifest()
            issues = collect_orphan_issues(
                {e.path for e in entries},
                strict_orphans=args.strict_orphans or args.strict,
            )
        except (OSError, ValueError, RuntimeError) as exc:
            print(f"generated-surfaces: {exc}", file=sys.stderr)
            return 1 if args.strict else 0
        if issues:
            for issue in issues:
                print(f"generated-surfaces: {issue}", file=sys.stderr)
            print(f"generated-surfaces: {len(issues)} issue(s)", file=sys.stderr)
            fail = args.strict or args.strict_orphans
            deferred_only = all(i.startswith("orphan (deferred):") for i in issues)
            return 1 if fail and not deferred_only else 0
        print("ok: generated surface orphan scan passed")
        return 0

    run_drift = args.check or (not args.headers_only and not args.manifest_only)
    run_orphans = run_drift or args.headers_only
    try:
        issues = collect_issues(
            run_drift=run_drift,
            run_orphans=run_orphans,
            strict_orphans=args.strict_orphans,
        )
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"generated-surfaces: {exc}", file=sys.stderr)
        return 1 if args.strict else 0

    if issues:
        for issue in issues:
            print(f"generated-surfaces: {issue}", file=sys.stderr)
        print(f"generated-surfaces: {len(issues)} issue(s)", file=sys.stderr)
        if args.strict:
            blocking = [i for i in issues if not i.startswith("orphan (deferred):")]
            if blocking:
                return 1
            mode_parts = ["headers"]
            if run_drift:
                mode_parts.append("drift")
            if run_orphans:
                mode_parts.append("orphans")
            print(
                f"ok: generated surfaces check passed ({'+'.join(mode_parts)}; deferred orphan warnings only)"
            )
            return 0
        return 0

    mode_parts = ["headers"]
    if run_drift:
        mode_parts.append("drift")
    if run_orphans:
        mode_parts.append("orphans")
    print(f"ok: generated surfaces check passed ({'+'.join(mode_parts)})")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
