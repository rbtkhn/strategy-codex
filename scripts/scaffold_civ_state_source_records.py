#!/usr/bin/env python3
"""
Scaffold CIV-STATE source-record stubs from bibliography era files.

Usage:
  python scripts/scaffold_civ_state_source_records.py
  python scripts/scaffold_civ_state_source_records.py --write outdir
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VOLUMES_DIR = REPO_ROOT / "statecraft" / "civ-state" / "volumes"

def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")

def parse_sources(path: Path) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    sources: list[str] = []
    in_primary = False
    for raw in lines:
        line = raw.strip()
        if line == "## Primary Sources":
            in_primary = True
            continue
        if not in_primary:
            continue
        lowered = line.lower()
        if line == "## Retrieval Priority" or "retrieval priority:" in lowered:
            break
        if re.match(r"^\d+\.\s+", line):
            item = re.sub(r"^\d+\.\s+", "", line).strip()
            sources.append(item)
            continue
        if line.startswith("- "):
            item = line[2:].strip()
            if item.endswith(":"):
                continue
            sources.append(item)
    return sources

def build_stub(civ: str, era: str, title: str) -> dict[str, object]:
    source_id = slugify(f"{civ}-{era}-{title}")
    return {
        "source_id": source_id,
        "civilization": civ,
        "era": era,
        "branch": "TODO",
        "title": title,
        "author_or_body": "TODO",
        "source_type": "TODO",
        "date_or_range": "TODO",
        "original_language": "TODO",
        "target_language": "TODO",
        "witness_type": "academic_text",
        "canonical_witness": {"label": "TODO", "language": "TODO", "locator": "TODO"},
        "working_translation": None,
        "alternate_translations": [],
        "rights_class": "unclear",
        "storage_class": "metadata_only",
        "acquisition_method": "manual_first_scaffold",
        "witness_locator": "",
        "sidecar_locator": "",
        "canonical_excerpt_available": False,
        "full_text_available": False,
        "validation_status": "unvalidated",
        "notes": "Scaffold generated from bibliography source door."
    }

def collect() -> list[dict[str, object]]:
    stubs: list[dict[str, object]] = []
    for volume_dir in sorted(VOLUMES_DIR.iterdir()):
        if not volume_dir.is_dir() or not volume_dir.name.startswith("civ-state-"):
            continue
        civ = volume_dir.name.removeprefix("civ-state-")
        for source_file in sorted(volume_dir.glob(f"{volume_dir.name}-primary-sources-*.md")):
            era = source_file.stem.split("-")[-1]
            for title in parse_sources(source_file):
                stubs.append(build_stub(civ, era, title))
    return stubs

def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold CIV-STATE source-record stubs from bibliography files.")
    parser.add_argument("--write", type=Path, help="Write one JSON stub per source into the given directory")
    args = parser.parse_args()

    stubs = collect()
    if args.write:
        outdir = args.write
        outdir.mkdir(parents=True, exist_ok=True)
        for stub in stubs:
            path = outdir / f"{stub['source_id']}.json"
            path.write_text(json.dumps(stub, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Wrote {len(stubs)} source-record stubs to {outdir}")
        return 0

    print(json.dumps(stubs, indent=2, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
