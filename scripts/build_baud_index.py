#!/usr/bin/env python3
"""Rebuild statecraft/voices/baud/baud-index.md from archive Baud captures."""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ARCHIVE = REPO / "source-archive" / "statecraft"
OUT = REPO / "statecraft" / "voices" / "baud" / "baud-index.md"
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
    r"^(?:(?:col\.?|colonel)\s+)?jacques\s+baud:\s*",
    re.I,
)

HOST_LABEL: dict[str, str] = {
    "nima": "Dialogue Works × Baud",
    "davis": "Davis × Baud",
    "diesen": "Diesen × Baud",
    "other": "Baud",
}

LAW_THREAD_FNS = frozenset(
    {
        "source-dialogue-works-col-jacques-baud-the-world-is-entering-a-lawless-era-2026-01-06.md",
        "source-dialogue-works-col-jacques-baud-why-the-eu-is-failing-on-every-front-2026-02-02.md",
        "source-dialogue-works-col-jacques-baud-iran-goes-all-in-this-could-be-the-eu-s-biggest-blunder-yet-2026-02-16.md",
        "source-baud-dialogue-works-nima-2026-04-27.md",
        "source-baud-dialogue-works-nima-2026-05-04.md",
    }
)

MAY_HINGE_FN = "source-dialogue-works-baud-hormuz-security-architecture-2026-05-11.md"
JUNE_HINGE_FN = "source-dialogue-works-baud-us-iran-reach-mou-war-ends-immediately-2026-06-15.md"

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
    if "glenn-diesen" in name or (
        "diesen" in name and "daniel-davis" not in name and "baud" in name
    ):
        return "diesen"
    if "daniel-davis" in name or name.startswith("source-daniel-davis"):
        return "davis"
    if "dialogue-works" in name or name.startswith("source-baud-dialogue"):
        return "nima"
    host = (meta.get("host") or "").casefold()
    show = (meta.get("show") or "").casefold()
    slug = (meta.get("channel_slug") or "").casefold()
    if "glenn diesen" in host or slug == "glenn-diesen":
        return "diesen"
    if "daniel davis" in host or slug == "daniel-davis":
        return "davis"
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

def row_suffix(path: Path, annotations: dict[str, str]) -> str:
    if path.name in annotations:
        return annotations[path.name]
    if path.name in LAW_THREAD_FNS:
        return "— intl-law thread spine"
    return ""

def row_label(meta: dict, path: Path, labels: dict[str, str], annotations: dict[str, str]) -> str:
    text = labels.get(path.name) or default_label(meta, path)
    rel = f"../../../source-archive/statecraft/{path.parent.name}/{path.name}"
    line = f"- [{text}]({rel})"
    suffix = row_suffix(path, annotations)
    if suffix:
        line += f" {suffix}"
    return line

def collect_rows() -> list[tuple[str, Path, dict]]:
    rows: list[tuple[str, Path, dict]] = []
    for path in iter_archive_captures_for_shelf("baud", ARCHIVE):
        meta = parse_head(path)
        body = path.read_text(encoding="utf-8")[:8000]
        if shelf_utils.shelf_capture_excluded("baud", path, meta, body):
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
    hinge_fn = None
    hinge_label = None
    if month == "2026-06" and any(r[1].name == JUNE_HINGE_FN for r in section_rows):
        hinge_fn = JUNE_HINGE_FN
        hinge_label = "**June hinge (DW × Baud — US–Iran MOU / war ends — 2026-06-15):**"
    elif month == "2026-05" and any(r[1].name == MAY_HINGE_FN for r in section_rows):
        hinge_fn = MAY_HINGE_FN
        hinge_label = "**May hinge (DW × Baud — Hormuz security architecture — 2026-05-11):**"
    if hinge_fn and hinge_label:
        lines.extend([hinge_label, ""])
        for _pub, path, meta in section_rows:
            if path.name == hinge_fn:
                lines.append(row_label(meta, path, labels, annotations))
                lines.append("")
                break
        other = [r for r in section_rows if r[1].name != hinge_fn]
        if other:
            lines.append("**Other anchors:**")
            lines.append("")
            for _pub, path, meta in sorted(other, reverse=True):
                lines.append(row_label(meta, path, labels, annotations))
            lines.append("")
    else:
        for _pub, path, meta in sorted(section_rows, reverse=True):
            lines.append(row_label(meta, path, labels, annotations))
        lines.append("")
    return lines

