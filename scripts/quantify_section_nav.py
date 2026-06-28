#!/usr/bin/env python3
"""Quantify transcript sectioning navigation for a statecraft archive day."""
from __future__ import annotations

import argparse
import re
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "source-archive/statecraft"

MIN_SECTION_WARN = 100
MAX_SECTION_WARN = 1500
FLAT_NUDGE_WORDS = 4000
MAX_PARA_WARN = 150
SINGLE_PARA_MEGABLOCK = 200

SLUG_MARKERS = re.compile(r"^Segment \d+ —|^Show Open — Introduction$", re.I)
BODY_MARKERS = (
    r"## Transcript\s*\n",
    r"## Cleaned Transcript\s*\n",
    r"## Part I: Full transcript\s*\n",
)


def extract_transcript(body: str) -> str:
    for pattern in BODY_MARKERS:
        if m := re.search(pattern + r"(.*)", body, re.S):
            return m.group(1).strip()
    return body.strip()


def section_paragraph_stats(section_text: str) -> list[int]:
    paras = [p.strip() for p in re.split(r"\n\s*\n", section_text.strip()) if p.strip()]
    return [len(re.findall(r"\b\w+\b", p)) for p in paras]


def analyze(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    body = text.split("---", 2)[2] if text.startswith("---") else text
    transcript = extract_transcript(body)
    headings = re.findall(r"^### (.+)$", transcript, re.M)
    chunks = re.split(r"^### .+$", transcript, flags=re.M)
    chunks = [c.strip() for c in chunks if c.strip()]
    words = len(re.findall(r"\b\w+\b", transcript))
    sec_words = (
        [len(re.findall(r"\b\w+\b", c)) for c in chunks]
        if headings
        else [words]
    )
    curation = "none"
    if m := re.search(r"transcript_curation:\s*(\S+)", text):
        curation = m.group(1)
    slug_titles = sum(1 for h in headings if SLUG_MARKERS.search(h) or h.startswith("Segment "))
    warnings: list[str] = []
    if not headings and words >= FLAT_NUDGE_WORDS:
        warnings.append(f"flat body >= {FLAT_NUDGE_WORDS}w — nudge source-section outline")
    if slug_titles:
        warnings.append(f"{slug_titles} bootstrap slug title(s) — nudge thematic retitle")
    for i, w in enumerate(sec_words, start=1):
        if w < MIN_SECTION_WARN:
            warnings.append(f"section {i} < {MIN_SECTION_WARN}w ({w}w)")
        elif w > MAX_SECTION_WARN:
            warnings.append(f"section {i} > {MAX_SECTION_WARN}w ({w}w)")
    sec_para_counts: list[int] = []
    all_para_words: list[int] = []
    for i, chunk in enumerate(chunks, start=1):
        para_words = section_paragraph_stats(chunk)
        sec_para_counts.append(len(para_words))
        all_para_words.extend(para_words)
        if len(para_words) == 1 and para_words[0] > SINGLE_PARA_MEGABLOCK:
            warnings.append(
                f"section {i} single-paragraph megablock (>{SINGLE_PARA_MEGABLOCK}w, {para_words[0]}w)"
            )
        for j, pw in enumerate(para_words, start=1):
            if pw > MAX_PARA_WARN:
                warnings.append(f"section {i} para {j} > {MAX_PARA_WARN}w ({pw}w)")
    cv = 0.0
    if len(sec_words) > 1 and statistics.mean(sec_words):
        cv = 100 * statistics.pstdev(sec_words) / statistics.mean(sec_words)
    return {
        "file": path.name,
        "short": path.name.replace("source-", "")[:42],
        "curation": curation,
        "sections": len(headings),
        "words": words,
        "sec_words": sec_words,
        "sec_para_counts": sec_para_counts,
        "all_para_words": all_para_words,
        "slug_titles": slug_titles,
        "warnings": warnings,
        "chunk_cv": cv,
        "flat": len(headings) <= 1,
    }


def print_capture(r: dict) -> None:
    sw = r["sec_words"]
    print(f"{r['short']}")
    flat_tag = "FLAT" if r["flat"] else "SECTIONED"
    print(
        f"  {flat_tag}  sections={r['sections']}  words={r['words']}  "
        f"curation={r['curation']}"
    )
    if len(sw) > 1:
        print(
            f"  chunk words: min={min(sw)}  med={statistics.median(sw):.0f}  "
            f"mean={statistics.mean(sw):.0f}  max={max(sw)}  cv={r['chunk_cv']:.0f}%"
        )
    para_words = r.get("all_para_words") or []
    if para_words:
        print(
            f"  para words: min={min(para_words)}  med={statistics.median(para_words):.0f}  "
            f"max={max(para_words)}  paras={len(para_words)}"
        )
    if r["warnings"]:
        for w in r["warnings"]:
            print(f"  WARN: {w}")
    print()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--day", required=True, help="pub_date folder YYYY-MM-DD")
    parser.add_argument("--path", action="append", help="Single capture filename under day")
    args = parser.parse_args(argv)

    day_dir = ARCHIVE / args.day
    if not day_dir.is_dir():
        print(f"missing day folder: {day_dir}", file=sys.stderr)
        return 1

    if args.path:
        paths = [day_dir / name for name in args.path]
    else:
        paths = sorted(day_dir.glob("source-*.md"))

    rows = [analyze(p) for p in paths if p.is_file()]
    if not rows:
        print(f"no captures under {day_dir}")
        return 1

    print(f"=== SECTION NAV — {args.day} ===\n")
    for r in rows:
        print_capture(r)

    total_words = sum(r["words"] for r in rows)
    total_sections = sum(r["sections"] for r in rows)
    flat_count = sum(1 for r in rows if r["flat"])
    slug_count = sum(r["slug_titles"] for r in rows)
    all_sec = [w for r in rows for w in r["sec_words"]]
    sectioned = [r for r in rows if not r["flat"]]

    print("=== DAY SUMMARY ===")
    print(f"captures={len(rows)}  words={total_words}  headings={total_sections}")
    print(f"flat={flat_count}  sectioned={len(sectioned)}  slug_titles={slug_count}")
    if all_sec and len(all_sec) > len(rows):
        print(
            f"chunk: med={statistics.median(all_sec):.0f}w  max={max(all_sec)}w  "
            f"cv={100 * statistics.pstdev(all_sec) / statistics.mean(all_sec):.0f}%"
        )
    if sectioned:
        sec_words = sum(r["words"] for r in sectioned)
        sec_heads = sum(r["sections"] for r in sectioned)
        avg_file = sec_words / len(sectioned)
        avg_chunk = sec_words / sec_heads if sec_heads else avg_file
        scan_before = avg_file * 0.5
        scan_after = avg_chunk * 0.5
        reduction = 100 * (1 - scan_after / scan_before) if scan_before else 0
        print(
            f"navigation (sectioned only): {len(sectioned)} files -> {sec_heads} jumps; "
            f"~{reduction:.0f}% less expected random-topic scan vs monolith"
        )
    warn_files = [r["short"] for r in rows if r["warnings"]]
    if warn_files:
        print(f"files with warnings: {len(warn_files)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
