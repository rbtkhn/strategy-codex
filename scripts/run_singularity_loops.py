#!/usr/bin/env python3
"""List singularity loops from the generated registry (orchestrator stub)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REGISTRY = REPO_ROOT / "runtime" / "artifacts" / "loop-registry.json"
DEFAULT_SIGNALS = REPO_ROOT / "runtime" / "artifacts" / "singularity-signals.json"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from singularity_loop_lib import (  # noqa: E402
    load_registry,
    refresh_orchestrator_signals,
)

def _print_loops(loops: list[dict], *, status_filter: str | None) -> None:
    for row in loops:
        status = str((row.get("state") or {}).get("status") or "")
        if status_filter and status != status_filter:
            continue
        loop_id = row.get("id", "?")
        print(f"[loop] {loop_id} ({status})")

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--registry",
        type=Path,
        default=DEFAULT_REGISTRY,
        help="Loop registry JSON path",
    )
    ap.add_argument(
        "--status",
        action="store_true",
        help="Write orchestrator signals stub from loop states",
    )
    ap.add_argument(
        "--signals-output",
        type=Path,
        default=DEFAULT_SIGNALS,
        help="Signals JSON output path for --status",
    )
    ap.add_argument(
        "--active-only",
        action="store_true",
        help="Print only active loops",
    )
    args = ap.parse_args()

    try:
        registry = load_registry(registry_path=args.registry)
    except (FileNotFoundError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    loops = registry.get("loops") or []
    if not isinstance(loops, list):
        print("error: registry loops must be a list", file=sys.stderr)
        return 1

    status_filter = "active" if args.active_only else None
    _print_loops(loops, status_filter=status_filter)

    if args.status:
        refresh_orchestrator_signals(
            registry_path=args.registry,
            output_path=args.signals_output,
            source="scripts/run_singularity_loops.py --status",
        )
        print(f"[ok] wrote {args.signals_output.relative_to(REPO_ROOT)}")

    print("[ok] singularity loops listed (dry-run; no execution)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
