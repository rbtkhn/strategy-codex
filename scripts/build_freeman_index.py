#!/usr/bin/env python3
"""Rebuild statecraft/voices/freeman/freeman-index.md from archive Freeman captures."""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ARCHIVE = REPO / "source-archive" / "statecraft"
OUT = REPO / "statecraft" / "voices" / "freeman" / "freeman-index.md"
_SCRIPTS = REPO / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import shelf_index_utils as shelf_utils  # noqa: E402
from audit_statecraft_archive_index import iter_archive_captures_for_shelf  # noqa: E402
from statecraft_day_archive import read_text  # noqa: E402

LINK_SUFFIX_RE = re.compile(
    r"\]\((?:\.\./\.\./\.\./source-archive/statecraft/\d{4}-\d{2}-\d{2}/([^)]+))\)(.*)$"
)


def parse_head(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")[:5000]
    out: dict = {}
    for key in ("title", "pub_date", "kind", "source_form", "host", "show", "channel_slug", "thread"):
        m = re.search(rf"^{key}:\s*(.+)$", text, re.M)
        if m:
            out[key] = m.group(1).strip().strip('"').strip("'")
    if not out.get("title"):
        hm = re.search(r"^#\s+(.+)$", text, re.M)
        if hm:
            out["title"] = hm.group(1).strip()
    return out


def pub_date_key(meta: dict, path: Path) -> str:
    pub = meta.get("pub_date", "")
    if pub and len(pub) >= 10:
        return pub[:10]
    day = path.parent.name
    if re.match(r"^\d{4}-\d{2}-\d{2}$", day):
        return day
    return day


def host_short(meta: dict, path: Path) -> str:
    name = path.name.casefold()
    host = (meta.get("host") or "").casefold()
    show = (meta.get("show") or "").casefold()
    slug = (meta.get("channel_slug") or "").casefold()
    if "india-global-left" in name or slug == "india-global-left":
        return "India Global Left"
    if "dialogue-works" in name or slug == "dialogue-works":
        return "Dialogue Works"
    if "judging-freedom" in name or slug == "judging-freedom":
        return "Napolitano"
    if "daniel-davis" in name or ("davis-" in name and "daniel" in name):
        return "Davis"
    if "glenn-diesen" in name or "diesen-" in name or "chas-freeman" in name and "diesen" in name:
        return "Diesen"
    if "chas-freeman" in name or "freeman-" in name:
        if "judging" in name:
            return "Napolitano"
        if "dialogue" in name:
            return "Dialogue Works"
    if "napolitano" in host or "judging freedom" in show:
        return "Napolitano"
    if meta.get("show"):
        return meta["show"]
    if meta.get("host"):
        return meta["host"]
    return "Other"


def row_label(meta: dict, path: Path) -> str:
    pub = pub_date_key(meta, path)
    host = host_short(meta, path)
    rel = f"../../../source-archive/statecraft/{path.parent.name}/{path.name}"
    return f"- [{pub} {host}]({rel})"


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


def collect_rows() -> list[tuple[str, Path, dict]]:
    rows: list[tuple[str, Path, dict]] = []
    for path in iter_archive_captures_for_shelf("freeman", ARCHIVE):
        meta = parse_head(path)
        body = path.read_text(encoding="utf-8")[:8000]
        if shelf_utils.shelf_capture_excluded("freeman", path, meta, body):
            continue
        pub = pub_date_key(meta, path)
        rows.append((pub, path, meta))
    rows.sort(key=lambda t: (t[0], t[1].name))
    return rows


def render_june_cadence_table() -> list[str]:
    """Curated routing overlay — not part of archive parity rows."""
    return [
        "## June 2026 cadence (landed)",
        "",
        "Greater-Israel / agenda-collapse lane — one row per pub day; full archive list in **2026-06** above.",
        "",
        "| Pub date | Host | Type | Mechanism lane |",
        "|----------|------|------|----------------|",
        "| Jun 02 | Napolitano | Solo | US lost geopolitical primacy |",
        "| Jun 05 | Dialogue Works (Alkhorshid) | Solo | Israel free-fall on all fronts |",
        "| Jun 06 | Dialogue Works · Diesen | Solo + guest | Greater Israel project collapsing |",
        "| Jun 09 | Napolitano | Solo | Can Netanyahu defy Trump |",
        "| Jun 11 | India Global Left | Guest | Regional fallout US-Iran war — [IGL arc close](../../../source-archive/statecraft/2026-06-11/source-india-global-left-freeman-regional-fallout-us-iran-war-2026-06-11.md) |",
        "| Jun 12 | Dialogue Works (Alkhorshid) | Solo | Era of impunity Israel/US West Asia over |",
        "| Jun 16 | Napolitano | Solo | If Trump says no to Netanyahu |",
        "| Jun 19 | Dialogue Works (Alkhorshid) | Solo | Israel agenda major collapse |",
        "| Jun 23 | Napolitano | Solo | Should Iran trust Trump |",
        "| Jun 26 | Dialogue Works (Alkhorshid) | Solo | Collapse Israel agenda — [archive](../../../source-archive/statecraft/2026-06-26/source-dialogue-works-chas-freeman-collapse-israel-agenda-2026-06-26.md) |",
        "",
        "May lane closes [2026-05-29](../../../source-archive/statecraft/2026-05-29/source-dialogue-works-chas-freeman-hezbollah-strikes-israel-hard-israel-now-prepares-for-war-with-egypt-turkey-2026-05-29.md) (Hezbollah / Egypt-Turkey prep); last IGL May row [2026-05-20](../../../source-archive/statecraft/2026-05-20/source-india-global-left-is-iran-now-a-world-power-chas-freeman-2026-05-20.md).",
        "",
    ]


def render_curated_overlays() -> list[str]:
    """Cross-weave routing overlay — not part of archive parity row count."""
    return [
        "## Curated cross-weave lanes",
        "",
        "**India Global Left (IGL) Iran arc:** [Freeman × IGL Iran war (Feb 24→Jun 11 2026)](../../notes/arc-freeman-india-global-left-iran.md) · **2025 registers:** [Jun Iran push](../../notes/2025-freeman-igl-iran-war-push-register.md) · [Oct Gaza ceasefire](../../notes/2025-freeman-igl-gaza-ceasefire-register.md) · [2025 vs 2026 seam](../../notes/2025-vs-2026-freeman-igl-register-seam.md) · **Cross-register:** [Ritter × IGL Iran arc (Feb 20→Apr 9)](../../notes/arc-ritter-india-global-left-iran.md)",
        "",
        "Support spine (host chronology residue): [freeman-support-spine-2025-2026.md](freeman-support-spine-2025-2026.md) · backward extension: [freeman-backward-extension-note.md](freeman-backward-extension-note.md).",
        "",
        "## 2026-01 Greenland week — Jan 20 cross-weave",
        "",
        "Same-day **Greenland crisis** — route Freeman **alliance-law / credibility** against Helmer **Moscow sea-war** and Mercouris **solo institutional braid**; do **not** collapse into one verdict.",
        "",
        "| Register | Shelf | Capture / note |",
        "| --- | --- | --- |",
        "| **Freeman** (alliance law) | this index · [Jan 2026 shelf](freeman-shelf-2026-01.md) | [2026-01-20 Davis Deep Dive](../../../source-archive/statecraft/2026-01-20/source-daniel-davis-iran-eu-trump-greenland-lt-col-daniel-davis-chas-freeman-2026-01-20.md) — **full transcript** |",
        "| **Helmer** (Moscow sea-war) | [Helmer index](../helmer/helmer-source-index.md) | [2026-01-20 Dialogue Works](../../../source-archive/statecraft/2026-01-20/source-dialogue-works-helmer-two-fronts-collapsing-eu-greenland-ukraine-2026-01-20.md) |",
        "| **Mercouris** (institutional solo) | [Mercouris analytical bench](../mercouris/mercouris-analytical-bench.md) | [2026-01-20 solo — Starmer/Macron; Greenland; Kiev AD](../../../source-archive/statecraft/2026-01-20/source-alexander-mercouris-trump-humiliates-starmer-macron-again-demands-greenland-russia-destroys-2026-01-20.md) |",
        "",
        "**Mechanism lane (Jan 20 Davis):** **alliance-law / US credibility** — Trump **serious** on Greenland force; NATO **rupture** if Denmark invaded; Rasmussen–WH messaging **misalignment**; Archbishop **refusal-of-orders** line; Board of Peace / international-law register; Venezuela **intimidation-without-regime-change** rhyme.",
        "",
        "**Host frame (Davis):** allies increasingly vocal (Starmer); fear **order may actually be given** — complements Freeman legal register with **implementation anxiety**.",
        "",
        "**Synthesis objects:** [Jan 20 Greenland three-way weave](../../notes/2026-01-20-greenland-same-day-weave-helmer-freeman.md) · [Jan 20 Davos Dmitriev — Helmer × Mercouris](../../notes/arc-helmer-dmitriev-lane.md) · [2026-01-20 daily synthesis](../../synthesis/day/2026-01-20.md)",
        "",
        "**January Greenland arc (Freeman lane):** Jan 20 Davis · [Jan 22 Dialogue Works — Iran vows huge response](../../../source-archive/statecraft/2026-01-22/source-dialogue-works-amb-chas-freeman-iran-vows-huge-response-to-us-israel-attack-2026-01-22.md) · [Jan 7 Diesen — collapse of law/reason](../../../source-archive/statecraft/2026-01-07/source-glenn-diesen-chas-freeman-collapse-of-law-reason-return-to-war-2026-01-07.md)",
        "",
        "## Reading rule",
        "",
        "1. Open **Statecraft Archive** direct files first (month sections below).",
        "2. Treat Freeman as **alliance-law + strategic backfire** — orthogonal to Helmer **Moscow faction** and Mercouris **institutional solo braid**.",
        "3. **Davis Deep Dive** = implementation / ORBAT anxiety complement; **Napolitano** = Judging Freedom cadence; **Dialogue Works** = Amb. Freeman solo or paired; **Diesen** = Eurasia-order frame; **India Global Left** = long-form order / toll-governance Iran lane.",
        "4. Apply [source-lattice](../../../docs/source-lattice-beyond-the-repo.md) before lane judgment.",
        "",
    ]


def render_index(rows: list[tuple[str, Path, dict]], annotations: dict[str, str]) -> str:
    by_month: dict[str, list[tuple[str, Path, dict]]] = defaultdict(list)
    for row in rows:
        pub = row[0]
        month = pub[:7] if len(pub) >= 7 else pub
        by_month[month].append(row)

    lines = [
        "# Freeman source index",
        "",
        "WORK only; not Record.",
        "",
        "Purpose: exhaustive canonical route map for Amb. Chas Freeman guest appearances and direct archive anchors on the Freeman shelf.",
        "",
        "**Audit:** `python scripts/audit_statecraft_archive_index.py --shelf-index freeman` — author/guest parity; skill **`audit index`**. (_Curated rebuild via builder — no `--fix`._)",
        "",
        "**Identity / routing hub:** [freeman-arc.md](freeman-arc.md) · [freeman-routing.md](freeman-routing.md) · [freeman-helix.md](freeman-helix.md) · compat [freeman-source-index.md](freeman-source-index.md).",
        "",
        "## Corpus note",
        "",
        f"- **{len(rows)}** eligible archive captures on disk",
        "- Rebuild: `python scripts/build_freeman_index.py`",
        "",
    ]

    for month in sorted(by_month):
        lines.append(f"## {month}")
        lines.append("")
        for _pub, path, meta in by_month[month]:
            line = row_label(meta, path)
            ann = annotations.get(path.name)
            if ann:
                line += f" {ann}"
            lines.append(line)
        lines.append("")

    lines.extend(render_june_cadence_table())
    lines.extend(render_curated_overlays())
    lines.extend(
        [
            "## Boundary Notes",
            "",
            "- host-local arcs and support spine still own first-open transformations",
            "- this file is the canonical source-index and therefore the ordinary source bench, not a month atlas",
            "- open source-bearing files before quoting or making claim-grade factual use",
            "",
        ]
    )
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

    annotations = load_annotation_map(OUT)
    body = render_index(rows, annotations)
    if args.check:
        print(f"rows: {len(rows)}")
        print(f"annotations preserved: {len(annotations)}")
        return 0

    OUT.write_text(body if body.endswith("\n") else body + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {OUT} ({len(rows)} rows, {len(annotations)} annotations preserved)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
