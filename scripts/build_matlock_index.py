#!/usr/bin/env python3
"""Rebuild statecraft/voices/matlock/matlock-index.md from archive Matlock captures."""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ARCHIVE = REPO / "source-archive" / "statecraft"
OUT = REPO / "statecraft" / "voices" / "matlock" / "matlock-index.md"
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

GUEST_PREFIX_RE = re.compile(
    r"^(?:jack\s+)?matlock:\s*",
    re.I,
)

ANCHOR_FN = (
    "source-diesen-matlock-how-nato-expansionism-broke-european-security-2026-04-19.md"
)

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
        "guest",
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

def short_title(meta: dict, path: Path) -> str:
    title = (meta.get("title") or "").strip()
    title = GUEST_PREFIX_RE.sub("", title).strip()
    if not title:
        title = path.stem.removeprefix("source-").replace("-", " ")
    if len(title) > 88:
        title = title[:85] + "…"
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

def default_label(meta: dict, path: Path) -> str:
    pub = pub_date_key(meta, path)
    return f"{pub} | Diesen × Matlock | {short_title(meta, path)}"

def row_label(meta: dict, path: Path, labels: dict[str, str], annotations: dict[str, str]) -> str:
    text = labels.get(path.name) or default_label(meta, path)
    rel = f"../../../source-archive/statecraft/{path.parent.name}/{path.name}"
    line = f"- [{text}]({rel})"
    ann = annotations.get(path.name)
    if ann:
        line += f" {ann}"
    return line

def collect_rows() -> list[tuple[str, Path, dict]]:
    rows: list[tuple[str, Path, dict]] = []
    for path in iter_archive_captures_for_shelf("matlock", ARCHIVE):
        meta = parse_head(path)
        body = path.read_text(encoding="utf-8")[:8000]
        if shelf_utils.shelf_capture_excluded("matlock", path, meta, body):
            continue
        pub = pub_date_key(meta, path)
        rows.append((pub, path, meta))
    rows.sort(key=lambda t: (t[0], t[1].name))
    return rows

def render_curated_overlays() -> list[str]:
    return [
        "## Host routing",
        "",
        "| Host | Index |",
        "| --- | --- |",
        "| Glenn Diesen | [arc-matlock-diesen-host](../../notes/arc-matlock-diesen-host.md) · [diesen-matlock-speaker-arc](../diesen/diesen-matlock-speaker-arc.md) · [glenn-diesen-channel-index](../../channels/glenn-diesen/glenn-diesen-channel-index.md) |",
        "",
        "## Reading rule",
        "",
        "1. Open **Statecraft Archive** direct files first.",
        "2. Treat Matlock as **U.S. diplomatic-memory witness** — Reagan/Bush negotiation method, NATO expansion dispute, lost European security settlement; not live military analysis.",
        "3. Mentions in Freeman, Sachs, McGovern, Johnson lanes are **reinforcement** — not Matlock appearances (see [matlock-speaker-object.md](matlock-speaker-object.md)).",
        "",
        "## Intake backlog (not parity gaps yet)",
        "",
        "Speaker-object cites additional **2025** Diesen × Matlock episodes via day-index / diesen arc — not yet mirrored as `source-*matlock*` captures:",
        "",
        "- [2025-03-27 day-index](../../../source-archive/statecraft/2025-03-27/day-index.md)",
        "- [2025-06-21 day-index](../../../source-archive/statecraft/2025-06-21/day-index.md)",
        "- [2025-09-01 diesen-matlock-speaker-arc](../diesen/diesen-matlock-speaker-arc.md)",
        "- [2025-12-10 day-index](../../../source-archive/statecraft/2025-12-10/day-index.md)",
        "",
        "## Boundary notes",
        "",
        "- Object doctrine: [matlock-speaker-object.md](matlock-speaker-object.md) · [README.md](README.md)",
        "- **Single-helix** Diesen branch only on disk until further captures land.",
        "",
    ]

def render_index(
    rows: list[tuple[str, Path, dict]],
    labels: dict[str, str],
    annotations: dict[str, str],
) -> str:
    date_span = f"{rows[0][0]} → {rows[-1][0]}" if rows else "—"
    by_month: dict[str, list[tuple[str, Path, dict]]] = defaultdict(list)
    for row in rows:
        pub = row[0]
        month = pub[:7] if len(pub) >= 7 else pub
        by_month[month].append(row)

    lines = [
        "# Matlock source index",
        "",
                "",
        "Purpose: canonical statecraft-side source index for **Jack Matlock** while raw-text authority stays in the Statecraft Archive.",
        "",
        "**Audit:** `python scripts/audit_statecraft_archive_index.py --shelf-index matlock` — author/guest parity; skill **`audit index`**. (_Curated rebuild via builder — no `--fix`._)",
        "",
        "## Surface Grammar",
        "",
        "- **Surface name:** `matlock-source-index.md`",
        "- **Surface role:** source bench for breadth-first Matlock retrieval",
        "- **Surface interior:** Diesen-anchored diplomatic-memory guest appearances",
        "",
        "**Identity / object hub:** [matlock-speaker-object.md](matlock-speaker-object.md)",
        "",
        "## Corpus note",
        "",
        f"- **{len(rows)}** eligible archive capture(s) on disk ({date_span})",
        "- Rebuild: `python scripts/build_matlock_index.py`",
        "- **2025 Diesen run** partially cited in object/README — intake backlog until `source-*matlock*` lands",
        "- **`thread: matlock`** on new lands; filename token `matlock` matches legacy rows",
        "",
    ]

    for month in sorted(by_month, reverse=True):
        lines.append(f"## {month}")
        lines.append("")
        if any(r[1].name == ANCHOR_FN for r in by_month[month]):
            lines.append("**April anchor (Diesen × Matlock — NATO expansion / European security — 2026-04-19):**")
            lines.append("")
        for _pub, path, meta in sorted(by_month[month], key=lambda t: (t[0], t[1].name)):
            lines.append(row_label(meta, path, labels, annotations))
        lines.append("")

    lines.extend(render_curated_overlays())
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

    labels = load_label_map(OUT)
    annotations = load_annotation_map(OUT)
    body = render_index(rows, labels, annotations)
    if args.check:
        print(f"rows: {len(rows)}")
        print(f"labels preserved: {len(labels)}")
        print(f"annotations preserved: {len(annotations)}")
        return 0

    OUT.write_text(body if body.endswith("\n") else body + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {OUT} ({len(rows)} rows, {len(labels)} labels preserved)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
