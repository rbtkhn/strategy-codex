"""Scrub mojibake from skill markdown files."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import ftfy
except ModuleNotFoundError:  # pragma: no cover
    ftfy = None  # type: ignore

MOJIBAKE_MARKERS = ("Ãƒ", "Ã¢", "â€", "Ã‚", "Ã†", "Ã¢â‚¬", "ÃƒÆ")


def latin_roundtrip(text: str, *, rounds: int = 4) -> str:
    current = text
    for _ in range(rounds):
        try:
            nxt = current.encode("latin-1").decode("utf-8")
        except UnicodeError:
            break
        if nxt == current:
            break
        current = nxt
    return current


def fix_mojibake(text: str) -> str:
    if ftfy is not None:
        text = ftfy.fix_text(text)
    text = latin_roundtrip(text)
    if ftfy is not None:
        text = ftfy.fix_text(text)
    # Strip control chars that break YAML tooling.
    text = text.replace("\u009d", "")
    return text


def marker_count(text: str) -> int:
    return sum(text.count(m) for m in MOJIBAKE_MARKERS)


def control_char_issues(text: str) -> list[str]:
    """Return human-readable control-char findings (frontmatter-weighted)."""
    issues: list[str] = []
    if "\u009d" in text:
        issues.append("U+009D control character present")
    for i, ch in enumerate(text):
        o = ord(ch)
        if o < 32 and ch not in "\n\r\t":
            issues.append(f"control character U+{o:04X} at offset {i}")
            if len(issues) >= 3:
                break
    return issues


def scrub_file(path: Path, *, dry_run: bool) -> tuple[int, int]:
    original = path.read_text(encoding="utf-8")
    before = marker_count(original)
    fixed = fix_mojibake(original)
    after = marker_count(fixed)
    if not dry_run and fixed != original:
        path.write_text(fixed, encoding="utf-8", newline="\n")
    return before, after


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if ftfy is None:
        print("warning: ftfy not installed; using latin roundtrip only", file=sys.stderr)

    exit_code = 0
    for path in args.paths:
        if not path.exists():
            print(f"missing: {path}", file=sys.stderr)
            exit_code = 1
            continue
        before, after = scrub_file(path, dry_run=args.dry_run)
        action = "would scrub" if args.dry_run else "scrubbed"
        print(f"{action} {path}: markers {before} -> {after}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
