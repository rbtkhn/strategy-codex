#!/usr/bin/env python3
"""Batch-fix common Repo Surgeon link patterns (repo-root paths, Windows abs, depth)."""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from repo_io import SKILLS_DIR

from validate_structured_files import iter_markdown_links  # noqa: E402

INLINE_LINK_RE = re.compile(r"(\[[^\]]*\]\()([^)]+)(\))")
WIN_ABS = re.compile(r"/C:/dev/strategy-codex/([^)\s]+)", re.IGNORECASE)
WIN_ABS2 = re.compile(r"C:\\\\dev\\\\strategy-codex\\\\([^)\s]+)", re.IGNORECASE)

REPO_ROOT_TARGETS = (
    "statecraft/",
    "source-archive/",
    "docs/",
    "codex/",
    "archive/",
    "skills/",
    "singularity/",
    "essays/",
    "runtime/",
    "research/",
    "public/",
)

ROOT_FILES = frozenset(
    {
        "AGENTS.md",
        "LLM-ROUTING.md",
        "instance-doctrine.md",
        "contributing.md",
        "README.md",
        "repo-map.yaml",
    }
)

TARGET_REWRITES: dict[str, str] = {
    "daily-strategy-inbox.md": "codex/daily-strategy-inbox.md",
    "strategy-expert-freeman-thread.md": "freeman-thread.md",
    "strategy-expert-mearsheimer-thread.md": "mearsheimer-thread.md",
    "ph-civ/docs/source-video-index.md": (
        "public/predictive-history/docs/predictive-history-index.md"
    ),
    "recursion-gate.md": "archive/grace-mar-instance/recursion-gate.md",
    "strategy-notebook/experts/pape/transcript.md": (
        "statecraft/voices/pape/pape-transcript.md"
    ),
    "strategy-notebook/experts/mercouris/transcript.md": (
        "statecraft/voices/mercouris/mercouris-transcript.md"
    ),
    "strategy-notebook/experts/mearsheimer/transcript.md": (
        "statecraft/voices/mearsheimer/mearsheimer-transcript.md"
    ),
    "strategy-notebook/experts/crooke/transcript.md": (
        "statecraft/voices/crooke/crooke-transcript.md"
    ),
    "crooke-forecast-ledger-2026.md": (
        "statecraft/voices/crooke/crooke-forecast-ledger-2026.md"
    ),
}

PROVENANCE_LINK_RE = re.compile(
    r"(?:(?:\.\./)+(?:codex/)?years/2026/provenance/|provenance/)"
    r"(\d{4}-\d{2}-\d{2})/([^)\s#]+)"
)
SCAFFOLD_DATE_RE = re.compile(r"^\./(\d{4}-\d{2}-\d{2})/(.+)$")
LEGACY_EXPERTS_RE = re.compile(r"^experts/([a-z0-9-]+)/(.+)$")
STRATEGY_EXPERT_THREAD_RE = re.compile(r"^strategy-expert-([a-z0-9-]+)-thread\.md$")
STRATEGY_EXPERT_PROFILE_RE = re.compile(r"^strategy-expert-([a-z0-9-]+)\.md$")
STRATEGY_EXPERT_TRANSCRIPT_RE = re.compile(
    r"^strategy-expert-([a-z0-9-]+)-transcript\.md$"
)
SOURCE_BASENAME_INDEX: dict[str, Path] | None = None


def build_source_basename_index() -> dict[str, Path]:
    index: dict[str, Path] = {}
    root = REPO_ROOT / "source-archive" / "statecraft"
    if not root.is_dir():
        return index
    for path in root.rglob("source-*.md"):
        if path.is_file():
            index.setdefault(path.name, path)
    return index


def get_source_basename_index() -> dict[str, Path]:
    global SOURCE_BASENAME_INDEX
    if SOURCE_BASENAME_INDEX is None:
        SOURCE_BASENAME_INDEX = build_source_basename_index()
    return SOURCE_BASENAME_INDEX


