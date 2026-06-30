#!/usr/bin/env python3
"""Enforce Predictive History as an external, read-only project in strategy-codex."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

FROZEN_PREFIXES = (
    "codex/predictive-history/",
    "research/external/youtube-channels/predictive-history/",
)

ALLOWED_FROZEN_PATHS = frozenset(
    {
        "codex/predictive-history/README.md",
        "codex/predictive-history/README-operator.md",
        "codex/years/2026/supporting-voices/jiang/jiang-profile.md",
        "research/external/youtube-channels/predictive-history/README.md",
        "research/external/work-strategy/transcripts/README.md",
        "docs/predictive-history-external-boundary.md",
        "docs/skill-work/work-strategy/predictive-history-review-packets.md",
        "docs/skill-work/work-strategy/daily-brief-jiang-layer.md",
        "AGENTS.md",
        "scripts/validate_predictive_history_boundary.py",
        "scripts/work_jiang/rebuild_all.py",
        ".github/workflows/work-jiang.yml",
        ".github/workflows/test.yml",
        "tests/test_validate_predictive_history_boundary.py",
    }
)

def normalize_repo_path(path: str) -> str:
    normalized = path.replace("\\", "/").lstrip("./")
    return re.sub(r"/+", "/", normalized)

def classify_paths(paths: list[str]) -> tuple[list[str], list[str]]:
    blocked: list[str] = []
    allowed: list[str] = []
    for raw_path in paths:
        path = normalize_repo_path(raw_path.strip())
        if not path:
            continue
        if any(path.startswith(prefix) for prefix in FROZEN_PREFIXES):
            if path in ALLOWED_FROZEN_PATHS:
                allowed.append(path)
            else:
                blocked.append(path)
    return blocked, allowed

def get_changed_files_from_diff(diff_spec: str) -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--name-only", diff_spec],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"git diff failed for {diff_spec!r}")
    return [line for line in result.stdout.splitlines() if line.strip()]

def get_changed_files_from_staged() -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git diff --cached failed")
    return [line for line in result.stdout.splitlines() if line.strip()]

def format_violation_message(blocked: list[str], allowed: list[str]) -> str:
    lines = [
        "Predictive History boundary violation:",
        "  `rbtkhn/predictive-history` is now the canonical public Predictive History repo.",
        "  It contains the public two-volume PH artifact: ph-civ, ph-apo, and ph-mus.",
        "  `strategy-codex` may review, observe, critique, and cite public ph-civ IDs,",
        "  but it must not mutate the frozen legacy PH trees in this repo.",
        "  Treat `rbtkhn/ph-workshop` as legacy workshop/import provenance unless explicitly invoked.",
        "",
        "Blocked paths:",
    ]
    lines.extend(f"  - {path}" for path in blocked)
    if allowed:
        lines.extend(["", "Allowed boundary-maintenance paths in this change:"])
        lines.extend(f"  - {path}" for path in allowed)
    lines.extend(
        [
            "",
            "Allowed work here:",
            "  - boundary docs and migration notices",
            "  - validator / CI guardrail maintenance",
            "  - review packets and critique outside the frozen PH trees",
            "  - public ph-civ source_id, pattern_id, and route references",
            "",
            "Move canonical public Predictive History edits to `rbtkhn/predictive-history` instead.",
        ]
    )
    return "\n".join(lines)

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--diff", help="Git diff spec to inspect, e.g. BASE...HEAD")
    group.add_argument("--staged", action="store_true", help="Inspect staged changes")
    group.add_argument("--files", nargs="*", default=None, help="Explicit repo-relative paths")
    args = parser.parse_args()

    if args.diff:
        paths = get_changed_files_from_diff(args.diff)
    elif args.staged:
        paths = get_changed_files_from_staged()
    else:
        paths = args.files or []

    blocked, allowed = classify_paths(paths)
    if blocked:
        print(format_violation_message(blocked, allowed), file=sys.stderr)
        return 1

    print(
        f"Predictive History boundary OK: {len(paths)} path(s) inspected, "
        f"{len(allowed)} frozen-path maintenance change(s) allowed."
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
