#!/usr/bin/env python3
"""Compose standalone strategy-page scaffolds for named streams.

The **page** command is the Ship-lane complement to **weave** (Think lane).
New strategy-pages are standalone files in the owning stream folder. Legacy
thread-fenced page insertion remains available behind ``--legacy-thread-fence``
for compatibility with older notebook material.

Usage::

    python3 scripts/strategy_page.py davis barnes
    python3 scripts/strategy_page.py davis barnes --watch hormuz
    python3 scripts/strategy_page.py pape --id zero-sum-hormuz
    python3 scripts/strategy_page.py davis barnes --dry-run

**Refined pages (`experts/<id>/*-page-*.md`):** target **~3000** words, **~70–80%** verbatim; see
`docs/skill-work/work-strategy/strategy-notebook/refined-page-template.md` and
`python3 scripts/strategy/refined_page_word_budget.py check|condense`.

WORK only; not Record.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from strategy_notebook.receipts import (
    NotebookReceipt,
    PageOperation,
    append_receipt,
    rel_posix,
)
from strategy_expert_corpus import (
    CANONICAL_EXPERT_IDS,
    THREAD_MARKER_START,
    _EXPERT_IDS_SET,
    thread_path_for_page_month,
)
from strategy_page_reader import discover_pages

DEFAULT_INBOX = (
    REPO_ROOT
    / "docs/skill-work/work-strategy/strategy-notebook/daily-strategy-inbox.md"
)
DEFAULT_NOTEBOOK = (
    REPO_ROOT / "codex"
)

PAGE_MARKER_START = '<!-- strategy-page:start id="{id}" date="{date}" watch="{watch}" -->'
PAGE_MARKER_END = "<!-- strategy-page:end -->"

_RE_MONTH_H2 = re.compile(r"^##\s+(\d{4}-\d{2})\s*$")


# ---------------------------------------------------------------------------
# Inbox material extraction
# ---------------------------------------------------------------------------

def _gather_inbox_material(
    experts: list[str],
    inbox_path: Path,
) -> list[str]:
    """Extract inbox lines tagged with ``thread:<expert>`` or batch-analysis
    lines referencing any of the named experts."""
    if not inbox_path.is_file():
        return []
    text = inbox_path.read_text(encoding="utf-8")
    relevant: list[str] = []
    for line in text.splitlines():
        lower = line.lower()
        for eid in experts:
            if f"thread:{eid}" in lower:
                relevant.append(line.rstrip())
                break
        else:
            if "batch-analysis" in lower:
                for eid in experts:
                    if eid in lower:
                        relevant.append(line.rstrip())
                        break
    return relevant


# ---------------------------------------------------------------------------
# Page block construction
# ---------------------------------------------------------------------------

def build_page_block(
    page_id: str,
    page_date: str,
    watch: str,
    experts: list[str],
    current_expert: str,
    inbox_lines: list[str],
) -> str:
    """Render a page block ready for insertion."""
    also_in = [e for e in experts if e != current_expert]

    marker = PAGE_MARKER_START.format(id=page_id, date=page_date, watch=watch)
    lines = [marker, f"### Page: {page_id}", ""]
    lines.append(f"**Date:** {page_date}")
    if watch:
        lines.append(f"**Watch:** {watch}")
    if also_in:
        lines.append(f"**Also in:** {', '.join(also_in)}")
    lines.append("")

    if inbox_lines:
        lines.append("**Inbox material:**")
        lines.append("")
        for il in inbox_lines[:20]:
            lines.append(il)
        lines.append("")

    lines.append("_(Operator/assistant: refine this page content.)_")
    lines.append(PAGE_MARKER_END)
    return "\n".join(lines)


def _slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def page_path_for_stream(
    notebook_root: Path,
    stream_id: str,
    page_date: str,
    page_id: str,
    *,
    explicit_id: bool,
) -> Path:
    """Return the preferred standalone strategy-page path for a stream."""
    year = page_date[:4]
    stream_slug = _slugify(stream_id)
    stem = f"{stream_slug}-page-{page_date}"
    if explicit_id:
        suffix = _slugify(page_id)
        if suffix and suffix not in {stream_slug, page_date, f"{stream_slug}-{page_date}"}:
            stem = f"{stem}-{suffix}"
    return notebook_root / year / stream_slug / f"{stem}.md"


def build_strategy_page_document(
    *,
    stream_id: str,
    page_date: str,
    page_id: str,
    watch: str,
    streams: list[str],
    inbox_lines: list[str],
) -> str:
    """Render a public-draft standalone strategy-page scaffold."""
    also_in = [e for e in streams if e != stream_id]
    title = page_id.replace("-", " ").strip().title() or f"{stream_id} strategy-page"
    lines = [
        f"# {title}",
        "",
        f"**Date:** {page_date}",
        "**Status:** Draft strategy-page",
        f"**Stream:** {stream_id}",
    ]
    if watch:
        lines.append(f"**Watch:** {watch}")
    if also_in:
        lines.append(f"**Related streams:** {', '.join(also_in)}")
    lines.extend(
        [
            "",
            "### Signal",
            "",
            "- Replace this with the source claim or observation that made the page worth writing. When source text exists, support the bullet with 1-3 full quoted sentences.",
            "",
        ]
    )
    if inbox_lines:
        lines.append("- Candidate source prompts from inbox:")
        for il in inbox_lines[:10]:
            lines.append(f"  - {il}")
        lines.append("")
    lines.extend(
        [
            "### Judgment",
            "",
            "- Replace this with the first argument step. Support major claims with a quote, source fact, or explicit inference.",
            "- Include historical-pattern reasoning in public prose when it sharpens the judgment; do not use backend labels.",
            "",
            "### Prediction",
            "",
            "- **Prediction:** <falsifiable expectation or interpretive claim>",
            "- **Falsifier:** <what would weaken or overturn it>",
            "- **Revisit:** <date, event, or threshold>",
            "",
            "### Sources",
            "",
            "- <source link or receipt>",
            "",
        ]
    )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Thread file insertion
# ---------------------------------------------------------------------------

def insert_page(thread_path: Path, month: str, page_block: str, dry_run: bool) -> str:
    """Insert a page block under ``## YYYY-MM`` in a thread file."""
    if not thread_path.is_file():
        return f"skip (thread file missing): {thread_path}"

    text = thread_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    month_heading = f"## {month}"
    insert_idx: int | None = None

    for i, line in enumerate(lines):
        if line.strip() == month_heading:
            j = i + 1
            while j < len(lines):
                ln = lines[j].strip()
                if ln == THREAD_MARKER_START:
                    insert_idx = j
                    break
                if _RE_MONTH_H2.match(lines[j]):
                    insert_idx = j
                    break
                j += 1
            else:
                insert_idx = len(lines)
            break

    if insert_idx is None:
        if THREAD_MARKER_START in text:
            marker_idx = next(
                i for i, ln in enumerate(lines) if ln.strip() == THREAD_MARKER_START
            )
            new_lines = lines[:marker_idx] + [
                "", month_heading, "", page_block, ""
            ] + lines[marker_idx:]
        else:
            new_lines = lines + ["", month_heading, "", page_block, ""]
    else:
        new_lines = lines[:insert_idx] + [page_block, ""] + lines[insert_idx:]

    label = "would insert" if dry_run else "inserted"
    if not dry_run:
        thread_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    return f"{label} page '{month_heading}' in {thread_path}"