def resolve_legacy_path(path_part: str) -> Path | None:
    norm = path_part.replace("\\", "/").lstrip("./")
    basename = Path(norm).name

    if basename in TARGET_REWRITES:
        candidate = REPO_ROOT / TARGET_REWRITES[basename]
        if candidate.is_file():
            return candidate

    scaffold = SCAFFOLD_DATE_RE.match(norm)
    if scaffold:
        candidate = archive_target_for_provenance(scaffold.group(1), scaffold.group(2))
        if candidate is not None:
            return candidate

    experts = LEGACY_EXPERTS_RE.match(norm)
    if experts:
        speaker, rest = experts.group(1), experts.group(2)
        candidate = REPO_ROOT / "statecraft" / "voices" / speaker / rest
        if candidate.is_file():
            return candidate

    for pattern, builder in (
        (STRATEGY_EXPERT_THREAD_RE, lambda s: f"{s}-thread.md"),
        (STRATEGY_EXPERT_TRANSCRIPT_RE, lambda s: f"{s}-transcript.md"),
        (STRATEGY_EXPERT_PROFILE_RE, lambda s: f"{s}-profile.md"),
    ):
        match = pattern.match(norm)
        if match:
            speaker = match.group(1)
            candidate = REPO_ROOT / "statecraft" / "voices" / speaker / builder(speaker)
            if candidate.is_file():
                return candidate

    if norm.startswith("speakers/"):
        tail = norm.removeprefix("speakers/")
        candidate = REPO_ROOT / "statecraft" / "voices" / tail
        if candidate.exists():
            return candidate

    if basename.startswith("source-") and basename.endswith(".md"):
        indexed = get_source_basename_index().get(basename)
        if indexed is not None:
            return indexed

    if basename == "rome-persia-legitimacy-signal-check.md":
        candidate = REPO_ROOT / "codex" / basename
        if candidate.is_file():
            return candidate

    if basename == "transcript-analysis-haiphong-ritter-johnson-iran-2026-04.md":
        candidate = (
            REPO_ROOT
            / "docs"
            / "skill-work"
            / "work-strategy"
            / basename
        )
        if candidate.is_file():
            return candidate

    if "legacy page index" in norm:
        candidate = REPO_ROOT / "codex" / "watches" / "README.md"
        if candidate.is_file():
            return candidate

    return None


def fix_days_md(from_file: Path, path_part: str, frag: str) -> str | None:
    norm = path_part.replace("\\", "/")
    if not norm.endswith("days.md"):
        return None
    month = "04"
    if frag:
        month_match = re.search(r"2026-(\d{2})-\d{2}", frag)
        if month_match:
            month = month_match.group(1)
    candidate = REPO_ROOT / "codex" / "chapters" / "2026" / f"2026-{month}" / "days.md"
    if not candidate.is_file():
        return None
    new_path = os.path.relpath(candidate, from_file.parent.resolve()).replace("\\", "/") + frag
    return new_path


