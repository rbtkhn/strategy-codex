#!/usr/bin/env python3
"""Rebuild statecraft/voices/marandi/marandi-index.md from archive Marandi captures."""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ARCHIVE = REPO / "source-archive" / "statecraft"
OUT = REPO / "statecraft" / "voices" / "marandi" / "marandi-index.md"
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
    slug = (meta.get("channel_slug") or "").casefold()
    if "india-global-left" in name:
        return "India Global Left"
    if "breaking-points" in name:
        return "Breaking Points"
    if "dialogue-works" in name or slug == "dialogue-works":
        return "Dialogue Works"
    if "judging-freedom" in name or slug == "judging-freedom":
        return "Napolitano"
    if "daniel-davis" in name or ("davis-" in name and "marandi" in name):
        return "Davis"
    if "glenn-diesen" in name or "diesen-" in name:
        return "Diesen"
    if name.startswith("source-marandi-"):
        return "Shorthand"
    if "ghalibaf" in name:
        return "Ghalibaf repost"
    if "napolitano" in host or "judging freedom" in (meta.get("show") or "").casefold():
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
    for path in iter_archive_captures_for_shelf("marandi", ARCHIVE):
        meta = parse_head(path)
        body = path.read_text(encoding="utf-8")[:8000]
        if shelf_utils.shelf_capture_excluded("marandi", path, meta, body):
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
        "MOU / Geneva / Hormuz mechanism week — one row per pub day; full archive list in **2026-06** above.",
        "",
        "| Pub date | Host | Type | Mechanism lane |",
        "|----------|------|------|----------------|",
        "| Jun 02 | Dialogue Works (Alkhorshid) | Solo | Lebanon rockets; decisive Iran–US clash imminent |",
        "| Jun 03 | Napolitano | Solo | From Tehran — how Iran trapped Trump |",
        "| Jun 05 | Dialogue Works · Diesen | Solo + guest | Hormuz toll; Kuwait strike; Israeli decline / nuke bomb lane |",
        "| Jun 06 | Dialogue Works (Alkhorshid) | Solo | Kuwait hit; US 5th Fleet Bahrain |",
        "| Jun 08 | Diesen | Guest | Israel strikes; Trump humiliated; Yemen Red Sea |",
        "| Jun 09 | Davis · Dialogue Works | Deep dive + solo | Expect escalation; Iran new equation vs Israel |",
        "| Jun 11 | Breaking Points · Napolitano | Guest + solo | Iran welcomes US invasion? / why Iran risks war |",
        "| Jun 13 | Dialogue Works (Alkhorshid) | Breaking | US–Iran brink; final deal framing |",
        "| Jun 14 | Davis · Dialogue Works · Diesen | Triple same-day | Deal complete; full details; Beirut sabotage — [Johnson×Marandi](../../../source-archive/statecraft/2026-06-14/source-dialogue-works-johnson-marandi-us-iran-reach-deal-full-details-2026-06-14.md) |",
        "| Jun 16 | Dialogue Works (Alkhorshid) | Solo | Hezbollah buffer zone; Israel refuses withdraw |",
        "| Jun 17 | Dialogue Works w/ Johnson | Solo | White House 14-point MOU — [archive](../../../source-archive/statecraft/2026-06-17/source-dialogue-works-larry-johnson-marandi-white-house-full-14-point-mou-2026-06-17.md) |",
        "| Jun 19 | Dialogue Works w/ Johnson | Solo | Geneva talks shut; MOU week — [archive](../../../source-archive/statecraft/2026-06-19/source-dialogue-works-seyed-m-marandi-larry-johnson-iran-shuts-down-geneva-talks-mou-2026-06-19.md) |",
        "| Jun 23 | Dialogue Works (Alkhorshid) | Solo | New Hormuz mechanism; IAEA access on hold |",
        "| Jun 24 | Napolitano | Solo | Stands firm; live Tehran / MOU restraint — [archive](../../../source-archive/statecraft/2026-06-24/source-judging-freedom-marandi-iran-stands-firm-negotiations-2026-06-24.md) |",
        "| Jun 25 | Diesen | Guest | Trump lost Iran war; must sell victory |",
        "| Jun 26 | Davis | Deep dive | Will US collapse global economy |",
        "",
        "May lane closes [2026-05-30](../../../source-archive/statecraft/2026-05-30/source-dialogue-works-seyed-m-marandi-iran-dropped-the-hammer-in-strait-of-hormuz-trump-s-no-tolls-plan-backfires-2026-05-30.md) (Hormuz hammer); prior Napolitano Tehran [2026-05-28](../../../source-archive/statecraft/2026-05-28/source-judging-freedom-marandi-from-tehran-should-iran-trust-trump-2026-05-28.md).",
        "",
    ]

def render_curated_overlays() -> list[str]:
    """Host-arc routing overlay — not part of archive parity row count."""
    return [
        "## Curated host lanes",
        "",
        "Three-host mature core (transformations, not parity substitutes):",
        "",
        "- **Dialogue Works x Marandi** — legitimacy, red lines, selective Hormuz, Gulf complicity · [arc-marandi-nima-host.md](../../notes/arc-marandi-nima-host.md)",
        "- **Diesen x Marandi** — strategic-order and escalation-horizon lane · [arc-marandi-diesen-host.md](../../notes/arc-marandi-diesen-host.md)",
        "- **Davis x Marandi** — operational-limit and failed-intimidation lane · [Daniel Davis channel shelf](../../channels/daniel-davis/README.md)",
        "- **Napolitano x Marandi** — Tehran live / U.S.-audience translation (support-tier, not co-equal helix)",
        "",
        "Support spine: [marandi-support-spine-2025-2026.md](marandi-support-spine-2025-2026.md) · routing: [marandi-routing.md](marandi-routing.md) · compat: [marandi-source-index.md](marandi-source-index.md).",
        "",
        "**Open first by task:** mature lane → Dialogue Works; strategic altitude → Diesen; operational limits → Davis; live Tehran reinforcement → Napolitano Jun 24.",
        "",
    ]

def render_index(rows: list[tuple[str, Path, dict]], annotations: dict[str, str]) -> str:
    by_month: dict[str, list[tuple[str, Path, dict]]] = defaultdict(list)
    for row in rows:
        pub = row[0]
        month = pub[:7] if len(pub) >= 7 else pub
        by_month[month].append(row)

    lines = [
        "# Marandi source index",
        "",
                "",
        "Purpose: exhaustive canonical route map for Seyed Mohammad Marandi guest appearances and direct archive anchors on the Marandi shelf.",
        "",
        "**Audit:** `python scripts/audit_statecraft_archive_index.py --shelf-index marandi` — author/guest parity; skill **`audit index`**. (_Curated rebuild via builder — no `--fix`._)",
        "",
        "## Corpus note",
        "",
        f"- **{len(rows)}** eligible archive captures on disk",
        "- Rebuild: `python scripts/build_marandi_index.py`",
        "- Mature core is genuinely three-host (Dialogue Works / Diesen / Davis); Napolitano and shorthand captures are support-tier residue",
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
            "- host-local arcs still own first-open transformations",
            "- this file is the canonical source-index and therefore the ordinary source bench, not a month atlas",
            "- support-tier residue stays listed but should not silently promote into shelf-defining evidence",
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
