#!/usr/bin/env python3
"""
Scaffold a statecraft month note from the month routing registry, routing metadata, and route templates.

Defaults to stdout so existing month notes are not overwritten by accident.
Use --output to write a starter file under the repo.
"""

from __future__ import annotations

import argparse
import calendar
import json
import re
import sys
from pathlib import Path

from capture_scaffold_common import REPO_ROOT, ensure_output_dir_under_repo

REGISTRY_PATH = REPO_ROOT / "statecraft" / "data" / "month-maturity-routing-registry.json"
METADATA_PATH = REPO_ROOT / "statecraft" / "data" / "month-routing-metadata.json"
TEMPLATE_DIR = REPO_ROOT / "statecraft" / "templates"

ROUTE_TO_TEMPLATE = {
    "benchmark": TEMPLATE_DIR / "month-benchmark-note-template.md",
    "watchlist": TEMPLATE_DIR / "month-watchlist-note-template.md",
    "closure-audit": TEMPLATE_DIR / "month-closure-audit-template.md",
}
ROUTE_TO_FILENAME_SUFFIX = {
    "benchmark": "benchmark-note",
    "watchlist": "watchlist",
    "closure-audit": "contradiction-audit",
}
MONTH_RE = re.compile(r"^\d{4}-\d{2}$")

def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))

def month_name_parts(month: str) -> tuple[str, str, str]:
    year, month_num = month.split("-")
    month_index = int(month_num)
    month_name = calendar.month_name[month_index]
    return year, month_num, month_name

def month_display(month: str) -> str:
    year, _, name = month_name_parts(month)
    return f"{name} {year}"

def month_slug(month: str) -> str:
    year, _, name = month_name_parts(month)
    return f"{name.lower()}-{year}"

def last_day(month: str) -> str:
    year, month_num, _ = month_name_parts(month)
    day = calendar.monthrange(int(year), int(month_num))[1]
    return f"{year}-{month_num}-{day:02d}"

def month_title(route_class: str, month: str) -> str:
    display = month_display(month)
    if route_class == "benchmark":
        return f"# {display} benchmark note"
    if route_class == "watchlist":
        return f"# {display} watchlist"
    return f"# {display} contradiction audit"

def month_note_filename(route_class: str, month: str) -> str:
    return f"{month_slug(month)}-{ROUTE_TO_FILENAME_SUFFIX[route_class]}.md"

def load_registry_entry(month: str) -> dict | None:
    data = load_json(REGISTRY_PATH)
    for entry in data.get("months", []):
        if entry.get("month") == month:
            return entry
    return None

def load_metadata_entry(month: str) -> dict | None:
    data = load_json(METADATA_PATH)
    months = data.get("months", {})
    if not isinstance(months, dict):
        return None
    entry = months.get(month)
    return entry if isinstance(entry, dict) else None

def trim_template_scaffold(text: str) -> str:
    lines = text.splitlines()
    if lines and lines[0].strip() == "":
        lines = lines[1:]
    while lines and not lines[0].strip():
        lines = lines[1:]
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    while lines and not lines[0].strip():
        lines = lines[1:]
    return "\n".join(lines).rstrip() + "\n"

def replace_template_placeholders(text: str, month: str) -> str:
    display = month_display(month)
    _, _, name = month_name_parts(month)
    return (
        text.replace("[Month Year]", display)
        .replace("[Month]", name)
        .replace("[YYYY-MM]", month)
        .replace("[YYYY-MM-01]", f"{month}-01")
        .replace("[YYYY-MM-last]", last_day(month))
    )

def bullet_list(items: list[str], *, empty_text: str) -> str:
    if not items:
        return f"- {empty_text}"
    return "\n".join(f"- {item}" for item in items)

def format_surface(path_str: str) -> str:
    path = REPO_ROOT / path_str
    label = Path(path_str).name
    return f"[{label}](/" + path.as_posix() + ")"

def metadata_summary_lines(entry: dict | None) -> list[str]:
    if not entry:
        return ["Archive metadata unavailable at scaffold time."]
    return [
        f"Archive stats: `{entry.get('captured_days', '?')}` captured days, `{entry.get('source_count', '?')}` source files, `{entry.get('thread_count', '?')}` threads, `{entry.get('channel_or_show_count', '?')}` channels/shows, `{entry.get('host_count', '?')}` hosts, `{entry.get('guest_count', '?')}` guests.",
        f"Dense-month signal: `{str(bool(entry.get('is_dense_month', False))).lower()}`.",
        f"Label-normalization signal: `{str(bool(entry.get('needs_label_normalization', False))).lower()}`.",
    ]

def label_variant_lines(entry: dict | None) -> list[str]:
    if not entry:
        return ["Label-normalization review deferred because metadata is unavailable."]
    variants = entry.get("guest_label_variants", [])
    if not variants:
        return ["No material guest-label splits are currently visible in the routing metadata."]
    lines = []
    for variant in variants[:5]:
        labels = variant.get("labels", [])
        rendered = ", ".join(
            f"`{label.get('label', '?')}` ({label.get('count', '?')})"
            for label in labels[:4]
            if isinstance(label, dict)
        )
        if rendered:
            lines.append(rendered)
    return lines or ["No material guest-label splits are currently visible in the routing metadata."]

