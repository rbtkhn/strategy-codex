#!/usr/bin/env python3
"""Rebuild statecraft/voices/crooke/crooke-index.md from archive Crooke captures."""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ARCHIVE = REPO / "source-archive" / "statecraft"
OUT = REPO / "statecraft" / "voices" / "crooke" / "crooke-index.md"
_SCRIPTS = REPO / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import shelf_index_utils as shelf_utils  # noqa: E402
from audit_statecraft_archive_index import iter_archive_captures_for_shelf  # noqa: E402
from statecraft_day_archive import read_text  # noqa: E402

LINK_SUFFIX_RE = re.compile(
    r"\]\((?:\.\./\.\./\.\./source-archive/statecraft/\d{4}-\d{2}-\d{2}/([^)]+))\)(.*)$"
)
LABEL_RE = re.compile(
    r"- \[([^\]]+)\]\([^)]*/([^/)]+)\)"
)
MONTH_HEADING_RE = re.compile(r"^## (\d{4}-\d{2})$")
SHORTHAND_LABEL_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-")

BOUNDARY_TAIL = """## Source-boundary reminders

- Crooke-authored Substack captures belong here and feed the authored forecast ledger.
- Host-owned appearances belong here even when the interview support spine or host-local arcs carry the first-open interpretive job.
- Shorthand captures such as `2026-04-25-davis` and `2026-04-27-diesen` can remain visible as support-tier provenance without becoming best-entry speaker evidence.
- Compatibility or workshop scaffolds outside this file do not override raw-input truth.
"""


