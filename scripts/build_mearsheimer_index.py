#!/usr/bin/env python3
"""Rebuild statecraft/voices/mearsheimer/mearsheimer-index.md from archive Mearsheimer captures."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ARCHIVE = REPO / "source-archive" / "statecraft"
OUT = REPO / "statecraft" / "voices" / "mearsheimer" / "mearsheimer-index.md"
PROFILE = OUT.parent / "mearsheimer-profile.md"
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
MEARSHEIMER_TITLE_PREFIX = re.compile(
    r"^(?:Prof\.?\s+)?(?:John\s+)?Mearsheimer(?:\s+on)?:\s*|^Professor\s+John\s+Mearsheimer\s+on\s+",
    re.I,
)

def parse_head(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")[:5000]
    out: dict = {}
    for key in ("title", "pub_date", "kind", "source_form", "host", "show", "channel_slug", "thread"):
        m = re.search(rf"^{key}:\s*(.+)$", text, re.M)
        if m:
            out[key] = m.group(1).strip().strip('"').strip("'")
    if not out.get("title"):
        hm = re.search(r"^#\s+(.+)$", text, re.M)
        if hm:
            out["title"] = hm.group(1).strip()
    if not out.get("pub_date"):
        dm = re.search(r"^date:\s*(.+)$", text, re.M)
        if dm:
            out["pub_date"] = dm.group(1).strip()
    return out

def pub_date_key(meta: dict, path: Path) -> str:
    pub = meta.get("pub_date", "")
    if pub and len(pub) >= 10:
        return pub[:10]
    day = path.parent.name
    if re.match(r"^\d{4}-\d{2}-\d{2}$", day):
        return day
    return day

def host_bucket(path: Path, meta: dict) -> str:
    name = path.name.casefold()
    host = (meta.get("host") or "").casefold()
    show = (meta.get("show") or "").casefold()
    slug = (meta.get("channel_slug") or "").casefold()
    if name.startswith("source-mearsheimer-"):
        return "authored"
    if "judging-freedom" in name and "mearsheimer" in name:
        return "napolitano"
    if "daniel-davis" in name or ("davis" in name and "mearsheimer" in name):
        return "davis"
    if ("diesen" in name or "glenn-diesen" in name) and "mearsheimer" in name:
        return "diesen"
    if "duran" in name and "mearsheimer" in name:
        return "duran"
    if "tucker-carlson" in name or ("tucker" in name and "mearsheimer" in name):
        return "tucker"
    if "hedges" in name and "mearsheimer" in name:
        return "hedges"
    if "redacted" in name and "mearsheimer" in name:
        return "redacted"
    if "americano" in name:
        return "americano"
    if "judging freedom" in show or "napolitano" in host:
        return "napolitano"
    if "daniel davis" in host or "daniel-davis" in slug:
        return "davis"
    if "glenn diesen" in host or "diesen" in slug:
        return "diesen"
    if "duran" in show or "mercouris" in slug:
        return "duran"
    if "tucker" in slug:
        return "tucker"
    if "hedges" in host or "chris hedges" in show:
        return "hedges"
    return "other"

def display_title(meta: dict) -> str:
    raw = meta.get("title") or "Untitled"
    return MEARSHEIMER_TITLE_PREFIX.sub("", raw).strip()

def load_label_map(*paths: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    for index_path in paths:
        if not index_path.is_file():
            continue
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
    title = display_title(meta)
    return f"{pub} - {title}"

def row_label(meta: dict, path: Path, labels: dict[str, str]) -> str:
    text = labels.get(path.name) or default_label(meta, path)
    rel = f"../../../source-archive/statecraft/{path.parent.name}/{path.name}"
    return f"- [{text}]({rel})"

def collect_rows() -> list[tuple[str, Path, dict]]:
    rows: list[tuple[str, Path, dict]] = []
    for path in iter_archive_captures_for_shelf("mearsheimer", ARCHIVE):
        meta = parse_head(path)
        body = path.read_text(encoding="utf-8")[:8000]
        if shelf_utils.shelf_capture_excluded("mearsheimer", path, meta, body):
            continue
        pub = pub_date_key(meta, path)
        rows.append((pub, path, meta))
    rows.sort(key=lambda t: (t[0], t[1].name))
    return rows

def render_host_section(
    heading: str,
    blurb: str,
    rows: list[tuple[str, Path, dict]],
    bucket: str,
    labels: dict[str, str],
    annotations: dict[str, str],
) -> list[str]:
    section_rows = [r for r in rows if host_bucket(r[1], r[2]) == bucket]
    if not section_rows:
        return []
    lines = [heading, "", blurb, ""]
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
        "## Curated host lanes (routing overlay)",
        "",
        "Host arcs own first-open transformations — index rows above are audit parity; open arcs when host-conditioned interpretation matters.",
        "",
        "- **Diesen × Mearsheimer** — structural realism, great-power geometry, order-transition altitude · [arc-mearsheimer-diesen-host.md](../../notes/arc-mearsheimer-diesen-host.md)",
        "- **Davis × Mearsheimer** — coercive failure, bargaining geometry, war-feasibility limits · [arc-mearsheimer-davis-host.md](../../notes/arc-mearsheimer-davis-host.md)",
        "- **Napolitano × Mearsheimer** — defeat accounting, auxiliary anti-war reinforcement · [arc-mearsheimer-napolitano-host.md](../../notes/arc-mearsheimer-napolitano-host.md)",
        "- **Speaker object:** [mearsheimer-profile.md](mearsheimer-profile.md) · [mearsheimer-routing.md](mearsheimer-routing.md) · [mearsheimer-helix.md](mearsheimer-helix.md) · compat [mearsheimer-source-index.md](mearsheimer-source-index.md)",
        "",
        "## June 2026 cadence (landed)",
        "",
        "| Pub date | Host | Mechanism lane |",
        "|----------|------|----------------|",
        "| Jun 02 | Napolitano | Israel veto on American peace |",
        "| Jun 09 | Tucker | US resumes strikes; clean exit unlikely |",
        "| Jun 11 | Davis | Iran war strategy changes again |",
        "| Jun 25 | Napolitano | (latest JF land) — see host section |",
        "",
    ]

def render_tail() -> list[str]:
    return [
        "## Reading rule",
        "",
        "1. Open **Statecraft Archive** direct files first (host sections above).",
        "2. Use **host arcs** next when the task needs host-conditioned interpretation.",
        "3. Treat **Napolitano** as reinforcing orbit unless a later pass promotes it to co-equal helix.",
        "4. Treat **authored Substack**, **Hedges**, and **Redacted** as non-core appearance bench — listed for parity, not shelf-owning chronology.",
        "5. Apply [source-lattice](../../../docs/source-lattice-beyond-the-repo.md) before lane judgment.",
        "",
        "## Boundary",
        "",
        "- This index is the canonical exhaustive route map; host-local arcs still own transformations.",
        "- Raw-text authority stays in `source-archive/statecraft/` — not legacy page mirrors under `mearsheimer-page-*`.",
        "- Do not treat routing doctrine as an audit substitute for archive parity rows.",
        "",
    ]

def render_index(
    rows: list[tuple[str, Path, dict]],
    labels: dict[str, str],
    annotations: dict[str, str],
) -> str:
    date_span = f"{rows[0][0]} → {rows[-1][0]}" if rows else "—"
    buckets = (
        "diesen",
        "davis",
        "napolitano",
        "duran",
        "tucker",
        "hedges",
        "redacted",
        "americano",
        "authored",
        "other",
    )
    counts = {b: sum(1 for r in rows if host_bucket(r[1], r[2]) == b) for b in buckets}

    lines = [
                "",
        "# Mearsheimer source index",
        "",
        "Purpose: exhaustive canonical route map for John Mearsheimer guest appearances and direct archive anchors on the Mearsheimer shelf.",
        "",
        "**Audit:** `python scripts/audit_statecraft_archive_index.py --shelf-index mearsheimer` — author/guest parity; skill **`audit index`**. (_Curated rebuild via builder — no `--fix`._)",
        "",
        "## Corpus note",
        "",
        f"- **{len(rows)}** eligible archive captures on disk ({date_span})",
        "- Rebuild: `python scripts/build_mearsheimer_index.py`",
        f"- **{counts['diesen']}** Diesen · **{counts['davis']}** Davis · **{counts['napolitano']}** Judging Freedom · **{counts['authored']}** authored · misc **{counts['duran'] + counts['tucker'] + counts['hedges'] + counts['redacted'] + counts['americano'] + counts['other']}**",
        "- Host-led mature-month shelf: host arcs own chronology; this file owns **audit parity** across all materialized appearances",
        "",
        "## Direct materialized appearances",
        "",
    ]

    host_sections = [
        (
            "### Glenn Diesen × Mearsheimer",
            "Primary structural-realism lane — highest-altitude crisis-to-system translation.",
            "diesen",
        ),
        (
            "### Daniel Davis × Mearsheimer",
            "Primary mature lane — force-versus-bargaining and punishment-failure testing ground.",
            "davis",
        ),
        (
            "### Judging Freedom × Mearsheimer",
            "Reinforcing orbit — defeat accounting and Washington-has-already-lost register.",
            "napolitano",
        ),
        (
            "### Mercouris / The Duran × Mearsheimer",
            "Panel reinforcement — usually triad with Diesen; cross-ref Mercouris shelf when load-bearing.",
            "duran",
        ),
        ("### Tucker Carlson × Mearsheimer", "Long-form reinforcement — Iran exit / lobby geometry.", "tucker"),
        ("### Chris Hedges × Mearsheimer", "Non-core appearance bench — escalation ladder / Islamabad week.", "hedges"),
        ("### Redacted × Mearsheimer", "Non-core appearance bench — fast-turn Iran war commentary.", "redacted"),
        ("### Americano × Mearsheimer", "Occasional guest lane.", "americano"),
        (
            "### Authored (Substack / shorthand)",
            "Authored or shorthand captures — parity rows; not host-local chronology substitutes.",
            "authored",
        ),
    ]
    for heading, blurb, bucket in host_sections:
        lines.extend(render_host_section(heading, blurb, rows, bucket, labels, annotations))

    other_rows = [r for r in rows if host_bucket(r[1], r[2]) == "other"]
    if other_rows:
        lines.extend(
            render_host_section(
                "### Other hosts",
                "Residual guest captures not yet bucketed to a mature host lane.",
                rows,
                "other",
                labels,
                annotations,
            )
        )

    lines.extend(render_curated_overlays())
    lines.extend(render_tail())
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

    labels = load_label_map(OUT, PROFILE)
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
