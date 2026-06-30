#!/usr/bin/env python3
"""Rebuild statecraft/voices/sachs/sachs-index.md from archive Sachs captures."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ARCHIVE = REPO / "source-archive" / "statecraft"
OUT = REPO / "statecraft" / "voices" / "sachs" / "sachs-index.md"
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
SACHS_TITLE_PREFIX = re.compile(r"^(?:Jeffrey\s+Sachs|Prof\.?\s+Jeffrey\s+Sachs):\s*", re.I)

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

def host_bucket(path: Path, meta: dict) -> str:
    name = path.name.casefold()
    host = (meta.get("host") or "").casefold()
    show = (meta.get("show") or "").casefold()
    slug = (meta.get("channel_slug") or "").casefold()
    if "judging-freedom" in name and "sachs" in name:
        return "judging_freedom"
    if ("diesen" in name or "glenn-diesen" in name) and "sachs" in name:
        return "diesen"
    if "duran" in name and "sachs" in name:
        return "duran"
    if "tucker-carlson" in name or ("tucker" in name and "sachs" in name):
        return "tucker"
    if "fidias" in name:
        return "fidias"
    if "neutrality-studies" in name:
        return "neutrality"
    if "horizons" in name:
        return "horizons"
    if name.startswith("source-sachs-"):
        return "sachs_owned"
    if "judging freedom" in show or "napolitano" in host:
        return "judging_freedom"
    if "glenn diesen" in host or "diesen" in slug:
        return "diesen"
    if "duran" in show or "mercouris" in slug:
        return "duran"
    if "tucker" in slug:
        return "tucker"
    return "other"

def display_title(meta: dict) -> str:
    raw = meta.get("title") or "Untitled"
    return SACHS_TITLE_PREFIX.sub("", raw).strip()

def load_label_map(index_path: Path) -> dict[str, str]:
    if not index_path.is_file():
        return {}
    out: dict[str, str] = {}
    for line in read_text(index_path).splitlines():
        m = LABEL_RE.search(line)
        if m:
            out[m.group(2)] = m.group(1)
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
    title = display_title(meta)
    return f"{pub} - {title}"

def row_label(meta: dict, path: Path, labels: dict[str, str]) -> str:
    text = labels.get(path.name) or default_label(meta, path)
    rel = f"../../../source-archive/statecraft/{path.parent.name}/{path.name}"
    return f"- [{text}]({rel})"

def collect_rows() -> list[tuple[str, Path, dict]]:
    rows: list[tuple[str, Path, dict]] = []
    for path in iter_archive_captures_for_shelf("sachs", ARCHIVE):
        meta = parse_head(path)
        body = path.read_text(encoding="utf-8")[:8000]
        if shelf_utils.shelf_capture_excluded("sachs", path, meta, body):
            continue
        pub = pub_date_key(meta, path)
        rows.append((pub, path, meta))
    rows.sort(key=lambda t: (t[0], t[1].name))
    return rows

def render_host_section(
    heading: str,
    rows: list[tuple[str, Path, dict]],
    bucket: str,
    labels: dict[str, str],
    annotations: dict[str, str],
) -> list[str]:
    section_rows = [r for r in rows if host_bucket(r[1], r[2]) == bucket]
    if not section_rows:
        return []
    lines = [heading, ""]
    for _pub, path, meta in section_rows:
        line = row_label(meta, path, labels)
        ann = annotations.get(path.name)
        if ann:
            line += f" {ann}"
        lines.append(line)
    lines.append("")
    return lines

def render_month_floor_overlay() -> list[str]:
    """Curated rollup overlay — links may duplicate host-section rows."""
    return [
        "## Month-Floor Repair Additions",
        "",
        "These bounded additions were landed to bring every live Sachs month from `2025-01` through `2026-06` to at least `4` captures in the archive rollups.",
        "",
        "- `2025-01`: [2025-01-14 - #PEACE Prof. Jeffrey Sachs](../../../source-archive/statecraft/2025-01-14/source-judging-freedom-sachs-peace-2025-01-14.md), [2025-01-30 - Jeffrey Sachs on U.S. Arrogance, Global Power & Why We Can't Trust Our Leaders](../../../source-archive/statecraft/2025-01-30/source-sachs-on-us-arrogance-global-power-and-why-we-cant-trust-our-leaders-2025-01-30.md)",
        "- `2025-02`: [2025-02-18 - Jeffrey Sachs on the 3 Most Important Things Trump Has Done So Far and America's Global Dominance](../../../source-archive/statecraft/2025-02-18/source-sachs-three-most-important-things-trump-has-done-so-far-and-americas-global-dominance-2025-02-18.md), [2025-02-19 - Speech at the EU Parliament](../../../source-archive/statecraft/2025-02-19/source-sachs-speech-at-the-eu-parliament-2025-02-19.md)",
        "- `2025-03`: [2025-03-02 - Jeffrey Sachs on the Trump-Zelenskyy meeting and what comes next for Russia, Ukraine, Europe and the U.S](../../../source-archive/statecraft/2025-03-02/source-sachs-trump-zelenskyy-meeting-and-what-comes-next-2025-03-02.md), [2025-03-10 - The Heat: One-on-one with Jeffrey Sachs](../../../source-archive/statecraft/2025-03-10/source-sachs-the-heat-one-on-one-2025-03-10.md), [2025-03-22 - Jeffrey D. Sachs, Most Trusted Geopolitical Expert On Trump's Tariffs War & US' Role In Ukraine War](../../../source-archive/statecraft/2025-03-22/source-sachs-trumps-tariffs-war-and-us-role-in-ukraine-war-2025-03-22.md)",
        "- `2025-04`: [2025-04-08 - The Sachs Doctrine: Reimagining Growth Through Sustainable Development | Rising Bharat Summit 2025](../../../source-archive/statecraft/2025-04-08/source-sachs-reimagining-growth-through-sustainable-development-2025-04-08.md), [2025-04-09 - An Evening with Professor Jeffrey D. Sachs](../../../source-archive/statecraft/2025-04-09/source-sachs-an-evening-with-professor-jeffrey-d-sachs-2025-04-09.md), [2025-04-25 - Who Rules the New Global Order? with Professor Jeffrey Sachs](../../../source-archive/statecraft/2025-04-25/source-sachs-who-rules-the-new-global-order-2025-04-25.md)",
        "- `2025-05`: [2025-05-03 - Η Παγκόσμια Τάξη σε Μετάβαση - Prof. Jeffrey Sachs](../../../source-archive/statecraft/2025-05-03/source-sachs-global-order-in-transition-2025-05-03.md)",
        "- `2025-07`: [2025-07-15 - Jeffrey Sachs: End of the Western-Centric World & Rise of BRICS](../../../source-archive/statecraft/2025-07-15/source-diesen-sachs-end-of-the-western-centric-world-and-rise-of-brics-2025-07-15.md), [2025-07-21 - Doomsday Clock is Ticking: U.S. Foreign Policy and the Global Crisis](../../../source-archive/statecraft/2025-07-21/source-sachs-doomsday-clock-is-ticking-us-foreign-policy-and-the-global-crisis-2025-07-21.md)",
        "- `2026-01`: [2026-01-03 - Jeffrey Sachs: U.S. Attacks Venezuela & Kidnaps President Maduro](../../../source-archive/statecraft/2026-01-03/source-sachs-us-attacks-venezuela-and-kidnaps-president-maduro-2026-01-03.md), [2026-01-04 - Jeffrey Sachs: U.S. Attacks Venezuela & Kidnaps President Maduro (Diesen)](../../../source-archive/statecraft/2026-01-04/source-diesen-sachs-us-attacks-venezuela-and-kidnaps-president-maduro-2026-01-04.md), [2026-01-07 - Europe-Russia, two-century failure w/ Jeffrey Sachs (Live)](../../../source-archive/statecraft/2026-01-07/source-sachs-europe-russia-two-century-failure-2026-01-07.md), [2026-01-13 - The Western world is in a deeply neurotic state](../../../source-archive/statecraft/2026-01-13/source-sachs-the-western-world-is-in-a-deeply-neurotic-state-2026-01-13.md), [2026-01-27 - Using the Economy as a Weapon — Trump and Iran](../../../source-archive/statecraft/2026-01-27/source-judging-freedom-sachs-using-the-economy-as-a-weapon-trump-and-iran-2026-01-27.md)",
        "- `2026-02`: [2026-02-02 - Jeffrey Sachs: US-Iran War INEVITABLE...](../../../source-archive/statecraft/2026-02-02/source-sachs-us-iran-war-inevitable-2026-02-02.md), [2026-02-03 - Prof. Jeffrey Sachs: The Global Cost of MAGA Politics](../../../source-archive/statecraft/2026-02-03/source-judging-freedom-sachs-the-global-cost-of-maga-politics-2026-02-03.md), [2026-02-11 - U.S. Economic Coercion & Death of Dollar](../../../source-archive/statecraft/2026-02-11/source-sachs-us-economic-coercion-and-the-death-of-the-dollar-2026-02-11.md)",
        "- `2026-03`: [2026-03-03 - Did Trump Just Start WWIII?](../../../source-archive/statecraft/2026-03-03/source-judging-freedom-sachs-did-trump-just-start-wwiii-2026-03-03.md)",
        "- `2026-04`: [2026-04-02 - Incoherent, Illegal, Reckless...](../../../source-archive/statecraft/2026-04-02/source-sachs-incoherent-illegal-reckless-2026-04-02.md), [2026-04-06 - Trump Reveals His Desperation](../../../source-archive/statecraft/2026-04-06/source-judging-freedom-sachs-trump-reveals-his-desperation-2026-04-06.md), [2026-04-15 - Trump's Naval Blockade of the Strait of Hormuz](../../../source-archive/statecraft/2026-04-15/source-sachs-trumps-naval-blockade-of-the-strait-of-hormuz-2026-04-15.md), [2026-04-20 - Is the war over?](../../../source-archive/statecraft/2026-04-20/source-judging-freedom-sachs-is-the-war-over-2026-04-20.md)",
        "- `2026-05`: [2026-05-29 - Why is Israel at war with its neighbors?](../../../source-archive/statecraft/2026-05-29/source-judging-freedom-sachs-why-is-israel-at-war-with-its-neighbors-2026-05-29.md), [2026-05-31 - Germany Is Leading Europe Toward World War III (Diesen)](../../../source-archive/statecraft/2026-05-31/source-diesen-sachs-germany-is-leading-europe-toward-world-war-iii-2026-05-31.md)",
        "- `2026-06`: [2026-06-01 - Germany Is Leading Europe Toward World War III](../../../source-archive/statecraft/2026-06-01/source-diesen-sachs-germany-is-leading-europe-toward-world-war-three-2026-06-01.md), [2026-06-01 - How the best military and intel failed](../../../source-archive/statecraft/2026-06-01/source-judging-freedom-sachs-how-the-best-military-and-intel-failed-2026-06-01.md), [2026-06-02 - An Open Letter to Chancellor Friedrich Merz](../../../source-archive/statecraft/2026-06-02/source-sachs-an-open-letter-to-chancellor-friedrich-merz-2026-06-02.md), [2026-06-03 - European Leaders Do Nothing to Create Peace](../../../source-archive/statecraft/2026-06-03/source-diesen-sachs-european-leaders-do-nothing-to-create-peace-2026-06-03.md), [2026-06-08 - Is Trump losing it?](../../../source-archive/statecraft/2026-06-08/source-judging-freedom-sachs-is-trump-losing-it-2026-06-08.md), [2026-06-15 - US–Iran deal reached — peace or tactical pause? (Diesen)](../../../source-archive/statecraft/2026-06-15/source-diesen-sachs-us-iran-deal-reached-peace-or-tactical-pause-2026-06-15.md), [2026-06-15 - Netanyahu vs Trump](../../../source-archive/statecraft/2026-06-15/source-judging-freedom-sachs-netanyahu-vs-trump-2026-06-15.md), [2026-06-22 - Why Iran can't trust Trump](../../../source-archive/statecraft/2026-06-22/source-judging-freedom-sachs-why-iran-cant-trust-trump-2026-06-22.md)",
        "",
    ]

def render_tail() -> list[str]:
    return [
        "## Host-Arc Entries",
        "",
        "- [Diesen x Sachs](../../../source-archive/statecraft/2025-05-19/source-diesen-sachs-europes-declining-economy-security-and-common-sense-2025-05-19.md)",
        "- [Napolitano host shelf](../../channels/judging-freedom/README.md)",
        "",
        "## Reading Rule",
        "",
        "- use the direct materialized files first",
        "- use host arcs next when the task needs host-conditioned interpretation",
        "- treat the Napolitano branch as materially real but not yet a co-equal helix strand",
        "- treat the Mercouris and Tucker branches as reinforcing support, not shelf-owning primary chronology",
        "",
    ]

def render_index(
    rows: list[tuple[str, Path, dict]],
    labels: dict[str, str],
    annotations: dict[str, str],
) -> str:
    date_span = f"{rows[0][0]} → {rows[-1][0]}" if rows else "—"
    counts = {b: sum(1 for r in rows if host_bucket(r[1], r[2]) == b) for b in (
        "diesen", "judging_freedom", "sachs_owned", "fidias", "neutrality", "horizons", "duran", "tucker", "other"
    )}

    lines = [
                "",
        "# Sachs Source Index",
        "",
        "Purpose: provide the canonical route map for materialized Sachs appearances and the smaller set of direct archive anchors that explain the shelf shape.",
        "",
        "**Audit:** `python scripts/audit_statecraft_archive_index.py --shelf-index sachs` — author/guest parity; skill **`audit index`**. (_Curated rebuild via builder — no `--fix`._)",
        "",
        "## Corpus note",
        "",
        f"- **{len(rows)}** eligible archive captures on disk ({date_span})",
        "- Rebuild: `python scripts/build_sachs_index.py`",
        f"- **{counts['diesen']}** Diesen · **{counts['judging_freedom']}** Judging Freedom · **{counts['sachs_owned']}** Sachs-owned · **{counts['tucker']}** Tucker · **{counts['duran']}** Duran/Mercouris · misc **{counts['fidias'] + counts['neutrality'] + counts['horizons'] + counts['other']}**",
        "- Primary mature lane: **Diesen**; thick **Napolitano** bench; **Sachs-owned** lectures and month-floor repair residue",
        "",
        "## Direct Materialized Appearances",
        "",
    ]

    host_sections = [
        ("### Glenn Diesen", "diesen"),
        ("### Judging Freedom", "judging_freedom"),
        ("### Sachs-Owned Lectures", "sachs_owned"),
        ("### Fidias Podcast", "fidias"),
        ("### Neutrality Studies", "neutrality"),
        ("### HORIZONS / CIRSD", "horizons"),
        ("### Mercouris / The Duran", "duran"),
        ("### Tucker Carlson", "tucker"),
    ]
    for heading, bucket in host_sections:
        lines.extend(render_host_section(heading, rows, bucket, labels, annotations))

    other_rows = [r for r in rows if host_bucket(r[1], r[2]) == "other"]
    if other_rows:
        lines.extend(render_host_section("### Other hosts", rows, "other", labels, annotations))

    lines.extend(render_month_floor_overlay())
    lines.extend(render_tail())
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
        return 0

    OUT.write_text(body if body.endswith("\n") else body + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {OUT} ({len(rows)} rows, {len(labels)} labels preserved)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
