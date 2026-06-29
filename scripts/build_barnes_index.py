#!/usr/bin/env python3
"""Rebuild statecraft/voices/barnes/barnes-index.md from archive Barnes captures."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ARCHIVE = REPO / "source-archive" / "statecraft"
OUT = REPO / "statecraft" / "voices" / "barnes" / "barnes-index.md"
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
    if "kent-exit-ramp" in name or (name.startswith("source-barnes-") and "kent" in name):
        return "xpost"
    if "countercurrent" in name:
        return "support_johnson"
    if re.match(r"source-barnes-\d{4}-\d{2}-\d{2}\.md$", name):
        return "support_johnson"
    if name.startswith("source-barnes-") and "trump-informed" in name:
        return "nawfal"
    if "daniel-davis" in name:
        return "davis"
    if "duran" in name and "barnes" in name:
        return "duran"
    if "dialogue-works" in name and "barnes" in name:
        return "nima"
    if "mario-nawfal" in name or "barnes-mario-nawfal" in name:
        return "nawfal"
    if "judging-freedom" in name:
        return "napolitano"
    host = (meta.get("host") or "").casefold()
    show = (meta.get("show") or "").casefold()
    slug = (meta.get("channel_slug") or "").casefold()
    if "daniel davis" in host or "daniel-davis" in slug:
        return "davis"
    if "dialogue works" in show or slug == "dialogue-works":
        return "nima"
    if "mario nawfal" in host or "nawfal" in slug:
        return "nawfal"
    if "judging freedom" in show or "napolitano" in host:
        return "napolitano"
    if show and "duran" in show.casefold():
        return "duran"
    return "other"


def kind_prefix(meta: dict, path: Path) -> str:
    name = path.name.casefold()
    kind = (meta.get("kind") or "").casefold()
    if "countercurrent" in name or "verbatim" in kind:
        return "verbatim sidecar"
    if re.match(r"source-barnes-\d{4}-\d{2}-\d{2}\.md$", name):
        if "04-18" in name:
            return "shorthand transcript carry-forward note"
        return "shorthand transcript note"
    if "kent" in name:
        return "Barnes quote-post of Joe Kent: exit ramp vs escalation ramp"
    if "alert" in name or "companion" in (meta.get("source_note") or "").casefold():
        return "transcript-bearing companion capture"
    if "cleaned-transcript" in kind or kind == "transcript":
        return "transcript"
    if "transcript" in kind:
        return "transcript-bearing capture"
    return "transcript"


def load_label_map(index_path: Path) -> dict[str, str]:
    if not index_path.is_file():
        return {}
    out: dict[str, str] = {}
    for line in read_text(index_path).splitlines():
        m = LABEL_RE.search(line)
        if m:
            out[m.group(2)] = m.group(1)
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
    prefix = kind_prefix(meta, path)
    name = path.name.casefold()
    if "kent" in name:
        return f"{pub} - {prefix}"
    title = meta.get("title") or "Untitled"
    if prefix in ("shorthand transcript note", "shorthand transcript carry-forward note"):
        return f"{pub} - {prefix}"
    if prefix == "verbatim sidecar":
        return f"{pub} - {prefix} - {title}"
    if prefix == "transcript-bearing companion capture":
        return f"{pub} - {prefix} - {title}"
    return f"{pub} - {prefix} - {title}"


def row_label(meta: dict, path: Path, labels: dict[str, str]) -> str:
    text = labels.get(path.name) or default_label(meta, path)
    rel = f"../../../source-archive/statecraft/{path.parent.name}/{path.name}"
    return f"- [{text}]({rel})"


def collect_rows() -> list[tuple[str, Path, dict]]:
    rows: list[tuple[str, Path, dict]] = []
    for path in iter_archive_captures_for_shelf("barnes", ARCHIVE):
        meta = parse_head(path)
        body = path.read_text(encoding="utf-8")[:8000]
        if shelf_utils.shelf_capture_excluded("barnes", path, meta, body):
            continue
        pub = pub_date_key(meta, path)
        rows.append((pub, path, meta))
    rows.sort(key=lambda t: (t[0], t[1].name))
    return rows


def render_host_section(
    heading: str,
    blurb: str,
    bucket: str,
    rows: list[tuple[str, Path, dict]],
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


def render_open_first() -> list[str]:
    return [
        "## Open first by corpus layer",
        "",
        "- **Best mature lane:** [Davis host shelf](../../channels/daniel-davis/README.md)",
        "- **Best non-Davis lane:** [2026-04-23 / Mercouris x Barnes](../../../source-archive/statecraft/2026-04-23/source-duran-mercouris-barnes-fractured-iran-trump-2026-04-23.md)",
        "- **Best late-May reinforcement:** [2026-05-26 / Nima x Barnes](../../../source-archive/statecraft/2026-05-26/source-dialogue-works-barnes-us-iran-final-confrontation-as-russia-drops-heaviest-strikes-on-ukraine-yet-2026-05-26.md)",
        "- **Best fast public-pressure entry:** [2026-06-03 / Mario Nawfal x Barnes](../../../source-archive/statecraft/2026-06-03/source-barnes-trump-informed-iran-may-have-nukes-2026-06-03.md)",
        "- **Best latest mature lane:** [2026-06-26 / Davis x Barnes — Iran deal miscalculations](../../../source-archive/statecraft/2026-06-26/source-daniel-davis-robert-barnes-iran-deal-miscalculations-2026-06-26.md)",
        "- **Best June public-pressure cluster:** [2026-06-10 / Napolitano x Barnes](../../../source-archive/statecraft/2026-06-10/source-judging-freedom-barnes-how-trump-makes-decisions-2026-06-10.md) + [2026-06-10 / Nima x Barnes](../../../source-archive/statecraft/2026-06-10/source-dialogue-works-barnes-us-attacks-iran-jordan-bahrain-kuwait-hit-within-hours-2026-06-10.md)",
        "- **Best MOU-week tail:** [2026-06-25 / Nawfal GCC–Rubio](../../../source-archive/statecraft/2026-06-25/source-mario-nawfal-barnes-breaking-gcc-attack-iran-rubio-meeting-iran-strike-vessel-hormuz-2026-06-25.md) + [2026-06-26 / Nima drones without state approval](../../../source-archive/statecraft/2026-06-26/source-dialogue-works-robert-barnes-iran-drones-ship-without-state-approval-2026-06-26.md)",
        "",
    ]


def render_boundary() -> list[str]:
    return [
        "## Boundary",
        "",
        "- The primary guest corpus defines the Barnes object.",
        "- The public-pressure reinforcement branch is real, but it is not yet a co-equal mature host lane.",
        "- The support-tier captures widen routing confidence but do not create a new mature lane by themselves.",
        "- The May 26 Nima source is primary-corpus evidence.",
        "- The late-May and early-June Barnes additions strengthen the public-pressure branch and thicken Nima as a real reinforcing lane, but they do not yet displace Davis as the primary mature corpus.",
        "- The June 8–26 cluster (Nawfal, Napolitano, Nima, Davis) is same-week continuity evidence — route Davis first for mature lane, then the June 10 pair for fast-turn reinforcement; Jun 25–26 extend MOU-week Hormuz/GCC tail.",
        "",
    ]


def render_index(
    rows: list[tuple[str, Path, dict]],
    labels: dict[str, str],
    annotations: dict[str, str],
) -> str:
    date_span = f"{rows[0][0]} → {rows[-1][0]}" if rows else "—"
    davis_n = sum(1 for r in rows if host_bucket(r[1], r[2]) == "davis")
    duran_n = sum(1 for r in rows if host_bucket(r[1], r[2]) == "duran")
    nima_n = sum(1 for r in rows if host_bucket(r[1], r[2]) == "nima")
    nawfal_n = sum(1 for r in rows if host_bucket(r[1], r[2]) == "nawfal")
    napolitano_n = sum(1 for r in rows if host_bucket(r[1], r[2]) == "napolitano")
    support_n = sum(
        1 for r in rows if host_bucket(r[1], r[2]) in ("support_johnson", "xpost")
    )

    lines = [
        "WORK only; not Record.",
        "",
        "# Barnes source index",
        "",
        "Purpose: canonical route map for the materialized Barnes corpus now on disk, grouped by host and context.",
        "",
        "**Audit:** `python scripts/audit_statecraft_archive_index.py --shelf-index barnes` — author/guest parity; skill **`audit index`**. (_Curated rebuild via builder — no `--fix`._)",
        "",
        "## Corpus note",
        "",
        f"- **{len(rows)}** eligible archive captures on disk ({date_span})",
        "- Rebuild: `python scripts/build_barnes_index.py`",
        f"- **{davis_n}** Davis · **{duran_n}** Duran/Mercouris · **{nima_n}** Dialogue Works/Nima · **{nawfal_n}** Mario Nawfal · **{napolitano_n}** Napolitano · **{support_n}** support-tier",
        "- Dominant mature lane: **Daniel Davis**; real **Mercouris** reinforcement; thickened **Nima** through Jun 26; **Nawfal** public-pressure cluster through Jun 25",
        "",
        "For shelf purposes, the Barnes corpus now divides into:",
        "",
        "- **primary guest corpus:** full or transcript-bearing Barnes guest captures under Davis, The Duran, and Dialogue Works",
        "- **public-pressure reinforcement:** fast-turn host environments where Barnes translates war, lobbying, and domestic-liability claims into mass-audience political language",
        "- **support-tier Barnes-adjacent captures:** Johnson verbatim/support files and Barnes X-post residue that help routing but do not by themselves define a mature host-local branch",
        "",
        "## Primary guest corpus",
        "",
    ]

    lines.extend(
        render_host_section(
            "### Davis x Barnes",
            "Primary mature lane. Open here first unless a later section gives a more specific reason not to.",
            "davis",
            rows,
            labels,
            annotations,
        )
    )
    lines.extend(
        render_host_section(
            "### Mercouris x Barnes / The Duran",
            "Real reinforcing lane. Not yet primary, but strong enough to matter for cross-host continuity.",
            "duran",
            rows,
            labels,
            annotations,
        )
    )
    lines.extend(
        render_host_section(
            "### Nima x Barnes / Dialogue Works",
            "Thin but meaningful late-stage reinforcement. This required source is part of the canonical shelf, not an appendix.",
            "nima",
            rows,
            labels,
            annotations,
        )
    )
    lines.extend(
        render_host_section(
            "### Mario Nawfal x Barnes",
            "Public-pressure reinforcement. Useful when the notebook needs Barnes in mass-audience electoral, corruption, or Israel-lobby pressure mode rather than a mature host-local lane.",
            "nawfal",
            rows,
            labels,
            annotations,
        )
    )
    lines.extend(
        render_host_section(
            "### Napolitano x Barnes / Judging Freedom",
            "Public-pressure reinforcement. Useful for White House cognition, Vance rug-pull, and domestic-liability framing in a fast-turn legal-commentator register — not yet a mature host-local lane.",
            "napolitano",
            rows,
            labels,
            annotations,
        )
    )

    other = [r for r in rows if host_bucket(r[1], r[2]) == "other"]
    if other:
        lines.extend(
            render_host_section(
                "### Other hosts",
                "Uncategorized Barnes guest captures.",
                "other",
                rows,
                labels,
                annotations,
            )
        )

    lines.append("## Support-tier Barnes-adjacent captures")
    lines.append("")
    lines.extend(
        render_host_section(
            "### Johnson / Countercurrent domestic-process support",
            "Useful for room dynamics, Trump-decline framing, and work-politics adjacency. Do not treat these as proof of a fully materialized Barnes x Johnson shelf.",
            "support_johnson",
            rows,
            labels,
            annotations,
        )
    )
    lines.extend(
        render_host_section(
            "### Barnes X-post support",
            "Helpful as pressure-cluster residue and exit-ramp signal, but not part of the primary guest corpus.",
            "xpost",
            rows,
            labels,
            annotations,
        )
    )

    lines.extend(render_open_first())
    lines.extend(render_boundary())
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
        print(f"annotations preserved: {len(annotations)}")
        return 0

    OUT.write_text(body if body.endswith("\n") else body + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {OUT} ({len(rows)} rows, {len(labels)} labels preserved)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
