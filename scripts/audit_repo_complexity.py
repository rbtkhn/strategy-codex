#!/usr/bin/env python3
"""Measure repository complexity metrics for the mitigation program."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from repo_io import REPO_PATH_MIGRATIONS, TARGET_ROOT_FOLDERS, scan_legacy_path_layout  # noqa: E402

PRIMARY_DOC_PATHS = (
    "README.md",
    "AGENTS.md",
    "contributing.md",
    "instance-doctrine.md",
    "docs/start-here.md",
    "docs/product-identity.md",
    "LLM-ROUTING.md",
    "repo-map.yaml",
)

ARCHIVE_PREFIXES = (
    "archive/",
    "docs/archive/",
    "archive/grace-mar-corpus/",
)

LEGACY_MARKERS = (
    "compatibility",
    "legacy",
    "deprecated",
    "frozen archaeology",
)

TERM_PATTERNS: dict[str, re.Pattern[str]] = {
    "grace_mar": re.compile(r"Grace-Mar|grace-mar", re.I),
    "companion_self": re.compile(r"companion-self", re.I),
    "fork_revive": re.compile(r"fork revive|fork-revive", re.I),
    "record": re.compile(r"\bRecord\b"),
    "voice": re.compile(r"\bVoice\b"),
}

ROUTING_SURFACES = (
    REPO_ROOT / "repo-map.yaml",
    REPO_ROOT / "LLM-ROUTING.md",
    REPO_ROOT / "statecraft" / "voices" / "INDEX.md",
    REPO_ROOT / "source-archive" / "statecraft" / "thread-index.md",
    REPO_ROOT / "source-archive" / "statecraft" / "channel-index.md",
)

ALWAYS_READ_CANDIDATES = (
    REPO_ROOT / "AGENTS.md",
    REPO_ROOT / "instance-doctrine.md",
)

THRESHOLDS = {
    "root_files_max": 20,
    "root_dirs_max": len(TARGET_ROOT_FOLDERS),
    "primary_routing_docs_max": 3,
    "always_read_agent_docs_max": 1,
    "legacy_fallback_entries_max": 0,
    "grace_mar_primary_mentions_max": 3,
    "authority_categories_max": 4,
}


@dataclass
class ComplexityMetrics:
    root_directories: int
    root_files: int
    grace_mar_refs_total: int
    grace_mar_refs_primary: int
    fork_revive_refs: int
    companion_self_refs: int
    record_refs: int
    voice_refs: int
    legacy_marker_hits: int
    routing_index_surfaces: int
    repo_map_routes: int
    legacy_fallback_entries: int
    legacy_path_layout_issues: int
    repo_path_migration_keys: int
    always_read_docs: int
    always_read_lines: int
    cursor_rules_count: int
    cursor_rules_lines: int
    pyproject_name: str


def _is_archived(rel_posix: str) -> bool:
    return any(rel_posix.startswith(prefix) for prefix in ARCHIVE_PREFIXES)


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def _count_terms(text: str) -> dict[str, int]:
    return {name: len(pat.findall(text)) for name, pat in TERM_PATTERNS.items()}


SCAN_ROOTS = (
    REPO_ROOT,
    REPO_ROOT / "docs",
    REPO_ROOT / ".cursor" / "rules",
    REPO_ROOT / ".cursor" / "skills",
    REPO_ROOT / "archive",
    REPO_ROOT / "statecraft",
    REPO_ROOT / "singularity",
    REPO_ROOT / "essays",
    REPO_ROOT / "scripts",
    REPO_ROOT / ".github" / "workflows",
)

SKIP_PREFIXES = (
    "public/ph-civ/",
    "research/",
    "codex/predictive-history/",
)

def _scan_markdown_globs() -> list[Path]:
    paths: set[Path] = set()
    for root in SCAN_ROOTS:
        if not root.is_dir():
            continue
        for pattern in ("*.md", "*.mdc", "*.yaml", "*.yml", "**/*.md", "**/*.mdc", "**/*.yaml", "**/*.yml"):
            for path in root.glob(pattern):
                if not path.is_file():
                    continue
                rel = path.relative_to(REPO_ROOT).as_posix()
                if rel.startswith(".git/") or "/node_modules/" in rel:
                    continue
                if any(rel.startswith(prefix) for prefix in SKIP_PREFIXES):
                    continue
                paths.add(path)
    return sorted(paths)

def collect_metrics() -> ComplexityMetrics:
    root_dirs = sum(1 for p in REPO_ROOT.iterdir() if p.is_dir() and p.name in TARGET_ROOT_FOLDERS)
    root_files = sum(1 for p in REPO_ROOT.iterdir() if p.is_file() and not p.name.startswith("."))

    term_totals: Counter[str] = Counter()
    term_primary: Counter[str] = Counter()
    legacy_marker_hits = 0

    for path in _scan_markdown_globs():
        rel = path.relative_to(REPO_ROOT).as_posix()
        text = _read_text(path)
        if not text:
            continue
        counts = _count_terms(text)
        term_totals.update(counts)
        if not _is_archived(rel):
            term_primary.update(counts)
        lower = text.lower()
        legacy_marker_hits += sum(lower.count(marker) for marker in LEGACY_MARKERS)

    repo_map_routes = 0
    repo_map_path = REPO_ROOT / "repo-map.yaml"
    if repo_map_path.is_file():
        repo_map_routes = repo_map_path.read_text(encoding="utf-8").count("\n  - id:")

    legacy_fallback_entries = sum(
        1 for _key, entry in REPO_PATH_MIGRATIONS.items() if len(entry) > 1
    )
    legacy_path_layout_issues = len(scan_legacy_path_layout())

    always_read_lines = 0
    always_read_docs = 0
    for path in ALWAYS_READ_CANDIDATES:
        if path.is_file():
            always_read_docs += 1
            always_read_lines += len(_read_text(path).splitlines())

    cursor_rules = sorted((REPO_ROOT / ".cursor" / "rules").glob("*.mdc"))
    cursor_rules_lines = sum(len(_read_text(p).splitlines()) for p in cursor_rules)

    pyproject_name = "unknown"
    pyproject = REPO_ROOT / "pyproject.toml"
    if pyproject.is_file():
        match = re.search(r'^name\s*=\s*"([^"]+)"', pyproject.read_text(encoding="utf-8"), re.M)
        if match:
            pyproject_name = match.group(1)

    routing_present = sum(1 for p in ROUTING_SURFACES if p.is_file())

    return ComplexityMetrics(
        root_directories=root_dirs,
        root_files=root_files,
        grace_mar_refs_total=term_totals["grace_mar"],
        grace_mar_refs_primary=term_primary["grace_mar"],
        fork_revive_refs=term_totals["fork_revive"],
        companion_self_refs=term_totals["companion_self"],
        record_refs=term_totals["record"],
        voice_refs=term_totals["voice"],
        legacy_marker_hits=legacy_marker_hits,
        routing_index_surfaces=routing_present,
        repo_map_routes=repo_map_routes,
        legacy_fallback_entries=legacy_fallback_entries,
        legacy_path_layout_issues=legacy_path_layout_issues,
        repo_path_migration_keys=len(REPO_PATH_MIGRATIONS),
        always_read_docs=always_read_docs,
        always_read_lines=always_read_lines,
        cursor_rules_count=len(cursor_rules),
        cursor_rules_lines=cursor_rules_lines,
        pyproject_name=pyproject_name,
    )


def format_report(metrics: ComplexityMetrics) -> str:
    lines = [
        "# Complexity Audit",
        "",
        f"Generated: {date.today().isoformat()}",
        "",
        "## Summary",
        "",
        f"- Root directories: {metrics.root_directories} (target <= {THRESHOLDS['root_dirs_max']})",
        f"- Root files: {metrics.root_files} (target <= {THRESHOLDS['root_files_max']})",
        f"- Python package name (`pyproject.toml`): `{metrics.pyproject_name}`",
        "",
        "## Terminology scans (markdown/yaml/mdc)",
        "",
        f"- Grace-Mar / grace-mar (total): {metrics.grace_mar_refs_total}",
        f"- Grace-Mar / grace-mar (non-archive paths): {metrics.grace_mar_refs_primary}",
        f"- fork revive: {metrics.fork_revive_refs}",
        f"- companion-self: {metrics.companion_self_refs}",
        f"- Record (word): {metrics.record_refs}",
        f"- Voice (word): {metrics.voice_refs}",
        f"- legacy/compatibility/deprecated marker hits: {metrics.legacy_marker_hits}",
        "",
        "## Routing surfaces",
        "",
        f"- Present routing/index surfaces (of {len(ROUTING_SURFACES)} tracked): {metrics.routing_index_surfaces}",
        f"- repo-map.yaml routes (approx): {metrics.repo_map_routes}",
        f"- Primary routing front doors listed in plan: {len(PRIMARY_DOC_PATHS)}",
        "",
        "## Path resolver",
        "",
        f"- REPO_PATH_MIGRATIONS keys: {metrics.repo_path_migration_keys}",
        f"- Keys with legacy fallback tuples: {metrics.legacy_fallback_entries}",
        f"- Active legacy/dual path layouts on disk: {metrics.legacy_path_layout_issues}",
        "",
        "## Agent / contributor preflight",
        "",
        f"- Always-read candidate docs: {metrics.always_read_docs} ({metrics.always_read_lines} lines)",
        f"- `.cursor/rules/*.mdc`: {metrics.cursor_rules_count} files, {metrics.cursor_rules_lines} lines total",
        "",
        "## Threshold reference",
        "",
        "See docs/complexity-budget.md for mitigation targets and CI rollout.",
        "",
    ]
    return "\n".join(lines)


def check_thresholds(metrics: ComplexityMetrics) -> list[str]:
    failures: list[str] = []
    if metrics.root_files > THRESHOLDS["root_files_max"]:
        failures.append(f"root_files {metrics.root_files} > {THRESHOLDS['root_files_max']}")
    if metrics.root_directories > THRESHOLDS["root_dirs_max"]:
        failures.append(
            f"root_directories {metrics.root_directories} > {THRESHOLDS['root_dirs_max']}"
        )
    if len(PRIMARY_DOC_PATHS) > THRESHOLDS["primary_routing_docs_max"]:
        failures.append(
            f"primary routing doc list {len(PRIMARY_DOC_PATHS)} > {THRESHOLDS['primary_routing_docs_max']}"
        )
    if metrics.legacy_fallback_entries > THRESHOLDS["legacy_fallback_entries_max"]:
        failures.append(
            f"legacy_fallback_entries {metrics.legacy_fallback_entries} > {THRESHOLDS['legacy_fallback_entries_max']}"
        )
    if metrics.pyproject_name != "strategy-codex":
        failures.append(f"pyproject name {metrics.pyproject_name!r} != 'strategy-codex'")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write-baseline", type=Path)
    args = parser.parse_args()

    metrics = collect_metrics()
    report = format_report(metrics)

    if args.json:
        print(json.dumps(asdict(metrics), indent=2, sort_keys=True))
    else:
        print(report)

    if args.write_baseline:
        out = args.write_baseline
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(report + "\n", encoding="utf-8")
        print(f"Wrote baseline: {out.resolve().relative_to(REPO_ROOT.resolve())}", file=sys.stderr)

    if args.check:
        failures = check_thresholds(metrics)
        if failures:
            for msg in failures:
                print(f"threshold fail: {msg}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
