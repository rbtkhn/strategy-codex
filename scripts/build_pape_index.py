#!/usr/bin/env python3
"""Build statecraft/voices/pape/pape-index.md from archive Pape captures."""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ARCHIVE = REPO / "source-archive" / "statecraft"
OUT = REPO / "statecraft" / "voices" / "pape" / "pape-index.md"
_SCRIPTS = REPO / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from transcript_section_curation import is_source_section_eligible  # noqa: E402

PAPE_GUEST = re.compile(r"robert\s+pape|professor\s+pape|prof\s+pape", re.I)
PAPE_AUTHOR = re.compile(r"robert\s+pape|professor\s+pape|prof\s+pape", re.I)
DATE_STUB = re.compile(r"^source-pape-\d{4}-\d{2}-\d{2}\.md$", re.I)
JANSSEN_GUEST = re.compile(
    r"cyrus\s+janssen\s+studio|pape\s*\(\s*cyrus\s+janssen|cannot beat iran|can not beat iran",
    re.I,
)
JANSSEN_TITLE = (
    "Professor Robert Pape: The US Can NOT Beat Iran (Cyrus Janssen studio)"
)
INTERVIEW_KINDS = frozenset({"transcript", "cleaned-transcript", "interview"})
INTERVIEW_FORMS = frozenset({"interview", "post"})

HOST_CROSS_REFS = {
    "daniel-davis": (
        "daniel-davis-channel-index.md",
        "../../channels/daniel-davis/daniel-davis-channel-index.md",
    ),
    "cyrus-janssen": (
        "cyrus-janssen-channel-index.md",
        "../../channels/cyrus-janssen/cyrus-janssen-channel-index.md",
    ),
    "breaking-points": (
        "breaking-points-channel-index.md",
        "../../channels/breaking-points/breaking-points-channel-index.md",
    ),
    "mario-nawfal": (
        "mario-nawfal-channel-index.md",
        "../../channels/mario-nawfal/mario-nawfal-channel-index.md",
    ),
    "moral-resistance": (
        "moral-resistance-channel-index.md",
        "../../channels/moral-resistance/moral-resistance-channel-index.md",
    ),
    "redacted-news": (
        "redacted-news-channel-index.md",
        "../../channels/redacted-news/redacted-news-channel-index.md",
    ),
}

READING_RULE_HOST_LINKS = (
    "[daniel-davis-channel-index.md](../../channels/daniel-davis/daniel-davis-channel-index.md) · "
    "[cyrus-janssen-channel-index.md](../../channels/cyrus-janssen/cyrus-janssen-channel-index.md) · "
    "[breaking-points-channel-index.md](../../channels/breaking-points/breaking-points-channel-index.md) · "
    "[mario-nawfal-channel-index.md](../../channels/mario-nawfal/mario-nawfal-channel-index.md) · "
    "[moral-resistance-channel-index.md](../../channels/moral-resistance/moral-resistance-channel-index.md) · "
    "[redacted-news-channel-index.md](../../channels/redacted-news/redacted-news-channel-index.md)"
)