def parse_head(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")[:5000]
    out: dict = {}
    for key in (
        "title",
        "pub_date",
        "date",
        "kind",
        "source_form",
        "host",
        "show",
        "channel_slug",
        "thread",
        "author",
    ):
        m = re.search(rf"^{key}:\s*(.+)$", text, re.M)
        if m:
            out[key] = m.group(1).strip().strip('"').strip("'")
    if not out.get("title"):
        hm = re.search(r"^#\s+(.+)$", text, re.M)
        if hm:
            out["title"] = hm.group(1).strip()
    return out


def pub_date_key(meta: dict, path: Path) -> str:
    pub = meta.get("pub_date") or meta.get("date") or ""
    if pub and len(pub) >= 10:
        return pub[:10]
    day = path.parent.name
    if re.match(r"^\d{4}-\d{2}-\d{2}$", day):
        return day
    return day


def load_header(index_path: Path) -> str:
    if not index_path.is_file():
        return (
            "# Crooke Source Index\n\n"
            "WORK only; not Record.\n\n"
            "Purpose: exhaustive route map for Crooke appearances in the archive.\n"
        )
    lines: list[str] = []
    for line in read_text(index_path).splitlines():
        if MONTH_HEADING_RE.match(line):
            break
        lines.append(line)
    return "\n".join(lines).rstrip()


def load_label_map(index_path: Path) -> dict[str, str]:
    if not index_path.is_file():
        return {}
    out: dict[str, str] = {}
    for line in read_text(index_path).splitlines():
        m = LABEL_RE.search(line)
        if not m:
            continue
        fn = m.group(2)
        if len(m.group(1)) > len(out.get(fn, "")):
            out[fn] = m.group(1)
    return out


def load_annotation_map(index_path: Path) -> dict[str, str]:
    if not index_path.is_file():
        return {}
    out: dict[str, str] = {}
    for line in read_text(index_path).splitlines():
        m = LINK_SUFFIX_RE.search(line)
        if not m:
            continue
        suffix = m.group(2).strip()
        if not suffix.startswith("—"):
            continue
        fn = m.group(1)
        if len(suffix) > len(out.get(fn, "")):
            out[fn] = suffix
    return out


def load_shorthand_by_target(index_path: Path) -> dict[str, list[str]]:
    """Preserve support-tier alias rows (e.g. 2026-04-25-davis) keyed by target filename."""
    if not index_path.is_file():
        return {}
    out: dict[str, list[str]] = defaultdict(list)
    in_boundary = False
    for line in read_text(index_path).splitlines():
        if line.startswith("## Source-boundary reminders"):
            in_boundary = True
            continue
        if in_boundary:
            continue
        m = LABEL_RE.search(line)
        if not m:
            continue
        label, fn = m.group(1), m.group(2)
        if SHORTHAND_LABEL_RE.match(label):
            out[fn].append(line)
    return dict(out)


def default_label(meta: dict, path: Path) -> str:
    stem = path.stem.removeprefix("source-")
    if path.name.startswith("source-crooke-"):
        return f"substack-crooke-{stem.removeprefix('crooke-')}"
    return stem


def row_label(meta: dict, path: Path, labels: dict[str, str]) -> str:
    text = labels.get(path.name) or default_label(meta, path)
    rel = f"../../../source-archive/statecraft/{path.parent.name}/{path.name}"
    return f"- [{text}]({rel})"


def collect_rows() -> list[tuple[str, Path, dict]]:
    rows: list[tuple[str, Path, dict]] = []
    for path in iter_archive_captures_for_shelf("crooke", ARCHIVE):
        meta = parse_head(path)
        body = path.read_text(encoding="utf-8")[:8000]
        if shelf_utils.shelf_capture_excluded("crooke", path, meta, body):
            continue
        pub = pub_date_key(meta, path)
        rows.append((pub, path, meta))
    rows.sort(key=lambda t: (t[0], t[1].name))
    return rows


def render_month_section(
    month: str,
    month_rows: list[tuple[str, Path, dict]],
    labels: dict[str, str],
    annotations: dict[str, str],
    shorthands_by_target: dict[str, list[str]],
) -> list[str]:
    lines = [f"## {month}", ""]
    for _pub, path, meta in month_rows:
        line = row_label(meta, path, labels)
        ann = annotations.get(path.name)
        if ann:
            line += f" {ann}"
        lines.append(line)
        for sh_line in shorthands_by_target.get(path.name, []):
            lines.append(sh_line)
    lines.append("")
    return lines


def render_index(
    rows: list[tuple[str, Path, dict]],
    header: str,
    labels: dict[str, str],
    annotations: dict[str, str],
    shorthands_by_target: dict[str, list[str]],
) -> str:
    by_month: dict[str, list[tuple[str, Path, dict]]] = defaultdict(list)
    for pub, path, meta in rows:
        by_month[pub[:7]].append((pub, path, meta))

    lines = [header.rstrip(), ""]
    for month in sorted(by_month):
        month_rows = sorted(by_month[month], key=lambda t: (t[0], t[1].name))
        lines.extend(
            render_month_section(
                month, month_rows, labels, annotations, shorthands_by_target
            )
        )
    lines.append(BOUNDARY_TAIL.rstrip())
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Print row count only")
    parser.add_argument("--check", action="store_true", help="Compare row count to index links")
    args = parser.parse_args()

    rows = collect_rows()
    if args.dry_run:
        print(f"rows: {len(rows)}")
        return 0

    header = load_header(OUT)
    labels = load_label_map(OUT)
    annotations = load_annotation_map(OUT)
    shorthands = load_shorthand_by_target(OUT)
    body = render_index(rows, header, labels, annotations, shorthands)
    if args.check:
        print(f"rows: {len(rows)}")
        print(f"labels preserved: {len(labels)}")
        print(f"annotations preserved: {len(annotations)}")
        print(f"shorthand aliases: {sum(len(v) for v in shorthands.values())}")
        return 0

    OUT.write_text(body if body.endswith("\n") else body + "\n", encoding="utf-8", newline="\n")
    print(
        f"wrote {OUT} ({len(rows)} rows, {len(labels)} labels, "
        f"{sum(len(v) for v in shorthands.values())} shorthand aliases preserved)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
