#!/usr/bin/env python3
"""Parse work-cadence-events.md for coffee runs in a rolling UTC window.

Operator maintenance only — not Record truth. Used by auto_dream for last-dream.json.
"""

from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_EVENTS_PATH = REPO_ROOT / "docs" / "skill-work" / "work-cadence" / "work-cadence-events.md"

# - **2026-04-02 20:46 UTC** — coffee (grace-mar) ok=true mode=work-start
_COFFEE_LINE = re.compile(
    r"^- \*\*(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}) UTC\*\* — coffee \(([^)]+)\)\s*(.*)$"
)
# - **2026-04-02 20:46 UTC** — coffee_pick (grace-mar) picked=E steward=gate
_COFFEE_PICK_LINE = re.compile(
    r"^- \*\*(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}) UTC\*\* — coffee_pick \(([^)]+)\)\s*(.*)$"
)
_CONDUCTOR_OUTCOME_LINE = re.compile(
    r"^- \*\*(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}) UTC\*\* .+? coffee_conductor_outcome \(([^)]+)\)\s*(.*)$"
)


# Accept the canonical em dash and mojibake variants that appear in older cadence logs.
_COFFEE_LINE = re.compile(
    r"^- \*\*(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}) UTC\*\* .+? coffee \(([^)]+)\)\s*(.*)$"
)
_COFFEE_PICK_LINE = re.compile(
    r"^- \*\*(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}) UTC\*\* .+? coffee_pick \(([^)]+)\)\s*(.*)$"
)


def _parse_trailing_kv(rest: str) -> tuple[bool | None, str | None, dict[str, str]]:
    ok: bool | None = None
    mode: str | None = None
    kv: dict[str, str] = {}
    for token in rest.split():
        if "=" not in token:
            continue
        key, _, val = token.partition("=")
        key, val = key.strip(), val.strip()
        if key == "ok":
            ok = val.lower() == "true"
        elif key == "mode":
            mode = val or None
        else:
            kv[key] = val
    return ok, mode, kv


