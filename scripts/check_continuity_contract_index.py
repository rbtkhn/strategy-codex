#!/usr/bin/env python3
"""Validate continuity/ contract ownership index and required owner files."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from continuity_paths import continuity_root  # noqa: E402

REQUIRED_OWNERS = (
    "README.md",
    "NOTEBOOK-CONTRACT.md",
    "STRATEGY-NOTEBOOK-ARCHITECTURE.md",
    "STATUS.md",
    "daily-strategy-inbox.md",
    "BOUNDARY.md",
    "COMPATIBILITY.md",
    "TOOLS.md",
    "OPERATING-MODE.md",
    "CONTRACT-INDEX.md",
)

LINK_TARGETS = (
    ("README.md", "CONTRACT-INDEX.md"),
    ("NOTEBOOK-CONTRACT.md", "CONTRACT-INDEX.md"),
)


@dataclass
class ContractIndexReport:
    continuity_root: str
    missing_owners: list[str] = field(default_factory=list)
    missing_links: list[str] = field(default_factory=list)
    compiled_marked_derived: bool = False
    errors: list[str] = field(default_factory=list)


def check_contract_index(repo_root: Path) -> ContractIndexReport:
    root = continuity_root(repo_root)
    report = ContractIndexReport(continuity_root=root.relative_to(repo_root).as_posix())

    for name in REQUIRED_OWNERS:
        if not (root / name).is_file():
            report.missing_owners.append(name)

    for src, target in LINK_TARGETS:
        path = root / src
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        if target not in text:
            report.missing_links.append(f"{src} must link to {target}")

    index_path = root / "CONTRACT-INDEX.md"
    if index_path.is_file():
        index_text = index_path.read_text(encoding="utf-8")
        report.compiled_marked_derived = "derived" in index_text.lower()
        if not report.compiled_marked_derived:
            report.errors.append("CONTRACT-INDEX.md must mark compiled views as derived")
    else:
        report.errors.append("CONTRACT-INDEX.md missing")

    report.errors.extend(
        f"missing owner: {name}" for name in report.missing_owners
    )
    report.errors.extend(report.missing_links)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = check_contract_index(REPO_ROOT)
    if args.json:
        print(json.dumps(asdict(report), indent=2))
    else:
        print(f"continuity root: {report.continuity_root}")
        for e in report.errors:
            print(f"error: {e}", file=sys.stderr)
    return 1 if report.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
