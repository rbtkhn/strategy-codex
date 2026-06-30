#!/usr/bin/env python3
"""Rebuild statecraft/voices/jiang/jiang-index.md from external interview captures."""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ARCHIVE = REPO / "source-archive" / "statecraft"
OUT = REPO / "statecraft" / "voices" / "jiang" / "jiang-index.md"
_SCRIPTS = REPO / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import shelf_index_utils as shelf_utils  # noqa: E402
from audit_statecraft_archive_index import iter_archive_captures_for_shelf  # noqa: E402
from statecraft_day_archive import read_text  # noqa: E402

LABEL_RE = re.compile(r"- \[([^\]]+)\]\([^)]*/([^/)]+)\)")
YOUTUBE_RE = re.compile(r"^https?://(?:www\.)?youtube\.com/watch\?", re.I)
GUEST_PREFIX_RE = re.compile(r"^jiang\s+xueqin:\s*", re.I)

def parse_head(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")[:5000]
    out: dict = {}
    for key in (
        "title",
        "pub_date",
        "date",
        "kind",
        "source_form",
        "host",
        "show",
        "channel_slug",
        "thread",
        "guest",
        "source_url",
    ):
        m = re.search(rf"^{key}:\s*(.+)$", text, re.M)
        if m:
            out[key] = m.group(1).strip().strip('"').strip("'")
    if not out.get("title"):
        hm = re.search(r"^#\s+(.+)$", text, re.M)
        if hm:
            out["title"] = hm.group(1).strip()
    return out

def pub_date_key(meta: dict, path: Path) -> str:
    pub = meta.get("pub_date") or meta.get("date") or ""
    if pub and len(pub) >= 10:
        return pub[:10]
    day = path.parent.name
    if re.match(r"^\d{4}-\d{2}-\d{2}$", day):
        return day
    return day

def short_title(meta: dict, path: Path) -> str:
    title = (meta.get("title") or "").strip()
    title = GUEST_PREFIX_RE.sub("", title).strip()
    if not title:
        title = path.stem.removeprefix("source-").replace("-", " ")
    if len(title) > 88:
        title = title[:85] + "…"
    return title

def host_label(meta: dict) -> str:
    host = (meta.get("host") or "").strip()
    if host:
        return host
    show = (meta.get("show") or "").strip()
    if show:
        return show
    return "host"

def youtube_url(meta: dict, path: Path) -> str:
    url = (meta.get("source_url") or "").strip()
    if not url:
        raise ValueError(f"missing source_url: {path}")
    if not YOUTUBE_RE.match(url):
        raise ValueError(f"non-YouTube source_url for jiang-index row: {path} ({url})")
    return url

def load_label_map(index_path: Path) -> dict[str, str]:
    if not index_path.is_file():
        return {}
    out: dict[str, str] = {}
    for line in read_text(index_path).splitlines():
        m = LABEL_RE.search(line)
        if not m:
            continue
        fn = m.group(2)
        if len(m.group(1)) > len(out.get(fn, "")):
            out[fn] = m.group(1)
    return out

def default_label(meta: dict, path: Path) -> str:
    pub = pub_date_key(meta, path)
    host = host_label(meta)
    return f"{pub} | {host} × Jiang | {short_title(meta, path)}"

def row_label(meta: dict, path: Path, labels: dict[str, str]) -> str:
    text = labels.get(path.name) or default_label(meta, path)
    rel = f"../../../source-archive/statecraft/{path.parent.name}/{path.name}"
    url = youtube_url(meta, path)
    host = host_label(meta)
    return f"- [{text}]({rel}) — **guest** · {host} · [YouTube]({url})"

def collect_rows() -> list[tuple[str, Path, dict]]:
    rows: list[tuple[str, Path, dict]] = []
    for path in iter_archive_captures_for_shelf("jiang", ARCHIVE):
        meta = parse_head(path)
        body = path.read_text(encoding="utf-8")[:8000]
        if not shelf_utils.is_jiang_external_interview(meta, path, body):
            continue
        pub = pub_date_key(meta, path)
        rows.append((pub, path, meta))
    rows.sort(key=lambda t: (t[0], t[1].name))
    return rows

def render_index(rows: list[tuple[str, Path, dict]], labels: dict[str, str]) -> str:
    date_span = f"{rows[0][0]} → {rows[-1][0]}" if rows else "—"
    by_month: dict[str, list[tuple[str, Path, dict]]] = defaultdict(list)
    for row in rows:
        pub = row[0]
        month = pub[:7] if len(pub) >= 7 else pub
        by_month[month].append(row)

    lines = [
        "# Jiang external interview index",
        "",
                "",
        "Purpose: canonical **external-channel** guest interview index for **Jiang Xueqin**.",
        "",
        "**Audit:** `python scripts/audit_statecraft_archive_index.py --shelf-index jiang` — interview parity only.",
        "",
        "## Surface Grammar",
        "",
        "- **Surface name:** `jiang-index.md`",
        "- **Surface role:** guest interview bench (third-party channels only)",
        "- **Surface interior:** Diesen, Sneako, and other non–Predictive History host appearances",
        "",
        "**PH channel + essays:** [jiang-predictive-history-master-index.md](jiang-predictive-history-master-index.md) · [jiang-predictive-history-index.md](../../../source-archive/statecraft/jiang-predictive-history-index.md)",
        "",
        "## Corpus note",
        "",
        f"- **{len(rows)}** eligible external interview capture(s) on disk ({date_span})",
        "- Rebuild: `python scripts/build_jiang_index.py`",
        "- Each row carries an inline YouTube link from capture `source_url`",
        "- **Sneako #15** is dual-indexed here and in the PH archive Interviews table",
        "",
    ]

    for month in sorted(by_month, reverse=True):
        lines.append(f"## {month}")
        lines.append("")
        for _pub, path, meta in sorted(by_month[month], key=lambda t: (t[0], t[1].name)):
            lines.append(row_label(meta, path, labels))
        lines.append("")

    lines.extend(
        [
            "## Host routing",
            "",
            "| Host | Index |",
            "| --- | --- |",
            "| Glenn Diesen | [glenn-diesen-channel-index](../../channels/glenn-diesen/glenn-diesen-channel-index.md) |",
            "",
            "## Boundary notes",
            "",
            "- **Not listed here:** Game Theory, Great Books, Founding Members, Substack essays, solo PH lectures (`thread: jiang` on PH-owned captures).",
            "- **Not listed here:** panels *about* Jiang without him as guest (e.g. Dialogue Works).",
            "- **Routing / counts:** [jiang-routing.md](jiang-routing.md) · [jiang-predictive-history-master-index.md](jiang-predictive-history-master-index.md)",
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

    labels = load_label_map(OUT)
    try:
        body = render_index(rows, labels)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.check:
        print(f"rows: {len(rows)}")
        print(f"labels preserved: {len(labels)}")
        return 0

    OUT.write_text(body if body.endswith("\n") else body + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {OUT} ({len(rows)} rows, {len(labels)} labels preserved)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
