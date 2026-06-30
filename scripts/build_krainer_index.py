#!/usr/bin/env python3
"""Rebuild statecraft/voices/krainer/krainer-index.md from archive Krainer captures."""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ARCHIVE = REPO / "source-archive" / "statecraft"
OUT = REPO / "statecraft" / "voices" / "krainer" / "krainer-index.md"
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
    r"^(?:alex\s+)?krainer:\s*",
    re.I,
)

HOST_LABEL: dict[str, str] = {
    "nima": "Dialogue Works × Krainer",
    "diesen": "Diesen × Krainer",
    "multi_wilkerson": "DW × Krainer × Wilkerson",
    "multi_martyanov": "DW × Martyanov × Krainer",
    "multi_escobar": "DW × Escobar × Martyanov × Krainer",
    "other": "Krainer",
}

MAY_HINGE_FN = "source-diesen-krainer-hormuz-multipolar-world-order-2026-05-08.md"

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

def host_bucket(path: Path, meta: dict) -> str:
    name = path.name.casefold()
    if "glenn-diesen" in name or name.startswith("source-diesen-krainer"):
        return "diesen"
    if "dialogue-works" in name:
        if "wilkerson" in name:
            return "multi_wilkerson"
        if "escobar" in name or "pepe-escobar" in name:
            return "multi_escobar"
        if "martyanov" in name:
            return "multi_martyanov"
        return "nima"
    host = (meta.get("host") or "").casefold()
    show = (meta.get("show") or "").casefold()
    slug = (meta.get("channel_slug") or "").casefold()
    if "glenn diesen" in host or slug == "glenn-diesen":
        return "diesen"
    if "dialogue works" in show or slug == "dialogue-works":
        return "nima"
    return "other"

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
    bucket = host_bucket(path, meta)
    host = HOST_LABEL.get(bucket, HOST_LABEL["other"])
    return f"{pub} | {host} | {short_title(meta, path)}"

def row_label(meta: dict, path: Path, labels: dict[str, str]) -> str:
    text = labels.get(path.name) or default_label(meta, path)
    rel = f"../../../source-archive/statecraft/{path.parent.name}/{path.name}"
    return f"- [{text}]({rel})"

def collect_rows() -> list[tuple[str, Path, dict]]:
    rows: list[tuple[str, Path, dict]] = []
    for path in iter_archive_captures_for_shelf("krainer", ARCHIVE):
        meta = parse_head(path)
        body = path.read_text(encoding="utf-8")[:8000]
        if shelf_utils.shelf_capture_excluded("krainer", path, meta, body):
            continue
        pub = pub_date_key(meta, path)
        rows.append((pub, path, meta))
    rows.sort(key=lambda t: (t[0], t[1].name))
    return rows

def month_heading(month: str) -> str:
    return f"## {month}"

def render_month_section(
    month: str,
    section_rows: list[tuple[str, Path, dict]],
    labels: dict[str, str],
    annotations: dict[str, str],
) -> list[str]:
    if not section_rows:
        return []
    lines = [month_heading(month), ""]
    if month == "2026-05" and any(r[1].name == MAY_HINGE_FN for r in section_rows):
        lines.extend(
            [
                "**May hinge (Diesen × Krainer — Hormuz / multipolar order — 2026-05-08):**",
                "",
            ]
        )
        for _pub, path, meta in section_rows:
            if path.name == MAY_HINGE_FN:
                line = row_label(meta, path, labels)
                ann = annotations.get(path.name)
                if ann:
                    line += f" {ann}"
                lines.append(line)
                lines.append("")
                break
        other = [r for r in section_rows if r[1].name != MAY_HINGE_FN]
        if other:
            lines.append("**Other May anchors:**")
            lines.append("")
            for _pub, path, meta in sorted(other, reverse=True):
                line = row_label(meta, path, labels)
                ann = annotations.get(path.name)
                if ann:
                    line += f" {ann}"
                lines.append(line)
            lines.append("")
    else:
        for _pub, path, meta in sorted(section_rows, reverse=True):
            line = row_label(meta, path, labels)
            ann = annotations.get(path.name)
            if ann:
                line += f" {ann}"
            lines.append(line)
        lines.append("")
    return lines