def fix_bulk_text_patterns(text: str, file_path: Path) -> tuple[str, int]:
    rel = file_path.relative_to(REPO_ROOT).as_posix()
    count = 0
    replacements: list[tuple[str, str]] = []

    if "/synthesis/day/" in rel or "/synthesis/month/" in rel:
        replacements.append(("../notes/", "../../notes/"))

    if rel.startswith("statecraft/transactions/"):
        replacements.append(("../../../../speakers/", "../../voices/"))
        replacements.append(("../../../speakers/", "../../voices/"))

    if "/synthesis/day/" in rel or "/synthesis/month/" in rel:
        replacements.append(("../../../notes/", "../../notes/"))

    if rel.startswith("statecraft/notes/reentry/"):
        replacements.append(("../america/transactions/", "../../america/transactions/"))
        replacements.append(("../wire/", "../../notes/wire/"))

    if rel.startswith("statecraft/sheets/source-archive-control/"):
        replacements.append(
            ("../refined-page-template.md", "../../../codex/refined-page-template.md")
        )

    if rel.startswith("docs/skill-work/work-strategy/"):
        replacements.extend(
            [
                ("strategy-notebook/NOTEBOOK-PREFERENCES.md", "../../codex/NOTEBOOK-PREFERENCES.md"),
                ("strategy-notebook/chapters/", "../../codex/chapters/"),
                ("strategy-notebook/", "../../codex/"),
                ("../../codex/chapters/2026-04/", "../../../codex/chapters/2026/2026-04/"),
            ]
        )

    if "history-notebook/research/BOOKSHELF.md" == rel:
        replacements.append(
            (
                "../../../../self-library.",
                "../../../history-notebook/research/BOOKSHELF.md#",
            )
        )

    if "history-notebook/research/" in rel:
        replacements.extend(
            [
                ("../../STYLE-GUIDE.md", "../STYLE-GUIDE.md"),
                (
                    "../../research/VOL-I-PROBLEM-CHAPTERS.md",
                    "./VOL-I-PROBLEM-CHAPTERS.md",
                ),
            ]
        )

    if rel.startswith("docs/skill-work/work-strategy/minds/"):
        replacements.append(
            (
                "../strategy-notebook/",
                "../../../codex/",
            )
        )

    if rel.startswith("statecraft/voices/"):
        replacements.append(("../../codex/", "../../../codex/"))

    if rel.startswith(".cursor/skills/") or rel.startswith("skills/"):
        replacements.extend(
            [
                ("../runbooks/", "../../skills/runbooks/"),
                (
                    "../../../docs/skill-work/work-strategy/strategy-notebook/raw-input/",
                    "../../../../docs/skill-work/work-strategy/STRATEGY-NOTEBOOK-DEPRECATED.md",
                ),
                (
                    "../../../docs/skill-work/work-cici/archive/",
                    "../../../docs/skill-work/work-cici/",
                ),
            ]
        )

    if rel.startswith("docs/skill-work/work-dev/dev-notebook/work-cici/"):
        replacements.extend(
            [
                ("../../work-cici/", "../../../work-cici/"),
                ("../../../work-cici/work-cici-history.md", "../../work-cici/README.md"),
                ("../../../work-cici/archive/", "../../../work-cici/"),
            ]
        )

    for old, new in replacements:
        if old in text:
            n = text.count(old)
            text = text.replace(old, new)
            count += n
    return text, count


def relative_repo_path(from_file: Path, target_under_root: str) -> str:
    from_dir = from_file.parent.resolve()
    target = (REPO_ROOT / target_under_root.replace("\\", "/")).resolve()
    return os.path.relpath(target, from_dir).replace("\\", "/")


def normalize_target(raw: str) -> tuple[str, str]:
    target = raw.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1].strip()
    path_part, sep, frag = target.partition("#")
    return path_part.strip(), (sep + frag if sep else "")


def looks_repo_root_absolute(path_part: str) -> bool:
    if path_part in ROOT_FILES:
        return True
    return any(path_part.startswith(prefix) for prefix in REPO_ROOT_TARGETS)


def repo_target_path(path_part: str) -> Path | None:
    norm = path_part.replace("\\", "/")
    if norm in ROOT_FILES:
        candidate = REPO_ROOT / norm
        return candidate if candidate.exists() else None
    for marker in (*REPO_ROOT_TARGETS, *ROOT_FILES):
        if marker.endswith("/"):
            idx = norm.find(marker)
            if idx >= 0:
                sub = norm[idx:]
                candidate = REPO_ROOT / sub
                if candidate.exists():
                    return candidate
        elif norm == marker or norm.endswith("/" + marker):
            candidate = REPO_ROOT / norm
            if candidate.exists():
                return candidate
    rewritten = TARGET_REWRITES.get(norm)
    if rewritten:
        candidate = REPO_ROOT / rewritten
        return candidate if candidate.exists() else None
    basename = Path(norm).name
    rewritten = TARGET_REWRITES.get(basename)
    if rewritten:
        candidate = REPO_ROOT / rewritten
        return candidate if candidate.exists() else None
    return None


