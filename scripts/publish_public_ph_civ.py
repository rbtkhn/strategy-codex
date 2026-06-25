#!/usr/bin/env python3
"""DEPRECATED — Predictive History ships from the canonical repo, not strategy-codex."""

from __future__ import annotations

import sys

DOC = "docs/predictive-history-operator-workspace.md"


def main() -> int:
    print(
        "ERROR: publish_public_ph_civ.py is deprecated.\n"
        "Predictive History corpus is authored in rbtkhn/predictive-history only.\n"
        f"See {DOC} — edit PREDICTIVE_HISTORY_ROOT, git push upstream, then:\n"
        "  python scripts/sync_predictive_history_mirror.py\n"
        "  git commit -m \"[predictive-history-sync] …\"",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
