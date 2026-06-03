#!/usr/bin/env python3
"""Audit participant-lane projection across the statecraft source archive."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import build_speaker_routing_queue as speaker_routing
from statecraft_day_archive import (
    DEFAULT_ROOT,
    explicit_thread_values,
    guest_meta_values,
    parse_frontmatter,
    read_text,
)


@dataclass(frozen=True)
class FileAudit:
    path: str
    category: str
    reason: str
    explicit_threads: tuple[str, ...]
    legacy_threads: tuple[str, ...]
    projected_threads: tuple[str, ...]
    recognized_speakers: tuple[str, ...]
    unresolved_names: tuple[str, ...]
    has_guest_numbered: bool
    has_participants: bool
    has_speakers: bool
    has_thread_numbered: bool


def as_slug_tuple(values: list[str]) -> tuple[str, ...]:
    out: list[str] = []
    for value in values:
        normalized = str(value or "").strip()
        if normalized and normalized not in out:
            out.append(normalized)
    return tuple(out)


def legacy_thread_values(meta: dict[str, Any]) -> tuple[str, ...]:
    out: list[str] = []
    for raw in meta.get("thread"), meta.get("threads"):
        if raw is None:
            continue
        if isinstance(raw, (list, tuple)):
            values = raw
        else:
            values = [raw]
        for value in values:
            text = " ".join(str(value or "").split()).strip()
            if text and text not in out:
                out.append(text)
    return tuple(out)


def recognized_speaker_slugs(
    meta: dict[str, Any],
    inventory: speaker_routing.SpeakerInventory,
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    recognized: list[str] = []
    unresolved: list[str] = []

    host_slug = speaker_routing._canonical_host_slug(meta)  # noqa: SLF001
    if host_slug and host_slug in inventory.speaker_folders and host_slug not in recognized:
        recognized.append(host_slug)

    for name in guest_meta_values(meta):
        slug = speaker_routing._match_speaker(name, inventory)  # noqa: SLF001
        if slug:
            if slug not in recognized:
                recognized.append(slug)
        elif name not in unresolved:
            unresolved.append(name)

    return tuple(recognized), tuple(unresolved)


def classify_file(
    path: Path,
    inventory: speaker_routing.SpeakerInventory,
    root: Path,
) -> FileAudit | None:
    meta = parse_frontmatter(path)
    if not meta:
        return None

    text = read_text(path)
    has_guest_numbered = bool(re.search(r"^guest_\d+:", text, re.MULTILINE))
    has_participants = bool(re.search(r"^participants:", text, re.MULTILINE))
    has_speakers = bool(re.search(r"^speakers:", text, re.MULTILINE))
    has_thread_numbered = bool(re.search(r"^thread_\d+:", text, re.MULTILINE))

    participant_bearing = (
        has_guest_numbered
        or has_participants
        or has_speakers
        or has_thread_numbered
        or bool(meta.get("threads"))
    )
    if not participant_bearing:
        return None

    explicit_threads = explicit_thread_values(meta)
    legacy_threads = legacy_thread_values(meta)
    recognized, unresolved = recognized_speaker_slugs(meta, inventory)

    projected: list[str] = list(explicit_threads)
    for slug in recognized:
        if slug not in projected:
            projected.append(slug)

    explicit_set = set(explicit_threads)
    legacy_set = set(legacy_threads)
    projected_set = set(projected)
    recognized_set = set(recognized)

    category = "already-correct"
    reason = "explicit metadata already expresses all recognized participant lanes"

    if unresolved and not recognized_set:
        category = "ambiguous-hold"
        reason = "participant-bearing metadata exists but no participant resolves to a canonical speaker slug"
    elif projected_set != explicit_set:
        if "diesen-mearsheimer-mercouris" in path.name:
            category = "safe-metadata-normalization"
            reason = "recurring Diesen/Mearsheimer/Mercouris panels should carry explicit durable multi-thread metadata"
        elif "berletic" in path.name and "transcript-duran-mercouris" in path.name:
            category = "safe-metadata-normalization"
            reason = "recognized third-guest Duran/Mercouris live should carry explicit multi-thread metadata"
        elif unresolved:
            category = "ambiguous-hold"
            reason = "some participants resolve cleanly but unresolved names remain, so hold file-level normalization"
        else:
            category = "index-parser-undercount-only"
            reason = "parser inference fixes lane truth without requiring durable file edits"
    elif recognized_set - legacy_set:
        category = "index-parser-undercount-only"
        reason = "legacy thread semantics undercounted recognized participants but explicit/current metadata is now sufficient"

    return FileAudit(
        path=path.relative_to(root).as_posix(),
        category=category,
        reason=reason,
        explicit_threads=explicit_threads,
        legacy_threads=legacy_threads,
        projected_threads=tuple(projected),
        recognized_speakers=recognized,
        unresolved_names=unresolved,
        has_guest_numbered=has_guest_numbered,
        has_participants=has_participants,
        has_speakers=has_speakers,
        has_thread_numbered=has_thread_numbered,
    )


def month_from_path(rel_path: str) -> str:
    return rel_path[:7]


def build_report(root: Path) -> dict[str, Any]:
    inventory = speaker_routing._discover_inventory(speaker_routing.DEFAULT_SPEAKERS_DIR, root)
    all_files = sorted(path for path in root.rglob("*.md") if path.name != "README.md")
    audits = [audit for path in all_files if (audit := classify_file(path, inventory, root))]

    category_counter = Counter(audit.category for audit in audits)
    feature_counts = {
        "guest_numbered_files": sum(audit.has_guest_numbered for audit in audits),
        "participants_files": sum(audit.has_participants for audit in audits),
        "speakers_files": sum(audit.has_speakers for audit in audits),
        "thread_numbered_files": sum(audit.has_thread_numbered for audit in audits),
        "explicit_threads_files": sum(bool(audit.explicit_threads) for audit in audits),
    }

    lane_gains = Counter()
    month_changes = Counter()
    for audit in audits:
        gained = set(audit.projected_threads) - set(audit.legacy_threads)
        for slug in gained:
            lane_gains[slug] += 1
            month_changes[month_from_path(audit.path)] += 1

    unresolved_name_counter = Counter()
    for audit in audits:
        unresolved_name_counter.update(audit.unresolved_names)

    return {
        "root": str(root),
        "audited_files": len(audits),
        "category_counts": dict(category_counter),
        "feature_counts": feature_counts,
        "lane_gains_from_parser": dict(sorted(lane_gains.items(), key=lambda item: (-item[1], item[0]))),
        "months_with_lane_gains": dict(sorted(month_changes.items(), key=lambda item: (-item[1], item[0]))),
        "unresolved_names": dict(sorted(unresolved_name_counter.items(), key=lambda item: (-item[1], item[0]))),
        "files": [asdict(audit) for audit in audits],
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Statecraft Participant Index Audit",
        "",
        "_Generated by `python scripts/audit_statecraft_participant_indexes.py`._",
        "",
        "## Stats",
        "",
        f"- Audited participant-bearing files: `{report['audited_files']}`",
        f"- Category counts: "
        + ", ".join(
            f"`{name}` ({count})"
            for name, count in sorted(report["category_counts"].items(), key=lambda item: (-item[1], item[0]))
        ),
        f"- Feature counts: "
        + ", ".join(
            f"`{name}` ({count})"
            for name, count in sorted(report["feature_counts"].items(), key=lambda item: item[0])
        ),
        "",
        "## Parser Lane Gains",
        "",
    ]

    lane_gains = report["lane_gains_from_parser"]
    if lane_gains:
        lines.extend(f"- `{slug}`: `{count}` files gain projection" for slug, count in lane_gains.items())
    else:
        lines.append("- `(none)`")

    lines.extend(["", "## Months With Lane Gains", ""])
    month_gains = report["months_with_lane_gains"]
    if month_gains:
        lines.extend(f"- `{month}`: `{count}` files" for month, count in month_gains.items())
    else:
        lines.append("- `(none)`")

    lines.extend(["", "## Unresolved Names", ""])
    unresolved = report["unresolved_names"]
    if unresolved:
        lines.extend(f"- `{name}`: `{count}` files" for name, count in unresolved.items())
    else:
        lines.append("- `(none)`")

    lines.extend(["", "## Decision Table", ""])
    lines.append("| File | Category | Explicit threads | Projected threads | Unresolved names |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in report["files"]:
        lines.append(
            f"| `{row['path']}` | `{row['category']}` | "
            f"`{', '.join(row['explicit_threads']) or '(none)'}` | "
            f"`{', '.join(row['projected_threads']) or '(none)'}` | "
            f"`{', '.join(row['unresolved_names']) or '(none)'}` |"
        )

    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--md-out", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = build_report(args.root.resolve())
    rendered = render_markdown(report)

    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(report, indent=2), encoding="utf-8", newline="\n")
    if args.md_out:
        args.md_out.parent.mkdir(parents=True, exist_ok=True)
        args.md_out.write_text(rendered, encoding="utf-8", newline="\n")
    if not args.json_out and not args.md_out:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
