"""Forecast discipline contract for expert ledgers."""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = REPO_ROOT / "tests" / "fixtures" / "forecast_discipline_contract.json"
EXPECTED_SCORE = 100
EXPECTED_LEDGER_IDS = ["FDC-G001", "FDC-G002", "FDC-G003"]
REQUIRED_LEDGER_FIELDS = {
    "id",
    "speaker",
    "path",
    "heading",
    "points",
    "critical",
    "id_prefix",
    "required_columns",
    "min_rows",
}

def _load_fixture() -> dict:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

def _normalize(text: str) -> str:
    normalized = text.lower().replace("\u2019", "'").replace("\u2013", "-")
    normalized = normalized.replace("\u2014", "-")
    return re.sub(r"\s+", " ", normalized)

def _term_supported(term: str, haystack: str) -> bool:
    term = _normalize(term).replace("`", "")
    plain_haystack = haystack.replace("`", "")
    if term in plain_haystack:
        return True

    words = re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)?", term)
    stopwords = {
        "a",
        "an",
        "and",
        "as",
        "from",
        "in",
        "into",
        "of",
        "or",
        "the",
        "to",
        "with",
    }
    meaningful = [word for word in words if word not in stopwords]
    return bool(meaningful) and all(word in plain_haystack for word in meaningful)

def _missing_terms(terms: list[str], haystack: str) -> list[str]:
    return [term for term in terms if not _term_supported(term, haystack)]

def _section_after_heading(text: str, heading: str) -> str:
    heading_re = re.compile(rf"^##\s+{re.escape(heading)}\s*$", re.MULTILINE)
    match = heading_re.search(text)
    if not match:
        return ""
    next_heading = re.search(r"^##\s+", text[match.end() :], re.MULTILINE)
    if next_heading:
        return text[match.end() : match.end() + next_heading.start()]
    return text[match.end() :]

def _split_markdown_row(row: str) -> list[str]:
    cells = row.strip().strip("|").split("|")
    return [cell.strip() for cell in cells]

def _parse_table(section: str) -> tuple[list[str], list[dict[str, str]]]:
    rows = [line for line in section.splitlines() if line.strip().startswith("|")]
    if len(rows) < 3:
        return [], []
    headers = [header.strip(" `") for header in _split_markdown_row(rows[0])]
    data_rows: list[dict[str, str]] = []
    for row in rows[2:]:
        cells = _split_markdown_row(row)
        if len(cells) != len(headers):
            continue
        data_rows.append(dict(zip(headers, cells, strict=True)))
    return headers, data_rows

def _has_raw_input_link(cell: str) -> bool:
    return "raw-input" in cell and re.search(r"\[[^\]]+\]\([^)]+\)", cell) is not None

def _fixture_failures(fixture: dict) -> list[str]:
    failures: list[str] = []
    total = int(fixture["skill_contract"]["points"])
    ledger_ids = [ledger.get("id") for ledger in fixture.get("ledgers", [])]
    if ledger_ids != EXPECTED_LEDGER_IDS:
        failures.append("forecast discipline ledgers must be ordered FDC-G001..FDC-G003")

    for ledger in fixture.get("ledgers", []):
        missing = REQUIRED_LEDGER_FIELDS - ledger.keys()
        if missing:
            failures.append(f"{ledger.get('id', '<unknown>')} missing fields: {sorted(missing)}")
            continue
        total += int(ledger["points"])
        if not (REPO_ROOT / ledger["path"]).exists():
            failures.append(f"{ledger['id']} path does not exist: {ledger['path']}")

    if not (REPO_ROOT / fixture["skill_contract"]["path"]).exists():
        failures.append("expert forecast ledger draft skill path does not exist")

    if total != EXPECTED_SCORE:
        failures.append(f"fixture points must total {EXPECTED_SCORE}, got {total}")

    if fixture.get("allowed_statuses") != ["open", "held", "weakened", "contradiction"]:
        failures.append("allowed_statuses must preserve canonical forecast ledger vocabulary")

    return failures

