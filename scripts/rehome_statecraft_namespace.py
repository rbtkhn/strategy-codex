#!/usr/bin/env python3
"""Rehome statecraft/civ-lens -> voices and statecraft/civ-state -> states."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

GLOB_SUFFIXES = (".md", ".py", ".json", ".yaml", ".yml", ".mdc", ".toml")

REPLACEMENTS = (
    (r"statecraft\civ-lens", r"statecraft\voices"),
    (r"statecraft\civ-state", r"statecraft\states"),
    ("statecraft/civ-lens", "statecraft/voices"),
    ("statecraft/civ-state", "statecraft/states"),
    ("../../../civ-lens/", "../../../voices/"),
    ("../../civ-lens/", "../../voices/"),
    ("../civ-lens/", "../voices/"),
    ("../../../civ-state/", "../../../states/"),
    ("../../civ-state/", "../../states/"),
    ("../civ-state/", "../states/"),
    ("(civ-state/", "(states/"),
)

DEFAULT_EXCLUDE_PREFIXES = (
    "runtime/artifacts/benchmarks/",
)

SPECIAL_FILES = (
    REPO_ROOT / "self-library.md",
    REPO_ROOT / "repo-map.yaml",
    REPO_ROOT / ".gitmodules",
)


def _excluded(rel_posix: str, include_benchmarks: bool) -> bool:
    if include_benchmarks:
        return False
    return any(rel_posix.startswith(p) for p in DEFAULT_EXCLUDE_PREFIXES)


def iter_files(include_benchmarks: bool) -> list[Path]:
    import subprocess

    proc = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=REPO_ROOT,
        capture_output=True,
        check=False,
    )
    files: list[Path] = []
    if proc.returncode == 0:
        for raw in proc.stdout.split(b"\0"):
            if not raw:
                continue
            rel = raw.decode("utf-8", errors="replace")
            if not rel:
                continue
            suffix = Path(rel).suffix.lower()
            if suffix not in GLOB_SUFFIXES and rel != ".gitmodules":
                continue
            if _excluded(rel, include_benchmarks):
                continue
            # Submodule corpus: parent repo path strings only; bridge URLs in phase 4.
            if rel.startswith("statecraft/civ-lens/jiang/ph-civ/") or rel.startswith(
                "public/predictive-history/"
            ):
                continue
            fp = REPO_ROOT / rel
            if fp.is_file():
                files.append(fp)
    else:
        for path in REPO_ROOT.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix.lower() not in GLOB_SUFFIXES:
                continue
            try:
                rel = path.relative_to(REPO_ROOT).as_posix()
            except ValueError:
                continue
            if _excluded(rel, include_benchmarks):
                continue
            if "jiang/ph-civ/" in rel:
                continue
            files.append(path)
    return sorted(set(files))


def apply_replacements(text: str) -> tuple[str, int]:
    count = 0
    for old, new in REPLACEMENTS:
        if old in text:
            n = text.count(old)
            text = text.replace(old, new)
            count += n
    return text, count


def cmd_dry_run(include_benchmarks: bool) -> int:
    total_hits = 0
    files_with_hits = 0
    by_pattern: dict[str, int] = {old: 0 for old, _ in REPLACEMENTS}

    for fp in iter_files(include_benchmarks):
        try:
            text = fp.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        file_hits = 0
        for old, _ in REPLACEMENTS:
            n = text.count(old)
            if n:
                by_pattern[old] += n
                file_hits += n
        if file_hits:
            files_with_hits += 1
            total_hits += file_hits
            print(f"  {fp.relative_to(REPO_ROOT)} ({file_hits})")

    print(f"\n## Dry-run receipt")
    print(f"files_with_hits: {files_with_hits}")
    print(f"total_replacements: {total_hits}")
    for old, n in by_pattern.items():
        if n:
            print(f"  {old}: {n}")

    for special in SPECIAL_FILES:
        if special.is_file():
            text = special.read_text(encoding="utf-8", errors="replace")
            hits = sum(text.count(old) for old, _ in REPLACEMENTS)
            print(f"special {special.relative_to(REPO_ROOT)}: {hits} hit(s)")

    return 0


def cmd_apply(include_benchmarks: bool) -> int:
    total = 0
    changed = 0
    for fp in iter_files(include_benchmarks):
        try:
            text = fp.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError) as exc:
            print(f"skip {fp}: {exc}", file=sys.stderr)
            continue
        new_text, n = apply_replacements(text)
        if n:
            fp.write_text(new_text, encoding="utf-8")
            total += n
            changed += 1
            print(f"apply: {fp.relative_to(REPO_ROOT)} ({n})")
    print(f"\napply done: {total} replacement(s) in {changed} file(s)")
    return 0


def cmd_check(include_benchmarks: bool) -> int:
    offenders: list[tuple[str, int]] = []
    patterns = [old for old, _ in REPLACEMENTS]

    for fp in iter_files(include_benchmarks):
        try:
            text = fp.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        hits = sum(text.count(p) for p in patterns)
        if hits:
            offenders.append((fp.relative_to(REPO_ROOT).as_posix(), hits))

    if offenders:
        print("STALE PATH GATE FAILED:", file=sys.stderr)
        for rel, hits in sorted(offenders):
            print(f"  {rel} ({hits})", file=sys.stderr)
        return 1

    print("check ok: no statecraft/civ-lens or statecraft/civ-state outside exclusions")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--apply", action="store_true")
    mode.add_argument("--check", action="store_true")
    ap.add_argument(
        "--include-benchmarks",
        action="store_true",
        help="Include runtime/artifacts/benchmarks/ in scan/replace/check",
    )
    args = ap.parse_args()

    if args.dry_run:
        return cmd_dry_run(args.include_benchmarks)
    if args.apply:
        return cmd_apply(args.include_benchmarks)
    return cmd_check(args.include_benchmarks)


if __name__ == "__main__":
    raise SystemExit(main())
