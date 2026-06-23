#!/usr/bin/env python3
"""Rename Diesen-host / Davis-guest captures to source-glenn-diesen-daniel-davis-* prefix."""
from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ARCHIVE = REPO / "source-archive" / "statecraft"
SCAN_ROOTS = [
    REPO / "statecraft",
    REPO / "codex",
    REPO / "docs",
    ARCHIVE,
]
TEXT_EXTENSIONS = {".md", ".json", ".py", ".jsonl", ".txt", ".yaml", ".yml"}
SKIP_DIR_NAMES = {"runtime", ".git", "node_modules", "scripts"}

# Old basename -> new basename (Davis-host 2026-03-11 intentionally excluded).
RENAMES: dict[str, str] = {
    "source-daniel-davis-diesen-iran-knife-edge-2026-02-07.md": (
        "source-glenn-diesen-daniel-davis-iran-knife-edge-2026-02-07.md"
    ),
    "source-daniel-davis-diesen-iran-miscalculation-2026-03-01.md": (
        "source-glenn-diesen-daniel-davis-iran-miscalculation-2026-03-01.md"
    ),
    "source-daniel-davis-diesen-military-options-kent-2026-03-18.md": (
        "source-glenn-diesen-daniel-davis-military-options-kent-2026-03-18.md"
    ),
    "source-daniel-davis-diesen-trump-war-speech-2026-04-02.md": (
        "source-glenn-diesen-daniel-davis-trump-war-speech-2026-04-02.md"
    ),
}


def collect_file_renames() -> list[tuple[Path, Path]]:
    pairs: list[tuple[Path, Path]] = []
    for old_name, new_name in RENAMES.items():
        matches = list(ARCHIVE.rglob(old_name))
        if len(matches) != 1:
            raise SystemExit(f"expected 1 match for {old_name}, found {len(matches)}")
        old_path = matches[0]
        new_path = old_path.with_name(new_name)
        if new_path.exists():
            raise SystemExit(f"target already exists: {new_path}")
        pairs.append((old_path, new_path))
    return pairs


def apply_renames(pairs: list[tuple[Path, Path]]) -> None:
    for old, new in pairs:
        old.rename(new)
    print(f"Renamed {len(pairs)} capture files")


def patch_frontmatter(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return False
    end = text.find("---", 3)
    if end < 0:
        return False
    fm = text[3:end]
    if re.search(r"^channel_slug:\s*glenn-diesen\s*$", fm, re.MULTILINE):
        return False
    host = re.search(r"^host:\s*Glenn Diesen\s*$", fm, re.MULTILINE)
    if not host:
        return False
    insert_at = host.end()
    new_fm = fm[:insert_at] + "\nchannel_slug: glenn-diesen" + fm[insert_at:]
    path.write_text("---" + new_fm + text[end:], encoding="utf-8")
    return True


def patch_text_references() -> int:
    replacements = [(old, new) for old, new in RENAMES.items()]
    patched = 0
    for root in SCAN_ROOTS:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file() or path.suffix not in TEXT_EXTENSIONS:
                continue
            if any(part in SKIP_DIR_NAMES for part in path.parts):
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            new_text = text
            for old, new in replacements:
                new_text = new_text.replace(old, new)
            if new_text != text:
                path.write_text(new_text, encoding="utf-8")
                patched += 1
    return patched


def main() -> int:
    pairs = collect_file_renames()
    apply_renames(pairs)
    slugged = sum(1 for _, new in pairs if patch_frontmatter(new))
    patched = patch_text_references()
    print(f"Added channel_slug on {slugged} captures")
    print(f"Patched {patched} reference files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
