#!/usr/bin/env python3
"""Build statecraft/voices/blumenthal/blumenthal-index.md from archive guest captures."""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ARCHIVE = REPO / "source-archive" / "statecraft"
OUT = REPO / "statecraft" / "voices" / "blumenthal" / "blumenthal-index.md"
_SCRIPTS = REPO / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from transcript_section_curation import is_source_section_eligible  # noqa: E402

BLUMENTHAL = re.compile(r"max\s+blumenthal", re.I)
PANIC_TITLE = re.compile(
    r"blumenthal\s*:\s*israel\s+in\s+panic|is\s+israel\s+in\s+panic",
    re.I,
)

RESIDUE_STUBS = (
    ("2026-04-25", "../../sheets/source-archive-residue/2026-04-25/2026-04-25-blumenthal.md"),
    ("2026-04-26", "../../sheets/source-archive-residue/2026-04-26/2026-04-26-blumenthal.md"),
    ("2026-04-27", "../../sheets/source-archive-residue/2026-04-27/2026-04-27-blumenthal.md"),
    ("2026-04-28", "../../sheets/source-archive-residue/2026-04-28/2026-04-28-blumenthal.md"),
)

HOST_CROSS_REFS = {
    "glenn-diesen": ("diesen-index.md", "../diesen/diesen-index.md"),
    "judging-freedom": (
        "judging-freedom-channel-index.md",
        "../../channels/judging-freedom/judging-freedom-channel-index.md",
    ),
    "mario-nawfal": (
        "mario-nawfal-channel-index.md",
        "../../channels/mario-nawfal/mario-nawfal-channel-index.md",
    ),
}


def split_frontmatter(text: str) -> tuple[str, str]:
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            return parts[1], parts[2]
    return "", text


