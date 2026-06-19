#!/usr/bin/env python3
"""
Shared I/O and path helpers for strategy-codex scripts.

The repository now uses a sole-operator layout: canonical Record surfaces live
at the repository root. This module remains the single place for REPO_ROOT and
the canonical path helpers used by scripts and docs.
"""

import json
import os
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PROFILE_ID = (os.getenv("GRACE_MAR_USER_ID", "strategy-codex").strip() or "strategy-codex")
# Back-compat alias for scripts that still import the older constant name.
DEFAULT_USER_ID = DEFAULT_PROFILE_ID

# Authoritative on-disk names live at the repository root. Docs may say SELF/EVIDENCE
# as concepts; filenames are always these. See docs/canonical-paths.md.
CANONICAL_EVIDENCE_BASENAME = "self-archive.md"
CANONICAL_RECORD_FILES_REQUIRED: tuple[str, ...] = (
    "self.md",
    "self-knowledge.md",
    CANONICAL_EVIDENCE_BASENAME,
    "recursion-gate.md",
)

# Operator append-only ledgers (moved from repo root — see docs/root-directory-map.md).
OPERATOR_EVENTS_DIR = REPO_ROOT / "runtime" / "operator-events"
OPERATOR_LEDGER_FILES: tuple[str, ...] = (
    "pipeline-events.jsonl",
    "merge-receipts.jsonl",
    "cadence-learning-events.jsonl",
    "business-ledger.jsonl",
    "fork-lineage.jsonl",
    "strategy-fold-events.jsonl",
)
LAST_DREAM_BASENAME = "last-dream.json"

TARGET_ROOT_FOLDERS: frozenset[str] = frozenset(
    {
        ".cursor",
        ".github",
        "SELF-LIBRARY",
        "archive",
        "codex",
        "docs",
        "essays",
        "examples",
        "platform",
        "public",
        "research",
        "runtime",
        "schemas",
        "scripts",
        "singularity",
        "skills",
        "source-archive",
        "statecraft",
        "templates",
        "tests",
    }
)

REPO_PATH_MIGRATIONS: dict[str, tuple[str, ...]] = {
    "artifacts": ("runtime/artifacts", "artifacts"),
    "daily-handoff": ("runtime/daily-handoff", "daily-handoff"),
    "prepared-context": ("runtime/prepared-context", "prepared-context"),
    "runtime-bundle": ("runtime/bundle", "runtime-bundle"),
    "evidence": ("archive/placeholders/evidence", "evidence"),
    "reflection-proposals": ("archive/queues/reflection-proposals", "reflection-proposals"),
    "review-queue": ("archive/queues/review-queue", "review-queue"),
    "apps": ("platform/apps", "apps"),
    "app": ("platform/app", "app"),
    "src": ("platform/src", "src"),
    "bin": ("platform/bin", "bin"),
    "deployment": ("platform/deployment", "deployment"),
    "config": ("platform/config", "config"),
    "extension": ("platform/extension", "extension"),
    "integrations": ("platform/integrations", "integrations"),
    "miniapp": ("platform/miniapp", "miniapp"),
    "users": ("platform/users", "users"),
    "template": ("platform/template", "_template"),
    "profile": ("platform/profile", "profile"),
    "auto-research": ("research/auto-research", "auto-research"),
    "bridges": ("research/bridges", "bridges"),
    "skills-portable": ("skills", "skills-portable"),
    "skills": ("skills", "skills-portable"),
    "schema-registry": ("schemas/registry", "schema-registry"),
    "styles": ("templates/styles", "styles"),
    "bot": ("archive/grace-mar-instance/bot", "bot"),
    "recursion-gate-staging": (
        "archive/grace-mar-instance/recursion-gate-staging",
        "recursion-gate-staging",
    ),
    "bootstrap": ("archive/grace-mar-instance/bootstrap", "bootstrap"),
    "grace-mar-instance": ("archive/grace-mar-instance",),
}

GRACE_MAR_INSTANCE_DIR = REPO_ROOT / "archive" / "grace-mar-instance"


def resolve_repo_path(logical_key: str, *, prefer_existing: bool = True) -> Path:
    """Resolve consolidated repo path by logical key (canonical + legacy fallback)."""
    entry = REPO_PATH_MIGRATIONS.get(logical_key)
    if entry is None:
        raise ValueError(f"unknown repo path key: {logical_key!r}")
    canonical = REPO_ROOT / entry[0]
    if not prefer_existing:
        return canonical
    if canonical.exists():
        return canonical
    for legacy_rel in entry[1:]:
        legacy = REPO_ROOT / legacy_rel
        if legacy.exists():
            return legacy
    return canonical


DEFAULT_USERS_DIR = resolve_repo_path("users")

# Canonical consolidated directories (prefer imports over string paths in scripts).
ARTIFACTS_DIR = resolve_repo_path("artifacts")
PREPARED_CONTEXT_DIR = resolve_repo_path("prepared-context")
RUNTIME_BUNDLE_DIR = resolve_repo_path("runtime-bundle")
SRC_DIR = resolve_repo_path("src")
SKILLS_DIR = resolve_repo_path("skills")
APPS_DIR = resolve_repo_path("apps")
BOT_DIR = resolve_repo_path("bot")
SCHEMA_REGISTRY_DIR = resolve_repo_path("schema-registry")
AUTO_RESEARCH_DIR = resolve_repo_path("auto-research")
REVIEW_QUEUE_DIR = resolve_repo_path("review-queue")


