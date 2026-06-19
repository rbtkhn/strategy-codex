#!/usr/bin/env python3
"""
Operator Dashboard — umbrella orchestrator for strategy-codex aggregators.

Runs Repo Surgeon, Statecraft War Room, and Operator Command Deck in-process,
then writes a stitched index at runtime/artifacts/operator-dashboard/latest.*.

See runtime/artifacts/operator-dashboard/README.md and
docs/skill-work/work-dev/operator-dashboard-consolidation-phase0.md.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from operator_command_deck import generate_report as generate_deck_report  # noqa: E402
from operator_report_utils import authority_header, markdown_table, utc_now_iso, write_report  # noqa: E402
from repo_surgeon import generate_report as generate_surgeon_report  # noqa: E402
from statecraft_war_room import generate_report as generate_war_room_report  # noqa: E402

DEFAULT_OUT = Path("runtime/artifacts/operator-dashboard/latest.md")
DEFAULT_JSON = Path("runtime/artifacts/operator-dashboard/latest.json")

SURGEON_JSON = Path("runtime/artifacts/repo-surgeon/latest.json")
SURGEON_MD = Path("runtime/artifacts/repo-surgeon/latest.md")
WAR_ROOM_JSON = Path("runtime/artifacts/statecraft-war-room/latest.json")
WAR_ROOM_MD = Path("runtime/artifacts/statecraft-war-room/latest.md")
DECK_JSON = Path("runtime/artifacts/operator-command-deck/latest.json")
DECK_MD = Path("runtime/artifacts/operator-command-deck/latest.md")

RETURN_PATHS = [
    "runtime/artifacts/repo-surgeon/README.md",
    "runtime/artifacts/statecraft-war-room/README.md",
    "runtime/artifacts/operator-command-deck/README.md",
    "docs/operator-dashboard-when-to-use.md",
    "docs/skill-work/work-dev/operator-dashboard-consolidation-phase0.md",
]

CHILD_DASHBOARDS: tuple[tuple[str, str, Path], ...] = (
    ("Repo Surgeon", "What is structurally broken or drifting?", SURGEON_MD),
    (
        "Statecraft War Room",
        "Which statecraft objects are live?",
        WAR_ROOM_MD,
    ),
    (
        "Operator Command Deck",
        "What should I do next?",
        DECK_MD,
    ),
)


@dataclass
class DashboardRunConfig:
    out: Path = DEFAULT_OUT
    json_out: Path = DEFAULT_JSON
    snapshot: bool = False
    compose_only: bool = False
    surgeon_scope: str = "docs"
    full_surgeon: bool = False
    verify_portable_skills: bool = False
    fail_on_blocking: bool = False
    war_room_latest_days: int = 7
    war_room_max_objects: int = 12
    max_next_actions: int = 5
    include_gate: bool = False
    no_git: bool = False
    surgeon_out: Path = field(default_factory=lambda: SURGEON_MD)
    surgeon_json_out: Path = field(default_factory=lambda: SURGEON_JSON)
    war_room_out: Path = field(default_factory=lambda: WAR_ROOM_MD)
    war_room_json_out: Path = field(default_factory=lambda: WAR_ROOM_JSON)
    deck_out: Path = field(default_factory=lambda: DECK_MD)
    deck_json_out: Path = field(default_factory=lambda: DECK_JSON)


@dataclass
class UmbrellaResult:
    exit_code: int
    surgeon_payload: dict[str, Any]
    war_room_payload: dict[str, Any]
    deck_payload: dict[str, Any]
    umbrella_payload: dict[str, Any]


def _resolve(repo_root: Path, path: Path) -> Path:
    return path if path.is_absolute() else (repo_root / path).resolve()


def _rel_posix(repo_root: Path, path: Path) -> str:
    resolved = _resolve(repo_root, path)
    try:
        return resolved.relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return resolved.as_posix()


def _load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(f"missing child dashboard JSON: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"invalid JSON object in {path}")
    return data


def _worst_exit(*codes: int) -> int:
    return max(codes) if codes else 0


def run_child_producers(
    repo_root: Path,
    config: DashboardRunConfig,
) -> tuple[int, dict[str, Any], dict[str, Any], dict[str, Any]]:
    surgeon_code, surgeon_payload = generate_surgeon_report(
        repo_root,
        out=config.surgeon_out,
        json_out=config.surgeon_json_out,
        run_checks=config.full_surgeon,
        scope=config.surgeon_scope,
        verify_portable=config.verify_portable_skills,
        fail_on_blocking=config.fail_on_blocking,
    )
    war_room_code, war_room_payload = generate_war_room_report(
        repo_root,
        out=config.war_room_out,
        json_out=config.war_room_json_out,
        latest_days=config.war_room_latest_days,
        max_objects=config.war_room_max_objects,
    )
    deck_code, deck_payload = generate_deck_report(
        repo_root,
        out=config.deck_out,
        json_out=config.deck_json_out,
        max_next_actions=config.max_next_actions,
        full_surgeon=config.full_surgeon,
        surgeon_scope=config.surgeon_scope,
        verify_portable=config.verify_portable_skills,
        war_room_latest_days=config.war_room_latest_days,
        war_room_max_objects=config.war_room_max_objects,
        include_git=not config.no_git,
        include_gate=config.include_gate,
    )
    exit_code = _worst_exit(surgeon_code, war_room_code, deck_code)
    return exit_code, surgeon_payload, war_room_payload, deck_payload


def load_child_payloads(
    repo_root: Path,
    config: DashboardRunConfig,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    surgeon_path = _resolve(repo_root, config.surgeon_json_out)
    war_room_path = _resolve(repo_root, config.war_room_json_out)
    deck_path = _resolve(repo_root, config.deck_json_out)
    return (
        _load_json(surgeon_path),
        _load_json(war_room_path),
        _load_json(deck_path),
    )


def build_umbrella_json(
    surgeon: dict[str, Any],
    war_room: dict[str, Any],
    deck: dict[str, Any],
    *,
    generated_at: str,
    repo_root: Path,
    config: DashboardRunConfig,
) -> dict[str, Any]:
    posture = deck.get("posture") or {}
    surgeon_summary = deck.get("surgeon_summary") or {}
    war_room_summary = deck.get("war_room_summary") or {}
    return {
        "generated_at": generated_at,
        "authority": "runtime_derived",
        "posture": {
            "surgeon": {
                "status": surgeon.get("status") or surgeon_summary.get("status"),
                "blocking_count": surgeon.get("blocking_count")
                or surgeon_summary.get("blocking_count"),
                "warning_count": surgeon.get("warning_count")
                or surgeon_summary.get("warning_count"),
            },
            "war_room": {
                "sync_status": war_room.get("sync_status") or war_room_summary.get("sync_status"),
                "active_object_count": len(war_room.get("active_objects") or [])
                or war_room_summary.get("active_object_count"),
                "latest_archive_day": war_room.get("latest_archive_day")
                or war_room_summary.get("latest_archive_day"),
            },
            "deck": {
                "git_clean": posture.get("git_clean"),
                "budget_stale": posture.get("budget_stale"),
                "surgeon_status": posture.get("surgeon_status"),
                "war_room_sync_status": posture.get("war_room_sync_status"),
            },
        },
        "next_actions": deck.get("next_actions") or [],
        "child_paths": {
            "surgeon_md": _rel_posix(repo_root, config.surgeon_out),
            "surgeon_json": _rel_posix(repo_root, config.surgeon_json_out),
            "war_room_md": _rel_posix(repo_root, config.war_room_out),
            "war_room_json": _rel_posix(repo_root, config.war_room_json_out),
            "deck_md": _rel_posix(repo_root, config.deck_out),
            "deck_json": _rel_posix(repo_root, config.deck_json_out),
        },
    }


def build_umbrella_markdown(
    surgeon: dict[str, Any],
    war_room: dict[str, Any],
    deck: dict[str, Any],
    *,
    generated_at: str,
    repo_root: Path,
    config: DashboardRunConfig,
) -> str:
    umbrella_json = build_umbrella_json(
        surgeon,
        war_room,
        deck,
        generated_at=generated_at,
        repo_root=repo_root,
        config=config,
    )
    posture = umbrella_json["posture"]
    surgeon_row = posture["surgeon"]
    war_room_row = posture["war_room"]
    deck_row = posture["deck"]

    parts: list[str] = [
        authority_header(generated_at, RETURN_PATHS),
        "# Operator Dashboard (umbrella index)",
        "",
        "Stitched index over the three Phase 1–3 aggregators. Open child `latest.md` files for detail.",
        "",
        "## 1. Posture at a Glance",
        "",
        markdown_table(
            [
                {
                    "Surface": "Repo Surgeon",
                    "Signal": surgeon_row.get("status") or "unknown",
                    "Detail": f"blocking={surgeon_row.get('blocking_count', 0)}",
                },
                {
                    "Surface": "Statecraft War Room",
                    "Signal": war_room_row.get("sync_status") or "unknown",
                    "Detail": f"objects={war_room_row.get('active_object_count', 0)}",
                },
                {
                    "Surface": "Command Deck",
                    "Signal": "git "
                    + ("clean" if deck_row.get("git_clean") else "dirty")
                    + "; budget "
                    + ("stale" if deck_row.get("budget_stale") else "ok"),
                    "Detail": f"surgeon={deck_row.get('surgeon_status')}; sync={deck_row.get('war_room_sync_status')}",
                },
            ],
            ["Surface", "Signal", "Detail"],
        ),
        "## 2. Top Next Actions",
        "",
    ]

    next_actions = deck.get("next_actions") or []
    if next_actions:
        action_rows = [
            {
                "Priority": a.get("priority", ""),
                "Category": a.get("category", ""),
                "Action": a.get("action", ""),
                "Source": a.get("source_path") or "",
            }
            for a in next_actions[: max(config.max_next_actions, 7)]
        ]
        parts.append(markdown_table(action_rows, ["Priority", "Category", "Action", "Source"]))
    else:
        parts.append("_None — regenerate Command Deck or run with `--all`._\n")

    parts.extend(["", "## 3. Child Dashboards", ""])
    child_rows = [
        {
            "Dashboard": name,
            "Question": question,
            "Path": f"`{_rel_posix(repo_root, Path(path))}`",
        }
        for name, question, path in CHILD_DASHBOARDS
    ]
    parts.append(markdown_table(child_rows, ["Dashboard", "Question", "Path"]))

    parts.extend(
        [
            "",
            "## 4. Regeneration",
            "",
            "```bash",
            "python3 scripts/operator_dashboard.py --all",
            "```",
            "",
            "Individual producers remain available under `runtime/artifacts/<bucket>/README.md`.",
            "",
        ]
    )
    return "\n".join(parts)


def write_umbrella(
    repo_root: Path,
    config: DashboardRunConfig,
    surgeon: dict[str, Any],
    war_room: dict[str, Any],
    deck: dict[str, Any],
) -> dict[str, Any]:
    generated_at = utc_now_iso()
    out_path = _resolve(repo_root, config.out)
    json_path = _resolve(repo_root, config.json_out)
    md = build_umbrella_markdown(
        surgeon,
        war_room,
        deck,
        generated_at=generated_at,
        repo_root=repo_root,
        config=config,
    )
    payload = build_umbrella_json(
        surgeon,
        war_room,
        deck,
        generated_at=generated_at,
        repo_root=repo_root,
        config=config,
    )
    write_report(out_path, md, snapshot=config.snapshot)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out_path}")
    print(f"wrote {json_path}")
    return payload


def run_all(repo_root: Path, config: DashboardRunConfig) -> UmbrellaResult:
    if config.compose_only:
        surgeon, war_room, deck = load_child_payloads(repo_root, config)
        child_exit = 0
    else:
        child_exit, surgeon, war_room, deck = run_child_producers(repo_root, config)

    if not surgeon or not war_room or not deck:
        return UmbrellaResult(
            exit_code=_worst_exit(child_exit, 2),
            surgeon_payload=surgeon,
            war_room_payload=war_room,
            deck_payload=deck,
            umbrella_payload={},
        )

    umbrella_payload = write_umbrella(repo_root, config, surgeon, war_room, deck)
    return UmbrellaResult(
        exit_code=child_exit,
        surgeon_payload=surgeon,
        war_room_payload=war_room,
        deck_payload=deck,
        umbrella_payload=umbrella_payload,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--compose-only",
        action="store_true",
        help="Compose umbrella from existing child latest.json files (skip producers)",
    )
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--json-out", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--snapshot", action="store_true")
    parser.add_argument("--surgeon-scope", default="docs", choices=("docs", "statecraft", "skills", "all"))
    parser.add_argument("--full-surgeon", action="store_true")
    parser.add_argument("--verify-portable-skills", action="store_true")
    parser.add_argument("--fail-on-blocking", action="store_true")
    parser.add_argument("--war-room-latest-days", type=int, default=7)
    parser.add_argument("--war-room-max-objects", type=int, default=12)
    parser.add_argument("--max-next-actions", type=int, default=5)
    parser.add_argument("--include-gate", action="store_true")
    parser.add_argument("--no-git", action="store_true")
    args = parser.parse_args()

    config = DashboardRunConfig(
        out=args.out,
        json_out=args.json_out,
        snapshot=args.snapshot,
        compose_only=args.compose_only,
        surgeon_scope=args.surgeon_scope,
        full_surgeon=args.full_surgeon,
        verify_portable_skills=args.verify_portable_skills,
        fail_on_blocking=args.fail_on_blocking,
        war_room_latest_days=args.war_room_latest_days,
        war_room_max_objects=args.war_room_max_objects,
        max_next_actions=args.max_next_actions,
        include_gate=args.include_gate,
        no_git=args.no_git,
    )

    result = run_all(REPO_ROOT, config)
    if result.umbrella_payload:
        actions = len(result.umbrella_payload.get("next_actions") or [])
        print(f"umbrella: next_actions={actions} exit={result.exit_code}")
    return result.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
