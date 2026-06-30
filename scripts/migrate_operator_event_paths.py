#!/usr/bin/env python3
"""Move root operator JSONL ledgers into runtime/operator-events/ and last-dream into runtime/daily-handoff/.

Usage:
  python3 scripts/migrate_operator_event_paths.py --dry-run
  python3 scripts/migrate_operator_event_paths.py --apply
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from repo_io import (  # noqa: E402
    LAST_DREAM_BASENAME,
    OPERATOR_LEDGER_FILES,
    OPERATOR_EVENTS_DIR,
    last_dream_write_path,
    profile_dir,
)

def _plan_moves() -> list[tuple[Path, Path]]:
    moves: list[tuple[Path, Path]] = []
    root = profile_dir("")
    OPERATOR_EVENTS_DIR.mkdir(parents=True, exist_ok=True)
    for name in OPERATOR_LEDGER_FILES:
        src = root / name
        dst = OPERATOR_EVENTS_DIR / name
        if src.is_file() and not dst.exists():
            moves.append((src, dst))
    dream_src = root / LAST_DREAM_BASENAME
    dream_dst = last_dream_write_path("")
    if dream_src.is_file() and not dream_dst.exists():
        moves.append((dream_src, dream_dst))
    return moves

def main() -> int:
    parser = argparse.ArgumentParser(description="Migrate operator ledgers to runtime/operator-events/")
    parser.add_argument("--dry-run", action="store_true", help="Print planned moves only")
    parser.add_argument("--apply", action="store_true", help="Perform moves")
    args = parser.parse_args()
    if not args.dry_run and not args.apply:
        parser.error("Specify --dry-run or --apply")
    moves = _plan_moves()
    if not moves:
        print("No moves needed (targets exist or sources missing).")
        return 0
    for src, dst in moves:
        rel_src = src.relative_to(REPO_ROOT)
        rel_dst = dst.relative_to(REPO_ROOT)
        if args.dry_run:
            print(f"would move {rel_src} -> {rel_dst}")
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dst))
            print(f"moved {rel_src} -> {rel_dst}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
