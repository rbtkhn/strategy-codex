#!/usr/bin/env python3
"""Build synthesis scaffolds over Innermost Loop longitudinal artifacts.

Reads the deterministic longitudinal spine and local raw/source-sheet metadata and writes:
  - singularity/synthesis/README.md
  - singularity/synthesis/YYYY-MM.md
  - singularity/synthesis/support/*.md
This is scaffold generation, not final singularity synthesis.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
import re
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INDEX = REPO_ROOT / "singularity/workshop/longitudinal/innermost-loop-signals.json"
DEFAULT_SYNTHESIS_DIR = REPO_ROOT / "singularity/synthesis"
DEFAULT_SUPPORT_DIR = DEFAULT_SYNTHESIS_DIR / "support"
DEFAULT_SINGULARITY_README = REPO_ROOT / "singularity/README.md"
DEFAULT_WORKSHOP_README = REPO_ROOT / "singularity/workshop/README.md"

MONTH_STATUS = "scaffolded"
MONTH_QUALITY = "draft"
SUPPORT_STATUS = "scaffolded"
SUPPORT_QUALITY = "draft"
MEMO_FORMAT_VERSION = 1

ACTION_CLASSES = [
    "monitor",
    "prepare",
    "contain",
    "build",
    "route_to_statecraft",
    "route_to_work_dev",
    "route_to_work_cici",
    "promote_to_note",
    "promote_to_essay",
]

FAILURE_MODES = [
    "hype_smoothing",
    "substrate_erasure",
    "action_theater",
    "cross_front_blur",
    "counterweight_failure",
    "overpromotion",
    "commentary_inflation",
]

@dataclass(frozen=True)
class SupportNote:
    note_id: str
    issue_date: str
    title: str
    role: str
    raw_path: str
    source_sheet_path: str | None
    month: str
    fronts: tuple[str, ...]
    reasons: tuple[str, ...]

def _relative(path: Path, root: Path = REPO_ROOT) -> str:
    return str(path.resolve().relative_to(root.resolve())).replace("\\", "/")

def _parse_frontmatter(text: str) -> dict[str, Any]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    out: dict[str, Any] = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        out[key.strip()] = value.strip()
    return out

def _existing_status(path: Path) -> str | None:
    if not path.is_file():
        return None
    return _parse_frontmatter(path.read_text(encoding="utf-8")).get("status")

def _write_scaffold(path: Path, content: str) -> str:
    existing_status = _existing_status(path)
    if existing_status and existing_status != MONTH_STATUS and existing_status != SUPPORT_STATUS:
        return f"skip non-scaffolded: {_relative(path)}"
    if path.is_file() and path.read_text(encoding="utf-8") == content:
        return f"skip unchanged: {_relative(path)}"
    path.parent.mkdir(parents=True, exist_ok=True)
    existed_before = path.is_file()
    path.write_text(content, encoding="utf-8")
    return f"{'updated' if existed_before else 'wrote'}: {_relative(path)}"

def _month_from_date(day: str) -> str:
    return day[:7]

def _month_label(month: str) -> str:
    return datetime.strptime(month, "%Y-%m").strftime("%B %Y")

def _path_exists(rel_path: str | None) -> bool:
    return bool(rel_path) and (REPO_ROOT / rel_path).is_file()

def _sheet_path_for_date(day: str) -> str | None:
    path = f"singularity/workshop/sheets/innermost-loop-{day}.md"
    return path if _path_exists(path) else None

def _sheet_link_for_date(day: str, *, from_support: bool = False) -> str | None:
    if not _sheet_path_for_date(day):
        return None
    prefix = "../../workshop/sheets" if from_support else "../workshop/sheets"
    return f"{prefix}/innermost-loop-{day}.md"

def _raw_archive_path(raw_path: str) -> str:
    return f"source-archive/singularity/innermost-loop/{Path(raw_path).name}"

def _raw_archive_link(raw_path: str, *, from_support: bool = False) -> str:
    prefix = "../.." if from_support else ".."
    return f"{prefix}/{_raw_archive_path(raw_path)}"

def _issue_title(raw_path: str, fallback: str) -> str:
    path = REPO_ROOT / raw_path
    if not path.is_file():
        return fallback
    text = path.read_text(encoding="utf-8")
    for line in text.splitlines():
        if line.startswith("- Title: "):
            return line.removeprefix("- Title: ").strip()
    return fallback

def _monthly_groups(index: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    out: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in index["items"]:
        out[_month_from_date(item["date"])].append(item)
    return dict(sorted(out.items()))

def _front_counts(items: list[dict[str, Any]]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for item in items:
        for front in item["detected_fronts"]:
            if front.get("needs_review"):
                continue
            counts[front["label"]] += 1
    return counts

def _new_fronts(items: list[dict[str, Any]], first_seen: dict[str, str]) -> list[str]:
    month = _month_from_date(items[0]["date"])
    out = []
    for front, first_day in sorted(first_seen.items()):
        if _month_from_date(first_day) == month:
            out.append(front)
    return out

def _first_seen(index: dict[str, Any]) -> dict[str, str]:
    seen: dict[str, str] = {}
    for item in index["items"]:
        for front in item["detected_fronts"]:
            if front.get("needs_review"):
                continue
            seen.setdefault(front["label"], item["date"])
    return seen

def _previous_month_counts(months: list[str], grouped: dict[str, list[dict[str, Any]]]) -> dict[str, Counter[str] | None]:
    out: dict[str, Counter[str] | None] = {}
    previous: Counter[str] | None = None
    for month in months:
        out[month] = previous
        previous = _front_counts(grouped[month])
    return out

def _strongest_intensifications(current: Counter[str], previous: Counter[str] | None) -> list[str]:
    if previous is None:
        return []
    deltas: list[tuple[int, str]] = []
    for label, count in current.items():
        delta = count - previous.get(label, 0)
        if delta > 0:
            deltas.append((delta, label))
    deltas.sort(key=lambda pair: (-pair[0], pair[1]))
    return [f"{label} (+{delta})" for delta, label in deltas[:4]]

def _support_role(
    *,
    has_sheet: bool,
    first_seen_here: tuple[str, ...],
    has_no_stable_fronts: bool,
) -> tuple[str, list[str]]:
    reasons: list[str] = []
    if has_sheet:
        reasons.append("existing source sheet")
    if first_seen_here:
        reasons.append("first global appearance: " + ", ".join(first_seen_here))
    if has_no_stable_fronts:
        reasons.append("no stable fronts survived deterministic review")
    if has_sheet and has_no_stable_fronts:
        return "misreading_correction", reasons
    if has_sheet:
        return "action_wedge_seed", reasons
    if first_seen_here:
        return "substrate_anchor", reasons
    return "chronology_clarifier", reasons

def _build_support_notes(index: dict[str, Any], grouped: dict[str, list[dict[str, Any]]]) -> list[SupportNote]:
    first_seen = _first_seen(index)
    out: list[SupportNote] = []
    for month, items in grouped.items():
        for item in items:
            sheet_path = _sheet_path_for_date(item["date"])
            stable_fronts = tuple(
                front["label"]
                for front in item["detected_fronts"]
                if not front.get("needs_review")
            )
            first_seen_here = tuple(
                front for front in stable_fronts if first_seen.get(front) == item["date"]
            )
            has_no_stable_fronts = not stable_fronts
            should_emit = bool(sheet_path or first_seen_here or has_no_stable_fronts)
            if not should_emit:
                continue
            role, reasons = _support_role(
                has_sheet=bool(sheet_path),
                first_seen_here=first_seen_here,
                has_no_stable_fronts=has_no_stable_fronts,
            )
            out.append(
                SupportNote(
                    note_id=f"support-{item['date']}",
                    issue_date=item["date"],
                    title=_issue_title(item["raw_path"], f"Innermost Loop - {item['date']}"),
                    role=role,
                    raw_path=_raw_archive_path(item["raw_path"]),
                    source_sheet_path=sheet_path,
                    month=month,
                    fronts=stable_fronts,
                    reasons=tuple(reasons),
                )
            )
    return out

def _support_notes_by_month(notes: list[SupportNote]) -> dict[str, list[SupportNote]]:
    out: dict[str, list[SupportNote]] = defaultdict(list)
    for note in notes:
        out[note.month].append(note)
    return dict(out)

def _month_file_text(
    month: str,
    items: list[dict[str, Any]],
    support_notes: list[SupportNote],
    previous_month: str | None,
    next_month: str | None,
    previous_counts: Counter[str] | None,
    first_seen: dict[str, str],
) -> str:
    issue_count = len(items)
    fronts = _front_counts(items)
    front_labels = list(fronts.keys())[:6]
    support_ids = [note.note_id for note in support_notes]
    source_sheet_links = [
        f"[{item['date']} sheet]({_sheet_link_for_date(item['date'])})"
        for item in items
        if _sheet_path_for_date(item["date"])
    ]
    source_sheet_links = source_sheet_links[:5]
    strong_intensifications = _strongest_intensifications(fronts, previous_counts)
    new_fronts = _new_fronts(items, first_seen)
    month_title = _month_label(month)
    lines = [
        "---",
        f"synthesis_id: innermost-loop-synthesis-{month}",
        f"month: {month}",
        f"start_date: {items[0]['date']}",
        f"end_date: {items[-1]['date']}",
        f"issue_count: {issue_count}",
        "fronts:",
    ]
    for label in front_labels:
        lines.append(f"  - {label}")
    lines.extend(
        [
            "source_spine_path: singularity/workshop/longitudinal/innermost-loop.md",
        ]
    )
    if support_ids:
        lines.append("support_notes:")
        for note_id in support_ids:
            lines.append(f"  - {note_id}")
    else:
        lines.append("support_notes: []")
    lines.extend(
        [
            f"status: {MONTH_STATUS}",
            f"quality_level: {MONTH_QUALITY}",
            f"memo_format_version: {MEMO_FORMAT_VERSION}",
            "---",
            "",
            f"# Innermost Loop Synthesis - {month_title}",
            "",
                        "",
            "## Governing Law",
            "",
            "`Raw Capture -> Longitudinal Spine -> Support Notes -> Monthly Synthesis -> notes/essays or route-away`",
            "",
            "Interpret this file as the main singularity reasoning layer for the month. It is downstream of archive truth and deterministic chronology, and upstream of promotion or route-away decisions.",
            "",
            "## Source Support Block",
            "",
            f"- `primary_source_base`: `{items[0]['date']}` through `{items[-1]['date']}` raw captures plus `singularity/workshop/longitudinal/innermost-loop.md`",
            f"- `support_notes_used`: {', '.join(f'`{note_id}`' for note_id in support_ids) if support_ids else '`none yet`'}",
            "- `secondary_support_role`: chronology clarification, counterweight, misreading correction, substrate anchoring, and action-wedge seeding",
            "- `counterweight_used`: Keep compute, labor, legitimacy, and trust pressures visible at the same time so the month does not collapse into one smooth abundance or doom story.",
            "- `main_misreading_corrected`: Fill in the month-specific overread that the support layer is preventing.",
            "- `evidence_posture`: Fill with `strong`, `mixed`, or `thin` after the month is deepened.",
            "",
            "## Month in One Paragraph",
            "",
            f"Scaffold note: `{month}` contains `{issue_count}` captured issues. The strongest recurring fronts by deterministic count are {', '.join(f'`{label}` ({count})' for label, count in fronts.most_common(4)) if fronts else '`none`'}. Replace this paragraph with the month-level singularity read once the scaffold is deepened.",
            "",
            "## What Materially Changed",
            "",
            "- Fill the 2-4 shifts that most changed the singularity picture this month.",
            f"- Newly appearing fronts this month: {', '.join(f'`{label}`' for label in new_fronts) if new_fronts else '`none`'}.",
            f"- Strongest deterministic intensifications versus prior month: {', '.join(f'`{entry}`' for entry in strong_intensifications) if strong_intensifications else '`none`'}.",
            "",
            "## Dominant Fronts",
            "",
        ]
    )
    for label, count in fronts.most_common(6):
        lines.append(f"- `{label}` - detected in `{count}` issue(s); decide whether it is the real month driver or only the loudest recurring front.")
    if not fronts:
        lines.append("- `none` - no deterministic fronts detected; inspect the raw month manually.")
    lines.extend(
        [
            "",
            "## Control-Plane Shifts",
            "",
            "- Name where objective, authority, permissions, receipts, and rollback moved this month.",
            "- Note whether the month's strongest substrate pressure is compute, capital, institutions, workflow, or legitimacy.",
            "",
            "## Actionable Ideas",
            "",
        ]
    )
    for action_class in ACTION_CLASSES[:4]:
        lines.append(f"- `{action_class}` - Fill one actionable wedge and name the anchor issue(s) or support note(s).")
    lines.extend(
        [
            "",
            "## Open Tensions",
            "",
            "- Record the tension that should stay unresolved rather than being smoothed away.",
            "- Name one front that risks being overread if treated as the whole month.",
            "",
            "## Route Decisions",
            "",
            "- `stay_in_synthesis` - default until the month yields a clearer bounded promotion or route-away object.",
            "- `promote_to_note` - fill if this month produces a bounded but reusable argument.",
            "- `promote_to_essay` - fill if the month yields a carriage-bearing thesis.",
            "- `route_to_statecraft` - fill if the live object becomes legitimacy, sovereignty, carrier, treaty, or policy design.",
            "- `route_to_work_dev` - fill if the strongest wedge is technical leverage, tools, evals, or control-plane design.",
            "- `route_to_work_cici` - fill if the strongest wedge is beginner uplift, workflow substitution, or coordination design.",
            "",
            "## Source Anchors",
            "",
            f"- [Longitudinal spine](../workshop/longitudinal/innermost-loop.md) is the deterministic chronology substrate.",
            f"- Raw captures in this month: `{items[0]['date']}` through `{items[-1]['date']}`.",
        ]
    )
    for item in items:
        raw_link = _raw_archive_link(item["raw_path"])
        sheet_link = _sheet_link_for_date(item["date"])
        lines.append(
            f"- [{item['date']} raw]({raw_link})"
            + (f" - existing [source sheet]({sheet_link})" if sheet_link else "")
        )
    if support_notes:
        lines.append(f"- Support notes: {', '.join(f'[`{note.note_id}`](support/{note.note_id}.md)' for note in support_notes)}")
    if source_sheet_links:
        lines.append(f"- Month source-sheet entry points: {', '.join(source_sheet_links)}")
    lines.extend(
        [
            "",
            "## Failure-Mode Check",
            "",
        ]
    )
    for mode in FAILURE_MODES:
        lines.append(f"- `{mode}` - confirm whether this month currently clears or fails this risk.")
    lines.extend(
        [
            "",
            "## Navigation",
            "",
            f"- Previous month: [{previous_month}]({previous_month}.md)" if previous_month else "- Previous month: none",
            f"- Next month: [{next_month}]({next_month}.md)" if next_month else "- Next month: none",
            "- Return to [synthesis index](README.md).",
            "- Return to [singularity front door](../README.md).",
        ]
    )
    return "\n".join(lines) + "\n"

def _support_file_text(note: SupportNote, month_file: str) -> str:
    lines = [
        "---",
        f"support_note_id: {note.note_id}",
        f"issue_date: {note.issue_date}",
        f"month: {note.month}",
        f"role: {note.role}",
        "fronts:",
    ]
    for front in note.fronts:
        lines.append(f"  - {front}")
    lines.extend(
        [
            f"raw_path: {note.raw_path}",
            f"source_sheet_path: {note.source_sheet_path or ''}",
            f"status: {SUPPORT_STATUS}",
            f"quality_level: {SUPPORT_QUALITY}",
            f"memo_format_version: {MEMO_FORMAT_VERSION}",
            "---",
            "",
            f"# Support Note - {note.title}",
            "",
                        "",
            "## Role",
            "",
            f"- `primary_role`: `{note.role}`",
            f"- `why_this_exists`: {', '.join(note.reasons) if note.reasons else 'selected as a month support anchor'}",
            "",
            "## Provenance",
            "",
            f"- Raw capture: [Innermost Loop - {note.issue_date}]({_raw_archive_link(note.raw_path, from_support=True)})",
        ]
    )
    if note.source_sheet_path:
        lines.append(f"- Existing workshop sheet: [source sheet]({_sheet_link_for_date(note.issue_date, from_support=True)})")
    lines.extend(
        [
            f"- Monthly synthesis parent: [{note.month}](../{month_file})",
            "",
            "## Why This Issue Matters",
            "",
            "- Fill the narrow reason this issue deserves support-note treatment for the month synthesis.",
            "",
            "## Interpretive Discipline",
            "",
            "- Name the chronology, counterweight, misreading, substrate, or action-wedge function this note is serving.",
            "- Keep this note subordinate to the monthly synthesis rather than turning it into a rival archive surface.",
            "",
            "## Return Path",
            "",
            f"- Return to [{note.month} synthesis](../{month_file}).",
            "- Return to [synthesis index](../README.md).",
        ]
    )
    return "\n".join(lines) + "\n"

def _synthesis_readme_text(months: list[str], grouped: dict[str, list[dict[str, Any]]], support_notes: dict[str, list[SupportNote]]) -> str:
    lines = [
        "# Innermost Loop Synthesis",
        "",
                "",
        "This shelf is the singularity-facing synthesis layer for Innermost Loop. It is optimized for maximum analytical value and actionable ideas rather than equal-weight commentary on every issue.",
        "",
        "## Governing Law",
        "",
        "`Raw Capture -> Longitudinal Spine -> Support Notes -> Monthly Synthesis -> notes/essays or route-away`",
        "",
        "Use the layer this way:",
        "",
        "- raw captures preserve source truth",
        "- the longitudinal spine preserves deterministic chronology and front recurrence",
        "- support notes clarify difficulty without becoming a parallel archive",
        "- monthly synthesis is the main singularity reasoning layer",
        "- notes/essays are promotions, not replacements",
        "- statecraft/work-dev/work-cici are route-away destinations when the question changes",
        "",
        "## Surfaces",
        "",
        "- [Support notes](support/README.md) - minimal typed issue-level clarifiers for provenance, chronology, counterweight, substrate anchoring, or action extraction.",
        "- [Longitudinal spine](../workshop/longitudinal/innermost-loop.md) - deterministic chronology substrate.",
        "- [Singularity notes](../notes/README.md) - bounded promoted arguments.",
        "- [Singularity essays](../essays/README.md) - carriage-bearing promoted theses.",
        "",
        "## Monthly Synthesis Index",
        "",
        "| Month | Issues | Dominant fronts | Support notes |",
        "| --- | ---: | --- | ---: |",
    ]
    for month in months:
        items = grouped[month]
        fronts = _front_counts(items).most_common(3)
        front_text = ", ".join(f"`{label}` ({count})" for label, count in fronts) if fronts else "`none`"
        lines.append(
            f"| [{month}]({month}.md) | {len(items)} | {front_text} | {len(support_notes.get(month, []))} |"
        )
    lines.extend(
        [
            "",
            "## Review Discipline",
            "",
            "Every monthly synthesis should expose:",
            "",
            "- a Source Support Block",
            "- 2-5 actionable ideas with action-class tags",
            "- explicit route decisions",
            "- a short failure-mode check against hype smoothing, substrate erasure, action theater, cross-front blur, counterweight failure, overpromotion, and commentary inflation",
            "",
            "## Return Path",
            "",
            "- Return to [singularity front door](../README.md).",
            "- Return to [singularity workshop](../workshop/README.md).",
        ]
    )
    return "\n".join(lines) + "\n"

def _support_readme_text(notes: list[SupportNote]) -> str:
    lines = [
        "# Innermost Loop Support Notes",
        "",
                "",
        "These notes are subordinate support surfaces for the monthly Innermost Loop synthesis layer. They exist only where chronology, provenance, counterweight, misreading correction, substrate anchoring, or action-wedge extraction need a narrower issue-level object.",
        "",
        "## Roles",
        "",
        "- `chronology_clarifier`",
        "- `counterweight`",
        "- `misreading_correction`",
        "- `substrate_anchor`",
        "- `action_wedge_seed`",
        "",
        "## Index",
        "",
        "| Date | Role | Fronts | File |",
        "| --- | --- | --- | --- |",
    ]
    for note in notes:
        lines.append(
            f"| {note.issue_date} | `{note.role}` | {', '.join(f'`{front}`' for front in note.fronts) if note.fronts else '`none`'} | [{note.note_id}]({note.note_id}.md) |"
        )
    if not notes:
        lines.append("| none | none | none | none |")
    lines.extend(
        [
            "",
            "## Return Path",
            "",
            "- Return to [synthesis index](../README.md).",
            "- Return to [singularity front door](../../README.md).",
        ]
    )
    return "\n".join(lines) + "\n"

def _replace_or_insert_section(text: str, heading: str, body: str, *, before_heading: str | None = None) -> str:
    pattern = re.compile(rf"(?ms)^## {re.escape(heading)}\n.*?(?=^## |\Z)")
    replacement = f"## {heading}\n\n{body.rstrip()}\n\n"
    if pattern.search(text):
        return pattern.sub(replacement, text)
    if before_heading and f"## {before_heading}" in text:
        idx = text.index(f"## {before_heading}")
        return (text[:idx].rstrip() + "\n\n" + replacement + text[idx:].lstrip()).rstrip() + "\n"
    return text.rstrip() + "\n\n" + replacement

def _update_readme(path: Path, heading: str, body: str, before_heading: str | None = None) -> str:
    text = path.read_text(encoding="utf-8")
    new_text = _replace_or_insert_section(text, heading, body, before_heading=before_heading)
    if new_text == text:
        return f"skip unchanged: {_relative(path)}"
    path.write_text(new_text, encoding="utf-8")
    return f"updated: {_relative(path)}"

def _prune_stale_support_notes(support_dir: Path, active_ids: set[str]) -> list[str]:
    logs: list[str] = []
    for path in sorted(support_dir.glob("support-*.md")):
        if path.stem in active_ids:
            continue
        status = _existing_status(path)
        if status and status != SUPPORT_STATUS:
            logs.append(f"skip non-scaffolded stale support note: {_relative(path)}")
            continue
        path.unlink()
        logs.append(f"deleted stale scaffold: {_relative(path)}")
    return logs

def run(index_path: Path, synthesis_dir: Path, support_dir: Path) -> list[str]:
    index = json.loads(index_path.read_text(encoding="utf-8"))
    grouped = _monthly_groups(index)
    months = list(grouped.keys())
    first_seen = _first_seen(index)
    previous_counts = _previous_month_counts(months, grouped)
    support_notes = _build_support_notes(index, grouped)
    by_month = _support_notes_by_month(support_notes)
    active_support_ids = {note.note_id for note in support_notes}

    logs: list[str] = []
    synthesis_dir.mkdir(parents=True, exist_ok=True)
    support_dir.mkdir(parents=True, exist_ok=True)
    logs.extend(_prune_stale_support_notes(support_dir, active_support_ids))

    logs.append(_write_scaffold(synthesis_dir / "README.md", _synthesis_readme_text(months, grouped, by_month)))
    logs.append(_write_scaffold(support_dir / "README.md", _support_readme_text(support_notes)))

    for idx, month in enumerate(months):
        previous_month = months[idx - 1] if idx > 0 else None
        next_month = months[idx + 1] if idx + 1 < len(months) else None
        content = _month_file_text(
            month=month,
            items=grouped[month],
            support_notes=by_month.get(month, []),
            previous_month=previous_month,
            next_month=next_month,
            previous_counts=previous_counts[month],
            first_seen=first_seen,
        )
        logs.append(_write_scaffold(synthesis_dir / f"{month}.md", content))

    for note in support_notes:
        logs.append(_write_scaffold(support_dir / f"{note.note_id}.md", _support_file_text(note, f"{note.month}.md")))

    singularity_body = (
        "- [Synthesis](synthesis/README.md) - first-class monthly singularity synthesis shelf for extracting analytical value and actionable ideas from the Innermost Loop archive.\n"
        "- [Notes](notes/README.md) - first-class singularity notes shelf for exploratory and bounded interpretive outputs.\n"
        "- [Essays](essays/README.md) - first-class singularity essay shelf for more synthesized, stand-alone, carriage-bearing long-form outputs."
    )
    logs.append(_update_readme(DEFAULT_SINGULARITY_README, "Current Workshop Anchor", singularity_body, before_heading="External Watchlist"))

    output_surfaces_body = (
        "`singularity/` now recognizes three first-class output classes alongside workshop doctrine, sheets, raw captures, and watch surfaces:\n\n"
        "- [synthesis/](synthesis/README.md) for monthly singularity synthesis and route decisions\n"
        "- [notes/](notes/README.md) for working, exploratory, bounded interpretive outputs\n"
        "- [essays/](essays/README.md) for more synthesized, stand-alone, carriage-bearing long-form outputs\n\n"
        "Routing law:\n\n"
        "- use `synthesis/` when the main job is extracting month-level analytical value and actionable ideas from the Innermost Loop archive\n"
        "- use `notes/` when the piece is exploratory, bounded, workshop-adjacent, route-shaping, or interpretively partial\n"
        "- use `essays/` when the piece is synthesized enough to stand on its own as a more stable argument or carriage-bearing long-form output"
    )
    logs.append(_update_readme(DEFAULT_SINGULARITY_README, "Output Surfaces", output_surfaces_body, before_heading="Raw Capture Backfill"))

    workshop_body = (
        "- [Innermost Loop synthesis index](../synthesis/README.md) - monthly singularity reasoning layer above raw captures, longitudinal spine, and support notes.\n"
        "- [The Innermost Loop longitudinal spine](longitudinal/innermost-loop.md) - dated front-by-front trend view.\n"
        "- [The Innermost Loop signals JSON](longitudinal/innermost-loop-signals.json) - structured deterministic front index.\n"
        "- [Spine Health Checklist](longitudinal/spine-health-checklist.md) - quick QA pass for coverage, review load, bridge isolation, and rebuild sanity."
    )
    logs.append(_update_readme(DEFAULT_WORKSHOP_README, "Longitudinal Views", workshop_body, before_heading="First Instruments To Build"))
    return logs

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--index", type=Path, default=DEFAULT_INDEX)
    ap.add_argument("--synthesis-dir", type=Path, default=DEFAULT_SYNTHESIS_DIR)
    ap.add_argument("--support-dir", type=Path, default=DEFAULT_SUPPORT_DIR)
    args = ap.parse_args()
    for line in run(args.index, args.synthesis_dir, args.support_dir):
        print(line)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
