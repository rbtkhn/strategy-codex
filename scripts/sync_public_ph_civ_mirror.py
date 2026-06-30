#!/usr/bin/env python3
"""DEPRECATED shim — use sync_predictive_history_mirror.py."""

from __future__ import annotations

import sys
import warnings

from sync_predictive_history_mirror import main as sync_main

def main(argv: list[str] | None = None) -> int:
    warnings.warn(
        "sync_predictive_history_mirror.py is deprecated; use sync_predictive_history_mirror.py",
        DeprecationWarning,
        stacklevel=1,
    )
    print(
        "NOTE: sync_predictive_history_mirror.py is deprecated; use sync_predictive_history_mirror.py",
        file=sys.stderr,
    )
    return sync_main(argv)

if __name__ == "__main__":
    raise SystemExit(main())
