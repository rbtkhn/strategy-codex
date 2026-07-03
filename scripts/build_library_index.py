#!/usr/bin/env python3
"""
Retired: operator-books dashboard from museum self-library.md.

Operator books are discovered via misc folder README/STATUS and continuity/README.md.
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from repo_io import ARTIFACTS_DIR  # noqa: E402

STUB = """# Library index — retired

**Generated:** {stamp}

The central operator-books dashboard is **retired**. Operator books live in **misc folder homes** only.

| Phrase | Path |
|--------|------|
| strategy-codex | `continuity/` |
| predictive-history | `continuity/predictive-history/` |
| cici notebook | `singularity/work-cici/cici-notebook/` |
| dev journal | `docs/archive/skill-work-legacy/work-dev/dev-notebook/work-dev/journal/` |
| history notebook | `docs/archive/skill-work-legacy/work-strategy/history-notebook/` |
| theology notebook | `docs/archive/skill-work-legacy/work-strategy/theology-notebook/` |

See **`continuity/README.md`** § Operator books (misc homes) and **`.cursor/rules/operator-books-routing.mdc`**.
"""

def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--check", action="store_true", help="Verify stub exists (no-op rebuild)")
    args = p.parse_args()
    out = ARTIFACTS_DIR / "library-index.md"
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    text = STUB.format(stamp=stamp)
    if args.check and out.is_file() and "retired" in out.read_text(encoding="utf-8"):
        print("library-index stub: ok")
        return 0
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(f"Wrote {out}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
