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
WIN_ABS3 = re.compile(r"C:\\dev\\strategy-codex\\([^)\s]+)", re.IGNORECASE)
MAC_HOME = re.compile(r"/Users/[^)\s]+/([^)\s]*strategy-codex[^)\s]*)", re.IGNORECASE)

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
    "self-library.md": "archive/grace-mar-instance/self-library.md",
    "SELF-LIBRARY.md": "archive/grace-mar-instance/self-library.md",
    "self.md": "archive/grace-mar-instance/self.md",
    "strategy-codex-template-page.md": "codex/strategy-codex-template-page.md",
    "work-cici-history.md": "singularity/work-cici/README.md",
    "STRATEGY-NOTEBOOK-ARCHITECTURE.md": "codex/STRATEGY-NOTEBOOK-ARCHITECTURE.md",
    "strategy-commentator-threads.md": "codex/strategy-commentator-threads.md",
    "arc-mercouris-continuity-threads.md": (
        "statecraft/voices/mercouris/mercouris-arc-threads.md"
    ),
    "arc-johnson-continuity.md": "statecraft/voices/johnson/johnson-arc.md",
    "statecraft.md": "statecraft/README.md",
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
WORK_CICI_BASENAME_INDEX: dict[str, Path] | None = None
SCAFFOLD_BASENAME_INDEX: dict[str, Path] | None = None
SCRIPTS_BASENAME_INDEX: dict[str, Path] | None = None


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


def _build_flat_index(root: Path, pattern: str = "*.md") -> dict[str, Path]:
    index: dict[str, Path] = {}
    if not root.is_dir():
        return index
    for path in root.rglob(pattern):
        if path.is_file():
            index.setdefault(path.name, path)
    return index


def get_work_cici_basename_index() -> dict[str, Path]:
    global WORK_CICI_BASENAME_INDEX
    if WORK_CICI_BASENAME_INDEX is None:
        WORK_CICI_BASENAME_INDEX = _build_flat_index(REPO_ROOT / "singularity" / "work-cici")
    return WORK_CICI_BASENAME_INDEX


def get_scaffold_basename_index() -> dict[str, Path]:
    global SCAFFOLD_BASENAME_INDEX
    if SCAFFOLD_BASENAME_INDEX is None:
        sheets = REPO_ROOT / "statecraft" / "sheets"
        SCAFFOLD_BASENAME_INDEX = _build_flat_index(sheets)
    return SCAFFOLD_BASENAME_INDEX