def write_standalone_page(path: Path, content: str, dry_run: bool) -> str:
    label = "would write" if dry_run else "wrote"
    if not dry_run:
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            return f"skip (strategy-page already exists): {path}"
        path.write_text(content, encoding="utf-8")
    return f"{label} standalone strategy-page: {path}"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "experts",
        nargs="+",
        help="Expert IDs to include in this page",
    )
    ap.add_argument("--watch", default="", help="Watch tag for this page")
    ap.add_argument("--id", dest="page_id", default="", help="Explicit page slug")
    ap.add_argument(
        "--date",
        default="",
        help="Page date (YYYY-MM-DD); defaults to today",
    )
    ap.add_argument("--inbox", type=Path, default=DEFAULT_INBOX)
    ap.add_argument("--notebook", type=Path, default=DEFAULT_NOTEBOOK)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument(
        "--legacy-thread-fence",
        action="store_true",
        help="Use the old thread-fenced strategy-page insertion path.",
    )
    ap.add_argument(
        "--operation",
        choices=[e.value for e in PageOperation],
        default=PageOperation.APPEND.value,
        help="Declared page operation for receipts (default: APPEND for new scaffolds)",
    )
    ap.add_argument(
        "--no-receipt",
        action="store_true",
        help="Do not append a line to strategy notebook receipts JSONL",
    )
    args = ap.parse_args()

    expert_ids = [e.lower().strip() for e in args.experts]
    for eid in expert_ids:
        if eid not in _EXPERT_IDS_SET:
            print(f"error: unknown expert ID: {eid}", file=sys.stderr)
            print(f"valid IDs: {', '.join(CANONICAL_EXPERT_IDS)}", file=sys.stderr)
            return 1

    page_date = args.date or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    month = page_date[:7]

    if args.page_id:
        page_id = args.page_id
    else:
        page_id = "-".join(expert_ids) + "-" + page_date

    inbox_lines = _gather_inbox_material(expert_ids, args.inbox)

    sources_read: list[str] = []
    if args.inbox.is_file():
        sources_read.append(rel_posix(REPO_ROOT, args.inbox.resolve()))
    outputs_touched: list[str] = []
    for eid in expert_ids:
        if args.legacy_thread_fence:
            page_block = build_page_block(
                page_id=page_id,
                page_date=page_date,
                watch=args.watch,
                experts=expert_ids,
                current_expert=eid,
                inbox_lines=inbox_lines,
            )
            thread_path = thread_path_for_page_month(args.notebook, eid, month)
            thread_path = thread_path.resolve()
            sources_read.append(rel_posix(REPO_ROOT, thread_path))
            result = insert_page(thread_path, month, page_block, args.dry_run)
            if not args.dry_run:
                outputs_touched.append(rel_posix(REPO_ROOT, thread_path))
        else:
            page_path = page_path_for_stream(
                args.notebook.resolve(),
                eid,
                page_date,
                page_id,
                explicit_id=bool(args.page_id),
            )
            content = build_strategy_page_document(
                stream_id=eid,
                page_date=page_date,
                page_id=page_id,
                watch=args.watch,
                streams=expert_ids,
                inbox_lines=inbox_lines,
            )
            result = write_standalone_page(page_path, content, args.dry_run)
            if not args.dry_run and page_path.exists():
                outputs_touched.append(rel_posix(REPO_ROOT, page_path))
        print(f"  {result}")

    if args.dry_run:
        print(f"\nDry run: strategy-page '{page_id}' for {', '.join(expert_ids)} (not written)")
    else:
        print(f"\nCreated strategy-page '{page_id}' for {', '.join(expert_ids)}")

    if not args.no_receipt:
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        status = "dry_run" if args.dry_run else "ok"
        rec = NotebookReceipt(
            ts=ts,
            entrypoint="strategy_page",
            page_operation=args.operation,
            status=status,
            sources_read=sorted(set(sources_read)),
            outputs_touched=outputs_touched,
            decision=(
                "dry-run new strategy-page scaffolds (not written)"
                if args.dry_run
                else (
                    "inserted legacy thread-fenced strategy-page scaffolds"
                    if args.legacy_thread_fence
                    else "wrote standalone strategy-page scaffolds"
                )
            ),
            details={
                "page_id": page_id,
                "expert_ids": ",".join(expert_ids),
                "watch": args.watch or "",
                "month": month,
            },
        )
        log = append_receipt(REPO_ROOT, rec)
        print(f"receipt: {log.relative_to(REPO_ROOT)}", flush=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
