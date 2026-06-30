#!/usr/bin/env python3
"""Build derived continuity-layer observability report (non-authoritative)."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from check_continuity_status import check_status  # noqa: E402
from continuity_paths import continuity_root  # noqa: E402

OUT_JSON = REPO_ROOT / "runtime" / "artifacts" / "continuity-report.json"
OUT_MD = REPO_ROOT / "runtime" / "artifacts" / "continuity-report.md"

RE_CHAPTER = re.compile(r"chapters/(\d{4}-\d{2})")


@dataclass
class ContinuityReport:
    generated: str
    authority: str = "derived — not SSOT; regenerate via build_continuity_report.py"
    continuity_root: str = ""
    active_chapters: list[str] = field(default_factory=list)
    latest_chapter_months: list[str] = field(default_factory=list)
    status_last_substantive: str | None = None
    daily_inbox_exists: bool = False
    daily_inbox_lines: int = 0
    prediction_ledger_exists: bool = False
    prediction_row_count: int | None = None
    stale_status_warning: bool = False
    status_errors: list[str] = field(default_factory=list)
    compiled_views_note: str = "Compiled views and strategy-console outputs are derived only."
    next_suggested_action: str = ""


def _chapter_months(root: Path) -> list[str]:
    months: list[str] = []
    chapters = root / "chapters"
    if chapters.is_dir():
        for days in chapters.rglob("days.md"):
            rel = days.relative_to(root).as_posix()
            m = RE_CHAPTER.search(rel)
            if m:
                months.append(m.group(1))
    return sorted(set(months))


def _count_prediction_rows(path: Path) -> int | None:
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8")
    # Rough: rows with status open/pending in table
    return len(re.findall(r"\|\s*`pred-[^`]+`", text))


def build_report(repo_root: Path) -> ContinuityReport:
    root = continuity_root(repo_root)
    status = check_status(repo_root)
    report = ContinuityReport(
        generated=date.today().isoformat(),
        continuity_root=root.relative_to(repo_root).as_posix(),
        status_last_substantive=status.last_entry_date,
        daily_inbox_exists=status.inbox_exists,
        prediction_ledger_exists=status.predictions_exists,
        stale_status_warning=bool(status.warnings),
        status_errors=status.errors,
        active_chapters=status.active_chapters,
    )
    inbox = root / "daily-strategy-inbox.md"
    if inbox.is_file():
        report.daily_inbox_lines = len(inbox.read_text(encoding="utf-8").splitlines())
    preds = root / "strategy-expert-predictions.md"
    report.prediction_row_count = _count_prediction_rows(preds)
    report.latest_chapter_months = _chapter_months(root)
    if status.errors:
        report.next_suggested_action = "Fix STATUS.md cross-references (check_continuity_status.py)."
    elif status.warnings:
        report.next_suggested_action = "Review active chapter vs latest month in STATUS.md."
    else:
        report.next_suggested_action = "Continue EOD compose per OPERATING-MODE.md."
    return report


def format_md(report: ContinuityReport) -> str:
    lines = [
        "# Continuity report",
        "",
        f"Generated: {report.generated}",
        "",
        f"**Authority:** {report.authority}",
        "",
        f"- Continuity root: `{report.continuity_root}`",
        f"- Last substantive entry: {report.status_last_substantive}",
        f"- Active chapters: {', '.join(report.active_chapters) or '(none parsed)'}",
        f"- Latest chapter months: {', '.join(report.latest_chapter_months[-5:]) or '(none)'}",
        f"- Daily inbox: {'yes' if report.daily_inbox_exists else 'no'} ({report.daily_inbox_lines} lines)",
        f"- Prediction ledger: {'yes' if report.prediction_ledger_exists else 'no'}",
        f"- Prediction rows: {report.prediction_row_count}",
        f"- Stale status warning: {report.stale_status_warning}",
        "",
        f"**Compiled views:** {report.compiled_views_note}",
        "",
        f"**Suggested next action:** {report.next_suggested_action}",
        "",
    ]
    if report.status_errors:
        lines.append("## Status errors")
        lines.append("")
        for e in report.status_errors:
            lines.append(f"- {e}")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Print JSON to stdout only")
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write runtime/artifacts/continuity-report.{json,md}",
    )
    args = parser.parse_args()

    report = build_report(REPO_ROOT)
    payload = asdict(report)

    if args.write:
        OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
        OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        OUT_MD.write_text(format_md(report), encoding="utf-8")
        if not args.json:
            print(f"Wrote {OUT_JSON.relative_to(REPO_ROOT)}", file=sys.stderr)
            print(f"Wrote {OUT_MD.relative_to(REPO_ROOT)}", file=sys.stderr)

    if args.json:
        print(json.dumps(payload, indent=2))
    elif not args.write:
        print(format_md(report))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
