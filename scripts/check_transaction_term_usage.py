#!/usr/bin/env python3
"""Guard against transaction vocabulary as default durable-work doctrine."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# SSOT: docs/complexity-budget.md — Term law (note vs transaction)
CANONICAL_NOTE_TERM_LAW = (
    "Use note for durable analytical work products. "
    "Use transaction only for operational receipts, business ledger entries, or legacy compatibility stubs."
)

# Tier 1: high-traffic doctrine (strict scan)
TIER1_DOCS = (
    "README.md",
    "AGENTS.md",
    "contributing.md",
    "LLM-ROUTING.md",
    "docs/start-here.md",
    "docs/public-orientation.md",
    "docs/product-identity.md",
    "docs/intelligence-harness.md",
    "docs/architecture.md",
    "docs/complexity-budget.md",
    "docs/agent-rules/deep-rules.md",
    "docs/statecraft-intake-queue.md",
    "docs/glossary.md",
    "docs/harness-architecture-map.md",
    "docs/strategy-codex-redesign-brief.md",
    "docs/prose-index.md",
    "docs/work-membrane-v2.md",
    "statecraft/README.md",
    "statecraft/statecraft.md",
    "statecraft/notes/README.md",
    "essays/from-accumulation-to-governed-interpretive-machine.md",
)

# Tier 2: agent contract skills
TIER2_SKILLS = (
    ".cursor/skills/coffee/SKILL.md",
    ".cursor/skills/civ-state/SKILL.md",
    ".cursor/skills/memory/SKILL.md",
    ".cursor/skills/state-synthesis/SKILL.md",
    ".cursor/skills/statecraft-source-intake/SKILL.md",
)

DISALLOWED_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (
        re.compile(r"archive\s*→\s*synthesis\s*→\s*transactions?", re.I),
        "retired ladder: archive → synthesis → transactions",
    ),
    (
        re.compile(r"archive\s*->\s*synthesis\s*->\s*transactions?", re.I),
        "retired ladder: archive -> synthesis -> transactions",
    ),
    (
        re.compile(r"transaction object\s*[—–-]\s*default ceiling", re.I),
        "transaction object as default ceiling",
    ),
    (
        re.compile(r"bounded output object under a lane", re.I),
        "transaction defined as bounded output object under a lane",
    ),
    (
        re.compile(r"\|\s*\*\*transaction\*\*\s*\|\s*Bounded", re.I),
        "terms table: transaction | Bounded …",
    ),
    (
        re.compile(r"transaction objects carry judgment", re.I),
        "transaction objects carry judgment",
    ),
    (
        re.compile(r"judgment\s*/\s*transaction object", re.I),
        "retired kernel: judgment / transaction object",
    ),
    (
        re.compile(r"transaction object\s*\(\s*accountable ceiling\s*\)", re.I),
        "transaction object (accountable ceiling)",
    ),
    (
        re.compile(r"\|\s*\*\*transactions\*\*\s*\|\s*reusable statecraft instruments", re.I),
        "prose-index: transactions as reusable instruments",
    ),
    (
        re.compile(r"synthesis and transaction objects", re.I),
        "synthesis and transaction objects (use notes)",
    ),
]

ALLOWED_PATH_FRAGMENTS = (
    "docs/archive/skill-work-legacy/work-business/",
    "scripts/emit_business_transaction.py",
    "scripts/import_bank_csv.py",
    "statecraft/templates/sid-transaction-memo.md",
    "docs/audits/transaction-retirement-inventory",
)

ALLOWED_LINE_PHRASES = (
    "transaction receipt",
    "business transaction",
    "legacy transaction",
    "operational transaction",
    "transaction-router",
    "instrument-router",
    "Deprecated compatibility stub",
    "transaction retirement",
    "transaction-fit screening",
    "transactional settlement",
    "transaction use",
    "instrument use",
    "settlement hook",
    "Older docs may use",
    'Use "transaction" only for operational',
    "Use transaction only for operational",
    "legacy transaction stub",
    "Term law (note vs transaction)",
    "transaction-retirement-inventory",
)

STUB_MARKER = "Deprecated compatibility stub"

def _path_allowed(rel: str) -> bool:
    if any(frag in rel for frag in ALLOWED_PATH_FRAGMENTS):
        return True
    if "/transactions/" in rel.replace("\\", "/") and STUB_MARKER in rel:
        return False  # still scan stubs for doctrine phrases in body
    return False

def _line_allowed(line: str) -> bool:
    lower = line.lower()
    return any(phrase.lower() in lower for phrase in ALLOWED_LINE_PHRASES)

def _is_legacy_stub(text: str) -> bool:
    return STUB_MARKER in text

def scan_file(path: Path, *, skills_only: bool = False) -> list[str]:
    rel = path.relative_to(REPO_ROOT).as_posix()
    if _path_allowed(rel):
        return []
    if skills_only and not rel.startswith(".cursor/skills/"):
        return []

    text = path.read_text(encoding="utf-8", errors="replace")
    if _is_legacy_stub(text) and "/transactions/" in rel:
        return []

    issues: list[str] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        if _line_allowed(line):
            continue
        for pattern, label in DISALLOWED_PATTERNS:
            if pattern.search(line):
                issues.append(f"{rel}:{lineno}: {label}: {line.strip()[:120]}")
    return issues

def collect_targets(*, skills_strict: bool) -> list[Path]:
    targets: list[Path] = []
    for rel in TIER1_DOCS:
        p = REPO_ROOT / rel
        if p.is_file():
            targets.append(p)
    if skills_strict:
        for rel in TIER2_SKILLS:
            p = REPO_ROOT / rel
            if p.is_file():
                targets.append(p)
    return sorted(set(targets))

def run_check(*, strict: bool, skills_strict: bool) -> int:
    issues: list[str] = []
    for path in collect_targets(skills_strict=skills_strict):
        issues.extend(scan_file(path, skills_only=skills_strict and path not in [
            REPO_ROOT / r for r in TIER1_DOCS
        ]))

    if issues:
        for line in issues:
            print(line, file=sys.stderr)
        mode = "strict" if strict else "warn"
        print(
            f"check_transaction_term_usage ({mode}): {len(issues)} violation(s)",
            file=sys.stderr,
        )
        return 1 if strict else 0

    n = len(collect_targets(skills_strict=skills_strict))
    print(f"check_transaction_term_usage: ok ({n} file(s))")
    return 0

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 on violations (default: warn only, exit 0)",
    )
    ap.add_argument(
        "--warn",
        action="store_true",
        help="Warn mode (default; same as omitting --strict)",
    )
    ap.add_argument(
        "--skills-strict",
        action="store_true",
        help="Also scan tier-2 agent skills",
    )
    args = ap.parse_args()
    return run_check(strict=args.strict, skills_strict=args.skills_strict)

if __name__ == "__main__":
    raise SystemExit(main())
