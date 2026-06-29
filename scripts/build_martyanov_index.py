#!/usr/bin/env python3
"""Rebuild statecraft/voices/martyanov/martyanov-index.md from archive Martyanov captures."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ARCHIVE = REPO / "source-archive" / "statecraft"
OUT = REPO / "statecraft" / "voices" / "martyanov" / "martyanov-index.md"
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

GUEST_PREFIX_RE = re.compile(
    r"^andrei\s+martyanov:\s*",
    re.I,
)


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


def host_bucket(path: Path, meta: dict) -> str:
    name = path.name.casefold()
    if "glenn-diesen" in name or "diesen" in name and "martyanov" in name:
        return "diesen"
    if "daniel-davis" in name:
        return "davis"
    if "dialogue-works" in name:
        return "nima"
    host = (meta.get("host") or "").casefold()
    show = (meta.get("show") or "").casefold()
    slug = (meta.get("channel_slug") or "").casefold()
    if "glenn diesen" in host or slug == "glenn-diesen":
        return "diesen"
    if "daniel davis" in host or slug == "daniel-davis":
        return "davis"
    if "dialogue works" in show or slug == "dialogue-works":
        return "nima"
    return "other"


def short_title(meta: dict, path: Path) -> str:
    title = (meta.get("title") or "").strip()
    title = GUEST_PREFIX_RE.sub("", title).strip()
    if not title:
        title = path.stem.removeprefix("source-").replace("-", " ")
    if len(title) > 72:
        title = title[:69] + "…"
    return title


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
    return f"{pub} - {short_title(meta, path)}"


def row_label(meta: dict, path: Path, labels: dict[str, str]) -> str:
    text = labels.get(path.name) or default_label(meta, path)
    rel = f"../../../source-archive/statecraft/{path.parent.name}/{path.name}"
    return f"- [{text}]({rel})"


def collect_rows() -> list[tuple[str, Path, dict]]:
    rows: list[tuple[str, Path, dict]] = []
    for path in iter_archive_captures_for_shelf("martyanov", ARCHIVE):
        meta = parse_head(path)
        body = path.read_text(encoding="utf-8")[:8000]
        if shelf_utils.shelf_capture_excluded("martyanov", path, meta, body):
            continue
        pub = pub_date_key(meta, path)
        rows.append((pub, path, meta))
    rows.sort(key=lambda t: (t[0], t[1].name))
    return rows


def render_host_section(
    heading: str,
    bucket: str,
    rows: list[tuple[str, Path, dict]],
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


def render_curated_overlays() -> list[str]:
    return [
        "## Resolved 2025 Dialogue Works Bench",
        "",
        "These rows are not yet materialized into `source-archive/statecraft`, but the direct YouTube watch URLs and publish dates are already resolved from the local Dialogue Works crawl artifacts. They are shelf-relevant because they prove the 2025 Nima-side Martyanov bench is materially thicker than the currently captured direct corpus alone.",
        "",
        "- `2025-06-11` - [Russia Strikes Back: Bone-Chilling Retaliation! | Dmitry Orlov & Andrei Martyanov](https://www.youtube.com/watch?v=aTT3FlKUs68)",
        "- `2025-06-30` - [Israel's STUNNING Setback That Changes Everything | Dmitry Orlov & Andrei Martyanov](https://www.youtube.com/watch?v=rsXalm7ai-s)",
        "- `2025-07-19` - [Putin's Move Stuns the West | Dmitry Orlov & Andrei Martyanov](https://www.youtube.com/watch?v=IN8h4QX36_w)",
        "- `2025-08-03` - [Trump in DISBELIEF After Putin's BOLD Move | Andrei Martyanov & Dmitry Orlov](https://www.youtube.com/watch?v=8oOIPrnMI5g)",
        "",
        "## Host-Arc Entries",
        "",
        "- [Dialogue Works x Martyanov](../../notes/arc-martyanov-nima-host.md)",
        "- [Davis x Martyanov](../../notes/arc-martyanov-davis-host.md)",
        "- [Diesen x Martyanov](../../notes/arc-martyanov-diesen-host.md)",
        "",
        "## Reading Rule",
        "",
        "- use the direct materialized files first",
        "- use the resolved 2025 watch-URL bench next when the question is whether the Nima-side Martyanov object is actually present before full backfill",
        "- use host arcs next when the task needs host-conditioned interpretation",
        "- treat `Dialogue Works` as the strongest current branch, `Davis` as the strongest secondary branch, and `Diesen` as materially real but thinner",
        "- treat 2025 Dialogue Works as a real developing branch with a June to December mixed-guest and solo bench, not a January singleton followed by a sudden November jump",
        "- treat the January through April 2026 Dialogue Works run as a now-thickened direct bench, not a sparse bridge from January 1 straight to March",
        "- grow the bench by additional direct capture, not by symmetry",
        "",
    ]


def render_index(
    rows: list[tuple[str, Path, dict]],
    labels: dict[str, str],
    annotations: dict[str, str],
) -> str:
    date_span = f"{rows[0][0]} → {rows[-1][0]}" if rows else "—"
    diesen_n = sum(1 for r in rows if host_bucket(r[1], r[2]) == "diesen")
    davis_n = sum(1 for r in rows if host_bucket(r[1], r[2]) == "davis")
    nima_n = sum(1 for r in rows if host_bucket(r[1], r[2]) == "nima")
    other_n = sum(1 for r in rows if host_bucket(r[1], r[2]) == "other")

    lines = [
        "WORK only; not Record.",
        "",
        "# Martyanov Source Index",
        "",
        "Purpose: provide the canonical route map for materialized Martyanov appearances and the resolved watch-URL bench that explains the shelf shape before full backfill lands.",
        "",
        "**Audit:** `python scripts/audit_statecraft_archive_index.py --shelf-index martyanov` — author/guest parity; skill **`audit index`**. (_Curated rebuild via builder — no `--fix`._)",
        "",
        "## Corpus note",
        "",
        f"- **{len(rows)}** eligible archive captures on disk ({date_span})",
        "- Rebuild: `python scripts/build_martyanov_index.py`",
        f"- **{nima_n}** Dialogue Works/Nima · **{davis_n}** Davis · **{diesen_n}** Diesen · **{other_n}** other",
        "- Host buckets own first-open label transforms; curated watch-URL bench and host arcs sit beside parity rows",
        "",
        "## Direct Materialized Appearances",
        "",
    ]

    lines.extend(
        render_host_section("### Glenn Diesen", "diesen", rows, labels, annotations)
    )
    lines.extend(
        render_host_section("### Daniel Davis Deep Dive", "davis", rows, labels, annotations)
    )
    lines.extend(
        render_host_section("### Dialogue Works / Nima", "nima", rows, labels, annotations)
    )
    other = [r for r in rows if host_bucket(r[1], r[2]) == "other"]
    if other:
        lines.extend(
            render_host_section("### Other hosts", "other", rows, labels, annotations)
        )

    lines.extend(render_curated_overlays())
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
