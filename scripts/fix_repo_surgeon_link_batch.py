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
    "museum-knowledge.md": "archive/grace-mar-instance/self-knowledge.md",
    "statecraft-opener-pack.md": "docs/skills/statecraft-opener-pack.md",
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
    "approval-workflow.md": "docs/externals/massie/smm-training/approval-workflow.md",
    "templates.md": "docs/externals/massie/smm-training/templates.md",
    "massie-ky4.md": "docs/skill-work/work-politics/clients/massie-ky4.md",
    "wap-candidate-template.md": "docs/skill-work/work-politics/pol-candidate-template.md",
    "self-moonshots.md": "archive/grace-mar-instance/self-moonshots.md",
    "runtime-worker.md": "docs/runtime-worker.md",
    "recursive-self-learning-objectives.md": (
        "docs/skill-work/skill-work-human-teacher/README.md"
    ),
    "jiang-predictive-history-index.md": (
        "source-archive/statecraft/jiang-predictive-history-index.md"
    ),
    "self-llm.txt": "archive/grace-mar-instance/self-llm.txt",
    "arc-pape-continuity.md": "statecraft/notes/arc-pape-continuity.md",
    "arc-mearsheimer-continuity.md": "statecraft/voices/mearsheimer/mearsheimer-arc.md",
    "arc-mercouris-continuity.md": "statecraft/voices/mercouris/mercouris-arc.md",
    "arc-ritter-continuity.md": "statecraft/voices/ritter/ritter-arc.md",
    "openclaw-integration.md": "docs/openclaw-integration.md",
    "polyphonic-cognition-protocol-skill.md": (
        "docs/skill-work/work-politics/polyphonic-cognition-protocol-skill.md"
    ),
    "self-archive.md": "archive/grace-mar-instance/self-archive.md",
    "self-evidence.md": "archive/grace-mar-instance/self-evidence.md",
    "CIV-MIND-BARNES.md": "codex/minds/CIV-MIND-BARNES.md",
    "CIV-MIND-MERCOURIS.md": "codex/minds/CIV-MIND-MERCOURIS.md",
    "strategy-expert-mearsheimer-thread.md": "statecraft/voices/mearsheimer/mearsheimer-thread.md",
    "strategy-expert-davis-thread.md": "statecraft/voices/davis/davis-thread.md",
    "strategy-expert-diesen-transcript.md": "statecraft/voices/diesen/diesen-transcript.md",
    "arc-march-2026-interview-cross-host-crooke-host.md": (
        "statecraft/voices/crooke/crooke-march-2026-interview-cross-host-arc.md"
    ),
    "arc-april-2026-interview-cross-host-crooke-host.md": (
        "statecraft/voices/crooke/crooke-april-2026-interview-cross-host-arc.md"
    ),
    "arc-may-2026-interview-cross-host-crooke-host.md": (
        "statecraft/voices/crooke/crooke-may-2026-interview-cross-host-arc.md"
    ),
    "mearsheimer-mind.md": "statecraft/voices/mearsheimer/mearsheimer-mind.md",
    "CIV-MIND-MEARSHEIMER.md": "codex/minds/CIV-MIND-MEARSHEIMER.md",
    "china-volume-seeds.md": "codex/academy/statecraft/china/chapter-seeds.md",
    "locals-arc-barnes-continuity-worked-example.md": (
        "docs/skill-write/locals-barnes-arc-worked-example.md"
    ),
    "codex/experts/barnes/mind.md": "statecraft/voices/barnes/barnes-mind.md",
    "mtp-coffee-dream.md": "skills/runbooks/mtp-coffee-dream.runbook.md",
    "alkorshid-book-2026-04.md": "statecraft/voices/alkhorshid/alkhorshid-profile.md",
    "diesen-book-2026-04.md": "statecraft/voices/diesen/diesen-profile.md",
    "mercouris-book-2026-04.md": "statecraft/voices/mercouris/mercouris-profile.md",
    "davis-book-2026-04.md": "statecraft/voices/davis/davis-profile.md",
    "interviews-14-diesen-iran-war-petrodollar.md": (
        "codex/predictive-history/lectures/interviews-14-glenn-diesen-iran-war-petrodollar.md"
    ),
    "statecraft/states/theory/form.md": "public/civ-state/theory/memory.md",
    "integration-apis.md": "docs/architecture.md",
    "skill-work.md": "docs/skill-work/README.md",
    "conceptual-frameoork.md": "docs/conceptual-framework.md",
    "boundary-self-knooledge-self-library.md": "docs/archive/boundary-self-knowledge-self-library.md",
    "COMPANION-SELF-museum library shelf-ALIGNMENT.md": (
        "docs/skill-work/work-companion-self/TEMPLATE-BASELINE.md"
    ),
    "platform/template/work-business.md": "docs/skill-work/work-business/README.md",
    "ingestion-and-sources.md": "docs/architecture.md",
    "project-6week-coding.md": "docs/contributing.md",
    "cursor-pack-from-seed.md": "platform/template/README.md",
    "evolving-practice-recursive-improvement.md": "docs/agent-rules/deep-rules.md",
    "export_manifest": "docs/portable-record/export-contract.md",
    "progressive-disclosure.md": "runtime/prepared-context/budgeted-work-strategy.md",
    "good-morning-brief-spec.md": "docs/skill-work/work-cadence/README.md",
    "good-night-brief-spec.md": "docs/skill-work/work-cadence/README.md",
    "good-night-template.md": "docs/skill-work/work-cadence/decision-fatigue-reduction.md",
    "speaker-accuracy-ledger.md": "statecraft/notes/speaker-audit-workflow.md",
    "speaker-credibility-accuracy-bridge.md": "statecraft/notes/speaker-audit-workflow.md",
    "speaker-credibility-matrix.md": "statecraft/notes/speaker-audit-workflow.md",
    "strategy-expert-template.md": "statecraft/voices/voice-profile-template.md",
    "continuity-log.jsonl": "docs/skill-work/work-dev/persistence-and-memory-surfaces.md",
    "sandbox-adapter.md": "docs/skill-work/work-dev/managed-agent-design.md",
    "analysis-grace-mar-self-evidence.md": "docs/archive/analysis-grace-mar-self-evidence.md",
    "ANALYSIS-GRACE-MAR-museum knowledge.md": "archive/grace-mar-instance/self-knowledge.md",
    "deveeopment-handoff.md": "docs/development-handoff.md",
    "canonical-paths.md": "docs/canonical-paths.md",
    "CIV-MEM.md": "archive/legacy-users/grace-mar/SELF-LIBRARY/CIV-MEM.md",
    "health-fitness-profile-hannah.md": (
        "archive/companion-freeze-abby-2026-04-14/companion-files/health-fitness-profile-hannah.md"
    ),
    "health-fitness-profile.md": (
        "archive/companion-freeze-abby-2026-04-14/companion-files/health-fitness-profile.md"
    ),
    "artifact-registry.md": "statecraft/artifact-registry.md",
    "review-queue.md": "statecraft/states/review-queue.md",
    "anchored-historical-citation-policy.md": (
        "statecraft/bridges/anchored-historical-citation-policy.md"
    ),
    "sid-desk-competitive-comparison.md": (
        "docs/skill-work/work-business/sid-desk-offer-spine.md"
    ),
    "arc-marandi-continuity.md": "statecraft/voices/marandi/marandi-arc.md",
    "arc-parsi-continuity.md": "statecraft/voices/parsi/parsi-arc.md",
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

    if re.match(r"arc-.+-host\.md$", norm):
        candidate = REPO_ROOT / "statecraft" / "notes" / norm
        if candidate.is_file():
            return candidate

    if basename.startswith("pape-marandi-parsi-"):
        candidate = REPO_ROOT / "statecraft" / "bridges" / basename
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

    if norm.startswith("public/predictive-history/book/volume-"):
        candidate = REPO_ROOT / "public/predictive-history/book/README.md"
        if candidate.is_file():
            return candidate

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
        if basename.endswith(".md") and basename not in {"README.md", "INDEX.md"}:
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


