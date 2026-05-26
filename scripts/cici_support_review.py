#!/usr/bin/env python3
"""
Generate a cici-ai support review from standardized member profiles.

The script reads singularity/work-cici/member-profiles/*.md, extracts the
standard fields, and emits:
- a markdown support review table
- a Telegram-ready payment-track message

The goal is to make the next-month support review repeatable and evidence-based.
The profiles remain the source of truth; this script only summarizes them.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
PROFILE_DIR = REPO_ROOT / "singularity" / "work-cici" / "member-profiles"
OUTPUT_PATH = PROFILE_DIR / "support-review.md"


@dataclass
class MemberProfile:
    slug: str
    name: str
    github_handle: str
    spreadsheet_name: str
    current_status: str
    primary_lane: str
    secondary_lane: str
    last_verified_activity: str
    evidence_level: str
    role: str
    contribution: str
    intent: str
    support: str
    support_reason: str
    score: int
    floor_met: bool


def _strip_md_link(value: str) -> str:
    m = re.match(r"\[(.*?)\]\((.*?)\)", value.strip())
    return m.group(1) if m else value.strip()


def _extract_field(content: str, field: str) -> str:
    m = re.search(rf"^\*\*{re.escape(field)}:\*\*\s*(.+)$", content, re.MULTILINE)
    return m.group(1).strip() if m else ""


def _extract_section_text(content: str, heading: str) -> str:
    pattern = rf"^##\s+{re.escape(heading)}\s*$\n(.*?)(?=^##\s+|\Z)"
    m = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    if not m:
        return ""
    return m.group(1).strip()


def _clean_sentence(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if text.endswith("."):
        return text
    return text + "."


def _latest_date_from_text(value: str) -> date | None:
    dates = [datetime.strptime(match, "%Y-%m-%d").date() for match in re.findall(r"\d{4}-\d{2}-\d{2}", value)]
    return max(dates) if dates else None


def _score_evidence(level: str) -> int:
    mapping = {"A": 30, "B": 20, "C": 10}
    return mapping.get(level.strip().upper(), 0)


def _score_recency(last_verified_activity: str) -> int:
    latest = _latest_date_from_text(last_verified_activity)
    if latest is None:
        return 0
    days = max(0, (date.today() - latest).days)
    if days <= 7:
        return 30
    if days <= 14:
        return 25
    if days <= 30:
        return 20
    if days <= 45:
        return 10
    return 0


def _score_substance(current_status: str) -> int:
    normalized = current_status.strip().lower()
    if "builder-coordinator" in normalized:
        return 20
    if "active builder" in normalized:
        return 20
    if "active but mapping needs cleanup" in normalized:
        return 15
    if normalized == "active":
        return 15
    if "quiet" in normalized:
        return 0
    return 10


def _score_clarity(current_status: str, support_reason: str) -> int:
    combined = f"{current_status} {support_reason}".strip().lower()
    if "unresolved" in combined or "unclear" in combined:
        return 0
    if "mapping needs cleanup" in combined or "mapping cleanup" in combined:
        return 10
    return 20


def _score_profile(evidence_level: str, last_verified_activity: str, current_status: str, support_reason: str) -> int:
    score = 0
    score += _score_evidence(evidence_level)
    score += _score_recency(last_verified_activity)
    score += _score_substance(current_status)
    score += _score_clarity(current_status, support_reason)
    return min(score, 100)


def parse_profile(path: Path) -> MemberProfile:
    content = path.read_text(encoding="utf-8")
    name = _extract_field(content, "Name")
    github_handle = _strip_md_link(_extract_field(content, "GitHub handle"))
    spreadsheet_name = _extract_field(content, "Spreadsheet name")
    current_status = _extract_field(content, "Current status")
    primary_lane = _extract_field(content, "Primary lane")
    secondary_lane = _extract_field(content, "Secondary lane")
    last_verified_activity = _extract_field(content, "Last verified GitHub activity")
    evidence_level = _extract_field(content, "Evidence level")

    role = _extract_section_text(content, "Role")
    contribution = _extract_section_text(content, "What they are responsible for")
    intent = _extract_section_text(content, "What value they create")
    support_block = _extract_section_text(content, "Current support threshold")

    support = ""
    support_reason = ""
    if support_block:
        m = re.search(r"\*\*Pay / support next month:\*\*\s*(.+)", support_block)
        if m:
            support = m.group(1).strip()
        m = re.search(r"\*\*Reason:\*\*\s*(.+)", support_block)
        if m:
            support_reason = m.group(1).strip()

    score = _score_profile(evidence_level, last_verified_activity, current_status, support_reason)
    floor_met = score >= 70

    return MemberProfile(
        slug=path.stem,
        name=name,
        github_handle=github_handle,
        spreadsheet_name=spreadsheet_name,
        current_status=current_status,
        primary_lane=primary_lane,
        secondary_lane=secondary_lane,
        last_verified_activity=last_verified_activity,
        evidence_level=evidence_level,
        role=_clean_sentence(role.splitlines()[0]) if role else "",
        contribution=_clean_sentence(contribution.splitlines()[0]) if contribution else "",
        intent=_clean_sentence(intent.splitlines()[0]) if intent else "",
        support=support,
        support_reason=_clean_sentence(support_reason) if support_reason else "",
        score=score,
        floor_met=floor_met,
    )


def load_profiles() -> list[MemberProfile]:
    if not PROFILE_DIR.is_dir():
        return []
    skip = {"README.md", "template.md", "support-review.md", "scoring.md"}
    return [parse_profile(path) for path in sorted(PROFILE_DIR.glob("*.md")) if path.name not in skip]


def support_rank(value: str) -> int:
    normalized = value.strip().lower()
    if normalized.startswith("yes"):
        return 0
    if normalized.startswith("maybe") or normalized.startswith("yes, after"):
        return 1
    if normalized.startswith("hold"):
        return 2
    return 3


def render_markdown(profiles: list[MemberProfile]) -> str:
    lines: list[str] = []
    lines.append("# cici-ai support review")
    lines.append("")
    lines.append(f"- Profiles reviewed: {len(profiles)}")
    lines.append("- Decision basis: standardized member profiles")
    lines.append("- Threshold floor: 70 / 100")
    lines.append("")
    lines.append("## Support table")
    lines.append("")
    lines.append("| Member | Handle | Evidence | Last verified | Score | Floor | Support |")
    lines.append("|---|---|---:|---:|---:|---|---|")
    for p in sorted(profiles, key=lambda x: (support_rank(x.support), x.name.lower())):
        lines.append(
            f"| {p.name} | [{p.github_handle}](https://github.com/{p.github_handle}) | {p.evidence_level} | {p.last_verified_activity} | {p.score} | {'Pass' if p.floor_met else 'Hold'} | {p.support} |"
        )
    lines.append("")
    lines.append("## Notes")
    lines.append("")
    for p in sorted(profiles, key=lambda x: (support_rank(x.support), x.name.lower())):
        reason = p.support_reason or "No support reason recorded."
        lines.append(f"- **{p.name}**: {reason} (score {p.score}/100; {'floor met' if p.floor_met else 'below floor'}).")
    lines.append("")
    lines.append("## Scoring floor")
    lines.append("")
    lines.append("- Evidence strength: A=30, B=20, C=10")
    lines.append("- Recency: 0-7 days=30, 8-14 days=25, 15-30 days=20, 31-45 days=10, 46+ days=0")
    lines.append("- Work substance: active builder-coordinator=20, active builder=20, active but mapping cleanup=15, active=15, quiet=0")
    lines.append("- Clarity: clean mapping and explicit reason=20, mapping cleanup=10, unresolved or unclear=0")
    lines.append("")
    return "\n".join(lines)


def render_telegram(profiles: list[MemberProfile]) -> str:
    ordered = sorted(profiles, key=lambda x: (support_rank(x.support), x.name.lower()))
    lines: list[str] = []
    lines.append("> Team update: based on current GitHub evidence and follow-through, next-month payment track includes:")
    lines.append(">")
    for p in ordered:
        reason = p.support_reason or "Current profile support threshold marked Yes."
        lines.append(f"> - **{p.name}** - {reason} (score {p.score}/100; {'floor met' if p.floor_met else 'below floor'}).")
    lines.append(">")
    lines.append("> If a handle is not listed, next-month support decision remains open pending stronger public evidence.")
    lines.append(">")
    lines.append("> Keep building, keep work visible on GitHub, and keep the journal updated.")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate cici-ai support review from member profiles")
    parser.add_argument("--format", choices=["markdown", "telegram", "both"], default="both")
    parser.add_argument(
        "--write",
        action="store_true",
        help=f"Write the markdown review to {OUTPUT_PATH.relative_to(REPO_ROOT)}",
    )
    args = parser.parse_args()

    profiles = load_profiles()
    if not profiles:
        raise SystemExit(f"No member profiles found in {PROFILE_DIR}")

    markdown = render_markdown(profiles)
    telegram = render_telegram(profiles)

    if args.format in {"markdown", "both"}:
        print(markdown)
    if args.format == "both":
        print("\n\n---\n\n")
    if args.format in {"telegram", "both"}:
        print(telegram)

    if args.write:
        OUTPUT_PATH.write_text(markdown + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
