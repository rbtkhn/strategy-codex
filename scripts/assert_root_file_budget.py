#!/usr/bin/env python3
"""Warn or fail when repository root file count exceeds the complexity budget."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MANIFEST = REPO_ROOT / "root-file-budget.yaml"

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore[assignment]

@dataclass(frozen=True)
class BudgetEntry:
    path: str
    category: str
    relocation_target: str | None = None
    generator: str | None = None

@dataclass(frozen=True)
class RootFileBudget:
    max_root_files: int
    entries: tuple[BudgetEntry, ...]
    ignore_local: frozenset[str]
    categories: dict[str, str]

def _list_root_files() -> list[str]:
    return sorted(
        p.name
        for p in REPO_ROOT.iterdir()
        if p.is_file() and not p.name.startswith(".")
    )

def load_budget(manifest_path: Path = DEFAULT_MANIFEST) -> RootFileBudget:
    if yaml is None:
        raise RuntimeError("PyYAML required; install requirements-dev.txt")
    if not manifest_path.is_file():
        raise FileNotFoundError(f"missing manifest: {manifest_path.relative_to(REPO_ROOT)}")

    raw = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("root-file-budget.yaml must be a mapping")

    max_root_files = int(raw.get("max_root_files") or 20)
    categories = raw.get("categories") or {}
    if not isinstance(categories, dict):
        raise ValueError("categories must be a mapping")

    ignore_raw = raw.get("ignore_local") or []
    if not isinstance(ignore_raw, list):
        raise ValueError("ignore_local must be a list")
    ignore_local = frozenset(str(x) for x in ignore_raw)

    files_raw = raw.get("files")
    if not isinstance(files_raw, list) or not files_raw:
        raise ValueError("files must be a non-empty list")

    entries: list[BudgetEntry] = []
    seen: set[str] = set()
    for item in files_raw:
        if not isinstance(item, dict):
            raise ValueError("each files entry must be a mapping")
        rel = str(item.get("path") or "").strip().replace("\\", "/")
        category = str(item.get("category") or "").strip()
        if not rel or not category:
            raise ValueError("files entries require path and category")
        if category not in categories:
            raise ValueError(f"unknown category for {rel}: {category}")
        if rel in seen:
            raise ValueError(f"duplicate allowlist path: {rel}")
        seen.add(rel)
        relocation = item.get("relocation_target")
        generator = item.get("generator")
        entries.append(
            BudgetEntry(
                path=rel,
                category=category,
                relocation_target=str(relocation).strip() if relocation else None,
                generator=str(generator).strip() if generator else None,
            )
        )

    return RootFileBudget(
        max_root_files=max_root_files,
        entries=tuple(entries),
        ignore_local=ignore_local,
        categories={str(k): str(v) for k, v in categories.items()},
    )

def evaluate_budget(budget: RootFileBudget) -> tuple[list[str], dict[str, object]]:
    on_disk = [name for name in _list_root_files() if name not in budget.ignore_local]
    allowlisted = {entry.path: entry for entry in budget.entries}

    issues: list[str] = []
    unlisted = sorted(set(on_disk) - set(allowlisted))
    missing_allowlisted = sorted(set(allowlisted) - set(on_disk))

    if unlisted:
        issues.append(f"unlisted root files ({len(unlisted)}): {', '.join(unlisted)}")
    for path in missing_allowlisted:
        issues.append(f"allowlisted but absent: {path}")

    count = len(on_disk)
    over = count - budget.max_root_files
    if over > 0:
        issues.append(
            f"root file count {count} exceeds max_root_files {budget.max_root_files} by {over}"
        )

    by_category = Counter(allowlisted[name].category for name in on_disk if name in allowlisted)
    relocation_candidates = sorted(
        {
            entry.path
            for entry in budget.entries
            if entry.path in on_disk and entry.relocation_target
        }
    )

    report: dict[str, object] = {
        "root_file_count": count,
        "max_root_files": budget.max_root_files,
        "over_budget_by": max(0, over),
        "unlisted": unlisted,
        "missing_allowlisted": missing_allowlisted,
        "by_category": dict(sorted(by_category.items())),
        "relocation_candidates_on_disk": relocation_candidates,
    }
    return issues, report

def format_human(report: dict[str, object]) -> str:
    lines = [
        "# Root file budget",
        "",
        f"- Root files (non-dot): {report['root_file_count']} (max {report['max_root_files']})",
        f"- Over budget by: {report['over_budget_by']}",
        "",
        "## By category (allowlisted files on disk)",
        "",
    ]
    by_category = report.get("by_category") or {}
    if by_category:
        for category, count in by_category.items():
            lines.append(f"- {category}: {count}")
    else:
        lines.append("- (none)")
    lines.append("")
    relocation = report.get("relocation_candidates_on_disk") or []
    if relocation:
        lines.append("## Relocation candidates on disk")
        lines.append("")
        for path in relocation:
            lines.append(f"- {path}")
        lines.append("")
    return "\n".join(lines)

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        type=Path,
        default=DEFAULT_MANIFEST,
        help="Path to root-file-budget.yaml",
    )
    parser.add_argument("--json", action="store_true", help="Emit machine-readable report")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 when over budget or unlisted files exist",
    )
    args = parser.parse_args()

    try:
        budget = load_budget(args.manifest.resolve())
        issues, report = evaluate_budget(budget)
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"root-file-budget: {exc}", file=sys.stderr)
        return 1 if args.strict else 0

    if args.json:
        payload = {"ok": not issues, "issues": issues, **report}
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(format_human(report))
        if issues:
            for issue in issues:
                print(f"root-file-budget: {issue}", file=sys.stderr)

    if issues:
        return 1 if args.strict else 0

    print("ok: root file budget within limits")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
