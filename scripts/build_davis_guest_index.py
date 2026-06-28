#!/usr/bin/env python3
"""Build statecraft/voices/davis/davis-index.md from archive guest captures."""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ARCHIVE = REPO / "source-archive" / "statecraft"
OUT = REPO / "statecraft" / "voices" / "davis" / "davis-index.md"
DAVIS = re.compile(r"daniel\s+davis|lt\.?\s*col\.?\s*daniel\s+davis", re.I)

HOST_CROSS_REFS = {
    "glenn-diesen": (
        "glenn-diesen-channel-index.md",
        "../../channels/glenn-diesen/glenn-diesen-channel-index.md",
    ),
    "dialogue-works": (
        "dialogue-works-channel-index.md",
        "../../channels/dialogue-works/dialogue-works-channel-index.md",
    ),
}

CHANNEL_INDEX = "../../channels/daniel-davis/daniel-davis-channel-index.md"


def parse_head(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")[:4000]
    out: dict = {}
    for key in ("title", "channel_slug", "show", "host", "guest", "thread", "youtube_id"):
        m = re.search(rf"^{key}:\s*(.+)$", text, re.M)
        if m:
            out[key] = m.group(1).strip().strip('"')
    gp = re.search(r"^guest_people:\s*\n((?:\s+-\s+.+\n)*)", text, re.M)
    if gp:
        out["guest_people"] = [
            ln.split("-", 1)[1].strip() for ln in gp.group(1).strip().splitlines()
        ]
    return out


def is_davis_material(path: Path, meta: dict) -> bool:
    if DAVIS.search(path.name) or meta.get("thread") == "davis":
        return True
    blob = " ".join([meta.get("host", ""), meta.get("guest", ""), " ".join(meta.get("guest_people") or [])])
    return bool(DAVIS.search(blob))


def is_host_channel(meta: dict, path: Path) -> bool:
    slug = meta.get("channel_slug", "")
    if slug == "daniel-davis":
        return True
    if path.name.lower().startswith("source-daniel-davis-"):
        return True
    return False


def is_guest(meta: dict, path: Path) -> bool:
    if not is_davis_material(path, meta):
        return False
    if is_host_channel(meta, path):
        return False
    if DAVIS.search(meta.get("guest", "")):
        return True
    for g in meta.get("guest_people") or []:
        if DAVIS.search(g):
            return True
    slug = meta.get("channel_slug", "")
    host = meta.get("host", "")
    if DAVIS.search(host):
        return False
    name = path.name.lower()
    if slug == "glenn-diesen" and "daniel-davis" in name:
        return True
    if slug == "dialogue-works" and "daniel-davis" in name:
        return True
    return False


def month_key(day: str) -> str:
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
        "# Davis Index",
        "",
        "Purpose: route map for **Daniel Davis** as **guest / interviewed analyst on other hosts and channels** — not Daniel Davis Deep Dive host work.",
        "",
        f"**Host channel (Daniel Davis):** [`daniel-davis-channel-index.md`]({CHANNEL_INDEX})",
        "",
        "## Boundary",
        "",
        "| Route here | Route to Daniel Davis channel shelf |",
        "|---|---|",
        "| `guest:` / `guest_people:` Daniel Davis on **another** `channel_slug` | `source-daniel-davis-*` · Deep Dive host interviews · solo monologues |",
        "| Cross-host analyst continuity | Host-conditioned framing (Diesen panel, Dialogue Works guest stream, …) |",
        "",
        "Do **not** dedupe by calendar day alone — same person on Diesen vs Dialogue Works = two host reads.",
        "",
        "## Corpus note",
        "",
        f"- **{total}** materialized cross-host guest captures on disk; expand as archive grows",
        "- Filename family: `source-glenn-diesen-daniel-davis-*` · `source-dialogue-works-*daniel-davis*` · explicit `guest: Daniel Davis` with `channel_slug` ≠ `daniel-davis`",
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
            "| Host | When Davis is guest there |",
            "|---|---|",
            "| **Glenn Diesen** | panel / co-host register on Iran–Ukraine feasibility — not Deep Dive host tempo |",
            "| **Dialogue Works (Nima)** | guest stream on escalation trap / Hormuz reads — not Davis host register |",
            "",
            "## Reading rule",
            "",
            "- **Guest mechanism / cross-host Davis** → this index",
            f"- **Davis as host on Deep Dive** → [`daniel-davis-channel-index.md`]({CHANNEL_INDEX})",
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
        if is_guest(meta, path):
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
