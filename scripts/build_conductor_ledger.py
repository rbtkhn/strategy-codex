#!/usr/bin/env python3
"""Build a WORK-only conductor ledger from cadence events and recent close notes."""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from audit_cadence_rhythm import EVENTS_PATH, compute_conductor_audit, parse_events
from cadence_conductor_resolution import (
    active_conductor_arc,
    compiled_shortcut_for_conductor,
    should_offer_compiled_shortcut,
)
DEFAULT_OUTPUT = REPO_ROOT / "artifacts" / "context" / "conductor-ledger.md"
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
    return parser.parse_args()


def collect_recent_conductor_closes(
    user_id: str,
    *,
    days: int = 30,
    events_path: Path = EVENTS_PATH,
    now: datetime | None = None,
    limit: int = 8,
) -> list[dict[str, Any]]:
    now = now or datetime.now(timezone.utc)
    cutoff = now - timedelta(days=days)
    events = [e for e in parse_events(user_id, events_path=events_path) if e["dt"] >= cutoff]
    events.sort(key=lambda e: e["dt"])
    closes: list[dict[str, Any]] = []
    for event in events:
        kv = event.get("kv") or {}
        if event.get("kind") == "coffee_conductor_outcome":
            closes.append(
                {
                    "kind": "coffee_conductor_outcome",
                    "ts": event["dt"].isoformat(),
                    "conductor": str(kv.get("conductor", "")).strip() or "unattributed",
                    "verdict": str(kv.get("verdict", "")).strip() or None,
                    "notebook_ref": str(kv.get("notebook_ref", "")).strip() or None,
                    "falsify": str(kv.get("falsify", "")).strip() or None,
                    "action": str(kv.get("action", "")).strip() or None,
                }
            )
        elif event.get("kind") == "coffee_close":
            conductor = str(kv.get("conductor", "")).strip()
            state = str(kv.get("conductor_state", "")).strip().lower()
            if conductor and state == "closed":
                closes.append(
                    {
                        "kind": "coffee_close",
                        "ts": event["dt"].isoformat(),
                        "conductor": conductor,
                        "verdict": str(kv.get("outcome", "")).strip() or None,
                        "notebook_ref": str(kv.get("artifacts", "")).strip() or None,
                        "falsify": str(kv.get("next", "")).strip() or None,
                        "action": str(kv.get("loops", "")).strip() or None,
                    }
                )
    return closes[-limit:]


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


def build_conductor_ledger(
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
    recent_events = [e for e in parse_events(user_id, events_path=events_path) if e["dt"] >= now - timedelta(days=days)]
    recent_events.sort(key=lambda e: e["dt"])
    active = active_conductor_arc(recent_events)
    active_slug = str(active.get("conductor")) if active else None
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
        "recent_closes": collect_recent_conductor_closes(
            user_id,
            days=days,
            events_path=events_path,
            now=now,
            limit=max_closes,
        ),
        "friction_candidates": collect_friction_candidates(max_items=max_friction),
    }


def render_conductor_ledger_markdown(payload: dict[str, Any]) -> str:
    audit = payload["audit"]
    closure = audit["closure"]
    active = payload.get("active_arc")
    lines = [
        "# Conductor Ledger",
        "",
        "WORK only; derived from cadence and close notes. Not Record.",
        "",
        f"- Window: last `{payload['days']}` day(s)",
        f"- Generated: `{payload['generated_at']}`",
        f"- User: `{payload['user_id']}`",
        "",
        "## Summary",
        "",
        f"- Explicit picks: `{audit['explicit_pick_count']}`",
        f"- Explicit outcomes: `{audit['explicit_outcome_count']}`",
        f"- Inferred outcomes: `{audit['inferred_outcome_count']}`",
        f"- Open arcs: `{closure['open_pick_count']}`",
        f"- Closure rate: `{closure['closure_rate']}`",
        f"- Outcome lines with `notebook_ref=`: `{audit['evidence_richness']['notebook_ref']}`",
        f"- Outcome lines with `falsify=`: `{audit['evidence_richness']['falsify']}`",
        "",
        "## Continuity",
        "",
    ]
    if active:
        lines.extend(
            [
                f"- Active conductor: `{active['conductor']}`",
                f"- Picked at: `{active['picked_at'].isoformat()}`",
                f"- Outcome count since pick: `{active['outcome_count']}`",
            ]
        )
        if active.get("focus"):
            lines.append(f"- Focus: `{active['focus']}`")
        if payload.get("compiled_shortcut_offer"):
            lines.append(
                f"- Compiled shortcut offer: `{payload['compiled_shortcut_offer']}`"
            )
    else:
        lines.append("- No open conductor arc detected from cadence.")

    lines.extend(["", "## Per-Conductor Counts", ""])
    all_conductors = sorted(
        set(audit["explicit_picks_by_conductor"])
        | set(audit["explicit_outcomes_by_conductor"])
        | set(audit["inferred_outcomes_by_conductor"])
        | set(audit["coffee_close_closes_by_conductor"])
    )
    for conductor in all_conductors:
        lines.append(
            "- `{}` picks={} explicit_outcomes={} inferred_outcomes={} coffee_closes={}".format(
                conductor,
                audit["explicit_picks_by_conductor"].get(conductor, 0),
                audit["explicit_outcomes_by_conductor"].get(conductor, 0),
                audit["inferred_outcomes_by_conductor"].get(conductor, 0),
                audit["coffee_close_closes_by_conductor"].get(conductor, 0),
            )
        )

    lines.extend(["", "## Open Arcs", ""])
    if audit["open_picks"]:
        for row in audit["open_picks"][:8]:
            lines.append(
                f"- `{row['conductor']}` from `{row['ts']}`"
            )
    else:
        lines.append("- None.")

    lines.extend(["", "## Recent Closes", ""])
    if payload["recent_closes"]:
        for row in payload["recent_closes"]:
            details: list[str] = [f"`{row['conductor']}`", row["kind"]]
            if row.get("verdict"):
                details.append(f"verdict=`{row['verdict']}`")
            if row.get("notebook_ref"):
                details.append(f"ref=`{row['notebook_ref']}`")
            if row.get("falsify"):
                details.append(f"falsify=`{row['falsify']}`")
            lines.append("- " + " | ".join(details))
    else:
        lines.append("- None in window.")

    lines.extend(["", "## Friction Watch", ""])
    if payload["friction_candidates"]:
        for row in payload["friction_candidates"]:
            lines.append(f"- `{row['path']}:{row['line']}` — {row['text']}")
    else:
        lines.append("- No recent friction/rule-candidate lines found in the scanned notebook roots.")

    return "\n".join(lines) + "\n"


def main() -> int:
    args = _parse_args()
    payload = build_conductor_ledger(
        args.user_id,
        days=args.days,
        events_path=args.events_path,
        max_closes=args.max_closes,
        max_friction=args.max_friction,
    )
    markdown = render_conductor_ledger_markdown(payload)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(markdown, encoding="utf-8")
    else:
        print(markdown, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
