"""Contract gauntlets for high-drift draft skills.

These tests do not evaluate model output. They verify that the draft skill files
contain the operating promises needed before a future model-facing gauntlet can
exercise them.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = REPO_ROOT / "tests" / "fixtures" / "draft_skill_contract_gauntlets.json"
REQUIRED_SUITE_FIELDS = {
    "skill",
    "path",
    "minimum_score",
    "critical_must_cover",
    "cases",
}
REQUIRED_CASE_FIELDS = {
    "id",
    "prompt",
    "must_cover",
    "must_not",
    "expected_behavior",
}

def _load_suites() -> list[dict]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

def _normalize(text: str) -> str:
    normalized = text.lower().replace("\u2019", "'").replace("\u2013", "-")
    normalized = normalized.replace("\u2014", "-")
    normalized = normalized.replace("`", "")
    return re.sub(r"\s+", " ", normalized)

def _term_supported(term: str, haystack: str) -> bool:
    term = _normalize(term)
    if term in haystack:
        return True

    words = re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)?", term)
    stopwords = {
        "a",
        "an",
        "and",
        "as",
        "before",
        "for",
        "from",
        "if",
        "in",
        "into",
        "is",
        "it",
        "of",
        "or",
        "the",
        "them",
        "this",
        "to",
        "with",
    }
    meaningful = [word for word in words if word not in stopwords]
    return bool(meaningful) and all(word in haystack for word in meaningful)

def _missing(terms: list[str], haystack: str) -> list[str]:
    return [term for term in terms if not _term_supported(term, haystack)]

def _validate_fixture_shape(suites: list[dict]) -> None:
    assert suites, "draft skill gauntlet fixture must not be empty"
    seen_skills: set[str] = set()

    for suite in suites:
        missing = REQUIRED_SUITE_FIELDS - suite.keys()
        assert not missing, f"suite missing fields: {missing}"
        assert suite["skill"] not in seen_skills, f"duplicate suite {suite['skill']}"
        seen_skills.add(suite["skill"])
        assert 0 <= suite["minimum_score"] <= 100
        assert suite["critical_must_cover"], f"{suite['skill']} lacks critical gates"
        assert suite["cases"], f"{suite['skill']} lacks cases"

        for index, case in enumerate(suite["cases"], start=1):
            case_missing = REQUIRED_CASE_FIELDS - case.keys()
            assert not case_missing, f"{suite['skill']} case missing fields: {case_missing}"
            expected_prefix = suite.get("id_prefix", suite["skill"].split("-")[0]).upper()
            assert case["id"].endswith(f"G{index:03d}"), f"{case['id']} not sequential"
            assert case["id"].startswith(expected_prefix), f"{case['id']} has unexpected prefix"
            for field in ("must_cover", "must_not", "expected_behavior"):
                assert isinstance(case[field], list) and case[field], (
                    f"{case['id']} has empty {field}"
                )

def _score_suite(suite: dict, skill_text: str) -> tuple[int, list[str]]:
    haystack = _normalize(skill_text)
    possible = len(suite["critical_must_cover"]) + 3 * len(suite["cases"])
    earned = 0
    misses: list[str] = []

    critical_missing = _missing(suite["critical_must_cover"], haystack)
    if critical_missing:
        misses.append(f"{suite['skill']} critical missing: {critical_missing}")
    else:
        earned += len(suite["critical_must_cover"])

    for case in suite["cases"]:
        for field in ("must_cover", "must_not", "expected_behavior"):
            field_missing = _missing(case[field], haystack)
            if field_missing:
                misses.append(f"{case['id']} {field} missing: {field_missing}")
            else:
                earned += 1

    return round((earned / possible) * 100), misses

def test_draft_skill_gauntlet_fixture_integrity() -> None:
    suites = _load_suites()
    _validate_fixture_shape(suites)

def test_draft_skill_contract_gauntlets_pass() -> None:
    suites = _load_suites()
    _validate_fixture_shape(suites)

    summaries: list[str] = []
    failures: list[str] = []

    for suite in suites:
        skill_path = REPO_ROOT / suite["path"]
        assert skill_path.exists(), f"{suite['skill']} missing skill file: {skill_path}"
        score, misses = _score_suite(suite, skill_path.read_text(encoding="utf-8"))
        status = "PASS" if score >= suite["minimum_score"] and not misses else "FAIL"
        summaries.append(f"{suite['skill']} gauntlet: {score}/100 {status}")
        if status != "PASS":
            failures.extend([summaries[-1], *misses])

    print("\n".join(summaries))
    assert not failures, "\n".join(failures)
