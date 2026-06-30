#!/usr/bin/env python3
"""Promote YouTube watch URLs from capture frontmatter notes into source_url YAML."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PREDICTIONS_JSON = REPO_ROOT / "statecraft" / "voices" / "freeman" / "freeman-predictions.json"
YT = re.compile(r"https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([\w-]+)")


def extract_watch_url(text: str) -> str | None:
    m = YT.search(text)
    if not m:
        return None
    vid = m.group(1)
    return f"https://www.youtube.com/watch?v={vid}"


def patch_capture(path: Path, *, dry_run: bool = False) -> bool:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return False
    parts = text.split("---", 2)
    if len(parts) < 3:
        return False
    fm, body = parts[1], parts[2]
    if re.search(r"^source_url:\s*https?://", fm, re.M):
        return False
    url = extract_watch_url(fm) or extract_watch_url(body[:5000])
    if not url:
        return False
    if re.search(r"^source_url:", fm, re.M):
        new_fm = re.sub(r"^source_url:\s*.+$", f'source_url: "{url}"', fm, flags=re.M)
    else:
        new_fm = fm.rstrip() + f'\nsource_url: "{url}"\n'
    new_text = "---" + new_fm + "---" + body
    if dry_run:
        print(f"[dry-run] would patch {path.relative_to(REPO_ROOT)} -> {url}")
        return True
    path.write_text(new_text, encoding="utf-8", newline="\n")
    print(f"[ok] patched {path.relative_to(REPO_ROOT)}")
    return True


def main() -> int:
    dry_run = "--dry-run" in sys.argv
    data = json.loads(PREDICTIONS_JSON.read_text(encoding="utf-8"))
    captures = sorted(
        {tp["capture"] for ev in data["events"] for tp in ev["touchpoints"]}
    )
    patched = 0
    for rel in captures:
        path = REPO_ROOT / rel.replace("\\", "/")
        if path.is_file() and patch_capture(path, dry_run=dry_run):
            patched += 1
    print(f"{'would patch' if dry_run else 'patched'} {patched} capture(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
