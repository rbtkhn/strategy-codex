#!/usr/bin/env python3
"""Falsify Jiang / Predictive History master-index totals against local sources."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MASTER_INDEX = REPO_ROOT / "statecraft" / "speakers" / "jiang" / "jiang-predictive-history-master-index.md"
MIRROR_CARDS = REPO_ROOT / "statecraft" / "speakers" / "jiang" / "ph-civ" / "data" / "cards.jsonl"
SOURCE_VIDEO_INDEX = REPO_ROOT / "statecraft" / "speakers" / "jiang" / "ph-civ" / "docs" / "source-video-index.md"
RAW_ARCHIVE_ROOT = REPO_ROOT / "source-archive" / "statecraft"

def count_public_cards() -> tuple[int, Counter[str]]:
    counts: Counter[str] = Counter()
    with MIRROR_CARDS.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            counts[obj.get("series", "unknown")] += 1
    return sum(counts.values()), counts

def count_source_video_rows() -> tuple[int, Counter[str]]:
    counts: Counter[str] = Counter()
    total = 0
    for line in SOURCE_VIDEO_INDEX.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| `"):
            continue
        total += 1
        if line.startswith("| `geo-"):
            counts["geo"] += 1
        elif line.startswith("| `gt-"):
            counts["gt"] += 1
        elif line.startswith("| `sh-"):
            counts["sh"] += 1
        elif line.startswith("| `civ-"):
            counts["civ"] += 1
        elif line.startswith("| `gb-"):
            counts["gb"] += 1
        elif line.startswith("| `int-"):
            counts["int"] += 1
    return total, counts

def count_raw_archive() -> tuple[int, Counter[str]]:
    counts: Counter[str] = Counter()
    for path in RAW_ARCHIVE_ROOT.rglob("*.md"):
        rel = path.relative_to(RAW_ARCHIVE_ROOT).as_posix()
        if rel.endswith("README.md") or rel.startswith("snippets/") or rel.startswith("_aired-pending/"):
            continue
        name = path.name
        if name.startswith("transcript-diesen-jiang-"):
            counts["interviews"] += 1
        elif name.startswith("predictive-history-game-theory-"):
            counts["gt"] += 1
        elif name.startswith("predictive-history-gb-"):
            counts["gb"] += 1
        elif name.startswith("substack-predictive-history-"):
            counts["essays"] += 1
    return sum(counts.values()), counts

def expected_counts_from_master() -> dict[str, int]:
    text = MASTER_INDEX.read_text(encoding="utf-8")
    checks = {
        "public_total": r"Public mirror corpus \| .* \| `(\d+)` \|",
        "source_video_total": r"Public source-video table \| .* \| `(\d+)` \|",
        "raw_total": r"Local raw archive captures \| .* \| `(\d+)` \|",
        "civilization": r"\| Civilization \| `(\d+)` \| .*volume-ii",
        "geo_strategy": r"\| Geo-Strategy \| `(\d+)` \| .*volume-i",
        "game_theory": r"\| Game Theory \| `(\d+)` \| .*volume-iii",
        "secret_history": r"\| Secret History \| `(\d+)` \| .*volume-vi",
        "great_books": r"\| Great Books \| `(\d+)` \| .*volume-v",
        "essays": r"\| Essays \| `(\d+)` \| .*ph-apo",
        "source_geo": r"\| Geo-Strategy \| `(\d+)` \| .*source-video-index",
        "source_gt": r"\| Game Theory \| `(\d+)` \| .*source-video-index",
        "source_sh": r"\| Secret History \| `(\d+)` \| .*source-video-index",
        "raw_interviews": r"\| Interviews \| `(\d+)` \| .*jiang-predictive-history-index",
        "raw_gt": r"\| Game Theory \| `(\d+)` \| .*jiang-predictive-history-index",
        "raw_gb": r"\| Great Books \| `(\d+)` \| .*jiang-predictive-history-index",
        "raw_essays": r"\| Essays \| `(\d+)` \| .*jiang-predictive-history-index",
    }
    result: dict[str, int] = {}
    for key, pattern in checks.items():
        match = re.search(pattern, text)
        if not match:
            raise RuntimeError(f"could not find expected count for {key} in master index")
        result[key] = int(match.group(1))
    return result

def main() -> int:
    expected = expected_counts_from_master()
    public_total, public_counts = count_public_cards()
    source_total, source_counts = count_source_video_rows()
    raw_total, raw_counts = count_raw_archive()

    actual = {
        "public_total": public_total,
        "source_video_total": source_total,
        "raw_total": raw_total,
        "civilization": public_counts.get("civilization", 0),
        "geo_strategy": public_counts.get("geo-strategy", 0),
        "game_theory": public_counts.get("game-theory", 0),
        "secret_history": public_counts.get("secret-history", 0),
        "great_books": public_counts.get("great-books", 0),
        "essays": public_counts.get("essays", 0),
        "source_geo": source_counts.get("geo", 0),
        "source_gt": source_counts.get("gt", 0),
        "source_sh": source_counts.get("sh", 0),
        "raw_interviews": raw_counts.get("interviews", 0),
        "raw_gt": raw_counts.get("gt", 0),
        "raw_gb": raw_counts.get("gb", 0),
        "raw_essays": raw_counts.get("essays", 0),
    }

    mismatches: list[str] = []
    for key, expected_value in expected.items():
        actual_value = actual.get(key)
        if actual_value != expected_value:
            mismatches.append(f"{key}: expected {expected_value}, got {actual_value}")

    print("Jiang / Predictive History index check")
    print(f"public_total={public_total}")
    print(f"source_video_total={source_total}")
    print(f"raw_total={raw_total}")
    print(
        "public_series="
        f"civilization:{actual['civilization']} "
        f"geo-strategy:{actual['geo_strategy']} "
        f"game-theory:{actual['game_theory']} "
        f"secret-history:{actual['secret_history']} "
        f"great-books:{actual['great_books']} "
        f"essays:{actual['essays']}"
    )
    print(
        "source_video_series="
        f"geo:{actual['source_geo']} "
        f"gt:{actual['source_gt']} "
        f"sh:{actual['source_sh']}"
    )
    print(
        "raw_archive_series="
        f"interviews:{actual['raw_interviews']} "
        f"gt:{actual['raw_gt']} "
        f"gb:{actual['raw_gb']} "
        f"essays:{actual['raw_essays']}"
    )

    if mismatches:
        print("status=failed")
        for mismatch in mismatches:
            print(mismatch)
        return 1

    print("status=ok")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
