"""Deprecated grace-mar CLI alias."""

from __future__ import annotations

import sys

from grace_mar.cli import main as _grace_main


def main() -> int:
    print(
        "warning: `grace-mar` CLI is deprecated; use `strategy-codex` instead. "
        "See docs/archive/grace-mar-compatibility.md.",
        file=sys.stderr,
    )
    return _grace_main()


if __name__ == "__main__":
    raise SystemExit(main())