def archive_target_for_provenance(date: str, filename: str) -> Path | None:
    norm = filename.replace("\\", "/").lstrip("./")
    day_dir = REPO_ROOT / "source-archive" / "statecraft" / date
    candidate = day_dir / norm
    if candidate.is_file():
        return candidate
    if not day_dir.is_dir():
        return None
    stem = Path(norm).stem.lower()
    partial: list[Path] = []
    for path in day_dir.glob("*.md"):
        name = path.name.lower()
        if stem and (stem in name or name in stem):
            partial.append(path)
    if len(partial) == 1:
        return partial[0]
    day_index = day_dir / "day-index.md"
    if day_index.is_file():
        return day_index
    return None


def fix_provenance_in_target(from_file: Path, path_part: str, frag: str) -> str | None:
    match = PROVENANCE_LINK_RE.search(path_part.replace("\\", "/"))
    if not match:
        return None
    date, filename = match.group(1), match.group(2)
    candidate = archive_target_for_provenance(date, filename)
    if candidate is None:
        return None
    new_path = os.path.relpath(candidate, from_file.parent.resolve()).replace("\\", "/") + frag
    return new_path


def fix_target(from_file: Path, raw: str) -> str | None:
    path_part, frag = normalize_target(raw)
    if not path_part or "://" in path_part:
        return None

    base = from_file.parent
    direct = (base / path_part).resolve()
    if direct.exists():
        return None

    provenance_fixed = fix_provenance_in_target(from_file, path_part, frag)
    if provenance_fixed is not None:
        normalized_raw = raw.strip().lstrip("<").rstrip(">")
        if provenance_fixed != normalized_raw:
            return provenance_fixed

    days_fixed = fix_days_md(from_file, path_part, frag)
    if days_fixed is not None:
        normalized_raw = raw.strip().lstrip("<").rstrip(">")
        if days_fixed != normalized_raw:
            return days_fixed

    legacy = resolve_legacy_path(path_part)
    if legacy is not None:
        new_path = os.path.relpath(legacy, base.resolve()).replace("\\", "/") + frag
        normalized_raw = raw.strip().lstrip("<").rstrip(">")
        if new_path != normalized_raw:
            return new_path

    basename = Path(path_part.replace("\\", "/")).name
    if basename in ROOT_FILES:
        root_candidate = REPO_ROOT / basename
        if root_candidate.is_file():
            new_path = os.path.relpath(root_candidate, base.resolve()).replace("\\", "/") + frag
            normalized_raw = raw.strip().lstrip("<").rstrip(">")
            if new_path != normalized_raw:
                return new_path

    candidate = repo_target_path(path_part)
    if candidate is None and path_part in TARGET_REWRITES:
        candidate = repo_target_path(TARGET_REWRITES[path_part])

    if candidate is None:
        return None

    new_path = os.path.relpath(candidate, base.resolve()).replace("\\", "/") + frag
    normalized_raw = raw.strip().lstrip("<").rstrip(">")
    if new_path == normalized_raw:
        return None
    return new_path


def fix_windows_absolute(text: str, file_path: Path) -> tuple[str, int]:
    count = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal count
        rest = match.group(1)
        trailing = ""
        while rest and rest[-1] in ".,;":
            trailing = rest[-1] + trailing
            rest = rest[:-1]
        rel = relative_repo_path(file_path, rest)
        count += 1
        return rel + trailing

    text = WIN_ABS.sub(repl, text)
    text = WIN_ABS2.sub(repl, text)
    return text, count