def render_curated_overlays() -> list[str]:
    return [
        "## Orthogonality routing (not replaced by this index)",
        "",
        "Archive parity lives here; interpretation still routes through:",
        "",
        "- [index.md](index.md) — orthogonality front door",
        "- [baud-arc.md](baud-arc.md) — person-level continuity",
        "- [baud-thread-international-law.md](baud-thread-international-law.md) — law-of-war / post-1945 order topical thread",
        "- [baud-helix.md](baud-helix.md) — Davis × DW double-helix comparison",
        "- [baud-cross-year-note.md](baud-cross-year-note.md) — Diesen 2025 branch vs 2026 DW/Davis lanes",
        "",
        "## Host routing",
        "",
        "| Host | Index |",
        "| --- | --- |",
        "| Dialogue Works / Alkorshid | [arc-baud-nima-host](../../notes/arc-baud-nima-host.md) · [dialogue-works-channel-index](../../channels/dialogue-works/dialogue-works-channel-index.md) |",
        "| Daniel Davis | [arc-baud-davis-host](../../notes/arc-baud-davis-host.md) · [daniel-davis-channel-index](../../channels/daniel-davis/daniel-davis-channel-index.md) |",
        "| Glenn Diesen | [arc-baud-diesen-host](../../notes/arc-baud-diesen-host.md) · [glenn-diesen-channel-index](../../channels/glenn-diesen/glenn-diesen-channel-index.md) |",
        "",
        "## Reading rule",
        "",
        "1. Open **Statecraft Archive** direct files first (rows above).",
        "2. Route **legal taxonomy / law-of-war** claims through [baud-thread-international-law.md](baud-thread-international-law.md); **negotiated-order legitimacy** → [Crooke intl-law thread](../crooke/crooke-thread-international-law.md).",
        "3. Pick host arc by pressure: **live crisis** (DW) vs **alliance mandate / coercive feasibility** (Davis) vs **order-transition** (Diesen 2025).",
        "",
        "## Boundary notes",
        "",
        "- [baud-thread.md](baud-thread.md) is legacy compatibility only — not a second canonical topical thread.",
        "- Rows marked **intl-law thread spine** overlap [baud-thread-international-law.md](baud-thread-international-law.md); host arcs may cite subsets without duplicating parity duty here.",
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

    nima_n = sum(1 for r in rows if host_bucket(r[1], r[2]) == "nima")
    davis_n = sum(1 for r in rows if host_bucket(r[1], r[2]) == "davis")
    diesen_n = sum(1 for r in rows if host_bucket(r[1], r[2]) == "diesen")
    law_n = sum(1 for r in rows if r[1].name in LAW_THREAD_FNS)

    lines = [
        "# Baud source index",
        "",
                "",
        "Purpose: canonical **archive parity** bench for **Jacques Baud** while orthogonality routing (arc, helix, topical threads, host arcs) stays in sibling surfaces.",
        "",
        "**Audit:** `python scripts/audit_statecraft_archive_index.py --shelf-index baud` — author/guest parity; skill **`audit index`**. (_Curated rebuild via builder — no `--fix`._)",
        "",
        "## Surface Grammar",
        "",
        "- **Surface name:** `baud-source-index.md` (compat) · **`baud-index.md`** (canonical corpus route map)",
        "- **Surface role:** exhaustive capture index for breadth-first Baud retrieval",
        "- **Orthogonality front door:** [index.md](index.md) — not a substitute for this parity surface",
        "",
        "**Identity / voice hub:** [baud-profile.md](baud-profile.md)",
        "",
        "## Corpus note",
        "",
        f"- **{len(rows)}** eligible archive captures on disk ({date_span})",
        "- Rebuild: `python scripts/build_baud_index.py`",
        f"- **{nima_n}** Dialogue Works · **{davis_n}** Davis · **{diesen_n}** Diesen",
        f"- **{law_n}** rows tagged intl-law thread spine (see [baud-thread-international-law.md](baud-thread-international-law.md))",
        "- **`thread: baud`** on lands; filename token `baud` / `jacques-baud` matches legacy rows",
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