def _check_skill_contract(fixture: dict) -> list[str]:
    contract = fixture["skill_contract"]
    text = (REPO_ROOT / contract["path"]).read_text(encoding="utf-8")
    return _missing_terms(contract["must_cover"], _normalize(text))

def _check_ledger(ledger: dict, allowed_statuses: list[str]) -> list[str]:
    text = (REPO_ROOT / ledger["path"]).read_text(encoding="utf-8")
    section = _section_after_heading(text, ledger["heading"])
    if not section:
        return [f"missing ## {ledger['heading']} section"]

    headers, rows = _parse_table(section)
    failures: list[str] = []
    missing_columns = [column for column in ledger["required_columns"] if column not in headers]
    if missing_columns:
        failures.append(f"missing columns: {missing_columns}")
    if len(rows) < int(ledger["min_rows"]):
        failures.append(f"expected at least {ledger['min_rows']} rows, got {len(rows)}")

    if failures:
        return failures

    for row_number, row in enumerate(rows, start=1):
        row_id = row["id"]
        if not row_id.startswith(ledger["id_prefix"]):
            failures.append(f"row {row_number}: id {row_id!r} lacks prefix {ledger['id_prefix']}")
        if not re.match(r"\d{4}-\d{2}-\d{2}$", row["date"]):
            failures.append(f"{row_id}: invalid date {row['date']!r}")
        if not _has_raw_input_link(row["essay"]):
            failures.append(f"{row_id}: essay must link to raw-input")
        for column in ("mechanism", "falsifier", "revisit", "status"):
            if not row[column].strip():
                failures.append(f"{row_id}: empty {column}")
        if row["status"].strip(" `") not in allowed_statuses:
            failures.append(f"{row_id}: invalid status {row['status']!r}")
        if row["status"].strip(" `") == "held":
            support_text = " ".join([row.get("notes", ""), row.get("mechanism", "")]).lower()
            if not any(term in support_text for term in ("later", "corpus", "essays", "reuse", "confirm")):
                failures.append(f"{row_id}: held status lacks in-corpus support language")

    return failures

def _score_fixture(fixture: dict) -> tuple[int, list[str], list[str]]:
    score = 0
    misses: list[str] = []
    critical_failures: list[str] = []

    skill_missing = _check_skill_contract(fixture)
    if skill_missing:
        message = f"skill contract missing: {skill_missing}"
        misses.append(message)
        if fixture["skill_contract"]["critical"]:
            critical_failures.append(message)
    else:
        score += int(fixture["skill_contract"]["points"])

    for ledger in fixture["ledgers"]:
        failures = _check_ledger(ledger, fixture["allowed_statuses"])
        if failures:
            message = f"{ledger['id']} {ledger['speaker']} ledger failures: {failures}"
            misses.append(message)
            if ledger["critical"]:
                critical_failures.append(message)
        else:
            score += int(ledger["points"])

    return score, misses, critical_failures

def _status(score: int, critical_failures: list[str], fixture: dict) -> str:
    if critical_failures:
        return "FAIL"
    if score >= int(fixture["score_bands"]["pass"]):
        return "PASS"
    if score >= int(fixture["score_bands"]["warn"]):
        return "WARN"
    return "FAIL"

def test_forecast_discipline_fixture_integrity() -> None:
    fixture = _load_fixture()
    failures = _fixture_failures(fixture)
    assert not failures, "\n".join(failures)

def test_forecast_discipline_contract_passes() -> None:
    fixture = _load_fixture()
    fixture_failures = _fixture_failures(fixture)
    assert not fixture_failures, "\n".join(fixture_failures)

    score, misses, critical_failures = _score_fixture(fixture)
    status = _status(score, critical_failures, fixture)
    summary = f"Forecast discipline contract: {score}/100 {status}"
    print(summary)

    assert status == "PASS", "\n".join([summary, *critical_failures, *misses])
    assert not misses, "\n".join(misses)
