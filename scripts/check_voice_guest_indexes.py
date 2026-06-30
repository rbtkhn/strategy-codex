#!/usr/bin/env python3
"""Run --check on split-identity guest voice index builders."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"

GUEST_INDEX_BUILDERS: tuple[str, ...] = (
    "build_alkhorshid_guest_index.py",
    "build_davis_guest_index.py",
    "build_diesen_guest_index.py",
    "build_mercouris_guest_index.py",
)

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--voice",
        metavar="SLUG",
        help="Check one guest index builder (alkhorshid, davis, diesen, mercouris)",
    )
    args = parser.parse_args(argv)

    builders = GUEST_INDEX_BUILDERS
    if args.voice:
        slug = args.voice.strip().casefold()
        match = tuple(b for b in builders if b == f"build_{slug}_guest_index.py" or slug in b)
        if not match:
            print(
                f"error: no guest builder for slug {args.voice!r}; "
                f"expected one of alkhorshid, davis, diesen, mercouris",
                file=sys.stderr,
            )
            return 1
        builders = match

    rc = 0
    for name in builders:
        script = SCRIPTS / name
        if not script.is_file():
            print(f"error: missing {script.relative_to(REPO_ROOT)}", file=sys.stderr)
            rc = 1
            continue
        proc = subprocess.run(
            [sys.executable, str(script), "--check"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        tail = (proc.stdout or proc.stderr or "").strip().splitlines()
        summary = tail[-1] if tail else f"exit {proc.returncode}"
        if proc.returncode == 0:
            print(f"ok: {name}: {summary}")
        else:
            print(f"fail: {name}: {summary}", file=sys.stderr)
            rc = 1
    return rc

if __name__ == "__main__":
    raise SystemExit(main())
