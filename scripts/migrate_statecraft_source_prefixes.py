from repo_io import SKILLS_DIR
#!/usr/bin/env python3
"""Migrate canonical statecraft day-folder source files to the `source-` prefix."""

from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path

from statecraft_day_archive import guest_meta_values, infer_source_form, parse_frontmatter


REPO_ROOT = Path(__file__).resolve().parent.parent
ARCHIVE_ROOT = REPO_ROOT / "source-archive" / "statecraft"
DATE_DIR_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DATE_SUFFIX_RE = re.compile(r"-(\d{4}-\d{2}-\d{2})$")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", re.DOTALL)
TEXT_SUFFIXES = {
    ".json",
    ".jsonl",
    ".md",
    ".mdc",
    ".py",
    ".txt",
    ".yaml",
    ".yml",
}
COMPOUND_PREFIXES = (
    "judging-freedom-",
    "predictive-history-",
    "responsiblestatecraft-",
)


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="Report planned changes without mutating files.")
    return ap.parse_args()


def iter_day_source_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for day_dir in sorted(root.iterdir(), key=lambda path: path.name):
        if not day_dir.is_dir() or not DATE_DIR_RE.fullmatch(day_dir.name):
            continue
        for path in sorted(day_dir.glob("*.md"), key=lambda item: item.name):
            if path.name == "README.md":
                continue
            meta = parse_frontmatter(path)
            if not meta:
                continue
            if not any(meta.get(key) for key in ("kind", "source_type", "source_url", "publication", "show", "title")):
                continue
            files.append(path)
    return files


def strip_legacy_prefix(stem_without_date: str) -> str:
    if stem_without_date.startswith("source-"):
        return stem_without_date[len("source-") :]
    for prefix in COMPOUND_PREFIXES:
        if stem_without_date.startswith(prefix):
            return stem_without_date[len(prefix) :]
    if "-" not in stem_without_date:
        return stem_without_date
    return stem_without_date.split("-", 1)[1]


def target_name(path: Path) -> str:
    date = path.parent.name
    stem = path.stem
    stripped = DATE_SUFFIX_RE.sub("", stem)
    preserved = strip_legacy_prefix(stripped)
    return f"source-{preserved}-{date}.md"


def updated_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return text

    meta = parse_frontmatter(path)
    host_values = tuple(
        filter(
            None,
            (" ".join(str(v).split()).strip() for v in ((meta.get("host"),) if meta.get("host") else tuple(meta.get("hosts") or ()))),
        )
    )
    guests = guest_meta_values(meta)
    source_form = infer_source_form(meta, host_values, guests)

    lines = match.group(1).splitlines()
    replaced = False
    insert_at = None
    for idx, line in enumerate(lines):
        if re.match(r"^source_form:\s*", line):
            lines[idx] = f"source_form: {source_form}"
            replaced = True
            break
        if insert_at is None and re.match(r"^(source_type|kind):\s*", line):
            insert_at = idx + 1
    if not replaced:
        if insert_at is None:
            lines.append(f"source_form: {source_form}")
        else:
            lines.insert(insert_at, f"source_form: {source_form}")

    rebuilt = "---\n" + "\n".join(lines) + "\n---"
    return rebuilt + text[match.end() - 1 :]


def build_path_mapping(paths: list[Path]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    targets: Counter[str] = Counter()
    for path in paths:
        new_name = target_name(path)
        new_path = path.with_name(new_name)
        rel_old = path.relative_to(REPO_ROOT).as_posix()
        rel_new = new_path.relative_to(REPO_ROOT).as_posix()
        mapping[rel_old] = rel_new
        mapping[path.name] = new_name
        mapping[path.as_posix()] = new_path.as_posix()
        mapping[f"/{path.as_posix()}"] = f"/{new_path.as_posix()}"
        targets[rel_new] += 1
    collisions = [rel_path for rel_path, count in targets.items() if count > 1]
    if collisions:
        raise SystemExit("target-name collisions detected:\n" + "\n".join(collisions))
    return mapping


def iter_text_files() -> list[Path]:
    roots = [
        REPO_ROOT / ".cursor" / "skills",
        REPO_ROOT / "codex",
        REPO_ROOT / "docs",
        REPO_ROOT / "scripts",
        SKILLS_DIR,
        REPO_ROOT / "source-archive" / "statecraft",
        REPO_ROOT / "statecraft",
    ]
    files: list[Path] = []
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
                continue
            files.append(path)
    return files


def replace_refs(text: str, mapping: dict[str, str]) -> str:
    updated = text
    for old, new in mapping.items():
        if old in updated:
            updated = updated.replace(old, new)
    return updated


def main() -> int:
    args = parse_args()
    source_files = iter_day_source_files(ARCHIVE_ROOT)
    mapping = build_path_mapping(source_files)

    changed_texts = 0
    renamed = 0
    for path in source_files:
        new_text = updated_text(path)
        old_text = path.read_text(encoding="utf-8-sig", errors="replace")
        if new_text != old_text:
            changed_texts += 1
            if not args.check:
                path.write_text(new_text, encoding="utf-8", newline="\n")

    for path in source_files:
        new_path = path.with_name(target_name(path))
        if new_path == path:
            continue
        renamed += 1
        if not args.check:
            path.rename(new_path)

    replaced_files = 0
    for path in iter_text_files():
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        updated = replace_refs(text, mapping)
        if updated != text:
            replaced_files += 1
            if not args.check:
                path.write_text(updated, encoding="utf-8", newline="\n")

    if args.check:
        print(f"would update source_form in {changed_texts} files")
        print(f"would rename {renamed} files")
        print(f"would rewrite references in {replaced_files} files")
        return 0

    print(f"updated source_form in {changed_texts} files")
    print(f"renamed {renamed} files")
    print(f"rewrote references in {replaced_files} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
