#!/usr/bin/env python3
"""
Shared I/O and path helpers for strategy-codex scripts.

Canonical Record surfaces live under `archive/grace-mar-instance/` when relocated.
This module is the single place for REPO_ROOT and path helpers used by scripts and docs.
"""

import json
import os
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterator

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PROFILE_ID = (os.getenv("GRACE_MAR_USER_ID", "strategy-codex").strip() or "strategy-codex")
# Back-compat alias for scripts that still import the older constant name.
DEFAULT_USER_ID = DEFAULT_PROFILE_ID

# Authoritative on-disk names under the profile bundle (see docs/canonical-paths.md).
CANONICAL_EVIDENCE_BASENAME = "self-archive.md"
CANONICAL_RECORD_FILES_REQUIRED: tuple[str, ...] = (
    "self.md",
    "self-knowledge.md",
    CANONICAL_EVIDENCE_BASENAME,
    "recursion-gate.md",
)

# Sprint 4 classification for REPO_PATH_MIGRATIONS retirement (see docs/complexity-budget.md).
REPO_PATH_CLASSIFICATION: dict[str, str] = {
    "artifacts": "active_canonical",
    "daily-handoff": "active_canonical",
    "prepared-context": "active_canonical",
    "runtime-bundle": "active_canonical",
    "src": "active_canonical",
    "skills": "active_canonical",
    "skills-portable": "active_canonical",
    "apps": "active_canonical",
    "app": "active_canonical",
    "bin": "active_canonical",
    "deployment": "active_canonical",
    "config": "active_canonical",
    "extension": "active_canonical",
    "integrations": "active_canonical",
    "miniapp": "active_canonical",
    "users": "active_canonical",
    "template": "active_canonical",
    "profile": "active_canonical",
    "auto-research": "active_canonical",
    "bridges": "active_canonical",
    "schema-registry": "active_canonical",
    "styles": "active_canonical",
    "evidence": "archive_placeholder",
    "reflection-proposals": "archive_placeholder",
    "review-queue": "archive_placeholder",
    "bot": "grace_mar_compat",
    "recursion-gate-staging": "grace_mar_compat",
    "bootstrap": "grace_mar_compat",
    "grace-mar-instance": "grace_mar_compat",
    "codex": "active_canonical",
}

_LEGACY_PATH_WARNED: set[str] = set()
_LEGACY_PATH_RESOLVE_COUNT: Counter[str] = Counter()

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
NIGHT_HANDOFF_BASENAME = "night-handoff.json"

