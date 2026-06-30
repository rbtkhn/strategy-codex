#!/usr/bin/env python3
"""Merge a statecraft source-archive header plus body sidecar(s) into one file.

Use when operator-pasted transcript bodies are large enough that a single IDE
Write to source-archive/ can hang on Windows harnesses. See statecraft-source-intake
§ Large transcript body land.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def merge(header_path: Path, body_paths: list[Path], out_path: Path, dry_run: bool) -> int:
    if not header_path.is_file():
        print(f"error: header not found: {header_path}", file=sys.stderr)
        return 1
    for bp in body_paths:
        if not bp.is_file():
            print(f"error: body sidecar not found: {bp}", file=sys.stderr)
            return 1

    header = _read_text(header_path)
    if not header.endswith("\n"):
        header += "\n"

    body_parts: list[str] = []
    for bp in body_paths:
        chunk = _read_text(bp).strip()
        if chunk:
            body_parts.append(chunk)
    body = "\n\n".join(body_parts)
    if body and not body.endswith("\n"):
        body += "\n"

    merged = header + body
    body_chars = len(body)
    total_bytes = len(merged.encode("utf-8"))

    if dry_run:
        print(f"dry-run: would write {out_path}")
        print(f"  header: {header_path} ({header_path.stat().st_size} bytes)")
        for bp in body_paths:
            print(f"  body:   {bp} ({bp.stat().st_size} bytes)")
        print(f"  body_chars={body_chars} total_bytes={total_bytes}")
        return 0

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(merged, encoding="utf-8")
    print(f"wrote {out_path} ({total_bytes} bytes, body_chars={body_chars})")
    return 0

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Merge statecraft source-archive header + body sidecars into one capture file."
    )
    parser.add_argument(
        "--header",
        required=True,
        type=Path,
        help="Path to header file: YAML frontmatter + markdown through ## Transcript (inclusive).",
    )
    parser.add_argument(
        "--body",
        action="append",
        default=[],
        type=Path,
        help="Body sidecar path; repeat for p1, p2, … (concatenated in order).",
    )
    parser.add_argument(
        "--body-dir",
        type=Path,
        help="Directory of body sidecars; uses sorted *.txt files when --body is omitted.",
    )
    parser.add_argument("--out", required=True, type=Path, help="Canonical archive output path.")
    parser.add_argument("--dry-run", action="store_true", help="Print merge plan without writing.")
    args = parser.parse_args()

    body_paths: list[Path] = list(args.body)
    if args.body_dir:
        if body_paths:
            print("error: use --body or --body-dir, not both", file=sys.stderr)
            return 1
        body_paths = sorted(args.body_dir.glob("*.txt"))
        if not body_paths:
            print(f"error: no *.txt in {args.body_dir}", file=sys.stderr)
            return 1
    if not body_paths:
        print("error: at least one --body or a non-empty --body-dir is required", file=sys.stderr)
        return 1

    return merge(args.header, body_paths, args.out, args.dry_run)

if __name__ == "__main__":
    raise SystemExit(main())
