#!/usr/bin/env python3
"""
Generate a Telegram-ready daily brief for the cici-ai team.

The script reads bounded WORK-layer sources:
- singularity/work-cici/cici-ai-community-dashboard.md
- singularity/work-cici/member-profiles/*.md

It emits:
- a structured operator digest
- a Telegram-ready daily brief

The generator is deliberately narrow. It summarizes evidence-backed movement and
names one or two concrete asks; it does not invent activation or promote
self-report into proof.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parent.parent
DASHBOARD_PATH = REPO_ROOT / "singularity" / "work-cici" / "cici-ai-community-dashboard.md"
PROFILE_DIR = REPO_ROOT / "singularity" / "work-cici" / "member-profiles"
PROGRESS_README_PATH = REPO_ROOT / "singularity" / "work-cici" / "cici-ai-progress" / "README.md"
TELEGRAM_README_PATH = REPO_ROOT / "singularity" / "work-cici" / "cici-ai-telegram" / "README.md"
EVIDENCE_DIR = REPO_ROOT / "singularity" / "work-cici" / "evidence"


@dataclass
class DashboardRow:
    week_of: str
    evidence_links: str
    invited: int
    joined: int
    introduced: int
    goal_stated: int
    first_task_completed: int
    returned_within_7d: int
    issue_pr_artifact: int
    helper_behavior: int
    notes: str
    confidence: str


@dataclass
class MemberProfile:
    name: str
    github_handle: str
    current_status: str
    last_verified_activity: str
    evidence_level: str
    open_loops: list[str]


@dataclass
class LaneState:
    name: str
    next_action: str
    open_loops: list[str]


@dataclass
class EvidenceNote:
    path: str
    title: str
    note_date: str
    confidence: str
    movement_bullets: list[str]
    follow_up_bullets: list[str]


@dataclass
class BriefDigest:
    date: str
    mode: str
    confidence: str
    source_week: str
    pulse: str
    what_moved: list[str]
    what_matters_today: list[str]
    who_needs_action: list[str]
    reply_format: str
    source_paths: list[str]


def _extract_section(text: str, heading: str) -> str:
    pattern = rf"^##\s+{re.escape(heading)}\s*$\n(.*?)(?=^##\s+|\Z)"
    match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
    return match.group(1).strip() if match else ""


def _extract_subsection(text: str, heading: str) -> str:
    pattern = rf"^###\s+{re.escape(heading)}\s*$\n(.*?)(?=^###\s+|^##\s+|\Z)"
    match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
    return match.group(1).strip() if match else ""


def _extract_h1_title(text: str) -> str:
    match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    return match.group(1).strip() if match else ""


def _safe_relpath(path: Path, repo_root: Path = REPO_ROOT) -> str:
    try:
        return str(path.relative_to(repo_root)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def _ascii_safe(text: str) -> str:
    replacements = {
        "\u2014": "-",
        "\u2013": "-",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2192": "->",
        "\u2194": "<->",
        "\u00a7": "Sec.",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def _parse_confidence(notes: str) -> str:
    match = re.search(r"\bConfidence\b[^ABC0-9]{0,12}([ABC])\b", notes, re.I)
    return match.group(1).upper() if match else "C"


def _parse_int(cell: str) -> int:
    cell = cell.strip()
    if not cell:
        return 0
    return int(cell)


def _split_table_row(row: str) -> list[str]:
    parts = [part.strip() for part in row.strip().strip("|").split("|")]
    return parts


def parse_latest_dashboard_row(path: Path = DASHBOARD_PATH) -> DashboardRow:
    text = path.read_text(encoding="utf-8")
    section = _extract_section(text, "4. Weekly snapshot table")
    if not section:
        raise ValueError(f"Missing weekly snapshot table in {path}")

    rows: list[DashboardRow] = []
    for raw in section.splitlines():
        line = raw.strip()
        if not line.startswith("|"):
            continue
        if ":---" in line or "---:" in line:
            continue
        cols = _split_table_row(line)
        if len(cols) != 11:
            continue
        week_of = cols[0]
        if not week_of or week_of == "Week of" or week_of == "YYYY-MM-DD":
            continue
        row = DashboardRow(
            week_of=week_of,
            evidence_links=cols[1],
            invited=_parse_int(cols[2]),
            joined=_parse_int(cols[3]),
            introduced=_parse_int(cols[4]),
            goal_stated=_parse_int(cols[5]),
            first_task_completed=_parse_int(cols[6]),
            returned_within_7d=_parse_int(cols[7]),
            issue_pr_artifact=_parse_int(cols[8]),
            helper_behavior=_parse_int(cols[9]),
            notes=cols[10],
            confidence=_parse_confidence(cols[10]),
        )
        rows.append(row)
    if not rows:
        raise ValueError(f"No filled weekly rows found in {path}")
    rows.sort(key=lambda row: row.week_of)
    return rows[-1]


def _extract_bullets(block: str) -> list[str]:
    bullets: list[str] = []
    for raw in block.splitlines():
        line = raw.strip()
        if line.startswith("- "):
            bullets.append(line[2:].strip())
    return bullets


def parse_dashboard_qualitative(path: Path = DASHBOARD_PATH) -> dict[str, list[str]]:
    text = path.read_text(encoding="utf-8")
    sections = {
        "what_worked": _extract_bullets(_extract_subsection(text, "What worked")),
        "what_confused": _extract_bullets(_extract_subsection(text, "What confused people")),
        "what_produced_action": _extract_bullets(_extract_subsection(text, "What produced action")),
        "simpler_prompt": _extract_bullets(_extract_subsection(text, "What needs a simpler prompt")),
        "retire_or_simplify": _extract_bullets(_extract_subsection(text, "What should be retired or simplified")),
    }
    return sections


def parse_lane_readme(path: Path, *, lane_name: str) -> LaneState:
    text = path.read_text(encoding="utf-8")
    next_action = _extract_section(text, "Next action").splitlines()[0].strip() if _extract_section(text, "Next action") else ""
    return LaneState(
        name=lane_name,
        next_action=next_action,
        open_loops=_extract_bullets(_extract_section(text, "Open loops")),
    )


def _parse_date_from_text(text: str, path: Path) -> str:
    matches = re.findall(r"\d{4}-\d{2}-\d{2}", text)
    if matches:
        return max(matches)
    matches = re.findall(r"\d{4}-\d{2}-\d{2}", path.name)
    if matches:
        return max(matches)
    return "0000-00-00"


def parse_evidence_note(path: Path, *, repo_root: Path = REPO_ROOT) -> EvidenceNote:
    text = path.read_text(encoding="utf-8")
    title = _extract_h1_title(text) or path.stem
    confidence = _parse_confidence(text)
    movement_bullets: list[str] = []
    follow_up_bullets: list[str] = []

    for heading in ("Dashboard implications", "Operational reading", "Aggregate summary", "Context"):
        block = _extract_section(text, heading)
        if not block:
            continue
        bullets = _extract_bullets(block)
        if bullets:
            movement_bullets.extend(bullets)
            break
        compact = _compact_sentence(block.splitlines()[0]) if block.splitlines() else ""
        if compact:
            movement_bullets.append(compact)
            break

    follow_up_bullets.extend(_extract_bullets(_extract_section(text, "Follow-up")))
    return EvidenceNote(
        path=_safe_relpath(path, repo_root),
        title=title,
        note_date=_parse_date_from_text(text, path),
        confidence=confidence,
        movement_bullets=movement_bullets,
        follow_up_bullets=follow_up_bullets,
    )


def load_recent_evidence(
    evidence_dir: Path = EVIDENCE_DIR, limit: int = 4, *, repo_root: Path = REPO_ROOT
) -> list[EvidenceNote]:
    if not evidence_dir.is_dir():
        return []
    notes: list[EvidenceNote] = []
    for path in evidence_dir.glob("*.md"):
        if path.name == "README.md":
            continue
        notes.append(parse_evidence_note(path, repo_root=repo_root))
    notes.sort(key=lambda note: (note.note_date, note.path), reverse=True)
    return notes[:limit]


def _extract_field(content: str, field: str) -> str:
    match = re.search(rf"^\*\*{re.escape(field)}:\*\*\s*(.+)$", content, re.MULTILINE)
    return match.group(1).strip() if match else ""


def _strip_md_link(value: str) -> str:
    match = re.match(r"\[(.*?)\]\((.*?)\)", value.strip())
    return match.group(1).strip() if match else value.strip()


def _extract_list_section(content: str, heading: str) -> list[str]:
    section = _extract_section(content, heading)
    bullets = _extract_bullets(section)
    return bullets


def load_profiles(profile_dir: Path = PROFILE_DIR) -> list[MemberProfile]:
    if not profile_dir.is_dir():
        return []
    skip = {"README.md", "template.md", "support-review.md", "scoring.md"}
    profiles: list[MemberProfile] = []
    for path in sorted(profile_dir.glob("*.md")):
        if path.name in skip:
            continue
        content = path.read_text(encoding="utf-8")
        profiles.append(
            MemberProfile(
                name=_extract_field(content, "Name"),
                github_handle=_strip_md_link(_extract_field(content, "GitHub handle")),
                current_status=_extract_field(content, "Current status"),
                last_verified_activity=_extract_field(content, "Last verified GitHub activity"),
                evidence_level=_extract_field(content, "Evidence level") or "C",
                open_loops=_extract_list_section(content, "Open loops"),
            )
        )
    return profiles


def choose_mode(row: DashboardRow, qualitative: dict[str, list[str]]) -> str:
    notes_lower = row.notes.lower()
    produced = " ".join(qualitative.get("what_produced_action", [])).lower()
    if "comment" in notes_lower or "comment" in produced or "apprentice" in produced:
        return "public-output"
    if row.first_task_completed > 0 or row.issue_pr_artifact > 0 or row.helper_behavior > 0:
        return "proof"
    if "fork" in notes_lower or "github" in notes_lower or "setup" in notes_lower:
        return "setup"
    if row.joined > 0 or row.introduced > 0:
        return "intake"
    return "review-reset"


def build_pulse(mode: str, row: DashboardRow) -> str:
    if mode == "public-output":
        return "The group has visible public-output motion, but quality and proof still matter more than volume."
    if mode == "proof":
        return "We have real movement; today is about turning visible activity into proof-level artifacts."
    if mode == "setup":
        return "We have setup-stage motion, but most of it still needs artifact-linked confirmation."
    if mode == "intake":
        return "New joins and introductions are creating motion; the next step is converting that attention into one concrete artifact."
    return "The group needs a simple reset today: fewer claims, clearer proof, and one concrete next step."


def _compact_sentence(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text.rstrip(".")


def build_movements(row: DashboardRow, qualitative: dict[str, list[str]], limit: int = 3) -> list[str]:
    items: list[str] = []
    confidence = row.confidence

    if row.joined or row.introduced:
        items.append(
            f"{row.joined} joined and {row.introduced} introduced themselves in the latest evidence-backed window. [{confidence}]"
        )
    if row.goal_stated:
        items.append(f"{row.goal_stated} members stated a concrete goal. [{confidence}]")
    if row.first_task_completed:
        items.append(f"{row.first_task_completed} members reached first-task proof. [{confidence}]")
    if row.issue_pr_artifact:
        items.append(f"{row.issue_pr_artifact} issue, PR, or artifact signals were counted. [{confidence}]")
    if row.helper_behavior:
        items.append(f"{row.helper_behavior} helper-behavior signals were observed. [{confidence}]")

    for bullet in qualitative.get("what_produced_action", []):
        cleaned = _compact_sentence(bullet)
        items.append(f"{cleaned} [{confidence}]")
        if len(items) >= limit:
            break

    if not items:
        items.append("Most visible movement still needs confirmation before we count it as activation. [C]")
    return items[:limit]


def build_evidence_movements(notes: list[EvidenceNote], limit: int = 2) -> list[str]:
    items: list[str] = []
    for note in notes:
        for bullet in note.movement_bullets:
            cleaned = _compact_sentence(bullet)
            items.append(f"{cleaned} [{note.confidence}]")
            if len(items) >= limit:
                return items
    return items


def _parse_dateish(value: str) -> date | None:
    matches = re.findall(r"\d{4}-\d{2}-\d{2}", value)
    if not matches:
        return None
    parsed = [datetime.strptime(match, "%Y-%m-%d").date() for match in matches]
    return max(parsed)


def build_followups(profiles: Iterable[MemberProfile], today: date) -> list[str]:
    mapping_cleanup: list[str] = []
    stale_builders: list[str] = []
    active_builders: list[str] = []

    for profile in profiles:
        status = profile.current_status.lower()
        latest = _parse_dateish(profile.last_verified_activity)
        if "mapping needs cleanup" in status:
            mapping_cleanup.append(profile.name)
            continue
        if "active" in status:
            if latest is None or (today - latest).days > 14:
                stale_builders.append(profile.name)
            else:
                active_builders.append(profile.name)

    actions: list[str] = []
    if mapping_cleanup:
        names = ", ".join(mapping_cleanup)
        actions.append(f"{names}: reply with your exact GitHub handle so roster mapping can be cleaned up.")
    if stale_builders:
        names = ", ".join(stale_builders)
        actions.append(f"{names}: post one fresh artifact or screenshot so progress does not stay stale.")
    if active_builders:
        names = ", ".join(active_builders[:3])
        actions.append(f"{names}: if you already have visible repo motion, post one artifact from your first task.")
    return actions[:2]


def build_primary_asks(
    mode: str,
    qualitative: dict[str, list[str]],
    progress_lane: LaneState,
    telegram_lane: LaneState,
    evidence_notes: list[EvidenceNote],
) -> tuple[list[str], str]:
    simpler_prompt = qualitative.get("simpler_prompt", [])
    if simpler_prompt:
        primary = simpler_prompt[0]
    elif telegram_lane.next_action:
        primary = telegram_lane.next_action
    elif progress_lane.next_action:
        primary = progress_lane.next_action
    elif mode == "proof":
        primary = "If you already forked, post one artifact from your first task so we can count it as proof."
    elif mode == "setup":
        primary = "Post your OB1 fork URL or a screenshot showing the fork in your GitHub account."
    elif mode == "public-output":
        primary = "Post one public-output artifact or receipt so we can score quality and reach with evidence."
    elif mode == "intake":
        primary = "Reply with one concrete artifact that shows your next setup step."
    else:
        primary = "Reply with one artifact or blocker so the next step can be routed clearly."

    asks = [primary]
    for note in evidence_notes:
        for follow_up in note.follow_up_bullets:
            cleaned = _compact_sentence(follow_up)
            if cleaned and cleaned not in asks:
                asks.append(cleaned)
            if len(asks) >= 2:
                break
        if len(asks) >= 2:
            break
    if mode in {"setup", "proof"}:
        blocked_prompt = "If you are blocked, post the exact screen or error so help can be routed quickly."
        if blocked_prompt not in asks:
            asks.append(blocked_prompt)

    if "fork url" in primary.lower():
        reply_format = "fork URL or screenshot + one-line status"
    elif "public-output" in primary.lower() or "quality and reach" in primary.lower():
        reply_format = "artifact URL or screenshot + one-line status"
    else:
        reply_format = "one artifact or screenshot + one-line status"
    return asks[:2], reply_format


def build_digest(repo_root: Path = REPO_ROOT, brief_date: date | None = None) -> BriefDigest:
    today = brief_date or date.today()
    row = parse_latest_dashboard_row(repo_root / DASHBOARD_PATH.relative_to(REPO_ROOT))
    qualitative = parse_dashboard_qualitative(repo_root / DASHBOARD_PATH.relative_to(REPO_ROOT))
    profiles = load_profiles(repo_root / PROFILE_DIR.relative_to(REPO_ROOT))
    progress_lane = parse_lane_readme(repo_root / PROGRESS_README_PATH.relative_to(REPO_ROOT), lane_name="progress")
    telegram_lane = parse_lane_readme(repo_root / TELEGRAM_README_PATH.relative_to(REPO_ROOT), lane_name="telegram")
    evidence_notes = load_recent_evidence(repo_root / EVIDENCE_DIR.relative_to(REPO_ROOT), repo_root=repo_root)
    mode = choose_mode(row, qualitative)
    what_matters, reply_format = build_primary_asks(mode, qualitative, progress_lane, telegram_lane, evidence_notes)
    evidence_movements = build_evidence_movements(evidence_notes)
    movements = build_movements(row, qualitative, limit=2)
    for item in evidence_movements:
        if item not in movements:
            movements.append(item)
    digest = BriefDigest(
        date=today.isoformat(),
        mode=mode,
        confidence=row.confidence,
        source_week=row.week_of,
        pulse=build_pulse(mode, row),
        what_moved=movements[:3],
        what_matters_today=what_matters,
        who_needs_action=build_followups(profiles, today),
        reply_format=reply_format,
        source_paths=[
            "singularity/work-cici/cici-ai-community-dashboard.md",
            "singularity/work-cici/cici-ai-progress/README.md",
            "singularity/work-cici/cici-ai-telegram/README.md",
            "singularity/work-cici/evidence/",
            "singularity/work-cici/member-profiles/",
        ],
    )
    return digest


def render_operator_digest(digest: BriefDigest) -> str:
    lines: list[str] = []
    lines.append("# cici-ai daily brief digest")
    lines.append("")
    lines.append(f"- Date: {digest.date}")
    lines.append(f"- Mode: {digest.mode}")
    lines.append(f"- Confidence: {digest.confidence}")
    lines.append(f"- Source week: {digest.source_week}")
    lines.append("- Sources:")
    for path in digest.source_paths:
        lines.append(f"  - `{path}`")
    lines.append("")
    lines.append("## Pulse")
    lines.append("")
    lines.append(digest.pulse)
    lines.append("")
    lines.append("## What moved")
    lines.append("")
    for item in digest.what_moved:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## What matters today")
    lines.append("")
    for item in digest.what_matters_today:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## Who needs action")
    lines.append("")
    for item in digest.who_needs_action:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## Reply format")
    lines.append("")
    lines.append(f"- {digest.reply_format}")
    return _ascii_safe("\n".join(lines))


def render_telegram_brief(digest: BriefDigest) -> str:
    lines: list[str] = []
    lines.append(f"Daily cici-ai brief - {digest.date}")
    lines.append("")
    lines.append("Pulse")
    lines.append(digest.pulse)
    lines.append("")
    lines.append("What moved")
    for item in digest.what_moved:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("What matters today")
    for item in digest.what_matters_today:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("Who needs action")
    for item in digest.who_needs_action:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("Reply format")
    lines.append(f"- Reply with: {digest.reply_format}")
    return _ascii_safe("\n".join(lines))


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate the cici-ai daily Telegram brief and operator digest.")
    parser.add_argument("--format", choices=["digest", "telegram", "json", "both"], default="both")
    parser.add_argument("--date", help="Override brief date (YYYY-MM-DD). Defaults to today.")
    args = parser.parse_args()

    brief_date = datetime.strptime(args.date, "%Y-%m-%d").date() if args.date else None
    digest = build_digest(brief_date=brief_date)

    if args.format == "json":
        print(json.dumps(asdict(digest), indent=2))
        return 0

    if args.format in {"digest", "both"}:
        print(render_operator_digest(digest))
    if args.format == "both":
        print("\n\n---\n\n")
    if args.format in {"telegram", "both"}:
        print(render_telegram_brief(digest))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
