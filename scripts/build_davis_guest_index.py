#!/usr/bin/env python3
"""Build statecraft/channels/daniel-davis/davis-index.md from archive guest captures."""
from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ARCHIVE = REPO / "source-archive" / "statecraft"
OUT = REPO / "statecraft" / "channels" / "daniel-davis" / "davis-index.md"
DAVIS = re.compile(r"daniel\s+davis|lt\.?\s*col\.?\s*daniel\s+davis", re.I)


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
        "# Davis Index",
        "",
        "Purpose: route map for **Daniel Davis** as **guest / interviewed analyst on other hosts and channels** — not Daniel Davis Deep Dive host work.",
        "",
        "**Host channel (Daniel Davis):** [`daniel-davis-channel-index.md`](daniel-davis-channel-index.md)",
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
            "- **Davis as host on Deep Dive** → [`daniel-davis-channel-index.md`](daniel-davis-channel-index.md)",
            "",
        ]
    )
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO)} ({total} rows)")


if __name__ == "__main__":
    main()
