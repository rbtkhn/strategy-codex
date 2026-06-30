#!/usr/bin/env python3
"""Build statecraft/voices/mercouris/mercouris-index.md from archive guest captures."""
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
OUT = REPO / "statecraft" / "voices" / "mercouris" / "mercouris-index.md"

HEADER = """

# Mercouris Index

Purpose: primary route map for **Alexander Mercouris** — guest captures on other hosts; pair with analytical bench and host channel below.

## Open first

| Surface | Path | Job |
|---|---|---|
| **Guest captures (this file)** | `mercouris-index.md` | Cross-host guest appearances (`channel_slug` ≠ `alexander-mercouris`) |
| **Analytical bench** | [mercouris-analytical-bench.md](mercouris-analytical-bench.md) | Month hinges, cross-weaves, prehistory anchors |
| **Host channel** | [alexander-mercouris-channel-index.md](../../channels/alexander-mercouris/alexander-mercouris-channel-index.md) | Solo `@AlexMercouris` uploads |
| **Compat redirect** | [mercouris-source-index.md](mercouris-source-index.md) | Back-compat entry only |

## Boundary

| Route here | Route to Alexander Mercouris channel shelf |
|---|---|
| `guest:` / `guest_people:` / `guest_2:` … Mercouris on **another** `channel_slug` | `source-alexander-mercouris-*` · solo monologues on `@AlexMercouris` |
| Cross-host analyst continuity (Davis, Diesen, Duran, Neutrality Studies, …) | Host-conditioned framing on that channel |

Do **not** dedupe by calendar day alone — same analyst on Davis vs Diesen vs Duran = distinct host reads.

## Corpus note

- **{total}** materialized cross-host guest captures on disk; expand as archive grows
- Filename families: `source-duran-mercouris-*` · `source-daniel-davis-*mercouris*` · `source-glenn-diesen-*mercouris*` · explicit Mercouris in `guest` / `guest_people` / `guest_2` with `channel_slug` ≠ `alexander-mercouris`
- **The Duran:** YAML lists Christoforou host / Mercouris guest — route host lens to [`the-duran-channel-index.md`](../../channels/the-duran/the-duran-channel-index.md); Mercouris mechanism here
"""

FOOTER = """## Host cross-refs

| Host | When Mercouris is guest there |
|---|---|
| **Daniel Davis** | Deep Dive institutional realism — not solo Mercouris register |
| **Glenn Diesen** | Karaganov triads · legitimacy dyad · Iran–Ukraine braid panels |
| **The Duran** | Christoforou host register · co-host continuity on Duran shelf |
| **Neutrality Studies** | Lottaz / neutrality-studies frame |

## Reading rule

- **Guest mechanism / cross-host Mercouris** → this index
- **Analytical bench (hinges / weaves)** → [mercouris-analytical-bench.md](mercouris-analytical-bench.md)
- **Mercouris solo on Alexander Mercouris channel** → [`alexander-mercouris-channel-index.md`](../../channels/alexander-mercouris/alexander-mercouris-channel-index.md)
"""

def parse_head(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")[:4000]
    out: dict = {}
    for key in ("title", "channel_slug", "show", "host", "guest", "thread", "youtube_id"):
        m = re.search(rf"^{key}:\s*(.+)$", text, re.M)
        if m:
            val = m.group(1).strip().strip('"').replace('\\"', '"')
            out[key] = val
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
    return f"- [{path.parent.name} — {title}](../../../source-archive/statecraft/{path.parent.name}/{path.name}){yt_bit} — host: **{host}**{slug_bit}"

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
        if shelf_utils.is_mercouris_guest_index_capture(meta, path):
            by_month[month_key(path.parent.name)].append((path, meta))

    total = sum(len(v) for v in by_month.values())
    lines = [HEADER.format(total=total), ""]
    for mk in sorted(by_month.keys()):
        lines.append(f"## {mk}")
        lines.append("")
        for path, meta in sorted(by_month[mk], key=lambda t: t[0].name):
            lines.append(row_label(meta, path))
        lines.append("")
    lines.append(FOOTER.rstrip())
    content = "\n".join(lines) + "\n"

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
