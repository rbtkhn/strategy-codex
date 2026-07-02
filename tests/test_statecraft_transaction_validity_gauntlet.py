"""Deterministic validity gauntlet for academy-statecraft transactions."""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = REPO_ROOT / "tests" / "fixtures" / "statecraft_transaction_validity_gauntlet.json"
EXPECTED_SCORE = 100
EXPECTED_CASE_COUNT = 10
REQUIRED_CASE_FIELDS = {
    "id",
    "label",
    "role",
    "path",
    "points",
    "critical",
    "must_cover",
}
VALID_ROLES = {"template", "full_transaction", "framework_readme"}

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
        "when",
        "with",
    }
    meaningful = [word for word in words if word not in stopwords]
    return bool(meaningful) and all(word in haystack for word in meaningful)

def _missing_terms(terms: list[str], haystack: str) -> list[str]:
    return [term for term in terms if not _term_supported(term, haystack)]

def _case_text(case: dict) -> str:
    path = REPO_ROOT / case["path"]
    return path.read_text(encoding="utf-8")

def _has_valid_status(text: str, valid_statuses: list[str]) -> bool:
    normalized = _normalize(text)
    return any(re.search(rf"\b{re.escape(status)}\b", normalized) for status in valid_statuses)

def _has_markdown_link(text: str) -> bool:
    return bool(re.search(r"\[[^\]]+\]\([^)]+\)", text))

def _fixture_failures(fixture: dict) -> list[str]:
    failures: list[str] = []
    cases = fixture.get("cases", [])
    if len(cases) != EXPECTED_CASE_COUNT:
        failures.append(f"fixture must contain exactly {EXPECTED_CASE_COUNT} cases")

    expected_ids = [f"STX-G{i:03d}" for i in range(1, len(cases) + 1)]
    actual_ids = [case.get("id") for case in cases]
    if actual_ids != expected_ids:
        failures.append(f"case ids must be sequential: {actual_ids}")

    total = 0
    for case in cases:
        missing = REQUIRED_CASE_FIELDS - case.keys()
        if missing:
            failures.append(f"{case.get('id', '<unknown>')} missing fields: {sorted(missing)}")
            continue
        if case["role"] not in VALID_ROLES:
            failures.append(f"{case['id']} has invalid role {case['role']}")
        if not isinstance(case["points"], int) or case["points"] <= 0:
            failures.append(f"{case['id']} points must be positive integer")
        total += int(case["points"])
        if not case["must_cover"]:
            failures.append(f"{case['id']} must_cover is empty")
        path = REPO_ROOT / case["path"]
        if not path.exists():
            failures.append(f"{case['id']} path does not exist: {case['path']}")

    if total != EXPECTED_SCORE:
        failures.append(f"fixture points must total {EXPECTED_SCORE}, got {total}")

    valid_statuses = fixture.get("valid_statuses", [])
    if valid_statuses != ["draft", "validated", "volatile", "superseded"]:
        failures.append("valid_statuses must preserve canonical transaction statuses")

    return failures

def _critical_failures(fixture: dict) -> list[str]:
    failures: list[str] = []
    valid_statuses = fixture["valid_statuses"]

    for case in fixture["cases"]:
        text = _case_text(case)
        normalized = _normalize(text)
        path = case["path"]

        if case["role"] == "template":
            if "non-authoritative; not record" not in normalized:
                failures.append(f"{path}: template omits WORK boundary")
            if "validity status" not in normalized:
                failures.append(f"{path}: template lacks Validity Status")
            if _missing_terms(["authority", "restraint", "settlement"], normalized):
                failures.append(f"{path}: template lacks authority/restraint/settlement")

        if case["role"] in {"full_transaction", "framework_readme"}:
            if not _has_markdown_link(text):
                failures.append(f"{path}: exemplar lacks source/provenance links")
            if not _has_valid_status(text, valid_statuses):
                failures.append(f"{path}: exemplar lacks canonical validity status")
            if "source" not in normalized and "provenance" not in normalized:
                failures.append(f"{path}: exemplar lacks source/provenance anchor language")

        if case["role"] == "full_transaction":
            if "instrument text" not in normalized and "draft clause" not in normalized:
                failures.append(f"{path}: full transaction lacks instrument text")
            if "authority" not in normalized:
                failures.append(f"{path}: full transaction lacks authority carrier language")
            if "settlement" not in normalized:
                failures.append(f"{path}: full transaction lacks settlement language")
            if "falsifier" not in normalized or "revisit trigger" not in normalized:
                failures.append(f"{path}: full transaction lacks falsifier/revisit")

    return sorted(set(failures))

def _score_fixture(fixture: dict) -> tuple[int, list[str]]:
    score = 0
    misses: list[str] = []

    for case in fixture["cases"]:
        text = _case_text(case)
        normalized = _normalize(text)
        missing = _missing_terms(case["must_cover"], normalized)
        if missing:
            misses.append(f"{case['id']} {case['label']} missing: {missing}")
        else:
            score += int(case["points"])

    return score, misses

def _status(score: int, critical_failures: list[str], bands: dict) -> str:
    if critical_failures:
        return "FAIL"
    if score >= int(bands["pass"]):
        return "PASS"
    if score >= int(bands["warn"]):
        return "WARN"
    return "FAIL"

def test_statecraft_transaction_fixture_integrity() -> None:
    fixture = _load_fixture()
    failures = _fixture_failures(fixture)
    assert not failures, "\n".join(failures)

def test_statecraft_transaction_validity_gauntlet_passes() -> None:
    fixture = _load_fixture()
    fixture_failures = _fixture_failures(fixture)
    assert not fixture_failures, "\n".join(fixture_failures)

    score, misses = _score_fixture(fixture)
    critical = _critical_failures(fixture)
    status = _status(score, critical, fixture["score_bands"])
    summary = f"Statecraft transaction validity gauntlet: {score}/100 {status}"
    print(summary)

    assert status == "PASS", "\n".join([summary, *critical, *misses])
    assert not misses, "\n".join(misses)
