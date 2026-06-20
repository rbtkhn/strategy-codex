#!/usr/bin/env python3
"""QA checker for CIV-STATE civic-chain essay prose (Rome v0.2 bands)."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

SCHEMATIC_BAN = re.compile(
    r"\b(grammar|hinge|apparatus|sequence|strain|logic|stacks|substrate|"
    r"nullification|machinery|shell|smaller world)\b",
    re.I,
)

# proof excluded from ban — earned narrative use allowed

MODERN_FAIL = re.compile(
    r"\b(Syme|Goldsworthy|Everitt|Durant)\b",
    re.I,
)

RECEPTION_ALLOW = re.compile(
    r"\b(Gibbon|Mommsen)\b",
    re.I,
)

QUOTE_RE = re.compile(r'"([^"]+)"')

ROME_CIVIC_CHAIN_FOUR = [
    "public/civ-state/volumes/rome/essays/essay-rome-genesis.md",
    "public/civ-state/volumes/rome/essays/essay-rome-republic.md",
    "public/civ-state/volumes/rome/essays/essay-rome-caesar.md",
    "public/civ-state/volumes/rome/essays/essay-rome-augustus.md",
]

BANDS = {
    "civic-chain-rome-v2": {
        "body_min": 2400,
        "body_max": 2600,
        "quoted_min": 450,
        "quoted_max": 550,
    },
}


def split_body(text: str) -> str:
    if "## Notes" in text:
        return text.split("## Notes", 1)[0]
    return text


def word_count(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


def quoted_words(body: str) -> tuple[int, list[str]]:
    segments = QUOTE_RE.findall(body)
    total = sum(word_count(s) for s in segments)
    return total, segments


def schematic_hits(body: str) -> list[tuple[int, str]]:
    hits: list[tuple[int, str]] = []
    for i, line in enumerate(body.splitlines(), 1):
        if SCHEMATIC_BAN.search(line):
            hits.append((i, line.strip()[:120]))
    return hits


def outside_quotes(text: str) -> str:
    """Remove quoted segments for surname grep."""
    return QUOTE_RE.sub("", text)


def modern_surname_violations(body: str) -> list[str]:
    outside = outside_quotes(body)
    fails = MODERN_FAIL.findall(outside)
    # Gibbon/Mommsen only allowed inside quotes
    for name in RECEPTION_ALLOW.findall(outside):
        fails.append(f"{name} (outside quotes)")
    return fails


def footnote_refs(body: str) -> set[str]:
    return set(re.findall(r"\[\^(\d+)\]", body))


def footnote_defs(notes: str) -> set[str]:
    return set(re.findall(r"\[\^(\d+)\]:", notes))


def check_file(path: Path, band_key: str) -> dict:
    text = path.read_text(encoding="utf-8")
    body = split_body(text)
    notes = text.split("## Notes", 1)[1] if "## Notes" in text else ""
    bands = BANDS[band_key]

    bw = word_count(body)
    qw, quote_segments = quoted_words(body)
    aw = bw - qw
    qpct = (qw / bw * 100) if bw else 0.0

    sch = schematic_hits(body)
    mod = modern_surname_violations(body)
    refs = footnote_refs(body)
    defs = footnote_defs(notes)
    orphan_refs = refs - defs

    errors: list[str] = []
    if bw < bands["body_min"] or bw > bands["body_max"]:
        errors.append(f"body_words={bw} (want {bands['body_min']}–{bands['body_max']})")
    if qw < bands["quoted_min"] or qw > bands["quoted_max"]:
        errors.append(f"quoted_words={qw} (want {bands['quoted_min']}–{bands['quoted_max']})")
    if sch:
        errors.append(f"schematic_hits={len(sch)}")
    if mod:
        errors.append(f"modern_surname_violations={mod}")
    if orphan_refs:
        errors.append(f"unresolved_footnotes={sorted(orphan_refs, key=int)}")

    return {
        "path": str(path),
        "body_words": bw,
        "quoted_words": qw,
        "authorial_words": aw,
        "quote_pct": round(qpct, 1),
        "quote_count": len(quote_segments),
        "schematic_hits": sch,
        "modern_violations": mod,
        "errors": errors,
        "ok": not errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check CIV-STATE civic-chain essay prose bands.")
    parser.add_argument("--path", action="append", dest="paths", help="Essay path (repeatable)")
    parser.add_argument(
        "--rome-civic-chain-four",
        action="store_true",
        help="Check Rome genesis–augustus civic-chain four",
    )
    parser.add_argument(
        "--class",
        dest="band_class",
        default="civic-chain-rome-v2",
        choices=list(BANDS.keys()),
        help="Band profile (default: civic-chain-rome-v2)",
    )
    args = parser.parse_args()

    paths: list[Path] = []
    if args.rome_civic_chain_four:
        paths.extend(REPO_ROOT / p for p in ROME_CIVIC_CHAIN_FOUR)
    for p in args.paths or []:
        paths.append(Path(p) if Path(p).is_absolute() else REPO_ROOT / p)

    if not paths:
        parser.error("Provide --path and/or --rome-civic-chain-four")

    any_fail = False
    for path in paths:
        if not path.is_file():
            print(f"FAIL {path}: file not found", file=sys.stderr)
            any_fail = True
            continue
        r = check_file(path, args.band_class)
        status = "OK" if r["ok"] else "FAIL"
        print(
            f"{status} {path.name}: body={r['body_words']} quoted={r['quoted_words']} "
            f"({r['quote_pct']}%) authorial={r['authorial_words']} quotes={r['quote_count']}"
        )
        if r["schematic_hits"]:
            for ln, text in r["schematic_hits"][:8]:
                print(f"  schematic L{ln}: {text}")
        if r["modern_violations"]:
            print(f"  modern: {r['modern_violations']}")
        for e in r["errors"]:
            print(f"  {e}")
        if not r["ok"]:
            any_fail = True

    return 1 if any_fail else 0


if __name__ == "__main__":
    sys.exit(main())