def parse_head(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")[:5000]
    out: dict = {}
    for key in (
        "title",
        "pub_date",
        "kind",
        "source_form",
        "author",
        "channel_slug",
        "show",
        "host",
        "hosts",
        "guest",
        "thread",
        "youtube_id",
        "source_path",
        "transcript_curation",
    ):
        m = re.search(rf"^{key}:\s*(.+)$", text, re.M)
        if m:
            out[key] = m.group(1).strip().strip('"').strip("'")
    gp = re.search(r"^guest_people:\s*\n((?:\s+-\s+.+\n)*)", text, re.M)
    if gp:
        out["guest_people"] = [
            ln.split("-", 1)[1].strip() for ln in gp.group(1).strip().splitlines()
        ]
    if not out.get("title"):
        hm = re.search(r"^#\s+(.+)$", text, re.M)
        if hm:
            out["title"] = hm.group(1).strip()
    return out


def is_pape_guest(meta: dict, body: str = "") -> bool:
    if PAPE_GUEST.search(meta.get("guest", "")):
        return True
    for g in meta.get("guest_people") or []:
        if PAPE_GUEST.search(g):
            return True
    if JANSSEN_GUEST.search(body[:20000]):
        return True
    return False


def is_janssen_studio_capture(meta: dict, body: str) -> bool:
    return meta.get("thread") == "pape" and bool(JANSSEN_GUEST.search(body[:20000]))


def enrich_janssen_meta(meta: dict) -> None:
    meta.setdefault("title", JANSSEN_TITLE)
    meta.setdefault("host", "Cyrus Janssen")
    meta.setdefault("show", "Cyrus Janssen")
    meta.setdefault("channel_slug", "cyrus-janssen")
    meta["_janssen_note"] = "one studio session · four indexed theme segments in inbox/registry"


def enrich_breaking_points_meta(meta: dict, path: Path) -> None:
    """Ryan Grim is a Breaking Points host — route by channel slug, not person name."""
    name = path.name.lower()
    show = (meta.get("show") or "").lower()
    host = (meta.get("host") or "").lower()
    if show != "breaking points" and "breaking-points" not in name and "pape-grim" not in name:
        return
    meta.setdefault("show", "Breaking Points")
    meta["host"] = "Breaking Points"
    meta.setdefault("channel_slug", "breaking-points")


def infer_channel_slug(meta: dict, path: Path) -> None:
    if meta.get("channel_slug"):
        return
    name = path.name.lower()
    host = (meta.get("host") or "").lower()
    show = (meta.get("show") or "").lower()
    if "moral-resistance" in name:
        meta["channel_slug"] = "moral-resistance"
    elif "mario-nawfal" in name:
        meta["channel_slug"] = "mario-nawfal"
    elif "redacted" in name or "morris" in host or show == "redacted news":
        meta["channel_slug"] = "redacted-news"
    elif "cyrus-janssen" in name or "janssen" in name:
        meta["channel_slug"] = "cyrus-janssen"
    elif "daniel-davis" in name:
        meta["channel_slug"] = "daniel-davis"


def is_excluded(path: Path, meta: dict, body: str) -> bool:
    name = path.name.lower()
    if name.startswith("verify-pape-"):
        return True
    if name.startswith("x-pape-"):
        return True
    if is_janssen_studio_capture(meta, body):
        return False
    if DATE_STUB.match(path.name):
        return True
    source_path = meta.get("source_path", "")
    if "strategy-notebook/experts/pape/transcript" in source_path:
        return True
    return False


def is_included(path: Path, meta: dict, body: str) -> bool:
    if is_excluded(path, meta, body):
        return False
    if meta.get("thread") == "pape":
        return True
    if "pape" in path.name.lower():
        return True
    if is_pape_guest(meta, body):
        return True
    return False


def classify(meta: dict, path: Path, body: str) -> str:
    if is_pape_guest(meta, body):
        return "guest"
    kind = meta.get("kind", "")
    source_form = meta.get("source_form", "")
    if kind == "substack-post" or source_form == "newsletter":
        return "authored"
    author = meta.get("author", "")
    if PAPE_AUTHOR.search(author) and not is_pape_guest(meta, body):
        return "authored"
    if kind in INTERVIEW_KINDS or source_form in INTERVIEW_FORMS:
        if is_pape_guest(meta, body):
            return "guest"
    if "pape" in path.name.lower() and not is_pape_guest(meta, body):
        return "authored"
    return "authored"


def host_label(meta: dict) -> str:
    if meta.get("host"):
        return meta["host"]
    hosts = meta.get("hosts", "")
    if hosts:
        return hosts.split(";")[0].strip()
    if meta.get("show"):
        return meta["show"]
    return "?"


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
    if len(pub) >= 7:
        return pub[:7]
    return pub


def short_title(meta: dict, path: Path) -> str:
    title = meta.get("title") or path.stem.replace("source-", "", 1)
    if len(title) > 72:
        title = title[:69] + "…"
    return title


def row_label(meta: dict, path: Path, row_class: str) -> str:
    pub = pub_date_key(meta, path)
    title = short_title(meta, path)
    rel = f"../../../source-archive/statecraft/{path.parent.name}/{path.name}"
    kind = meta.get("kind") or meta.get("source_form") or ""
    if row_class == "guest":
        host = host_label(meta)
        slug = meta.get("channel_slug") or ""
        yt = meta.get("youtube_id") or ""
        yt_bit = f" (`{yt}`)" if yt else ""
        slug_bit = f" · `{slug}`" if slug else ""
        kind_bit = f" · {kind}" if kind else ""
        janssen_bit = ""
        if meta.get("_janssen_note"):
            janssen_bit = f" · _{meta['_janssen_note']}_"
        cross_bit = ""
        slug_key = (slug or "").lower()
        if slug_key in HOST_CROSS_REFS:
            xref_label, xref_rel = HOST_CROSS_REFS[slug_key]
            cross_bit = f" · cross-ref [{xref_label}]({xref_rel})"
        return (
            f"- [{pub} — {title}]({rel}){yt_bit} — **guest** · host: **{host}**{slug_bit}{kind_bit}{janssen_bit}{cross_bit}"
        )
    kind_bit = f" · {kind}" if kind else ""
    return f"- [{pub} — {title}]({rel}) — **authored**{kind_bit}"


def collect_rows() -> list[tuple[str, Path, dict, str]]:
    rows: list[tuple[str, Path, dict, str]] = []
    for path in sorted(ARCHIVE.glob("**/source-*.md")):
        body = path.read_text(encoding="utf-8")
        meta = parse_head(path)
        if not is_included(path, meta, body):
            continue
        if is_janssen_studio_capture(meta, body):
            enrich_janssen_meta(meta)
        enrich_breaking_points_meta(meta, path)
        infer_channel_slug(meta, path)
        row_class = classify(meta, path, body)
        pub = pub_date_key(meta, path)
        rows.append((pub, path, meta, row_class))
    rows.sort(key=lambda t: (t[0], t[1].name))
    return rows


def source_section_applicable(meta: dict, row_class: str) -> bool:
    guest = row_class == "guest"
    return is_source_section_eligible(meta, guest=guest)


def render_index(rows: list[tuple[str, Path, dict, str]]) -> str:
    authored = sum(1 for *_, c in rows if c == "authored")
    guest = sum(1 for *_, c in rows if c == "guest")
    total = len(rows)
    applicable = sum(1 for _, _, meta, rc in rows if source_section_applicable(meta, rc))
    sectioned = sum(
        1
        for _, _, meta, rc in rows
        if source_section_applicable(meta, rc)
        and meta.get("transcript_curation") == "curated_sectioned"
    )

    by_month: dict[str, list[tuple[str, Path, dict, str]]] = defaultdict(list)
    for row in rows:
        by_month[month_key(row[0])].append(row)

    lines = [
        "WORK only; not Record.",
        "",
        "# Pape Index",
        "",
        "Purpose: exhaustive canonical route map for Robert Pape **authored essays** and **guest appearances** in Statecraft Archive.",
        "",
        "**Audit:** `python scripts/audit_statecraft_archive_index.py --shelf-index pape` — author/guest parity; skill **`audit index`**. Post-land: `python scripts/shelf_index_from_capture.py --path <capture> --apply`. (_Curated rebuild via builder — no `--fix`._)",
        "",
        "Mechanism spine (load-bearing forecast arc): [pape-forecast-ledger-2026.md](pape-forecast-ledger-2026.md) · [Escalation Trap arc](../../notes/arc-pape-escalation-trap.md)",
        "",
        "## Corpus note",
        "",
        f"- **{authored}** authored · **{guest}** guest · **{total}** total on disk",
        f"- **{sectioned}/{applicable}** guest YouTube captures `curated_sectioned` (**source-section**; authored essays out of scope)",
        "- Rebuild: `python3 scripts/build_pape_index.py`",
        "",
        "## Boundary",
        "",
        "**Excluded from this index:** `verify-pape-*` · generic date stubs (`source-pape-YYYY-MM-DD.md`) unless **Cyrus Janssen studio** guest signal · legacy registry captures (`source_path` → strategy-notebook/experts/pape/transcript) unless Janssen studio · `x-pape-*`",
        "",
        "**Inbox-only (not indexed):** *Diary of CEO* Pape interview referenced inside Janssen material — no canonical archive capture yet.",
        "",
        "**Reading rule:**",
        "",
        "1. Authored Substack = mechanism spine — pair with [forecast ledger](pape-forecast-ledger-2026.md) and [arc](../../notes/arc-pape-escalation-trap.md).",
        f"2. Guest appearances = host-conditioned pressure tests — cross-ref host channel index when load-bearing ({READING_RULE_HOST_LINKS}).",
        "3. Same guest on another host = separate host read — do not dedupe by guest alone.",
        "4. **`source-section`** = YouTube channel transcripts only (guest interviews / solo monologues). **Not** authored Substack essays.",
        "",
    ]

    for mk in sorted(by_month.keys()):
        lines.append(f"## {mk}")
        lines.append("")
        for pub, path, meta, row_class in by_month[mk]:
            lines.append(row_label(meta, path, row_class))
        lines.append("")

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
    authored = sum(1 for *_, c in rows if c == "authored")
    guest = sum(1 for *_, c in rows if c == "guest")
    print(f"wrote {OUT.relative_to(REPO)} ({len(rows)} rows: {authored} authored, {guest} guest)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
