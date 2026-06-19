from repo_io import ARTIFACTS_DIR
#!/usr/bin/env python3
"""Build a small audit artifact for read-time statecraft metadata normalization."""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from statecraft_day_archive import (
    DEFAULT_ROOT,
    as_values,
    collect_archive_file,
    counter_to_list,
    is_probable_topic_fragment,
    iter_all_day_dirs,
    norm_scalar,
    parse_frontmatter,
    split_person_field_value,
)


REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ARTIFACTS_DIR / "statecraft" / "metadata"
OUT_JSON = OUT_DIR / "normalization-audit.json"
OUT_MD = OUT_DIR / "normalization-audit.md"
SCHEMA_VERSION = "1.0.0-statecraft-metadata-normalization-audit"
SLUG_PERSON_RE = re.compile(r"^[a-z]+(?:-[a-z]+)+$")
ROLE_MARKER_RE = re.compile(r"\((?:host|guest)\)", re.IGNORECASE)


def _raw_person_values(meta: dict, keys: tuple[str, ...], pattern_prefix: str | None = None) -> list[str]:
    out: list[str] = []
    for key in keys:
        out.extend(str(value) for value in as_values(meta.get(key)))
    if pattern_prefix:
        for key, raw_value in meta.items():
            if str(key).startswith(pattern_prefix):
                out.extend(str(value) for value in as_values(raw_value))
    return out


def _classify_host_boundary_failure(raw_host: str, meta: dict, normalized_parts: tuple[str, ...]) -> list[str]:
    classes: list[str] = []
    clean_host = norm_scalar(raw_host)
    show_values = {
        norm_scalar(value)
        for key in ("show", "channel_slug", "publication")
        for value in as_values(meta.get(key))
    }
    if clean_host and clean_host in show_values:
        if normalized_parts and any(_looks_like_known_speaker(part) for part in normalized_parts):
            classes.append("person-host-shares-show-identity")
        else:
            classes.append("channel-label-in-host-field")
    if clean_host and ROLE_MARKER_RE.search(clean_host):
        classes.append("multi-role-mixed-field")
    if len(normalized_parts) >= 2:
        classes.append("compound-person-field")
    if SLUG_PERSON_RE.fullmatch(clean_host):
        classes.append("slug-person-field")
    return classes


def _looks_like_known_speaker(value: str) -> bool:
    import build_speaker_routing_queue as speaker_routing
    from statecraft_day_archive import _speaker_inventory

    return bool(speaker_routing._match_speaker(value, _speaker_inventory()))  # noqa: SLF001


def _classify_guest_boundary_failure(
    raw_guest: str,
    title: str,
    normalized_parts: tuple[str, ...],
    record_guest_values: tuple[str, ...],
) -> list[str]:
    classes: list[str] = []
    clean_guest = norm_scalar(raw_guest)
    if is_probable_topic_fragment(clean_guest, title):
        classes.append("title-fragment-as-guest")
    if clean_guest and ROLE_MARKER_RE.search(clean_guest):
        classes.append("multi-role-mixed-field")
    if len(normalized_parts) >= 2:
        classes.append("compound-person-field")
    if SLUG_PERSON_RE.fullmatch(clean_guest):
        classes.append("slug-person-field")
    if normalized_parts and not any(part in record_guest_values for part in normalized_parts) and not classes:
        classes.append("unresolved-guest-fragment")
    return classes


