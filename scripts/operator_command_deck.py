#!/usr/bin/env python3
"""
Operator Command Deck — advisory what-next cockpit for strategy-codex.

Aggregates Repo Surgeon, Statecraft War Room, git, budget, and backlog signals.
Read-only except report outputs.

See runtime/artifacts/operator-command-deck/README.md and
docs/skill-work/work-dev/operator-dashboard-consolidation-phase0.md.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from build_review_dashboard import _pending_structs  # noqa: E402
from git_worktree_snapshot import capture_git_worktree_snapshot  # noqa: E402
from operator_handoff_check import (  # noqa: E402
    RUNTIME_NOISE_MARKERS,
    EXPORT_CHURN_MARKERS,
    _classify_lane_slice,
    _status_path,
)
from operator_report_utils import (  # noqa: E402
    Finding,
    authority_header,
    count_by_severity,
    markdown_table,
    overall_status,
    utc_now_iso,
    write_report,
)
from repo_io import ARTIFACTS_DIR, DEFAULT_PROFILE_ID, PREPARED_CONTEXT_DIR, profile_dir  # noqa: E402
from repo_surgeon import build_findings  # noqa: E402
from statecraft_war_room import WarRoomContext, build_war_room_context  # noqa: E402

DEFAULT_OUT = ARTIFACTS_DIR / "operator-command-deck" / "latest.md"
DEFAULT_JSON = ARTIFACTS_DIR / "operator-command-deck" / "latest.json"

BUDGET_STALE_DAYS = 7
RETURN_PATHS = [
    "docs/harness-architecture-map.md",
    "docs/intelligence-harness.md",
    "docs/statecraft-intake-queue.md",
    "docs/runtime/context-budgeting.md",
    "runtime/artifacts/repo-surgeon/README.md",
    "runtime/artifacts/statecraft-war-room/README.md",
]

SKILL_LOG_ROW_RE = re.compile(r"^\|\s*\d{4}-\d{2}-\d{2}\s*\|")

@dataclass
class NextAction:
    priority: int
    category: str
    action: str
    source_path: str | None = None
    urgency: str = "medium"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

@dataclass
class DeckContext:
    surgeon_findings: list[Finding]
    surgeon_status: str
    war_room: WarRoomContext
    git_summary: dict[str, Any]
    budget_summary: dict[str, Any]
    backlog_summary: dict[str, Any]
    gate_pending: list[dict[str, Any]] | None = None
    gate_summary: dict[str, Any] | None = None

def _classify_change(path: str) -> str:
    normalized = path.replace("\\", "/")
    for marker in RUNTIME_NOISE_MARKERS:
        if marker in normalized:
            return "runtime_noise"
    for marker in EXPORT_CHURN_MARKERS:
        if marker in normalized:
            return "export_churn"
    return "meaningful"

def _parse_built_timestamp(raw: str) -> datetime | None:
    text = (raw or "").strip()
    if not text:
        return None
    for fmt in (
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%d %H:%M UTC",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%d",
    ):
        try:
            dt = datetime.strptime(text.replace("+00:00", "Z"), fmt.replace("%z", "Z") if "%z" in fmt else fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except ValueError:
            continue
    return None

def load_budget_summary(repo_root: Path) -> dict[str, Any]:
    path = repo_root / "runtime" / "prepared-context" / "last-budget-builds.json"
    if not path.is_file():
        alt = PREPARED_CONTEXT_DIR / "last-budget-builds.json"
        path = alt if alt.is_file() else path
    summary: dict[str, Any] = {
        "receipt_path": None,
        "stale": True,
        "stale_reason": "missing receipt",
        "lanes": {},
    }
    if not path.is_file():
        return summary
    try:
        rel = path.relative_to(repo_root).as_posix()
    except ValueError:
        rel = path.as_posix()
    summary["receipt_path"] = rel
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        summary["stale_reason"] = "invalid receipt JSON"
        return summary
    lanes = data.get("lanes") if isinstance(data, dict) else None
    if not isinstance(lanes, dict) or not lanes:
        summary["stale_reason"] = "empty lanes"
        return summary

    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=BUDGET_STALE_DAYS)
    lane_info: dict[str, Any] = {}
    stale = False
    stale_reason = ""
    for lane, blob in sorted(lanes.items()):
        if not isinstance(blob, dict):
            continue
        built_raw = str(blob.get("built") or "")
        built_dt = _parse_built_timestamp(built_raw)
        lane_stale = built_dt is None or built_dt < cutoff
        if lane_stale:
            stale = True
            stale_reason = stale_reason or f"lane `{lane}` build older than {BUDGET_STALE_DAYS} days"
        lane_info[lane] = {
            "built": built_raw,
            "path": blob.get("path"),
            "mode": blob.get("mode"),
            "stale": lane_stale,
        }
    summary["lanes"] = lane_info
    summary["stale"] = stale
    summary["stale_reason"] = stale_reason if stale else ""
    return summary

def load_skill_candidate_backlog(repo_root: Path) -> dict[str, Any]:
    path = repo_root / "skills" / "skill-candidates.md"
    summary: dict[str, Any] = {
        "path": "skills/skill-candidates.md",
        "unpromoted_count": 0,
        "sample_names": [],
    }
    if not path.is_file():
        return summary
    in_log = False
    unpromoted: list[str] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.strip() == "## Log":
            in_log = True
            continue
        if in_log and line.startswith("## "):
            break
        if not in_log or not SKILL_LOG_ROW_RE.match(line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 4:
            continue
        _date, name, _trigger, pointer = cells[0], cells[1], cells[2], cells[3]
        if "*(promoted)*" in name or "*(promoted)*" in pointer:
            continue
        if "_drafts/" in pointer:
            continue
        unpromoted.append(name.strip("`"))
    summary["unpromoted_count"] = len(unpromoted)
    summary["sample_names"] = unpromoted[:5]
    return summary

def _packet_has_receipt(md_path: Path) -> bool:
    stem = md_path.stem
    parent = md_path.parent
    candidates = [
        parent / f"{stem}.receipt.json",
        parent / f"{stem}.json",
        parent / f"{stem}-receipt.json",
    ]
    return any(p.is_file() for p in candidates)

def load_review_packet_gaps(repo_root: Path) -> dict[str, Any]:
    packet_dir = repo_root / "runtime" / "artifacts" / "review-packets"
    missing: list[str] = []
    if packet_dir.is_dir():
        for md_path in sorted(packet_dir.glob("*.md")):
            if md_path.name.lower() == "readme.md":
                continue
            if not _packet_has_receipt(md_path):
                try:
                    missing.append(md_path.relative_to(repo_root).as_posix())
                except ValueError:
                    missing.append(md_path.as_posix())
    return {
        "directory": "runtime/artifacts/review-packets",
        "missing_receipt_count": len(missing),
        "missing_receipt_paths": missing[:10],
    }

def load_gate_pending(repo_root: Path, *, user_id: str = DEFAULT_PROFILE_ID) -> list[dict[str, Any]]:
    candidates = [
        repo_root / "recursion-gate.md",
        repo_root / "archive" / "grace-mar-instance" / "recursion-gate.md",
        profile_dir(user_id) / "recursion-gate.md",
    ]
    for gate_path in candidates:
        if gate_path.is_file():
            return _pending_structs(gate_path.read_text(encoding="utf-8", errors="replace"))
    return []

def load_git_summary(repo_root: Path, *, enabled: bool) -> dict[str, Any]:
    if not enabled:
        return {
            "enabled": False,
            "branch": "",
            "tracking": "",
            "clean": True,
            "uncommitted_slices": {},
        }
    snap = capture_git_worktree_snapshot(repo_root=repo_root)
    if not snap.ok:
        return {
            "enabled": True,
            "branch": "unknown",
            "tracking": snap.error or "unknown",
            "clean": True,
            "uncommitted_slices": {},
            "error": snap.error,
        }
    slices: dict[str, int] = {
        "statecraft": 0,
        "ph-civ": 0,
        "singularity": 0,
        "other": 0,
    }
    meaningful: list[str] = []
    for line in snap.status_lines:
        path = _status_path(line)
        category = _classify_change(path)
        if category != "meaningful":
            continue
        meaningful.append(path)
        bucket = _classify_lane_slice(path.replace("\\", "/"))
        slices[bucket] = slices.get(bucket, 0) + 1
    return {
        "enabled": True,
        "branch": snap.branch_name,
        "tracking": snap.tracking,
        "clean": len(meaningful) == 0,
        "uncommitted_slices": slices,
        "dirty_tracked_count": snap.dirty_tracked_count,
        "untracked_count": snap.untracked_count,
    }

def build_deck_context(
    repo_root: Path,
    *,
    full_surgeon: bool = False,
    surgeon_scope: str = "docs",
    verify_portable: bool = False,
    war_room_latest_days: int = 7,
    war_room_max_objects: int = 12,
    include_git: bool = True,
    include_gate: bool = False,
) -> DeckContext:
    findings, _check_outputs = build_findings(
        repo_root,
        run_checks=full_surgeon,
        scope=surgeon_scope,
        verify_portable=verify_portable,
        max_link_errors=50,
    )
    surgeon_status = overall_status(findings)
    war_room = build_war_room_context(
        repo_root,
        latest_days=war_room_latest_days,
        max_objects=war_room_max_objects,
    )
    git_summary = load_git_summary(repo_root, enabled=include_git)
    budget_summary = load_budget_summary(repo_root)
    backlog_summary = {
        "skill_candidates": load_skill_candidate_backlog(repo_root),
        "review_packets": load_review_packet_gaps(repo_root),
    }
    gate_pending: list[dict[str, Any]] | None = None
    gate_summary: dict[str, Any] | None = None
    if include_gate:
        gate_pending = load_gate_pending(repo_root)
        gate_summary = {
            "pending_count": len(gate_pending or []),
            "pending_ids": [p.get("id") for p in (gate_pending or [])[:10]],
        }
    return DeckContext(
        surgeon_findings=findings,
        surgeon_status=surgeon_status,
        war_room=war_room,
        git_summary=git_summary,
        budget_summary=budget_summary,
        backlog_summary=backlog_summary,
        gate_pending=gate_pending,
        gate_summary=gate_summary,
    )

def _intake_backlog_rows(war_room: WarRoomContext) -> list[Any]:
    rows = []
    for row in war_room.queue_rows:
        if row.synthesis_status in {"new", "queued"} and row.queue_eligible:
            rows.append(row)
    return rows

def rank_next_actions(ctx: DeckContext, *, max_actions: int = 5) -> list[NextAction]:
    candidates: list[NextAction] = []

    for finding in ctx.surgeon_findings:
        if finding.severity != "blocking":
            continue
        loc = finding.file or "repo"
        candidates.append(
            NextAction(
                priority=1,
                category="repo_surgeon",
                action=f"Fix blocking {finding.category}: {finding.message}",
                source_path=finding.file,
                urgency="high",
            )
        )
        if len([c for c in candidates if c.category == "repo_surgeon"]) >= 3:
            break

    intake_day = ctx.war_room.latest_archive_day or (
        ctx.war_room.days_scanned[-1] if ctx.war_room.days_scanned else None
    )
    if ctx.war_room.sync_status == "desync" and intake_day:
        candidates.append(
            NextAction(
                priority=2,
                category="intake",
                action=f"Run daily synthesis or intake review for archive day {intake_day} (sync desync)",
                source_path=f"statecraft/synthesis/day/{intake_day}.md",
                urgency="high",
            )
        )
    else:
        backlog = _intake_backlog_rows(ctx.war_room)
        if backlog:
            row = backlog[0]
            day = intake_day or "latest archive day"
            candidates.append(
                NextAction(
                    priority=2,
                    category="intake",
                    action=(
                        f"Promote or discard queued intake `{row.source_stem}` "
                        f"({row.synthesis_status}) for {day}"
                    ),
                    source_path=row.source_path,
                    urgency="medium",
                )
            )

    if ctx.budget_summary.get("stale"):
        reason = ctx.budget_summary.get("stale_reason") or "receipt missing or stale"
        candidates.append(
            NextAction(
                priority=3,
                category="context_budget",
                action=f"Refresh context budget: {reason} — run build_budgeted_context.py",
                source_path=ctx.budget_summary.get("receipt_path"),
                urgency="medium",
            )
        )

    packet_gaps = ctx.backlog_summary.get("review_packets", {})
    missing_count = packet_gaps.get("missing_receipt_count", 0)
    if missing_count:
        sample = (packet_gaps.get("missing_receipt_paths") or [None])[0]
        candidates.append(
            NextAction(
                priority=4,
                category="review_packet",
                action=(
                    f"Add receipt sidecar for {missing_count} review packet(s) "
                    f"(orchestrator --receipt-out)"
                ),
                source_path=sample,
                urgency="low",
            )
        )

    skill_info = ctx.backlog_summary.get("skill_candidates", {})
    unpromoted = skill_info.get("unpromoted_count", 0)
    if unpromoted:
        candidates.append(
            NextAction(
                priority=5,
                category="skill_candidate",
                action=(
                    f"Triage {unpromoted} unpromoted skill-candidate row(s) — "
                    f"promote to _drafts/ or strike stale entries"
                ),
                source_path=skill_info.get("path"),
                urgency="low",
            )
        )

    if ctx.gate_pending:
        candidates.append(
            NextAction(
                priority=7,
                category="gate",
                action=(
                    f"Review {len(ctx.gate_pending)} pending gate candidate(s) "
                    f"(fork-revive territory; operator confirm only)"
                ),
                source_path="recursion-gate.md",
                urgency="low",
            )
        )

    if ctx.war_room.objects:
        obj = ctx.war_room.objects[0]
        candidates.append(
            NextAction(
                priority=6,
                category="war_room",
                action=(
                    f"Review war-room object `{obj.name}` — "
                    f"transaction fit `{obj.transaction_fit.kind}` (operator confirm)"
                ),
                source_path=(
                    obj.source_floor[0]["path"] if obj.source_floor else None
                ),
                urgency="low",
            )
        )

    ranked = sorted(candidates, key=lambda a: (a.priority, a.category))
    seen: set[tuple[int, str]] = set()
    out: list[NextAction] = []
    for action in ranked:
        key = (action.priority, action.category)
        if key in seen:
            continue
        seen.add(key)
        out.append(action)
        if len(out) >= max_actions:
            break
    for i, action in enumerate(out, start=1):
        action.priority = i
    return out

def build_markdown(
    ctx: DeckContext,
    actions: list[NextAction],
    *,
    generated_at: str,
) -> str:
    counts = count_by_severity(ctx.surgeon_findings)
    git_clean = ctx.git_summary.get("clean", True)
    budget_stale = ctx.budget_summary.get("stale", False)

    parts = [
        "# Operator Command Deck",
        "",
        authority_header(generated_at, RETURN_PATHS),
        "## 1. Operator Posture",
        "",
        f"- Repo Surgeon status: **{ctx.surgeon_status}** (blocking: {counts['blocking']}, warnings: {counts['warning']})",
        f"- War Room sync: **{ctx.war_room.sync_status}** (archive day: `{ctx.war_room.latest_archive_day or 'none'}`)",
        f"- Git working tree: **{'clean' if git_clean else 'dirty'}**",
        f"- Context budget: **{'stale' if budget_stale else 'ok'}**",
        "",
        "## 2. Recommended Next Actions",
        "",
    ]
    action_rows = [
        {
            "Priority": a.priority,
            "Category": a.category,
            "Urgency": a.urgency,
            "Action": a.action,
        }
        for a in actions
    ]
    parts.append(
        markdown_table(action_rows, ["Priority", "Category", "Urgency", "Action"])
        if action_rows
        else "_No urgent actions detected._\n"
    )

    parts.extend(["", "## 3. Repo Health Summary", ""])
    top_findings = ctx.surgeon_findings[:5]
    finding_rows = [
        {
            "Severity": f.severity,
            "Category": f.category,
            "Message": f.message[:120],
            "File": f.file or "",
        }
        for f in top_findings
    ]
    parts.append(
        markdown_table(finding_rows, ["Severity", "Category", "Message", "File"])
        if finding_rows
        else "_No findings in fast surgeon scan._\n"
    )

    parts.extend(["", "## 4. Statecraft Summary", ""])
    obj_rows = [
        {
            "Object": o.name[:60],
            "Status": o.status,
            "Fit": o.transaction_fit.kind,
            "Lane": o.lane,
        }
        for o in ctx.war_room.objects[:5]
    ]
    parts.append(
        markdown_table(obj_rows, ["Object", "Status", "Fit", "Lane"])
        if obj_rows
        else "_No active war-room objects in window._\n"
    )

    parts.extend(["", "## 5. Git / Ship Snapshot", ""])
    if ctx.git_summary.get("enabled"):
        parts.append(f"- Branch: `{ctx.git_summary.get('branch', 'unknown')}`")
        parts.append(f"- Tracking: `{ctx.git_summary.get('tracking', 'unknown')}`")
        slices = ctx.git_summary.get("uncommitted_slices") or {}
        for key in ("statecraft", "ph-civ", "singularity", "other"):
            if slices.get(key):
                parts.append(f"- Uncommitted **{key}:** {slices[key]} file(s)")
        if git_clean:
            parts.append("- Working tree clean (meaningful changes).")
    else:
        parts.append("_Git summary disabled (`--no-git`)._")
    parts.append("")

    parts.extend(["## 6. Context Budget", ""])
    if ctx.budget_summary.get("receipt_path"):
        parts.append(f"- Receipt: `{ctx.budget_summary['receipt_path']}`")
        parts.append(f"- Stale: **{budget_stale}** — {ctx.budget_summary.get('stale_reason') or 'ok'}")
        for lane, info in (ctx.budget_summary.get("lanes") or {}).items():
            parts.append(f"- **{lane}:** built `{info.get('built', '')}` — stale={info.get('stale')}")
    else:
        parts.append("_No budget receipt — run `build_budgeted_context.py`._")
    parts.append("")

    skill_info = ctx.backlog_summary.get("skill_candidates", {})
    packet_info = ctx.backlog_summary.get("review_packets", {})
    parts.extend(
        [
            "## 7. Backlog Signals",
            "",
            f"- Unpromoted skill candidates: **{skill_info.get('unpromoted_count', 0)}**",
            f"- Review packets missing receipt: **{packet_info.get('missing_receipt_count', 0)}**",
            "",
        ]
    )

    if ctx.gate_summary is not None:
        parts.extend(["## 8. Gate Watch (fork-revive territory)", ""])
        parts.append(f"- Pending candidates: **{ctx.gate_summary.get('pending_count', 0)}**")
        ids = ctx.gate_summary.get("pending_ids") or []
        if ids:
            parts.append(f"- Sample ids: {', '.join(f'`{i}`' for i in ids if i)}")
        parts.append("")

    parts.extend(["## 9. Return Paths", ""])
    for path in RETURN_PATHS:
        parts.append(f"- `{path}`")
    parts.append("")
    return "\n".join(parts)

def build_json_payload(
    ctx: DeckContext,
    actions: list[NextAction],
    *,
    generated_at: str,
) -> dict[str, Any]:
    counts = count_by_severity(ctx.surgeon_findings)
    skill_info = ctx.backlog_summary.get("skill_candidates", {})
    packet_info = ctx.backlog_summary.get("review_packets", {})
    return {
        "generated_at": generated_at,
        "authority": "runtime_derived",
        "posture": {
            "surgeon_status": ctx.surgeon_status,
            "surgeon_blocking_count": counts["blocking"],
            "war_room_sync_status": ctx.war_room.sync_status,
            "git_clean": ctx.git_summary.get("clean", True),
            "budget_stale": ctx.budget_summary.get("stale", False),
        },
        "next_actions": [a.to_dict() for a in actions],
        "surgeon_summary": {
            "status": ctx.surgeon_status,
            "blocking_count": counts["blocking"],
            "warning_count": counts["warning"],
        },
        "war_room_summary": {
            "latest_archive_day": ctx.war_room.latest_archive_day,
            "active_object_count": len(ctx.war_room.objects),
            "sync_status": ctx.war_room.sync_status,
        },
        "git_summary": ctx.git_summary,
        "budget_summary": ctx.budget_summary,
        "backlog_summary": {
            "skill_candidates_unpromoted": skill_info.get("unpromoted_count", 0),
            "review_packets_missing_receipt": packet_info.get("missing_receipt_count", 0),
        },
        "gate_summary": ctx.gate_summary,
    }

def generate_report(
    repo_root: Path,
    *,
    out: Path = DEFAULT_OUT,
    json_out: Path = DEFAULT_JSON,
    snapshot: bool = False,
    max_next_actions: int = 5,
    full_surgeon: bool = False,
    surgeon_scope: str = "docs",
    verify_portable: bool = False,
    war_room_latest_days: int = 7,
    war_room_max_objects: int = 12,
    include_git: bool = True,
    include_gate: bool = False,
) -> tuple[int, dict[str, Any]]:
    """Build and write Operator Command Deck report; return (exit_code, json_payload)."""
    out_path = out if out.is_absolute() else (repo_root / out).resolve()
    json_path = json_out if json_out.is_absolute() else (repo_root / json_out).resolve()

    try:
        ctx = build_deck_context(
            repo_root,
            full_surgeon=full_surgeon,
            surgeon_scope=surgeon_scope,
            verify_portable=verify_portable,
            war_room_latest_days=war_room_latest_days,
            war_room_max_objects=war_room_max_objects,
            include_git=include_git,
            include_gate=include_gate,
        )
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 2, {}

    actions = rank_next_actions(ctx, max_actions=max_next_actions)
    generated_at = utc_now_iso()
    md = build_markdown(ctx, actions, generated_at=generated_at)
    payload = build_json_payload(ctx, actions, generated_at=generated_at)

    write_report(out_path, md, snapshot=snapshot)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    print(f"wrote {out_path}")
    print(f"wrote {json_path}")
    print(
        f"actions: {len(actions)} surgeon: {ctx.surgeon_status} war_room: {ctx.war_room.sync_status}"
    )
    return 0, payload

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--json-out", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--snapshot", action="store_true")
    parser.add_argument("--max-next-actions", type=int, default=5)
    parser.add_argument("--full-surgeon", action="store_true")
    parser.add_argument(
        "--surgeon-scope",
        default="docs",
        choices=("docs", "statecraft", "skills", "all"),
    )
    parser.add_argument("--verify-portable-skills", action="store_true")
    parser.add_argument("--war-room-latest-days", type=int, default=7)
    parser.add_argument("--war-room-max-objects", type=int, default=12)
    parser.add_argument("--no-git", action="store_true")
    parser.add_argument("--include-gate", action="store_true")
    args = parser.parse_args()

    code, _payload = generate_report(
        REPO_ROOT,
        out=args.out,
        json_out=args.json_out,
        snapshot=args.snapshot,
        max_next_actions=args.max_next_actions,
        full_surgeon=args.full_surgeon,
        surgeon_scope=args.surgeon_scope,
        verify_portable=args.verify_portable_skills,
        war_room_latest_days=args.war_room_latest_days,
        war_room_max_objects=args.war_room_max_objects,
        include_git=not args.no_git,
        include_gate=args.include_gate,
    )
    return code

if __name__ == "__main__":
    raise SystemExit(main())
