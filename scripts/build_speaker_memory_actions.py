#!/usr/bin/env python3
"""Build advisory speaker-memory actions from routed appearances.

WORK-layer advisory automation only. This script aggregates speaker-routing
rows into concrete operator-reviewable actions. It never edits raw-input,
speaker folders, arcs, helixes, lattice rows, or Record surfaces.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
from repo_io import ARTIFACTS_DIR

import build_voice_routing_queue as routing  # noqa: E402

DEFAULT_NOTEBOOK_ROOT = REPO_ROOT / "codex" / "years" / str(date.today().year)
DEFAULT_OUT_DIR = ARTIFACTS_DIR / "speaker-memory-actions"
ACTION_TYPES = {
    "update-existing-arc",
    "review-existing-object",
    "create-candidate-arc",
    "create-candidate-object",
    "consider-helix",
    "no-action",
}

@dataclass(frozen=True)
class ActionDraft:
    action_type: str
    priority: str
    target_path: str
    speaker_slug: str
    host_slug: str
    evidence_appearances: list[str]
    evidence_grades: list[str]
    reason: str
    operator_instruction: str

def _parse_date(value: str) -> date:
    return date.fromisoformat(value)

def _window_slug(start: date, end: date) -> str:
    return f"{start.isoformat()}_to_{end.isoformat()}"

def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line:
            rows.append(routing.normalize_route_row(json.loads(line)))
    return rows

def _action_id(action: ActionDraft) -> str:
    identity = "|".join(
        [
            action.action_type,
            action.target_path,
            action.speaker_slug,
            action.host_slug,
            ",".join(sorted(action.evidence_appearances)),
        ]
    )
    return f"act-{hashlib.sha1(identity.encode('utf-8')).hexdigest()[:12]}"

def _has_comparative_note(row: dict[str, Any]) -> bool:
    for path in row.get("also_strengthens") or []:
        stem = Path(str(path)).stem
        if stem.endswith("-cross-host-note") or "helix" in stem:
            return True
    return False

def _speaker_helix_target(speaker_slug: str, speaker_rows: list[dict[str, Any]]) -> str:
    year = str(date.today().year)
    for row in speaker_rows:
        raw_input_path = _normalize_appearance(row).get("raw_input_path", "")
        match = re.search(r"(?:^|/)continuity/years/(\d{4})/", raw_input_path)
        if match:
            year = match.group(1)
            break
    return f"statecraft/voices/{speaker_slug}/{speaker_slug}-helix.md"

def _candidate_arc_target(row: dict[str, Any]) -> str:
    for path in row.get("also_strengthens") or []:
        if str(path).endswith("-speaker-arc.md"):
            return str(path)
    return str(row.get("recommended_route") or row.get("primary_route") or "")

def _normalize_appearance(row: dict[str, Any]) -> dict[str, str]:
    appearance = dict(row.get("appearance") or {})
    appearance.setdefault("appearance_id", "")
    appearance.setdefault("speaker_slug", str(row.get("guest") or ""))
    appearance.setdefault("host_slug", str(row.get("host") or ""))
    appearance.setdefault("pub_date", str(row.get("pub_date") or ""))
    appearance.setdefault("source_url", str(row.get("source_url") or ""))
    appearance.setdefault("raw_input_path", str(row.get("raw_input_path") or ""))
    return {key: str(value or "") for key, value in appearance.items()}

def _draft_from_row(row: dict[str, Any], *, include_no_action: bool) -> ActionDraft | None:
    appearance = _normalize_appearance(row)
    appearance_id = appearance["appearance_id"]
    evidence_grade = str(row.get("evidence_grade") or "")
    route_type = str(row.get("route_type") or "")
    next_action = str(row.get("next_action") or "")
    speaker_slug = appearance.get("speaker_slug", "")
    host_slug = appearance.get("host_slug", "")
    primary = str(row.get("primary_route") or row.get("recommended_route") or "")

    if route_type == "existing-voice-arc":
        return ActionDraft(
            action_type="update-existing-arc",
            priority="high",
            target_path=primary,
            speaker_slug=speaker_slug,
            host_slug=host_slug,
            evidence_appearances=[appearance_id],
            evidence_grades=[evidence_grade],
            reason="Appearance routes to an existing host-local speaker arc.",
            operator_instruction="Review the raw-input and update the existing speaker arc if it changes the ranked arc set, open-first choice, or boundary.",
        )

    if route_type == "existing-voice-object" and next_action == "create-candidate-arc":
        return ActionDraft(
            action_type="create-candidate-arc",
            priority="medium",
            target_path=_candidate_arc_target(row),
            speaker_slug=speaker_slug,
            host_slug=host_slug,
            evidence_appearances=[appearance_id],
            evidence_grades=[evidence_grade],
            reason="Appearance matched an existing speaker object but no host-local arc exists yet.",
            operator_instruction="Decide whether this host x speaker pairing deserves a new speaker-arc note before editing the speaker object.",
        )

    if route_type == "existing-voice-object":
        return ActionDraft(
            action_type="review-existing-object",
            priority="medium",
            target_path=primary,
            speaker_slug=speaker_slug,
            host_slug=host_slug,
            evidence_appearances=[appearance_id],
            evidence_grades=[evidence_grade],
            reason="Appearance routes to an existing speaker object without a clearer arc target.",
            operator_instruction="Review whether the speaker object open-first, routing use, or boundaries need a small update.",
        )

    if route_type == "candidate-voice-object":
        return ActionDraft(
            action_type="create-candidate-object",
            priority="medium",
            target_path=primary,
            speaker_slug=speaker_slug,
            host_slug=host_slug,
            evidence_appearances=[appearance_id],
            evidence_grades=[evidence_grade],
            reason="Appearance matched a speaker folder without an existing speaker object.",
            operator_instruction="Create a speaker-object note only if this recurring figure deserves durable orientation.",
        )

    if route_type == "candidate-voice-arc":
        return ActionDraft(
            action_type="create-candidate-arc",
            priority="medium",
            target_path=primary,
            speaker_slug=speaker_slug,
            host_slug=host_slug,
            evidence_appearances=[appearance_id],
            evidence_grades=[evidence_grade],
            reason="Appearance has guest metadata but no existing object or host-local arc matched.",
            operator_instruction="Create a speaker arc only if the host x guest pairing is recurring or strategically distinctive.",
        )

    if include_no_action:
        return ActionDraft(
            action_type="no-action",
            priority="low",
            target_path="",
            speaker_slug=speaker_slug,
            host_slug=host_slug,
            evidence_appearances=[appearance_id],
            evidence_grades=[evidence_grade],
            reason="No clear speaker-memory route was found.",
            operator_instruction="Stop at raw-input unless the operator supplies stronger speaker metadata.",
        )
    return None

def _merge_actions(actions: list[ActionDraft]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str, str, str], ActionDraft] = {}
    for action in actions:
        key = (action.action_type, action.target_path, action.speaker_slug, action.host_slug)
        existing = grouped.get(key)
        if not existing:
            grouped[key] = action
            continue
        evidence = sorted(set(existing.evidence_appearances + action.evidence_appearances))
        grouped[key] = ActionDraft(
            action_type=existing.action_type,
            priority=existing.priority,
            target_path=existing.target_path,
            speaker_slug=existing.speaker_slug,
            host_slug=existing.host_slug,
            evidence_appearances=evidence,
            evidence_grades=sorted(set(existing.evidence_grades + action.evidence_grades)),
            reason=existing.reason,
            operator_instruction=existing.operator_instruction,
        )

    rows: list[dict[str, Any]] = []
    for action in grouped.values():
        rows.append(
            {
                "action_id": _action_id(action),
                "action_type": action.action_type,
                "priority": action.priority,
                "target_path": action.target_path,
                "speaker_slug": action.speaker_slug,
                "host_slug": action.host_slug,
                "evidence_appearances": sorted(set(action.evidence_appearances)),
                "evidence_grades": sorted(set(action.evidence_grades)),
                "reason": action.reason,
                "operator_instruction": action.operator_instruction,
            }
        )
    return sorted(rows, key=lambda row: (row["priority"] != "high", row["action_type"], row["target_path"]))

def build_rollup(rows: list[dict[str, Any]]) -> dict[str, Any]:
    speakers: dict[str, dict[str, Any]] = {}
    for row in rows:
        appearance = _normalize_appearance(row)
        speaker = appearance.get("speaker_slug") or "_unknown"
        host = appearance.get("host_slug") or "_unknown"
        entry = speakers.setdefault(
            speaker,
            {"appearance_count": 0, "hosts": {}, "route_types": {}, "appearance_ids": []},
        )
        entry["appearance_count"] += 1
        entry["hosts"][host] = entry["hosts"].get(host, 0) + 1
        route_type = str(row.get("route_type") or "")
        entry["route_types"][route_type] = entry["route_types"].get(route_type, 0) + 1
        entry["appearance_ids"].append(appearance["appearance_id"])
    return {
        "appearance_count": len(rows),
        "speaker_count": len(speakers),
        "speakers": speakers,
    }

def build_actions(rows: list[dict[str, Any]], *, include_no_action: bool = False) -> list[dict[str, Any]]:
    drafts = [
        draft
        for row in rows
        if (draft := _draft_from_row(row, include_no_action=include_no_action)) is not None
    ]

    rows_by_speaker: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        appearance = _normalize_appearance(row)
        speaker_slug = appearance.get("speaker_slug", "")
        if speaker_slug:
            rows_by_speaker[speaker_slug].append(row)

    for speaker_slug, speaker_rows in rows_by_speaker.items():
        hosts = sorted(
            {
                _normalize_appearance(row).get("host_slug", "")
                for row in speaker_rows
                if _normalize_appearance(row).get("host_slug", "")
            }
        )
        if len(hosts) < 2 or any(_has_comparative_note(row) for row in speaker_rows):
            continue
        evidence = [_normalize_appearance(row)["appearance_id"] for row in speaker_rows]
        drafts.append(
            ActionDraft(
                action_type="consider-helix",
                priority="medium",
                target_path=_speaker_helix_target(speaker_slug, speaker_rows),
                speaker_slug=speaker_slug,
                host_slug=",".join(hosts),
                evidence_appearances=evidence,
                evidence_grades=sorted(set(str(row.get("evidence_grade") or "") for row in speaker_rows if str(row.get("evidence_grade") or ""))),
                reason="Speaker appears across multiple host slugs in this window without an existing comparative note in the route stack.",
                operator_instruction="Review whether the cross-host pattern is strong enough for a helix or cross-host note.",
            )
        )

    return _merge_actions(drafts)

def _render_rollup_md(rollup: dict[str, Any], start: date, end: date) -> str:
    lines = [
        "# Appearance rollup",
        "",
                "",
        f"Window: `{start.isoformat()}` to `{end.isoformat()}`",
        "",
        f"- appearances: `{rollup['appearance_count']}`",
        f"- speakers: `{rollup['speaker_count']}`",
        "",
    ]
    for speaker, data in sorted(rollup["speakers"].items()):
        hosts = ", ".join(f"{host}:{count}" for host, count in sorted(data["hosts"].items()))
        lines.append(f"- `{speaker}` appearances `{data['appearance_count']}` hosts `{hosts}`")
    return "\n".join(lines).rstrip() + "\n"

def _render_actions_md(actions: list[dict[str, Any]], start: date, end: date) -> str:
    lines = [
        "# Speaker memory action queue",
        "",
                "",
        f"Window: `{start.isoformat()}` to `{end.isoformat()}`",
        "",
    ]
    if not actions:
        lines.extend(["_No speaker-memory actions._", ""])
        return "\n".join(lines)
    for action in actions:
        target = action["target_path"] or "_none_"
        lines.append(
            f"- `{action['priority']}` `{action['action_type']}` `{target}` "
            f"({len(action['evidence_appearances'])} appearance(s); grades: {', '.join(action.get('evidence_grades') or ['_none_'])})"
        )
        lines.append(f"  - reason: {action['reason']}")
        lines.append(f"  - operator: {action['operator_instruction']}")
    return "\n".join(lines).rstrip() + "\n"

def write_outputs(
    *,
    rows: list[dict[str, Any]],
    actions: list[dict[str, Any]],
    output_dir: Path,
    start: date,
    end: date,
) -> dict[str, str]:
    window_dir = output_dir / _window_slug(start, end)
    window_dir.mkdir(parents=True, exist_ok=True)
    rollup = build_rollup(rows)

    rollup_json = window_dir / "appearance-rollup.json"
    rollup_json.write_text(json.dumps(rollup, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    rollup_md = window_dir / "appearance-rollup.md"
    rollup_md.write_text(_render_rollup_md(rollup, start, end), encoding="utf-8")

    action_jsonl = window_dir / "memory-action-queue.jsonl"
    with action_jsonl.open("w", encoding="utf-8", newline="") as fh:
        for action in actions:
            fh.write(json.dumps(action, ensure_ascii=True, sort_keys=True) + "\n")

    action_md = window_dir / "memory-action-queue.md"
    action_md.write_text(_render_actions_md(actions, start, end), encoding="utf-8")

    return {
        "appearance_rollup_json": str(rollup_json),
        "appearance_rollup_markdown": str(rollup_md),
        "memory_action_queue_jsonl": str(action_jsonl),
        "memory_action_queue_markdown": str(action_md),
    }

def build_routing_rows(start: date, end: date, notebook_root: Path) -> list[dict[str, Any]]:
    notebook_root = notebook_root.resolve()
    voices_dir = routing.DEFAULT_VOICES_DIR
    inventory = routing._discover_inventory(voices_dir, notebook_root)
    raw_root = notebook_root / "raw-input"
    return routing.build_rows(routing._discover_raw_inputs(raw_root, start, end), inventory, notebook_root)

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start", required=True, type=_parse_date, help="Start date, YYYY-MM-DD.")
    parser.add_argument("--end", required=True, type=_parse_date, help="End date, YYYY-MM-DD.")
    parser.add_argument("--notebook-root", type=Path, default=DEFAULT_NOTEBOOK_ROOT)
    parser.add_argument("--routing-jsonl", type=Path, default=None)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--include-no-action", action="store_true")
    return parser.parse_args(argv)

def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.end < args.start:
        print("--end must be on or after --start", file=sys.stderr)
        return 2
    rows = _load_jsonl(args.routing_jsonl) if args.routing_jsonl else build_routing_rows(
        args.start, args.end, args.notebook_root
    )
    actions = build_actions(rows, include_no_action=args.include_no_action)
    written = write_outputs(rows=rows, actions=actions, output_dir=args.output_dir, start=args.start, end=args.end)
    print(json.dumps({"rows": len(rows), "actions": len(actions), "written": written}, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
