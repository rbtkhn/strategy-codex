#!/usr/bin/env python3
"""Build statecraft/voices/diesen/diesen-index.md from archive guest captures."""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import shelf_index_utils as shelf_utils  # noqa: E402

REPO = SCRIPTS.parent
ARCHIVE = REPO / "source-archive" / "statecraft"
OUT = REPO / "statecraft" / "voices" / "diesen" / "diesen-index.md"

HOST_CROSS_REFS = {
    "daniel-davis": (
        "daniel-davis-channel-index.md",
        "../../channels/daniel-davis/daniel-davis-channel-index.md",
    ),
    "mario-nawfal": (
        "mario-nawfal-channel-index.md",
        "../../channels/mario-nawfal/mario-nawfal-channel-index.md",
    ),
    "judging-freedom": (
        "judging-freedom-channel-index.md",
        "../../channels/judging-freedom/judging-freedom-channel-index.md",
    ),
}

CHANNEL_INDEX = "../../channels/glenn-diesen/glenn-diesen-channel-index.md"


def parse_head(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")[:4000]
    out: dict = {}
    for key in ("title", "channel_slug", "show", "host", "guest", "thread", "youtube_id"):
        m = re.search(rf"^{key}:\s*(.+)$", text, re.M)
        if m:
            out[key] = m.group(1).strip().strip('"')
    for m in re.finditer(r"^guest_(\d+):\s*(.+)$", text, re.M):
        out[f"guest_{m.group(1)}"] = m.group(2).strip().strip('"')
    gp = re.search(r"^guest_people:\s*\n((?:\s+-\s+.+\n)*)", text, re.M)
    if gp:
        out["guest_people"] = [
            ln.split("-", 1)[1].strip() for ln in gp.group(1).strip().splitlines()
        ]
    return out


def month_key(day: str) -> str:
    if day == "_aired-pending":
        return day
    return day[:7] if len(day) >= 7 else day


def row_label(meta: dict, path: Path) -> str:
    title = meta.get("title") or path.stem.replace("source-", "", 1)
    if len(title) > 72:
        title = title[:69] + "…"
    host = meta.get("host") or meta.get("show") or "?"
    slug = meta.get("channel_slug") or ""
    yt = meta.get("youtube_id") or ""
    yt_bit = f" (`{yt}`)" if yt else ""
    slug_bit = f" · `{slug}`" if slug else ""
    cross_bit = ""
    slug_key = slug.lower()
    if slug_key in HOST_CROSS_REFS:
        xref_label, xref_rel = HOST_CROSS_REFS[slug_key]
        cross_bit = f" · cross-ref [{xref_label}]({xref_rel})"
    return (
        f"- [{path.parent.name} — {title}](../../../source-archive/statecraft/{path.parent.name}/{path.name})"
        f"{yt_bit} — host: **{host}**{slug_bit}{cross_bit}"
    )


def render_index(by_month: dict[str, list[tuple[Path, dict]]]) -> str:
    total = sum(len(v) for v in by_month.values())
    lines = [
        "WORK only; not Record.",
        "",
        "# Diesen Index",
        "",
        "Purpose: route map for **Glenn Diesen** as **guest / interviewed analyst on other hosts and channels** — not Glenn Diesen channel host work.",
        "",
        f"**Host channel (Glenn Diesen):** [`glenn-diesen-channel-index.md`]({CHANNEL_INDEX})",
        "",
        "## Boundary",
        "",
        "| Route here | Route to Glenn Diesen channel shelf |",
        "|---|---|",
        "| `guest:` / `guest_people:` Glenn Diesen on **another** `channel_slug` | `source-glenn-diesen-*` · `source-diesen-*` on `channel_slug: glenn-diesen` · Diesen hosting guests on his channel |",
        "| Cross-host analyst continuity | Host-conditioned framing (how other shows surface Diesen) |",
        "",
        "Do **not** dedupe by calendar day alone — same person on Davis vs Judging Freedom = two host reads.",
        "",
        "## Corpus note",
        "",
        f"- **{total}** materialized cross-host guest captures on disk; expand as archive grows",
        "- Filename family for guest rows: `source-<host-channel>-*diesen*` with explicit `guest: Glenn Diesen` and `channel_slug` ≠ `glenn-diesen` (or host ≠ Glenn Diesen)",
        "",
    ]
    for mk in sorted(by_month.keys()):
        lines.append(f"## {mk}")
        lines.append("")
        for path, meta in sorted(by_month[mk], key=lambda t: t[0].name):
            lines.append(row_label(meta, path))
        lines.append("")
    lines.extend(
        [
            "## Host cross-refs",
            "",
            "| Host | When Diesen is guest there |",
            "|---|---|",
            "| **Daniel Davis** | negotiation-room / messaging realism on Iran war reads — not Glenn Diesen host register |",
            "| **Mario Nawfal** | breaking-news panel tempo on Hormuz / toll mechanics |",
            "| **Judging Freedom** | Napolitano legal-institutional frame on Europe war prep |",
            "",
            "## Reading rule",
            "",
            "- **Guest mechanism / cross-host Diesen** → this index",
            f"- **Diesen as host or solo on Glenn Diesen channel** → [`glenn-diesen-channel-index.md`]({CHANNEL_INDEX})",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit 1 if generated index would differ from file on disk",
    )
    args = parser.parse_args()

    by_month: dict[str, list[tuple[Path, dict]]] = defaultdict(list)
    for path in sorted(ARCHIVE.glob("**/source-*.md")):
        meta = parse_head(path)
        if shelf_utils.is_diesen_guest_index_capture(meta, path):
            by_month[month_key(path.parent.name)].append((path, meta))

    content = render_index(by_month)
    total = sum(len(v) for v in by_month.values())

    if args.check:
        if OUT.is_file() and OUT.read_text(encoding="utf-8") == content:
            print(f"OK {OUT.relative_to(REPO)} ({total} rows)")
            return 0
        print(f"STALE {OUT.relative_to(REPO)} ({total} rows)", file=sys.stderr)
        return 1

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(content, encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO)} ({total} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