def get_scripts_basename_index() -> dict[str, Path]:
    global SCRIPTS_BASENAME_INDEX
    if SCRIPTS_BASENAME_INDEX is None:
        SCRIPTS_BASENAME_INDEX = _build_flat_index(REPO_ROOT / "scripts", "*.py")
    return SCRIPTS_BASENAME_INDEX


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

    if norm.startswith("statecraft/research/bridges/"):
        candidate = REPO_ROOT / norm.replace(
            "statecraft/research/bridges/",
            "statecraft/bridges/",
            1,
        )
        if candidate.is_file():
            return candidate

    if re.match(r"2026-\d{2}-\d{2}-.+\.md$", norm):
        notes_candidate = REPO_ROOT / "statecraft" / "notes" / norm
        if notes_candidate.is_file():
            return notes_candidate

    if norm.startswith("ph-civ/"):
        rewritten = norm.replace("ph-civ/", "public/predictive-history/", 1)
        candidate = REPO_ROOT / rewritten
        if candidate.is_file():
            return candidate

    if "/iran/" in norm or norm.startswith("iran/"):
        persia_norm = norm.replace("/iran/", "/persia/").replace("iran/", "persia/", 1)
        candidate = REPO_ROOT / persia_norm
        if candidate.is_file():
            return candidate

    if norm.startswith("docs/skill-work/work-cici/"):
        tail = norm.removeprefix("docs/skill-work/work-cici/")
        candidate = REPO_ROOT / "singularity" / "work-cici" / tail
        if candidate.is_file():
            return candidate

    if "skill-strategy/SKILL.md" in norm.replace("\\", "/"):
        candidate = REPO_ROOT / "docs/skill-work/work-strategy/SKILL-STRATEGY-DEPRECATED.md"
        if candidate.is_file():
            return candidate

    if norm.endswith("experts/marandi/thread.md") or norm.endswith("marandi/thread.md"):
        candidate = REPO_ROOT / "statecraft/voices/marandi/marandi-thread.md"
        if candidate.is_file():
            return candidate

    if "strategy-notebook/" in norm:
        rewritten = norm.replace(
            "docs/skill-work/work-strategy/strategy-notebook/",
            "codex/",
        ).replace("strategy-notebook/", "codex/")
        candidate = REPO_ROOT / rewritten
        if candidate.is_file():
            return candidate
        dep = REPO_ROOT / "docs/skill-work/work-strategy/STRATEGY-NOTEBOOK-DEPRECATED.md"
        if dep.is_file() and "raw-input" in norm:
            return dep

    if norm.startswith("provenance/_aired-pending/"):
        candidate = REPO_ROOT / "source-archive" / "statecraft" / "_aired-pending" / Path(norm).name
        if candidate.is_file():
            return candidate

    if "synthesis/persia/transactions/" in norm:
        rewritten = norm.replace("synthesis/persia/transactions/", "persia/transactions/")
        candidate = REPO_ROOT / rewritten
        if candidate.is_file():
            return candidate

    if "years/2026/provenance/" in norm or norm.startswith("provenance/"):
        basename = Path(norm).name
        indexed = get_scaffold_basename_index().get(basename)
        if indexed is not None:
            return indexed

    if norm.startswith("public/predictive-history/"):
        candidate = REPO_ROOT / norm
        if candidate.is_file():
            return candidate

    resolved = resolve_by_tail_walk(norm)
    if resolved is not None:
        return resolved

    return None