def fix_agents_depth(text: str, file_path: Path) -> tuple[str, int]:
    """Fix common wrong-depth AGENTS.md links under docs/skill-work/."""
    rel = file_path.relative_to(REPO_ROOT).as_posix()
    if not rel.startswith("docs/skill-work/"):
        return text, 0
    agents = REPO_ROOT / "AGENTS.md"
    if not agents.is_file():
        return text, 0
    correct = os.path.relpath(agents, file_path.parent).replace("\\", "/")
    replacements = {
        "../../AGENTS.md": correct,
        "../../../AGENTS.md": correct,
        "../../../../AGENTS.md": correct,
    }
    count = 0
    for wrong, right in replacements.items():
        if wrong in text and wrong != right:
            n = text.count(wrong)
            text = text.replace(wrong, right)
            count += n
    return text, count


def fix_template_routing_prose(text: str, file_path: Path) -> tuple[str, int]:
    rel = file_path.relative_to(REPO_ROOT).as_posix()
    if rel != "docs/templates/llm-routing-prose.md":
        return text, 0
    replacements = {
        "](AGENTS.md)": "](../../AGENTS.md)",
        "](docs/harness-architecture-map.md)": "](../../docs/harness-architecture-map.md)",
        "](docs/root-directory-map.md)": "](../../docs/root-directory-map.md)",
        "](docs/archive/grace-mar.md)": "](../../docs/archive/grace-mar.md)",
    }
    count = 0
    for old, new in replacements.items():
        if old in text:
            c = text.count(old)
            text = text.replace(old, new)
            count += c
    return text, count


def fix_file(path: Path) -> int:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return 0

    original = text
    total = 0

    text, n = fix_windows_absolute(text, path)
    total += n

    text, n = fix_agents_depth(text, path)
    total += n

    text, n = fix_template_routing_prose(text, path)
    total += n

    text, n = fix_bulk_text_patterns(text, path)
    total += n

    # Fix inline markdown links
    def link_repl(match: re.Match[str]) -> str:
        nonlocal total
        prefix, target, suffix = match.group(1), match.group(2), match.group(3)
        fixed = fix_target(path, target)
        if fixed is None:
            return match.group(0)
        total += 1
        return f"{prefix}{fixed}{suffix}"

    text = INLINE_LINK_RE.sub(link_repl, text)

    if text != original:
        path.write_text(text, encoding="utf-8", newline="\n")
    return total


def iter_scope_roots(scope: str) -> list[Path]:
    scope = scope.strip().lower()
    roots: list[Path] = []
    if scope in {"docs", "all"}:
        roots.append(REPO_ROOT / "docs")
        roots.append(REPO_ROOT / "codex")
    if scope in {"statecraft", "all"}:
        roots.append(REPO_ROOT / "statecraft")
    if scope in {"skills", "all"}:
        roots.extend([SKILLS_DIR, REPO_ROOT / ".cursor" / "skills"])
    return roots


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--scope",
        default="all",
        choices=("docs", "statecraft", "skills", "all"),
    )
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    files: list[Path] = []
    for root in iter_scope_roots(args.scope):
        if root.is_dir():
            files.extend(sorted(root.rglob("*.md")))

    changed = 0
    links = 0
    for fp in files:
        if not args.apply:
            # dry-run: count would-be fixes without write
            try:
                text = fp.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            orig = text
            n = 0
            text, c = fix_windows_absolute(text, fp)
            n += c
            text, c = fix_agents_depth(text, fp)
            n += c
            text, c = fix_template_routing_prose(text, fp)
            n += c

            def link_repl(match: re.Match[str]) -> str:
                nonlocal n
                fixed = fix_target(fp, match.group(2))
                if fixed is None:
                    return match.group(0)
                n += 1
                return f"{match.group(1)}{fixed}{match.group(3)}"

            INLINE_LINK_RE.sub(link_repl, text)
            if n:
                print(f"dry-run: {fp.relative_to(REPO_ROOT)} ({n})")
                links += n
                changed += 1
        else:
            n = fix_file(fp)
            if n:
                print(f"fixed: {fp.relative_to(REPO_ROOT)} ({n})")
                links += n
                changed += 1

    print(f"done: {links} link(s) in {changed} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
