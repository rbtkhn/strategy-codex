#!/usr/bin/env python3
"""Rewrite singularity/research paths to research/narrative-systems after layout migration."""

from __future__ import annotations

import argparse
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Longest match first.
SUBSTITUTIONS: list[tuple[str, str]] = [
    (
        "singularity/research/narrative-systems/model-relations/",
        "research/narrative-systems/04_mappings/model_relations/",
    ),
    (
        "singularity/research/epistemic-geometry/",
        "research/narrative-systems/05_geometric_lenses/epistemic_geometry/",
    ),
    (
        "singularity/research/predictive-history/",
        "research/narrative-systems/03_core_models/predictive_history/",
    ),
    (
        "singularity/research/civilization-state/",
        "research/narrative-systems/03_core_models/civilization_state/",
    ),
    (
        "singularity/research/narrative-systems/",
        "research/narrative-systems/02_narrative_systems/",
    ),
    ("singularity/research/", "research/narrative-systems/"),
    ("../epistemic-geometry/", "../05_geometric_lenses/epistemic_geometry/"),
    ("../predictive-history/", "../03_core_models/predictive_history/"),
    ("../civilization-state/", "../03_core_models/civilization_state/"),
    ("../../predictive-history/", "../../03_core_models/predictive_history/"),
    ("../../epistemic-geometry/", "../../05_geometric_lenses/epistemic_geometry/"),
    ("../../civilization-state/", "../../03_core_models/civilization_state/"),
]

SCAN_ROOTS: tuple[Path, ...] = (
    REPO_ROOT / "research" / "narrative-systems",
    REPO_ROOT / "singularity",
    REPO_ROOT / "docs",
    REPO_ROOT / "continuity",
)


def rewrite_text(text: str) -> tuple[str, int]:
    count = 0
    for old, new in SUBSTITUTIONS:
        if old in text:
            n = text.count(old)
            text = text.replace(old, new)
            count += n
    return text, count


def iter_markdown_files() -> list[Path]:
    files: list[Path] = []
    for root in SCAN_ROOTS:
        if not root.is_dir():
            continue
        files.extend(sorted(root.rglob("*.md")))
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description="Rewrite narrative-systems research path refs")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    if not args.dry_run and not args.apply:
        parser.error("Specify --dry-run or --apply")

    total = 0
    changed_files = 0
    for path in iter_markdown_files():
        try:
            original = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            print(f"skip non-utf8: {path.relative_to(REPO_ROOT)}")
            continue
        updated, n = rewrite_text(original)
        if n == 0:
            continue
        rel = path.relative_to(REPO_ROOT)
        if args.dry_run:
            print(f"would update {rel} ({n} substitution(s))")
        else:
            path.write_text(updated, encoding="utf-8")
            print(f"updated {rel} ({n} substitution(s))")
        total += n
        changed_files += 1

    print(f"done: {changed_files} file(s), {total} substitution(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