def build_payload(root: Path = DEFAULT_ROOT) -> dict:
    host_rewrites: Counter[str] = Counter()
    guest_rewrites: Counter[str] = Counter()
    dropped_guest_fragments: Counter[str] = Counter()
    normalized_guest_variants: dict[str, Counter[str]] = defaultdict(Counter)
    normalized_host_variants: dict[str, Counter[str]] = defaultdict(Counter)
    boundary_failures: dict[str, Counter[str]] = defaultdict(Counter)
    boundary_examples: dict[str, dict[str, Counter[str]]] = defaultdict(lambda: defaultdict(Counter))
    structured_field_presence: Counter[str] = Counter()
    missing_structured_combos: Counter[str] = Counter()
    scanned_files = 0

    for day_dir in iter_all_day_dirs(root):
        for path in sorted(day_dir.glob("source-*.md")):
            scanned_files += 1
            meta = parse_frontmatter(path)
            record = collect_archive_file(path)
            title = norm_scalar(meta.get("title"))
            has_host_people = bool(as_values(meta.get("host_people")))
            has_guest_people = bool(as_values(meta.get("guest_people")))
            has_show_title = bool(norm_scalar(meta.get("show_title")))
            has_channel_name = bool(norm_scalar(meta.get("channel_name")))

            if has_host_people:
                structured_field_presence["host_people"] += 1
            if has_guest_people:
                structured_field_presence["guest_people"] += 1
            if has_show_title:
                structured_field_presence["show_title"] += 1
            if has_channel_name:
                structured_field_presence["channel_name"] += 1
            if any((has_host_people, has_guest_people, has_show_title, has_channel_name)):
                structured_field_presence["any_structured_fields"] += 1
            if all((has_show_title or record.source_form in {"newsletter", "article", "post"}, has_channel_name)):
                structured_field_presence["show_and_channel_complete"] += 1
            if record.host_values and not has_host_people:
                missing_structured_combos["missing_host_people"] += 1
            if record.guest_values and not has_guest_people:
                missing_structured_combos["missing_guest_people"] += 1
            if record.show and record.source_form not in {"newsletter", "article", "post"} and not has_show_title:
                missing_structured_combos["missing_show_title"] += 1
            if record.channel_values and not has_channel_name:
                missing_structured_combos["missing_channel_name"] += 1

            raw_hosts = _raw_person_values(meta, ("host", "hosts"))
            raw_guests = _raw_person_values(meta, ("guest", "guests", "speaker", "speakers", "participants"), "guest_")

            for raw_host in raw_hosts:
                normalized_parts = split_person_field_value(raw_host)
                if normalized_parts:
                    for normalized in normalized_parts:
                        normalized_host_variants[normalized][raw_host] += 1
                        if raw_host != normalized:
                            host_rewrites[f"{raw_host} -> {normalized}"] += 1
                for failure_class in _classify_host_boundary_failure(raw_host, meta, normalized_parts):
                    boundary_failures[failure_class]["host"] += 1
                    boundary_examples[failure_class]["host"][raw_host] += 1

            for raw_guest in raw_guests:
                normalized_parts = split_person_field_value(raw_guest)
                if not normalized_parts:
                    continue
                matched = False
                for normalized in normalized_parts:
                    if normalized in record.guest_values:
                        normalized_guest_variants[normalized][raw_guest] += 1
                        if raw_guest != normalized:
                            guest_rewrites[f"{raw_guest} -> {normalized}"] += 1
                        matched = True
                if not matched and raw_guest not in record.guest_values:
                    dropped_guest_fragments[raw_guest] += 1
                for failure_class in _classify_guest_boundary_failure(raw_guest, title, normalized_parts, record.guest_values):
                    boundary_failures[failure_class]["guest"] += 1
                    boundary_examples[failure_class]["guest"][raw_guest] += 1

    def top_variant_families(variants: dict[str, Counter[str]], *, min_variants: int = 2, limit: int = 20) -> list[dict]:
        rows: list[dict] = []
        for normalized, raw_counter in variants.items():
            if len(raw_counter) < min_variants:
                continue
            rows.append(
                {
                    "normalized": normalized,
                    "rawVariants": counter_to_list(raw_counter),
                    "totalCount": sum(raw_counter.values()),
                }
            )
        rows.sort(key=lambda row: (-row["totalCount"], -len(row["rawVariants"]), row["normalized"]))
        return rows[:limit]

    return {
        "schemaVersion": SCHEMA_VERSION,
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "root": str(root),
        "coverage": {
            "fileCount": scanned_files,
        },
        "structuredFieldPresence": counter_to_list(structured_field_presence),
        "missingStructuredCombos": counter_to_list(missing_structured_combos),
        "hostRewrites": counter_to_list(host_rewrites),
        "guestRewrites": counter_to_list(guest_rewrites),
        "droppedGuestFragments": counter_to_list(dropped_guest_fragments),
        "fieldBoundaryFailures": [
            {
                "class": failure_class,
                "counts": counter_to_list(counter),
                "hostExamples": counter_to_list(boundary_examples[failure_class]["host"]),
                "guestExamples": counter_to_list(boundary_examples[failure_class]["guest"]),
            }
            for failure_class, counter in sorted(
                boundary_failures.items(),
                key=lambda item: (-sum(item[1].values()), item[0]),
            )
        ],
        "hostVariantFamilies": top_variant_families(normalized_host_variants),
        "guestVariantFamilies": top_variant_families(normalized_guest_variants),
    }