def route_prefill_block(route_class: str, month: str, registry_entry: dict | None, metadata_entry: dict | None) -> dict[str, str]:
    status = registry_entry.get("status", "unregistered") if registry_entry else "unregistered"
    maturity = registry_entry.get("maturity_label", "unregistered month") if registry_entry else "unregistered month"
    surfaces = registry_entry.get("primary_surfaces", []) if registry_entry else []
    comparison_uses = registry_entry.get("comparison_uses", []) if registry_entry else []
    open_questions = registry_entry.get("open_questions", []) if registry_entry else []
    next_move = registry_entry.get("next_honest_move") if registry_entry else None

    truth_lines = [
        f"Registry route: `{route_class}`.",
        f"Registry status: `{status}`.",
        f"Maturity label: `{maturity}`.",
        *metadata_summary_lines(metadata_entry),
    ]
    if next_move:
        truth_lines.append(f"Next honest move: {next_move}")

    surface_lines = [format_surface(surface) for surface in surfaces]
    comparison_lines = comparison_uses[:]
    open_question_lines = open_questions[:]

    if route_class == "benchmark":
        return {
            "## Current Month Truth": bullet_list(truth_lines, empty_text="Fill the current month truth."),
            "## Primary Benchmark Surfaces": bullet_list(surface_lines, empty_text="Add the benchmark surfaces that make the month reusable."),
            "## What " + month_name_parts(month)[2] + " Is Good For": bullet_list(comparison_lines, empty_text="Add the key comparison uses for this benchmark month."),
            "## What " + month_display(month) + " Still Needs": bullet_list(open_question_lines, empty_text="Add bounded non-campaign improvement paths."),
        }

    if route_class == "watchlist":
        return {
            "## Current Month Truth": bullet_list(truth_lines, empty_text="State the month window and current archive-coverage read."),
            "## Healthy Coverage": "- Add speakers or strands that clearly look healthy on current local evidence.",
            "## Thin But Acceptable": "- Add present-but-light strands only when the archive truth supports them.",
            "## Needs Backfill Attention": bullet_list(open_question_lines, empty_text="Name only evidence-backed backfill candidates."),
            "## Label-Normalization Caveat": bullet_list(label_variant_lines(metadata_entry), empty_text="Add any material guest-label split that affects month judgment."),
            "## Promotion Condition": bullet_list(
                [next_move] if next_move else [],
                empty_text="State what would justify promotion to benchmark, narrowing into closure-audit, or staying a watchlist.",
            ),
        }

    return {
        "## Current On-Disk Baseline": bullet_list(truth_lines, empty_text="State the exact on-disk baseline."),
        "## Contradiction Audit Result": bullet_list(
            [f"Registry status at scaffold time: `{status}`.", f"Maturity label: `{maturity}`."]
            + ([next_move] if next_move else []),
            empty_text="State whether the current closure claim remains honest.",
        ),
        "## Candidate Queue": bullet_list(
            ["Registry says the month currently carries a finite queue."] if registry_entry and registry_entry.get("has_finite_queue") else ["Registry says there is no live finite queue at scaffold time."],
            empty_text="List candidate rows with date, host/source family, exact title, direct URL, status, and shelf consequence.",
        ),
        "## Month Verdict": bullet_list(
            [f"Current registry status: `{status}`."],
            empty_text="State the bounded month verdict after the audit.",
        ),
        "## Required Shelf Repairs If Any": bullet_list(surface_lines, empty_text="List the shelf surfaces that would need repair if the queue changes month truth."),
    }

def inject_prefill_sections(body: str, prefill_map: dict[str, str]) -> str:
    for heading, block in prefill_map.items():
        needle = f"{heading}\n"
        if needle in body:
            body = body.replace(needle, f"{heading}\n\n{block}\n\n", 1)
    return body

def render_note(month: str, route_class: str, registry_entry: dict | None, metadata_entry: dict | None) -> str:
    template_path = ROUTE_TO_TEMPLATE[route_class]
    template = trim_template_scaffold(template_path.read_text(encoding="utf-8"))
    template = replace_template_placeholders(template, month)
    prefill_map = route_prefill_block(route_class, month, registry_entry, metadata_entry)
    body = inject_prefill_sections(template, prefill_map)
    return "\n\n" + month_title(route_class, month) + "\n\n" + body.rstrip() + "\n"

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scaffold a statecraft month note from routing registry + metadata + templates."
    )
    parser.add_argument("--month", required=True, help="Month in YYYY-MM form.")
    parser.add_argument(
        "--route",
        choices=sorted(ROUTE_TO_TEMPLATE),
        default=None,
        help="Route class for an unregistered month. Ignored when the month is already registered unless it matches.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional output file path under the repo. Default: print scaffold to stdout.",
    )
    return parser.parse_args()

def main() -> int:
    args = parse_args()
    month = args.month.strip()
    if not MONTH_RE.match(month):
        raise SystemExit("--month must match YYYY-MM")

    registry_entry = load_registry_entry(month)
    metadata_entry = load_metadata_entry(month)

    route_class = registry_entry.get("route_class") if registry_entry else None
    if route_class and args.route and args.route != route_class:
        raise SystemExit(
            f"--route {args.route!r} conflicts with registered route {route_class!r} for {month}"
        )
    if not route_class:
        route_class = args.route
    if not route_class:
        raise SystemExit(f"{month} is not registered; provide --route to scaffold an unregistered month")

    rendered = render_note(month, route_class, registry_entry, metadata_entry)

    if args.output is None:
        sys.stdout.write(rendered)
        return 0

    output_path = args.output.resolve()
    ensure_output_dir_under_repo(output_path.parent, REPO_ROOT)
    if output_path.exists():
        raise SystemExit(f"Refusing to overwrite existing file: {output_path}")
    output_path.write_text(rendered, encoding="utf-8", newline="\n")
    print(output_path)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
