#!/usr/bin/env python3
"""Backfill prediction note frontmatter status from event registry."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from prediction_lib import (  # noqa: E402
    PREDICTIONS_DIR,
    expected_prediction_status,
    iter_prediction_note_paths,
    load_event_registry,
    parse_frontmatter_dict,
    repo_relative,
)

FRONTMATTER_RE = re.compile(r"\A(---\r?\n.*?\r?\n---\r?\n)", re.DOTALL)
STATUS_LINE_RE = re.compile(r"^status:\s*.+$", re.MULTILINE)

def _patch_frontmatter(text: str, status: str) -> str:
    match = FRONTMATTER_RE.match(text.lstrip("\ufeff"))
    if not match:
        raise ValueError("missing frontmatter")
    block = match.group(1)
    if STATUS_LINE_RE.search(block):
        new_block = STATUS_LINE_RE.sub(f"status: {status}", block, count=1)
    else:
        lines = block.splitlines()
        if len(lines) < 2 or lines[0] != "---":
            raise ValueError("invalid frontmatter fence")
        lines.insert(-1, f"status: {status}")
        new_block = "\n".join(lines) + ("\n" if not block.endswith("\n") else "")
    return text[: match.start()] + new_block + text[match.end() :]

def run_backfill(*, apply: bool = False, predictions_dir: Path | None = None) -> int:
    events = load_event_registry()
    root = predictions_dir or PREDICTIONS_DIR
    changed = 0
    skipped = 0

    for path in iter_prediction_note_paths(predictions_dir=root):
        rel = repo_relative(path)
        text = path.read_text(encoding="utf-8", errors="replace")
        data = parse_frontmatter_dict(text, feature=rel)
        if str(data.get("note_type") or "").strip() != "prediction":
            continue
        event_id = str(data.get("event_id") or "").strip()
        event = events.get(event_id)
        if event is None:
            print(f"[skip] {rel}: unknown event_id `{event_id}`", file=sys.stderr)
            skipped += 1
            continue
        event_status = str(event.get("status") or "open")
        status = expected_prediction_status(event_status)
        current = str(data.get("status") or "").strip()
        if current == status:
            continue
        new_text = _patch_frontmatter(text, status)
        changed += 1
        print(f"[{'apply' if apply else 'plan'}] {rel}: status -> {status}")
        if apply:
            path.write_text(new_text, encoding="utf-8", newline="\n")

    print(f"backfill_prediction_status: changed={changed} skipped={skipped}")
    return 0

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Write files (default: dry run)")
    args = parser.parse_args()
    return run_backfill(apply=args.apply)

if __name__ == "__main__":
    raise SystemExit(main())
