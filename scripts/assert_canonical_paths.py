#!/usr/bin/env python3
"""
Assert that the repository root has the canonical path layout (lowercase filenames).

Required: self.md, self-archive.md, recursion-gate.md
Optional: self-evidence.md (compatibility pointer; checked if --strict).

Usage:
  python scripts/assert_canonical_paths.py
  python scripts/assert_canonical_paths.py --strict

Exit: 0 if all required (and optional when --strict) paths exist at the root; 1 otherwise.
Set GRACE_MAR_SKIP_PATH_CHECK=1 to skip (exit 0 without checking).

Advisory: prints WARN to stderr for legacy `skills.md` / duplicate capability index
(see `repo_io.self_skills_layout_warnings`). Strict canonical skills: set
`GRACE_MAR_REQUIRE_CANONICAL_SELF_SKILLS=1` (enforced in `assert_canonical_record_layout`).
"""

import argparse
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(REPO_ROOT / "scripts"))
from repo_io import CANONICAL_RECORD_FILES_REQUIRED, self_skills_layout_warnings  # noqa: E402

REQUIRED = CANONICAL_RECORD_FILES_REQUIRED
OPTIONAL_STRICT = ("self-evidence.md",)


def main() -> int:
    if os.environ.get("GRACE_MAR_SKIP_PATH_CHECK") == "1":
        return 0
    parser = argparse.ArgumentParser(description="Assert canonical root paths exist.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Also require self-evidence.md (optional compatibility pointer)",
    )
    args = parser.parse_args()
    missing = []
    for name in REQUIRED:
        if not (REPO_ROOT / name).is_file():
            missing.append(name)
    if args.strict:
        for name in OPTIONAL_STRICT:
            if not (REPO_ROOT / name).is_file():
                missing.append(name)
    if missing:
        print(f"assert_canonical_paths: missing under repository root: {', '.join(missing)}", file=sys.stderr)
        return 1
    for w in self_skills_layout_warnings(REPO_ROOT):
        print(f"assert_canonical_paths: WARN â€” {w}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
