#!/usr/bin/env python3
"""
Coffee Step 1 - one-line "next task" hints for work-dev and singularity-academy.

Used by operator_coffee.py after session load. Sources are markdown on disk;
operators maintain canonical surfaces (workspace section Next actions and
Singularity workshop).

Usage:
    python3 scripts/coffee_lane_next_hints.py
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SINGULARITY_ROUTE_CLASSES = {
    "pulse",
    "control-plane",
    "warning",
    "reuse",
    "statecraft-bridge",
}


def _extract_next_actions_section(text: str) -> str | None:
    m = re.search(r"^## Next actions\s*$", text, re.MULTILINE)
    if not m:
        return None
    start = m.end()
    rest = text[start:]
    m2 = re.search(r"^## \S", rest, re.MULTILINE)
    return rest[: m2.start()] if m2 else rest


def next_work_dev_line(repo: Path) -> str:
    path = repo / "docs/skill-work/work-dev/workspace.md"
    if not path.is_file():
        return "Next work-dev: missing docs/skill-work/work-dev/workspace.md"
    text = path.read_text(encoding="utf-8")
    section = _extract_next_actions_section(text)
    if section is None:
        return "Next work-dev: add a ## Next actions section to workspace.md"
    for raw in section.splitlines():
        line = raw.strip()
        m = re.match(r"^(\d+)\.\s+(.*)$", line)
        if not m:
            continue
        body = m.group(2).strip()
        if not body:
            continue
        if body.startswith("~~"):
            continue
        short = body.replace("\n", " ")
        if len(short) > 220:
            short = short[:217] + "..."
        return f"Next work-dev (#{m.group(1)}): {short}"
    return (
        "Next work-dev: no open item in workspace.md section Next actions - "
        "add a numbered line or refresh Operator path"
    )


def _sync_daily_combined_block(text: str) -> str | None:
    if "### 3) Combined next action" not in text:
        return None
    i = text.index("### 3) Combined next action")
    tail = text[i:]
    end = re.search(r"\n---\s*\n", tail)
    chunk = tail[: end.start()] if end else tail.split("\n## ", 1)[0]
    return chunk


_SYNC_SIBLING_FIELD = re.compile(
    r"^(owner|done by|status|selected|lane|action|card path)\s*:",
    re.I,
)


def _first_filled_after_label(lines: list[str], label_lower: str) -> str | None:
    for i, raw in enumerate(lines):
        low = raw.lower()
        if label_lower in low and ":" in raw:
            after = raw.split(":", 1)[1].strip()
            if after and not after.startswith("`"):
                return after
            j = i + 1
            while j < len(lines):
                ln = lines[j].strip()
                if not ln:
                    j += 1
                    continue
                if ln.startswith("- "):
                    inner = ln[2:].strip()
                    if _SYNC_SIBLING_FIELD.match(inner):
                        break
                    if inner:
                        return inner
                if ln.startswith("#") or ln.startswith("---"):
                    break
                j += 1
    return None


def _hint_from_sync_daily(text: str) -> str | None:
    stale = _sync_daily_stale_reason(text)
    if stale:
        return stale
    block = _sync_daily_combined_block(text)
    if not block:
        return None
    lines = block.splitlines()
    return _first_filled_after_label(lines, "top sync task")


def _sync_daily_stale_reason(text: str, *, today: date | None = None) -> str | None:
    if re.search(r"stale sync state:\*\*\s*`yes`", text, re.I):
        return (
            "SYNC-DAILY is stale; run forced work-dev/work-politics mirror "
            "relevance scans before using mirror recommendations."
        )
    m = re.search(r"Date:\s*\*\*(\d{4}-\d{2}-\d{2})\*\*", text)
    if not m:
        return None
    try:
        snapshot_day = datetime.strptime(m.group(1), "%Y-%m-%d").date()
    except ValueError:
        return None
    current = today or date.today()
    if (current - snapshot_day).days > 3:
        return (
            "SYNC-DAILY is older than 3 days; mark stale and run forced "
            "work-dev/work-politics mirror relevance scans."
        )
    return None


def _first_active_watch(repo: Path) -> str | None:
    path = repo / "singularity/work-cici/WORK-LEDGER.md"
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8")
    if "## II-A. ACTIVE WATCHES" not in text:
        return None
    chunk = text.split("## II-A. ACTIVE WATCHES", 1)[1]
    m = re.search(r"\*\*Watch:\*\*\s*(.+)", chunk)
    if m:
        return m.group(1).strip()
    return None


def next_work_cici_line(repo: Path) -> str:
    sync_path = repo / "singularity/work-cici/SYNC-DAILY.md"
    if sync_path.is_file():
        st = _hint_from_sync_daily(sync_path.read_text(encoding="utf-8"))
        if st:
            short = st.replace("\n", " ")
            if len(short) > 220:
                short = short[:217] + "..."
            return f"Next work-cici (SYNC-DAILY): {short}"
    w = _first_active_watch(repo)
    if w:
        short = w if len(w) <= 220 else w[:217] + "..."
        return f"Next work-cici (WORK-LEDGER watch): {short}"
    return (
        "Next work-cici: fill SYNC-DAILY section Combined next action or "
        "WORK-LEDGER - see singularity/work-cici/INDEX.md"
    )


def _normalize_route_class(value: str) -> str:
    norm = value.strip().strip("`").lower()
    return norm if norm in _SINGULARITY_ROUTE_CLASSES else "pulse"


def _extract_bold_field(text: str, label: str) -> str | None:
    pattern = rf"^\s*[-*]\s+\*\*{re.escape(label)}:\*\*\s*(.+?)\s*$"
    match = re.search(pattern, text, re.MULTILINE)
    if not match:
        return None
    value = match.group(1).strip()
    return value or None


def _next_singularity_override(repo: Path) -> tuple[str, str, str] | None:
    path = repo / "singularity/workshop/sheets/coffee-d-singularity.md"
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8")
    if "## Coffee D Next Action" not in text:
        return None

    section = text.split("## Coffee D Next Action", 1)[1]
    route_class = _extract_bold_field(section, "Route class")
    source = _extract_bold_field(section, "Source")
    reason = _extract_bold_field(section, "Reason")
    if not (route_class and source and reason):
        return None
    return (_normalize_route_class(route_class), source.strip("`"), reason)


def _latest_matching_sheet(sheets: Path, patterns: list[str]) -> Path | None:
    matches: list[Path] = []
    for pattern in patterns:
        matches.extend(sorted(sheets.glob(pattern)))
    if not matches:
        return None
    return sorted(set(matches))[-1]


def _fallback_singularity_target(repo: Path) -> tuple[Path, str, str]:
    sheets = repo / "singularity/workshop/sheets"
    if sheets.is_dir():
        bridge = sheets / "sovereignty-under-acceleration.md"
        latest_innermost = _latest_matching_sheet(sheets, ["innermost-loop-*.md"])
        latest_moonshots = _latest_matching_sheet(sheets, ["moonshots-*.md"])

        if bridge.is_file():
            return (
                bridge,
                "statecraft-bridge",
                "authority, legitimacy, pause, rollback, and institutional carrier are already the live pressure.",
            )
        if latest_innermost is not None:
            return (
                latest_innermost,
                "pulse",
                "the latest source-bound acceleration sheet is the right place to name the front before choosing a control-plane or warning pass.",
            )
        if latest_moonshots is not None:
            return (
                latest_moonshots,
                "pulse",
                "the latest Moonshots bridge is the best available acceleration anchor before routing deeper.",
            )

    target = repo / "singularity/workshop/README.md"
    return (
        target,
        "reuse",
        "the workshop front door is the safest fallback when no fresher singularity source or override is present.",
    )


def next_academy_singularity_line(repo: Path) -> str:
    base = repo / "singularity/workshop"
    if not base.is_dir():
        return "Next singularity-academy: missing singularity/workshop"

    override = _next_singularity_override(repo)
    if override is not None:
        route_class, source, reason = override
        return f"Next singularity-academy [{route_class}]: {source} - {reason}"

    target, route_class, reason = _fallback_singularity_target(repo)
    rel = target.relative_to(repo).as_posix()
    return f"Next singularity-academy [{route_class}]: {rel} - {reason}"


def format_lane_next_hints(repo: Path | None = None) -> str:
    root = repo or REPO_ROOT
    b = next_work_dev_line(root)
    d = next_academy_singularity_line(root)
    return f"{b}\n{d}"


def main() -> int:
    p = argparse.ArgumentParser(
        description="Print work-dev + singularity-academy next-task hints for coffee."
    )
    p.add_argument(
        "--repo",
        type=Path,
        default=REPO_ROOT,
        help="Repository root (default: parent of scripts/)",
    )
    args = p.parse_args()
    print(format_lane_next_hints(args.repo))
    return 0


if __name__ == "__main__":
    sys.exit(main())
