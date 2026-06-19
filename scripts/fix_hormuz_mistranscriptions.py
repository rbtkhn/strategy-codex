from repo_io import ARTIFACTS_DIR
#!/usr/bin/env python3
"""Apply high-confidence Strait of Hormuz transcript fixes from an audit artifact.

WORK only; not Record.

This is a bounded repair pass: it only modifies files named in the audit JSON
and only applies high-confidence phrase-shaped replacements for direct
transcript body mistranscriptions.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_AUDIT_JSON = ARTIFACTS_DIR / "transcript-audits" / "statecraft-hormuz-mistranscriptions-2026-06-01.json"


@dataclass(frozen=True)
class ReplacementSpec:
    pattern: re.Pattern[str]
    replacement: str
    label: str


REPLACEMENT_SPECS: tuple[ReplacementSpec, ...] = (
    ReplacementSpec(re.compile(r"\bstraits of\s+homus\b", re.IGNORECASE), "Straits of Hormuz", "straits_of_homus"),
    ReplacementSpec(re.compile(r"\bstraits of\s+hormuse\b", re.IGNORECASE), "Straits of Hormuz", "straits_of_hormuse"),
    ReplacementSpec(re.compile(r"\bstraits of\s+hermuz\b", re.IGNORECASE), "Straits of Hormuz", "straits_of_hermuz"),
    ReplacementSpec(re.compile(r"\bstraight of\s+hormones\b", re.IGNORECASE), "Strait of Hormuz", "straight_of_hormones"),
    ReplacementSpec(re.compile(r"\bstraight of\s+hormone\b", re.IGNORECASE), "Strait of Hormuz", "straight_of_hormone"),
    ReplacementSpec(re.compile(r"\bstraight of\s+humus\b", re.IGNORECASE), "Strait of Hormuz", "straight_of_humus"),
    ReplacementSpec(re.compile(r"\bstraight of\s+hormuse\b", re.IGNORECASE), "Strait of Hormuz", "straight_of_hormuse"),
    ReplacementSpec(re.compile(r"\bstraight of\s+hermuz\b", re.IGNORECASE), "Strait of Hormuz", "straight_of_hermuz"),
    ReplacementSpec(re.compile(r"\bstraight of\s+hermus\b", re.IGNORECASE), "Strait of Hormuz", "straight_of_hermus"),
    ReplacementSpec(re.compile(r"\bstraight of\s+hormos\b", re.IGNORECASE), "Strait of Hormuz", "straight_of_hormos"),
    ReplacementSpec(re.compile(r"\bstraight of\s+homus\b", re.IGNORECASE), "Strait of Hormuz", "straight_of_homus"),
    ReplacementSpec(re.compile(r"\bstraight of\s+harmuz\b", re.IGNORECASE), "Strait of Hormuz", "straight_of_harmuz"),
    ReplacementSpec(re.compile(r"\bstraight of\s+armus\b", re.IGNORECASE), "Strait of Hormuz", "straight_of_armus"),
    ReplacementSpec(re.compile(r"\bstraight of\s+armoose\b", re.IGNORECASE), "Strait of Hormuz", "straight_of_armoose"),
    ReplacementSpec(re.compile(r"\bstraight of\s+foremost\b", re.IGNORECASE), "Strait of Hormuz", "straight_of_foremost"),
    ReplacementSpec(re.compile(r"\bstraight of\s+formos\b", re.IGNORECASE), "Strait of Hormuz", "straight_of_formos"),
    ReplacementSpec(re.compile(r"\bstraight of\s+barmuz\b", re.IGNORECASE), "Strait of Hormuz", "straight_of_barmuz"),
    ReplacementSpec(re.compile(r"\bstreet of\s+hormones\b", re.IGNORECASE), "Strait of Hormuz", "street_of_hormones"),
    ReplacementSpec(re.compile(r"\bstreet of\s+humus\b", re.IGNORECASE), "Strait of Hormuz", "street_of_humus"),
    ReplacementSpec(re.compile(r"\bstreet of\s+hormos\b", re.IGNORECASE), "Strait of Hormuz", "street_of_hormos"),
    ReplacementSpec(re.compile(r"\bstreet of\s+hermuz\b", re.IGNORECASE), "Strait of Hormuz", "street_of_hermuz"),
    ReplacementSpec(re.compile(r"\bstreet\s+hermuz\b", re.IGNORECASE), "Strait of Hormuz", "street_hermuz"),
    ReplacementSpec(re.compile(r"\bstreet of\s+ormuz\b", re.IGNORECASE), "Strait of Hormuz", "street_of_ormuz"),
    ReplacementSpec(re.compile(r"\bstreet of\s+armors\b", re.IGNORECASE), "Strait of Hormuz", "street_of_armors"),
    ReplacementSpec(re.compile(r"\bstrait of\s+humus\b", re.IGNORECASE), "Strait of Hormuz", "strait_of_humus"),
    ReplacementSpec(re.compile(r"\bstrait of\s+hermuz\b", re.IGNORECASE), "Strait of Hormuz", "strait_of_hermuz"),
    ReplacementSpec(re.compile(r"\bstate of\s+homus\b", re.IGNORECASE), "Strait of Hormuz", "state_of_homus"),
    ReplacementSpec(re.compile(r"\bstate of\s+hormos\b", re.IGNORECASE), "Strait of Hormuz", "state_of_hormos"),
    ReplacementSpec(re.compile(r"\bstate of\s+armus\b", re.IGNORECASE), "Strait of Hormuz", "state_of_armus"),
    ReplacementSpec(re.compile(r"\bstate of\s+formos\b", re.IGNORECASE), "Strait of Hormuz", "state_of_formos"),
    ReplacementSpec(re.compile(r"\bstrait of\s+armus\b", re.IGNORECASE), "Strait of Hormuz", "strait_of_armus"),
    ReplacementSpec(re.compile(r"\bstrait of\s+ormuz\b", re.IGNORECASE), "Strait of Hormuz", "strait_of_ormuz"),
    ReplacementSpec(re.compile(r"\bstrait of\s+hormos\b", re.IGNORECASE), "Strait of Hormuz", "strait_of_hormos"),
    ReplacementSpec(re.compile(r"\bstraits of\s+armoose\b", re.IGNORECASE), "Straits of Hormuz", "straits_of_armoose"),
    ReplacementSpec(re.compile(r"\btrade of\s+humus\b", re.IGNORECASE), "Strait of Hormuz", "trade_of_humus"),
    ReplacementSpec(re.compile(r"\btrade of\s+hormones\b", re.IGNORECASE), "Strait of Hormuz", "trade_of_hormones"),
    ReplacementSpec(re.compile(r"\btrade of\s+hermuz\b", re.IGNORECASE), "Strait of Hormuz", "trade_of_hermuz"),
    ReplacementSpec(re.compile(r"\btrade of\s+foremost\b", re.IGNORECASE), "Strait of Hormuz", "trade_of_foremost"),
    ReplacementSpec(re.compile(r"\btrade of\s+hormos\b", re.IGNORECASE), "Strait of Hormuz", "trade_of_hormos"),
    ReplacementSpec(re.compile(r"\btrade of\s+formos\b", re.IGNORECASE), "Strait of Hormuz", "trade_of_formos"),
    ReplacementSpec(re.compile(r"\bstraight of\s*\n\s*hormones\b", re.IGNORECASE), "Strait of Hormuz", "split_straight_of_hormones"),
    ReplacementSpec(re.compile(r"\bstraight of\s*\n\s*hormone\b", re.IGNORECASE), "Strait of Hormuz", "split_straight_of_hormone"),
    ReplacementSpec(re.compile(r"\bstraight of\s*\n\s*humus\b", re.IGNORECASE), "Strait of Hormuz", "split_straight_of_humus"),
    ReplacementSpec(re.compile(r"\bstraight of\s*\n\s*hormos\b", re.IGNORECASE), "Strait of Hormuz", "split_straight_of_hormos"),
    ReplacementSpec(re.compile(r"\bstraight of\s*\n\s*homus\b", re.IGNORECASE), "Strait of Hormuz", "split_straight_of_homus"),
    ReplacementSpec(re.compile(r"\bstraight of\s*\n\s*foremost\b", re.IGNORECASE), "Strait of Hormuz", "split_straight_of_foremost"),
    ReplacementSpec(re.compile(r"\bstraight of\s*\n\s*formos\b", re.IGNORECASE), "Strait of Hormuz", "split_straight_of_formos"),
    ReplacementSpec(re.compile(r"\btrade of\s*\n\s*foremost\b", re.IGNORECASE), "Strait of Hormuz", "split_trade_of_foremost"),
)


def load_target_paths(audit_json: Path) -> list[Path]:
    payload = json.loads(audit_json.read_text(encoding="utf-8"))
    paths = {
        REPO_ROOT / row["path"]
        for row in payload.get("findings", [])
        if row.get("tier") == "high_confidence" and row.get("match_text")
    }
    return sorted(paths)


def apply_replacements(text: str) -> tuple[str, Counter[str]]:
    counts: Counter[str] = Counter()
    for spec in REPLACEMENT_SPECS:
        text, n = spec.pattern.subn(spec.replacement, text)
        if n:
            counts[spec.label] += n
    return text, counts


def fix_paths(paths: Iterable[Path], *, write: bool) -> dict[str, object]:
    changed_files = 0
    total_replacements: Counter[str] = Counter()
    file_rows: list[dict[str, object]] = []
    for path in paths:
        original = path.read_text(encoding="utf-8", errors="replace")
        updated, counts = apply_replacements(original)
        if not counts:
            continue
        changed_files += 1
        total_replacements.update(counts)
        file_rows.append(
            {
                "path": str(path.relative_to(REPO_ROOT)).replace("\\", "/"),
                "replacements": dict(counts),
            }
        )
        if write:
            path.write_text(updated, encoding="utf-8", newline="\n")
    return {
        "changed_files": changed_files,
        "replacement_counts": dict(total_replacements),
        "files": file_rows,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit-json", type=Path, default=DEFAULT_AUDIT_JSON, help="Audit JSON artifact to source high-confidence targets from.")
    parser.add_argument("--write", action="store_true", help="Write fixes in place. Omit for dry run.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    paths = load_target_paths(args.audit_json.resolve())
    result = fix_paths(paths, write=args.write)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
