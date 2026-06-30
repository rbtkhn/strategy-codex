#!/usr/bin/env python3
"""Deprecated shim — use scripts/build_work_pass_ledger.py (Phase 3 compression).

Re-exports legacy names for import compatibility. CLI prints a one-line deprecation
notice to stderr then delegates to the work-pass ledger renderer.
"""

from __future__ import annotations

import sys
import warnings
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from build_work_pass_ledger import (  # noqa: E402,F401
    build_conductor_ledger,
    build_work_pass_ledger,
    collect_friction_candidates,
    collect_recent_conductor_closes,
    collect_recent_work_pass_closes,
    render_conductor_ledger_markdown,
    render_work_pass_ledger_markdown,
)

_DEPRECATION = (
    "build_conductor_ledger.py is deprecated; use build_work_pass_ledger.py "
    "(see CONDUCTOR-COMPRESSION-SPEC.md)."
)

def main() -> int:
    warnings.warn(_DEPRECATION, DeprecationWarning, stacklevel=1)
    print(f"note: {_DEPRECATION}", file=sys.stderr)
    from build_work_pass_ledger import main as work_pass_main

    return work_pass_main()

if __name__ == "__main__":
    raise SystemExit(main())
