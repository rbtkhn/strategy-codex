#!/usr/bin/env python3
"""Report hardcoded consolidated paths vs repo_io constant adoption."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from repo_io import REPO_PATH_MIGRATIONS  # noqa: E402

SCAN = REPO_ROOT / "scripts"
SKIP = {"adopt_repo_path_constants.py", "apply_root_path_rewrites.py", "check_repo_path_adoption.py"}

# Literal path strings that should shrink toward zero (use repo_io constants instead).
LEGACY_LITERALS: list[tuple[str, str]] = [
    ('REPO_ROOT / "runtime/artifacts"', "artifacts"),
    ('repo_root / "runtime/artifacts"', "artifacts"),
    (' / "runtime/artifacts"', "artifacts-subpath"),
    ('REPO_ROOT / "platform/src"', "src"),
    (' / "platform/src"', "src-subpath"),
    ('REPO_ROOT / "runtime/prepared-context"', "prepared-context"),
    ('REPO_ROOT / "skills"', "skills"),
    ('REPO_ROOT / "platform/apps"', "apps"),
]

ADOPTED_MARKERS = [
    "ARTIFACTS_DIR",
    "SRC_DIR",
    "PREPARED_CONTEXT_DIR",
    "SKILLS_DIR",
    "APPS_DIR",
    "BOT_DIR",
    "resolve_repo_path(",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Check repo path adoption")
    parser.add_argument(
        "--max-literals",
        type=int,
        default=120,
        help="Fail if legacy literal count exceeds this (default 120)",
    )
    args = parser.parse_args()

    literals = 0
    adopted = 0
    per_key: dict[str, int] = {k: 0 for _, k in LEGACY_LITERALS}

    for path in SCAN.rglob("*.py"):
        if not path.is_file() or path.name in SKIP:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for pat, key in LEGACY_LITERALS:
            n = text.count(pat)
            literals += n
            per_key[key] += n
        for pat in ADOPTED_MARKERS:
            adopted += text.count(pat)

    ratio = adopted / max(literals + adopted, 1)
    print(f"registry keys: {len(REPO_PATH_MIGRATIONS)}")
    print(f"legacy path literals: {literals}")
    for key, n in sorted(per_key.items(), key=lambda x: -x[1]):
        if n:
            print(f"  {key}: {n}")
    print(f"adopted markers (constants + resolve_repo_path): {adopted}")
    print(f"adoption ratio: {ratio:.1%}")

    if literals > args.max_literals:
        print(
            f"check_repo_path_adoption: FAIL ({literals} literals > max {args.max_literals})",
            file=sys.stderr,
        )
        print("Run: python scripts/adopt_repo_path_constants.py --apply", file=sys.stderr)
        return 1
    print("check_repo_path_adoption: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