def resolve_by_tail_walk(norm: str) -> Path | None:
    tail = norm.replace("\\", "/").lstrip("./")
    parts = tail.split("/")
    for start in range(len(parts)):
        sub = "/".join(parts[start:])
        if not sub:
            continue
        candidate = REPO_ROOT / sub
        if candidate.is_file():
            return candidate
        basename = Path(sub).name
        if basename.endswith(".md"):
            indexed = get_work_cici_basename_index().get(basename)
            if indexed is not None:
                return indexed
            indexed = get_scaffold_basename_index().get(basename)
            if indexed is not None:
                return indexed
        if basename.endswith(".py"):
            indexed = get_scripts_basename_index().get(basename)
            if indexed is not None:
                return indexed
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

    if rel.startswith("statecraft/notes/") and "/reentry/" not in rel:
        replacements.append(("../../america/transactions/", "../america/transactions/"))
        replacements.append(("../../america/", "../america/"))

    if rel.startswith("statecraft/compact/"):
        replacements.append(("../../america/transactions/", "../america/transactions/"))
        replacements.append(("../../america/", "../america/"))

    if rel.startswith("statecraft/states/migration/") or rel.startswith("statecraft/states/"):
        replacements.append(("../../iran/", "../../persia/"))
        replacements.append(("../iran/", "../persia/"))

    if rel.startswith("statecraft/"):
        replacements.append(("notes/notes/", "notes/"))
        replacements.append(("statecraft/iran/", "statecraft/persia/"))
        replacements.append(
            (
                "synthesis/persia/transactions/",
                "persia/transactions/",
            )
        )

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
                (
                    "../../.cursor/skills/skill-strategy/SKILL.md",
                    "../../../docs/skill-work/work-strategy/SKILL-STRATEGY-DEPRECATED.md",
                ),
                (
                    "../../../.cursor/skills/skill-strategy/SKILL.md",
                    "../../SKILL-STRATEGY-DEPRECATED.md",
                ),
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

    if rel.startswith("statecraft/notes/reentry/"):
        replacements.append(("../../../america/", "../../america/"))

    if rel.startswith("statecraft/notes/") and "/reentry/" not in rel:
        replacements.append(("../../notes/", ""))
        replacements.append(("../../arc-mercouris-continuity.md", "arc-mercouris-continuity.md"))
        replacements.append(("](../../notes/)", "](../notes/)"))
        replacements.append(("](crooke-helix.md)", "](../voices/crooke/crooke-helix.md)"))
        replacements.append(("](macgregor-helix.md)", "](../voices/macgregor/macgregor-helix.md)"))
        replacements.append(("](mercouris-helix.md)", "](../voices/mercouris/mercouris-helix.md)"))

    if rel.startswith("statecraft/notes/watch/"):
        replacements.append(("../compact/", "../../compact/"))

    if rel.startswith("statecraft/voices/johnson/"):
        replacements.append(("arc-johnson-continuity.md", "johnson-arc.md"))

    if rel.startswith("statecraft/voices/ritter/"):
        replacements.extend(
            [
                ("](transcript.md)", "](ritter-transcript.md)"),
                (
                    "../../../../../../../../../../../../codex/2026/ritter/ritter-thread.md",
                    "../../ritter-thread.md",
                ),
                (
                    "../../../../../../../../../../../../codex/2026/ritter/ritter-transcript.md",
                    "../../ritter-transcript.md",
                ),
                (
                    "../../../../../../../../../../../../codex/experts/ritter/thread.md",
                    "../../ritter-thread.md",
                ),
            ]
        )

    if rel.startswith("statecraft/voices/jiang/"):
        replacements.append(("ph-civ/", "../../../public/predictive-history/"))

    if rel.startswith("docs/skill-work/work-business/"):
        replacements.append(("../work-cici/", "../../singularity/work-cici/"))
        replacements.append(("../../work-cici/", "../../../singularity/work-cici/"))

    if rel.startswith("docs/skill-work/"):
        replacements.append(
            (
                "../../.cursor/skills/tri-mind/SKILL.md",
                "../../../docs/skill-work/work-strategy/TRI-MIND-DEPRECATED.md",
            )
        )
        replacements.append(
            (
                "../../../.cursor/skills/tri-mind/SKILL.md",
                "../../TRI-MIND-DEPRECATED.md",
            )
        )

    if rel.startswith(".cursor/skills/") or rel.startswith("skills/"):
        replacements.extend(
            [
                ("../runbooks/", "../../skills/runbooks/"),
                (
                    "../../../docs/skill-work/work-strategy/strategy-notebook/raw-input/",
                    "../../../../docs/skill-work/work-strategy/STRATEGY-NOTEBOOK-DEPRECATED.md",
                ),
                (
                    "../../../docs/skill-work/work-strategy/strategy-notebook/",
                    "../../../../codex/",
                ),
                (
                    "../../../docs/skill-work/work-cici/archive/",
                    "../../../../singularity/work-cici/",
                ),
                (
                    "../../../docs/skill-work/work-cici/",
                    "../../../../singularity/work-cici/",
                ),
                (
                    "../../.cursor/skills/skill-strategy/SKILL.md",
                    "../../../docs/skill-work/work-strategy/SKILL-STRATEGY-DEPRECATED.md",
                ),
                (
                    "../../../.cursor/skills/skill-strategy/SKILL.md",
                    "../../../../docs/skill-work/work-strategy/SKILL-STRATEGY-DEPRECATED.md",
                ),
            ]
        )

    if rel.startswith("docs/skill-work/work-dev/dev-notebook/work-cici/"):
        replacements.extend(
            [
                ("../../../work-cici/", "../../../../../singularity/work-cici/"),
                ("../../../singularity/work-cici/", "../../../../../singularity/work-cici/"),
                (
                    "../../../work-cici/work-cici-history.md",
                    "../../../../../singularity/work-cici/README.md",
                ),
                (
                    "../../../../../archive/placeholders/evidence",
                    "../../../../../../singularity/work-cici/archive/placeholders/evidence",
                ),
            ]
        )

    if rel.startswith("docs/skill-work/work-cici/"):
        replacements.append(
            (
                "../../../singularity/work-cici/",
                "../../../../singularity/work-cici/",
            )
        )

    for old, new in replacements:
        if old in text:
            n = text.count(old)
            text = text.replace(old, new)
            count += n
    return text, count


