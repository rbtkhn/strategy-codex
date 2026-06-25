#!/usr/bin/env python3
"""Finish ph-mus removal in public/predictive-history mirror (strategy-codex only)."""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MIRROR = REPO / "public" / "ph-civ"
CLI = MIRROR / "src" / "civ_ph" / "cli.py"
DATA = MIRROR / "src" / "civ_ph" / "data.py"

DOC_REPLACEMENTS = [
    (
        "It contains three related Predictive History surfaces:",
        "It contains two related Predictive History surfaces:",
    ),
    (
        "- `ph-mus`: **Predictive History Museum** - chapter exhibit layer for both volumes.\n\n",
        "",
    ),
    (
        "The repo as a whole is the two-volume public artifact: `ph-civ`, `ph-apo`, and `ph-mus` together.",
        "The repo as a whole is the two-volume public artifact: `ph-civ` and `ph-apo`.",
    ),
    (
        "`ph-civ`, `ph-apo`, and `ph-mus`",
        "`ph-civ` and `ph-apo`",
    ),
    (
        "three surfaces",
        "two surfaces",
    ),
    (
        "three public surfaces",
        "two public surfaces",
    ),
    (
        "ph-mus is the exhibit layer for both volumes",
        "chapter folders and study edition are the reader surfaces",
    ),
    (
        "open the ph-mus museum room for civ-07",
        "study civ-07 through its chapter folder",
    ),
    (
        "open the ph-mus museum room for the current route",
        "study the current route through its chapter folder",
    ),
    (
        "`ph-mus` is not a third volume",
        "two-volume public artifact",
    ),
    (
        "ph-mus is not a third volume",
        "two-volume public artifact",
    ),
    (
        "ph-mus` is not a third volume",
        "two-volume public artifact",
    ),
    (
        "corpus/media-packs/civ-07.md` when discussing the future museum room",
        "book/volume-ii/civ-07/civ-07-commentary.md` for the commentary canvas",
    ),
    (
        "Museum artifacts must be stored in a local museum vault and mirrored in a shared document cloud workspace. Git tracks manifests, exhibit metadata, derived thumbnails when appropriate, and validation rules, not the full artifact archive.",
        "Large media archives stay outside Git; this repo tracks transcripts, commentaries, cards, routes, and study navigation.",
    ),
    (
        "ph-mus exhibit readiness",
        "chapter study readiness",
    ),
    (
        "Public museum exhibit and artifact schemas.",
        "",
    ),
    (
        "Curator instructions for chapter-level exhibit assembly across both volumes.",
        "",
    ),
    (
        "Do not claim museum artifact binaries are stored in Git.",
        "",
    ),
    (
        "Do not claim ph-mus is a third volume.",
        "",
    ),
    (
        "ph-mus/README.md",
        "docs/archive/ph-mus-retired.md",
    ),
    (
        "schemas/museum-exhibit.schema.json",
        "",
    ),
    (
        "schemas/museum-artifact.schema.json",
        "",
    ),
    (
        "museum_room",
        "study",
    ),
    (
        "Design or review chapter exhibits through ph-mus schemas and manifest boundaries.",
        "Study one chapter through its card, transcript, commentary, limits, and return path.",
    ),
    (
        "Orient the reader to the two volumes, the museum layer, and the 10-route seed",
        "Orient the reader to the two volumes and the 10-route seed",
    ),
]

DOC_GLOBS = [
    "README.md",
    "START-HERE.md",
    "AGENTS.md",
    "llms.txt",
    "llms-full.txt",
    "CONTRIBUTING.md",
    "docs/*.md",
]


def patch_data_py() -> None:
    text = DATA.read_text(encoding="utf-8")
    text = re.sub(
        r"\ndef load_museum_index\(\) -> list\[dict\]:.*?^\s+\[\"exhibits\"\]\)\n",
        "\n",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    DATA.write_text(text, encoding="utf-8")


def patch_cli_validate_markers() -> None:
    text = CLI.read_text(encoding="utf-8")
    text = text.replace(
        '            "`ph-mus` is not a third volume",\n',
        '            "two-volume public artifact",\n',
    )
    text = text.replace(
        '            "ph-mus` is not a third volume",\n',
        '            "two-volume public artifact",\n',
    )
    CLI.write_text(text, encoding="utf-8")


def update_docs() -> int:
    count = 0
    paths: list[Path] = []
    for pattern in DOC_GLOBS:
        paths.extend(MIRROR.glob(pattern))
    paths = sorted({p for p in paths if p.is_file() and "ph-mus-retired" not in p.name})
    for path in paths:
        text = path.read_text(encoding="utf-8")
        original = text
        for old, new in DOC_REPLACEMENTS:
            text = text.replace(old, new)
        text = re.sub(r"\n{3,}", "\n\n", text)
        if text != original:
            path.write_text(text, encoding="utf-8")
            count += 1
    return count


def main() -> int:
    patch_data_py()
    patch_cli_validate_markers()
    updated = update_docs()
    print(f"Updated {updated} doc files; patched data.py and cli validate markers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