def fix_source_archive_master_index(text: str, file_path: Path) -> tuple[str, int]:
    rel = file_path.relative_to(REPO_ROOT).as_posix()
    if rel != "statecraft/sheets/source-archive-master-index.md":
        return text, 0
    count = 0
    patterns = [
        (
            r"\]\((\d{4}-\d{2}-\d{2})/day-index\.md\)",
            r"](../../source-archive/statecraft/\1/day-index.md)",
        ),
        (
            r"\]\(\.\./\.\./README\.md\) — Statecraft Archive - (\d{4}-\d{2}-\d{2})",
            r"](../../source-archive/statecraft/\1/README.md) — Statecraft Archive - \1",
        ),
        (
            r"\]\((\d{4}(?:-\d{2})?\.md)\)",
            r"](../../source-archive/statecraft/\1)",
        ),
    ]
    for pattern, repl in patterns:
        new_text, n = re.subn(pattern, repl, text)
        if n:
            text = new_text
            count += n
    # Undo double-prefix if regen + patch both ran.
    text, n = re.subn(
        r"\]\(\.\./\.\./\.\./\.\./source-archive/statecraft/\.\./\.\./source-archive/statecraft/",
        r"](../../source-archive/statecraft/",
        text,
    )
    count += n
    return text, count


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
        replacements.extend(
            [
                ("../../../../../.cursor/", "../../../.cursor/"),
                ("../../../../../../.cursor/", "../../../../.cursor/"),
                ("../_aired-pending/", "../../../../source-archive/statecraft/_aired-pending/"),
            ]
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
        replacements.extend(
            [
                ("../../../../../../../compact/", "../../compact/"),
                ("../../../../../../compact/", "../../compact/"),
                ("../../../../../compact/", "../../compact/"),
                ("../../../compact/", "../../compact/"),
            ]
        )

    if rel == "statecraft/notes/reentry/_templates/week-hinge-start-here.md":
        replacements.extend(
            [
                (
                    "[source-archive/statecraft/YYYY-MM.md](../../../../source-archive/statecraft/YYYY-MM/day-index.md)",
                    "`source-archive/statecraft/YYYY-MM/day-index.md`",
                ),
                (
                    "[YYYY-MM.md](../../synthesis/month/YYYY-MM.md)",
                    "`statecraft/synthesis/month/YYYY-MM.md`",
                ),
                (
                    "[YYYY-MM-weekN-1-start-here.md](../YYYY-MM-weekN-1-start-here.md)",
                    "`YYYY-MM-weekN-1-start-here.md` (prior week, same folder when instantiated)",
                ),
            ]
        )

    if rel == "statecraft/notes/arc-mercouris-continuity.md":
        replacements.extend(
            [
                (
                    "](../diesen/arc-mercouris-diesen-host.md -",
                    "](arc-mercouris-diesen-host.md) -",
                ),
                (
                    "(arc-mercouris-davis-host.md -",
                    "(arc-mercouris-davis-host.md) -",
                ),
                (
                    "](arc-mercouris-continuity-threads.md)",
                    "](../voices/mercouris/mercouris-arc-threads.md)",
                ),
            ]
        )

    if rel.startswith("statecraft/channels/dialogue-works/"):
        replacements.extend(
            [
                (
                    "[nima-profile.md](../../profiles/nima-profile.md and [nima-transcript.md](nima-transcript.md).",
                    "[nima-profile.md](nima-profile.md) and [nima-transcript.md](nima-transcript.md).",
                ),
                ("../../profiles/nima-profile.md", "nima-profile.md"),
                ("](transcript.md)", "](nima-transcript.md)"),
                ("`transcript.md`", "`nima-transcript.md`"),
                (
                    "../daily-strategy-inbox.md that include",
                    "../../../../codex/daily-strategy-inbox.md) that include",
                ),
                (
                    "nima-profile.md (cognitive profile)",
                    "nima-profile.md) (cognitive profile",
                ),
            ]
        )

    if rel == "statecraft/voices/mercouris/mercouris-thread.md":
        replacements.extend(
            [
                (
                    "](../../strategy-commentator-threads.md (`",
                    "](../../../codex/strategy-commentator-threads.md) (`",
                ),
                (
                    "](../../strategy-commentator-threads.md (",
                    "](../../../codex/strategy-commentator-threads.md) (",
                ),
            ]
        )

    if rel == "statecraft/synthesis/METHOD.md":
        replacements.append(
            (
                "./_templates/week-hinge-start-here.md",
                "../notes/reentry/_templates/week-hinge-start-here.md",
            )
        )

    if rel.startswith("statecraft/notes/") and "/reentry/" not in rel:
        replacements.append(("../../notes/", ""))
        replacements.append(("../../arc-mercouris-continuity.md", "arc-mercouris-continuity.md"))
        replacements.append(("](../../notes/)", "](../notes/)"))
        replacements.append(("](crooke-helix.md)", "](../voices/crooke/crooke-helix.md)"))
        replacements.append(("](macgregor-helix.md)", "](../voices/macgregor/macgregor-helix.md)"))
        replacements.append(("](mercouris-helix.md)", "](../voices/mercouris/mercouris-helix.md)"))

    if rel.startswith("statecraft/notes/watch/"):
        replacements.append(("../compact/", "../../compact/"))
        replacements.append(("../../../compact/", "../../compact/"))
        replacements.append(("../../../../compact/", "../../compact/"))

    if "work-strategy-rome/notes/exemplars" in rel:
        replacements.extend(
            [
                ("../../../../current-events-analysis.md", "../../../current-events-analysis.md"),
                ("../../../../civilizational-strategy-surface.md", "../../../civilizational-strategy-surface.md"),
                ("../../../../case-index.md", "../../../case-index.md"),
                ("../../../../promotion-ladder.md", "../../../promotion-ladder.md"),
            ]
        )

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
                ("../../.cursor/rules/", "../../../.cursor/rules/"),
                ("../../.codex-tmp/", "../../../.codex-tmp/"),
                ("../../../codex/academy/", "../../../../codex/academy/"),
                ("../../../../.cursor/rules/", "../../../.cursor/rules/"),
                ("../../../../../.cursor/rules/", "../../../.cursor/rules/"),
                ("../../../../.codex-tmp/", "../../../.codex-tmp/"),
                ("../../../../../.codex-tmp/", "../../../.codex-tmp/"),
                ("../../../../../codex/academy/", "../../../../codex/academy/"),
                ("../../../../../../codex/academy/", "../../../../codex/academy/"),
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

    if rel.startswith("statecraft/bridges/"):
        replacements.append(("../../america/", "../america/"))

    if rel.startswith("statecraft/notes/") and "/reentry/" not in rel and "/watch/" not in rel:
        replacements.append(("../../arc-", "arc-"))

    if rel.startswith("docs/skill-work/work-strategy/work-strategy-rome/notes/exemplars/"):
        replacements.extend(
            [
                ("../../current-events-analysis.md", "../../../current-events-analysis.md"),
                ("../../civilizational-strategy-surface.md", "../../../civilizational-strategy-surface.md"),
                ("../../case-index.md", "../../../case-index.md"),
                ("../../promotion-ladder.md", "../../../promotion-ladder.md"),
            ]
        )

    if rel.startswith("docs/skill-work/work-politics/"):
        replacements.extend(
            [
                ("../../wap-dashboard.md", "smm-workspace.md"),
                ("](approval-workflow.md)", "](../../externals/massie/smm-training/approval-workflow.md)"),
                ("](templates.md)", "](../../externals/massie/smm-training/templates.md)"),
                ("](massie-ky4.md)", "](clients/massie-ky4.md)"),
                ("](wap-candidate-template.md)", "](pol-candidate-template.md)"),
            ]
        )

    if rel.startswith("docs/runtime/"):
        replacements.append(("](runtime-worker.md)", "](../runtime-worker.md)"))

    if rel.startswith("docs/skill-work/work-civ-mem/"):
        replacements.extend(
            [
                ("topic-trace-tempeate.md", "topic-trace-template.md"),
                (
                    "../work-poeitics/civ-mem-draft-protocoe.md",
                    "../work-politics/civ-mem-draft-protocol.md",
                ),
            ]
        )

    if rel.startswith("docs/skill-work/work-moonshots/"):
        replacements.append(
            (
                "../../../self-moonshots.md",
                "../../../../archive/grace-mar-instance/self-moonshots.md",
            )
        )

    if rel.startswith("statecraft/voices/jiang/"):
        replacements.extend(
            [
                (
                    "../../../public/predictive-history/../../../public/predictive-history/",
                    "../../../public/predictive-history/",
                ),
                (
                    "[public/predictive-history/book/volume-i-civilization/interwoven-reader/README.md](../../../README.md)",
                    "[public/predictive-history/book/volume-i-civilization/interwoven-reader/README.md](../../../public/predictive-history/book/volume-i-civilization/interwoven-reader/README.md)",
                ),
                (
                    "[public/predictive-history/book/volume-i-civilization/parts/README.md](../../../README.md)",
                    "[public/predictive-history/book/volume-i-civilization/parts/README.md](../../../public/predictive-history/book/volume-i-civilization/parts/README.md)",
                ),
                (
                    "[parts/](../../../README.md)",
                    "[parts/](../../../public/predictive-history/book/volume-i-civilization/parts/README.md)",
                ),
                (
                    "[interwoven-reader](../../../README.md)",
                    "[interwoven-reader](../../../public/predictive-history/book/volume-i-civilization/interwoven-reader/README.md)",
                ),
            ]
        )

    if "work-strategy-rome/notes/exemplars" in rel:
        replacements.extend(
            [
                ("../../../../current-events-analysis.md", "../../../current-events-analysis.md"),
                ("../../../../civilizational-strategy-surface.md", "../../../civilizational-strategy-surface.md"),
                ("../../../../case-index.md", "../../../case-index.md"),
                ("../../../../promotion-ladder.md", "../../../promotion-ladder.md"),
                ("](../ROME-PASS.md)", "](../../ROME-PASS.md)"),
            ]
        )

    if rel.startswith("statecraft/notes/wire/"):
        replacements.append(("../notes/", "../"))

    if rel.startswith("statecraft/notes/watch/"):
        replacements.append(("../america/", "../../america/"))

    if rel.startswith("statecraft/notes/reentry/"):
        replacements.extend(
            [
                ("../persia/", "../../persia/"),
                (
                    "../notes/iran-war-inquiry-ladder-stress-test.md",
                    "../iran-war-inquiry-ladder-stress-test.md",
                ),
                (
                    "../notes/russia-inquiry-ladder-as-recursive-learning.md",
                    "../russia-inquiry-ladder-as-recursive-learning.md",
                ),
                ("../compact/", "../../compact/"),
            ]
        )

    if rel.startswith("statecraft/notes/") and "/wire/" not in rel and "/watch/" not in rel and "/reentry/" not in rel and "/intake/" not in rel:
        replacements.append(("../../artifacts/", "../../../runtime/artifacts/"))
        replacements.append(
            ("../voices/pape/arc-pape-continuity.md", "../arc-pape-continuity.md")
        )

    if rel.startswith("statecraft/notes/intake/"):
        replacements.append(("../persia/", "../../persia/"))

    if rel.startswith("docs/skill-work/work-politics/"):
        replacements.append(("../../work-strategy/", "../work-strategy/"))

    if rel.startswith("docs/skill-work/work-strategy/history-notebook/"):
        replacements.extend(
            [
                ("../../../codex/chapters/", "../../../../codex/chapters/"),
                ("../../../.cursor/rules/", "../../../../.cursor/rules/"),
            ]
        )

    if rel.startswith("docs/skill-work/work-strategy/") and "speaker-arc-vs-comparative" in rel:
        replacements.append(("../../notes/", "../../../statecraft/notes/"))

    if rel.startswith("skills/runbooks/"):
        replacements.append(("../../../.cursor/rules/", "../../.cursor/rules/"))

    if rel.startswith("statecraft/sheets/source-archive-residue/"):
        replacements.extend(
            [
                (
                    "strategy-state-iran/voices/iri-institutional/thread.md",
                    "../../../../codex/strategy-state-iran/voices/iri-institutional/thread.md",
                ),
                (
                    "../daily-brief-",
                    "../../../../docs/skill-work/work-strategy/daily-brief-",
                ),
                (
                    "../crooke/crooke-page-",
                    "../../../voices/crooke/crooke-page-",
                ),
            ]
        )

    if rel.startswith("docs/skill-work/work-strategy/"):
        replacements.extend(
            [
                ("../../.cursor/rules/", "../../../.cursor/rules/"),
                (
                    "../../../statecraft/states/sacred-grammar/rome.md",
                    "../../../../statecraft/states/volumes/civ-state-rome/sacred-grammar.md",
                ),
                (
                    "../../codex/strategy-expert-davis-thread.md",
                    "../../../../statecraft/voices/davis/davis-thread.md",
                ),
                ("../../notes/arc-freeman", "../../../statecraft/notes/arc-freeman"),
            ]
        )

    if rel.startswith("docs/skill-work/work-strategy/minds/"):
        replacements.extend(
            [
                ("**LIB:** []", "**LIB:** [self-library.md]"),
                ("**Not** the same as []", "**Not** the same as [self-library.md]"),
                (
                    "](../../../../civilization_memory)",
                    "](../../../../research/repos/civilization_memory)",
                ),
                (
                    "../../../../CIV-MEM.md",
                    "../../../../archive/legacy-users/grace-mar/SELF-LIBRARY/CIV-MEM.md",
                ),
            ]
        )

    if rel.startswith("docs/skill-work/work-dev/control-plane/"):
        replacements.extend(
            [
                (
                    "../../../../action-receipts.md",
                    "../../../../../docs/action-receipts.md",
                ),
                (
                    "../../../../mcp/mcp-execution-receipts.md",
                    "../../../../../docs/mcp/mcp-execution-receipts.md",
                ),
            ]
        )

    if rel.startswith("docs/skill-work/work-politics/") and "smm-xavier-handbook-bundle" in rel:
        replacements.extend(
            [
                ("](../calendar-2026.md)", "](calendar-2026.md)"),
                ("](../compliance-checklist.md)", "](compliance-checklist.md)"),
                ("](../opposition-brief.md)", "](opposition-brief.md)"),
                ("](../principal-profile.md)", "](principal-profile.md)"),
                ("](skill-work/work-politics/", "]("),
                (
                    "](content-playbook.md)",
                    "](../../externals/massie/smm-training/content-playbook.md)",
                ),
                (
                    "](day-1-quickstart.md)",
                    "](../../externals/massie/smm-training/day-1-quickstart.md)",
                ),
                (
                    "](kpi-scorecard.md)",
                    "](../../externals/massie/smm-training/kpi-scorecard.md)",
                ),
                (
                    "](daily-operating-rhythm.md)",
                    "](../../externals/massie/smm-training/daily-operating-rhythm.md)",
                ),
                ("](AGENT-SESSION-BRIEF.md)", "](america-first-ky/AGENT-SESSION-BRIEF.md)"),
                (
                    "](massie-issue-asymmetry.md)",
                    "](clients/massie-issue-asymmetry.md)",
                ),
                ("](miniapp-setup.md)", "](../../../miniapp-setup.md)"),
                (
                    "](../../../miniapp-setup.md)",
                    "](../../miniapp-setup.md)",
                ),
                (
                    "](week-1-ramp-plan.md)",
                    "](clients/massie-ky4-operator-checklist.md)",
                ),
                (
                    "](stress-test-brief-template.md)",
                    "](america-first-ky/stress-test-brief-template.md)",
                ),
            ]
        )

    if rel.startswith("statecraft/states/archive/"):
        replacements.extend(
            [
                ("](volumes/civ-state-", "](../../volumes/civ-state-"),
                ("](../../volumes/persia/bibliography.md)", "](../../volumes/civ-state-persia/civ-state-persia-bibliography.md)"),
                ("](../../volumes/china/bibliography.md)", "](../../volumes/civ-state-china/civ-state-china-bibliography.md)"),
                ("](../../volumes/rome/bibliography.md)", "](../../volumes/civ-state-rome/civ-state-rome-bibliography.md)"),
                ("](../../volumes/russia/bibliography.md)", "](../../volumes/civ-state-russia/civ-state-russia-bibliography.md)"),
                ("](../../volumes/america/bibliography.md)", "](../../volumes/civ-state-america/civ-state-america-bibliography.md)"),
                ("../volumes/", "../../volumes/"),
                ("../../../volumes/", "../../volumes/"),
                (
                    "../../volumes/rome/source-shelf.md",
                    "../../volumes/civ-state-rome/civ-state-rome-bibliography.md",
                ),
                ("../../glossary.md", "../../../glossary.md"),
            ]
        )

    if rel.startswith("statecraft/voices/mercouris/"):
        replacements.extend(
            [
                (
                    "../diesen/arc-mercouris-diesen-host.md",
                    "../../notes/arc-mercouris-diesen-host.md",
                ),
                (
                    "../../channels/daniel-davis/arc-mercouris-davis-host.md",
                    "../../notes/arc-mercouris-davis-host.md",
                ),
            ]
        )

    if rel.startswith("statecraft/voices/mearsheimer/"):
        replacements.extend(
            [
                ("../../notes/mearsheimer-arc.md", "mearsheimer-arc.md"),
                (
                    "../../minds/MINDS-SKILL-STRATEGY-PATTERNS.md",
                    "../../../../docs/skill-work/work-strategy/minds/MINDS-SKILL-STRATEGY-PATTERNS.md",
                ),
                (
                    "../../academy/statecraft/civ-emp/",
                    "../../../codex/academy/statecraft/civ-emp/",
                ),
                ("../../../codex/mearsheimer-mind.md", "mearsheimer-mind.md"),
                ("../../../../../../.cursor/", "../../../.cursor/"),
            ]
        )

    if rel.startswith("statecraft/synthesis/day/") or rel.startswith("statecraft/synthesis/month/"):
        replacements.extend(
            [
                ("../persia/", "../../persia/"),
                ("../../artifacts/", "../../../runtime/artifacts/"),
                ("../compact/", "../../compact/"),
                ("2026-06-week3-start-here.md", "2026-06-week2-start-here.md"),
            ]
        )

    if rel.startswith("statecraft/states/volumes/"):
        replacements.extend(
            [
                (
                    "../../../config/civilizational_statecraft_public_export.yaml",
                    "../../../../platform/config/civilizational_statecraft_public_export.yaml",
                ),
                ("](theory/README.md)", "](../../public/civ-state/theory/README.md)"),
                (
                    "../../../persia/iran-doctrine.md",
                    "../../../persia/transactions/lebanon-third-party-recognition-gate-transaction.md",
                ),
                (
                    "../../../rome/rome-volume-writer-guide.md",
                    "../civ-state-rome/README.md",
                ),
                (
                    "../../../russia/russia-doctrine.md",
                    "../../../russia/transactions/README.md",
                ),
            ]
        )

    if rel.startswith("statecraft/states/export-templates/"):
        replacements.extend(
            [
                ("../source-lattice.md", "source-lattice.md"),
                ("](theory/civilization.md)", "](../../public/civ-state/theory/civilization.md)"),
                ("](theory/empire.md)", "](../../public/civ-state/theory/empire.md)"),
                ("](theory/entropy.md)", "](../../public/civ-state/theory/entropy.md)"),
                ("](theory/faith.md)", "](../../public/civ-state/theory/faith.md)"),
                ("](theory/science.md)", "](../../public/civ-state/theory/science.md)"),
                ("](theory/memory.md)", "](../../public/civ-state/theory/memory.md)"),
                (
                    "](theory/rhythm.md)",
                    "](../../public/civ-state/theory/memory.md#civilizational-rhythm)",
                ),
                (
                    "](theory/time.md)",
                    "](../../public/civ-state/theory/memory.md#era-law)",
                ),
                ("](../../../memory.md)", "](../../public/civ-state/theory/memory.md)"),
                ("](docs/reader-guide.md", "](../reader-guide.md"),
                ("](docs/table-of-contents.md", "](../table-of-contents.md"),
                ("](docs/FOUNDING-PROVENANCE.md", "](FOUNDING-PROVENANCE.md)"),
                ("](docs/names-and-titles.md", "](../reader-guide.md#names-and-titles"),
                ("](docs/era-spine.md", "](../reader-guide.md#era-law"),
                ("](docs/hybrid-references.md", "](../hybrid-references.md)"),
                ("](docs/release-history.md", "](../README.md#release-history"),
                ("](EXPORT-RECEIPT.md", "](FOUNDING-PROVENANCE.md"),
                ("../../table-of-contents.md", "../table-of-contents.md"),
            ]
        )

    if rel.startswith("statecraft/states/") and not rel.startswith(
        "statecraft/states/export-templates/"
    ):
        replacements.extend(
            [
                (
                    "](theory/rhythm.md)",
                    "](../../public/civ-state/theory/memory.md#civilizational-rhythm)",
                ),
                (
                    "](theory/time.md)",
                    "](../../public/civ-state/theory/memory.md#era-law)",
                ),
                (
                    "../../public/civ-state/theory/rhythm.md",
                    "../../public/civ-state/theory/memory.md#civilizational-rhythm",
                ),
                (
                    "../../public/civ-state/theory/time.md",
                    "../../public/civ-state/theory/memory.md#era-law",
                ),
            ]
        )

    if rel.startswith("statecraft/voices/"):
        replacements.append(
            ("../../daily-strategy-inbox.md", "../../../codex/daily-strategy-inbox.md")
        )

    if rel.startswith("statecraft/voices/pape/"):
        replacements.extend(
            [
                (
                    "](../../profiles/pape-profile.md (profile)",
                    "](pape-profile.md) (profile",
                ),
                (
                    "`](../../sheets/source-archive-control/README.md.",
                    "`](../../sheets/source-archive-control/README.md).",
                ),
                (
                    "../../../codex/2026/pape/pape-transcript.md",
                    "pape-transcript.md",
                ),
                (
                    "../../../codex/2026/pape/pape-thread.md",
                    "pape-thread.md",
                ),
            ]
        )

    if rel.startswith("statecraft/voices/"):
        speaker = rel.split("/")[2] if rel.count("/") >= 3 else ""
        if speaker:
            replacements.extend(
                [
                    (
                        f"../../../statecraft/voices/{speaker}/{speaker}-thread.md",
                        f"{speaker}-thread.md",
                    ),
                    (
                        f"../../../statecraft/voices/{speaker}/{speaker}-transcript.md",
                        f"{speaker}-transcript.md",
                    ),
                    (
                        f"../../../statecraft/voices/{speaker}/stream",
                        f"{speaker}-routing.md",
                    ),
                    (f"../../notes/{speaker}-arc.md", f"{speaker}-arc.md"),
                    ("../../profiles/", "../"),
                    ("../../../minds/CIV-MIND-", "../../../codex/minds/CIV-MIND-"),
                    ("../../minds/CIV-MIND-", "../../../codex/minds/CIV-MIND-"),
                    ("](minds/CIV-MIND-", "](../../../codex/minds/CIV-MIND-"),
                    (
                        f"../../../codex/2026/{speaker}/{speaker}-thread.md",
                        f"{speaker}-thread.md",
                    ),
                    (
                        f"../../../codex/2026/{speaker}/{speaker}-transcript.md",
                        f"{speaker}-transcript.md",
                    ),
                    (
                        "strategy-expert-mearsheimer-mind.md",
                        "mearsheimer-mind.md",
                    ),
                    (
                        "strategy-expert-parsi-transcript.md",
                        "parsi-transcript.md",
                    ),
                ]
            )
        replacements.append(
            (
                "](../minds/MINDS-SKILL-STRATEGY-PATTERNS.md for",
                "](../../../../docs/skill-work/work-strategy/minds/MINDS-SKILL-STRATEGY-PATTERNS.md) for",
            )
        )

    if rel.startswith("statecraft/voices/johnson/"):
        replacements.append(("../../notes/johnson-arc.md", "johnson-arc.md"))

    if rel.startswith("statecraft/voices/ritter/"):
        replacements.extend(
            [
                ("../../../ritter-thread.md", "ritter-thread.md"),
                ("../../../ritter-transcript.md", "ritter-transcript.md"),
            ]
        )

    if rel.startswith("statecraft/voices/karaganov/"):
        replacements.append(
            ("../diesen/arc-karaganov-diesen-host.md", "../../notes/arc-karaganov-diesen-host.md")
        )

    if rel.startswith("statecraft/voices/diesen/"):
        replacements.extend(
            [
                ("../crooke/crooke-page-", "../../crooke/crooke-page-"),
                ("](stream)", "](diesen-routing.md)"),
                ("](stream->", "](diesen-routing.md"),
            ]
        )

    if rel.startswith("statecraft/voices/crooke/"):
        replacements.append(("../crooke-profile.md (profile", "crooke-profile.md) (profile"))

    if rel.startswith("statecraft/voices/davis/"):
        replacements.extend(
            [
                ("(../davis-transcript.md", "(davis-transcript.md"),
                ("(../davis-thread.md", "(davis-thread.md"),
                ("(../davis-profile.md", "(davis-profile.md"),
                (
                    "strategy-state-iran/voices/iri-institutional/thread.md",
                    "../../../../codex/strategy-state-iran/voices/iri-institutional/thread.md",
                ),
            ]
        )

    if rel.startswith("statecraft/voices/mercouris/"):
        replacements.append(
            (
                "strategy-state-iran/voices/iri-institutional/thread.md",
                "../../../../codex/strategy-state-iran/voices/iri-institutional/thread.md",
            )
        )

    if rel == "statecraft/recursive-learning-journal.md":
        replacements.extend(
            [
                (
                    "](daily/2026-06-08-barnes-america-capture-non-intercept-colby-mou.md)",
                    "](../notes/2026-06-08-barnes-america-capture-non-intercept-colby-mou.md)",
                ),
                (
                    "](../notes/2026-06-08-barnes-america-capture-non-intercept-colby-mou.md)",
                    "](notes/2026-06-08-barnes-america-capture-non-intercept-colby-mou.md)",
                ),
            ]
        )

    if rel == "statecraft/voices/core-thesis-matrix-pilot.md":
        replacements.extend(
            [
                ("../notes/barnes-arc.md", "barnes/barnes-arc.md"),
                ("../notes/johnson-arc.md", "johnson/johnson-arc.md"),
                ("../notes/marandi-arc.md", "marandi/marandi-arc.md"),
                ("../barnes/barnes-arc.md", "barnes/barnes-arc.md"),
                ("../johnson/johnson-arc.md", "johnson/johnson-arc.md"),
                ("../marandi/marandi-arc.md", "marandi/marandi-arc.md"),
            ]
        )

    if rel == "statecraft/sheets/civ-mem-resonance-2026-04.md":
        replacements.extend(
            [
                ("](alkhorshid/alkhorshid-book-2026-04.md)", "](../voices/alkhorshid/alkhorshid-profile.md)"),
                ("](diesen/diesen-book-2026-04.md)", "](../voices/diesen/diesen-profile.md)"),
                ("](mercouris/mercouris-book-2026-04.md)", "](../voices/mercouris/mercouris-profile.md)"),
                ("](davis/davis-book-2026-04.md)", "](../voices/davis/davis-profile.md)"),
            ]
        )

    if rel.startswith("docs/skill-write/"):
        replacements.extend(
            [
                ("../../../.cursor/rules/", "../../.cursor/rules/"),
                ("(../.cursor/rules/", "(../../.cursor/rules/"),
                ("](../.cursor/rules/", "](../../.cursor/rules/"),
            ]
        )

    if rel == "docs/merging-from-companion-self.md":
        replacements.extend(
            [
                (
                    "../demo/observability/observability-report.json",
                    "../../archive/legacy-users/demo/observability/observability-report.json",
                ),
                (
                    "../demo/seed-phase/work_business_seed.json",
                    "../platform/users/demo/seed-phase/work_business_seed.json",
                ),
                ("../demo/seed-phase/", "../platform/users/demo/seed-phase/"),
                (
                    "skill-work/work-companion-self/COMPANION-SELF-museum library shelf-ALIGNMENT.md",
                    "skill-work/work-companion-self/TEMPLATE-BASELINE.md",
                ),
                (
                    "../platform/template/work-business.md",
                    "skill-work/work-business/README.md",
                ),
            ]
        )

    if rel.startswith("docs/") and not rel.startswith("docs/skill-work/"):
        slash_depth = rel.count("/")
        replacements.extend(
            [
                ("../platform/integrations/", "../integrations/"),
                ("../memory-template.md", "memory-template.md"),
                ("integration-apis.md", "architecture.md"),
                ("../skill-work.md", "skill-work/README.md"),
                (
                    ".cursor/skills/handoff-check/SKILL.md",
                    "../.cursor/skills/handoff-check/SKILL.md",
                ),
                ("../integrations/openclaw_stage.py", "../../platform/integrations/openclaw_stage.py"),
                ("../cadence-learning-events.jsonl", "../../runtime/operator-events/cadence-learning-events.jsonl"),
                (
                    "../diagnostics-and-governance-tools.mdcounterfactual-",
                    "../examples/diagnostics/counterfactual-",
                ),
                (
                    "diagnostics-and-governance-tools.mdcounterfactual-",
                    "examples/diagnostics/counterfactual-",
                ),
            ]
        )
        if slash_depth >= 2:
            replacements.extend(
                [
                    ("(../.cursor/skills/", "(../../.cursor/skills/"),
                    ("(../.cursor/rules/", "(../../.cursor/rules/"),
                    ("](../.cursor/skills/", "](../../.cursor/skills/"),
                    ("](../.cursor/rules/", "](../../.cursor/rules/"),
                ]
            )
        if slash_depth >= 3:
            replacements.extend(
                [
                    ("(../../.cursor/skills/", "(../../../.cursor/skills/"),
                    ("(../../.cursor/rules/", "(../../../.cursor/rules/"),
                ]
            )

    if rel.startswith("docs/archive/"):
        replacements.append(("](memory-template.md)", "](../memory-template.md)"))

    if rel.startswith("docs/portable-record/"):
        replacements.extend(
            [
                ("../platform/integrations/", "../../integrations/"),
                (
                    "../../integrations/mcp_adapter.py",
                    "../../platform/integrations/mcp_adapter.py",
                ),
                (
                    "../../../runtime/artifacts/rationales/",
                    "artifact-rationale.md",
                ),
                (
                    "../../runtime/artifacts/rationales/",
                    "artifact-rationale.md",
                ),
                (
                    "../../runtime/prepared-context/progressive-disclosure.md",
                    "../../runtime/prepared-context/budgeted-work-strategy.md",
                ),
            ]
        )

    if rel.startswith("docs/runtime/"):
        replacements.extend(
            [
                (
                    "../runtime/prepared-context/progressive-disclosure.md",
                    "../../runtime/prepared-context/budgeted-work-strategy.md",
                ),
                (
                    "runtime/prepared-context/progressive-disclosure.md",
                    "../../runtime/prepared-context/budgeted-work-strategy.md",
                ),
                (
                    "../../orchestration/review-orchestrator.md",
                    "../orchestration/review-orchestrator.md",
                ),
                ("](runtime-vs-record.md)", "](../runtime-vs-record.md)"),
                (
                    "](../runtime_workers/registry.yaml",
                    "](../../platform/config/runtime_workers/registry.yaml",
                ),
            ]
        )

    if rel == "docs/predictive-history-external-boundary.md":
        replacements.append(
            (
                "../public/predictive-history/DO-NOT-EDIT.md",
                "../public/predictive-history/MIRROR-RECEIPT.md",
            )
        )

    if rel == "docs/singularity-statecraft-handoff-law.md":
        replacements.append(
            (
                "../statecraft/states/high-skill-labor-compression-and-civilizational-statecraft.md",
                "../statecraft/states/essays/high-skill-labor-compression-and-civilizational-statecraft.md",
            )
        )

    if rel == "docs/skill-think/observability.md":
        replacements.append(
            (
                "../WORK-LAYER-HARDENING-ROADMAP.md",
                "../skill-work/WORK-LAYER-HARDENING-ROADMAP.md",
            )
        )

    if rel == "docs/state-model.md":
        replacements.append(
            (
                "](../../integrations/ob1/mapping.md",
                "](integrations/ob1/mapping.md",
            )
        )

    if rel == "docs/skills-map.md":
        replacements.append(
            (
                "](statecraft-opener-pack.md)",
                "](skills/statecraft-opener-pack.md)",
            )
        )

    if rel == "docs/skill-work/work-strategy/predictive-history-comment-rollout/README.md":
        replacements.append(
            (
                "statecraft/voices/civ-lens-jiang/ph-civ/docs/source-video-index.md",
                "../../../../public/predictive-history/docs/predictive-history-index.md",
            )
        )

    if rel == "runtime/artifacts/operator-command-deck/README.md":
        replacements.append(
            (
                "](../../../recursion-gate.md)",
                "](../../../archive/grace-mar-instance/recursion-gate.md)",
            )
        )

    if rel.startswith("docs/mcp/"):
        replacements.append(("../platform/integrations/", "../../integrations/"))

    if rel.startswith("statecraft/synthesis/") and "/day/" not in rel and "/month/" not in rel:
        replacements.extend(
            [
                (
                    "../../persia/transactions/lebanon-third-party-recognition-gate-transaction.md",
                    "../persia/transactions/lebanon-third-party-recognition-gate-transaction.md",
                ),
                ("../../persia/", "../persia/"),
            ]
        )

    if rel.startswith("docs/skill-work/work-strategy/history-notebook/POLYPHONY-WORKFLOW.md"):
        replacements.extend(
            [
                (
                    "../../../.cursor/rules/strategy-minds-granular.mdc",
                    "../../../../.cursor/rules/strategy-minds-granular.mdc",
                ),
                (
                    "../../../../codex/chapters/YYYY-MM/meta.md",
                    "../../../../codex/chapters/2026/2026-04/meta.md",
                ),
                ("codex/chapters/YYYY-MM/", "codex/chapters/2026/2026-04/"),
            ]
        )

    if rel.startswith("docs/skill-work/"):
        slash_depth = rel.count("/")
        replacements.extend(
            [
                ("../../memory-template.md", "../memory-template.md"),
                ("../../operator-agent-lanes.md", "../operator-agent-lanes.md"),
                ("](../work-coffee/menu-reference.md", "](work-coffee/menu-reference.md)"),
                ("../../good-morning-brief-spec.md", "README.md"),
                ("../../good-night-brief-spec.md", "README.md"),
                ("../../good-night-template.md", "decision-fatigue-reduction.md"),
                ("../../../scripts/good-night-brief.py", "../../../scripts/operator_end_of_day.py"),
                ("../../daily-brief-jiang-layer.md", "../../../docs/skill-work/work-strategy/daily-brief-jiang-layer.md"),
                ("../../LEARN_MODE_RULES.md", "../../../docs/skill-work/work-strategy/LEARN_MODE_RULES.md"),
                ("../../../good-morning-brief-spec.md", "../../good-morning-brief-spec.md"),
                ("../../../good-night-brief-spec.md", "../../good-night-brief-spec.md"),
                ("../../../good-night-template.md", "../../good-night-template.md"),
                ("../../../self-work.md", "../../self-work/README.md"),
            ]
        )

    if rel == "docs/instance-patterns.md" or rel == "docs/schema-record-api.md":
        replacements.append(("](project-6week-coding.md)", "](../contributing.md)"))

    if rel == "docs/library-schema.md":
        replacements.append(
            (
                "../skill-work/lesson-rules-config.yaml",
                "skill-work/lesson-rules-config.yaml",
            )
        )

    if rel == "statecraft/notes/speaker-audit-workflow.md":
        replacements.extend(
            [
                ("](speaker-accuracy-ledger.md)", "](speaker-audit-workflow.md)"),
                (
                    "](speaker-credibility-accuracy-bridge.md)",
                    "](speaker-audit-workflow.md)",
                ),
                ("](speaker-credibility-matrix.md)", "](speaker-audit-workflow.md)"),
            ]
        )

    if rel == "statecraft/notes/recognition-threshold-vs-settlement-architecture.md":
        replacements.extend(
            [
                (
                    "](anchored-historical-citation-policy.md)",
                    "](../bridges/anchored-historical-citation-policy.md)",
                ),
                (
                    "](persia-recognition-vs-settlement-bridge.md)",
                    "](../bridges/persia-recognition-vs-settlement-bridge.md)",
                ),
                (
                    "](marandi-civ-state-retrieval-adapter.md)",
                    "](../bridges/marandi-civ-state-retrieval-adapter.md)",
                ),
                (
                    "](parsi-civ-state-retrieval-adapter.md)",
                    "](../bridges/parsi-civ-state-retrieval-adapter.md)",
                ),
            ]
        )

    if rel == "statecraft/voices/map/open-first-routes.md":
        replacements.extend(
            [
                (
                    "../../channels/daniel-davis/arc-barnes-davis-host.md",
                    "../../notes/arc-barnes-davis-host.md",
                ),
                (
                    "../../channels/dialogue-works/arc-freeman-nima-host.md",
                    "../../notes/arc-freeman-nima-host.md",
                ),
                (
                    "../freeman/arc-march-2026-cross-host-freeman-host.md",
                    "../freeman/freeman-march-2026-cross-host-arc.md",
                ),
                ("../napolitano/", "../notes/"),
            ]
        )

    if rel == "statecraft/voices/jiang/jiang-profile.md":
        replacements.extend(
            [
                (
                    "../../LEARN_MODE_RULES.md",
                    "../../../../docs/skill-work/work-strategy/LEARN_MODE_RULES.md",
                ),
                (
                    "../../daily-brief-jiang-layer.md",
                    "../../../../docs/skill-work/work-strategy/daily-brief-jiang-layer.md",
                ),
                (
                    "strategy-expert-template.md#voice-fingerprint-compact",
                    "../voice-profile-template.md#voice-fingerprint-compact",
                ),
            ]
        )

    if rel == "statecraft/voices/macgregor/macgregor-routing.md":
        replacements.extend(
            [
                (
                    "../../../statecraft/channels/daniel-davis/stream",
                    "../../channels/daniel-davis/index.md",
                ),
                (
                    "../../../statecraft/voices/diesen/stream",
                    "../diesen/index.md",
                ),
                (
                    "../../../statecraft/channels/judging-freedom/stream",
                    "../../channels/judging-freedom/index.md",
                ),
            ]
        )

    if rel.startswith("statecraft/states/archive/theory-cross-case-v1/"):
        replacements.extend(
            [
                ("../../../../../../../glossary.md", "../../../glossary.md"),
                (
                    "../../../volumes/civ-state-china/",
                    "../../volumes/civ-state-china/",
                ),
                (
                    "../../../volumes/civ-state-persia/",
                    "../../volumes/civ-state-persia/",
                ),
                (
                    "../../../volumes/civ-state-rome/",
                    "../../volumes/civ-state-rome/",
                ),
            ]
        )

    if rel.startswith("docs/automation/"):
        replacements.append(("../../../.cursor/", "../../.cursor/"))

    if rel.startswith("docs/skill-work/work-coffee/"):
        replacements.extend(
            [
                ("../operator-agent-lanes.md", "../../operator-agent-lanes.md"),
                ("../../memory-self-audit.md", "../../archive/memory-self-audit.md"),
            ]
        )

    if rel.startswith("docs/skill-work/work-dev/"):
        replacements.extend(
            [
                ("../operator-agent-lanes.md", "../../operator-agent-lanes.md"),
                ("../memory-template.md", "../../memory-template.md"),
                ("../../platform/integrations/", "../../integrations/"),
                ("../../../platform/integrations/", "../../../integrations/"),
                ("../../../../platform/integrations/", "../../../../integrations/"),
                ("../../../../../platform/integrations/", "../../../../../integrations/"),
                (
                    "../../../../../../platform/integrations/",
                    "../../../../../../integrations/",
                ),
                (
                    "](../../work-strategy/daily-brief-config.json",
                    "](../work-strategy/daily-brief-config.json",
                ),
                (
                    "polyphonic-cognition-protocol-skill.md",
                    "../work-politics/polyphonic-cognition-protocol-skill.md",
                ),
                (
                    "semantic-work-primitives.md",
                    "lessons-deepseek-insider-self-improving-agents.md",
                ),
                (
                    "research-semantic-work-primitives-nate-b-jones.md",
                    "../../../research/external/work-dev/transcripts/nate-b-jones-semantic-work-primitives-transcript-2026.txt",
                ),
                (
                    "nate-b-jones-google-stitch-design-markdown-meeting-transcript-2026.md",
                    "nate-b-jones-google-stitch-design-markdown-meeting-transcript-2026.txt",
                ),
                (
                    "interface-runtime/artifacts/INTERFACE-ARTIFACT-PROTOCOL.md",
                    "interface-artifacts/INTERFACE-ARTIFACT-PROTOCOL.md",
                ),
                (
                    "../../../runtime/artifacts/creative/",
                    "../../../runtime/artifacts/",
                ),
                (
                    "statecraft/voices/ritter/stream",
                    "statecraft/voices/ritter/index.md",
                ),
                (
                    "../../../../../docs/platform/integrations/",
                    "../../../../platform/integrations/",
                ),
                (
                    "../../../../../platform/users/grace-mar/dev-journal",
                    "../../../../../../archive/grace-mar-instance/",
                ),
            ]
        )

    if rel.startswith("docs/skill-work/self-work/"):
        replacements.append(
            (
                "../decision-fatigue-reduction.md",
                "../../work-cadence/decision-fatigue-reduction.md",
            )
        )

    if rel.startswith("docs/skill-work/skill-work-human-teacher/"):
        replacements.append(
            (
                "../../../skill-think/",
                "../../skill-think/",
            )
        )

    if rel.startswith("docs/skill-work/work-business/"):
        replacements.append(
            (
                "sid-desk-competitive-comparison.md",
                "sid-desk-offer-spine.md",
            )
        )

    if rel.startswith("docs/skill-work/work-civ-mem/"):
        replacements.append(
            (
                "../../deveeopment-handoff.md",
                "../../development-handoff.md",
            )
        )

    if rel.startswith("docs/skill-work/work-companion-self/"):
        replacements.append(
            (
                "../../../canonical-paths.md",
                "../../canonical-paths.md",
            )
        )

    if rel.startswith("docs/skill-work/work-dream/"):
        replacements.append(
            (
                "../work-cici/cici-notebook/",
                "../../../singularity/work-cici/cici-notebook/",
            )
        )

    if rel.startswith("docs/skill-work/work-health-fitness/"):
        replacements.extend(
            [
                (
                    "../../../health-fitness-profile-hannah.md",
                    "../../../../archive/companion-freeze-abby-2026-04-14/companion-files/health-fitness-profile-hannah.md",
                ),
                (
                    "../../../health-fitness-profile.md",
                    "../../../../archive/companion-freeze-abby-2026-04-14/companion-files/health-fitness-profile.md",
                ),
            ]
        )

    if rel == "docs/skill-work/work-strategy/DEFAULT-PATH.md":
        replacements.append(
            (
                "work-coffee/menu-reference.md",
                "../work-coffee/menu-reference.md",
            )
        )

    if rel.startswith("docs/skill-work/work-strategy/history-notebook/research/"):
        replacements.append(
            (
                "../../../../.github/workflows/",
                "../../../../../.github/workflows/",
            )
        )

    if rel.startswith("docs/skill-work/work-template/"):
        replacements.extend(
            [
                ("../operator-agent-lanes.md", "../../operator-agent-lanes.md"),
                (
                    "../work-cici/legacy-aliases.yml",
                    "../../../singularity/work-cici/legacy-aliases.yml",
                ),
            ]
        )

    if rel.startswith("docs/skill-work/work-dev/"):
        replacements.extend(
            [
                (
                    "../../../../platform/integrations/",
                    "../../../../integrations/",
                ),
                (
                    "../../../CIV-MEM.md",
                    "../../../../archive/legacy-users/grace-mar/SELF-LIBRARY/CIV-MEM.md",
                ),
            ]
        )

    if any(
        rel.startswith(p)
        for p in (
            "statecraft/notes/intake/",
            "statecraft/notes/watch/",
            "statecraft/notes/wire/",
        )
    ):
        replacements.extend(
            [
                ("../synthesis/", "../../synthesis/"),
                ("../source-archive/", "../../../source-archive/"),
                ("../notes/", "./"),
                ("../america/transactions/", "../../america/transactions/"),
            ]
        )

    if any(
        rel.startswith(p)
        for p in (
            "statecraft/notes/jiang-on-ai.md",
            "statecraft/notes/statecraft-v1-upgrade-plan",
            "statecraft/notes/pape-marandi",
            "statecraft/notes/recursive-learning",
        )
    ) or rel.startswith("statecraft/notes/arc-") or rel in {
        "statecraft/notes/arc-weichert-continuity.md",
        "statecraft/notes/arc-ritter-india-global-left-iran.md",
        "statecraft/notes/arc-may-2026-cross-context-parsi-host.md",
        "statecraft/notes/arc-karaganov-diesen-host.md",
    }:
        replacements.extend(
            [
                ("../../synthesis/", "../synthesis/"),
                ("../source-archive/", "../../../source-archive/"),
                ("../voices/jiang/", "../../voices/jiang/"),
                ("../marandi/", "../../voices/marandi/"),
                ("../karaganov/", "../voices/karaganov/"),
                (
                    "states/review-queue.md",
                    "../../states/review-queue.md",
                ),
                (
                    "artifact-registry.md",
                    "../artifact-registry.md",
                ),
            ]
        )

    if rel.startswith("statecraft/sheets/"):
        replacements.append(
            (
                "../../transactions/",
                "../transactions/",
            )
        )

    if rel.startswith("docs/skill-work/work-strategy/theology-notebook/STATUS.md"):
        replacements.append(
            (
                "../work-civ-mem/",
                "../../work-civ-mem/",
            )
        )

    if rel == "docs/skill-work/work-moonshots/swarm-spirit.md":
        replacements.append(
            (
                "../work-strategy/strategy-notebook/experts/",
                "../../../statecraft/voices/",
            )
        )

    if rel.startswith("statecraft/bridges/"):
        replacements.extend(
            [
                ("../../speakers/marandi/", "../voices/marandi/"),
                ("../../speakers/parsi/", "../voices/parsi/"),
                ("../../voices/marandi/", "../voices/marandi/"),
                ("../../voices/parsi/", "../voices/parsi/"),
                (
                    "arc-marandi-continuity.md",
                    "marandi-arc.md",
                ),
                (
                    "arc-parsi-continuity.md",
                    "parsi-arc.md",
                ),
            ]
        )

    if "theory-cross-case-v1/patterns/" in rel:
        replacements.extend(
            [
                ("../../volumes/", "../../../volumes/"),
                ("../../../../../glossary.md", "../../../glossary.md"),
            ]
        )

    if rel.startswith("statecraft/voices/"):
        replacements.extend(
            [
                (
                    "skills-portable/voice-profile-panel/",
                    "skills/voice-profile-panel/",
                ),
                (
                    "../../strategy-commentator-threads.md",
                    "../../../codex/strategy-commentator-threads.md",
                ),
                ("../ritter-profile.md", "ritter-profile.md"),
                ("../parsi-thread.md", "parsi-thread.md"),
                ("../parsi-transcript.md", "parsi-transcript.md"),
            ]
        )


    if rel.startswith("statecraft/channels/"):
        replacements.append(
            (
                "../../breaking-points/",
                "../breaking-points/",
            )
        )

    if rel.startswith("statecraft/notes/reentry/"):
        replacements.append(
            (
                "../../../compact/",
                "../compact/",
            )
        )

    if rel.startswith("runtime/artifacts/operator-command-deck/"):
        replacements.append(
            (
                "../../../recursion-gate.md",
                "../../../archive/grace-mar-instance/recursion-gate.md",
            )
        )

    if rel.startswith("skills/_drafts/"):
        replacements.append(
            (
                "../../.cursor/skills/coffee/",
                "../../../.cursor/skills/coffee/",
            )
        )

    if rel.startswith("skills/check-sources/") or rel.startswith("skills/monthly-deepening/"):
        replacements.append(
            (
                "../../../.codex-tmp/",
                "../../../../.codex-tmp/",
            )
        )

    for old, new in replacements:
        if old in text:
            n = text.count(old)
            text = text.replace(old, new)
            count += n
    return text, count


CIVMEM_DASH = "\u2013"


def _dashify_civmem_filename(match: re.Match[str]) -> str:
    prefix = match.group(1)
    name = match.group(2)
    if CIVMEM_DASH in name:
        return match.group(0)
    if not (name.startswith("CIV-") or name.startswith("MEM-")):
        return match.group(0)
    return prefix + name.replace("-", CIVMEM_DASH)



def fix_civ_mem_draft_protocol(text: str, file_path: Path) -> tuple[str, int]:
    """Collapse over-deep civ-mem-draft-protocol links under docs/skill-work/."""
    rel = file_path.relative_to(REPO_ROOT).as_posix()
    if not rel.startswith("docs/skill-work/"):
        return text, 0
    target = REPO_ROOT / "docs/skill-work/work-politics/civ-mem-draft-protocol.md"
    if not target.is_file():
        return text, 0
    correct = os.path.relpath(target, file_path.parent.resolve()).replace("\\", "/")
    pattern = r"\]\((?:\.\./)+work-politics/civ-mem-draft-protocol\.md\)"

    def repl(_match: re.Match[str]) -> str:
        return f"]({correct})"

    new_text, n = re.subn(pattern, repl, text)
    return new_text, n


def fix_regex_patterns(text: str, file_path: Path) -> tuple[str, int]:
    rel = file_path.relative_to(REPO_ROOT).as_posix()
    count = 0
    patterns: list[tuple[str, str]] = [
        (r"statecraft/research/bridges/", "statecraft/bridges/"),
        (r"ph-civ/book/", "public/predictive-history/book/"),
        (r"codex/chapters/(\d{4})-(\d{2})/", r"codex/chapters/\1/\1-\2/"),
        (r"codex/chapters/YYYY-MM/", "codex/chapters/2026/2026-04/"),
    ]
    if rel.startswith("statecraft/synthesis/"):
        patterns.append((r"(?:\.\./)+america/transactions/", "../../america/transactions/"))
        patterns.append((r"(?:\.\./)+persia/transactions/", "../../persia/transactions/"))
    if rel.startswith("statecraft/notes/intake/") or rel.startswith("statecraft/notes/reentry/"):
        patterns.append((r"(?:\.\./)+persia/transactions/", "../../persia/transactions/"))
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
    if rel.startswith("statecraft/voices/"):
        parts = rel.split("/")
        if len(parts) >= 3:
            speaker = parts[2]
            patterns.append((r"\]\(transcript\.md\)", rf"]({speaker}-transcript.md)"))
            patterns.append((r"\]\(thread\.md\)", rf"]({speaker}-thread.md)"))
        patterns.append((r"arc-([a-z0-9-]+)-continuity\.md", r"\1-arc.md"))
        patterns.append(
            (
                r"\]\((?:\.\./)+codex/daily-strategy-inbox\.md (?=[^\)])",
                r"](../../../codex/daily-strategy-inbox.md) ",
            )
        )
        patterns.append(
            (
                r"\]\((?:\.\./)+codex/daily-strategy-inbox\.md\(",
                r"](../../../codex/daily-strategy-inbox.md) (",
            )
        )
        patterns.append(
            (r"(?:\.\./)+\.cursor/skills/tri-mind/", "../../../.cursor/skills/tri-mind/")
        )
        patterns.append((r"(?:\.\./)+codex/predictive-history/", "../../../codex/predictive-history/"))
        patterns.append((r"(?:\.\./)+codex/", "../../../codex/"))
    if "source-archive-residue" in rel:
        patterns.append((r"(?:\.\./\.\./\.\./voices/marandi/)+", "../../../voices/marandi/"))
    if rel.startswith("docs/skill-work/work-strategy/history-notebook/"):
        patterns.extend(
            [
                (r"(?:\.\./)+codex/chapters/", "../../../../codex/chapters/"),
                (r"(?:\.\./)+codex/minds/", "../../../../codex/minds/"),
                (r"(?:\.\./)+codex/predictive-history/", "../../../../codex/predictive-history/"),
                (r"(?:\.\./)+codex/STRATEGY-NOTEBOOK-ARCHITECTURE\.md", "../../../../codex/STRATEGY-NOTEBOOK-ARCHITECTURE.md"),
                (r"(?:\.\./)+\\.cursor/rules/", "../../../../.cursor/rules/"),
                (r"(?:\.\./)+research/repos/", "../../../../research/repos/"),
            ]
        )
    if rel.startswith("docs/skill-work/work-strategy/"):
        patterns.append((r"(?:\.\./)+\.cursor/rules/", "../../../.cursor/rules/"))
    if rel.startswith("docs/skill-work/work-coffee/"):
        patterns.append(
            (r"(?:\.\./)+\.cursor/skills/coffee/", "../../../.cursor/skills/coffee/"),
        )
    if "dev-notebook/work-dev" in rel:
        if rel.endswith("dev-notebook/work-dev/journal/README.md"):
            patterns.append(
                (
                    r"\]\((?:\.\./)+journal-metrics-habit\.md\)",
                    r"](../../../../journal-metrics-habit.md)",
                ),
            )
        elif rel.startswith("docs/skill-work/work-dev/dev-notebook/work-dev/"):
            patterns.append(
                (
                    r"\]\((?:\.\./)+journal-metrics-habit\.md\)",
                    r"](../../../journal-metrics-habit.md)",
                ),
            )
    if "pape-page-" in rel or "parsi-page-" in rel:
        patterns.append(
            (
                r"\]\(\.\./daily-strategy-inbox\.md \(",
                r"](../../../codex/daily-strategy-inbox.md) (",
            )
        )
    if rel.startswith("statecraft/voices/"):
        patterns.append(
            (
                r"\]\(daily-brief-([0-9-]+)\.md ([^)]*)",
                r"](../../../../docs/skill-work/work-strategy/daily-brief-\1.md) \2",
            )
        )
        patterns.append(
            (
                r"\]\(\.\./([a-z]+)-profile\.md and ",
                r"](../\1-profile.md) and ",
            )
        )
        patterns.append(
            (
                r"\]\(\.\./(?:profiles/)?([a-z]+)-profile\.md \(",
                r"](\1-profile.md) (",
            )
        )
        patterns.append(
            (
                r"\]\(\.\./([a-z]+)-thread\.md \(",
                r"](\1-thread.md) (",
            )
        )
        patterns.append(
            (
                r"\]\(\.\./([a-z]+)-transcript\.md \(",
                r"](\1-transcript.md) (",
            )
        )
        patterns.append(
            (
                r"\]\((?:\.\./)+codex/minds/(CIV-MIND-[^.]+\.md) \(",
                r"](../../../codex/minds/\1) (",
            )
        )
        patterns.append(
            (
                r"\]\((?:\.\./)+codex/minds/(CIV-MIND-[^.]+\.md) ",
                r"](../../../codex/minds/\1) ",
            )
        )
        patterns.append(
            (
                r"\]\(strategy-state-iran/voices/",
                r"](../../../../codex/strategy-state-iran/voices/",
            )
        )
    if rel.startswith("statecraft/voices/davis/"):
        patterns.append((r"\]\(\.\./davis-", r"](davis-"))
    if rel.startswith("docs/skill-work/work-strategy/minds/"):
        patterns.append(
            (
                r"\]\(\.\./\.\./\.\./\.cursor/rules/",
                r"](../../../../.cursor/rules/",
            )
        )
    if rel.startswith("skills/") and not rel.startswith("skills/runbooks/"):
        patterns.append(
            (r"\]\(\.\./\.\./\.\./\.cursor/rules/", r"](../../.cursor/rules/"),
        )
        patterns.append(
            (r"\]\(\.\./\.\./\.\./\.cursor/skills/", r"](../../.cursor/skills/"),
        )
    if rel.startswith("statecraft/voices/davis/"):
        patterns.append((r"\]\(assets/davis/[^)]+\.png\)", r"](davis-profile.md)"))
    if rel.startswith("statecraft/voices/mercouris/"):
        patterns.append((r"\]\(assets/marandi/[^)]+\.png\)", r"](../marandi/marandi-profile.md)"))
    if rel.startswith(".cursor/skills/statecraft-framework/"):
        patterns.append(
            (
                r"\]\(\.\./\.\./\.\./statecraft/states/theory/form\.md\)",
                r"](../../../../public/civ-state/theory/memory.md)",
            )
        )
        patterns.append(
            (r"\]\(\.\./\.\./\.\./statecraft/", r"](../../../../statecraft/"),
        )
    if rel.startswith(".cursor/skills/strategy-notebook-expert-cross-weave/"):
        patterns.append(
            (
                r"\]\(\.\./\.\./\.\./codex/chapters/2026-04/meta\.md\)",
                r"](../../../../codex/chapters/2026/2026-04/meta.md)",
            )
        )
    if rel.startswith(".cursor/skills/skill-write/"):
        patterns.append(
            (
                r"\]\(\.\./\.\./\.\./codex/experts/barnes/mind\.md\)",
                r"](../../../statecraft/voices/barnes/barnes-mind.md)",
            )
        )
    if rel.startswith("skills/") and not rel.startswith("skills/runbooks/"):
        patterns.append(
            (r"\]\(\.\./\.\./\.\./\.cursor/rules/", r"](../../.cursor/rules/"),
        )
    if rel.startswith(".cursor/skills/"):
        patterns.append((r"\]\(\.\./\.\./\.\./\.\./codex/", r"](../../../codex/"))
        patterns.append(
            (
                r"statecraft/synthesis/day/_templates/week-hinge-start-here\.md",
                "statecraft/notes/reentry/_templates/week-hinge-start-here.md",
            )
        )
        patterns.append((r"(?:\.\./)+\.codex-tmp/", "../../../.codex-tmp/"))
        patterns.append((r"(?:\.\./)+\.cursor/rules/", "../../../.cursor/rules/"))
    elif rel.startswith("skills/"):
        patterns.append((r"\]\(\.\./\.\./\.\./\.\./codex/", r"](../../codex/"))
        patterns.append(
            (
                r"statecraft/synthesis/day/_templates/week-hinge-start-here\.md",
                "statecraft/notes/reentry/_templates/week-hinge-start-here.md",
            )
        )
        patterns.append((r"(?:\.\./)+codex/academy/", "../../codex/academy/"))
        patterns.append((r"(?:\.\./)+\.codex-tmp/", "../../../.codex-tmp/"))
        patterns.append((r"(?:\.\./)+\.cursor/rules/", "../../../.cursor/rules/"))
    if rel.startswith("skills/runbooks/"):
        patterns.append((r"\.\./\.\./\.\./\.cursor/rules/", "../../.cursor/rules/"))
    patterns.append((r"skills-portable/voice-profile-panel/", "skills/voice-profile-panel/"))
    patterns.append((r"(?:\.\./)+speakers/", "../../voices/"))
    patterns.append(
        (
            r"(?:\.\./)+codex/years/2025/provenance/([0-9-]+)/",
            r"../../../source-archive/statecraft/\1/",
        )
    )
    if rel.startswith("statecraft/voices/mercouris/"):
        patterns.append(
            (
                r"\]\(provenance/([0-9-]+)/([^)]+)\)",
                r"](../../../source-archive/statecraft/\1/\2)",
            )
        )
    if rel == "docs/state-model.md":
        patterns.append(
            (
                r"\]\((?:\.\./)+integrations/",
                r"](integrations/",
            )
        )

    if rel.startswith("statecraft/states/volumes/"):
        new_text, n = re.subn(
            r"(research/repos/civilization_memory/[^)\s]*?)([A-Z0-9]+(?:-[A-Z0-9]+)+\.md)",
            _dashify_civmem_filename,
            text,
        )
        if n:
            text = new_text
            count += n
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
    """Fix wrong-depth .cursor/skills and .cursor/rules links."""
    rel = file_path.relative_to(REPO_ROOT).as_posix()
    if not (
        rel.startswith("docs/")
        or rel.startswith("skills/")
        or rel.startswith("statecraft/")
        or rel.startswith(".cursor/skills/")
    ):
        return text, 0
    count = 0

    for sub in ("skills", "rules"):
        root = REPO_ROOT / ".cursor" / sub
        if not root.is_dir():
            continue

        def repl(match: re.Match[str], *, sub: str = sub, root: Path = root) -> str:
            nonlocal count
            tail = match.group(1)
            target = root / tail
            if not target.is_file():
                return match.group(0)
            correct = os.path.relpath(target, file_path.parent.resolve()).replace("\\", "/")
            inner = match.group(0)[2:-1]
            if correct == inner:
                return match.group(0)
            count += 1
            return f"]({correct})"

        text = re.sub(
            rf"\]\((?:\.\./)+\.cursor/{sub}/([^)]+)\)",
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

    text, n = fix_template_routing_prose(text, path)
    total += n

    text, n = fix_bulk_text_patterns(text, path)
    total += n

    text, n = fix_civ_mem_draft_protocol(text, path)
    total += n

    text, n = fix_source_archive_master_index(text, path)
    total += n

    text, n = fix_regex_patterns(text, path)
    total += n

    text, n = fix_cursor_skills_depth(text, path)
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