def fix_regex_patterns(text: str, file_path: Path) -> tuple[str, int]:
    rel = file_path.relative_to(REPO_ROOT).as_posix()
    count = 0
    patterns: list[tuple[str, str]] = [
        (r"statecraft/research/bridges/", "statecraft/bridges/"),
        (r"ph-civ/book/", "public/predictive-history/book/"),
    ]
    if rel.startswith("statecraft/synthesis/day/") or rel.startswith("statecraft/synthesis/month/"):
        patterns.append((r"\.\./america/transactions/", "../../america/transactions/"))
    if "dev-notebook/work-cici" in rel:
        patterns.extend(
            [
                (
                    r"(?:\.\./)+singularity/work-cici/",
                    "../../../../../singularity/work-cici/",
                ),
                (
                    r"(?:\.\./)+README\.md",
                    "../../../../../singularity/work-cici/README.md",
                ),
            ]
        )
    if rel.startswith("statecraft/states/"):
        patterns.append((r"\.\./\.\./iran/", "../../persia/"))
    if rel.startswith("statecraft/notes/reentry/"):
        patterns.append(
            (r"(?:\.\./)+notes/wire/", "../../notes/wire/"),
        )
        patterns.append((r"\.\./\.\./\.\./america/", "../../america/"))
    if rel.startswith("statecraft/"):
        patterns.append(
            (r"(?:\.\./)+years/2026/provenance/", "../../sheets/source-archive-control/"),
        )
        patterns.append((r"provenance/_aired-pending/", "../../../source-archive/statecraft/_aired-pending/"))
    if rel.startswith("statecraft/voices/jiang/"):
        patterns.append(
            (r"\]\(public/predictive-history/([^)#]+)\)", r"](../../../public/predictive-history/\1)"),
        )
    for pattern, repl in patterns:
        new_text, n = re.subn(pattern, repl, text)
        if n:
            text = new_text
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
        elif stem.replace("-verbatim", "") in name or stem.replace("-mercouris", "") in name:
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
    text = WIN_ABS3.sub(repl, text)

    def mac_repl(match: re.Match[str]) -> str:
        nonlocal count
        rest = match.group(1)
        if rest.startswith("/"):
            rest = rest.lstrip("/")
        rel = relative_repo_path(file_path, rest)
        count += 1
        return rel

    text = MAC_HOME.sub(mac_repl, text)
    return text, count


def fix_cursor_skills_depth(text: str, file_path: Path) -> tuple[str, int]:
    """Fix wrong-depth .cursor/skills links under docs/ and skills/."""
    rel = file_path.relative_to(REPO_ROOT).as_posix()
    if not (rel.startswith("docs/") or rel.startswith("skills/") or rel.startswith(".cursor/skills/")):
        return text, 0
    skills_root = REPO_ROOT / ".cursor" / "skills"
    if not skills_root.is_dir():
        return text, 0
    count = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal count
        tail = match.group(1)
        target = skills_root / tail
        if not target.is_file():
            return match.group(0)
        correct = os.path.relpath(target, file_path.parent.resolve()).replace("\\", "/")
        if correct == match.group(0)[2:-1]:  # strip ]( and )
            return match.group(0)
        count += 1
        return f"]({correct})"

    text = re.sub(
        r"\]\((?:\.\./)+\.cursor/skills/([^)]+)\)",
        repl,
        text,
    )
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

    text, n = fix_cursor_skills_depth(text, path)
    total += n

    text, n = fix_template_routing_prose(text, path)
    total += n

    text, n = fix_bulk_text_patterns(text, path)
    total += n

    text, n = fix_regex_patterns(text, path)
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