def render_curated_overlays() -> list[str]:
    return [
        "## Host routing",
        "",
        "| Host | Index |",
        "| --- | --- |",
        "| Dialogue Works / Alkorshid | [dialogue-works host](../../channels/dialogue-works/index.md) · [dialogue-works-channel-index](../../channels/dialogue-works/dialogue-works-channel-index.md) |",
        "| Glenn Diesen | guest: [diesen index](../diesen/diesen-index.md) · host arc: [arc-krainer-diesen-host](../../notes/arc-krainer-diesen-host.md) · host channel: [glenn-diesen-channel-index](../../channels/glenn-diesen/glenn-diesen-channel-index.md) |",
        "| The Duran | [the-duran channel-index](../../channels/the-duran/the-duran-channel-index.md) — search receipts in [krainer-cross-host-note.md](krainer-cross-host-note.md); not yet dense on disk |",
        "",
        "## Reading rule",
        "",
        "1. Open **Statecraft Archive** direct files first.",
        "2. Treat Krainer as **macro-financial / imperial-breakdown widening** — sanctions stress, commodity shock, elite decay, world-order transition; not mechanism-first destruction (→ [Postol](../postol/postol-index.md)) or Moscow military contrarian (→ [Krapivnik](../krapivnik/krapivnik-index.md)).",
        "3. **Diesen-side** branch is the clearest mature host-local form; Dialogue Works reinforces the same object across crisis cycles.",
        "",
        "## Boundary notes",
        "",
        "- Object doctrine: [krainer-speaker-object.md](krainer-speaker-object.md) · cross-host reinforcement: [krainer-cross-host-note.md](krainer-cross-host-note.md)",
        "- No `krainer-profile.md` yet — shelf is **speaker-object + index** until profile warrants split.",
        "- **DW search receipts** (2025-12-25 → 2026-05-14) in cross-host note are **not** all mirrored — intake backlog, not index parity gaps.",
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

    nima_n = sum(
        1
        for r in rows
        if host_bucket(r[1], r[2]) in ("nima", "multi_wilkerson", "multi_martyanov", "multi_escobar")
    )
    diesen_n = sum(1 for r in rows if host_bucket(r[1], r[2]) == "diesen")

    lines = [
        "# Krainer source index",
        "",
                "",
        "Purpose: canonical statecraft-side source index for **Alex Krainer** while raw-text authority stays in the Statecraft Archive.",
        "",
        "**Audit:** `python scripts/audit_statecraft_archive_index.py --shelf-index krainer` — author/guest parity; skill **`audit index`**. (_Curated rebuild via builder — no `--fix`._)",
        "",
        "## Surface Grammar",
        "",
        "- **Surface name:** `krainer-source-index.md`",
        "- **Surface role:** source bench for breadth-first Krainer retrieval",
        "- **Surface interior:** materialized guest appearances across Dialogue Works and Glenn Diesen (cross-host reinforced object)",
        "",
        "**Identity / object hub:** [krainer-speaker-object.md](krainer-speaker-object.md)",
        "",
        "## Corpus note",
        "",
        f"- **{len(rows)}** eligible archive captures on disk ({date_span})",
        "- Rebuild: `python scripts/build_krainer_index.py`",
        f"- **{nima_n}** Dialogue Works (incl. multi-guest panels) · **{diesen_n}** Diesen",
        "- **`thread: krainer`** on new lands when operator sets guest thread; filename token `krainer` matches legacy rows",
        "",
    ]

    for month in sorted(by_month, reverse=True):
        lines.extend(render_month_section(month, by_month[month], labels, annotations))

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
