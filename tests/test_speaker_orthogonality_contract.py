"""Civ-lens speaker-role orthogonality contract.

The goal is to prevent mature civ-lens speaker lanes from collapsing into
generic "geopolitical analysis." Each speaker must keep a distinct job in
comparisons and statecraft routing.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = REPO_ROOT / "tests" / "fixtures" / "speaker_orthogonality_contract.json"
EXPECTED_SCORE = 100
EXPECTED_CASE_IDS = [f"SPO-G{i:03d}" for i in range(1, 11)]
REQUIRED_CASE_FIELDS = {"id", "label", "points", "critical", "paths", "must_cover"}

def _load_fixture() -> dict:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

def _normalize(text: str) -> str:
    normalized = text.lower().replace("\u2019", "'").replace("\u2013", "-")
    normalized = normalized.replace("\u2014", "-").replace("`", "")
    return re.sub(r"\s+", " ", normalized)

def _case_text(case: dict) -> str:
    chunks = []
    for path in case["paths"]:
        chunks.append((REPO_ROOT / path).read_text(encoding="utf-8"))
    return "\n".join(chunks)

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
        "for",
        "from",
        "in",
        "into",
        "is",
        "it",
        "of",
        "or",
        "the",
        "this",
        "to",
        "with",
    }
    meaningful = [word for word in words if word not in stopwords]
    return bool(meaningful) and all(word in haystack for word in meaningful)

def _missing_terms(terms: list[str], haystack: str) -> list[str]:
    return [term for term in terms if not _term_supported(term, haystack)]

def _fixture_failures(fixture: dict) -> list[str]:
    failures: list[str] = []
    cases = fixture.get("cases", [])
    if [case.get("id") for case in cases] != EXPECTED_CASE_IDS:
        failures.append("speaker orthogonality cases must be ordered SPO-G001..SPO-G010")

    total = 0
    for case in cases:
        missing = REQUIRED_CASE_FIELDS - case.keys()
        if missing:
            failures.append(f"{case.get('id', '<unknown>')} missing fields: {sorted(missing)}")
            continue
        total += int(case["points"])
        for path in case["paths"]:
            if not (REPO_ROOT / path).exists():
                failures.append(f"{case['id']} path does not exist: {path}")
        if not case["must_cover"]:
            failures.append(f"{case['id']} must_cover is empty")

    if total != EXPECTED_SCORE:
        failures.append(f"case points must total {EXPECTED_SCORE}, got {total}")

    expected_speakers = ["pape", "ritter", "parsi", "crooke", "marandi", "mercouris"]
    if fixture.get("core_speakers") != expected_speakers:
        failures.append("core_speakers must preserve the six-speaker orthogonality set")

    return failures

def _score_fixture(fixture: dict) -> tuple[int, list[str], list[str]]:
    score = 0
    misses: list[str] = []
    critical_failures: list[str] = []

    for case in fixture["cases"]:
        haystack = _normalize(_case_text(case))
        missing = _missing_terms(case["must_cover"], haystack)
        if missing:
            message = f"{case['id']} {case['label']} missing: {missing}"
            misses.append(message)
            if case["critical"]:
                critical_failures.append(message)
        else:
            score += int(case["points"])

    return score, misses, critical_failures

def _collapse_phrase_failures(fixture: dict) -> list[str]:
    paths = {
        path
        for case in fixture["cases"]
        for path in case["paths"]
        if path.startswith("statecraft/voices/") or path.startswith("skills/_drafts/")
    }
    failures: list[str] = []
    patterns = [_normalize(phrase) for phrase in fixture["forbidden_collapse_phrases"]]

    for path in sorted(paths):
        text = _normalize((REPO_ROOT / path).read_text(encoding="utf-8"))
        for phrase in patterns:
            if phrase in text:
                failures.append(f"{path}: forbidden collapse phrase {phrase!r}")

    return failures

def _status(score: int, critical_failures: list[str], fixture: dict) -> str:
    if critical_failures:
        return "FAIL"
    if score >= int(fixture["score_bands"]["pass"]):
        return "PASS"
    if score >= int(fixture["score_bands"]["warn"]):
        return "WARN"
    return "FAIL"

def test_speaker_orthogonality_fixture_integrity() -> None:
    fixture = _load_fixture()
    failures = _fixture_failures(fixture)
    assert not failures, "\n".join(failures)

def test_speaker_orthogonality_contract_passes() -> None:
    fixture = _load_fixture()
    fixture_failures = _fixture_failures(fixture)
    assert not fixture_failures, "\n".join(fixture_failures)

    score, misses, critical_failures = _score_fixture(fixture)
    collapse_failures = _collapse_phrase_failures(fixture)
    critical_failures.extend(collapse_failures)
    status = _status(score, critical_failures, fixture)
    summary = f"Speaker orthogonality contract: {score}/100 {status}"
    print(summary)

    assert status == "PASS", "\n".join([summary, *critical_failures, *misses])
    assert not misses, "\n".join(misses)
