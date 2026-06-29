from repo_io import SKILLS_DIR
#!/usr/bin/env python3
"""Migrate codex/speakers/ into statecraft/voices/ and statecraft/channels/.

WORK only. Emits a JSON receipt for link rewrite. Use --plan before --apply.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CODEX_SPEAKERS = REPO_ROOT / "codex" / "speakers"
VOICES = REPO_ROOT / "statecraft" / "voices"
HOSTS = REPO_ROOT / "statecraft" / "channels"  # legacy name in API: host slugs
RECEIPT_PATH = REPO_ROOT / "runtime" / "artifacts" / "statecraft" / "codex-speakers-migration-receipt.json"

HOST_SLUGS = frozenset({"daniel-davis", "judging-freedom", "dialogue-works"})
SKIP_DIRS = frozenset({"alkhorshid"})  # compat pointer only; links target dialogue-works-channel-index
META_DIRS = frozenset({"_templates", "relations", "map"})
ROOT_FILES = (
    "authored-pressure-quartet.md",
    "core-thesis-matrix-pilot.md",
    "speaker-cluster-map.md",
    "expert-orthogonality-note.md",
)

VOICE_README_STUB = """# {title}

WORK only; not Record.

Promoted from legacy `codex/speakers/{slug}/` during statecraft voices migration.