def user_profile_dir(user_id: str) -> Path:
    """Per-fork profile directory under platform/users/."""
    return resolve_repo_path("users") / user_id.strip()


def artifacts_dir(base: Path | None = None) -> Path:
    """
    Return artifacts directory for repo root, Grace-Mar profile root, or users/<id>.

    Sole-operator profile (archive/grace-mar-instance) maps to repo-level ARTIFACTS_DIR.
    """
    if base is None:
        return ARTIFACTS_DIR
    root = base.resolve()
    if root == REPO_ROOT.resolve():
        return ARTIFACTS_DIR
    if (GRACE_MAR_INSTANCE_DIR / "self.md").is_file() and root == GRACE_MAR_INSTANCE_DIR.resolve():
        return ARTIFACTS_DIR
    nested = root / "runtime" / "artifacts"
    legacy = root / "artifacts"
    if legacy.is_dir() and not nested.is_dir():
        return legacy
    return nested


def src_dir(base: Path | None = None) -> Path:
    """Return platform/src for repo root or a nested checkout base."""
    if base is None:
        return SRC_DIR
    root = base.resolve()
    if root == REPO_ROOT.resolve():
        return SRC_DIR
    nested = root / "platform" / "src"
    legacy = root / "src"
    if legacy.is_dir() and not nested.is_dir():
        return legacy
    return nested


def read_path(path: Path) -> str:
    """Read path as utf-8; return '' if missing."""
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def profile_dir(user_id: str) -> Path:
    """Return canonical profile directory (Grace-Mar instance bundle when relocated)."""
    if (GRACE_MAR_INSTANCE_DIR / "self.md").is_file():
        return GRACE_MAR_INSTANCE_DIR
    if (REPO_ROOT / "self.md").is_file():
        return REPO_ROOT
    if GRACE_MAR_INSTANCE_DIR.is_dir():
        return GRACE_MAR_INSTANCE_DIR
    return REPO_ROOT


def dream_handoff_root(users_dir: Path, user_id: str) -> Path:
    """Filesystem root for dream handoff JSON (sole-operator root vs platform/users/<id>)."""
    if users_dir.resolve() == DEFAULT_USERS_DIR.resolve():
        return profile_dir(user_id)
    candidate = users_dir / user_id
    if candidate.is_dir() or (candidate / "self.md").is_file():
        return candidate
    return profile_dir(user_id)


def operator_ledger_write_path(user_id: str, name: str) -> Path:
    """Canonical append/write path for operator event ledgers."""
    OPERATOR_EVENTS_DIR.mkdir(parents=True, exist_ok=True)
    return OPERATOR_EVENTS_DIR / name


def resolve_ledger_path(user_id: str, name: str) -> Path:
    """
    Resolve operator ledger path for read or open-for-append.

    Prefers runtime/operator-events/; falls back to repository root for compat.
    """
    new = OPERATOR_EVENTS_DIR / name
    old = profile_dir(user_id) / name
    if new.is_file():
        return new
    if old.is_file():
        return old
    return operator_ledger_write_path(user_id, name)


def resolve_last_dream_path(user_id: str, users_dir: Path | None = None) -> Path:
    """Read path for last-dream.json (runtime/daily-handoff/ preferred; legacy compat)."""
    handoff_dir = resolve_repo_path("daily-handoff")
    new = handoff_dir / LAST_DREAM_BASENAME
    root = dream_handoff_root(users_dir or DEFAULT_USERS_DIR, user_id)
    old = root / "runtime/daily-handoff" / LAST_DREAM_BASENAME
    legacy_root = root / LAST_DREAM_BASENAME
    if new.is_file():
        return new
    if old.is_file():
        return old
    if legacy_root.is_file():
        return legacy_root
    return new


def last_dream_write_path(user_id: str, users_dir: Path | None = None) -> Path:
    """Canonical write path for last-dream.json."""
    handoff_dir = resolve_repo_path("daily-handoff")
    path = handoff_dir / LAST_DREAM_BASENAME
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def fork_root(fork_id: str) -> Path:
    """Alias for profile_dir: the filesystem root for the sole operator profile."""
    return profile_dir(fork_id)


def list_forks() -> list[str]:
    """
    Return the sole operator profile identifier when the canonical root files exist.
    """
    root = profile_dir(DEFAULT_PROFILE_ID)
    if (root / "self.md").exists() or (root / "recursion-gate.md").exists():
        return [DEFAULT_PROFILE_ID]
    return []


def fork_config_path(fork_id: str) -> Path:
    """Path to optional profile config (JSON)."""
    return REPO_ROOT / "fork-config.json"


def missing_canonical_record_files(user_id: str) -> list[str]:
    """
    Return basenames missing under the repository root. Empty list if all required exist.
    """
    root = profile_dir(user_id)
    return [name for name in CANONICAL_RECORD_FILES_REQUIRED if not (root / name).is_file()]