def parse_head(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    fm, body = split_frontmatter(text)
    scan = fm + "\n" + body[:4000]
    out: dict = {}
    for key in (
        "title",
        "pub_date",
        "kind",
        "source_form",
        "channel_slug",
        "show",
        "host",
        "guest",
        "thread",
        "youtube_id",
        "source_url",
        "transcript_curation",
        "verify_matrix_ref",
    ):
        m = re.search(rf"^{key}:\s*(.+)$", scan, re.M)
        if m:
            val = m.group(1).strip().strip('"').strip("'")
            out[key] = val.replace('\\"', '"')
    gp = re.search(r"^guest_people:\s*\n((?:\s+-\s+.+\n)*)", scan, re.M)
    if gp:
        out["guest_people"] = [
            ln.split("-", 1)[1].strip() for ln in gp.group(1).strip().splitlines()
        ]
    th = re.search(r"^threads:\s*\n((?:\s+-\s+.+\n)*)", scan, re.M)
    if th:
        out["threads"] = [ln.split("-", 1)[1].strip() for ln in th.group(1).strip().splitlines()]
    if not out.get("title"):
        hm = re.search(r"^#\s+(.+)$", body, re.M)
        if hm:
            out["title"] = hm.group(1).strip()
    if not out.get("youtube_id"):
        url = out.get("source_url") or ""
        ym = re.search(r"(?:v=|youtu\.be/)([A-Za-z0-9_-]{11})", url)
        if ym:
            out["youtube_id"] = ym.group(1)
    if not out.get("channel_slug"):
        name = path.name.lower()
        for slug in HOST_CROSS_REFS:
            if slug.replace("-", "-") in name or slug.replace("-", "_") in name:
                out["channel_slug"] = slug
                break
        if "mario-nawfal" in name:
            out["channel_slug"] = "mario-nawfal"
        elif "glenn-diesen" in name or "diesen" in name and "blumenthal" in name:
            out["channel_slug"] = "glenn-diesen"
        elif "judging-freedom" in name or "blumenthal-judging-freedom" in name:
            out["channel_slug"] = "judging-freedom"
    out["_section_count"] = len(re.findall(r"^### ", body, re.M))
    return out


def is_blumenthal_guest(meta: dict) -> bool:
    if BLUMENTHAL.search(meta.get("guest", "")):
        return True
    for g in meta.get("guest_people") or []:
        if BLUMENTHAL.search(g):
            return True
    return False


def is_included(path: Path, meta: dict) -> bool:
    name = path.name.lower()
    if name.startswith("verify-blumenthal-"):
        return False
    if meta.get("thread") == "blumenthal":
        return True
    if "blumenthal" in (meta.get("threads") or []):
        return True
    if "blumenthal" in name:
        return True
    return is_blumenthal_guest(meta)


def pub_date_key(meta: dict, path: Path) -> str:
    pub = meta.get("pub_date", "")
    if pub and len(pub) >= 10:
        return pub[:10]
    day = path.parent.name
    if re.match(r"^\d{4}-\d{2}-\d{2}$", day):
        return day
    return day


def month_key(pub: str) -> str:
    if pub == "_aired-pending":
        return pub
    return pub[:7] if len(pub) >= 7 else pub


def short_title(meta: dict, path: Path) -> str:
    title = meta.get("title") or path.stem.replace("source-", "", 1)
    if len(title) > 72:
        title = title[:69] + "…"
    return title


def host_bucket(meta: dict) -> str:
    slug = (meta.get("channel_slug") or "").lower()
    if slug == "judging-freedom":
        return "Judging Freedom"
    if slug == "glenn-diesen":
        return "Glenn Diesen"
    if slug == "mario-nawfal":
        return "Mario Nawfal"
    host = (meta.get("host") or "").strip()
    if host.lower() == "nemo":
        return "Nemo solo"
    if "napolitano" in host.lower() or slug == "judging-freedom":
        return "Judging Freedom"
    return host or meta.get("show") or "other"


def section_note(meta: dict) -> str:
    n = meta.get("_section_count", 0)
    if n:
        return f"**{n}§**"
    kind = meta.get("kind") or ""
    if kind == "operator-transcript":
        return ""
    return ""


def verify_note(meta: dict, pub: str) -> str:
    if not meta.get("_has_verify"):
        return ""
    ref = meta.get("verify_matrix_ref") or ""
    if "2026-06-25" in ref or pub == "2026-06-25":
        return "`verify:` J25"
    return "`verify:`"


def row_suffix(meta: dict, path: Path, pub: str) -> str:
    bits: list[str] = []
    sec = section_note(meta)
    if sec:
        bits.append(sec)
    v = verify_note(meta, pub)
    if v:
        bits.append(v)
    slug = (meta.get("channel_slug") or "").lower()
    if slug in HOST_CROSS_REFS:
        _, rel = HOST_CROSS_REFS[slug]
        bits.append(f"cross-ref [{HOST_CROSS_REFS[slug][0]}]({rel})")
    title = meta.get("title") or ""
    if pub == "2026-06-18" and PANIC_TITLE.search(title):
        bits.append("**not** Jun 25 duplicate")
    if pub == "2026-04-21":
        bits.append("speaker-object anchor · pin canonical `watch?v=` when confirmed")
    return " · ".join(bits)


def row_label(meta: dict, path: Path, pub: str) -> str:
    title = short_title(meta, path)
    rel = f"../../../source-archive/statecraft/{path.parent.name}/{path.name}"
    host = meta.get("host") or meta.get("show") or "?"
    slug = meta.get("channel_slug") or ""
    kind = meta.get("kind") or meta.get("source_form") or ""
    yt = meta.get("youtube_id") or ""
    yt_bit = f" (`{yt}`)" if yt else ""
    slug_bit = f" · `{slug}`" if slug else ""
    kind_bit = f" · {kind}" if kind else ""
    suffix = row_suffix(meta, path, pub)
    suffix_bit = f" · {suffix}" if suffix else ""
    return (
        f"- [{pub} — {title}]({rel}){yt_bit} — **guest** · host: **{host}**"
        f"{slug_bit}{kind_bit}{suffix_bit}"
    )


def collect_rows() -> list[tuple[str, Path, dict]]:
    rows: list[tuple[str, Path, dict]] = []
    for path in sorted(ARCHIVE.glob("**/source-*.md")):
        meta = parse_head(path)
        if not is_included(path, meta):
            continue
        if not is_blumenthal_guest(meta) and meta.get("thread") != "blumenthal":
            if "blumenthal" not in path.name.lower():
                continue
        pub = pub_date_key(meta, path)
        rows.append((pub, path, meta))
    rows.sort(key=lambda t: (t[0], t[1].name))
    return rows


def panic_youtube_ids(rows: list[tuple[str, Path, dict]]) -> list[tuple[str, str]]:
    panic_rows: list[tuple[str, str]] = []
    for pub, _, meta in rows:
        title = meta.get("title") or ""
        yt = meta.get("youtube_id") or ""
        if yt and PANIC_TITLE.search(title):
            panic_rows.append((pub, yt))
    return sorted(panic_rows)


def corpus_section_line(rows: list[tuple[str, Path, dict]]) -> str:
    chunks: list[str] = []
    for pub, _, meta in rows:
        if not pub.startswith("2026-06"):
            continue
        label = pub[5:10] if len(pub) >= 10 else pub
        sec = section_note(meta)
        v = verify_note(meta, pub)
        piece = label
        if sec and "§" in sec:
            piece += f" {sec}"
        elif sec:
            piece += f" {sec}"
        if v:
            piece += f" + {v}"
        chunks.append(piece)
    tail = "May rows flat transcript; Apr 21 operator ASR (flat)"
    if chunks:
        return "; ".join(chunks) + "; " + tail
    return tail


def host_split_line(rows: list[tuple[str, Path, dict]]) -> str:
    counts = Counter(host_bucket(meta) for _, _, meta in rows)
    bits = []
    for label in ("Judging Freedom", "Glenn Diesen", "Mario Nawfal", "Nemo solo"):
        n = counts.get(label, 0)
        if n:
            bits.append(f"**{label} ×{n}**")
    for label, n in sorted(counts.items()):
        if label not in ("Judging Freedom", "Glenn Diesen", "Mario Nawfal", "Nemo solo") and n:
            bits.append(f"**{label} ×{n}**")
    return " · ".join(bits)


def duplicate_panic_note(rows: list[tuple[str, Path, dict]]) -> str:
    panic_rows = panic_youtube_ids(rows)
    if len(panic_rows) < 2:
        return ""
    ids = " vs ".join(f"`{yt}`" for _, yt in panic_rows)
    return (
        f"- **Duplicate-title pair:** Jun 18 *Israel In Panic* vs Jun 25 *Is Israel in Panic?* "
        f"({ids}) — **distinct episodes**; do not merge by title alone"
    )


def render_index(rows: list[tuple[str, Path, dict]]) -> str:
    total = len(rows)
    if not rows:
        raise SystemExit("no Blumenthal archive rows found")

    pub_min = min(r[0] for r in rows)
    pub_max = max(r[0] for r in rows)

    by_month: dict[str, list[tuple[str, Path, dict]]] = defaultdict(list)
    for row in rows:
        by_month[month_key(row[0])].append(row)

    lines = [
        "WORK only; not Record.",
        "",
        "# Blumenthal Index",
        "",
        "Purpose: exhaustive canonical route map for **Max Blumenthal guest appearances** in Statecraft Archive.",
        "",
        "Shelf routing: [blumenthal-speaker-object.md](blumenthal-speaker-object.md) · "
        "[blumenthal-cross-host-note.md](blumenthal-cross-host-note.md)",
        "",
        "## Corpus note",
        "",
        f"- **{total}** archive guest captures on disk (**{pub_min}** → **{pub_max}**)",
        f"- Host split: {host_split_line(rows)}",
        f"- **Section / verify:** {corpus_section_line(rows)}",
    ]
    dup = duplicate_panic_note(rows)
    if dup:
        lines.append(dup)
    lines.append("- Rebuild: `python3 scripts/build_blumenthal_index.py`")

    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "**SSOT:** `source-archive/statecraft/` — not legacy `codex/years/…/provenance/` · not `raw-input` mirrors.",
            "",
            "**Reading rules:**",
            "",
            "1. Same guest on another host = separate host read — cross-ref host channel index when load-bearing "
            "([judging-freedom-channel-index.md](../../channels/judging-freedom/judging-freedom-channel-index.md) · "
            "[diesen-index.md](../diesen/diesen-index.md) · "
            "[mario-nawfal-channel-index.md](../../channels/mario-nawfal/mario-nawfal-channel-index.md)).",
            "2. Blumenthal = **commentary / media-legitimacy amplifier** — do not substitute for Marandi process register or Pape mechanism spine.",
            "3. Do not dedupe Jun 18 / Jun 25 “panic” episodes by title alone.",
            "",
        ]
    )

    for mk in sorted(by_month.keys(), reverse=True):
        lines.append(f"## {mk}")
        lines.append("")
        month_rows = sorted(by_month[mk], key=lambda t: (t[0], t[1].name), reverse=True)
        for pub, path, meta in month_rows:
            lines.append(row_label(meta, path, pub))
        lines.append("")

    lines.extend(
        [
            "## Secondary — discovery / residue",
            "",
            "Residue stubs are **pointers only** — not transcript SSOT.",
            "",
        ]
    )
    for day, rel in RESIDUE_STUBS:
        lines.append(f"- [{day} — residue pointer]({rel})")
    lines.extend(
        [
            "- [dialogue-works-inventory.md](../../sheets/source-archive-control/dialogue-works-inventory.md) — discovery surface only",
            "",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit 1 if generated index would differ from file on disk",
    )
    args = parser.parse_args()

    rows = collect_rows()
    content = render_index(rows)

    if args.check:
        if OUT.is_file() and OUT.read_text(encoding="utf-8") == content:
            print(f"OK {OUT.relative_to(REPO)} ({len(rows)} rows)")
            return 0
        print(f"STALE {OUT.relative_to(REPO)} ({len(rows)} rows)", file=sys.stderr)
        return 1

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(content, encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO)} ({len(rows)} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