Open [statecraft/voices/voice-index.md](../voice-index.md) for live routing.
"""


@dataclass
class MigrationEntry:
    source: str
    dest: str
    action: str  # moved | skipped_duplicate | skipped_empty | deleted_stub


def dest_root_for_slug(slug: str) -> Path:
    if slug in HOST_SLUGS:
        return HOSTS / slug
    return VOICES / slug


def rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def plan_migrations() -> list[MigrationEntry]:
    entries: list[MigrationEntry] = []
    if not CODEX_SPEAKERS.is_dir():
        return entries

    for name in ROOT_FILES:
        src = CODEX_SPEAKERS / name
        if src.is_file():
            dest = VOICES / name
            entries.append(_entry(src, dest))

    for special, dest_base in (
        ("_templates", REPO_ROOT / "statecraft" / "templates"),
        ("relations", VOICES / "relations"),
        ("map", VOICES / "map"),
    ):
        base = CODEX_SPEAKERS / special
        if base.is_dir():
            for f in sorted(base.rglob("*")):
                if f.is_file():
                    entries.append(_entry(f, dest_base / f.relative_to(base)))

    for child in sorted(CODEX_SPEAKERS.iterdir()):
        if not child.is_dir():
            continue
        slug = child.name
        if slug in SKIP_DIRS:
            for f in child.rglob("*"):
                if f.is_file():
                    entries.append(MigrationEntry(rel(f), "", "deleted_stub"))
            continue
        if slug in {"_templates", "relations", "map"}:
            continue
        dest_base = dest_root_for_slug(slug)
        for f in sorted(child.rglob("*")):
            if not f.is_file():
                continue
            if f.name == "README.md" and slug in SKIP_DIRS:
                continue
            rel_under = f.relative_to(child)
            dest = dest_base / rel_under
            entries.append(_entry(f, dest))

    return entries


def _entry(src: Path, dest: Path) -> MigrationEntry:
    if not dest.exists():
        return MigrationEntry(rel(src), rel(dest), "moved")
    try:
        if src.read_bytes() == dest.read_bytes():
            return MigrationEntry(rel(src), rel(dest), "skipped_duplicate")
    except OSError:
        pass
    # Dest exists with different body — keep statecraft SSOT; map for link rewrite only.
    return MigrationEntry(rel(src), rel(dest), "skipped_duplicate")


def ensure_voice_readme(slug: str, apply: bool) -> None:
    if slug in HOST_SLUGS or slug in SKIP_DIRS:
        return
    dest_dir = VOICES / slug
    readme = dest_dir / "README.md"
    if readme.exists():
        return
    if apply:
        dest_dir.mkdir(parents=True, exist_ok=True)
        title = slug.replace("-", " ").title()
        readme.write_text(
            VOICE_README_STUB.format(title=title, slug=slug),
            encoding="utf-8",
            newline="\n",
        )


def apply_migrations(entries: list[MigrationEntry], use_git_mv: bool) -> None:
    RECEIPT_PATH.parent.mkdir(parents=True, exist_ok=True)
    slugs_touched: set[str] = set()
    for e in entries:
        if e.action == "deleted_stub":
            src = REPO_ROOT / e.source
            if src.is_file():
                src.unlink()
            continue
        if e.action != "moved":
            continue
        src = REPO_ROOT / e.source
        dest = REPO_ROOT / e.dest
        if not src.is_file():
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        rel_parts = src.relative_to(CODEX_SPEAKERS).parts
        if len(rel_parts) >= 2:
            slug = rel_parts[0]
            if slug not in META_DIRS and slug not in SKIP_DIRS:
                slugs_touched.add(slug)
        if use_git_mv:
            subprocess.run(
                ["git", "mv", str(src), str(dest)],
                cwd=REPO_ROOT,
                check=False,
                capture_output=True,
            )
            if dest.is_file():
                continue
        shutil.move(str(src), str(dest))

    for slug in slugs_touched:
        ensure_voice_readme(slug, apply=True)


def write_receipt(entries: list[MigrationEntry]) -> None:
    RECEIPT_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_root": "codex/speakers",
        "counts": {},
        "path_map": {e.source: e.dest for e in entries if e.dest},
        "entries": [asdict(e) for e in entries],
    }
    for e in entries:
        payload["counts"][e.action] = payload["counts"].get(e.action, 0) + 1
    RECEIPT_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def rewrite_links(receipt_path: Path) -> int:
    data = json.loads(receipt_path.read_text(encoding="utf-8"))
    path_map: dict[str, str] = data.get("path_map", {})
    if not path_map:
        return 0

    # longest sources first to avoid partial replacements
    pairs = sorted(path_map.items(), key=lambda kv: len(kv[0]), reverse=True)

    def rewrite_text(text: str) -> str:
        for src, dest in pairs:
            src_norm = src.replace("\\", "/")
            dest_norm = dest.replace("\\", "/")
            # relative / posix
            text = text.replace(src_norm, dest_norm)
            text = text.replace(src_norm.replace("/", "\\"), dest_norm)
            # Windows absolute
            for root in (
                "C:/dev/strategy-codex/",
                "c:/dev/strategy-codex/",
                "/C:/dev/strategy-codex/",
            ):
                text = text.replace(root + src_norm, root + dest_norm)
            # broken mercouris shelf pattern
            broken = f"../../../../dev/strategy-codex/{src_norm}"
            text = text.replace(broken, dest_norm)
            text = text.replace(broken + ")", dest_norm + ")")
        # generic prefix fallback for anything missed
        text = re.sub(
            r"statecraft/channels/daniel-davis/",
            "statecraft/channels/daniel-davis/",
            text,
        )
        text = re.sub(
            r"statecraft/channels/judging-freedom/",
            "statecraft/channels/judging-freedom/",
            text,
        )
        text = re.sub(
            r"statecraft/channels/dialogue-works/",
            "statecraft/channels/dialogue-works/",
            text,
        )
        text = re.sub(
            r"codex/speakers/(_templates|relations|map)/",
            r"statecraft/voices/\1/",
            text,
        )
        text = re.sub(
            r"codex/speakers/([a-z0-9-]+)/",
            r"statecraft/voices/\1/",
            text,
        )
        return text

    skip_parts = {
        "runtime/artifacts/statecraft/codex-speakers-migration-receipt.json",
        "docs/archive/codex-speakers-deprecated.md",
    }
    roots = [
        REPO_ROOT / "statecraft",
        REPO_ROOT / "codex",
        REPO_ROOT / "docs",
        REPO_ROOT / "scripts",
        REPO_ROOT / "tests",
        REPO_ROOT / ".cursor",
        SKILLS_DIR,
        REPO_ROOT / "LLM-ROUTING.md",
        REPO_ROOT / "repo-map.yaml",
    ]
    changed = 0
    seen: set[Path] = set()
    for root in roots:
        files: list[Path]
        if root.is_file():
            files = [root]
        else:
            files = [
                p
                for p in root.rglob("*")
                if p.is_file()
                and p.suffix in {".md", ".mdc", ".json", ".yaml", ".yml", ".py", ".toml"}
                and "codex/speakers" not in rel(p)
            ]
        for path in files:
            if path in seen:
                continue
            seen.add(path)
            if any(part in rel(path) for part in skip_parts):
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            if "codex/speakers" not in text and "codex\\speakers" not in text:
                if "dev/strategy-codex/codex/speakers" not in text:
                    continue
            new_text = rewrite_text(text)
            if new_text != text:
                path.write_text(new_text, encoding="utf-8", newline="\n")
                changed += 1
    return changed


def remove_codex_speakers_tree() -> None:
    if not CODEX_SPEAKERS.exists():
        return
    shutil.rmtree(CODEX_SPEAKERS)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", action="store_true", help="Print summary and write receipt only.")
    parser.add_argument("--apply", action="store_true", help="Move files and write receipt.")
    parser.add_argument("--rewrite-links", action="store_true", help="Rewrite repo links from receipt.")
    parser.add_argument("--delete-tree", action="store_true", help="Remove codex/speakers after migration.")
    parser.add_argument("--git-mv", action="store_true", help="Use git mv when applying.")
    parser.add_argument("--all", action="store_true", help="apply + rewrite-links + delete-tree")
    args = parser.parse_args(argv)

    if args.all:
        args.apply = True
        args.rewrite_links = True
        args.delete_tree = True

    entries = plan_migrations()
    write_receipt(entries)
    counts = {}
    for e in entries:
        counts[e.action] = counts.get(e.action, 0) + 1
    print(json.dumps({"receipt": rel(RECEIPT_PATH), "counts": counts}, indent=2))

    if args.plan and not args.apply:
        return 0

    if args.apply:
        apply_migrations(entries, use_git_mv=args.git_mv)
        write_receipt(entries)

    if args.rewrite_links:
        n = rewrite_links(RECEIPT_PATH)
        print(f"rewrite_links: {n} files updated")

    if args.delete_tree:
        remove_codex_speakers_tree()
        print("deleted codex/speakers/")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