def resolve_surface_markdown_path(
    user_dir: Path,
    canonical_key: str,
    *,
    prefer_existing: bool = True,
) -> Path:
    """
    Resolve the Path for a Record surface markdown file under user_dir.

    Conflict rule (self_skills and similar): if both the canonical file
    (e.g. self-skills.md) and a legacy file (e.g. skills.md) exist, the
    canonical path wins — prefer_existing returns the canonical file when it
    is present.

    self_evidence: canonical body is self-archive.md. If it is missing but
    self-evidence.md exists (optional pointer / compat), returns
    self-evidence.md for read scenarios when prefer_existing is True; if
    neither exists, returns self-archive.md as the intended canonical target.

    Raises:
        ValueError: unknown canonical_key or logical-only surface (e.g. self_knowledge).
    """
    from surface_aliases import get_surface_by_key

    surface = get_surface_by_key(canonical_key)
    if surface is None:
        raise ValueError(f"unknown surface key: {canonical_key!r}")
    if surface.canonical_file_stem is None:
        raise ValueError(f"surface {surface.canonical_key!r} has no on-disk markdown file")

    canon = user_dir / f"{surface.canonical_file_stem}.md"

    if surface.canonical_key == "self_archive/placeholders/evidence":
        if prefer_existing:
            if canon.is_file():
                return canon
            fe = user_dir / "self-evidence.md"
            if fe.is_file():
                return fe
        return canon

    if not prefer_existing:
        return canon

    if canon.is_file():
        return canon
    for leg in surface.legacy_file_stems:
        p = user_dir / f"{leg}.md"
        if p.is_file():
            return p
    return canon


def resolve_self_memory_path(user_dir: Path) -> Path:
    """
    Canonical continuity file: self-memory.md. Legacy memory.md is still read if present
    and self-memory.md is absent (same pattern as skills.md → self-skills.md).
    """
    return resolve_surface_markdown_path(user_dir, "self_memory", prefer_existing=True)


def read_surface_markdown(user_dir: Path, canonical_key: str) -> str:
    """Read UTF-8 content for a surface; empty string if resolved path missing."""
    try:
        path = resolve_surface_markdown_path(user_dir, canonical_key, prefer_existing=True)
    except ValueError:
        return ""
    return read_path(path)


def self_skills_layout_warnings(user_dir: Path) -> list[str]:
    """
    Phase A (advisory): warn on legacy skills.md or duplicate capability index files.

    Canonical capability index: self-skills.md. See docs/canonical-paths.md.
    """
    if not user_dir.is_dir():
        return []
    legacy = user_dir / "skills.md"
    canon = user_dir / "self-skills.md"
    out: list[str] = []
    if legacy.is_file() and canon.is_file():
        out.append(
            "repository root: both skills.md and self-skills.md exist; readers prefer self-skills.md. "
            "Remove skills.md after confirming content is merged."
        )
    elif legacy.is_file() and not canon.is_file():
        out.append(
            "repository root: legacy skills.md present; rename to self-skills.md "
            "(e.g. python scripts/migrate_legacy_user_filenames.py --apply)."
        )
    return out


def enforce_canonical_self_skills_layout(user_dir: Path) -> None:
    """
    Phase B: when GRACE_MAR_REQUIRE_CANONICAL_SELF_SKILLS=1, fail if only legacy
    skills.md exists (canonical self-skills.md required when a capability index file is present).
    """
    if os.environ.get("GRACE_MAR_REQUIRE_CANONICAL_SELF_SKILLS", "").strip() != "1":
        return
    if not user_dir.is_dir():
        return
    legacy = user_dir / "skills.md"
    canon = user_dir / "self-skills.md"
    if legacy.is_file() and not canon.is_file():
        raise RuntimeError(
            "strategy-codex: GRACE_MAR_REQUIRE_CANONICAL_SELF_SKILLS=1 but the repository root "
            "has skills.md without self-skills.md. Migrate: "
            "python scripts/migrate_legacy_user_filenames.py --apply"
        )


def assert_canonical_record_layout(user_id: str, *, context: str = "") -> None:
    """
    Fail loudly if required Record files are missing. Set GRACE_MAR_SKIP_PATH_CHECK=1 to skip.

    Raises:
        RuntimeError: missing files or missing user directory
    """
    if os.environ.get("GRACE_MAR_SKIP_PATH_CHECK", "").strip() == "1":
        return
    missing = missing_canonical_record_files(user_id)
    if missing:
        ctx = f" ({context})" if context else ""
        fix = "See docs/canonical-paths.md. If you have legacy uppercase filenames, migrate them to the root-level canonical names."
        raise RuntimeError(
            f"strategy-codex: canonical Record files missing at the repository root: {missing}.{ctx}\n{fix}"
        )
    enforce_canonical_self_skills_layout(profile_dir(user_id))


def load_fork_config(fork_id: str) -> dict[str, Any] | None:
    """
    Load optional profile config from the repository root.
    Returns None if file missing or invalid.
    """
    path = fork_config_path(fork_id)
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
