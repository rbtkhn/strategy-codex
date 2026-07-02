#!/usr/bin/env python3
"""Validate continuity-layer STATUS.md freshness and cross-references."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

RE_DATE_HEADING = re.compile(r"^##\s+(\d{4}-\d{2}-\d{2})\b", re.MULTILINE)
RE_LAST_ENTRY_DATE = re.compile(
    r"\*\*Last substantive entry\*\*\s*\|\s*`(\d{4}-\d{2}-\d{2})`"
)
RE_DAYS_LINK = re.compile(r"\[`[^`]+`\]\(([^)]*days\.md[^)]*)\)")
RE_CHAPTER_MONTH = re.compile(r"chapters/(\d{4}-\d{2})")

from continuity_paths import continuity_root as _continuity_root

def continuity_root(repo_root: Path) -> Path:
    return _continuity_root(repo_root)

@dataclass
class StatusReport:
    continuity_root: str
    status_exists: bool = False
    inbox_exists: bool = False
    predictions_exists: bool = False
    has_next_actions: bool = False
    last_entry_date: str | None = None
    last_entry_days_path: str | None = None
    last_entry_anchor_found: bool = False
    active_chapters: list[str] = field(default_factory=list)
    latest_chapter_month: str | None = None
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

def _resolve_link(root: Path, link: str) -> Path:
    link = link.split("#", 1)[0]
    if link.startswith("../"):
        return (root.parent / link.removeprefix("../")).resolve()
    return (root / link).resolve()

def _find_chapter_months(root: Path) -> list[str]:
    chapters = root / "chapters"
    if not chapters.is_dir():
        return []
    months: list[str] = []
    for days in chapters.rglob("days.md"):
        rel = days.relative_to(root).as_posix()
        m = RE_CHAPTER_MONTH.search(rel)
        if m:
            months.append(m.group(1))
    return sorted(set(months))

def check_status(repo_root: Path) -> StatusReport:
    root = continuity_root(repo_root)
    report = StatusReport(continuity_root=root.relative_to(repo_root).as_posix())

    status_path = root / "STATUS.md"
    if not status_path.is_file():
        report.errors.append("STATUS.md missing")
        return report
    report.status_exists = True
    text = status_path.read_text(encoding="utf-8")

    if "## Next actions" not in text and "## Next Actions" not in text:
        report.errors.append("STATUS.md missing Next actions section")
    else:
        report.has_next_actions = True

    inbox = root / "daily-strategy-inbox.md"
    report.inbox_exists = inbox.is_file()
    if not report.inbox_exists:
        report.errors.append("daily-strategy-inbox.md missing")

    predictions = root / "strategy-expert-predictions.md"
    report.predictions_exists = predictions.is_file()
    if not report.predictions_exists:
        report.errors.append("strategy-expert-predictions.md missing")

    date_m = RE_LAST_ENTRY_DATE.search(text)
    if date_m:
        report.last_entry_date = date_m.group(1)
    else:
        report.errors.append("Last substantive entry date not found in STATUS.md")

    days_links = RE_DAYS_LINK.findall(text)
    for link in days_links:
        if "days.md" in link:
            report.last_entry_days_path = link
            break

    if report.last_entry_date and report.last_entry_days_path:
        days_path = _resolve_link(root, report.last_entry_days_path)
        if not days_path.is_file():
            report.errors.append(f"referenced days.md missing: {report.last_entry_days_path}")
        else:
            days_text = days_path.read_text(encoding="utf-8")
            anchor = f"## {report.last_entry_date}"
            report.last_entry_anchor_found = anchor in days_text
            if not report.last_entry_anchor_found:
                report.errors.append(
                    f"anchor {anchor!r} missing in {report.last_entry_days_path}"
                )

    for m in RE_CHAPTER_MONTH.finditer(text):
        report.active_chapters.append(m.group(1))

    all_months = _find_chapter_months(root)
    if all_months:
        report.latest_chapter_month = all_months[-1]
        if report.active_chapters:
            active_max = max(report.active_chapters)
            if active_max < report.latest_chapter_month:
                report.warnings.append(
                    f"active chapter month {active_max} appears behind "
                    f"latest chapter month {report.latest_chapter_month}"
                )

    return report

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    args = parser.parse_args()

    report = check_status(REPO_ROOT)

    if args.json:
        print(json.dumps(asdict(report), indent=2))
    else:
        print(f"continuity root: {report.continuity_root}")
        print(f"STATUS.md: {'ok' if report.status_exists else 'missing'}")
        print(f"last entry: {report.last_entry_date} anchor={'ok' if report.last_entry_anchor_found else 'fail'}")
        for w in report.warnings:
            print(f"warn: {w}", file=sys.stderr)
        for e in report.errors:
            print(f"error: {e}", file=sys.stderr)

    issues = list(report.errors)
    if args.strict:
        issues.extend(report.warnings)
    return 1 if issues else 0

if __name__ == "__main__":
    raise SystemExit(main())
