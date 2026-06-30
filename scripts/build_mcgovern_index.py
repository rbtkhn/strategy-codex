#!/usr/bin/env python3
"""Rebuild statecraft/voices/mcgovern/mcgovern-index.md from archive McGovern captures."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ARCHIVE = REPO / "source-archive" / "statecraft"
OUT = REPO / "statecraft" / "voices" / "mcgovern" / "mcgovern-index.md"
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
    r"^(?:(?:ray\s+)?mcgovern:\s*|intel\s+roundtable\s+w/\s+johnson\s+&\s+mcgovern:\s*)",
    re.I,
)

CADENCE_TAIL_MARKER = "## June 2026 cadence (landed)"


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
    if "consortium-news" in name or "consortium_news" in name:
        return "debate"
    if "glenn-diesen" in name or ("diesen" in name and "mcgovern" in name):
        return "diesen"
    if "dialogue-works" in name or "mcgovern-dialogue" in name:
        return "nima"
    if "judging-freedom" in name and "mcgovern" in name:
        return "judging"
    host = (meta.get("host") or "").casefold()
    show = (meta.get("show") or "").casefold()
    slug = (meta.get("channel_slug") or "").casefold()
    if "glenn diesen" in host or slug == "glenn-diesen":
        return "diesen"
    if "dialogue works" in show or slug == "dialogue-works":
        return "nima"
    if "judging freedom" in show or slug == "judging-freedom":
        return "judging"
    if "napolitano" in host:
        return "judging"
    return "other"


def short_title(meta: dict, path: Path) -> str:
    title = (meta.get("title") or "").strip()
    title = GUEST_PREFIX_RE.sub("", title).strip()
    if title.lower().startswith("ray mcgovern:"):
        title = title.split(":", 1)[1].strip()
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


def load_preserved_cadence_tail(index_path: Path) -> str:
    if not index_path.is_file():
        return ""
    text = read_text(index_path)
    marker = text.find(CADENCE_TAIL_MARKER)
    if marker < 0:
        return ""
    return text[marker:].rstrip() + "\n"


def default_label(meta: dict, path: Path) -> str:
    pub = pub_date_key(meta, path)
    return f"{pub} - {short_title(meta, path)}"


def row_label(meta: dict, path: Path, labels: dict[str, str]) -> str:
    text = labels.get(path.name) or default_label(meta, path)
    rel = f"../../../source-archive/statecraft/{path.parent.name}/{path.name}"
    return f"- [{text}]({rel})"


def collect_rows() -> list[tuple[str, Path, dict]]:
    rows: list[tuple[str, Path, dict]] = []
    for path in iter_archive_captures_for_shelf("mcgovern", ARCHIVE):
        meta = parse_head(path)
        body = path.read_text(encoding="utf-8")[:8000]
        if shelf_utils.shelf_capture_excluded("mcgovern", path, meta, body):
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


def render_curated_overlays(cadence_tail: str) -> list[str]:
    lines = [
        "## Host-Arc Entries",
        "",
        "- [Diesen x McGovern](../../notes/arc-mcgovern-diesen-host.md)",
        "- [Dialogue Works x McGovern](../../notes/arc-mcgovern-nima-host.md)",
        "",
        "## Reading Rule",
        "",
        "- use the direct materialized files first",
        "- use host arcs next when the task needs host-conditioned interpretation",
        "- treat the Judging Freedom branch as materially real but not yet a co-equal helix strand",
        "- treat the Consortium News debate as non-core stress-test material, not shelf-shaping host law",
        "",
    ]
    if cadence_tail:
        lines.append(cadence_tail.rstrip())
        lines.append("")
    return lines


def render_index(
    rows: list[tuple[str, Path, dict]],
    labels: dict[str, str],
    annotations: dict[str, str],
    cadence_tail: str,
) -> str:
    diesen_n = sum(1 for r in rows if host_bucket(r[1], r[2]) == "diesen")
    nima_n = sum(1 for r in rows if host_bucket(r[1], r[2]) == "nima")
    judging_n = sum(1 for r in rows if host_bucket(r[1], r[2]) == "judging")
    debate_n = sum(1 for r in rows if host_bucket(r[1], r[2]) == "debate")
    other_n = sum(1 for r in rows if host_bucket(r[1], r[2]) == "other")

    lines = [
        "WORK only; not Record.",
        "",
        "# McGovern Source Index",
        "",
        "Purpose: provide the canonical route map for materialized McGovern appearances and the smaller set of direct archive anchors that explain the shelf shape.",
        "",
        "**Audit:** `python scripts/audit_statecraft_archive_index.py --shelf-index mcgovern` — author/guest parity; skill **`audit index`**. Rebuild: `python scripts/build_mcgovern_index.py` · post-land: `python scripts/shelf_index_from_capture.py --path <capture> --apply`.",
        "",
        "## Direct Materialized Appearances",
        "",
    ]

    lines.extend(render_host_section("### Glenn Diesen", "diesen", rows, labels, annotations))
    lines.extend(render_host_section("### Dialogue Works / Nima", "nima", rows, labels, annotations))
    lines.extend(render_host_section("### Judging Freedom", "judging", rows, labels, annotations))
    lines.extend(render_host_section("### Debate / Non-core", "debate", rows, labels, annotations))
    other = [r for r in rows if host_bucket(r[1], r[2]) == "other"]
    if other:
        lines.extend(render_host_section("### Other hosts", "other", rows, labels, annotations))

    lines.extend(render_curated_overlays(cadence_tail))

    # Corpus note kept minimal at end of header in future; counts for operator receipt only in CLI.
    _ = (diesen_n, nima_n, judging_n, debate_n, other_n)
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Print row count only")
    parser.add_argument("--check", action="store_true", help="Compare row count to index links")
    args = parser.parse_args()

    rows = collect_rows()
    if args.dry_run:
        print(f"rows: {len(rows)}")
        for pub, path, _ in rows:
            print(f"  {pub} {path.name}")
        return 0

    labels = load_label_map(OUT)
    annotations = load_annotation_map(OUT)
    cadence_tail = load_preserved_cadence_tail(OUT)
    body = render_index(rows, labels, annotations, cadence_tail)
    if args.check:
        print(f"rows: {len(rows)}")
        print(f"labels preserved: {len(labels)}")
        print(f"annotations preserved: {len(annotations)}")
        print(f"cadence tail: {'yes' if cadence_tail else 'no'}")
        return 0

    OUT.write_text(body if body.endswith("\n") else body + "\n", encoding="utf-8", newline="\n")
    print(
        f"wrote {OUT} ({len(rows)} rows, {len(labels)} labels preserved, "
        f"{len(annotations)} annotations preserved)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
