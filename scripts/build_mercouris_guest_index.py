#!/usr/bin/env python3
"""Build statecraft/voices/mercouris/mercouris-index.md from archive guest captures."""
from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ARCHIVE = REPO / "source-archive" / "statecraft"
OUT = REPO / "statecraft" / "voices" / "mercouris" / "mercouris-index.md"
MERC = re.compile(r"alexander\s+mercouris|alex\s+mercouris", re.I)


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


def is_mercouris_material(path: Path, meta: dict) -> bool:
    if MERC.search(path.name) or meta.get("thread") == "mercouris":
        return True
    blob = " ".join(
        [meta.get("host", ""), meta.get("guest", ""), " ".join(meta.get("guest_people") or [])]
    )
    return bool(MERC.search(blob))


def is_host_channel(meta: dict, path: Path) -> bool:
    if meta.get("channel_slug") == "alexander-mercouris":
        return True
    if path.name.lower().startswith("source-alexander-mercouris-"):
        return True
    return False


def is_guest(meta: dict, path: Path) -> bool:
    if not is_mercouris_material(path, meta):
        return False
    if is_host_channel(meta, path):
        return False
    if MERC.search(meta.get("guest", "")):
        return True
    for g in meta.get("guest_people") or []:
        if MERC.search(g):
            return True
    if MERC.search(meta.get("host", "")):
        return False
    return "mercouris" in path.name.lower()


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
    return f"- [{path.parent.name} — {title}](../../../source-archive/statecraft/{path.parent.name}/{path.name}){yt_bit} — host: **{host}**{slug_bit}"


def main() -> None:
    by_month: dict[str, list[tuple[Path, dict]]] = defaultdict(list)
    for path in sorted(ARCHIVE.glob("**/source-*.md")):
        meta = parse_head(path)
        if is_guest(meta, path):
            by_month[month_key(path.parent.name)].append((path, meta))

    total = sum(len(v) for v in by_month.values())
    lines = [
        "WORK only; not Record.",
        "",
        "# Mercouris Index",
        "",
        "Purpose: route map for **Alexander Mercouris** as **guest / interviewed analyst on other hosts and channels** — not Alexander Mercouris solo-channel work.",
        "",
        "**Host channel (Alexander Mercouris):** [`alexander-mercouris-channel-index.md`](../../channels/alexander-mercouris/alexander-mercouris-channel-index.md)",
        "",
        "## Boundary",
        "",
        "| Route here | Route to Alexander Mercouris channel shelf |",
        "|---|---|",
        "| `guest:` / `guest_people:` Mercouris on **another** `channel_slug` | `source-alexander-mercouris-*` · solo monologues on `@AlexMercouris` |",
        "| Cross-host analyst continuity (Davis, Diesen, Duran, Neutrality Studies, …) | Host-conditioned framing on that channel |",
        "",
        "Do **not** dedupe by calendar day alone — same analyst on Davis vs Diesen vs Duran = distinct host reads.",
        "",
        "## Corpus note",
        "",
        f"- **{total}** materialized cross-host guest captures on disk; expand as archive grows",
        "- Filename families: `source-duran-mercouris-*` · `source-daniel-davis-*mercouris*` · `source-glenn-diesen-*mercouris*` · explicit `guest: Alexander Mercouris` with `channel_slug` ≠ `alexander-mercouris`",
        "- **The Duran:** YAML lists Christoforou host / Mercouris guest — route host lens to [`the-duran-channel-index.md`](../../channels/the-duran/the-duran-channel-index.md); Mercouris mechanism here",
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
            "| Host | When Mercouris is guest there |",
            "|---|---|",
            "| **Daniel Davis** | Deep Dive institutional realism — not solo Mercouris register |",
            "| **Glenn Diesen** | Karaganov triads · legitimacy dyad · Iran–Ukraine braid panels |",
            "| **The Duran** | Christoforou host register · co-host continuity on Duran shelf |",
            "| **Neutrality Studies** | Lottaz / neutrality-studies frame |",
            "",
            "## Reading rule",
            "",
            "- **Guest mechanism / cross-host Mercouris** → this index",
            "- **Mercouris solo on Alexander Mercouris channel** → [`alexander-mercouris-channel-index.md`](../../channels/alexander-mercouris/alexander-mercouris-channel-index.md)",
            "",
        ]
    )
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO)} ({total} rows)")


if __name__ == "__main__":
    main()
