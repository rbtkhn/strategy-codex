#!/usr/bin/env python3
"""
Consolidated coffee Step 1 - single entry point for all warmup modes.

Replaces the need for the agent (or operator) to choose between
operator_daily_warmup, harness_warmup, operator_handoff_check, and
operator_reentry_stack depending on context.  Mode selects the right
combination; all four underlying scripts are preserved and still callable
individually.

Modes
-----
  work-start  Full work-start coffee: daily warmup + harness warmup + branch snapshot
  light       Lighter pass: daily warmup + compact harness + one-line branch
  minimal     Minimal pass: compact harness only (no daily warmup unless --include-warmup)
  closeout    Signing-off Step 1: handoff check (gate, PH closeout, commits, worktree) - same coffee A-D hub menu after; conductor remains name-only
  reentry     Cold-thread stack: handoff + daily warmup + harness (same as operator_reentry_stack)
  first-command
              New-chat bootstrap: Coffee Bootstrap Brief + inline fast Step 1 (one Python
              process, one git status scan). Skips subprocess chain, integrity validator,
              gh auth probe, and daily warmup. Use --verbose for full blocks; --subprocess
              for legacy subprocess chain.

Usage
-----
    python3 scripts/operator_coffee.py                                  # default: strategy-codex work-start
    python3 scripts/operator_coffee.py -u strategy-codex --mode first-command
    python3 scripts/operator_coffee.py -u strategy-codex --first-command
    python3 scripts/operator_coffee.py -u strategy-codex --mode light
    python3 scripts/operator_coffee.py -u strategy-codex --mode closeout
    python3 scripts/operator_coffee.py -u strategy-codex --mode reentry --compact
    python3 scripts/operator_coffee.py -u strategy-codex --verbose-dream   # full last-dream block in daily warmup
    CURSOR_MODEL="Sonnet" python3 scripts/operator_coffee.py -u strategy-codex   # cadence audit parity (optional)
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from repo_io import DEFAULT_USER_ID, profile_dir
MODES = ("work-start", "light", "minimal", "closeout", "reentry", "first-command")
_CAPTURE_KWARGS = {
    "capture_output": True,
    "text": True,
    "encoding": "utf-8",
    "errors": "replace",
}

def _configure_utf8_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8", errors="replace")

def _run(argv: list[str], *, label: str | None = None, quiet: bool = False) -> int:
    display = label or " ".join(argv)
    if quiet:
        r = subprocess.run(argv, cwd=str(_REPO), **_CAPTURE_KWARGS)
        if r.returncode == 0:
            print(f"$ {display} ... ok", flush=True)
            return 0
        print(f"\n{'=' * 60}\n$ {display}\n{'=' * 60}\n", flush=True)
        if r.stdout:
            print(r.stdout, end="" if r.stdout.endswith("\n") else "\n")
        if r.stderr:
            print(r.stderr, end="" if r.stderr.endswith("\n") else "\n", file=sys.stderr)
        return r.returncode
    print(f"\n{'=' * 60}\n$ {display}\n{'=' * 60}\n", flush=True)
    r = subprocess.run(argv, cwd=str(_REPO))
    return r.returncode

def _branch_snapshot() -> str:
    """One plain-language block: branch hygiene status."""
    try:
        from git_worktree_snapshot import get_git_worktree_snapshot
    except ImportError:
        from scripts.git_worktree_snapshot import get_git_worktree_snapshot  # type: ignore

    snap = get_git_worktree_snapshot()
    if not snap.ok:
        return f"Branch snapshot unavailable: {snap.error}"
    if snap.branch_name == "main" and not snap.status_lines:
        return "Branch hygiene: clean (main only)."
    status_out = "\n".join(snap.porcelain_lines)
    return (
        f"Branch snapshot:\n{status_out}\n\n"
        f"Non-main branch check: branch={snap.branch_name}."
    )

def _emit_inline(label: str, text: str, *, quiet: bool) -> None:
    if quiet:
        print(f"$ {label} ... ok", flush=True)
        return
    print(f"\n{'=' * 60}\n$ {label}\n{'=' * 60}\n", flush=True)
    if text:
        print(text, end="" if text.endswith("\n") else "\n")

def _refresh_singularity_loop_signals(*, quiet: bool) -> None:
    try:
        from singularity_loop_lib import refresh_and_brief

        brief = refresh_and_brief(source="scripts/operator_coffee.py")
        if brief and not quiet:
            print(f"\n{brief}\n", flush=True)
    except Exception:
        pass

def _emit_agent_handoff_glance(*, quiet: bool) -> None:
    try:
        from check_agent_handoff_queue import render_agent_handoff_glance
    except ImportError:
        from scripts.check_agent_handoff_queue import render_agent_handoff_glance  # type: ignore

    _emit_inline(
        "check_agent_handoff_queue.py --glance",
        render_agent_handoff_glance(),
        quiet=False,
    )

def _run_inline_steps(
    user: str,
    *,
    mode: str,
    compact: bool,
    quiet: bool,
    verbose_dream: bool,
    show_civ_mem: bool,
    show_rollup: bool,
    fast: bool,
) -> int:
    """Run coffee Step 1 in-process (one Python interpreter, one git snapshot)."""
    try:
        from git_worktree_snapshot import get_git_worktree_snapshot
    except ImportError:
        from scripts.git_worktree_snapshot import get_git_worktree_snapshot  # type: ignore

    get_git_worktree_snapshot(refresh=True)

    if mode == "closeout":
        from operator_handoff_check import build_handoff_check

        _emit_inline(
            f"operator_handoff_check.py -u {user}",
            build_handoff_check(user_id=user, fast=fast),
            quiet=quiet,
        )
        return 0

    if mode in {"reentry", "first-command"}:
        from operator_handoff_check import build_handoff_check

        handoff_fast = fast or mode == "first-command"
        _emit_inline(
            f"operator_handoff_check.py -u {user}" + (" --fast" if handoff_fast else ""),
            build_handoff_check(user_id=user, fast=handoff_fast),
            quiet=quiet,
        )

    if mode in {"work-start", "light", "reentry"}:
        from operator_daily_warmup import build_operator_daily_warmup

        _emit_inline(
            f"operator_daily_warmup.py -u {user}",
            build_operator_daily_warmup(
                user_id=user,
                verbose_dream=verbose_dream,
                show_civ_mem=show_civ_mem or None,
                show_rollup=show_rollup or None,
                fast=fast or mode in {"light", "first-command"},
            ),
            quiet=quiet,
        )

    if mode in {"work-start", "light", "minimal", "reentry", "first-command"}:
        from harness_warmup import render_compact_warmup

        _emit_inline(
            f"harness_warmup.py -u {user} --compact",
            render_compact_warmup(user),
            quiet=quiet,
        )

    if mode in {"work-start", "light", "minimal", "reentry", "first-command", "closeout"}:
        _emit_agent_handoff_glance(quiet=quiet)

    _refresh_singularity_loop_signals(quiet=quiet)
    return 0

def main() -> int:
    _configure_utf8_stdio()
    p = argparse.ArgumentParser(
        description="Consolidated coffee Step 1 - single entry point for all warmup modes."
    )
    p.add_argument("-u", "--user", default=DEFAULT_USER_ID, help=f"User id (default: {DEFAULT_USER_ID})")
    p.add_argument(
        "--mode", "-m",
        choices=MODES,
        default="work-start",
        help="Warmup mode (default: work-start)",
    )
    p.add_argument(
        "--compact",
        action="store_true",
        help="Pass --compact to harness_warmup.py",
    )
    p.add_argument(
        "--first-command",
        action="store_true",
        help="Alias for --mode first-command (new-chat archive/grace-mar-instance/bootstrap).",
    )
    p.add_argument(
        "--verbose",
        action="store_true",
        help="In first-command mode, print detailed underlying script blocks.",
    )
    p.add_argument(
        "--include-warmup",
        action="store_true",
        help="In minimal mode, also run operator_daily_warmup",
    )
    p.add_argument(
        "--verbose-dream",
        action="store_true",
        help="Pass --verbose-dream to operator_daily_warmup.py (full last-dream block)",
    )
    p.add_argument(
        "--show-civ-mem",
        action="store_true",
        help="Pass --show-civ-mem to operator_daily_warmup.py (collapsed civ-mem line)",
    )
    p.add_argument(
        "--show-rollup",
        action="store_true",
        help="Pass --show-rollup to operator_daily_warmup.py (collapsed coffee rollup line)",
    )
    p.add_argument(
        "--cursor-model",
        default=None,
        help="Cursor UI model label for work-cadence-events line (else CURSOR_MODEL env, else unknown)",
    )
    p.add_argument(
        "--fast",
        action="store_true",
        help="Fast Step 1: shared git snapshot, skip integrity/gh/pytest probes, handoff --fast.",
    )
    p.add_argument(
        "--subprocess",
        action="store_true",
        help="Force legacy subprocess chain instead of in-process Step 1.",
    )
    args = p.parse_args()
    if args.first_command:
        args.mode = "first-command"
    user = args.user
    py = sys.executable

    from gate_block_parser import sweep_rejected_to_processed
    gate_path = profile_dir(user) / "recursion-gate.md"
    swept = sweep_rejected_to_processed(gate_path)
    if swept:
        print(f"Gate cleanup: moved {len(swept)} rejected candidate(s) to Processed: {', '.join(swept)}")

    warmup = [py, "scripts/operator_daily_warmup.py", "-u", user]
    if args.verbose_dream:
        warmup.append("--verbose-dream")
    if args.show_civ_mem:
        warmup.append("--show-civ-mem")
    if args.show_rollup:
        warmup.append("--show-rollup")
    harness = [py, "scripts/harness_warmup.py", "-u", user]
    harness_compact = [py, "scripts/harness_warmup.py", "-u", user, "--compact"]
    handoff = [py, "scripts/operator_handoff_check.py", "-u", user]

    steps: list[list[str]] = []

    if args.mode == "work-start":
        steps = [warmup, harness_compact if args.compact else harness]
    elif args.mode == "light":
        steps = [warmup, harness_compact]
    elif args.mode == "minimal":
        if args.include_warmup:
            steps.append(warmup)
        steps.append(harness_compact)
    elif args.mode == "closeout":
        steps = [handoff]
    elif args.mode == "reentry":
        steps = [handoff, warmup, harness_compact if args.compact else harness]
    elif args.mode == "first-command":
        steps = [handoff, warmup, harness_compact]

    first_command = args.mode == "first-command"
    show_details = not first_command or args.verbose
    fast = args.fast or first_command
    use_inline = not args.subprocess

    if first_command:
        try:
            from coffee_bootstrap_brief import build_coffee_bootstrap_brief, format_coffee_bootstrap_brief

            print(format_coffee_bootstrap_brief(build_coffee_bootstrap_brief(user, fast=fast)))
            if args.verbose:
                print()
        except Exception as exc:
            print(f"Coffee Bootstrap Brief: unavailable ({exc})")

    if use_inline:
        code = _run_inline_steps(
            user,
            mode=args.mode,
            compact=args.compact,
            quiet=first_command and not args.verbose,
            verbose_dream=args.verbose_dream,
            show_civ_mem=args.show_civ_mem,
            show_rollup=args.show_rollup,
            fast=fast,
        )
        if code != 0:
            return code
    else:
        for argv in steps:
            argv = list(argv)
            if fast and "operator_handoff_check.py" in " ".join(argv):
                argv.append("--fast")
            if fast and "operator_daily_warmup.py" in " ".join(argv):
                argv.append("--fast")
            code = _run(argv, quiet=first_command and not args.verbose)
            if code != 0:
                return code

    if args.mode != "closeout" and show_details:
        print(f"\n{'=' * 60}\n$ git branch snapshot\n{'=' * 60}\n", flush=True)
        print(_branch_snapshot())

    if args.mode in {
        "work-start",
        "light",
        "minimal",
        "reentry",
        "first-command",
        "closeout",
    }:
        try:
            from check_agent_handoff_queue import render_agent_handoff_glance
        except ImportError:
            from scripts.check_agent_handoff_queue import render_agent_handoff_glance  # type: ignore

        if not use_inline:
            print(f"\n{'=' * 60}\n$ agent handoff queue glance\n{'=' * 60}\n", flush=True)
            print(render_agent_handoff_glance())

    try:
        from assess_session_load import (
            assess_load,
            format_default_acceptance_line,
            format_load_one_liner,
        )
        load_result = assess_load(user)
        if show_details:
            print(f"\n{'=' * 60}\n$ session load assessment\n{'=' * 60}\n", flush=True)
            print(format_load_one_liner(load_result))
            print(format_default_acceptance_line(load_result))
    except Exception:
        try:
            from scripts.assess_session_load import (
                assess_load,
                format_default_acceptance_line,
                format_load_one_liner,
            )
            load_result = assess_load(user)
            if show_details:
                print(f"\n{'=' * 60}\n$ session load assessment\n{'=' * 60}\n", flush=True)
                print(format_load_one_liner(load_result))
                print(format_default_acceptance_line(load_result))
        except Exception:
            pass

    try:
        from build_memory_observability import build_report, format_observability_one_liner
        memory_report = build_report(user)
        if show_details and memory_report.get("overall_status") != "ok":
            print(f"\n{'=' * 60}\n$ memory observability\n{'=' * 60}\n", flush=True)
            print(format_observability_one_liner(memory_report))
    except Exception:
        try:
            from scripts.build_memory_observability import build_report, format_observability_one_liner
            memory_report = build_report(user)
            if show_details and memory_report.get("overall_status") != "ok":
                print(f"\n{'=' * 60}\n$ memory observability\n{'=' * 60}\n", flush=True)
                print(format_observability_one_liner(memory_report))
        except Exception:
            pass

    try:
        from cadence_conductor_resolution import format_coffee_hub_e_line

        if show_details:
            print(
                f"\n{'=' * 60}\n"
                f"$ Standalone Conductor note (not a coffee hub line)\n"
                f"{'=' * 60}\n",
                flush=True,
            )
            print(format_coffee_hub_e_line(user), flush=True)
    except Exception:
        try:
            from scripts.cadence_conductor_resolution import format_coffee_hub_e_line

            if show_details:
                print(
                    f"\n{'=' * 60}\n"
                    f"$ Standalone Conductor note (not a coffee hub line)\n"
                    f"{'=' * 60}\n",
                    flush=True,
                )
                print(format_coffee_hub_e_line(user), flush=True)
        except Exception:
            pass

    try:
        from log_cadence_event import append_cadence_event
        from cadence_learning import log_coffee_choice_start
        coffee_id = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        append_cadence_event(
            "coffee",
            user,
            ok=True,
            mode=args.mode,
            cursor_model=args.cursor_model.strip() if args.cursor_model else None,
        )
        if "load_result" in locals():
            log_coffee_choice_start(user, coffee_id=coffee_id, load_result=load_result)
    except Exception:
        pass

    _refresh_singularity_loop_signals(quiet=first_command and not args.verbose)
    return 0

if __name__ == "__main__":
    sys.exit(main())
