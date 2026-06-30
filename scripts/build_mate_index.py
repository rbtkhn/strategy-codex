#!/usr/bin/env python3
"""Rebuild statecraft/voices/mate/mate-index.md from archive Maté captures."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ARCHIVE = REPO / "source-archive" / "statecraft"
OUT = REPO / "statecraft" / "voices" / "mate" / "mate-index.md"
_SCRIPTS = REPO / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import shelf_index_utils as shelf_utils  # noqa: E402
from audit_statecraft_archive_index import iter_archive_captures_for_shelf  # noqa: E402
from statecraft_day_archive import read_text  # noqa: E402

LINK_SUFFIX_RE = re.compile(
    r"\]\((?:\.\./\.\./\.\./source-archive/statecraft/\d{4}-\d{2}-\d{2}/([^)]+))\)(.*)$"
)
LABEL_RE = re.compile(r"- \[([^\]]+)\]\([^)]*/([^/)]+)\)")

def parse_head(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")[:5000]
    out: dict = {}
    for key in ("title", "pub_date", "date", "host", "show", "thread", "guest"):
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
    return day if re.match(r"^\d{4}-\d{2}-\d{2}$", day) else day

def short_title(meta: dict, path: Path) -> str:
    title = (meta.get("title") or "").strip()
    if not title:
        title = path.stem.removeprefix("source-").replace("-", " ")
    if len(title) > 72:
        title = title[:69] + "…"
    return title

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

def load_preserved_tail(index_path: Path, marker: str) -> str:
    if not index_path.is_file():
        return ""
    text = read_text(index_path)
    pos = text.find(marker)
    if pos < 0:
        return ""
    return text[pos:].rstrip() + "\n"

def collect_rows() -> list[tuple[str, Path, dict]]:
    rows: list[tuple[str, Path, dict]] = []
    for path in iter_archive_captures_for_shelf("mate", ARCHIVE):
        meta = parse_head(path)
        body = path.read_text(encoding="utf-8")[:8000]
        if shelf_utils.shelf_capture_excluded("mate", path, meta, body):
            continue
        rows.append((pub_date_key(meta, path), path, meta))
    rows.sort(key=lambda t: (t[0], t[1].name))
    return rows

def row_label(meta: dict, path: Path, labels: dict[str, str], annotations: dict[str, str]) -> str:
    pub = pub_date_key(meta, path)
    text = labels.get(path.name) or f"{pub} — {short_title(meta, path)}"
    rel = f"../../../source-archive/statecraft/{path.parent.name}/{path.name}"
    line = f"- [{text}]({rel})"
    ann = annotations.get(path.name)
    if ann:
        line += f" {ann}"
    return line

def render_index(rows: list[tuple[str, Path, dict]], labels: dict[str, str], annotations: dict[str, str], tail: str) -> str:
    by_month: dict[str, list[tuple[str, Path, dict]]] = {}
    for row in rows:
        month = row[0][:7] if len(row[0]) >= 7 else row[0]
        by_month.setdefault(month, []).append(row)

    lines = [
                "",
        "# Maté source index",
        "",
        "Purpose: canonical route map for materialized **Aaron Maté** guest appearances in **Statecraft Archive** (Judging Freedom lane).",
        "",
        "## Corpus note",
        "",
        f"- **{len(rows)}** direct captures on disk",
        "- Host: **Judging Freedom / Judge Andrew Napolitano** (sole materialized lane)",
        "- Register: Israel-first / AIPAC accountability · Iran war deception · MOU-as-pause · domestic-politics spillover (NYC primaries)",
        "- Rebuild: `python scripts/build_mate_index.py`",
        "",
        "## Materialized appearances",
        "",
        "### Judging Freedom × Maté",
        "",
    ]
    for month in sorted(by_month, reverse=True):
        lines.append(f"#### {month}")
        lines.append("")
        for _pub, path, meta in by_month[month]:
            lines.append(row_label(meta, path, labels, annotations))
        lines.append("")

    if tail:
        lines.append(tail.rstrip())
        lines.append("")
    return "\n".join(lines)

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    rows = collect_rows()
    labels = load_label_map(OUT)
    annotations = load_annotation_map(OUT)
    tail = load_preserved_tail(OUT, "## Open first")
    body = render_index(rows, labels, annotations, tail)

    if args.check:
        print(f"rows: {len(rows)} labels: {len(labels)} annotations: {len(annotations)}")
        return 0

    OUT.write_text(body if body.endswith("\n") else body + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {OUT} ({len(rows)} rows, {len(labels)} labels preserved)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
