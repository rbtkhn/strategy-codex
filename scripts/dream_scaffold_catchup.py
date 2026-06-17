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
from normalize_breaking_points_scaffold import (  # noqa: E402
    is_breaking_points_capture,
    normalize_breaking_points,
)
from normalize_davis_deep_dive_scaffold import is_davis_capture, normalize_davis  # noqa: E402
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
from normalize_redacted_scaffold import is_redacted_capture, normalize_redacted  # noqa: E402
from post_land_caption_wrapper_normalize import post_land_caption_wrapper_normalize  # noqa: E402
from post_land_dialogue_works_opening_normalize import (  # noqa: E402
    post_land_dialogue_works_opening_normalize,
)
from post_land_mercouris_close_normalize import post_land_mercouris_close_normalize  # noqa: E402
from post_land_napolitano_opening_normalize import post_land_napolitano_opening_normalize  # noqa: E402
from post_land_nawfal_opening_normalize import post_land_nawfal_opening_normalize  # noqa: E402
from statecraft_day_archive import DEFAULT_ROOT as ARCHIVE_ROOT  # noqa: E402

DAY_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

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


def _audit_off_post_land(path: Path, text: str, meta: dict[str, Any]) -> dict[str, Any] | None:
    """Dry-run family normalizers not yet routed through post_land batch."""
    if is_davis_capture(meta, path):
        changed, _, change = normalize_davis(path, text, apply=False)
        if changed and change:
            return {
                "status": "would_trim",
                "family": "davis-deep-dive",
                "anchor": change.anchor,
                "chars": change.chars_removed,
                "flags": change.anchor,
            }
    if is_redacted_capture(meta, path):
        changed, _, change = normalize_redacted(path, text, apply=False)
        if changed and change:
            return {
                "status": "would_trim",
                "family": "redacted",
                "anchor": change.anchor,
                "chars": change.chars_removed,
                "flags": change.anchor,
            }
    if is_breaking_points_capture(meta, path):
        changed, _, change = normalize_breaking_points(path, text, apply=False)
        if changed and change:
            return {
                "status": "would_trim",
                "family": "breaking-points",
                "anchor": change.anchor,
                "chars": change.chars_removed,
                "flags": change.anchor,
            }
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

    cap = post_land_caption_wrapper_normalize(path, dry_run=True)
    if cap.status == "dry-run" and cap.flags and cap.flags != "metadata":
        actions.append(
            {
                "path": rel,
                "status": "needs_caption_wrapper",
                "flags": cap.flags,
            }
        )

    family = _family_label(meta, path)
    post_land_hooks: list[tuple[str, Any]] = [
        ("napolitano", post_land_napolitano_opening_normalize),
        ("nawfal", post_land_nawfal_opening_normalize),
        ("dialogue-works", post_land_dialogue_works_opening_normalize),
        ("mercouris-solo", post_land_mercouris_close_normalize),
    ]
    post_land_would_trim = False
    for fam, hook in post_land_hooks:
        try:
            result = hook(path, dry_run=True)
        except (FileNotFoundError, ValueError):
            continue
        if result.status == "dry-run":
            post_land_would_trim = True
            actions.append(
                {
                    "path": rel,
                    "status": "would_trim",
                    "family": fam,
                    "flags": result.flags,
                }
            )

    if not post_land_would_trim:
        off_pl = _audit_off_post_land(path, text, meta)
        if off_pl:
            off_pl["path"] = rel
            actions.append(off_pl)

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


def run_scaffold_catchup(
    *,
    local_dates: list[date],
    repo_root: Path = REPO_ROOT,
    apply: bool = False,
) -> dict[str, Any]:
    """Audit (and optionally apply — not implemented in P0/P1) captures for local dates."""
    if apply:
        raise NotImplementedError(
            "apply mode is not enabled in P0/P1; use post_land_statecraft_batch at intake"
        )

    by_day: dict[str, Any] = {}
    all_actions: list[dict[str, Any]] = []
    files_scanned = 0
    skipped_no_folder = 0

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
        if day_actions or files:
            by_day[iso] = {"files": len(files), "actions": day_actions}

    summary = _summarize(all_actions)
    exit_code = 1 if summary["blocked_truncated"] > 0 or summary["read_error"] > 0 else 0

    return {
        "semantics": "since_previous_dream",
        "mode": "report",
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
    if days == 0 and catchup.get("files_scanned", 0) == 0:
        return None
    parts = [f"would_trim={would}", f"stale_flags={stale}", f"blocked={blocked}"]
    if caption:
        parts.append(f"caption={caption}")
    if manual:
        parts.append(f"manual={manual}")
    return f"statecraft scaffold catch-up: {days} day(s) — {', '.join(parts)} (report-only)"


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
    parser.add_argument("--users-dir", type=Path, default=REPO_ROOT / "users")
    parser.add_argument("--json", action="store_true")
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

    result = run_scaffold_catchup(local_dates=local_dates, apply=False)
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
