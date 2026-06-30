#!/usr/bin/env python3
"""Normalize Daniel Davis capture filenames to source-daniel-davis-* prefix."""
from __future__ import annotations

import json
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
TEXT_EXTENSIONS = {".md", ".json", ".jsonl", ".txt", ".yaml", ".yml"}
SKIP_DIR_NAMES = {"runtime", ".git", "node_modules", "scripts"}

def target_name(name: str) -> str | None:
    if name.startswith("source-daniel-davis-deep-dive-"):
        return "source-daniel-davis-" + name[len("source-daniel-davis-deep-dive-") :]
    if name.startswith("source-davis-"):
        return "source-daniel-davis-" + name[len("source-davis-") :]
    if name.startswith("source-deep-dive-"):
        return "source-daniel-davis-" + name[len("source-deep-dive-") :]
    if name.startswith("source-daniel-davis-"):
        return None
    return None

def collect_renames() -> list[tuple[Path, Path]]:
    renames: list[tuple[Path, Path]] = []
    for path in ARCHIVE.rglob("*.md"):
        if "_land_" in path.parts or path.name == "header.md":
            continue
        new_name = target_name(path.name)
        if not new_name or new_name == path.name:
            continue
        renames.append((path, path.with_name(new_name)))
    targets: dict[Path, list[Path]] = {}
    for old, new in renames:
        targets.setdefault(new, []).append(old)
    collisions = {k: v for k, v in targets.items() if len(v) > 1}
    if collisions:
        lines = [f"collision {k.name}: {[p.name for p in v]}" for k, v in collisions.items()]
        raise SystemExit("rename collisions:\n" + "\n".join(lines))
    return renames

def apply_renames(renames: list[tuple[Path, Path]]) -> None:
    for old, new in sorted(renames, key=lambda pair: len(str(pair[0]))):
        new.parent.mkdir(parents=True, exist_ok=True)
        old.rename(new)
    print(f"Renamed {len(renames)} capture files")

def patch_discovery_config() -> None:
    path = REPO / "platform" / "config" / "statecraft_youtube_discovery.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    prefixes: list[list[str]] = data.get("filename_prefix_index_canonical", [])
    wanted = ["source-daniel-davis-", "daniel-davis"]
    if wanted not in prefixes:
        prefixes.insert(0, wanted)
    # Drop legacy short prefix once canonical prefix is primary.
    prefixes = [row for row in prefixes if row != ["source-davis-", "daniel-davis"]]
    data["filename_prefix_index_canonical"] = prefixes
    channel = next(c for c in data["channels"] if c["channel_key"] == "daniel-davis")
    channel["file_prefix"] = "source-daniel-davis"
    path.write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print("Updated statecraft_youtube_discovery.json")

def patch_text_references() -> int:
    replacements = [
        ("source-daniel-davis-deep-dive-", "source-daniel-davis-"),
        ("source-davis-", "source-daniel-davis-"),
        ("source-deep-dive-", "source-daniel-davis-"),
    ]
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

def normalize_legacy_threads() -> int:
    pattern = re.compile(r"^thread: daniel-davis(?:-deep-dive)?\s*$", re.MULTILINE)
    count = 0
    for path in ARCHIVE.rglob("source-daniel-davis-*.md"):
        text = path.read_text(encoding="utf-8")
        new_text = pattern.sub("thread: davis", text)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            count += 1
    return count

def main() -> int:
    renames = collect_renames()
    apply_renames(renames)
    patched = patch_text_references()
    threads = normalize_legacy_threads()
    patch_discovery_config()
    print(f"Patched {patched} reference files")
    print(f"Normalized {threads} legacy thread fields")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
