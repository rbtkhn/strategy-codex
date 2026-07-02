"""Thin CLI: delegates to ``scripts/`` entrypoints (see pyproject ``project.scripts``)."""

from __future__ import annotations

import os
import subprocess
import sys

from grace_mar.repo_io import repo_root

def _usage() -> str:
    return (
        "Usage: grace-mar <command> [args...]\n\n"
        "Commands:\n"
        "  warmup              -> scripts/harness_warmup.py\n"
        "  reflect             -> scripts/reflection_cycle.py\n"
        "  predictive-history  -> scripts/predictive-history.py\n"
        "  gate board [-u USER]     -> scripts/build_gate_board.py\n"
        "  gate list [-u USER]      -> scripts/preview_candidate_impact.py\n"
        "  gate diff ID [-u USER]   -> scripts/preview_candidate_impact.py --candidate ID\n"
        "  gate merge [-u USER]     -> scripts/process_approved_candidates.py --apply\n"
    )

def _run_script(root, script_name: str, *args: str) -> int:
    script = root / "scripts" / script_name
    return subprocess.call([sys.executable, str(script), *args])

def _default_user_flag(rest: list[str]) -> list[str]:
    if "-u" in rest or "--user" in rest:
        return rest
    user = os.getenv("GRACE_MAR_USER_ID", "strategy-codex").strip() or "strategy-codex"
    return ["-u", user, *rest]

def _gate_command(root, rest: list[str]) -> int:
    if not rest or rest[0] in ("-h", "--help"):
        print(_usage(), file=sys.stderr)
        return 0 if rest and rest[0] in ("-h", "--help") else 2

    sub = rest[0]
    tail = rest[1:]

    if sub == "board":
        return _run_script(root, "build_gate_board.py", *_default_user_flag(tail))

    if sub == "list":
        return _run_script(root, "preview_candidate_impact.py", *_default_user_flag(tail))

    if sub == "diff":
        if not tail or tail[0].startswith("-"):
            print("gate diff requires CANDIDATE-XXXX", file=sys.stderr)
            return 2
        candidate_id = tail[0]
        user_tail = tail[1:]
        return _run_script(
            root,
            "preview_candidate_impact.py",
            *_default_user_flag(user_tail),
            "--candidate",
            candidate_id,
        )

    if sub == "merge":
        print(
            "Companion approval required — merges approved candidates into Record surfaces only.",
            file=sys.stderr,
        )
        return _run_script(
            root,
            "process_approved_candidates.py",
            *_default_user_flag(tail),
            "--apply",
        )

    print(f"Unknown gate subcommand: {sub}", file=sys.stderr)
    return 2

def main() -> int:
    argv = sys.argv[1:]
    if not argv or argv[0] in ("-h", "--help"):
        print(_usage(), file=sys.stderr)
        return 0 if argv and argv[0] in ("-h", "--help") else 2

    cmd = argv[0]
    rest = argv[1:]
    root = repo_root()
    if cmd == "warmup":
        return _run_script(root, "harness_warmup.py", *rest)
    if cmd == "reflect":
        return _run_script(root, "reflection_cycle.py", *rest)
    if cmd == "predictive-history":
        return _run_script(root, "predictive-history.py", *rest)
    if cmd == "gate":
        return _gate_command(root, rest)

    print(f"Unknown command: {cmd}", file=sys.stderr)
    return 2

if __name__ == "__main__":
    raise SystemExit(main())
