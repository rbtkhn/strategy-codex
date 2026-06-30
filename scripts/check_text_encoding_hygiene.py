#!/usr/bin/env python3
"""Detect mojibake and text-encoding artifacts in continuity-layer markdown."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

MOJIBAKE_PATTERNS = (
    "Ãƒ",
    "Ã¢",
    "Ã‚",
    "â€™",
    "â€œ",
    "â€�",
    "ÃƒÆ'",
    "Ã¢â‚¬",
)


@dataclass
class EncodingMatch:
    path: str
    line: int
    pattern: str
    context: str


from continuity_paths import continuity_root as _continuity_root


def _continuity_scope_root(repo_root: Path, scope: str) -> Path | None:
    if scope == "continuity":
        p = repo_root / "continuity"
        return p if p.is_dir() else None
    if scope == "codex":
        return _continuity_root(repo_root) if (repo_root / "codex").is_dir() else None
    raise ValueError(f"unknown scope: {scope}")


def scan_tree(root: Path, repo_root: Path) -> list[EncodingMatch]:
    matches: list[EncodingMatch] = []
    if not root.is_dir():
        return matches
    for path in sorted(root.rglob("*.md")):
        rel = path.relative_to(repo_root).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for line_no, line in enumerate(text.splitlines(), start=1):
            for pat in MOJIBAKE_PATTERNS:
                if pat in line:
                    matches.append(
                        EncodingMatch(
                            path=rel,
                            line=line_no,
                            pattern=pat,
                            context=line.strip()[:100],
                        )
                    )
                    break
    return matches


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--scope",
        choices=("codex", "continuity"),
        default="codex",
        help="Tree to scan (default codex during pre-move)",
    )
    parser.add_argument("--strict", action="store_true", help="Exit 1 when matches found")
    parser.add_argument("--warn", action="store_true", help="Report matches but exit 0")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = _continuity_scope_root(REPO_ROOT, args.scope)
    if root is None:
        print(f"scope {args.scope}: directory missing", file=sys.stderr)
        return 0 if args.warn else 1

    matches = scan_tree(root, REPO_ROOT)

    if args.json:
        print(json.dumps({"scope": args.scope, "matches": [asdict(m) for m in matches]}, indent=2))
    elif matches:
        print(f"encoding hygiene ({args.scope}): {len(matches)} match(es)", file=sys.stderr)
        for m in matches[:20]:
            print(f"  {m.path}:{m.line} [{m.pattern}]", file=sys.stderr)
        if len(matches) > 20:
            print(f"  ... and {len(matches) - 20} more", file=sys.stderr)
    else:
        print(f"encoding hygiene ({args.scope}): clean", file=sys.stderr)

    if matches and args.strict:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