TARGET_ROOT_FOLDERS: frozenset[str] = frozenset(
    {
        ".cursor",
        ".github",
        "library",
        "archive",
        "continuity",
        "docs",
        "education",
        "essays",
        "examples",
        "operations",
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
    "artifacts": ("runtime/artifacts",),
    "daily-handoff": ("runtime/daily-handoff",),
    "prepared-context": ("runtime/prepared-context",),
    "runtime-bundle": ("runtime/bundle",),
    "evidence": ("archive/placeholders/evidence",),
    "reflection-proposals": ("archive/queues/reflection-proposals",),
    "review-queue": ("archive/queues/review-queue",),
    "apps": ("platform/apps",),
    "app": ("platform/app",),
    "src": ("platform/src",),
    "bin": ("platform/bin",),
    "deployment": ("platform/deployment",),
    "config": ("platform/config",),
    "extension": ("platform/extension",),
    "integrations": ("platform/integrations",),
    "miniapp": ("platform/miniapp",),
    "users": ("platform/users",),
    "template": ("platform/template",),
    "profile": ("platform/profile",),
    "auto-research": ("research/auto-research",),
    "bridges": ("research/bridges",),
    "skills-portable": ("skills",),
    "skills": ("skills",),
    "schema-registry": ("schemas/registry",),
    "styles": ("templates/styles",),
    "bot": ("archive/grace-mar-instance/bot",),
    "recursion-gate-staging": ("archive/grace-mar-instance/recursion-gate-staging",),
    "bootstrap": ("archive/grace-mar-instance/bootstrap",),
    "grace-mar-instance": ("archive/grace-mar-instance",),
    "codex": ("continuity", "codex"),
    "singularity/business/grace-gems": ("operations/grace-gems",),
    "singularity/business/mountain-homestead": ("operations/mountain-homestead",),
}

GRACE_MAR_INSTANCE_DIR = REPO_ROOT / "archive" / "grace-mar-instance"

def strict_paths_enabled() -> bool:
    return os.environ.get("STRATEGY_CODEX_STRICT_PATHS", "").strip() == "1"

def legacy_path_resolve_count() -> dict[str, int]:
    """Return per-key counts of legacy fallback resolutions this process."""
    return dict(_LEGACY_PATH_RESOLVE_COUNT)

def reset_legacy_path_resolve_count() -> None:
    _LEGACY_PATH_RESOLVE_COUNT.clear()
    _LEGACY_PATH_WARNED.clear()

def scan_legacy_path_layout() -> list[str]:
    """
    Report legacy or dual-layout path keys without mutating resolver state.

    Used by check_repo_path_strict.py and complexity audit.
    """
    issues: list[str] = []
    for key, entry in REPO_PATH_MIGRATIONS.items():
        if len(entry) < 2:
            continue
        canonical = REPO_ROOT / entry[0]
        legacy_hits = [rel for rel in entry[1:] if (REPO_ROOT / rel).exists()]
        if not legacy_hits:
            continue
        if canonical.exists():
            for rel in legacy_hits:
                issues.append(f"{key}: dual layout ({entry[0]} + {rel})")
        else:
            for rel in legacy_hits:
                issues.append(f"{key}: legacy-only ({rel}; canonical {entry[0]} missing)")
    return issues

PATH_FALLBACK_RETIREMENT_PATH = REPO_ROOT / "path-fallback-retirement.yaml"
GRACE_MAR_COMPAT_KEYS = frozenset(
    {"bot", "recursion-gate-staging", "bootstrap", "grace-mar-instance"}
)
RETIREMENT_CATEGORIES = frozenset(
    {"active_canonical", "archive_placeholder", "grace_mar_compat"}
)
RETIREMENT_STATUSES = frozenset(
    {
        "remove_when_clean",
        "keep_temporarily",
        "move_to_grace_mar_compat",
        "keep_no_legacy",
    }
)
WAVE_READINESS_STATUSES = frozenset(
    {
        "ready",
        "ready_docs_only_refs",
        "blocked_missing_canonical",
        "blocked_active_refs",
        "not_checked",
    }
)
_WAVE_SCAN_EXTENSIONS = frozenset({".py", ".sh", ".yaml", ".yml", ".json", ".toml"})
_WAVE_SCAN_ROOTS = ("scripts", "tests", "platform", ".github")
_WAVE_SCAN_EXCLUDE_FILES = frozenset(
    {
        "path-fallback-retirement.yaml",
        "docs/path-fallback-retirement.md",
        "docs/complexity-budget.md",
        "scripts/repo_io.py",
        "scripts/migrate_root_layout.py",
        "scripts/check_repo_path_strict.py",
    }
)
_WAVE_SCAN_EXCLUDE_DIR_PREFIXES = (
    ".git/",
    "runtime/artifacts/complexity-audit/",
    "archive/grace-mar-instance/",
    "archive/grace-mar-corpus/",
)

def validate_repo_path_classification() -> list[str]:
    """Ensure REPO_PATH_CLASSIFICATION bijects with REPO_PATH_MIGRATIONS keys."""
    migration_keys = set(REPO_PATH_MIGRATIONS)
    classification_keys = set(REPO_PATH_CLASSIFICATION)
    issues: list[str] = []
    for key in sorted(migration_keys - classification_keys):
        issues.append(f"missing classification for repo path key: {key}")
    for key in sorted(classification_keys - migration_keys):
        issues.append(f"classification without migration key: {key}")
    return issues

def load_path_fallback_retirement() -> dict[str, Any]:
    """Load path-fallback-retirement.yaml entries keyed by logical path key."""
    if not PATH_FALLBACK_RETIREMENT_PATH.is_file():
        raise FileNotFoundError(
            f"missing retirement policy: {PATH_FALLBACK_RETIREMENT_PATH.relative_to(REPO_ROOT)}"
        )
    try:
        import yaml
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("PyYAML required for path fallback retirement") from exc
    raw = yaml.safe_load(PATH_FALLBACK_RETIREMENT_PATH.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("path-fallback-retirement.yaml must be a mapping")
    entries = raw.get("entries")
    if not isinstance(entries, list):
        raise ValueError("path-fallback-retirement.yaml must define entries list")
    by_key: dict[str, Any] = {}
    for item in entries:
        if not isinstance(item, dict):
            raise ValueError("each retirement entry must be a mapping")
        key = str(item.get("key") or "").strip()
        if not key:
            raise ValueError("retirement entry missing key")
        if key in by_key:
            raise ValueError(f"duplicate retirement entry key: {key}")
        by_key[key] = item
    return by_key

def validate_path_fallback_retirement() -> list[str]:
    """Validate retirement YAML against migrations and classification."""
    issues: list[str] = []
    try:
        by_key = load_path_fallback_retirement()
    except (OSError, ValueError, RuntimeError) as exc:
        return [str(exc)]

    migration_keys = set(REPO_PATH_MIGRATIONS)
    retirement_keys = set(by_key)

    for key in sorted(migration_keys - retirement_keys):
        issues.append(f"missing retirement policy for repo path key: {key}")
    for key in sorted(retirement_keys - migration_keys):
        issues.append(f"retirement policy without migration key: {key}")

    for key, entry in sorted(by_key.items()):
        if key not in REPO_PATH_MIGRATIONS:
            continue
        category = str(entry.get("category") or "")
        if category not in RETIREMENT_CATEGORIES:
            issues.append(f"{key}: invalid retirement category: {category}")
        elif category != REPO_PATH_CLASSIFICATION.get(key):
            issues.append(
                f"{key}: retirement category {category} != "
                f"classification {REPO_PATH_CLASSIFICATION.get(key)}"
            )
        status = str(entry.get("retirement_status") or "")
        if status not in RETIREMENT_STATUSES:
            issues.append(f"{key}: invalid retirement_status: {status}")
        canonical = str(entry.get("canonical") or "").replace("\\", "/")
        legacy_raw = entry.get("legacy") or []
        if not isinstance(legacy_raw, list):
            issues.append(f"{key}: legacy must be a list")
            continue
        legacy = [str(p).replace("\\", "/") for p in legacy_raw]
        expected = REPO_PATH_MIGRATIONS[key]
        if canonical != expected[0]:
            issues.append(
                f"{key}: retirement canonical {canonical!r} != migration {expected[0]!r}"
            )
        if tuple(legacy) != tuple(expected[1:]):
            issues.append(
                f"{key}: retirement legacy {legacy!r} != migration {list(expected[1:])!r}"
            )
        if category == "grace_mar_compat" and key not in GRACE_MAR_COMPAT_KEYS:
            issues.append(f"{key}: grace_mar_compat category on unexpected key")
        if category != "grace_mar_compat" and key in GRACE_MAR_COMPAT_KEYS:
            issues.append(f"{key}: expected grace_mar_compat category")
        readiness = entry.get("readiness")
        if readiness is not None:
            readiness_s = str(readiness).strip()
            if readiness_s not in WAVE_READINESS_STATUSES:
                issues.append(f"{key}: invalid readiness: {readiness_s!r}")

    for key, category in REPO_PATH_CLASSIFICATION.items():
        if category == "grace_mar_compat" and key not in GRACE_MAR_COMPAT_KEYS:
            issues.append(f"{key}: grace_mar_compat classification outside compat set")

    return issues

def keys_for_wave(wave: int) -> frozenset[str]:
    """Load wave N keys from path-fallback-retirement.yaml."""
    by_key = load_path_fallback_retirement()
    return frozenset(k for k, entry in by_key.items() if entry.get("wave") == wave)

def _wave_scan_rel_path(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()

def _wave_scan_is_excluded(rel_posix: str) -> bool:
    if rel_posix in _WAVE_SCAN_EXCLUDE_FILES:
        return True
    return any(rel_posix.startswith(prefix) for prefix in _WAVE_SCAN_EXCLUDE_DIR_PREFIXES)

def _iter_wave_scan_files() -> Iterator[Path]:
    for root_name in _WAVE_SCAN_ROOTS:
        root = REPO_ROOT / root_name
        if not root.is_dir():
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix.lower() not in _WAVE_SCAN_EXTENSIONS:
                continue
            rel = _wave_scan_rel_path(path)
            if _wave_scan_is_excluded(rel):
                continue
            yield path

def _legacy_active_ref_patterns(legacy: str) -> list[re.Pattern[str]]:
    escaped = re.escape(legacy)
    return [
        re.compile(rf'REPO_ROOT\s*/\s*["\']({escaped})["\']'),
        re.compile(rf'Path\(["\']({escaped})["\']\)'),
    ]

def _line_has_platform_prefix(line: str, legacy: str) -> bool:
    return f"platform/{legacy}" in line or f'platform\\{legacy}' in line

def _line_has_canonical_path_prefix(line: str, canonical_rel: str) -> bool:
    if not canonical_rel:
        return False
    return canonical_rel in line or canonical_rel.replace("/", "\\") in line

def _scan_active_legacy_refs(legacy: str, *, canonical_rel: str = "") -> list[dict[str, Any]]:
    """Find hardcoded repo-root legacy path references in active code."""
    refs: list[dict[str, Any]] = []
    patterns = _legacy_active_ref_patterns(legacy)
    for path in _iter_wave_scan_files():
        rel = _wave_scan_rel_path(path)
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        for line_no, line in enumerate(text.splitlines(), start=1):
            if _line_has_platform_prefix(line, legacy):
                continue
            if _line_has_canonical_path_prefix(line, canonical_rel):
                continue
            for pattern in patterns:
                if pattern.search(line):
                    refs.append(
                        {
                            "path": rel,
                            "line": line_no,
                            "pattern": pattern.pattern,
                            "text": line.strip(),
                        }
                    )
                    break
    return refs

def _derive_wave_key_status(
    *,
    canonical_exists: bool,
    active_refs: list[dict[str, Any]],
) -> str:
    if not canonical_exists:
        return "blocked_missing_canonical"
    if active_refs:
        return "blocked_active_refs"
    return "ready"

def collect_wave_readiness_report(wave: int) -> dict[str, Any]:
    """Audit fallback removal readiness for a retirement wave."""
    wave_keys = keys_for_wave(wave)
    key_reports: dict[str, Any] = {}
    summary: Counter[str] = Counter()

    for key in sorted(wave_keys):
        entry = REPO_PATH_MIGRATIONS.get(key)
        if entry is None:
            raise ValueError(f"wave {wave} key missing from REPO_PATH_MIGRATIONS: {key!r}")
        canonical_rel = entry[0]
        legacy_rels = list(entry[1:])
        canonical = REPO_ROOT / canonical_rel
        canonical_exists = canonical.exists()
        legacy_exists = any((REPO_ROOT / rel).exists() for rel in legacy_rels)
        active_refs: list[dict[str, Any]] = []
        for legacy in legacy_rels:
            active_refs.extend(_scan_active_legacy_refs(legacy, canonical_rel=canonical_rel))
        status = _derive_wave_key_status(
            canonical_exists=canonical_exists,
            active_refs=active_refs,
        )
        key_reports[key] = {
            "canonical": canonical_rel,
            "legacy": legacy_rels,
            "canonical_exists": canonical_exists,
            "legacy_exists": legacy_exists,
            "active_refs": active_refs,
            "status": status,
        }
        summary[status] += 1

    return {
        "wave": wave,
        "keys": key_reports,
        "summary": dict(summary),
    }

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
            if strict_paths_enabled():
                raise RuntimeError(
                    "strategy-codex: STRATEGY_CODEX_STRICT_PATHS=1 but legacy path resolved for "
                    f"{logical_key!r}: {legacy_rel} (canonical: {entry[0]})"
                )
            _LEGACY_PATH_RESOLVE_COUNT[logical_key] += 1
            if logical_key not in _LEGACY_PATH_WARNED:
                _LEGACY_PATH_WARNED.add(logical_key)
                print(
                    f"repo-path: legacy fallback for {logical_key!r}: {legacy_rel} "
                    f"(canonical {entry[0]} missing)",
                    file=sys.stderr,
                )
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
SCHEMA_REGISTRY_DIR = resolve_repo_path("schema-registry")
AUTO_RESEARCH_DIR = resolve_repo_path("auto-research")
REVIEW_QUEUE_DIR = resolve_repo_path("review-queue")
CONTINUITY_DIR = resolve_repo_path("codex")

def continuity_dir() -> Path:
    """Canonical continuity-layer root (continuity/ with continuity/ fallback)."""
    return CONTINUITY_DIR

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

PROFILE_DERIVED_EXPORTS: tuple[str, ...] = (
    "manifest.json",
    "llms.txt",
    "intent_snapshot.json",
    "fork-manifest.json",
    "session-transcript.md",
    "gate-dashboard.html",
    "telegram_bot_username.txt",
    "evidence-graph.json",
    "symbolic_identity.json",
    "self-work.md",
)

def derived_export_dir(user_id: str) -> Path:
    """Directory for profile-scoped derived exports (Record bundle home)."""
    return profile_dir(user_id)

def resolve_profile_export_path(
    user_id: str,
    basename: str,
    *,
    prefer_existing: bool = True,
) -> Path:
    """
    Resolve a profile-scoped derived export with optional legacy root fallback.

    Canonical home: profile_dir(user_id) / basename (e.g. archive/grace-mar-instance/).
    During soak, returns REPO_ROOT / basename when only the legacy root copy exists.
    """
    canonical = profile_dir(user_id) / basename
    legacy_root = REPO_ROOT / basename
    if prefer_existing and legacy_root.is_file() and not canonical.is_file():
        return legacy_root
    return canonical

def resolve_prp_export_path(user_id: str, *, prefer_existing: bool = True) -> Path:
    """Resolve PRP / self-llm export path for a profile id."""
    profile = profile_dir(user_id)
    uid = user_id.strip()
    if profile.resolve() == REPO_ROOT.resolve():
        for name in ("self-llm.txt", "grace-mar-llm.txt"):
            candidate = REPO_ROOT / name
            if prefer_existing and candidate.is_file():
                return candidate
        return REPO_ROOT / "self-llm.txt"
    primary = profile / f"{uid}-llm.txt"
    if prefer_existing:
        if primary.is_file():
            return primary
        alt = profile / "self-llm.txt"
        if alt.is_file():
            return alt
    return primary

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

def profile_rel_posix(user_id: str) -> str:
    """Repo-relative POSIX path to the operator profile / Record bundle directory."""
    return profile_dir(user_id).relative_to(REPO_ROOT).as_posix()

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

def resolve_night_handoff_path(user_id: str, users_dir: Path | None = None) -> Path:
    """Read path for night-handoff.json (runtime/daily-handoff/ preferred; legacy compat)."""
    handoff_dir = resolve_repo_path("daily-handoff")
    new = handoff_dir / NIGHT_HANDOFF_BASENAME
    root = dream_handoff_root(users_dir or DEFAULT_USERS_DIR, user_id)
    old = root / "runtime/daily-handoff" / NIGHT_HANDOFF_BASENAME
    candidates = [p for p in (new, old) if p.is_file()]
    if not candidates:
        return new
    if len(candidates) == 1:
        return candidates[0]
    return max(candidates, key=lambda p: p.stat().st_mtime)

def night_handoff_write_path(user_id: str, users_dir: Path | None = None) -> Path:
    """Canonical write path for night-handoff.json."""
    handoff_dir = resolve_repo_path("daily-handoff")
    path = handoff_dir / NIGHT_HANDOFF_BASENAME
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
    """Return required Record basenames missing under the profile bundle."""
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

    if surface.canonical_key == "self_archive":
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

SKILL_SPLIT_NAMES: tuple[str, ...] = (
    "skill-think.md",
    "skill-write.md",
    "skill-steward.md",
)

def resolve_skill_split_path(name: str, user_dir: Path | None = None) -> Path:
    """Profile-local override, then continuity/ canonical. No repo-root fallback."""
    if user_dir is not None and (user_dir / name).is_file():
        return user_dir / name
    return REPO_ROOT / "continuity" / name

def resolve_memory_path(user_dir: Path | None = None) -> Path:
    """Strategy-codex continuity buffer at repo-root memory.md."""
    root_mem = REPO_ROOT / "memory.md"
    if root_mem.is_file():
        return root_mem
    if user_dir is not None:
        for name in ("memory.md", "self-memory.md"):
            leg = user_dir / name
            if leg.is_file():
                return leg
    return root_mem

def resolve_self_memory_path(user_dir: Path) -> Path:
    """Deprecated alias — use resolve_memory_path()."""
    return resolve_memory_path(user_dir)

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
        rel = profile_rel_posix(user_id)
        fix = "See docs/canonical-paths.md and docs/root-directory-map.md."
        raise RuntimeError(
            f"strategy-codex: canonical Record files missing under {rel}: {missing}.{ctx}\n{fix}"
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
