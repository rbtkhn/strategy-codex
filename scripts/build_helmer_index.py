#!/usr/bin/env python3
"""Rebuild statecraft/voices/helmer/helmer-index.md from archive Helmer captures."""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ARCHIVE = REPO / "source-archive" / "statecraft"
OUT = REPO / "statecraft" / "voices" / "helmer" / "helmer-index.md"
_SCRIPTS = REPO / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import shelf_index_utils as shelf_utils  # noqa: E402
from audit_statecraft_archive_index import iter_archive_captures_for_shelf  # noqa: E402
from statecraft_day_archive import read_text  # noqa: E402

LINK_SUFFIX_RE = re.compile(
    r"\]\((?:\.\./\.\./\.\./source-archive/statecraft/\d{4}-\d{2}-\d{2}/([^)]+))\)(.*)$"
)
HELMER_TITLE_PREFIX = re.compile(r"^John Helmer:\s*", re.I)


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


def host_bucket(path: Path) -> str:
    name = path.name.casefold()
    if "lascaris-helmer" in name or name.startswith("source-lascaris-"):
        return "lascaris"
    if "dialogue-works-helmer" in name or "dialogue-works" in name:
        return "dialogue_works"
    return "other"


def display_title(meta: dict) -> str:
    raw = meta.get("title") or "Untitled"
    return HELMER_TITLE_PREFIX.sub("", raw).strip()


def row_label(meta: dict, path: Path) -> str:
    pub = pub_date_key(meta, path)
    title = display_title(meta)
    rel = f"../../../source-archive/statecraft/{path.parent.name}/{path.name}"
    return f"- [{pub} - {title}]({rel})"


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
    for path in iter_archive_captures_for_shelf("helmer", ARCHIVE):
        meta = parse_head(path)
        body = path.read_text(encoding="utf-8")[:8000]
        if shelf_utils.shelf_capture_excluded("helmer", path, meta, body):
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
        "| Pub date | Title (short) | Mechanism lane |",
        "|----------|---------------|----------------|",
        "| Jun 02 | Unthinkable move | Iran escalation / Middle East reorder; Beirut/Dahieh opening context |",
        "| Jun 09 | Crisis of confidence | Contrarian: Russian **public frustration** with slow war vs escalation camp ([Krapivnik same-day rebuttal](../../../source-archive/statecraft/2026-06-09/source-dialogue-works-stanislav-krapivnik-breaking-us-attacks-iran-russia-no-deal-coming-2026-06-09.md) cites Helmer — **not** a Helmer appearance) |",
        "| Jun 13 | Restore deterrence (Lascaris) | Domestic recession + Duma election; Nabiev/Siluanov vs military; Lavrov May 25 systemic strikes repudiated; **no NATO-target strikes** while Dmitriev–Witkoff Anchorage line holds; Karaganov cited via Oslo Glendes; cross-ref [Diesen Karaganov/Mearsheimer same day](../../../source-archive/statecraft/2026-06-13/source-glenn-diesen-mearsheimer-karaganov-nuclear-strike-europe-restore-deterrence-2026-06-13.md) |",
        "| Jun 16 | MOU reaction | MOU-week Moscow read: Dmitriev/Anchorage vs Lavrov/military; Lebanon 60-day; $300B fund; GCC protection buying; Ukraine two-track |",
        "| Jun 23 | Vance / Lebanon MOU / Hormuz | Post-MOU Moscow read: Vance-Netanyahu cabinet row; Lebanon buffer; Hormuz mechanism; Putin Ukraine two-track |",
        "| Jun 25 | Destroy Russia and Iran (Lascaris) | Trump endgame unchanged — simultaneous pressure on Moscow and Tehran; domestic faction vs Dmitriev lane |",
        "",
        "**Pattern:** earliest 2026 land **Jan 20** (Dialogue Works); **Feb 03–17** pre-Geneva window; **Mar 03–24** Iran-war escalation arc; **Apr 28** resume; ~weekly **Tuesday** Dialogue Works through Jun 23 plus **May 24**, **Jun 13**, and **Jun 25** Reason to Resist (Lascaris).",
        "",
        "**Cross-weave:** Jun 16 pairs with [MOU-week Napolitano bench](../../notes/2026-06-15-mou-week-napolitano-bench-seam.md) (McGovern/Crooke/Sachs/Pape) — Helmer supplies **Kremlin domestic faction** lane; Pape supplies leverage math. **Jan 20** — [Greenland three-way weave](../../notes/2026-01-20-greenland-same-day-weave-helmer-freeman.md) (Helmer × Freeman × Mercouris — all transcript-tier); [Davos Dmitriev — Helmer × Mercouris](../../notes/arc-helmer-dmitriev-lane.md). **Feb 17** — [Geneva day weave — Helmer × Mercouris](../../notes/2026-02-17-geneva-day-weave-helmer-mercouris.md) (both **transcript-tier**).",
        "",
    ]


