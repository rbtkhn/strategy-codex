#!/usr/bin/env python3
"""Rebuild statecraft/voices/aguilar/aguilar-index.md from archive Aguilar captures."""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ARCHIVE = REPO / "source-archive" / "statecraft"
OUT = REPO / "statecraft" / "voices" / "aguilar" / "aguilar-index.md"
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
    r"^(?:(?:lt\.?|col\.?)\s+)?anthony\s+aguilar:\s*",
    re.I,
)

HOST_LABEL: dict[str, str] = {
    "nima": "Dialogue Works × Aguilar",
    "nawfal": "Nawfal × Aguilar",
    "moral_resistance": "Moral Resistance × Aguilar",
    "kiriakou": "Kiriakou × Aguilar",
    "other": "Aguilar",
}

MAY_HINGE_FN = (
    "source-dialogue-works-anthony-aguilar-hormuz-canberra-blockade-2026-05-04.md"
)
KIRIOKOU_FN = "source-kiriakou-anthony-aguilar-gaza-whistleblower-death-by-design-2026-02-27.md"


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
    if "kiriakou" in name:
        return "kiriakou"
    if "moral-resistance" in name:
        return "moral_resistance"
    if "mario-nawfal" in name:
        return "nawfal"
    if "dialogue-works" in name:
        return "nima"
    host = (meta.get("host") or "").casefold()
    show = (meta.get("show") or "").casefold()
    slug = (meta.get("channel_slug") or "").casefold()
    if "kiriakou" in host:
        return "kiriakou"
    if "moral resistance" in show or slug == "moral-resistance":
        return "moral_resistance"
    if "mario nawfal" in host or "nawfal" in slug:
        return "nawfal"
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
    for path in iter_archive_captures_for_shelf("aguilar", ARCHIVE):
        meta = parse_head(path)
        body = path.read_text(encoding="utf-8")[:8000]
        if shelf_utils.shelf_capture_excluded("aguilar", path, meta, body):
            continue
        pub = pub_date_key(meta, path)
        rows.append((pub, path, meta))
    rows.sort(key=lambda t: (t[0], t[1].name))
    return rows


def month_heading(month: str) -> str:
    if month == "2026-02":
        return "## 2026-02 (Kiriakou prehistory)"
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
                "**May hinge (DW × Aguilar — Hormuz / Canberra blockade — 2026-05-04):**",
                "",
            ]
        )
        for _pub, path, meta in section_rows:
            if path.name == MAY_HINGE_FN:
                lines.append(row_label(meta, path, labels, annotations))
                lines.append("")
                break
        other = [r for r in section_rows if r[1].name != MAY_HINGE_FN]
        if other:
            lines.append("**Other May anchors:**")
            lines.append("")
            for _pub, path, meta in sorted(other, reverse=True):
                lines.append(row_label(meta, path, labels, annotations))
            lines.append("")
    elif month == "2026-02" and any(r[1].name == KIRIOKOU_FN for r in section_rows):
        for _pub, path, meta in section_rows:
            if path.name == KIRIOKOU_FN:
                lines.append(row_label(meta, path, labels, annotations))
                lines.append(
                    "_Second-host evidence — not yet a stable branch; see "
                    "[aguilar-cross-host-note.md](aguilar-cross-host-note.md)._"
                )
                lines.append("")
                break
    else:
        for _pub, path, meta in sorted(section_rows, reverse=True):
            lines.append(row_label(meta, path, labels, annotations))
        lines.append("")
    return lines


def render_curated_overlays() -> list[str]:
    return [
        "## Host routing",
        "",
        "| Host | Index |",
        "| --- | --- |",
        "| Dialogue Works / Alkorshid | [arc-aguilar-nima-host](../../notes/arc-aguilar-nima-host.md) · [dialogue-works-channel-index](../../channels/dialogue-works/dialogue-works-channel-index.md) |",
        "| Mario Nawfal | [mario-nawfal channel-index](../../channels/mario-nawfal/mario-nawfal-channel-index.md) |",
        "| Moral Resistance | [moral-resistance channel-index](../../channels/moral-resistance/moral-resistance-channel-index.md) |",
        "| John Kiriakou | second-host evidence only — [aguilar-cross-host-note.md](aguilar-cross-host-note.md) |",
        "",
        "## Reading rule",
        "",
        "1. Open **Statecraft Archive** direct files first.",
        "2. Treat Aguilar as **practitioner-facing operational / war-conduct witness** — blockade, naval posture, escalation feasibility; not engineering-first (→ [Postol](../postol/postol-index.md)) or macro-order collapse (→ [Martyanov](../martyanov/martyanov-index.md)).",
        "3. Default host branch: **Alkorshid / Dialogue Works** — Nawfal and Moral Resistance reinforce live-crisis lanes without constituting a second helix yet.",
        "",
        "## Boundary notes",
        "",
        "- Object doctrine: [aguilar-speaker-object.md](aguilar-speaker-object.md) · [aguilar-cross-host-note.md](aguilar-cross-host-note.md)",
        "- **Single-helix** on disk — do not infer multi-host maturity from Nawfal/Moral Resistance density alone.",
        "- No `aguilar-profile.md` yet — shelf is **speaker-object + index**.",
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
    nawfal_n = sum(1 for r in rows if host_bucket(r[1], r[2]) == "nawfal")
    moral_n = sum(1 for r in rows if host_bucket(r[1], r[2]) == "moral_resistance")
    kiriakou_n = sum(1 for r in rows if host_bucket(r[1], r[2]) == "kiriakou")

    lines = [
        "# Aguilar source index",
        "",
        "WORK only; not Record.",
        "",
        "Purpose: canonical statecraft-side source index for **Anthony Aguilar** while raw-text authority stays in the Statecraft Archive.",
        "",
        "**Audit:** `python scripts/audit_statecraft_archive_index.py --shelf-index aguilar` — author/guest parity; skill **`audit index`**. (_Curated rebuild via builder — no `--fix`._)",
        "",
        "## Surface Grammar",
        "",
        "- **Surface name:** `aguilar-source-index.md`",
        "- **Surface role:** source bench for breadth-first Aguilar retrieval",
        "- **Surface interior:** materialized guest appearances across Dialogue Works, Nawfal, Moral Resistance, and one Kiriakou anchor",
        "",
        "**Identity / object hub:** [aguilar-speaker-object.md](aguilar-speaker-object.md)",
        "",
        "## Corpus note",
        "",
        f"- **{len(rows)}** eligible archive captures on disk ({date_span})",
        "- Rebuild: `python scripts/build_aguilar_index.py`",
        f"- **{nima_n}** Dialogue Works · **{nawfal_n}** Nawfal · **{moral_n}** Moral Resistance · **{kiriakou_n}** Kiriakou",
        "- **`thread: aguilar`** on new lands; filename token `aguilar` matches legacy rows",
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
