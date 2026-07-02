"""Path-hygiene contract for the codex rehome.

This test guards the durable rehome decision:
academy and speakers live directly under continuity/, while calendar material lives
under continuity/years/<YYYY>/.
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = REPO_ROOT / "tests" / "fixtures" / "rehome_path_hygiene_contract.json"
EXPECTED_SCORE = 100
EXPECTED_CASE_IDS = [f"RPH-G{i:03d}" for i in range(1, 6)]
REQUIRED_CASE_FIELDS = {"id", "label", "points", "critical", "check"}

def _load_fixture() -> dict:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

def _to_repo_path(path: Path | str) -> str:
    return str(path).replace("\\", "/")

def _tracked_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=REPO_ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]

def _is_excluded(path: str, excluded_prefixes: list[str]) -> bool:
    normalized = _to_repo_path(path)
    return any(normalized.startswith(prefix) for prefix in excluded_prefixes)

def _read_text(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8", errors="ignore")

def _fixture_failures(fixture: dict) -> list[str]:
    failures: list[str] = []
    cases = fixture.get("cases", [])
    if [case.get("id") for case in cases] != EXPECTED_CASE_IDS:
        failures.append("rehome path hygiene cases must be ordered RPH-G001..RPH-G005")

    total = 0
    for case in cases:
        missing = REQUIRED_CASE_FIELDS - case.keys()
        if missing:
            failures.append(f"{case.get('id', '<unknown>')} missing fields: {sorted(missing)}")
            continue
        total += int(case["points"])

    if total != EXPECTED_SCORE:
        failures.append(f"case points must total {EXPECTED_SCORE}, got {total}")

    if "runtime/artifacts/benchmarks/" not in fixture.get("excluded_path_prefixes", []):
        failures.append("runtime/artifacts/benchmarks/ must remain an explicit provenance exclusion")

    return failures

def _check_required_roots(fixture: dict) -> list[str]:
    return [
        root
        for root in fixture["required_roots"]
        if not (REPO_ROOT / root).exists()
    ]

def _check_forbidden_roots(fixture: dict) -> list[str]:
    return [
        root
        for root in fixture["forbidden_roots"]
        if (REPO_ROOT / root).exists()
    ]

def _check_mirror_receipt(fixture: dict) -> list[str]:
    contract = fixture["mirror_receipt"]
    failures: list[str] = []
    receipt = REPO_ROOT / contract["path"]
    if not receipt.is_file():
        failures.append(f"missing {contract['path']}")
    forbidden = contract.get("forbidden_file")
    if forbidden and (REPO_ROOT / forbidden).exists():
        failures.append(f"forbidden {forbidden} (vendored mirror, not submodule)")
    return failures

def _check_tracked_content(fixture: dict) -> list[str]:
    excluded = fixture["excluded_path_prefixes"]
    patterns = [re.compile(pattern, re.IGNORECASE) for pattern in fixture["stale_content_patterns"]]
    failures: list[str] = []

    for path in _tracked_files():
        normalized_path = _to_repo_path(path)
        if _is_excluded(normalized_path, excluded):
            continue
        full_path = REPO_ROOT / path
        if not full_path.is_file():
            continue
        text = _read_text(path)
        for pattern in patterns:
            for match in pattern.finditer(text):
                line_no = text.count("\n", 0, match.start()) + 1
                failures.append(f"{normalized_path}:{line_no}: {match.group(0)}")

    return failures

def _score_fixture(fixture: dict) -> tuple[int, list[str], list[str]]:
    score = 0
    misses: list[str] = []
    critical_failures: list[str] = []

    checks = {
        "required_roots": _check_required_roots,
        "forbidden_roots_absent": _check_forbidden_roots,
        "mirror_receipt": _check_mirror_receipt,
        "tracked_content": _check_tracked_content,
        "exclusion_policy": lambda f: []
        if "runtime/artifacts/benchmarks/" in f["excluded_path_prefixes"]
        else ["runtime/artifacts/benchmarks/ not excluded"],
    }

    for case in fixture["cases"]:
        failures = checks[case["check"]](fixture)
        if failures:
            misses.append(f"{case['id']} {case['label']}: {failures}")
            if case["critical"]:
                critical_failures.extend(failures)
        else:
            score += int(case["points"])

    return score, misses, critical_failures

def _status(score: int, critical_failures: list[str], fixture: dict) -> str:
    if critical_failures:
        return "FAIL"
    if score >= int(fixture["score_bands"]["pass"]):
        return "PASS"
    if score >= int(fixture["score_bands"]["warn"]):
        return "WARN"
    return "FAIL"

def test_rehome_path_hygiene_fixture_integrity() -> None:
    fixture = _load_fixture()
    failures = _fixture_failures(fixture)
    assert not failures, "\n".join(failures)

def test_rehome_path_hygiene_contract_passes() -> None:
    fixture = _load_fixture()
    fixture_failures = _fixture_failures(fixture)
    assert not fixture_failures, "\n".join(fixture_failures)

    score, misses, critical_failures = _score_fixture(fixture)
    status = _status(score, critical_failures, fixture)
    summary = f"Rehome path hygiene contract: {score}/100 {status}"
    print(summary)

    assert status == "PASS", "\n".join([summary, *misses])
    assert not misses, "\n".join(misses)
