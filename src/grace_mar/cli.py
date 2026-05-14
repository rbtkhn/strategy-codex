"""Thin CLI: delegates to ``scripts/`` entrypoints (see pyproject ``project.scripts``)."""

from __future__ import annotations

import subprocess
import sys

from grace_mar.repo_io import repo_root


def main() -> int:
    argv = sys.argv[1:]
    if not argv or argv[0] in ("-h", "--help"):
        print(
            "Usage: grace-mar <command> [args...]\n\n"
            "Commands:\n"
            "  warmup              -> scripts/harness_warmup.py\n"
            "  reflect             -> scripts/reflection_cycle.py\n"
            "  predictive-history  -> scripts/predictive-history.py\n",
            file=sys.stderr,
        )
        return 0 if argv and argv[0] in ("-h", "--help") else 2

    cmd = argv[0]
    rest = argv[1:]
    root = repo_root()
    if cmd == "warmup":
        script = root / "scripts" / "harness_warmup.py"
        return subprocess.call([sys.executable, str(script), *rest])
    if cmd == "reflect":
        script = root / "scripts" / "reflection_cycle.py"
        return subprocess.call([sys.executable, str(script), *rest])
    if cmd == "predictive-history":
        script = root / "scripts" / "predictive-history.py"
        return subprocess.call([sys.executable, str(script), *rest])

    print(f"Unknown command: {cmd}", file=sys.stderr)
    return 2
