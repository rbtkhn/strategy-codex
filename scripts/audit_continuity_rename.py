#!/usr/bin/env python3
"""Audit codex/ → continuity/ rename references and migration state."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

SCAN_EXTENSIONS = frozenset({".md", ".mdc", ".py", ".yaml", ".yml", ".json", ".toml", ".sh", ".txt"})

SKIP_DIR_NAMES = frozenset(
    {
        ".git",
        ".venv",
        "node_modules",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
    }
)

SKIP_DIR_PREFIXES = (".tmp-pytest-", ".codex-pytest-", ".codex-tmp", ".codex-test-temp")

ARCHIVE_PREFIXES = (
    "archive/",
    "docs/archive/",
)

CANONICAL_ROUTING_DOCS = (
    "README.md",
    "AGENTS.md",
    "LLM-ROUTING.md",
    "repo-map.yaml",
    "docs/start-here.md",
    "docs/root-directory-map.md",
    "docs/canonical-paths.md",
    "docs/context-layer.md",
    "memory.md",
)

# Post-move: codex/ path refs allowed under these repo-relative prefixes.
APPROVED_LEGACY_PATH_PREFIXES = (
    "codex/README.md",
    "docs/codex-to-continuity-rename.md",
    "docs/archive/",
    "archive/",
    "platform/users/grace-mar/",
    "platform/config/fork-language-audit",
    "scripts/audit_continuity_rename.py",
    "scripts/migrate_codex_speakers_to_statecraft.py",
    "scripts/build_external_codex_family_report.py",
    "scripts/build_external_codex_neighborhood.py",
    "scripts/external_codex_common.py",
    "scripts/strategy_codex_config.py",
    "scripts/validate_strategy_codex_transition.py",
    "platform/config/strategy_codex.yaml",
    "platform/src/strategy_codex/",
    "tests/test_audit_continuity_rename.py",
)

TOKEN_PATTERNS: dict[str, re.Pattern[str]] = {
    "codex_slash": re.compile(r"(?<![\w-])\.?/?\.?/?codex/"),
    "continuity_slash": re.compile(r"(?<![\w-])\.?/?\.?/?continuity/"),
    "strategy_codex": re.compile(r"strategy-codex"),
    "strategy_notebook": re.compile(r"strategy-notebook"),
    "strategy_expert": re.compile(r"strategy-expert"),
    "memory_md": re.compile(r"\bmemory\.md\b"),
}

Classification = str

CLASSIFICATIONS = (
    "path_reference",
    "public_project_name",
    "legacy_compatibility_name",
    "script_contract",
    "parser_contract",
    "fixture_contract",
    "generated_artifact",
    "doc_prose",
    "redirect_pointer",
    "unknown",
)


@dataclass
class Finding:
    path: str
    line: int
    token: str
    match: str
    classification: Classification
    context: str = ""


@dataclass
class AuditReport:
    migration_state: str
    scanned_files: int = 0
    findings: list[Finding] = field(default_factory=list)
    by_classification: dict[str, int] = field(default_factory=dict)
    by_token: dict[str, int] = field(default_factory=dict)
    strict_issues: list[str] = field(default_factory=list)


def _should_skip_dir(name: str) -> bool:
    if name in SKIP_DIR_NAMES:
        return True
    return any(name.startswith(p) for p in SKIP_DIR_PREFIXES)


def _is_archived(rel_posix: str) -> bool:
    return any(rel_posix.startswith(p) for p in ARCHIVE_PREFIXES)


def _approved_legacy_path(rel_posix: str) -> bool:
    if rel_posix in APPROVED_LEGACY_PATH_PREFIXES:
        return True
    return any(rel_posix.startswith(p) for p in APPROVED_LEGACY_PATH_PREFIXES)


def detect_migration_state(repo_root: Path) -> str:
    codex = repo_root / "codex"
    continuity = repo_root / "continuity"
    codex_is_dir = codex.is_dir()
    continuity_is_dir = continuity.is_dir()

    if continuity_is_dir and codex_is_dir:
        codex_entries = [p for p in codex.iterdir() if p.name != ".gitkeep"]
        if len(codex_entries) == 1 and codex_entries[0].name == "README.md":
            return "post_move_redirect"
        if codex_entries:
            return "dual_layout"
        return "post_move_redirect"
    if continuity_is_dir:
        return "post_move"
    if codex_is_dir:
        return "pre_move"
    return "missing_both"


def _classify(
    rel_posix: str,
    token: str,
    match: str,
    line_text: str,
) -> Classification:
    if token == "strategy_codex":
        if re.search(r"codex/", line_text) and "strategy-codex" not in match:
            pass
        return "public_project_name"
    if token == "strategy_notebook":
        return "legacy_compatibility_name"
    if token == "strategy_expert":
        if "strategy-expert-" in line_text or "strategy_expert" in rel_posix:
            if rel_posix.startswith("tests/fixtures/"):
                return "fixture_contract"
            if "/scripts/" in rel_posix or rel_posix.startswith("scripts/"):
                return "parser_contract"
        return "legacy_compatibility_name"
    if token == "memory_md":
        return "doc_prose"
    if token in {"codex_slash", "continuity_slash"}:
        if rel_posix == "codex/README.md" and "continuity/" in line_text:
            return "redirect_pointer"
        if rel_posix.startswith("runtime/artifacts/"):
            return "generated_artifact"
        if rel_posix.startswith("tests/fixtures/"):
            return "fixture_contract"
        if rel_posix.startswith("scripts/") or "/scripts/" in rel_posix:
            return "script_contract"
        if _is_archived(rel_posix):
            return "doc_prose"
        return "path_reference"
    return "unknown"


def iter_scan_files(repo_root: Path) -> list[Path]:
    files: list[Path] = []
    for path in repo_root.rglob("*"):
        if not path.is_file():
            continue
        rel_parts = path.relative_to(repo_root).parts
        if any(_should_skip_dir(p) for p in rel_parts):
            continue
        if path.suffix.lower() not in SCAN_EXTENSIONS:
            continue
        files.append(path)
    return sorted(files)


def scan_repo(repo_root: Path) -> AuditReport:
    state = detect_migration_state(repo_root)
    report = AuditReport(migration_state=state)
    findings: list[Finding] = []

    for path in iter_scan_files(repo_root):
        rel = path.relative_to(repo_root).as_posix()
        report.scanned_files += 1
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for line_no, line in enumerate(text.splitlines(), start=1):
            for token, pattern in TOKEN_PATTERNS.items():
                for m in pattern.finditer(line):
                    classification = _classify(rel, token, m.group(0), line)
                    findings.append(
                        Finding(
                            path=rel,
                            line=line_no,
                            token=token,
                            match=m.group(0),
                            classification=classification,
                            context=line.strip()[:120],
                        )
                    )

    report.findings = findings
    report.by_classification = dict(Counter(f.classification for f in findings))
    report.by_token = dict(Counter(f.token for f in findings))
    return report


def _codex_path_finding_allowed(f: Finding, state: str) -> bool:
    if f.token != "codex_slash":
        return True
    if state in {"pre_move", "dual_layout"}:
        return True
    if _approved_legacy_path(f.path):
        return True
    if f.path.startswith("platform/src/grace_mar/"):
        return True
    if f.path.startswith("runtime/bundle/"):
        return True
    if f.path.startswith("runtime/artifacts/"):
        return True
    if f.path.startswith("source-archive/"):
        return True
    if f.path in {"continuity/COMPATIBILITY.md", "docs/repo-convergence.md", "docs/codex-to-continuity-rename.md"}:
        return True
    if "legacy" in f.context.lower() or "formerly" in f.context.lower() or "→" in f.context:
        return True
    if _is_archived(f.path):
        return True
    if f.classification in {
        "redirect_pointer",
        "legacy_compatibility_name",
        "parser_contract",
        "fixture_contract",
        "generated_artifact",
    }:
        return True
    # Inside continuity/ corpus referencing old name in prose
    if f.path.startswith("continuity/") and "formerly" in f.context.lower():
        return True
    if "/intake/" in f.path and f.path.endswith(".txt"):
        return True
    return False


def strict_checks(report: AuditReport, repo_root: Path) -> list[str]:
    issues: list[str] = []
    state = report.migration_state

    if state == "dual_layout":
        issues.append(
            "dual_layout: both codex/ and continuity/ contain live corpus — "
            "finish migration or remove duplicate"
        )
    if state == "missing_both":
        issues.append("missing_both: neither codex/ nor continuity/ exists")

    codex_dir = repo_root / "codex"
    continuity_dir = repo_root / "continuity"

    if state in {"post_move", "post_move_redirect"}:
        if not continuity_dir.is_dir():
            issues.append("post_move: continuity/ directory missing")
        if not (continuity_dir / "README.md").is_file():
            issues.append("post_move: continuity/README.md missing")
        if codex_dir.is_dir():
            extras = [
                p.relative_to(codex_dir).as_posix()
                for p in codex_dir.rglob("*")
                if p.is_file() and p.name not in {"README.md", ".gitkeep"}
            ]
            if extras:
                issues.append(
                    "post_move: codex/ must be redirect-only; live files: "
                    + ", ".join(sorted(extras)[:10])
                    + ("..." if len(extras) > 10 else "")
                )
            if not (codex_dir / "README.md").is_file():
                issues.append("post_move: codex/README.md redirect missing")

    if state == "pre_move":
        if not codex_dir.is_dir():
            issues.append("pre_move: codex/ directory missing")
        if continuity_dir.is_dir() and any(continuity_dir.iterdir()):
            issues.append("pre_move: continuity/ populated before folder move")

    # Unapproved codex/ path references after migration
    if state in {"post_move", "post_move_redirect"}:
        bad_path_refs: list[str] = []
        for f in report.findings:
            if f.classification != "path_reference" or f.token != "codex_slash":
                continue
            if not _codex_path_finding_allowed(f, state):
                bad_path_refs.append(f"{f.path}:{f.line}")
        if bad_path_refs:
            sample = bad_path_refs[:15]
            issues.append(
                f"unclassified codex/ path references ({len(bad_path_refs)}): "
                + "; ".join(sample)
                + ("..." if len(bad_path_refs) > 15 else "")
            )

        # Canonical routing docs should prefer continuity/
        for rel in CANONICAL_ROUTING_DOCS:
            p = repo_root / rel
            if not p.is_file():
                continue
            text = p.read_text(encoding="utf-8", errors="replace")
            if re.search(r"(?<![\w-])codex/", text) and "formerly" not in text:
                if rel == "docs/codex-to-continuity-rename.md":
                    continue
                if "legacy" in text.lower() or "redirect" in text.lower():
                    continue
                issues.append(
                    f"canonical doc {rel} still uses codex/ as path without legacy framing"
                )

    if state in {"post_move", "post_move_redirect", "dual_layout"}:
        if continuity_dir.is_dir() and not (continuity_dir / "README.md").is_file():
            issues.append("continuity/README.md missing or broken")

    return issues


def format_markdown_report(report: AuditReport) -> str:
    lines = [
        "# Continuity rename audit",
        "",
        f"Generated: {date.today().isoformat()}",
        "",
        f"Migration state: **{report.migration_state}**",
        f"Scanned files: {report.scanned_files}",
        f"Findings: {len(report.findings)}",
        "",
        "## By classification",
        "",
    ]
    for cls, count in sorted(report.by_classification.items()):
        lines.append(f"- {cls}: {count}")
    lines.extend(["", "## By token", ""])
    for tok, count in sorted(report.by_token.items()):
        lines.append(f"- {tok}: {count}")
    if report.strict_issues:
        lines.extend(["", "## Strict issues", ""])
        for issue in report.strict_issues:
            lines.append(f"- {issue}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emit JSON report on stdout")
    parser.add_argument("--strict", action="store_true", help="Fail on migration violations")
    parser.add_argument(
        "--write-report",
        action="store_true",
        help="Write runtime/artifacts/continuity-rename-audit.{json,md}",
    )
    args = parser.parse_args()

    report = scan_repo(REPO_ROOT)
    if args.strict:
        report.strict_issues = strict_checks(report, REPO_ROOT)

    if args.write_report:
        out_dir = REPO_ROOT / "runtime" / "artifacts"
        out_dir.mkdir(parents=True, exist_ok=True)
        json_path = out_dir / "continuity-rename-audit.json"
        md_path = out_dir / "continuity-rename-audit.md"
        payload = {
            "migration_state": report.migration_state,
            "scanned_files": report.scanned_files,
            "by_classification": report.by_classification,
            "by_token": report.by_token,
            "strict_issues": report.strict_issues,
            "finding_count": len(report.findings),
        }
        json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        md_path.write_text(format_markdown_report(report), encoding="utf-8")
        print(f"Wrote {json_path.relative_to(REPO_ROOT)}", file=sys.stderr)
        print(f"Wrote {md_path.relative_to(REPO_ROOT)}", file=sys.stderr)

    if args.json:
        payload = {
            "migration_state": report.migration_state,
            "scanned_files": report.scanned_files,
            "by_classification": report.by_classification,
            "by_token": report.by_token,
            "strict_issues": report.strict_issues,
            "findings": [asdict(f) for f in report.findings[:500]],
            "findings_truncated": len(report.findings) > 500,
        }
        print(json.dumps(payload, indent=2))
    elif not args.write_report:
        print(format_markdown_report(report))

    if args.strict and report.strict_issues:
        for issue in report.strict_issues:
            print(f"strict: {issue}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
