#!/usr/bin/env python3
"""Shared audit gate for manual-curated voice indexes (no auto-regen body)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"

def run_shelf_audit(slug: str) -> int:
    proc = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "audit_statecraft_archive_index.py"),
            "--shelf-index",
            slug,
        ],
        cwd=REPO,
    )
    return proc.returncode

def gate_main(slug: str, *, check_only_default_ok: bool = True) -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description=f"Parity gate for manual-curated {slug}-index.md (audit only; edit index by hand)."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit non-zero when shelf audit fails",
    )
    args = parser.parse_args()
    rc = run_shelf_audit(slug)
    if rc == 0:
        print(f"ok: {slug}-index manual curated; audit pass")
    return rc if args.check else (0 if check_only_default_ok and rc == 0 else rc)
