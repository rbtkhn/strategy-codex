#!/usr/bin/env python3
"""One-off inventory: May 2026 Mario Nawfal capture section status."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def scan(path: Path) -> dict | None:
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        return None
    head = text.split("---", 2)[1]
    slug_m = re.search(r"^channel_slug:\s*(\S+)", head, re.M)
    slug = slug_m.group(1) if slug_m else ""
    show_m = re.search(r"^show:\s*(.+)$", head, re.M)
    show = show_m.group(1).strip() if show_m else ""
    is_nawfal = (
        slug == "mario-nawfal"
        or show == "Mario Nawfal"
        or "mario-nawfal" in path.name.lower()
    )
    if not is_nawfal:
        return None
    if path.name.endswith(".cleaned.md"):
        return None

    tc_m = re.search(r"^transcript_curation:\s*(\S+)", head, re.M)
    tc = tc_m.group(1) if tc_m else ""
    gp_m = re.search(r"^guest_people:\n((?:  - .+\n)+)", head, re.M)
    guests: list[str] = []
    if gp_m:
        guests = re.findall(r"^  - (.+)$", gp_m.group(1), re.M)
    if not guests:
        g_m = re.search(r"^guest:\s*(.+)$", head, re.M)
        if g_m:
            guests = [g_m.group(1).strip()]
    yt_m = re.search(r"^youtube_id:\s*(\S+)", head, re.M)
    pub_m = re.search(r"^pub_date:\s*(\S+)", head, re.M)

    body = ""
    if "## Transcript" in text:
        body = text.split("## Transcript", 1)[1]
    elif text.startswith("---"):
        tail = text.split("---", 2)[2]
        body = tail.split("\n", 1)[1] if tail.startswith("\n#") else tail
    n_h3 = len(re.findall(r"^### ", body, re.M))
    words = len(body.split())
    status = "sectioned" if tc == "curated_sectioned" or n_h3 >= 3 else "flat"

    return {
        "pub": pub_m.group(1) if pub_m else path.parent.name,
        "guest": guests[0] if guests else "?",
        "status": status,
        "sections": n_h3,
        "words": words,
        "yt": yt_m.group(1) if yt_m else "",
        "name": path.name,
    }

def main() -> None:
    rows: list[dict] = []
    for d in sorted(ROOT.glob("source-archive/statecraft/2026-05-*")):
        if not d.is_dir():
            continue
        for p in sorted(d.glob("source-*.md")):
            r = scan(p)
            if r:
                rows.append(r)

    sectioned = [r for r in rows if r["status"] == "sectioned"]
    flat = [r for r in rows if r["status"] == "flat"]

    print(f"May Nawfal captures: {len(rows)} total | sectioned {len(sectioned)} | flat {len(flat)}")
    print("\nSECTIONED")
    for r in sectioned:
        print(f"  {r['pub']}  {r['guest'][:32]:32}  {r['sections']}sec  {r['yt'] or 'no-id'}  {r['name']}")
    print("\nFLAT")
    for r in flat:
        print(f"  {r['pub']}  {r['guest'][:32]:32}  {r['words']:5}w  {r['yt'] or 'no-id'}  {r['name']}")

if __name__ == "__main__":
    main()
