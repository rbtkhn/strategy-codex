"""Deprecated local work-jiang rebuild entrypoint.

Predictive History is now owned canonically by the external `rbtkhn/ph-workshop`
repo. This script remains only to make the boundary explicit if an old workflow tries
to use strategy-codex as the writable build surface.
"""
from __future__ import annotations

import sys

DEPRECATION_MESSAGE = """\
Predictive History local rebuilds are deprecated in `strategy-codex`.

Canonical writable ownership now lives in:
  https://github.com/rbtkhn/ph-workshop

`strategy-codex` may review Predictive History packets and critique external work,
but it must not regenerate or maintain PH corpus/manuscript state locally.
"""

def main() -> int:
    print(DEPRECATION_MESSAGE, file=sys.stderr)
    return 2

if __name__ == "__main__":
    raise SystemExit(main())
