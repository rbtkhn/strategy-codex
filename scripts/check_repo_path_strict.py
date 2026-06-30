#!/usr/bin/env python3
"""Warn on legacy repo path layouts (Sprint 4 — warn mode; --strict fails CI)."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from repo_io import (  # noqa: E402
    REPO_PATH_CLASSIFICATION,
    REPO_PATH_MIGRATIONS,
    collect_wave_readiness_report,
    load_path_fallback_retirement,
    scan_legacy_path_layout,
    validate_path_fallback_retirement,
    validate_repo_path_classification,
)

def _layout_issue_kind(issue: str) -> str:
    if ": dual layout" in issue:
        return "dual"
    if ": legacy-only" in issue:
        return "legacy_only"
    return "other"

def collect_scan_report() -> dict[str, Any]:
    classification_issues = validate_repo_path_classification()
    retirement_issues = validate_path_fallback_retirement()
    layout_issues = scan_legacy_path_layout()

    category_counts = Counter(REPO_PATH_CLASSIFICATION.values())
    layout_kinds = Counter(_layout_issue_kind(i) for i in layout_issues)

    try:
        retirement_by_key = load_path_fallback_retirement()
    except (OSError, ValueError, RuntimeError):
        retirement_by_key = {}

    retirement_candidates: list[dict[str, Any]] = []
    for key in sorted(REPO_PATH_MIGRATIONS):
        entry = retirement_by_key.get(key) or {}
        status = str(entry.get("retirement_status") or "")
        if status not in {"remove_when_clean", "move_to_grace_mar_compat"}:
            continue
        has_layout = any(issue.startswith(f"{key}:") for issue in layout_issues)
        if has_layout or status == "move_to_grace_mar_compat":
            retirement_candidates.append(
                {
                    "key": key,
                    "retirement_status": status,
                    "wave": entry.get("wave"),
                    "category": entry.get("category"),
                    "has_layout_issue": has_layout,
                }
            )

    summary = {
        "total_keys": len(REPO_PATH_MIGRATIONS),
        "active_canonical": category_counts.get("active_canonical", 0),
        "archive_placeholder": category_counts.get("archive_placeholder", 0),
        "grace_mar_compat": category_counts.get("grace_mar_compat", 0),
        "legacy_only_layouts": layout_kinds.get("legacy_only", 0),
        "dual_layouts": layout_kinds.get("dual", 0),
        "missing_classifications": len(classification_issues),
        "retirement_policy_issues": len(retirement_issues),
        "layout_issues": len(layout_issues),
    }

    policy_issues = classification_issues + retirement_issues
    all_issues: list[str] = list(policy_issues)
    for issue in layout_issues:
        key = issue.split(":", 1)[0]
        bucket = REPO_PATH_CLASSIFICATION.get(key, "unclassified")
        all_issues.append(f"[{bucket}] {issue}")

    return {
        "summary": summary,
        "issues": all_issues,
        "policy_issues": policy_issues,
        "layout_issues": layout_issues,
        "retirement_candidates": retirement_candidates,
    }

def _print_text_report(report: dict[str, Any]) -> None:
    summary = report["summary"]
    print("Repo path strict scan")
    print("=====================")
    print("Summary:")
    print(f"- total keys: {summary['total_keys']}")
    print(f"- active_canonical: {summary['active_canonical']}")
    print(f"- archive_placeholder: {summary['archive_placeholder']}")
    print(f"- grace_mar_compat: {summary['grace_mar_compat']}")
    print(f"- legacy-only layouts: {summary['legacy_only_layouts']}")
    print(f"- dual layouts: {summary['dual_layouts']}")
    print(f"- missing classifications: {summary['missing_classifications']}")
    print(f"- retirement policy issues: {summary['retirement_policy_issues']}")

    issues = report["issues"]
    if issues:
        print("")
        print("Issues:")
        for issue in issues:
            print(f"- {issue}")

    candidates = report["retirement_candidates"]
    if candidates:
        print("")
        print("Retirement candidates:")
        for item in candidates:
            wave = item.get("wave")
            wave_s = f" (Wave {wave})" if wave is not None else ""
            print(f"- {item['key']} -> {item['retirement_status']}{wave_s}")

    if not issues:
        print("")
        print("ok: no active legacy repo path layouts detected")

def _yes_no(value: bool) -> str:
    return "yes" if value else "no"

_WAVE_READINESS_TITLES: dict[int, str] = {
    2: "Wave 2 platform readiness",
    3: "Wave 3 archive placeholder readiness",
    4: "Wave 4 Grace-Mar compatibility readiness",
}

def _wave_readiness_title(wave: int) -> str:
    return _WAVE_READINESS_TITLES.get(wave, f"Wave {wave} readiness")

def _print_wave_readiness_report(report: dict[str, Any]) -> None:
    wave = report["wave"]
    title = _wave_readiness_title(wave)
    keys = report.get("keys") or {}
    key_width = max(14, max((len(k) for k in keys), default=0) + 2)
    print(title)
    print("=" * len(title))
    print(
        f"{'Key':<{key_width}}{'Canonical exists':<20}{'Legacy exists':<16}"
        f"{'Active refs':<14}{'Status'}"
    )
    for key, item in keys.items():
        active_count = len(item.get("active_refs") or [])
        print(
            f"{key:<{key_width}}"
            f"{_yes_no(item['canonical_exists']):<20}"
            f"{_yes_no(item['legacy_exists']):<16}"
            f"{active_count:<14}"
            f"{item['status']}"
        )
    summary = report.get("summary") or {}
    if summary:
        print("")
        print("Summary:")
        for status, count in sorted(summary.items()):
            print(f"- {status}: {count}")

def _wave_readiness_has_blockers(report: dict[str, Any]) -> bool:
    allowed = {"ready", "ready_docs_only_refs"}
    return any(item.get("status") not in allowed for item in report["keys"].values())

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 when any legacy or dual-layout path key is present",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable scan report as JSON",
    )
    parser.add_argument(
        "--wave",
        type=int,
        metavar="N",
        help="Emit fallback removal readiness report for retirement wave N",
    )
    parser.add_argument(
        "--strict-readiness",
        action="store_true",
        help="With --wave, exit 1 when any key is not ready or ready_docs_only_refs",
    )
    args = parser.parse_args()

    if args.wave is not None:
        wave_report = collect_wave_readiness_report(args.wave)
        if args.json:
            print(json.dumps(wave_report, indent=2, sort_keys=True))
        else:
            _print_wave_readiness_report(wave_report)
        if args.strict_readiness and _wave_readiness_has_blockers(wave_report):
            if not args.json:
                print("repo-path-strict: wave readiness blocked", file=sys.stderr)
            return 1
        return 0

    report = collect_scan_report()

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        _print_text_report(report)

    has_issues = bool(report["issues"])
    if has_issues and not args.json:
        print(f"repo-path-strict: {len(report['issues'])} issue(s)", file=sys.stderr)
    return 1 if (args.strict and has_issues) else (0 if not has_issues else 0)

if __name__ == "__main__":
    raise SystemExit(main())