def render_host_compat_and_boundary() -> list[str]:
    return [
        "## Host / compatibility entries",
        "",
        "- [Reason to Resist channel index](../../channels/reason-resist/reason-resist-channel-index.md) — host shelf (May 24 dormitory + May 26 flotilla + Jun 13/25 Helmer; Jun 18 Henningsen)",
        "- [Dialogue Works index](../../channels/dialogue-works/dialogue-works-channel-index.md) — partial Helmer rows pre-archive migration",
        "- [Dialogue Works inventory](../../sheets/source-archive-control/dialogue-works-inventory.md) — wider uncaptured run",
        "",
        "## Reading rule",
        "",
        "1. Open **Statecraft Archive** direct files first.",
        "2. Treat Helmer as **Moscow reporting + faction inference** — orthogonal to McGovern ease-at-SPIEF and Ritter Karaganov fence ([arc-ritter-karaganov-doctrine.md](../../notes/arc-ritter-karaganov-doctrine.md)).",
        "3. Same-day **guest mentions** (e.g. Krapivnik on Helmer) = continuity signal, **not** index rows.",
        "4. Apply [source-lattice](../../../docs/source-lattice-beyond-the-repo.md) before lane judgment.",
        "",
        "## Boundary notes",
        "",
        "- No `helmer-arc.md` yet — shelf is **profile + index** until month density warrants arc/helix.",
        "- Helmer Substack (`johnhelmer.net`) not mirrored in archive; in-interview citations only.",
        "",
    ]


def render_host_section(
    heading: str,
    rows: list[tuple[str, Path, dict]],
    annotations: dict[str, str],
) -> list[str]:
    by_month: dict[str, list[tuple[str, Path, dict]]] = defaultdict(list)
    for row in rows:
        pub = row[0]
        month = pub[:7] if len(pub) >= 7 else pub
        by_month[month].append(row)

    lines = [heading, ""]
    for month in sorted(by_month):
        lines.append(f"#### {month}")
        lines.append("")
        for _pub, path, meta in by_month[month]:
            line = row_label(meta, path)
            ann = annotations.get(path.name)
            if ann:
                line += f" {ann}"
            lines.append(line)
        lines.append("")
    return lines


def render_index(rows: list[tuple[str, Path, dict]], annotations: dict[str, str]) -> str:
    dw_rows = [r for r in rows if host_bucket(r[1]) == "dialogue_works"]
    lascaris_rows = [r for r in rows if host_bucket(r[1]) == "lascaris"]
    other_rows = [r for r in rows if host_bucket(r[1]) == "other"]

    dw_count = len(dw_rows)
    lascaris_count = len(lascaris_rows)
    date_span = f"{rows[0][0]} → {rows[-1][0]}" if rows else "—"

    lines = [
        "WORK only; not Record.",
        "",
        "# Helmer Source Index",
        "",
        "Purpose: canonical route map for materialized John Helmer appearances in **Statecraft Archive**. **Identity / voice hub:** [helmer-profile.md](helmer-profile.md). Primary hosts: **Dialogue Works / Nima** and **Reason to Resist / Lascaris** — Moscow insider-reporting register, Kremlin faction reads, deterrence / drone-war lanes.",
        "",
        "**Audit:** `python scripts/audit_statecraft_archive_index.py --shelf-index helmer` — author/guest parity; skill **`audit index`**. (_Curated rebuild via builder — no `--fix`._)",
        "",
        "## Corpus note",
        "",
        f"- **{len(rows)}** direct captures on disk ({date_span}): **{dw_count}** `source-dialogue-works-helmer-*`, **{lascaris_count}** `source-lascaris-helmer-*`",
        "- Rebuild: `python scripts/build_helmer_index.py`",
        "- **0** authored Substack / solo-site captures in archive (Helmer blog cited in-interview only)",
        "- **`thread: helmer`** on Jun 09+ lands; earlier rows **`thread: nima`** / **`thread: alkorshid`** — all route here for guest appearances",
        "",
        "Verify Kremlin quotations, poll claims, and naval-incident narratives against primary sources before Chronicle promotion ([editorial notes on captures](../../../source-archive/statecraft/2026-04-28/source-dialogue-works-helmer-middle-east-unthinkable-iran-play-2026-04-28.md)).",
        "",
        "## Direct Materialized Appearances",
        "",
    ]

    lines.extend(render_host_section("### Dialogue Works / Nima", dw_rows, annotations))
    lines.extend(render_host_section("### Reason to Resist / Lascaris", lascaris_rows, annotations))

    if other_rows:
        lines.extend(render_host_section("### Other hosts", other_rows, annotations))

    lines.extend(render_june_cadence_table())
    lines.extend(render_host_compat_and_boundary())
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
