#!/usr/bin/env python3
"""
Generate a stop/resume handoff summary for the current repo state.

Includes a dedicated RECURSION-GATE section: pending counts by territory (work-politics vs
companion), up to a capped list of pending candidate IDs and summaries, and proposed next
steps to review/approve/merge via process_approved_candidates (read-only â€” this script does
not merge). Intended for good-night / handoff-check workflows.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

try:
    from harness_warmup import _last_activity_oneliner, _pending_candidates, _read
    from recursion_gate_territory import TERRITORY_LABEL_WORK_POLITICS, pending_by_territory
    from work_politics_ops import get_work_politics_snapshot
except ImportError:
    from scripts.harness_warmup import _last_activity_oneliner, _pending_candidates, _read
    from scripts.recursion_gate_territory import TERRITORY_LABEL_WORK_POLITICS, pending_by_territory
    from scripts.work_politics_ops import get_work_politics_snapshot

# Max pending rows to list verbatim before collapsing (closeout handoff stays scannable).
_GATE_PENDING_DISPLAY_CAP = 12

REPO_ROOT = Path(__file__).resolve().parent.parent
USERS_DIR = REPO_ROOT / "platform/users"
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

try:
    from work_jiang.warmup_jiang_pulse import build_night_pulse_lines
except ImportError:
    build_night_pulse_lines = None  # type: ignore[misc, assignment]

RUNTIME_NOISE_MARKERS = (
    "runtime/operator-events/",
    "pipeline-events.jsonl",
    "harness-events.jsonl",
    "cadence-learning-events.jsonl",
    "last-dream.json",
    "self-memory.md",
    "night-handoff.json",
    "runtime/daily-handoff/",
    "work-cadence-events.md",
    "memory-observability",
    ".capability-shift-cache.json",
    ".capability-shift-last-check",
    "runtime/bundle/runtime/",
    "runtime/bundle/audit/",
)

# Regenerated exports / integrity-adjacent â€” batch-commit or refresh; not "lane editorial" work.
EXPORT_CHURN_MARKERS = (
    "compute-ledger.jsonl",
    "self-llm.txt",
    "fork-manifest.json",
    "/manifest.json",
    "/llms.txt",
    "month-routing-metadata.json",
)


def _configure_utf8_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8", errors="replace")


def _run_git(*args: str) -> list[str]:
    proc = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        return [f"git {' '.join(args)} failed: {proc.stderr.strip() or 'unknown error'}"]
    return [line for line in proc.stdout.splitlines() if line.strip()]


def _run_git_status_bundle() -> tuple[list[str], list[str], str]:
    """One git invocation: branch tracking line + porcelain short status."""
    try:
        from git_worktree_snapshot import get_git_worktree_snapshot
    except ImportError:
        from scripts.git_worktree_snapshot import get_git_worktree_snapshot  # type: ignore

    snap = get_git_worktree_snapshot()
    if not snap.ok:
        fail = snap.error or "git status failed"
        return [fail], [fail], "unknown"
    status_sb_lines = [snap.branch_line] if snap.branch_line else []
    return list(snap.status_lines), status_sb_lines, snap.branch_name


SINGULARITY_INTAKE_PREFIXES = (
    "source-archive/singularity/moonshots/",
    "singularity/notes/",
)


def _classify_lane_slice(path: str) -> str:
    """Classify a repo path into ship-receipt lane buckets."""
    if "ph-civ" in path or path.startswith("codex/predictive-history/"):
        return "ph-civ"
    if path.startswith("statecraft/"):
        return "statecraft"
    if path.startswith("singularity/") or path.startswith("source-archive/singularity/"):
        return "singularity"
    return "other"


def build_singularity_intake_nudge(status_lines: list[str]) -> list[str]:
    """Surface uncommitted singularity intake paths (archive + promoted notes)."""
    paths: list[str] = []
    for line in status_lines:
        category, _path = _classify_change(line)
        if category in ("runtime_noise", "export_churn"):
            continue
        path = _status_path(line)
        if any(path.startswith(prefix) for prefix in SINGULARITY_INTAKE_PREFIXES):
            paths.append(path)
    if not paths:
        return []
    lines = [
        "",
        "## Singularity intake (uncommitted)",
        "",
        "_Moonshots archive and promoted notes should ship with verify receipts on the parent workshop sheet._",
        "",
    ]
    for path in sorted(set(paths)):
        lines.append(f"- `{path}`")
    lines.extend(
        [
            "",
            "**Handoff asks:** What intake is still unverified? What is staged but uncommitted? "
            "Record freeze still binding (yes by default).",
            "",
        ]
    )
    return lines


def _parse_ahead_behind(status_sb_lines: list[str]) -> str:
    for line in status_sb_lines:
        if line.startswith("## "):
            branch_part = line[3:].strip()
            if "[" in branch_part and "]" in branch_part:
                return branch_part
            if "..." in branch_part:
                return branch_part
            return branch_part
    return "unknown"


def _status_path(line: str) -> str:
    return line[3:].strip() if len(line) > 3 else line.strip()


def build_ship_receipt(
    *,
    status_lines: list[str] | None = None,
    branch_lines: list[str] | None = None,
    status_sb_lines: list[str] | None = None,
    origin_main_lines: list[str] | None = None,
    recent_commits: list[str] | None = None,
    skip_origin_main: bool = False,
) -> list[str]:
    """Compact ship-state block for post-commit / signing-off handoff."""
    branch = "unknown"
    if status_lines is None and status_sb_lines is None and branch_lines is None:
        bundled_status, bundled_sb, bundled_branch = _run_git_status_bundle()
        status_lines = bundled_status
        status_sb_lines = bundled_sb
        branch = bundled_branch
    else:
        if status_lines is None:
            status_lines = _run_git("status", "--short")
        if branch_lines is None:
            branch_lines = _run_git("branch", "--show-current")
        if status_sb_lines is None:
            status_sb_lines = _run_git("status", "-sb")
        branch = branch_lines[0] if branch_lines else "unknown"
    if origin_main_lines is None and not skip_origin_main:
        origin_main_lines = _run_git("rev-parse", "origin/main")
    if recent_commits is None:
        recent_commits = _run_git("log", "--oneline", "-3")

    if branch_lines is not None and branch == "unknown":
        branch = branch_lines[0] if branch_lines else "unknown"
    ahead_behind = _parse_ahead_behind(status_sb_lines)
    if skip_origin_main:
        origin_main = "skipped (--fast)"
    else:
        origin_main = (
            origin_main_lines[0]
            if origin_main_lines and not origin_main_lines[0].startswith("git ")
            else "unavailable"
        )

    meaningful: list[str] = []
    runtime_noise: list[str] = []
    export_churn: list[str] = []
    for line in status_lines:
        category, _path = _classify_change(line)
        if category == "runtime_noise":
            runtime_noise.append(line)
        elif category == "export_churn":
            export_churn.append(line)
        else:
            meaningful.append(line)

    slices: dict[str, list[str]] = {
        "statecraft": [],
        "ph-civ": [],
        "singularity": [],
        "other": [],
    }
    for line in meaningful:
        path = _status_path(line)
        bucket = _classify_lane_slice(path)
        slices[bucket].append(path)

    ahead_count = 0
    if "ahead" in ahead_behind:
        match = re.search(r"ahead (\d+)", ahead_behind)
        if match:
            ahead_count = int(match.group(1))

    clean_tree = len(meaningful) == 0
    if ahead_count > 0 and clean_tree:
        suggested_push = f"git push origin {branch}"
    elif ahead_count > 0:
        suggested_push = f"commit remaining slices, then `git push origin {branch}`"
    else:
        suggested_push = "no push needed (not ahead of upstream)"

    lines = [
        "## Ship receipt",
        "",
        f"- **Branch:** `{branch}`",
        f"- **Tracking:** {ahead_behind}",
        f"- **origin/main:** `{origin_main}`",
        "",
        "### Uncommitted slices",
        "",
    ]
    any_slice = False
    for key in ("statecraft", "ph-civ", "singularity", "other"):
        paths = slices[key]
        if paths:
            any_slice = True
            lines.append(f"- **{key}:** {len(paths)} file(s)")
            for p in paths[:5]:
                lines.append(f"  - `{p}`")
            if len(paths) > 5:
                lines.append(f"  - _… and {len(paths) - 5} more_")
    if not any_slice:
        lines.append("- _Clean working tree (meaningful changes)._")

    lines.extend(["", "### Recent local commits", ""])
    if recent_commits:
        for commit in recent_commits:
            lines.append(f"- `{commit}`")
    else:
        lines.append("- _No recent commits found._")

    lines.extend(["", "### Suggested push", "", f"- {suggested_push}", ""])

    excluded: list[str] = []
    for line in meaningful + export_churn + runtime_noise:
        excluded.append(_status_path(line))
    if excluded:
        lines.extend(["### Excluded WIP (not in last commit)", ""])
        for path in excluded[:12]:
            lines.append(f"- `{path}`")
        if len(excluded) > 12:
            lines.append(f"- _… and {len(excluded) - 12} more_")
        lines.append("")

    return lines


def _classify_change(path_line: str) -> tuple[str, str]:
    path = path_line[3:] if len(path_line) > 3 else path_line
    if any(marker in path for marker in RUNTIME_NOISE_MARKERS):
        return "runtime_noise", path
    if any(marker in path for marker in EXPORT_CHURN_MARKERS):
        return "export_churn", path
    if (
        path.startswith(".cursor/skills/")
        or path == "docs/operator-skills.md"
        or path.startswith("scripts/operator_")
    ):
        return "operator_workflow", path
    if (
        "work-politics" in path
        or         "operator-pol" in path
        or "operator-wap" in path
        or "work_politics" in path
        or "generate_wap_weekly_brief.py" in path
    ):
        return "work_politics_lane", path
    if path.startswith("") or "recursion_gate" in path or path == "archive/grace-mar-instance/bot/prompt.py":
        return "record_pipeline", path
    return "repo_misc", path


def _gate_detail_lines(recursion_gate_md: str, user_id: str) -> list[str]:
    """Human-readable pending queue + proposed merge steps (read-only; does not merge)."""
    try:
        from strategy_codex_config import record_frozen
    except ImportError:
        from scripts.strategy_codex_config import record_frozen  # type: ignore
    if record_frozen():
        return [
            "## RECURSION-GATE (frozen)",
            "",
            "Grace-Mar Record is operator-archived. Gate review is **fork revive only**.",
            "See `docs/grace-mar-instance-boundary.md`. Say **`fork revive`** or coffee **`A gate`** to reopen.",
            "",
        ]
    gate_rel = f"{user_id}/recursion-gate.md"
    politics_rows, companion_rows = pending_by_territory(recursion_gate_md)
    total = len(politics_rows) + len(companion_rows)
    lines: list[str] = [
        "## RECURSION-GATE (pending)",
        "",
        f"- **Total pending:** {total} (work-politics: {len(politics_rows)} · companion: {len(companion_rows)})",
        f"- **Canonical file:** `{gate_rel}`",
        "",
    ]
    if total == 0:
        lines.extend(
            [
                "_No pending candidates above `## Processed`._",
                "",
                "## Proposed: processing pipeline (when you have new candidates)",
                "",
                "1. Stage or confirm candidates in `recursion-gate.md` (pending, above Processed).",
                "2. Review: open the gate file or run "
                f"`python3 scripts/operator_gate_review_pass.py -u {user_id}` for a recommendation-oriented pass.",
                "3. Set `status: approved` or `status: rejected` per companion/operator policy.",
                "4. Merge approved candidates only: "
                f"`python3 scripts/process_approved_candidates.py -u {user_id} --apply` "
                "(or the receipt flow in AGENTS.md). **Record changes require companion approval.**",
                "",
            ]
        )
        return lines

    combined: list[tuple[str, dict]] = [
        *[(TERRITORY_LABEL_WORK_POLITICS, r) for r in politics_rows],
        *[("Companion", r) for r in companion_rows],
    ]
    lines.append("### Pending items")
    lines.append("")
    shown = 0
    for label, row in combined:
        if shown >= _GATE_PENDING_DISPLAY_CAP:
            rest = total - shown
            lines.append(f"- _â€¦ and {rest} more â€” open `{gate_rel}` for full list._")
            break
        cid = row.get("id") or "?"
        summary = (row.get("summary") or "(no summary)")[:160]
        lines.append(f"- **{cid}** [{label}] â€” {summary}")
        shown += 1
    lines.extend(
        [
            "",
            "## Proposed: complete processing (this handoff does not merge)",
            "",
            f"1. **Review** each pending row in `{gate_rel}` "
            f"or run `python3 scripts/operator_gate_review_pass.py -u {user_id}`.",
            "2. **Decide** `status: approved` or `status: rejected` (companion policy for Record-facing items).",
            "3. **Apply** approved merges only: "
            f"`python3 scripts/process_approved_candidates.py -u {user_id} --apply` "
            "(or `--generate-receipt` / `--apply --receipt` per AGENTS.md).",
            "4. **Verify** pending count is zero: re-run this script or `python3 scripts/harness_warmup.py -u "
            f"{user_id}`.",
            "",
        ]
    )
    return lines


def _record_frozen() -> bool:
    try:
        from strategy_codex_config import record_frozen
    except ImportError:
        from scripts.strategy_codex_config import record_frozen  # type: ignore
    return record_frozen()


def _active_thread(meaningful_changes: list[str], gate_pending: int, politics_blockers: list[dict]) -> tuple[str, str]:
    frozen = _record_frozen()
    counts = {
        "operator_workflow": 0,
        "work_politics_lane": 0,
        "record_pipeline": 0,
        "repo_misc": 0,
    }
    for raw in meaningful_changes:
        category, _path = _classify_change(raw)
        if category in counts:
            counts[category] += 1
    dominant = max(counts, key=counts.get)
    if counts[dominant] == 0:
        if gate_pending and not frozen:
            return (
                "gate continuity",
                "Start with `python3 scripts/operator_gate_review_pass.py` to review pending candidates.",
            )
        if gate_pending and frozen:
            return (
                "interpretive machine",
                "Record is frozen — say `fork revive` before gate work; otherwise run statecraft health checks or ship receipt.",
            )
        if politics_blockers:
            return (
                "work-politics lane",
                "Start with `python3 scripts/operator_work_politics_pulse.py` and address the first blocker.",
            )
        return (
            "stable baseline",
            "Start with `python3 scripts/operator_daily_warmup.py` and choose the next highest-value task.",
        )
    if dominant == "operator_workflow":
        return (
            "operator workflow stack",
            "Resume the operator workflow pass and either test or commit the local workflow files.",
        )
    if dominant == "work_politics_lane":
        return (
            "work-politics lane",
            "Resume work-politics work with `python3 scripts/operator_work_politics_pulse.py` and then run the brief workflow if ready.",
        )
    if dominant == "record_pipeline":
        if frozen:
            return (
                "archived record paths",
                "Record is frozen — avoid Record-adjacent edits unless you invoked `fork revive`; prefer boundary/git Steward track.",
            )
        return (
            "record pipeline",
            "Resume with a gate review before making any Record-adjacent edits (fork active only).",
        )
    return (
        "mixed repo maintenance",
        "Start with `python3 scripts/operator_daily_warmup.py` and sort local changes into one active thread.",
    )


def build_fast_receipt(user_id: str = "strategy-codex") -> str:
    """Ship receipt only — fewer git calls, no lane snapshots."""
    _ = user_id
    lines = ["# Handoff check (fast)", ""]
    lines.extend(build_ship_receipt(skip_origin_main=True))
    lines.extend(
        [
            "",
            "## Guardrail",
            "",
            "- Fast mode: ship receipt only. Full handoff: `python3 scripts/operator_handoff_check.py`.",
            "",
        ]
    )
    return "\n".join(lines)


def build_handoff_check(user_id: str = "strategy-codex", *, fast: bool = False) -> str:
    if fast:
        return build_fast_receipt(user_id=user_id)
    user_dir = USERS_DIR / user_id
    recursion_gate = _read(user_dir / "recursion-gate.md")
    evidence = _read(user_dir / "self-archive.md") or _read(user_dir / "self-evidence.md")
    gate_pending = _pending_candidates(recursion_gate, "all")
    last_activity = _last_activity_oneliner(archive/placeholders/evidence) or "_none parsed_"
    politics_snapshot = get_work_politics_snapshot(user_id)

    status_lines, status_sb_lines, branch_from_bundle = _run_git_status_bundle()
    recent_commits = _run_git("log", "--oneline", "-3")
    runtime_noise: list[str] = []
    export_churn: list[str] = []
    meaningful_changes: list[str] = []
    for line in status_lines:
        category, _path = _classify_change(line)
        if category == "runtime_noise":
            runtime_noise.append(line)
        elif category == "export_churn":
            export_churn.append(line)
        else:
            meaningful_changes.append(line)

    thread_label, reentry_prompt = _active_thread(
        meaningful_changes,
        gate_pending=len(gate_pending),
        politics_blockers=politics_snapshot.get("territory_blockers") or [],
    )

    lines = [
        "# Handoff check",
        "",
        f"- User: `{user_id}`",
        f"- Last activity: {last_activity}",
        f"- Pending gate items: {len(gate_pending)} (detail below)",
        f"- Active thread guess: {thread_label}",
        "",
    ]
    lines.extend(_gate_detail_lines(recursion_gate, user_id))
    lines.append("")
    if build_night_pulse_lines is not None:
        try:
            lines.extend(build_night_pulse_lines(user_id))
        except Exception:
            lines.append("## Predictive History â€” night closeout")
            lines.append("")
            lines.append("_Jiang night pulse skipped (could not read work-jiang paths)._")
            lines.append("")
    else:
        lines.append("## Predictive History â€” night closeout")
        lines.append("")
        lines.append(
            "_Run `python3 scripts/work_jiang/warmup_jiang_pulse.py -u %s --night` if import failed._" % user_id
        )
        lines.append("")
    lines.extend(
        build_ship_receipt(
            status_lines=status_lines,
            status_sb_lines=status_sb_lines,
            branch_lines=[branch_from_bundle],
            recent_commits=recent_commits,
        )
    )
    lines.extend(build_singularity_intake_nudge(status_lines))

    lines.extend(["", "## Local work still in progress", ""])
    if meaningful_changes:
        for line in meaningful_changes[:10]:
            lines.append(f"- `{line}`")
    else:
        lines.append("- No meaningful local changes detected.")

    lines.extend(["", "## Derived / export churn", ""])
    if export_churn:
        lines.append(
            "_Regenerated or integrity-adjacent files â€” often safe to batch-commit separately "
            "from editorial work, or refresh via bootstrap verify block (`export_prp`, "
            "`export_manifest`, `validate-integrity`)._"
        )
        lines.append("")
        for line in export_churn[:12]:
            lines.append(f"- `{line}`")
    else:
        lines.append("- No derived / export churn detected in `git status`.")

    lines.extend(["", "## Runtime noise", ""])
    if runtime_noise:
        for line in runtime_noise[:10]:
            lines.append(f"- `{line}`")
    else:
        lines.append("- No runtime-only local noise detected.")

    lines.extend(["", "## Work-politics continuity", ""])
    lines.append(f"- Territory blockers: {len(politics_snapshot.get('territory_blockers') or [])}")
    for action in (politics_snapshot.get("next_actions") or [])[:3]:
        lines.append(f"- {action}")

    lines.extend(["", "## Next re-entry prompt", ""])
    lines.append(f"- {reentry_prompt}")

    lines.extend(
        [
            "",
            "## Guardrail",
            "",
            "- Treat **derived / export churn** and **runtime noise** separately from meaningful "
            "local work before committing or pushing.",
            "- This workflow summarizes stop/resume state only; it does not stage, commit, or merge anything.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    _configure_utf8_stdio()
    parser = argparse.ArgumentParser(description="Generate a handoff summary for Grace-Mar.")
    parser.add_argument("--user", "-u", default="strategy-codex", help="Profile id")
    parser.add_argument(
        "--fast",
        action="store_true",
        help="Ship receipt only (fewer git calls; skip politics/Jiang/gate detail).",
    )
    parser.add_argument(
        "--receipt",
        action="store_true",
        dest="fast",
        help="Alias for --fast.",
    )
    args = parser.parse_args()
    print(build_handoff_check(user_id=args.user, fast=args.fast))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

