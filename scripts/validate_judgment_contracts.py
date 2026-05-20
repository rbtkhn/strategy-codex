#!/usr/bin/env python3
"""Run the judgment contract gauntlets as one read-only validation check."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

TEST_TARGETS = [
    "tests/test_forecast_discipline_contract.py",
    "tests/test_speaker_orthogonality_contract.py",
    "tests/test_crisis_premise_realism_contract.py",
    "tests/test_rehome_path_hygiene_contract.py",
    "tests/test_statecraft_transaction_validity_gauntlet.py",
    "tests/test_draft_skill_contract_gauntlets.py",
    "tests/test_mercouris_civmem_gauntlet.py",
]


def _score_lines(stdout: str) -> list[str]:
    markers = ("contract:", "gauntlet:")
    return [
        line.strip()
        for line in stdout.splitlines()
        if any(marker in line.lower() for marker in markers)
        and any(status in line for status in ("PASS", "WARN", "FAIL"))
    ]


def main() -> int:
    cmd = [sys.executable, "-m", "pytest", "-s", *TEST_TARGETS]
    proc = subprocess.run(
        cmd,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        shell=False,
    )

    print("Judgment contract gauntlets:")
    for line in _score_lines(proc.stdout):
        print(f"- {line}")

    if proc.returncode == 0:
        print(f"Judgment contract gauntlets: PASS ({len(TEST_TARGETS)} suites)")
        return 0

    print(f"Judgment contract gauntlets: FAIL ({len(TEST_TARGETS)} suites)")
    if proc.stdout.strip():
        print("\n--- pytest stdout ---")
        print(proc.stdout.rstrip())
    if proc.stderr.strip():
        print("\n--- pytest stderr ---", file=sys.stderr)
        print(proc.stderr.rstrip(), file=sys.stderr)
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
