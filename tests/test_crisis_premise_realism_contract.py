"""Premise-realism contract for academy-statecraft crisis drafting.

This protects the pre-drafting judgment: weak or over-attributed crisis
premises must be reclassified before they become elegant instruments.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = REPO_ROOT / "tests" / "fixtures" / "crisis_premise_realism_contract.json"
EXPECTED_SCORE = 100
EXPECTED_CASE_IDS = [f"CPR-G{i:03d}" for i in range(1, 7)]
REQUIRED_CASE_FIELDS = {
    "id",
    "label",
    "points",
    "critical",
    "paths",
    "must_cover",
    "must_not",
    "expected_routing",
}
SKILL_PATH = REPO_ROOT / "skills-portable" / "_drafts" / "academy-statecraft-drafting" / "SKILL.md"
CASEBOOK_PATH = REPO_ROOT / "codex" / "academy" / "statecraft" / "sheets" / "crisis-test-casebook.md"


def _load_fixture() -> dict:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _normalize(text: str) -> str:
    normalized = text.lower().replace("\u2019", "'").replace("\u2013", "-")
    normalized = normalized.replace("\u2014", "-").replace("`", "")
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
        "in",
        "into",
        "is",
        "it",
        "of",
        "or",
        "the",
        "to",
        "with",
    }
    meaningful = [word for word in words if word not in stopwords]
    return bool(meaningful) and all(word in haystack for word in meaningful)


def _missing_terms(terms: list[str], haystack: str) -> list[str]:
    return [term for term in terms if not _term_supported(term, haystack)]


def _case_text(case: dict) -> str:
    chunks = []
    for path in case["paths"]:
        chunks.append((REPO_ROOT / path).read_text(encoding="utf-8"))
    return "\n".join(chunks)


def _fixture_failures(fixture: dict) -> list[str]:
    failures: list[str] = []
    cases = fixture.get("cases", [])

    if [case.get("id") for case in cases] != EXPECTED_CASE_IDS:
        failures.append("crisis premise realism cases must be ordered CPR-G001..CPR-G006")

    total = 0
    for case in cases:
        missing = REQUIRED_CASE_FIELDS - case.keys()
        if missing:
            failures.append(f"{case.get('id', '<unknown>')} missing fields: {sorted(missing)}")
            continue
        total += int(case["points"])
        if not case["must_cover"]:
            failures.append(f"{case['id']} must_cover is empty")
        if not case["expected_routing"]:
            failures.append(f"{case['id']} expected_routing is empty")
        for path in case["paths"]:
            if not (REPO_ROOT / path).exists():
                failures.append(f"{case['id']} path does not exist: {path}")

    if total != EXPECTED_SCORE:
        failures.append(f"case points must total {EXPECTED_SCORE}, got {total}")

    if fixture.get("protected_judgment") != "premise realism before crisis drafting":
        failures.append("protected_judgment must preserve the premise-realism framing")

    if len(fixture.get("critical_gates", [])) < 5:
        failures.append("fixture must declare at least five critical gates")

    return failures


def _hard_gate_failures(fixture: dict) -> list[str]:
    failures: list[str] = []
    skill = _normalize(SKILL_PATH.read_text(encoding="utf-8"))
    casebook = _normalize(CASEBOOK_PATH.read_text(encoding="utf-8"))
    combined = f"{skill}\n{casebook}"

    required_skill_terms = [
        "Premise realism gate",
        "mandatory before drafting",
        "should this premise be allowed onto the board",
        "Do not jump from capability to intent",
        "actor dependence on the target",
        "accident, negligence, private actor behavior, third-party provocation",
        "reclassify the crisis before drafting",
        "do not let an elegant instrument launder a bad premise",
    ]
    missing_skill = _missing_terms(required_skill_terms, skill)
    if missing_skill:
        failures.append(f"academy-statecraft skill missing premise gate terms: {missing_skill}")

    required_casebook_terms = [
        "Premise Realism Gate",
        "The Baltic case is the model failure check",
        "investigate before attributing",
        "harden before retaliating",
    ]
    missing_casebook = _missing_terms(required_casebook_terms, casebook)
    if missing_casebook:
        failures.append(f"crisis-test casebook missing premise gate terms: {missing_casebook}")

    for phrase in fixture.get("forbidden_phrases", []):
        normalized = _normalize(phrase)
        if normalized in combined:
            failures.append(f"forbidden premise-collapse phrase present: {phrase!r}")

    return failures


def _score_fixture(fixture: dict) -> tuple[int, list[str], list[str]]:
    score = 0
    misses: list[str] = []
    critical_failures: list[str] = []

    for case in fixture["cases"]:
        haystack = _normalize(_case_text(case))
        missing = _missing_terms(case["must_cover"] + case["expected_routing"], haystack)
        forbidden = [
            phrase
            for phrase in case["must_not"]
            if _normalize(phrase) in haystack
        ]
        if missing or forbidden:
            message = f"{case['id']} {case['label']}"
            if missing:
                message += f" missing: {missing}"
            if forbidden:
                message += f" forbidden: {forbidden}"
            misses.append(message)
            if case["critical"]:
                critical_failures.append(message)
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


def test_crisis_premise_realism_fixture_integrity() -> None:
    fixture = _load_fixture()
    failures = _fixture_failures(fixture)
    assert not failures, "\n".join(failures)


def test_crisis_premise_realism_contract_passes() -> None:
    fixture = _load_fixture()
    fixture_failures = _fixture_failures(fixture)
    assert not fixture_failures, "\n".join(fixture_failures)

    score, misses, critical_failures = _score_fixture(fixture)
    critical_failures.extend(_hard_gate_failures(fixture))
    status = _status(score, critical_failures, fixture)
    summary = f"Crisis premise realism contract: {score}/100 {status}"
    print(summary)

    assert status == "PASS", "\n".join([summary, *critical_failures, *misses])
    assert not misses, "\n".join(misses)
