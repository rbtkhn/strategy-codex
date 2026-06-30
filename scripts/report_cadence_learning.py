#!/usr/bin/env python3
"""Read-only markdown report for the cadence learning ledger."""

from __future__ import annotations

import argparse
from pathlib import Path

from cadence_learning import summarize_learning
from repo_io import DEFAULT_PROFILE_ID

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-u", "--user", default=DEFAULT_PROFILE_ID)
    parser.add_argument("--ledger", type=Path, default=None)
    args = parser.parse_args()

    summary = summarize_learning(args.user, ledger_path=args.ledger)
    lines = ["# Cadence learning report", ""]
    counts = summary["counts"]
    lines.append(f"- Dream stages: {counts['dream_stage']}")
    lines.append(f"- Coffee choices: {counts['coffee_choice']}")
    lines.append(f"- Coffee resolutions: {counts['coffee_resolution']}")
    lines.append("")

    if summary["dream_match_classes"]:
        lines.append("## Dream accuracy")
        lines.append("")
        for key, value in sorted(summary["dream_match_classes"].items()):
            lines.append(f"- {key}: {value}")
        lines.append("")

    if summary["hindsight_classes"]:
        lines.append("## Coffee hindsight")
        lines.append("")
        for key, value in sorted(summary["hindsight_classes"].items()):
            lines.append(f"- {key}: {value}")
        lines.append("")

    if summary["action_counts"]:
        lines.append("## Learning actions")
        lines.append("")
        for key, value in sorted(summary["action_counts"].items()):
            lines.append(f"- {key}: {value}")
        lines.append("")

    pattern = summary.get("pattern_watch")
    if pattern:
        lines.append("## Pattern watch")
        lines.append("")
        lines.append(f"- {pattern['message']} {pattern['adjustment']}")
        lines.append("")

    print("\n".join(lines))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
