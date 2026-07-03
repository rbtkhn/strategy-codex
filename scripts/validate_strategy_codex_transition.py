#!/usr/bin/env python3
"""Validate strategy-notebook -> strategy-codex compatibility migration guardrails."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

LEGACY_DIR = REPO_ROOT / "docs" / "skill-work" / "work-strategy" / "strategy-notebook"

SKILL_STRATEGY_PATH = REPO_ROOT / ".cursor" / "skills" / "skill-strategy" / "SKILL.md"

CRITICAL_DOCS = (
    "AGENTS.md",
    "docs/archive/skill-work-legacy/work-strategy/README.md",
    "docs/archive/skill-work-legacy/work-strategy/DEFAULT-PATH.md",
    "docs/archive/skill-work-legacy/work-strategy/SKILL-STRATEGY-DEPRECATED.md",
    ".cursor/rules/strategy-codex-pass.mdc",
)

REQUIRED_MARKERS = (
    "strategy-codex",
    "strategy-notebook",
    "deprecated compatibility",
)

FORBIDDEN_ACTIVE_ASSERTIONS = (
    "current on-disk path remains `strategy-notebook/`",
    "on disk under `strategy-notebook/`",
    "Those docs live under `docs/.../strategy-notebook/` for **length and SSOT**",
    "strategy-notebook (inbox, `days.md`, expert threads)",
)

def read_rel(rel: str) -> str:
    return (REPO_ROOT / rel).read_text(encoding="utf-8")

def validate_legacy_dir_is_pointer_only() -> list[str]:
    errors: list[str] = []
    if not LEGACY_DIR.is_dir():
        return [f"{LEGACY_DIR.relative_to(REPO_ROOT)}: missing legacy pointer directory"]
    allowed = {LEGACY_DIR / "README.md"}
    extra = [
        path.relative_to(REPO_ROOT).as_posix()
        for path in LEGACY_DIR.iterdir()
        if path not in allowed
    ]
    if extra:
        errors.append(
            "legacy strategy-notebook directory must remain pointer-only; found: "
            + ", ".join(sorted(extra))
        )
    return errors

def validate_critical_docs() -> list[str]:
    errors: list[str] = []
    for rel in CRITICAL_DOCS:
        text = read_rel(rel)
        missing = [marker for marker in REQUIRED_MARKERS if marker not in text]
        if missing:
            errors.append(f"{rel}: missing migration marker(s): {', '.join(missing)}")
        for forbidden in FORBIDDEN_ACTIVE_ASSERTIONS:
            if forbidden in text:
                errors.append(f"{rel}: forbidden active assertion: {forbidden}")
    return errors

def validate_skill_strategy_dissolved() -> list[str]:
    errors: list[str] = []
    if SKILL_STRATEGY_PATH.is_file():
        errors.append(
            f"{SKILL_STRATEGY_PATH.relative_to(REPO_ROOT)}: skill-strategy skill must be "
            "removed (dissolved); use DEFAULT-PATH + strategy-codex-pass.mdc"
        )
    deprecated = read_rel("docs/archive/skill-work-legacy/work-strategy/SKILL-STRATEGY-DEPRECATED.md")
    if "dissolved" not in deprecated.lower():
        errors.append("SKILL-STRATEGY-DEPRECATED.md: must document dissolved status")
    return errors

def validate_strategy_context_constants() -> list[str]:
    from strategy_context import (  # type: ignore
        LEGACY_STRATEGY_NOTEBOOK_DIR,
        NOTEBOOK,
        STRATEGY_CODEX_DIR,
    )

    errors: list[str] = []
    if NOTEBOOK != STRATEGY_CODEX_DIR:
        errors.append("scripts/strategy_context.py: NOTEBOOK must alias STRATEGY_CODEX_DIR")
    if STRATEGY_CODEX_DIR != REPO_ROOT / "codex":
        errors.append("scripts/strategy_context.py: STRATEGY_CODEX_DIR must point to /codex")
    if LEGACY_STRATEGY_NOTEBOOK_DIR != LEGACY_DIR:
        errors.append(
            "scripts/strategy_context.py: LEGACY_STRATEGY_NOTEBOOK_DIR must point to the deprecated pointer directory"
        )
    return errors

def main() -> int:
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    errors: list[str] = []
    errors.extend(validate_legacy_dir_is_pointer_only())
    errors.extend(validate_critical_docs())
    errors.extend(validate_skill_strategy_dissolved())
    errors.extend(validate_strategy_context_constants())
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(
            f"validate_strategy_codex_transition: failed ({len(errors)} issue(s))",
            file=sys.stderr,
        )
        return 1
    print("validate_strategy_codex_transition: OK", file=sys.stderr)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
