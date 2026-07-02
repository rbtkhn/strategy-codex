"""Deterministic contract gauntlet for the Mercouris CIV-MEM draft skill."""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = REPO_ROOT / "tests" / "fixtures" / "mercouris_civmem_gauntlet.json"
SKILL_PATH = (
    REPO_ROOT
    / "skills"
    / "_drafts"
    / "mercouris-daily-continuity-extraction"
    / "SKILL.md"
)

REQUIRED_FIELDS = {
    "id",
    "prompt",
    "mode",
    "must_cover",
    "must_not",
    "expected_routing",
    "score",
}
SCORE_FIELDS = ("coverage", "anti_pattern", "routing", "civmem")
CASE_SCORE = 7.5
FIXTURE_INTEGRITY_SCORE = 10
EXPECTED_CASE_COUNT = 12
EXPECTED_CASE_BUDGET = 90
EXPECTED_SUITE_BUDGET = 100

CRITICAL_GATES = {
    "civmem_cannot_prove_current_facts": [
        "civ-mem is not proof",
        "do not cite civ-mem as evidence for current facts",
        "must not override current-source archive/placeholders/evidence",
    ],
    "iran_maps_to_persia": [
        "for iran questions",
        "persia",
        "iran statecraft lane",
        "current authority/instrument home",
    ],
    "durable_outputs_route_to_statecraft": [
        "durable outputs",
        "continuity/academy/statecraft/",
        "do not write them into mercouris speaker surfaces unless",
    ],
    "comparative_roles_do_not_collapse": [
        "comparative speaker mode",
        "do not let mercouris carry another speaker's role",
        "ritter's force-constraint voice",
        "parsi's settlement architect",
        "marandi's inside-state authority",
    ],
}

def _load_cases() -> list[dict]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

def _skill_text() -> str:
    return SKILL_PATH.read_text(encoding="utf-8")

def _normalize(text: str) -> str:
    normalized = text.lower().replace("\u2019", "'").replace("\u2013", "-")
    normalized = normalized.replace("\u2014", "-")
    return re.sub(r"\s+", " ", normalized)

def _term_supported(term: str, haystack: str) -> bool:
    """Return whether a fixture term is supported by the skill contract.

    Most terms are exact phrase checks. For a few compound workflow labels, allow
    all meaningful words to appear so the test does not force brittle prose.
    """

    term = _normalize(term)
    if term in haystack:
        return True

    words = re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)?", term)
    meaningful = [
        word
        for word in words
        if word
        not in {
            "a",
            "an",
            "and",
            "as",
            "for",
            "from",
            "in",
            "into",
            "of",
            "or",
            "the",
            "to",
            "with",
        }
    ]
    return bool(meaningful) and all(word in haystack for word in meaningful)

def _missing_terms(terms: list[str], haystack: str) -> list[str]:
    return [term for term in terms if not _term_supported(term, haystack)]

def _validate_fixture_shape(cases: list[dict]) -> None:
    assert len(cases) == EXPECTED_CASE_COUNT, "fixture count must be exactly 12"

    ids = [case.get("id") for case in cases]
    expected_ids = [f"MCM-G{i:03d}" for i in range(1, EXPECTED_CASE_COUNT + 1)]
    assert ids == expected_ids, "case ids must be unique and sequential"

    total_case_budget = 0.0
    for case in cases:
        missing_fields = REQUIRED_FIELDS - case.keys()
        assert not missing_fields, f"{case.get('id', '<unknown>')} missing {missing_fields}"

        for field in ("prompt", "mode"):
            assert isinstance(case[field], str) and case[field].strip(), (
                f"{case['id']} has empty {field}"
            )

        for field in ("must_cover", "must_not", "expected_routing"):
            assert isinstance(case[field], list) and case[field], (
                f"{case['id']} has empty {field}"
            )
            assert all(isinstance(item, str) and item.strip() for item in case[field]), (
                f"{case['id']} has invalid {field} item"
            )

        score = case["score"]
        assert set(score) == set(SCORE_FIELDS), f"{case['id']} has invalid score fields"
        case_budget = 0.0
        for field in SCORE_FIELDS:
            assert isinstance(score[field], (int, float)), f"{case['id']} score is not numeric"
            case_budget += float(score[field])
        assert abs(case_budget - CASE_SCORE) < 0.001, f"{case['id']} score must be 7.5"
        total_case_budget += case_budget

    assert abs(total_case_budget - EXPECTED_CASE_BUDGET) < 0.001
    assert abs(total_case_budget + FIXTURE_INTEGRITY_SCORE - EXPECTED_SUITE_BUDGET) < 0.001

def _score_suite(cases: list[dict], skill_text: str) -> tuple[float, list[str]]:
    haystack = _normalize(skill_text)
    score = float(FIXTURE_INTEGRITY_SCORE)
    misses: list[str] = []

    for case in cases:
        case_score = case["score"]
        coverage_misses = _missing_terms(case["must_cover"], haystack)
        anti_pattern_misses = _missing_terms(case["must_not"], haystack)
        routing_misses = _missing_terms(case["expected_routing"], haystack)

        if coverage_misses:
            misses.append(f"{case['id']} coverage missing: {coverage_misses}")
        else:
            score += float(case_score["coverage"])

        if anti_pattern_misses:
            misses.append(f"{case['id']} anti-pattern missing: {anti_pattern_misses}")
        else:
            score += float(case_score["anti_pattern"])

        if routing_misses:
            misses.append(f"{case['id']} routing missing: {routing_misses}")
        else:
            score += float(case_score["routing"])

        civmem_terms = [
            "civ-mem",
            "authority",
            "restraint",
            "settlement",
            "statecraft",
        ]
        civmem_misses = _missing_terms(civmem_terms, haystack)
        if civmem_misses:
            misses.append(f"{case['id']} civmem behavior missing: {civmem_misses}")
        else:
            score += float(case_score["civmem"])

    return round(score), misses

def _critical_failures(skill_text: str) -> list[str]:
    haystack = _normalize(skill_text)
    failures = []
    for gate, terms in CRITICAL_GATES.items():
        missing = _missing_terms(terms, haystack)
        if missing:
            failures.append(f"{gate}: missing {missing}")
    return failures

def _suite_status(score: float, critical_failures: list[str]) -> str:
    if critical_failures:
        return "FAIL"
    if score >= 90:
        return "PASS"
    if score >= 75:
        return "WARN"
    return "FAIL"

def test_fixture_integrity_and_budget() -> None:
    cases = _load_cases()
    _validate_fixture_shape(cases)

def test_all_gauntlet_terms_are_supported_by_skill_contract() -> None:
    cases = _load_cases()
    _validate_fixture_shape(cases)

    score, misses = _score_suite(cases, _skill_text())
    assert not misses, "\n".join(misses)
    assert score == EXPECTED_SUITE_BUDGET

def test_critical_failure_gates_are_closed() -> None:
    cases = _load_cases()
    _validate_fixture_shape(cases)
    assert len(cases) == EXPECTED_CASE_COUNT

    failures = _critical_failures(_skill_text())
    assert not failures, "\n".join(failures)

def test_quantified_suite_score_passes() -> None:
    cases = _load_cases()
    _validate_fixture_shape(cases)

    score, misses = _score_suite(cases, _skill_text())
    critical = _critical_failures(_skill_text())
    status = _suite_status(score, critical)
    summary = f"Mercouris CIV-MEM gauntlet: {score}/100 {status}"
    print(summary)

    assert status == "PASS", "\n".join([summary, *critical, *misses])