def render_markdown(payload: dict) -> str:
    lines = [
        "# Statecraft Metadata Normalization Audit",
        "",
        "_Generated audit artifact for read-time host/guest normalization._",
        "",
        f"- Generated: `{payload['generatedAt']}`",
        f"- Root: `{payload['root']}`",
        f"- Scanned files: `{payload['coverage']['fileCount']}`",
        "",
    ]

    def add_counter_section(title: str, rows: list[dict]) -> None:
        lines.extend([f"## {title}", "", "| Rewrite | Count |", "| --- | ---: |"])
        for row in rows[:20]:
            lines.append(f"| `{row['name']}` | {row['count']} |")
        if not rows:
            lines.append("| `(none)` | 0 |")
        lines.append("")

    add_counter_section("Top Host Rewrites", payload["hostRewrites"])
    add_counter_section("Top Guest Rewrites", payload["guestRewrites"])
    add_counter_section("Dropped Guest Fragments", payload["droppedGuestFragments"])
    add_counter_section("Structured Field Presence", payload["structuredFieldPresence"])
    add_counter_section("Missing Structured Field Combos", payload["missingStructuredCombos"])

    lines.extend(["## Field-Boundary Failure Classes", ""])
    for row in payload["fieldBoundaryFailures"]:
        counts = ", ".join(f"`{item['name']}` ({item['count']})" for item in row["counts"]) or "`(none)` (0)"
        lines.append(f"- `{row['class']}`: {counts}")
        if row["hostExamples"]:
            host_examples = ", ".join(f"`{item['name']}` ({item['count']})" for item in row["hostExamples"][:5])
            lines.append(f"  Host examples: {host_examples}")
        if row["guestExamples"]:
            guest_examples = ", ".join(f"`{item['name']}` ({item['count']})" for item in row["guestExamples"][:5])
            lines.append(f"  Guest examples: {guest_examples}")
    if not payload["fieldBoundaryFailures"]:
        lines.append("- `(none)`")
    lines.append("")

    lines.extend(["## Guest Variant Families", ""])
    for row in payload["guestVariantFamilies"]:
        lines.append(f"- `{row['normalized']}`: " + ", ".join(f"`{item['name']}` ({item['count']})" for item in row["rawVariants"]))
    if not payload["guestVariantFamilies"]:
        lines.append("- `(none)`")
    lines.append("")

    lines.extend(["## Host Variant Families", ""])
    for row in payload["hostVariantFamilies"]:
        lines.append(f"- `{row['normalized']}`: " + ", ".join(f"`{item['name']}` ({item['count']})" for item in row["rawVariants"]))
    if not payload["hostVariantFamilies"]:
        lines.append("- `(none)`")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    payload = build_payload()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8", newline="\n")
    OUT_MD.write_text(render_markdown(payload), encoding="utf-8", newline="\n")
    print(f"wrote {OUT_MD}")
    print(f"wrote {OUT_JSON}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
