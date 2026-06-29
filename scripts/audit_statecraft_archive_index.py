#!/usr/bin/env python3
"""Audit statecraft archive index surfaces (day → month/year inventory → global navigation).

Usage:
    python scripts/audit_statecraft_archive_index.py --day 2026-06-28
    python scripts/audit_statecraft_archive_index.py --day 2026-06-28 --table
    python scripts/audit_statecraft_archive_index.py --month 2026-06 --table-only
    python scripts/audit_statecraft_archive_index.py --global
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Literal

REPO_ROOT = Path(__file__).resolve().parents[1]
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import build_statecraft_archive_navigation as nav  # noqa: E402
import build_statecraft_day_indices as day_idx  # noqa: E402
from quantify_section_nav import extract_transcript  # noqa: E402
from statecraft_day_archive import (  # noqa: E402
    DAY_INDEX_FILENAME,
    DEFAULT_ROOT,
    build_day_index,
    build_day_readme_stub,
    classify_day_captures,
    is_youtube_capture,
    iter_day_dirs,
    iter_source_files,
    norm_scalar,
    parse_day_readme,
    parse_frontmatter,
    read_text,
    summarize_day_dir,
)

Bucket = Literal["channel", "writer", "other"]
SortKey = Literal["date", "words", "title", "bucket"]

DEFAULT_MONTH_YEAR_TABLE_LIMIT = 50


@dataclass(frozen=True)
class InventoryRow:
    day_folder: str
    pub_date: str
    filename: str
    title: str
    source_url: str
    words: int
    bucket: Bucket
    kind: str
    sections: int | None

    def sort_date(self) -> str:
        return self.pub_date or self.day_folder


@dataclass
class AuditFinding:
    level: Literal["pass", "fail", "warn"]
    code: str
    message: str


def word_count_capture(path: Path) -> int:
    text = read_text(path)
    body = text.split("---", 2)[2] if text.startswith("---") else text
    transcript = extract_transcript(body)
    return len(re.findall(r"\b\w+\b", transcript))


def section_count_capture(path: Path, meta: dict[str, Any]) -> int | None:
    curation = norm_scalar(meta.get("transcript_curation"))
    if curation != "curated_sectioned":
        return None
    text = read_text(path)
    body = text.split("---", 2)[2] if text.startswith("---") else text
    transcript = extract_transcript(body)
    count = len(re.findall(r"^### .+$", transcript, re.MULTILINE))
    return count if count else None


def inventory_row_for_capture(path: Path, day_dir: Path) -> InventoryRow:
    meta = parse_frontmatter(path)
    record_bucket: Bucket = "other"
    for entry in classify_day_captures(day_dir):
        if entry.path == path:
            record_bucket = entry.bucket
            break
    title = norm_scalar(meta.get("title")) or path.stem.removeprefix("source-")
    pub_date = norm_scalar(meta.get("pub_date")) or day_dir.name
    kind = norm_scalar(meta.get("kind")) or norm_scalar(meta.get("source_form")) or "—"
    url = norm_scalar(meta.get("source_url")) or "—"
    return InventoryRow(
        day_folder=day_dir.name,
        pub_date=pub_date,
        filename=path.name,
        title=title,
        source_url=url,
        words=word_count_capture(path),
        bucket=record_bucket,
        kind=kind,
        sections=section_count_capture(path, meta),
    )


def collect_inventory_rows(day_dirs: list[Path]) -> list[InventoryRow]:
    rows: list[InventoryRow] = []
    for day_dir in day_dirs:
        for path in iter_source_files(day_dir):
            rows.append(inventory_row_for_capture(path, day_dir))
    return rows


def sort_inventory_rows(rows: list[InventoryRow], sort_key: SortKey) -> list[InventoryRow]:
    if sort_key == "words":
        return sorted(rows, key=lambda r: (-r.words, r.sort_date(), r.filename))
    if sort_key == "title":
        return sorted(rows, key=lambda r: (r.title.casefold(), r.sort_date(), r.filename))
    if sort_key == "bucket":
        return sorted(rows, key=lambda r: (r.bucket, r.sort_date(), r.filename))
    return sorted(rows, key=lambda r: (r.sort_date(), r.filename))


def apply_table_limit(
    rows: list[InventoryRow],
    limit: int | None,
) -> tuple[list[InventoryRow], int]:
    if limit is None or limit <= 0 or len(rows) <= limit:
        return rows, 0
    return rows[:limit], len(rows) - limit


def default_table_limit(scope: str) -> int | None:
    if scope == "day":
        return None
    return DEFAULT_MONTH_YEAR_TABLE_LIMIT


def capture_hygiene_warnings(path: Path, meta: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    host_scalar = norm_scalar(meta.get("host"))
    host_people = meta.get("host_people")
    if host_scalar and not host_people:
        warnings.append(f"{path.name}: host scalar set but host_people empty")
    thread_scalar = norm_scalar(meta.get("thread"))
    threads = meta.get("threads")
    if thread_scalar and not threads:
        warnings.append(f"{path.name}: thread scalar set but threads empty")
    if is_youtube_capture(meta) and not norm_scalar(meta.get("source_url")):
        warnings.append(f"{path.name}: YouTube capture missing source_url")
    return warnings


def audit_day_dir(day_dir: Path) -> list[AuditFinding]:
    findings: list[AuditFinding] = []
    if not day_dir.is_dir():
        findings.append(AuditFinding("fail", "missing_day", f"day directory not found: {day_dir}"))
        return findings

    disk_files = {p.name for p in iter_source_files(day_dir)}
    index_path = day_dir / DAY_INDEX_FILENAME
    parsed = None
    if not index_path.is_file():
        findings.append(AuditFinding("fail", "missing_index", f"missing {DAY_INDEX_FILENAME}"))
        indexed_files: set[str] = set()
    else:
        parsed = parse_day_readme(day_dir)
        indexed_files = set(parsed.file_names) if parsed else set()
        rendered = build_day_index(day_dir)
        existing = read_text(index_path)
        if existing != rendered:
            findings.append(
                AuditFinding("fail", "stale_index", f"{DAY_INDEX_FILENAME} stale vs recomputed build")
            )
        else:
            findings.append(AuditFinding("pass", "index_fresh", f"{DAY_INDEX_FILENAME} matches builder"))

    if disk_files != indexed_files:
        only_disk = sorted(disk_files - indexed_files)
        only_index = sorted(indexed_files - disk_files)
        parts: list[str] = []
        if only_disk:
            parts.append(f"on disk only: {', '.join(only_disk)}")
        if only_index:
            parts.append(f"in index only: {', '.join(only_index)}")
        findings.append(AuditFinding("fail", "parity", "; ".join(parts)))
    else:
        findings.append(AuditFinding("pass", "parity", f"Files list matches disk ({len(disk_files)} sources)"))

    readme_path = day_dir / "README.md"
    stub_expected = build_day_readme_stub(day_dir)
    if not readme_path.is_file():
        findings.append(AuditFinding("fail", "readme_stub", "README.md missing"))
    else:
        readme_text = read_text(readme_path)
        if readme_text != stub_expected:
            findings.append(AuditFinding("fail", "readme_stub", "README.md not day-index stub"))
        else:
            findings.append(AuditFinding("pass", "readme_stub", "README.md stub ok"))

    if parsed:
        live = summarize_day_dir(day_dir)
        if parsed.source_count != live.source_count:
            findings.append(
                AuditFinding(
                    "warn",
                    "stats_drift",
                    f"index source_count {parsed.source_count} vs live {live.source_count}",
                )
            )

    for path in iter_source_files(day_dir):
        meta = parse_frontmatter(path)
        for msg in capture_hygiene_warnings(path, meta):
            findings.append(AuditFinding("warn", "hygiene", msg))

    return findings


def audit_global(root: Path) -> list[AuditFinding]:
    findings: list[AuditFinding] = []
    import io
    from contextlib import redirect_stdout

    old_argv = sys.argv
    sys.argv = ["build_statecraft_archive_navigation.py", "--root", str(root), "--check"]
    buf = io.StringIO()
    try:
        with redirect_stdout(buf):
            code = nav.main()
    finally:
        sys.argv = old_argv
    output = buf.getvalue().strip()
    if code == 0:
        findings.append(
            AuditFinding("pass", "global_nav", output or "global navigation indices ok")
        )
    else:
        findings.append(
            AuditFinding("fail", "global_nav", output or "global navigation indices stale")
        )
    return findings


def format_findings(scope_label: str, findings: list[AuditFinding]) -> str:
    lines = [f"## Index audit — {scope_label}", ""]
    for level in ("pass", "fail", "warn"):
        bucket = [f for f in findings if f.level == level]
        if not bucket:
            continue
        label = level.upper()
        for item in bucket:
            lines.append(f"{label} [{item.code}] {item.message}")
    fails = sum(1 for f in findings if f.level == "fail")
    lines.append("")
    lines.append(f"exit {'1' if fails else '0'}")
    return "\n".join(lines)


def format_inventory_table(
    scope_label: str,
    rows: list[InventoryRow],
    *,
    truncated: int,
    sort_key: SortKey,
) -> str:
    lines = [
        f"## Index inventory — {scope_label}",
        "",
        f"_Sorted by `{sort_key}`; word count is transcript/body words (not comparable across kinds)._",
        "",
        "| Date | Title | URL | Words | Bucket | Kind | § |",
        "| --- | --- | --- | ---: | --- | --- | ---: |",
    ]
    for row in rows:
        title = row.title.replace("|", "\\|")
        if len(title) > 72:
            title = title[:69] + "..."
        url = row.source_url if row.source_url != "—" else "—"
        if len(url) > 48 and url != "—":
            url = url[:45] + "..."
        sec = str(row.sections) if row.sections is not None else "—"
        lines.append(
            f"| {row.pub_date} | {title} | {url} | {row.words} | {row.bucket} | {row.kind} | {sec} |"
        )
    if truncated:
        lines.append("")
        lines.append(f"_… and {truncated} more row(s); use `--table-limit 0` for full list._")
    lines.append("")
    lines.append(f"rows shown: {len(rows)}")
    return "\n".join(lines)


def resolve_day_dirs(root: Path, args: argparse.Namespace) -> tuple[list[Path], str]:
    if args.day:
        day_dir = root / args.day
        return [day_dir], args.day
    if args.month:
        day_dirs = day_idx.iter_day_dirs_for_scope(root, year=args.month[:4], month=args.month)
        return day_dirs, args.month
    if args.year:
        day_dirs = iter_day_dirs(root, args.year)
        return day_dirs, args.year
    return [], ""


def resolve_scope_name(args: argparse.Namespace) -> str:
    if args.global_audit:
        return "global"
    if args.day:
        return "day"
    if args.month:
        return "month"
    if args.year:
        return "year"
    return ""


def run_fix(root: Path, args: argparse.Namespace, day_dirs: list[Path]) -> None:
    if args.global_audit or args.month or args.year:
        old_argv = sys.argv
        sys.argv = ["build_statecraft_archive_navigation.py", "--root", str(root)]
        try:
            nav.main()
        finally:
            sys.argv = old_argv
    for day_dir in day_dirs:
        if day_dir.is_dir():
            day_idx.write_day_index(day_dir, check=False)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    scope = parser.add_mutually_exclusive_group()
    scope.add_argument("--day", metavar="YYYY-MM-DD", help="Audit one calendar day folder.")
    scope.add_argument("--month", metavar="YYYY-MM", help="Audit each day in month + inventory scope.")
    scope.add_argument("--year", metavar="YYYY", help="Inventory / audit all days in year.")
    scope.add_argument("--global", dest="global_audit", action="store_true", help="Global navigation stale check.")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="Statecraft archive root.")
    parser.add_argument("--table", action="store_true", help="Append inventory table to output.")
    parser.add_argument("--table-only", action="store_true", help="Inventory table only; skip audit checks.")
    parser.add_argument(
        "--table-limit",
        type=int,
        default=None,
        help="Max table rows (0 = unlimited). Default: unlimited for --day, 50 for month/year.",
    )
    parser.add_argument(
        "--table-sort",
        choices=("date", "words", "title", "bucket"),
        default="date",
        help="Inventory row sort (default: date).",
    )
    parser.add_argument("--section", action="store_true", help="Run quantify_section_nav per day (audit mode).")
    parser.add_argument("--daily-sync", metavar="YYYY-MM-DD", help="Run intake vs daily synthesis sync.")
    parser.add_argument("--fix", action="store_true", help="Rebuild stale day-index / global navigation.")
    parser.add_argument("--json", action="store_true", help="JSON receipt.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    root = args.root.resolve()

    if not args.global_audit and not args.day and not args.month and not args.year:
        print("error: specify --day, --month, --year, or --global", file=sys.stderr)
        return 2

    day_dirs, scope_label = resolve_day_dirs(root, args)
    scope_kind = resolve_scope_name(args)

    if args.fix:
        run_fix(root, args, day_dirs)

    findings: list[AuditFinding] = []

    if args.global_audit:
        findings.extend(audit_global(root))
        if not scope_label:
            scope_label = "global navigation"

    if not args.table_only and day_dirs:
        for day_dir in day_dirs:
            findings.extend(audit_day_dir(day_dir))

    if args.section and args.day:
        import quantify_section_nav as qsn

        qsn.main(["--day", args.day])

    if args.daily_sync:
        import check_statecraft_intake_daily_sync as daily_sync

        report = daily_sync.build_sync_report(args.daily_sync.strip(), root=root)
        if report.status == "desync":
            findings.append(
                AuditFinding("fail", "daily_sync", f"daily synthesis desync for {args.daily_sync}")
            )
        elif report.status == "ok":
            findings.append(AuditFinding("pass", "daily_sync", f"daily synthesis ok for {args.daily_sync}"))

    table_rows: list[InventoryRow] = []
    truncated = 0
    if (args.table or args.table_only) and day_dirs:
        all_rows = collect_inventory_rows(day_dirs)
        table_rows = sort_inventory_rows(all_rows, args.table_sort)
        limit = args.table_limit
        if limit is None:
            limit = default_table_limit(scope_kind) if scope_kind else DEFAULT_MONTH_YEAR_TABLE_LIMIT
        table_rows, truncated = apply_table_limit(table_rows, limit)
        if scope_kind == "year" and len(all_rows) > 200:
            findings.append(
                AuditFinding(
                    "warn",
                    "table_large",
                    "year scope exceeds 200 captures; prefer --month or raise --table-limit",
                )
            )

    exit_code = 1 if any(f.level == "fail" for f in findings) else 0

    if args.json:
        payload = {
            "scope": scope_label,
            "exit_code": exit_code,
            "findings": [asdict(f) for f in findings],
            "table": [asdict(r) for r in table_rows],
            "table_truncated": truncated,
            "table_sort": args.table_sort,
        }
        print(json.dumps(payload, indent=2))
        return exit_code

    parts: list[str] = []
    if not args.table_only:
        parts.append(format_findings(scope_label, findings))
    if args.table or args.table_only:
        inv_label = scope_label or "inventory"
        parts.append(format_inventory_table(inv_label, table_rows, truncated=truncated, sort_key=args.table_sort))
    print("\n\n".join(p for p in parts if p))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
