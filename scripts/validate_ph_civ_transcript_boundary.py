#!/usr/bin/env python3
"""Block unintentional edits to PH-CIV lecture transcript SSOT in the embedded mirror."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

MIRROR_REL = "statecraft/civ-lens/jiang/ph-civ"
MIRROR_ROOT = REPO_ROOT / MIRROR_REL

ESCAPE_ENV = "PH_CIV_TRANSCRIPT_EDIT"
ESCAPE_COMMIT_TOKEN = "PH-TRANSCRIPT-EDIT:"

ALLOWED_MAINTENANCE_PATHS = frozenset(
    {
        "scripts/validate_ph_civ_transcript_boundary.py",
        "scripts/validate_transcript_proper_nouns.py",
        "scripts/generate_ph_civ_asr_blocklist.py",
        "tests/test_validate_ph_civ_transcript_boundary.py",
        "tests/test_validate_transcript_proper_nouns.py",
        ".pre-commit-config.yaml",
        ".cursor/rules/ph-civ-transcript-immutability.mdc",
        "statecraft/civ-lens/jiang/jiang-routing.md",
        "statecraft/civ-lens/jiang/ph-civ/data/asr-blocklist/volume-ii-pilot.json",
    }
)

MIRROR_RELATIVE_PREFIXES = (
    "book/",
    "ph-civ/",
    "ph-apo/",
    "ph-mus/",
    "corpus/",
    "data/",
)


def normalize_repo_path(path: str) -> str:
    normalized = path.replace("\\", "/").lstrip("./")
    return re.sub(r"/+", "/", normalized)


def escape_hatch_open() -> bool:
    if os.environ.get(ESCAPE_ENV) == "1":
        return True
    try:
        head_msg = subprocess.run(
            ["git", "log", "-1", "--format=%B"],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            check=False,
        )
        if ESCAPE_COMMIT_TOKEN in (head_msg.stdout or ""):
            return True
    except OSError:
        pass
    return False


def is_protected_transcript_path(path: str) -> bool:
    norm = normalize_repo_path(path)
    if norm in ALLOWED_MAINTENANCE_PATHS:
        return False
    if norm.endswith("-transcript.md"):
        if norm.startswith(f"{MIRROR_REL}/"):
            return True
        if any(norm.startswith(prefix) for prefix in MIRROR_RELATIVE_PREFIXES):
            return True
    return False


def classify_paths(paths: list[str]) -> tuple[list[str], list[str]]:
    blocked: list[str] = []
    allowed: list[str] = []
    for raw_path in paths:
        path = normalize_repo_path(raw_path.strip())
        if not path:
            continue
        if is_protected_transcript_path(path):
            blocked.append(path)
        else:
            allowed.append(path)
    return blocked, allowed


def git_name_only(args: list[str], cwd: Path) -> list[str]:
    result = subprocess.run(
        ["git", *args],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "unknown git error"
        raise RuntimeError(f"git {' '.join(args)} failed in {cwd}: {detail}")
    return [line for line in result.stdout.splitlines() if line.strip()]


def get_changed_files_from_staged() -> list[str]:
    paths = git_name_only(["diff", "--cached", "--name-only"], REPO_ROOT)
    if MIRROR_ROOT.is_dir():
        for sub_path in git_name_only(["diff", "--cached", "--name-only"], MIRROR_ROOT):
            paths.append(f"{MIRROR_REL}/{normalize_repo_path(sub_path)}")
    return paths


def get_changed_files_from_diff(diff_spec: str) -> list[str]:
    paths = git_name_only(["diff", "--name-only", diff_spec], REPO_ROOT)
    if MIRROR_ROOT.is_dir():
        for sub_path in git_name_only(["diff", "--name-only", diff_spec], MIRROR_ROOT):
            paths.append(f"{MIRROR_REL}/{normalize_repo_path(sub_path)}")
    return paths


def format_violation_message(blocked: list[str]) -> str:
    lines = [
        "PH-CIV transcript boundary violation:",
        f"  Lecture transcript SSOT (`*-transcript.md`) under `{MIRROR_REL}/` must not change",
        "  during commentary, corridor, or synthesis work.",
        "",
        "Blocked paths:",
    ]
    lines.extend(f"  - {path}" for path in blocked)
    lines.extend(
        [
            "",
            "Allowed edit surfaces:",
            "  - *-commentary.md, cards, corridors, orientation YAML",
            "  - line references (e.g. civ-07-transcript.md:90-93), not body rewrites",
            "",
            "To commit an intentional transcript change:",
            f"  - set {ESCAPE_ENV}=1, or",
            f"  - include `{ESCAPE_COMMIT_TOKEN} <reason>` in the commit message",
            "  - operator must have named a transcript lane (re-import, materialize, cleanup skill)",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--diff", help="Git diff spec to inspect, e.g. BASE...HEAD")
    group.add_argument("--staged", action="store_true", help="Inspect staged changes (parent + mirror submodule)")
    group.add_argument("--files", nargs="*", default=None, help="Explicit repo-relative paths")
    args = parser.parse_args()

    if args.diff:
        paths = get_changed_files_from_diff(args.diff)
    elif args.staged:
        paths = get_changed_files_from_staged()
    else:
        paths = args.files or []

    blocked, _allowed = classify_paths(paths)
    if blocked and not escape_hatch_open():
        print(format_violation_message(blocked), file=sys.stderr)
        return 1

    if blocked and escape_hatch_open():
        print(
            f"PH-CIV transcript boundary: escape hatch open; "
            f"{len(blocked)} transcript path(s) allowed."
        )
        return 0

    print(
        f"PH-CIV transcript boundary OK: {len(paths)} path(s) inspected, "
        "no protected transcript edits."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
