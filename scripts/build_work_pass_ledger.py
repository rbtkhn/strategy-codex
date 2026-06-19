#!/usr/bin/env python3
"""Build a WORK-only work-pass ledger from extended coffee_close cadence and close notes.

Phase 3+ observability SSOT — replaces conductor-branded ledger naming while keeping
legacy conductor audit fields for read-only archaeology.
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from repo_io import ARTIFACTS_DIR

from audit_cadence_rhythm import EVENTS_PATH, compute_conductor_audit, parse_events
from cadence_conductor_resolution import (
    active_conductor_arc,
    compiled_shortcut_for_conductor,
    should_offer_compiled_shortcut,
)

DEFAULT_OUTPUT = ARTIFACTS_DIR / "context" / "work-pass-ledger.md"
LEGACY_OUTPUT = ARTIFACTS_DIR / "context" / "conductor-ledger.md"
DEFAULT_FRICTION_ROOTS = (
    REPO_ROOT / "docs" / "skill-work" / "work-dev" / "dev-notebook" / "work-dev" / "journal",
    REPO_ROOT / "docs" / "skill-work" / "work-strategy",
)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-u", "--user-id", default="strategy-codex")
    parser.add_argument("--days", type=int, default=30)
    parser.add_argument("--max-closes", type=int, default=8)
    parser.add_argument("--max-friction", type=int, default=6)
    parser.add_argument("--events-path", type=Path, default=EVENTS_PATH)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument(
        "--legacy-output",
        action="store_true",
        help="Also write runtime/artifacts/context/conductor-ledger.md (compatibility mirror)",
    )
    return parser.parse_args()


def collect_recent_work_pass_closes(
    user_id: str,
    *,
    days: int = 30,
    events_path: Path = EVENTS_PATH,
    now: datetime | None = None,
    limit: int = 8,
) -> list[dict[str, Any]]:
    """Collect recent coffee_close rows (+ legacy coffee_conductor_outcome read-only)."""
    now = now or datetime.now(timezone.utc)
    cutoff = now - timedelta(days=days)
    events = [e for e in parse_events(user_id, events_path=events_path) if e["dt"] >= cutoff]
    events.sort(key=lambda e: e["dt"])
    combined: list[dict[str, Any]] = []
    for event in events:
        kv = event.get("kv") or {}
        if event.get("kind") == "coffee_close":
            combined.append(
                {
                    "kind": "coffee_close",
                    "ts": event["dt"].isoformat(),
                    "conductor": str(kv.get("conductor", "")).strip()
                    or str(kv.get("attention", "")).strip()
                    or str(kv.get("picked", "")).strip()
                    or "work-pass",
                    "picked": str(kv.get("picked", "")).strip() or None,
                    "outcome": str(kv.get("outcome", "")).strip() or None,
                    "readiness": str(kv.get("readiness", "")).strip() or None,
                    "verdict": str(kv.get("verdict", "")).strip() or None,
                    "object_ref": str(kv.get("object_ref", "")).strip() or None,
                    "falsify": str(kv.get("falsify", "")).strip() or None,
                    "attention": str(kv.get("attention", "")).strip() or None,
                    "artifacts": str(kv.get("artifacts", "")).strip() or None,
                    "next": str(kv.get("next", "")).strip() or None,
                    "loops": str(kv.get("loops", "")).strip() or None,
                    "legacy": False,
                }
            )
        elif event.get("kind") == "coffee_conductor_outcome":
            combined.append(
                {
                    "kind": "coffee_conductor_outcome",
                    "ts": event["dt"].isoformat(),
                    "conductor": str(kv.get("conductor", "")).strip() or "unattributed",
                    "verdict": str(kv.get("verdict", "")).strip() or None,
                    "notebook_ref": str(kv.get("notebook_ref", "")).strip() or None,
                    "falsify": str(kv.get("falsify", "")).strip() or None,
                    "action": str(kv.get("action", "")).strip() or None,
                    "legacy": True,
                }
            )
    return combined[-limit:]


# Compatibility alias (Phase 3 read-only)
collect_recent_conductor_closes = collect_recent_work_pass_closes


def collect_friction_candidates(
    *,
    search_roots: tuple[Path, ...] = DEFAULT_FRICTION_ROOTS,
    max_items: int = 6,
) -> list[dict[str, str]]:
    if max_items <= 0:
        return []
    results: list[dict[str, str]] = []
    for root in search_roots:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*.md")):
            if path.name == "CONDUCTOR-CLOSE-TEMPLATE.md":
                continue
            try:
                lines = path.read_text(encoding="utf-8").splitlines()
            except OSError:
                continue
            for idx, line in enumerate(lines, start=1):
                if "**Friction / rule candidate" not in line:
                    continue
                if "<what failed" in line:
                    continue
                text = line.strip()
                if text.startswith("- "):
                    text = text[2:].strip()
                prefix = "**Friction / rule candidate (optional):**"
                if text.startswith(prefix):
                    text = text[len(prefix) :].strip()
                if not text.endswith(":") and text:
                    try:
                        display_path = str(path.relative_to(REPO_ROOT)).replace("\\", "/")
                    except ValueError:
                        display_path = str(path).replace("\\", "/")
                    results.append(
                        {
                            "path": display_path,
                            "line": str(idx),
                            "text": text,
                        }
                    )
                if len(results) >= max_items:
                    return results
    return results


def build_work_pass_ledger(
    user_id: str,
    *,
    days: int = 30,
    now: datetime | None = None,
    events_path: Path = EVENTS_PATH,
    max_closes: int = 8,
    max_friction: int = 6,
) -> dict[str, Any]:
    now = now or datetime.now(timezone.utc)
    audit = compute_conductor_audit(
        user_id,
        days=days,
        events_path=events_path,
        now=now,
    )
    recent_events = [
        e for e in parse_events(user_id, events_path=events_path) if e["dt"] >= now - timedelta(days=days)
    ]
    recent_events.sort(key=lambda e: e["dt"])
    active = active_conductor_arc(recent_events)
    active_slug = str(active.get("conductor")) if active else None
    recent_closes = collect_recent_work_pass_closes(
        user_id,
        days=days,
        events_path=events_path,
        now=now,
        limit=max_closes,
    )
    work_pass_closes = sum(1 for row in recent_closes if row.get("kind") == "coffee_close")
    legacy_outcomes = sum(1 for row in recent_closes if row.get("kind") == "coffee_conductor_outcome")
    return {
        "user_id": user_id,
        "days": days,
        "generated_at": now.isoformat(),
        "audit": audit,
        "active_arc": active,
        "compiled_shortcut_offer": (
            compiled_shortcut_for_conductor(active_slug)
            if active_slug and should_offer_compiled_shortcut(recent_events, active_slug)
            else None
        ),
        "recent_closes": recent_closes,
        "work_pass_close_count": work_pass_closes,
        "legacy_outcome_count": legacy_outcomes,
        "friction_candidates": collect_friction_candidates(max_items=max_friction),
    }


# Compatibility alias (Phase 3 read-only)
build_conductor_ledger = build_work_pass_ledger


def render_work_pass_ledger_markdown(payload: dict[str, Any]) -> str:
    audit = payload["audit"]
    closure = audit["closure"]
    active = payload.get("active_arc")
    lines = [
        "# Work-pass ledger",
        "",
        "WORK only; derived from extended `coffee_close` cadence (+ legacy conductor rows read-only). Not Record.",
        "",
        f"- Window: last `{payload['days']}` day(s)",
        f"- Generated: `{payload['generated_at']}`",
        f"- User: `{payload['user_id']}`",
        (
            f"- Recent rows: `{payload.get('work_pass_close_count', 0)}` coffee_close / "
            f"`{payload.get('legacy_outcome_count', 0)}` legacy outcome"
        ),
        "",
        "## Snapshot",
        "",
        (
            "- Picks / explicit outcomes / inferred outcomes: "
            f"`{audit['explicit_pick_count']}` / `{audit['explicit_outcome_count']}` / "
            f"`{audit['inferred_outcome_count']}`"
        ),
        (
            "- Unmatched explicit picks / inferred closure rate: "
            f"`{closure['open_pick_count']}` / `{closure['closure_rate']}`"
        ),
        (
            "- Outcome receipts with `notebook_ref=` / `falsify=`: "
            f"`{audit['evidence_richness']['notebook_ref']}` / "
            f"`{audit['evidence_richness']['falsify']}`"
        ),
        "",
        "## Continuity",
        "",
    ]
    if active:
        lines.extend(
            [
                f"- Inferred active conductor arc (legacy read): `{active['conductor']}`",
                f"- Picked at: `{active['picked_at'].isoformat()}`",
                f"- Outcome count since pick: `{active['outcome_count']}`",
            ]
        )
        if active.get("focus"):
            lines.append(f"- Focus: `{active['focus']}`")
        if payload.get("compiled_shortcut_offer"):
            lines.append(
                f"- Advisory compiled shortcut offer: `{payload['compiled_shortcut_offer']}`"
            )
    else:
        lines.append("- No inferred open legacy conductor arc detected from cadence.")

    lines.extend(["", "## Per-Conductor Counts (legacy audit)", ""])
    all_conductors = sorted(
        set(audit["explicit_picks_by_conductor"])
        | set(audit["explicit_outcomes_by_conductor"])
        | set(audit["inferred_outcomes_by_conductor"])
        | set(audit["coffee_close_closes_by_conductor"])
    )
    if all_conductors:
        lines.extend(
            [
                "| Conductor | Picks | Explicit outcomes | Inferred outcomes | Coffee closes |",
                "|---|---:|---:|---:|---:|",
            ]
        )
        for conductor in all_conductors:
            lines.append(
                "| `{}` | {} | {} | {} | {} |".format(
                    conductor,
                    audit["explicit_picks_by_conductor"].get(conductor, 0),
                    audit["explicit_outcomes_by_conductor"].get(conductor, 0),
                    audit["inferred_outcomes_by_conductor"].get(conductor, 0),
                    audit["coffee_close_closes_by_conductor"].get(conductor, 0),
                )
            )
    else:
        lines.append("- None in window.")

    lines.extend(["", "## Unmatched Explicit Picks", ""])
    if audit["open_picks"]:
        for row in audit["open_picks"][:8]:
            lines.append(f"- `{row['conductor']}` from `{row['ts']}`")
    else:
        lines.append("- None.")

    lines.extend(["", "## Recent closes", ""])
    if payload["recent_closes"]:
        for row in payload["recent_closes"]:
            ts = str(row.get("ts", ""))[:16]
            details: list[str] = [f"`{ts}`", f"`{row['conductor']}`", row["kind"]]
            if row.get("verdict"):
                details.append(f"verdict=`{row['verdict']}`")
            if row["kind"] == "coffee_conductor_outcome":
                if row.get("notebook_ref"):
                    details.append(f"notebook_ref=`{row['notebook_ref']}`")
                if row.get("falsify"):
                    details.append(f"falsify=`{row['falsify']}`")
                details.append("legacy=read-only")
            elif row["kind"] == "coffee_close":
                if row.get("picked"):
                    details.append(f"picked=`{row['picked']}`")
                if row.get("object_ref"):
                    details.append(f"object_ref=`{row['object_ref']}`")
                if row.get("falsify"):
                    details.append(f"falsify=`{row['falsify']}`")
                if row.get("attention"):
                    details.append(f"attention=`{row['attention']}`")
                if row.get("artifacts"):
                    details.append(f"artifacts=`{row['artifacts']}`")
                if row.get("next"):
                    details.append(f"next=`{row['next']}`")
                if row.get("loops"):
                    details.append(f"loops=`{row['loops']}`")
            lines.append("- " + " | ".join(details))
    else:
        lines.append("- None in window.")

    lines.extend(["", "## Friction watch", ""])
    if payload["friction_candidates"]:
        for row in payload["friction_candidates"]:
            lines.append(f"- `{row['path']}:{row['line']}` — {row['text']}")
    else:
        lines.append("- No recent friction/rule-candidate lines found in the scanned notebook roots.")

    return "\n".join(lines) + "\n"


# Compatibility alias (Phase 3 read-only)
render_conductor_ledger_markdown = render_work_pass_ledger_markdown


def main() -> int:
    args = _parse_args()
    payload = build_work_pass_ledger(
        args.user_id,
        days=args.days,
        events_path=args.events_path,
        max_closes=args.max_closes,
        max_friction=args.max_friction,
    )
    markdown = render_work_pass_ledger_markdown(payload)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(markdown, encoding="utf-8")
    else:
        print(markdown, end="")
    if args.legacy_output and not args.output:
        LEGACY_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        LEGACY_OUTPUT.write_text(markdown, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
