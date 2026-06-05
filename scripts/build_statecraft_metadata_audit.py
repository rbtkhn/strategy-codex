#!/usr/bin/env python3
"""Build a small audit artifact for read-time statecraft metadata normalization."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from statecraft_day_archive import (
    DEFAULT_ROOT,
    as_values,
    collect_archive_file,
    counter_to_list,
    guest_meta_values,
    iter_all_day_dirs,
    parse_frontmatter,
    split_person_field_value,
)


REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = REPO_ROOT / "artifacts" / "statecraft" / "metadata"
OUT_JSON = OUT_DIR / "normalization-audit.json"
OUT_MD = OUT_DIR / "normalization-audit.md"
SCHEMA_VERSION = "1.0.0-statecraft-metadata-normalization-audit"


def _raw_person_values(meta: dict, keys: tuple[str, ...], pattern_prefix: str | None = None) -> list[str]:
    out: list[str] = []
    for key in keys:
        out.extend(str(value) for value in as_values(meta.get(key)))
    if pattern_prefix:
        for key, raw_value in meta.items():
            if str(key).startswith(pattern_prefix):
                out.extend(str(value) for value in as_values(raw_value))
    return out


def build_payload(root: Path = DEFAULT_ROOT) -> dict:
    host_rewrites: Counter[str] = Counter()
    guest_rewrites: Counter[str] = Counter()
    dropped_guest_fragments: Counter[str] = Counter()
    normalized_guest_variants: dict[str, Counter[str]] = defaultdict(Counter)
    normalized_host_variants: dict[str, Counter[str]] = defaultdict(Counter)
    scanned_files = 0

    for day_dir in iter_all_day_dirs(root):
        for path in sorted(day_dir.glob("source-*.md")):
            scanned_files += 1
            meta = parse_frontmatter(path)
            record = collect_archive_file(path)

            raw_hosts = _raw_person_values(meta, ("host", "hosts"))
            raw_guests = _raw_person_values(meta, ("guest", "guests", "speaker", "speakers", "participants"), "guest_")

            for raw_host in raw_hosts:
                normalized_parts = split_person_field_value(raw_host)
                if normalized_parts:
                    for normalized in normalized_parts:
                        normalized_host_variants[normalized][raw_host] += 1
                        if raw_host != normalized:
                            host_rewrites[f"{raw_host} -> {normalized}"] += 1

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
        "hostRewrites": counter_to_list(host_rewrites),
        "guestRewrites": counter_to_list(guest_rewrites),
        "droppedGuestFragments": counter_to_list(dropped_guest_fragments),
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
