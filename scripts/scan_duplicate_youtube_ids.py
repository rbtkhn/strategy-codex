#!/usr/bin/env python3
"""Scan statecraft archive for duplicate youtube_id / source_url video IDs."""

from __future__ import annotations

import argparse
import re
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ARCHIVE_ROOT = REPO_ROOT / "source-archive" / "statecraft"
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)
YT_RE = re.compile(r"(?:youtube\.com/watch\?v=|youtu\.be/)([A-Za-z0-9_-]{11})")
STUB_BYTES = 400


def parse_scalar(block: str, key: str) -> str | None:
    m = re.search(rf"^{re.escape(key)}:\s*(.+)$", block, re.M)
    if not m:
        return None
    val = m.group(1).strip().strip('"').strip("'")
    return val or None


def youtube_id_from_block(block: str) -> str | None:
    yt = parse_scalar(block, "youtube_id")
    if yt and yt.lower() not in {"null", "none", "tbd", "?"}:
        return yt
    for key in ("source_url", "canonical_url"):
        val = parse_scalar(block, key)
        if not val:
            continue
        m = YT_RE.search(val)
        if m:
            return m.group(1)
    return None


def body_byte_len(text: str) -> int:
    m = FRONTMATTER_RE.match(text)
    body = text[m.end() :] if m else text
    return len(body.strip())


def collect(root: Path) -> dict[str, list[dict]]:
    by_id: dict[str, list[dict]] = defaultdict(list)
    for path in sorted(root.rglob("source-*.md")):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        m = FRONTMATTER_RE.match(text)
        block = m.group(1) if m else ""
        yt = youtube_id_from_block(block)
        if not yt:
            continue
        blen = body_byte_len(text)
        by_id[yt].append(
            {
                "path": path.relative_to(root).as_posix(),
                "pub_date": parse_scalar(block, "pub_date") or "?",
                "body": blen,
                "stub": blen < STUB_BYTES,
                "channel_slug": parse_scalar(block, "channel_slug") or "",
            }
        )
    return by_id


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--min-files", type=int, default=2)
    parser.add_argument("--show-ok", action="store_true", help="Include same-day renames")
    args = parser.parse_args()

    by_id = collect(ARCHIVE_ROOT)
    dups = {k: v for k, v in by_id.items() if len(v) >= args.min_files}

    print(f"captures_with_youtube_id={sum(len(v) for v in by_id.values())}")
    print(f"distinct_youtube_ids={len(by_id)}")
    print(f"duplicate_youtube_ids={len(dups)}")
    print("---")

    for yt in sorted(dups, key=lambda k: (-len(dups[k]), k)):
        rows = dups[yt]
        pubs = {r["pub_date"] for r in rows}
        stubs = sum(1 for r in rows if r["stub"])
        flag = []
        if len(pubs) > 1:
            flag.append("cross-day")
        if stubs and stubs < len(rows):
            flag.append("stub+body")
        if stubs == len(rows):
            flag.append("all-stub")
        tag = f" [{', '.join(flag)}]" if flag else ""
        print(f"{yt} ({len(rows)} files){tag}")
        for r in sorted(rows, key=lambda x: x["path"]):
            kind = "STUB" if r["stub"] else f"{r['body']}b"
            slug = f" slug={r['channel_slug']}" if r["channel_slug"] else ""
            print(f"  {r['path']} | pub={r['pub_date']} | {kind}{slug}")
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
