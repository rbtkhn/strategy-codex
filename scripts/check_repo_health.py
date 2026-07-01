#!/usr/bin/env python3
"""Orchestrate repo health checks for contributor and agent preflight."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

def _run(cmd: list[str], *, label: str) -> tuple[int, str]:
    proc = subprocess.run(
        cmd,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    tail = (proc.stdout or proc.stderr or "").strip().splitlines()
    summary = tail[-1] if tail else f"exit {proc.returncode}"
    print(f"[{'ok' if proc.returncode == 0 else 'fail'}] {label}: {summary}")
    return proc.returncode, summary

def run_quick() -> int:
    checks = [
        (["python3", "scripts/validate_repo_routing.py"], "repo routing"),
        (["python3", "scripts/check_generated_surfaces.py", "--check", "--strict"], "generated surfaces strict"),
        (["python3", "scripts/check_voice_guest_indexes.py"], "voice guest index builders"),
        (["python3", "scripts/assert_root_file_budget.py", "--strict"], "root file budget"),
        (["python3", "scripts/check_doc_duplication.py"], "doc duplication"),
        (["python3", "scripts/check_routing_front_doors.py"], "routing front doors"),
        (["python3", "scripts/check_archive_boundary.py"], "archive mention budget"),
        (["python3", "scripts/check_repo_path_strict.py", "--strict"], "path strict scan"),
        (["python3", "scripts/check_record_surface_retirement.py"], "record surface retirement"),
        (["python3", "scripts/check_membrane_policy_light.py"], "membrane policy light"),
        (["python3", "scripts/check_transaction_term_usage.py", "--strict", "--skills-strict"], "transaction term usage"),
        (["python3", "scripts/check_work_record_doctrine.py"], "work/record doctrine banner"),
        (["python3", "scripts/validate_all_schemas.py", "--scope", "prediction"], "schema validation"),
        (["python3", "scripts/check_event_integrity.py"], "event integrity"),
        (["python3", "scripts/check_event_registry.py"], "event registry"),
        (
            ["python3", "scripts/check_event_registry.py", "--strict-enrolled"],
            "event registry (strict enrolled falsifiers)",
        ),
        (["python3", "scripts/build_prediction_event_pages.py"], "build prediction event pages"),
        (["python3", "scripts/build_prediction_event_pages.py", "--check"], "prediction event pages fresh"),
        (["python3", "scripts/build_prediction_registry.py"], "build prediction registry"),
        (["python3", "scripts/check_prediction_registry.py"], "prediction registry"),
        (["python3", "scripts/build_prediction_metrics.py"], "build prediction metrics"),
        (["python3", "scripts/check_prediction_metrics.py"], "prediction metrics"),
        (["python3", "scripts/build_prediction_disagreement.py"], "build prediction disagreement"),
        (["python3", "scripts/check_prediction_disagreement.py"], "prediction disagreement shape"),
        (["python3", "scripts/build_prediction_timeline.py"], "build prediction timeline"),
        (["python3", "scripts/check_prediction_timeline.py"], "prediction timeline shape"),
        (["python3", "scripts/build_freeman_predictions.py", "--check"], "freeman predictions fresh"),
        (["python3", "scripts/check_freeman_predictions.py"], "freeman predictions shape"),
        (["python3", "scripts/build_loop_registry.py", "--check"], "loop registry fresh"),
        (["python3", "scripts/check_loop_registry.py"], "loop registry shape"),
        (["python3", "scripts/check_singularity_loop_runs.py"], "singularity loop run receipts"),
        (["python3", "scripts/validate_all_schemas.py", "--scope", "singularity"], "singularity schema validation"),
        (["python3", "scripts/check_statecraft_notes.py", "--warn"], "statecraft notes gate"),
        (
            [
                "python3",
                "scripts/check_statecraft_notes.py",
                "--strict",
                "--changed-only",
                "--tier-a-only",
            ],
            "statecraft notes gate (changed Tier A)",
        ),
    ]
    rc = 0
    if (REPO_ROOT / "statecraft" / "voices" / "_templates").exists():
        print("[fail] retired path exists: statecraft/voices/_templates")
        rc = 1
    if (REPO_ROOT / "statecraft" / "voices" / "_scratch").exists():
        print("[fail] retired path exists: statecraft/voices/_scratch")
        rc = 1
    if (REPO_ROOT / "examples").exists():
        print("[fail] retired path exists: examples/")
        rc = 1
    for cmd, label in checks:
        code, _ = _run(cmd, label=label)
        rc = rc or code
    return rc

def run_full() -> int:
    rc = run_quick()
    extra = [
        (["python3", "scripts/check_generated_prediction_artifacts.py"], "prediction artifacts fresh"),
        (["python3", "scripts/audit_statecraft_archive_index.py", "--all-voice-indexes"], "voice index parity"),
        (["python3", "scripts/audit_repo_complexity.py", "--check"], "complexity audit"),
        (
            [
                "python3",
                "-m",
                "pytest",
                "tests/test_routing_generated.py",
                "tests/test_repo_path_strict.py",
                "tests/test_check_archive_boundary.py",
                "tests/test_check_generated_surfaces.py",
                "tests/test_assert_root_file_budget.py",
                "tests/test_check_doc_duplication.py",
                "tests/test_check_membrane_policy_light.py",
                "tests/test_harness_architecture_map_links.py",
                "tests/test_strategy_codex_cli.py",
                "tests/test_check_event_integrity.py",
                "tests/test_validate_all_schemas.py",
                "tests/test_schema_invariants.py",
                "tests/test_check_work_record_doctrine.py",
                "tests/test_prediction_registry_metrics.py",
                "tests/test_prediction_disagreement_timeline.py",
                "tests/test_freeman_predictions.py",
                "-q",
            ],
            "pytest subset",
        ),
    ]
    for cmd, label in extra:
        code, _ = _run(cmd, label=label)
        rc = rc or code
    return rc

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quick", action="store_true", help="Routing, archive, path checks")
    parser.add_argument("--full", action="store_true", help="Quick + audit --check + pytest subset")
    args = parser.parse_args()
    if args.full:
        return run_full()
    if args.quick or not (args.quick or args.full):
        return run_quick()
    parser.error("specify --quick or --full")
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
