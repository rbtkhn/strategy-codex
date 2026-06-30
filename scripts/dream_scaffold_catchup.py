#!/usr/bin/env python3
"""Since-previous-dream statecraft archive scaffold audit (report-only by default).

Backstop for missed post-land normalization — does not replace intake hooks.
Reuses ``dream_catchup.local_calendar_dates`` window semantics.

Usage:
    python3 scripts/dream_scaffold_catchup.py --since-previous-dream -u strategy-codex
    python3 scripts/dream_scaffold_catchup.py --day 2026-06-16 --json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from dream_catchup import catch_up_window_dict  # noqa: E402
from normalize_breaking_points_scaffold import is_breaking_points_capture  # noqa: E402
from normalize_davis_deep_dive_scaffold import is_davis_capture  # noqa: E402
from normalize_dialogue_works_opening_scaffold import is_dialogue_works_capture  # noqa: E402
from normalize_mercouris_close_scaffold import (  # noqa: E402
    is_mercouris_solo_capture,
    normalize_mercouris,
)
from normalize_napolitano_opening_scaffold import (  # noqa: E402
    is_napolitano_capture,
    split_frontmatter,
)
from normalize_nawfal_opening_banter import is_nawfal_hosted  # noqa: E402
from normalize_redacted_scaffold import is_redacted_capture  # noqa: E402
from post_land_statecraft_family import apply_statecraft_capture_scaffold  # noqa: E402
from statecraft_day_archive import DEFAULT_ROOT as ARCHIVE_ROOT  # noqa: E402

DAY_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DEFAULT_MAX_APPLY = 25

MERCOURIS_PROMO_TAIL_RE = re.compile(
    r"(?:find all our programs|Locals,?\s*Rumble|Patreon|Subscribe\s*Star|"
    r"tick the like button|shop links under this video)",
    re.IGNORECASE,
)
NAWFAL_CLOSE_PROMO_TAIL_RE = re.compile(
    r"(?:subscribe to my Substack|Like comment in the tweet|"
    r"subscribe to the channel,?\s*have your notifications on|"
    r"That was Professor|we'll see you next time)",
    re.IGNORECASE,
)
GENERIC_PROMO_TAIL_RE = re.compile(
    r"(?:subscribe to the channel|tick the like button|find all our programs|"
    r"Like comment in the tweet|please subscribe to my Substack|"
    r"have your notifications on)",
    re.IGNORECASE,
)

def _files_for_day(day_iso: str) -> list[Path]:
    day_dir = ARCHIVE_ROOT / day_iso
    if not day_dir.is_dir():
        return []
    return sorted(
        p
        for p in day_dir.glob("source-*.md")
        if p.is_file() and p.name.lower() != "readme.md" and ".cleaned." not in p.name
    )

def _rel_path(path: Path, repo_root: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()

def _family_label(meta: dict[str, Any], path: Path) -> str | None:
    if is_napolitano_capture(meta, path):
        return "napolitano"
    if is_nawfal_hosted(meta, path):
        return "nawfal"
    if is_dialogue_works_capture(meta, path):
        return "dialogue-works"
    if is_mercouris_solo_capture(meta, path):
        return "mercouris-solo"
    if is_davis_capture(meta, path):
        return "davis-deep-dive"
    if is_redacted_capture(meta, path):
        return "redacted"
    if is_breaking_points_capture(meta, path):
        return "breaking-points"
    return None

def audit_capture(path: Path, *, repo_root: Path = REPO_ROOT) -> list[dict[str, Any]]:
    """Return zero or more audit action rows for one capture file."""
    rel = _rel_path(path, repo_root)
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return [{"path": rel, "status": "read_error", "detail": str(exc)}]

    meta, _ = split_frontmatter(text)
    actions: list[dict[str, Any]] = []

    completeness = meta.get("transcript_completeness")
    if completeness == "truncated_tail":
        actions.append({"path": rel, "status": "blocked_truncated"})
        return actions

    tail = text[-2500:]
    if meta.get("mercouris_close_promo_trim_applied") and MERCOURIS_PROMO_TAIL_RE.search(tail):
        actions.append({"path": rel, "status": "stale_mercouris_close_flag", "family": "mercouris-solo"})
        changed, _, change = normalize_mercouris(path, text, apply=False, force_close=True)
        if changed and change and change.close_promo_trimmed:
            actions.append(
                {
                    "path": rel,
                    "status": "would_trim",
                    "family": "mercouris-solo",
                    "anchor": change.anchor,
                    "chars": change.chars_removed,
                    "flags": f"force-close,{change.anchor}",
                }
            )

    if meta.get("nawfal_close_promo_trim_applied") and NAWFAL_CLOSE_PROMO_TAIL_RE.search(tail):
        actions.append({"path": rel, "status": "stale_nawfal_close_flag", "family": "nawfal"})

    family = _family_label(meta, path)
    scaffold = apply_statecraft_capture_scaffold(path, dry_run=True)
    if scaffold.family and scaffold.family_status == "dry-run":
        actions.append(
            {
                "path": rel,
                "status": "would_trim",
                "family": scaffold.family,
                "flags": scaffold.family_flags,
            }
        )
    elif (
        scaffold.caption
        and scaffold.caption.status == "dry-run"
        and scaffold.caption.flags
        and scaffold.caption.flags != "metadata"
    ):
        actions.append(
            {
                "path": rel,
                "status": "needs_caption_wrapper",
                "flags": scaffold.caption.flags,
            }
        )

    if (
        family is None
        and GENERIC_PROMO_TAIL_RE.search(text[-3500:])
        and not any(a["status"] in ("would_trim", "blocked_truncated") for a in actions)
        and not any(a["status"].startswith("stale_") for a in actions)
    ):
        actions.append({"path": rel, "status": "needs_manual_review"})

    return actions

def _summarize(all_actions: list[dict[str, Any]]) -> dict[str, int]:
    counts = {
        "would_trim": 0,
        "applied": 0,
        "blocked_truncated": 0,
        "stale_flags": 0,
        "needs_caption_wrapper": 0,
        "needs_manual_review": 0,
        "read_error": 0,
    }
    seen_would_trim: set[str] = set()
    for row in all_actions:
        status = row.get("status", "")
        path = row.get("path", "")
        if status == "would_trim":
            if path not in seen_would_trim:
                seen_would_trim.add(path)
                counts["would_trim"] += 1
        elif status == "blocked_truncated":
            counts["blocked_truncated"] += 1
        elif status.startswith("stale_"):
            counts["stale_flags"] += 1
        elif status == "needs_caption_wrapper":
            counts["needs_caption_wrapper"] += 1
        elif status == "needs_manual_review":
            counts["needs_manual_review"] += 1
        elif status == "read_error":
            counts["read_error"] += 1
    return counts

def _needs_apply(rows: list[dict[str, Any]]) -> tuple[bool, bool]:
    """Return (should_apply, force_mercouris_close)."""
    if any(r.get("status") == "blocked_truncated" for r in rows):
        return False, False
    force = any(r.get("status") == "stale_mercouris_close_flag" for r in rows)
    would = any(r.get("status") == "would_trim" for r in rows)
    caption = any(r.get("status") == "needs_caption_wrapper" for r in rows)
    return would or force or caption, force

def _apply_capture(
    path: Path,
    *,
    force_mercouris_close: bool,
) -> bool:
    result = apply_statecraft_capture_scaffold(
        path,
        dry_run=False,
        force_mercouris_close=force_mercouris_close,
    )
    return result.changed

def run_scaffold_catchup(
    *,
    local_dates: list[date],
    repo_root: Path = REPO_ROOT,
    apply: bool = False,
    max_apply: int = DEFAULT_MAX_APPLY,
    refresh_indices: bool = True,
) -> dict[str, Any]:
    """Audit captures for local dates; optionally apply bounded post-land repair."""
    by_day: dict[str, Any] = {}
    all_actions: list[dict[str, Any]] = []
    files_scanned = 0
    skipped_no_folder = 0
    applied_count = 0
    deferred_over_cap = 0
    apply_paths: list[tuple[Path, bool]] = []

    for d in sorted(local_dates):
        iso = d.isoformat()
        files = _files_for_day(iso)
        if not files and not (ARCHIVE_ROOT / iso).is_dir():
            skipped_no_folder += 1
            continue
        day_actions: list[dict[str, Any]] = []
        for path in files:
            files_scanned += 1
            rows = audit_capture(path, repo_root=repo_root)
            day_actions.extend(rows)
            all_actions.extend(rows)
            should, force = _needs_apply(rows)
            if apply and should:
                apply_paths.append((path, force))
        if day_actions or files:
            by_day[iso] = {"files": len(files), "actions": day_actions}

    if apply and apply_paths:
        for path, force in apply_paths:
            if applied_count >= max_apply:
                deferred_over_cap += 1
                continue
            rows = audit_capture(path, repo_root=repo_root)
            if any(r.get("status") == "blocked_truncated" for r in rows):
                continue
            if _apply_capture(path, force_mercouris_close=force):
                applied_count += 1
                rel = _rel_path(path, repo_root)
                all_actions.append({"path": rel, "status": "applied", "family": "batch"})
        if applied_count > 0 and refresh_indices:
            import refresh_statecraft_archive_indices as refresh

            stale_count, _ = refresh.refresh_or_check(ARCHIVE_ROOT, check=False)
            all_actions.append(
                {
                    "path": str(ARCHIVE_ROOT.relative_to(repo_root)),
                    "status": "index_refresh",
                    "flags": str(stale_count),
                }
            )

    summary = _summarize(all_actions)
    summary["applied"] = applied_count
    summary["deferred_over_cap"] = deferred_over_cap
    exit_code = 1 if summary["blocked_truncated"] > 0 or summary["read_error"] > 0 else 0

    mode = "apply" if apply else "report"
    return {
        "semantics": "since_previous_dream",
        "mode": mode,
        "max_apply": max_apply if apply else None,
        "days_scanned": len(by_day),
        "files_scanned": files_scanned,
        "skipped_no_folder": skipped_no_folder,
        "summary": summary,
        "by_day": by_day,
        "exit_code": exit_code,
    }

def format_scaffold_catchup_line(catchup: dict[str, Any]) -> str | None:
    """One-line human summary for auto_dream / CLI."""
    if not catchup:
        return None
    if catchup.get("error"):
        return f"statecraft scaffold catch-up: error — {catchup['error']}"
    summary = catchup.get("summary") or {}
    days = catchup.get("days_scanned", 0)
    would = summary.get("would_trim", 0)
    stale = summary.get("stale_flags", 0)
    blocked = summary.get("blocked_truncated", 0)
    manual = summary.get("needs_manual_review", 0)
    caption = summary.get("needs_caption_wrapper", 0)
    applied = summary.get("applied", 0)
    deferred = summary.get("deferred_over_cap", 0)
    mode_label = catchup.get("mode", "report")
    if days == 0 and catchup.get("files_scanned", 0) == 0:
        return None
    parts = [f"would_trim={would}", f"stale_flags={stale}", f"blocked={blocked}"]
    if applied:
        parts.append(f"applied={applied}")
    if deferred:
        parts.append(f"deferred={deferred}")
    if caption:
        parts.append(f"caption={caption}")
    if manual:
        parts.append(f"manual={manual}")
    return f"statecraft scaffold catch-up: {days} day(s) — {', '.join(parts)} ({mode_label})"

def scaffold_catchup_followups(catchup: dict[str, Any]) -> list[str]:
    """Optional handoff followup lines."""
    out: list[str] = []
    if not catchup or catchup.get("error"):
        return out
    summary = catchup.get("summary") or {}
    if summary.get("blocked_truncated", 0) > 0:
        paths = [
            a["path"]
            for day in (catchup.get("by_day") or {}).values()
            for a in day.get("actions") or []
            if a.get("status") == "blocked_truncated"
        ]
        sample = ", ".join(paths[:3])
        out.append(f"Statecraft truncated tail(s) — re-ingest before trim ({sample})")
    if summary.get("stale_flags", 0) > 0:
        out.append(
            "Statecraft stale scaffold trim flag(s) — run post-land or "
            "python3 scripts/dream_scaffold_catchup.py --since-previous-dream"
        )
    if summary.get("would_trim", 0) > 0 and summary.get("stale_flags", 0) == 0:
        out.append(
            "Statecraft scaffold would_trim — run post_land_statecraft_batch for catch-up day(s)"
        )
    if summary.get("applied", 0) > 0:
        out.append(
            f"Statecraft scaffold catch-up applied {summary['applied']} file(s) "
            f"(cap={catchup.get('max_apply')})"
        )
    return out

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--since-previous-dream",
        action="store_true",
        help="Use dream_catchup local_calendar_dates window",
    )
    parser.add_argument("--day", action="append", default=[], metavar="YYYY-MM-DD")
    parser.add_argument("-u", "--user", default="strategy-codex")
    parser.add_argument("--users-dir", type=Path, default=REPO_ROOT / "platform/users")
    parser.add_argument("--json", action="store_true")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply bounded post-land repair (default cap 25; use --max-apply)",
    )
    parser.add_argument(
        "--max-apply",
        type=int,
        default=DEFAULT_MAX_APPLY,
        help=f"Max files to apply per run (default {DEFAULT_MAX_APPLY})",
    )
    parser.add_argument(
        "--no-index-refresh",
        action="store_true",
        help="Skip archive index refresh after apply",
    )
    args = parser.parse_args()

    if args.since_previous_dream:
        window = catch_up_window_dict(users_dir=args.users_dir, user_id=args.user)
        if window.get("error"):
            payload = {"error": window["error"]}
            if args.json:
                print(json.dumps(payload, indent=2))
            else:
                print(f"error: {window['error']}", file=sys.stderr)
            return 1
        local_dates = [date.fromisoformat(s) for s in window.get("local_calendar_dates") or []]
    elif args.day:
        local_dates = []
        for raw in args.day:
            if not DAY_RE.match(raw):
                print(f"invalid --day {raw!r}", file=sys.stderr)
                return 2
            local_dates.append(date.fromisoformat(raw))
    else:
        parser.error("provide --since-previous-dream or --day YYYY-MM-DD")

    result = run_scaffold_catchup(
        local_dates=local_dates,
        apply=args.apply,
        max_apply=max(1, args.max_apply),
        refresh_indices=not args.no_index_refresh,
    )
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        line = format_scaffold_catchup_line(result)
        if line:
            print(line)
        else:
            print("statecraft scaffold catch-up: no archive days in window")
        for followup in scaffold_catchup_followups(result):
            print(f"  follow-up: {followup}")
    return int(result.get("exit_code", 0))

if __name__ == "__main__":
    raise SystemExit(main())
