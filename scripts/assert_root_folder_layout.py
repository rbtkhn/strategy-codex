#!/usr/bin/env python3
"""Assert repository root has at most TARGET_ROOT_FOLDERS count."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from repo_io import TARGET_ROOT_FOLDERS  # noqa: E402

MAX_ROOT_FOLDERS = len(TARGET_ROOT_FOLDERS)

def main() -> int:
    names = sorted(
        p.name for p in REPO_ROOT.iterdir() if p.is_dir() and p.name in TARGET_ROOT_FOLDERS
    )
    if len(names) > MAX_ROOT_FOLDERS:
        extra = sorted(set(names) - set(TARGET_ROOT_FOLDERS))
        print(
            f"assert_root_folder_layout: {len(names)} root folders (max {MAX_ROOT_FOLDERS}). "
            f"Extra: {', '.join(extra) if extra else 'unknown'}",
            file=sys.stderr,
        )
        return 1
    missing = sorted(set(TARGET_ROOT_FOLDERS) - set(names))
    if missing:
        print(
            f"assert_root_folder_layout: missing expected folders: {', '.join(missing)}",
            file=sys.stderr,
        )
        return 1
    print(f"assert_root_folder_layout: ok ({len(names)} folders)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