def _parse_ts(date_part: str, time_part: str) -> datetime:
    dt = datetime.strptime(f"{date_part} {time_part}", "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)
    return dt


def parse_coffee_pick_cadence_lines(
    markdown: str,
    *,
    user_id: str,
    window_start: datetime,
    window_end: datetime,
    max_events: int = 40,
) -> list[dict[str, Any]]:
    """Return coffee_pick events for user_id with ts in [window_start, window_end], oldest first."""
    out: list[dict[str, Any]] = []
    for line in markdown.splitlines():
        m = _COFFEE_PICK_LINE.match(line.strip())
        if not m:
            continue
        uid = m.group(3).strip()
        if uid != user_id:
            continue
        ts = _parse_ts(m.group(1), m.group(2))
        if ts < window_start or ts > window_end:
            continue
        _ok, _mode, kv = _parse_trailing_kv(m.group(4).strip())
        raw_pick = (kv.get("picked") or "").strip()
        if not raw_pick:
            continue
        if raw_pick.lower() == "conductor":
            picked = "conductor"
        else:
            picked = raw_pick[0].upper()
        if picked not in {"A", "B", "C", "D", "E", "conductor"}:
            continue
        steward = (kv.get("steward") or "").strip().lower() or None
        cond = (kv.get("conductor") or "").strip() or None
        row: dict[str, Any] = {
            "ts_iso": ts.isoformat(),
            "picked": picked,
            "menu_label": raw_pick,
        }
        if steward in {"gate", "template", "both"}:
            row["steward"] = steward
        if cond:
            row["conductor"] = cond
        out.append(row)
    out.sort(key=lambda r: r["ts_iso"])
    if len(out) > max_events:
        out = out[-max_events:]
    return out


def parse_conductor_cadence_lines(
    markdown: str,
    *,
    user_id: str,
    window_start: datetime,
    window_end: datetime,
    max_events: int = 60,
) -> list[dict[str, Any]]:
    """Return Conductor pick/outcome telemetry in a rolling window."""
    events: list[dict[str, Any]] = []
    active_conductor: str | None = None
    for line in markdown.splitlines():
        stripped = line.strip()
        pick = _COFFEE_PICK_LINE.match(stripped)
        outcome = _CONDUCTOR_OUTCOME_LINE.match(stripped)
        if not pick and not outcome:
            continue
        m = pick or outcome
        assert m is not None
        uid = m.group(3).strip()
        if uid != user_id:
            continue
        ts = _parse_ts(m.group(1), m.group(2))
        if ts < window_start or ts > window_end:
            continue
        _ok, _mode, kv = _parse_trailing_kv(m.group(4).strip())
        if pick:
            conductor = (kv.get("conductor") or "").strip() or None
            raw_pick = (kv.get("picked") or "").strip() or None
            if not conductor:
                continue
            active_conductor = conductor
            events.append(
                {
                    "ts_iso": ts.isoformat(),
                    "kind": "pick",
                    "conductor": conductor,
                    "menu_label": raw_pick,
                }
            )
            continue
        conductor = (kv.get("conductor") or "").strip() or active_conductor
        row: dict[str, Any] = {
            "ts_iso": ts.isoformat(),
            "kind": "outcome",
            "conductor": conductor,
            "verdict": (kv.get("verdict") or "").strip() or None,
            "action": (kv.get("action") or "").strip() or None,
            "falsify": (kv.get("falsify") or "").strip() or None,
            "commit": (kv.get("commit") or "").strip() or None,
            "notebook_ref": (kv.get("notebook_ref") or "").strip() or None,
        }
        events.append({k: v for k, v in row.items() if v is not None})
    events.sort(key=lambda r: r["ts_iso"])
    if len(events) > max_events:
        events = events[-max_events:]
    return events


def parse_coffee_cadence_lines(
    markdown: str,
    *,
    user_id: str,
    window_start: datetime,
    window_end: datetime,
    max_runs: int = 20,
) -> list[dict[str, Any]]:
    """Return coffee events for user_id with ts in [window_start, window_end], oldest first."""
    runs: list[dict[str, Any]] = []
    for line in markdown.splitlines():
        m = _COFFEE_LINE.match(line.strip())
        if not m:
            continue
        uid = m.group(3).strip()
        if uid != user_id:
            continue
        ts = _parse_ts(m.group(1), m.group(2))
        if ts < window_start or ts > window_end:
            continue
        ok, mode, kv = _parse_trailing_kv(m.group(4).strip())
        runs.append(
            {
                "ts_iso": ts.isoformat(),
                "ok": ok,
                "mode": mode or "unknown",
                "kv": kv,
            }
        )
    runs.sort(key=lambda r: r["ts_iso"])
    if len(runs) > max_runs:
        runs = runs[-max_runs:]
    return runs


def rollup_coffee_24h(
    *,
    user_id: str,
    now_utc: datetime | None = None,
    events_path: Path = DEFAULT_EVENTS_PATH,
    window_hours: float = 24.0,
    max_runs: int = 20,
) -> dict[str, Any]:
    """Aggregate coffee cadence in (now - window_hours, now] UTC."""
    if now_utc is None:
        now_utc = datetime.now(timezone.utc)
    if now_utc.tzinfo is None:
        now_utc = now_utc.replace(tzinfo=timezone.utc)
    window_end = now_utc
    window_start = now_utc - timedelta(hours=window_hours)

    if not events_path.is_file():
        return {
            "window_start_utc": window_start.isoformat(),
            "window_end_utc": window_end.isoformat(),
            "window_hours": window_hours,
            "count": 0,
            "first_ts": None,
            "last_ts": None,
            "span_hours": None,
            "by_mode": {},
            "runs": [],
            "picks": [],
            "by_picked": {},
            "note": "no cadence file",
        }

    text = events_path.read_text(encoding="utf-8")
    runs = parse_coffee_cadence_lines(
        text,
        user_id=user_id,
        window_start=window_start,
        window_end=window_end,
        max_runs=max_runs,
    )
    picks = parse_coffee_pick_cadence_lines(
        text,
        user_id=user_id,
        window_start=window_start,
        window_end=window_end,
    )

    by_mode: dict[str, int] = {}
    for r in runs:
        m = r["mode"]
        by_mode[m] = by_mode.get(m, 0) + 1

    by_picked: dict[str, int] = {}
    for r in picks:
        letter = r["picked"]
        by_picked[letter] = by_picked.get(letter, 0) + 1

    first_ts = runs[0]["ts_iso"] if runs else None
    last_ts = runs[-1]["ts_iso"] if runs else None
    span_hours: float | None = None
    if len(runs) >= 2:
        t0 = datetime.fromisoformat(runs[0]["ts_iso"].replace("Z", "+00:00"))
        t1 = datetime.fromisoformat(runs[-1]["ts_iso"].replace("Z", "+00:00"))
        span_hours = round((t1 - t0).total_seconds() / 3600.0, 2)

    return {
        "window_start_utc": window_start.isoformat(),
        "window_end_utc": window_end.isoformat(),
        "window_hours": window_hours,
        "count": len(runs),
        "first_ts": first_ts,
        "last_ts": last_ts,
        "span_hours": span_hours,
        "by_mode": by_mode,
        "runs": runs,
        "picks": picks,
        "by_picked": by_picked,
    }


def _one_line_capped(s: str, max_len: int) -> str:
    t = " ".join(s.split())
    if len(t) <= max_len:
        return t
    return t[: max_len - 1] + "…"


def _is_refusal_outcome(row: dict[str, Any]) -> bool:
    verdict = str(row.get("verdict") or "").lower()
    action = str(row.get("action") or "").lower()
    refusal_tokens = {"no_action", "refuse", "refused", "park", "parked", "shelf"}
    return verdict in refusal_tokens or action in refusal_tokens


def _conductor_outcome_label(row: dict[str, Any]) -> str:
    for key in ("action", "falsify", "commit", "notebook_ref", "verdict"):
        value = str(row.get(key) or "").strip()
        if value:
            return value
    return "closed pass"


def rollup_conductor_24h(
    *,
    user_id: str,
    now_utc: datetime | None = None,
    events_path: Path = DEFAULT_EVENTS_PATH,
    window_hours: float = 24.0,
    max_events: int = 60,
) -> dict[str, Any]:
    """Compatibility shim: dream handoff reads work-pass rollup (Phase 3)."""
    rollup = rollup_work_pass_24h(
        user_id=user_id,
        now_utc=now_utc,
        events_path=events_path,
        window_hours=window_hours,
        max_events=max_events,
    )
    keep = {
        "window_start_utc",
        "window_end_utc",
        "window_hours",
        "pick_count",
        "outcome_count",
        "completed_passes",
        "orientation_only",
        "off_menu_refusals",
        "last_master",
        "last_outcome",
        "echo",
        "note",
    }
    return {key: value for key, value in rollup.items() if key in keep}


def rollup_work_pass_24h(
    *,
    user_id: str,
    now_utc: datetime | None = None,
    events_path: Path = DEFAULT_EVENTS_PATH,
    window_hours: float = 24.0,
    max_events: int = 60,
) -> dict[str, Any]:
    """Aggregate extended coffee_close rows for dream / bootstrap handoff (Phase 3 SSOT)."""
    if now_utc is None:
        now_utc = datetime.now(timezone.utc)
    if now_utc.tzinfo is None:
        now_utc = now_utc.replace(tzinfo=timezone.utc)
    window_end = now_utc
    window_start = now_utc - timedelta(hours=window_hours)

    result: dict[str, Any] = {
        "window_start_utc": window_start.isoformat(),
        "window_end_utc": window_end.isoformat(),
        "window_hours": window_hours,
        "close_count": 0,
        "substantive_count": 0,
        "object_ref_count": 0,
        "falsify_count": 0,
        "completed_passes": 0,
        "orientation_only": 0,
        "off_menu_refusals": 0,
        "pick_count": 0,
        "outcome_count": 0,
        "last_object_ref": None,
        "last_falsify": None,
        "last_verdict": None,
        "last_attention": None,
        "last_picked": None,
        "last_outcome": None,
        "last_master": None,
        "echo": None,
        "source": "none",
        "note": None,
    }
    if not events_path.is_file():
        result["note"] = "no cadence file"
        return result

    try:
        from audit_cadence_rhythm import parse_events
    except ImportError:
        from scripts.audit_cadence_rhythm import parse_events  # type: ignore

    events = parse_events(user_id, events_path=events_path)
    in_window = [e for e in events if window_start <= e["dt"] <= window_end]
    closes = [e for e in in_window if e.get("kind") == "coffee_close"]
    hub_picks = [
        e
        for e in in_window
        if e.get("kind") == "coffee_pick"
        and str((e.get("kv") or {}).get("picked", "")).strip() in {"A", "B", "C", "D"}
    ]

    if not closes and not hub_picks:
        legacy = rollup_conductor_window(
            user_id=user_id,
            now_utc=now_utc,
            events_path=events_path,
            window_hours=window_hours,
            max_events=max_events,
        )
        if int(legacy.get("pick_count") or 0) or int(legacy.get("outcome_count") or 0):
            result.update(
                {
                    "pick_count": legacy.get("pick_count", 0),
                    "outcome_count": legacy.get("outcome_count", 0),
                    "completed_passes": legacy.get("completed_passes", 0),
                    "orientation_only": legacy.get("orientation_only", 0),
                    "off_menu_refusals": legacy.get("off_menu_refusals", 0),
                    "last_master": legacy.get("last_master"),
                    "last_outcome": legacy.get("last_outcome"),
                    "echo": legacy.get("echo"),
                    "source": "legacy_conductor",
                    "note": "legacy conductor cadence only (read-only)",
                }
            )
        else:
            result["note"] = "no work-pass or legacy conductor activity in window"
        return result

    def _substantive(kv: dict[str, str]) -> bool:
        return bool(
            str(kv.get("object_ref") or "").strip()
            or str(kv.get("falsify") or "").strip()
            or str(kv.get("verdict") or "").strip()
        )

    object_ref_count = 0
    falsify_count = 0
    substantive_count = 0
    completed_passes = 0
    off_menu_refusals = 0
    last_with_anchor: dict[str, Any] | None = None

    for event in closes:
        kv = event.get("kv") or {}
        if kv.get("object_ref"):
            object_ref_count += 1
        if kv.get("falsify"):
            falsify_count += 1
        if _substantive(kv):
            substantive_count += 1
        outcome = str(kv.get("outcome") or "").strip().lower()
        if outcome in {"blocked", "parked"}:
            off_menu_refusals += 1
        elif outcome in {"done", "partial"}:
            completed_passes += 1
        if kv.get("object_ref") or kv.get("falsify"):
            last_with_anchor = event

    last = last_with_anchor or (closes[-1] if closes else None)
    last_kv = (last.get("kv") or {}) if last else {}
    obj = str(last_kv.get("object_ref") or "").strip()
    fals = str(last_kv.get("falsify") or "").strip()
    echo_parts: list[str] = []
    if obj:
        echo_parts.append(f"object={obj}")
    if fals:
        echo_parts.append(f"falsify={fals}")
    picked = str(last_kv.get("picked") or "").strip() or None
    attention = str(last_kv.get("attention") or "").strip() or None
    if picked and not echo_parts:
        echo_parts.append(f"hub={picked}")
    echo = _one_line_capped("; ".join(echo_parts), 180) if echo_parts else None

    pick_count = len(hub_picks) or len(closes)
    orientation_only = max(0, pick_count - len(closes))

    last_outcome = None
    if last:
        last_outcome = {
            "picked": picked,
            "outcome": last_kv.get("outcome"),
            "readiness": last_kv.get("readiness"),
            "object_ref": obj or None,
            "falsify": fals or None,
            "verdict": last_kv.get("verdict"),
            "attention": attention,
        }

    result.update(
        {
            "close_count": len(closes),
            "substantive_count": substantive_count,
            "object_ref_count": object_ref_count,
            "falsify_count": falsify_count,
            "completed_passes": completed_passes,
            "off_menu_refusals": off_menu_refusals,
            "orientation_only": orientation_only,
            "pick_count": pick_count,
            "outcome_count": len(closes),
            "last_object_ref": obj or None,
            "last_falsify": fals or None,
            "last_verdict": last_kv.get("verdict") or None,
            "last_attention": attention,
            "last_picked": picked,
            "last_outcome": last_outcome,
            "last_master": attention or picked,
            "echo": echo,
            "source": "coffee_close",
            "note": None,
        }
    )
    return result


def rollup_object_closes_24h(
    *,
    user_id: str,
    now_utc: datetime | None = None,
    events_path: Path = DEFAULT_EVENTS_PATH,
    window_hours: float = 24.0,
) -> dict[str, Any]:
    """Scan recent coffee_close events for object_ref + falsify bootstrap echo."""
    rollup = rollup_work_pass_24h(
        user_id=user_id,
        now_utc=now_utc,
        events_path=events_path,
        window_hours=window_hours,
    )
    keep = {
        "window_start_utc",
        "window_end_utc",
        "window_hours",
        "close_count",
        "object_ref_count",
        "falsify_count",
        "last_object_ref",
        "last_falsify",
        "last_verdict",
        "last_attention",
        "last_picked",
        "echo",
        "note",
    }
    return {key: rollup.get(key) for key in keep}


def rollup_conductor_window(
    *,
    user_id: str,
    now_utc: datetime | None = None,
    events_path: Path = DEFAULT_EVENTS_PATH,
    window_hours: float = 24.0,
    max_events: int = 60,
) -> dict[str, Any]:
    """Aggregate conductor telemetry over an arbitrary UTC look-back window.

    This keeps the 24h dream handoff intact while also supporting longer
    review windows for conductor ledgers and monthly audits.
    """
    if now_utc is None:
        now_utc = datetime.now(timezone.utc)
    if now_utc.tzinfo is None:
        now_utc = now_utc.replace(tzinfo=timezone.utc)
    window_end = now_utc
    window_start = now_utc - timedelta(hours=window_hours)
    empty: dict[str, Any] = {
        "window_start_utc": window_start.isoformat(),
        "window_end_utc": window_end.isoformat(),
        "window_hours": window_hours,
        "pick_count": 0,
        "outcome_count": 0,
        "completed_passes": 0,
        "orientation_only": 0,
        "off_menu_refusals": 0,
        "notebook_ref_count": 0,
        "falsify_count": 0,
        "last_master": None,
        "last_outcome": None,
        "by_conductor": {},
        "open_arcs": [],
        "recent_closed": [],
        "commits": [],
        "falsifiers": [],
        "events": [],
        "echo": None,
    }
    if not events_path.is_file():
        empty["note"] = "no cadence file"
        return empty

    text = events_path.read_text(encoding="utf-8")
    events = parse_conductor_cadence_lines(
        text,
        user_id=user_id,
        window_start=window_start,
        window_end=window_end,
        max_events=max_events,
    )
    picks = [e for e in events if e.get("kind") == "pick"]
    outcomes = [e for e in events if e.get("kind") == "outcome"]
    refusal_count = sum(1 for e in outcomes if _is_refusal_outcome(e))
    completed = max(0, len(outcomes) - refusal_count)
    notebook_ref_count = sum(1 for e in outcomes if e.get("notebook_ref"))
    falsify_count = sum(1 for e in outcomes if e.get("falsify"))
    by_conductor: dict[str, dict[str, int]] = {}
    open_arcs: list[dict[str, Any]] = []
    recent_closed: list[dict[str, Any]] = []
    for event in events:
        conductor = str(event.get("conductor") or "unknown")
        bucket = by_conductor.setdefault(conductor, {"picks": 0, "outcomes": 0, "refusals": 0})
        if event.get("kind") == "pick":
            bucket["picks"] += 1
            open_arcs.append(
                {
                    "conductor": conductor,
                    "ts_iso": event.get("ts_iso"),
                    "menu_label": event.get("menu_label"),
                }
            )
        else:
            bucket["outcomes"] += 1
            if _is_refusal_outcome(event):
                bucket["refusals"] += 1
            recent_closed.append(
                {
                    "conductor": conductor,
                    "ts_iso": event.get("ts_iso"),
                    "verdict": event.get("verdict"),
                    "notebook_ref": event.get("notebook_ref"),
                    "falsify": event.get("falsify"),
                    "action": event.get("action"),
                }
            )
            if open_arcs:
                for idx in range(len(open_arcs) - 1, -1, -1):
                    if open_arcs[idx]["conductor"] == conductor:
                        open_arcs.pop(idx)
                        break

    commits = [str(e["commit"]) for e in outcomes if e.get("commit")]
    falsifiers = [str(e["falsify"]) for e in outcomes if e.get("falsify")]
    last_event_with_master = next((e for e in reversed(events) if e.get("conductor")), None)
    last_outcome = outcomes[-1] if outcomes else None
    orientation_only = max(0, len(picks) - len(outcomes))
    echo = None
    if events:
        pieces: list[str] = []
        if last_event_with_master and last_event_with_master.get("conductor"):
            pieces.append(f"{last_event_with_master['conductor']} carried the latest conductor line")
        if last_outcome:
            pieces.append(f"last close: {_conductor_outcome_label(last_outcome)}")
        if completed:
            pieces.append(f"{completed} closed pass(es)")
        if refusal_count:
            pieces.append(f"{refusal_count} parked/refused")
        echo = _one_line_capped("; ".join(pieces), 180)

    empty.update(
        {
            "pick_count": len(picks),
            "outcome_count": len(outcomes),
            "completed_passes": completed,
            "orientation_only": orientation_only,
            "off_menu_refusals": refusal_count,
            "notebook_ref_count": notebook_ref_count,
            "falsify_count": falsify_count,
            "last_master": (
                str(last_event_with_master.get("conductor"))
                if last_event_with_master and last_event_with_master.get("conductor")
                else None
            ),
            "last_outcome": last_outcome,
            "by_conductor": by_conductor,
            "open_arcs": open_arcs[-8:],
            "recent_closed": recent_closed[-8:],
            "commits": commits[-8:],
            "falsifiers": falsifiers[-8:],
            "events": events,
            "echo": echo,
        }
    )
    return empty


def build_last_coffee_echo(rollup: dict[str, Any]) -> dict[str, Any] | None:
    """Derive a compact, single-line echo from a 24h coffee rollup; no cadence re-parse.

    Returns None if there is no recent coffee *run* in the window (not Record).
    """
    runs = rollup.get("runs") or []
    if not runs or int(rollup.get("count") or 0) <= 0:
        return None
    last = runs[-1]
    ts = (last.get("ts_iso") or rollup.get("last_ts") or "") or None
    if not ts:
        return None
    mode = str(last.get("mode") or "unknown")
    picks = rollup.get("picks") or []
    last_pick = picks[-1] if picks else None
    conductor: str | None = None
    menu_letter: str | None = None
    if last_pick and isinstance(last_pick, dict):
        c = (last_pick.get("conductor") or "").strip()
        if c:
            conductor = c
        ml = (last_pick.get("menu_label") or last_pick.get("picked") or "").strip()
        if ml:
            menu_letter = ml
    # Warm, bounded one-liner (no raw event text)
    bits: list[str] = [f"Yesterday’s {mode} coffee is still the thread."]
    if menu_letter:
        bits.append(f"Menu pick: {menu_letter}.")
    if conductor:
        bits.append(f"Conductor line: {conductor}.")
    highlight = _one_line_capped(" ".join(bits), 160)
    return {
        "timestamp": ts,
        "conductor": conductor,
        "mode": mode,
        "menu_letter": menu_letter,
        "highlight": highlight,
        "source": "coffee_rollup_24h",
    }
