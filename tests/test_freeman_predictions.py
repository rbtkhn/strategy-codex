"""Tests for Freeman prediction record — colocated JSON + public markdown."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
JSON_PATH = REPO_ROOT / "statecraft" / "voices" / "freeman" / "freeman-predictions.json"
MD_PATH = REPO_ROOT / "statecraft" / "voices" / "freeman" / "freeman-predictions.md"
CAPTURE_MAP = REPO_ROOT / "statecraft" / "data" / "freeman-prediction-capture-map.json"
PUBLIC_MAP = REPO_ROOT / "statecraft" / "data" / "freeman-prediction-public-map.json"

if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import check_voice_predictions as checker  # noqa: E402
from voice_prediction_pilot import (  # noqa: E402
    FREEMAN_PILOT_EVENT_ORDER,
    get_voice_config,
    load_capture_map,
    load_public_map,
    validate_capture_row,
)

DISALLOWED_EXCEPTIONS = {
    "under_30_verified",
    "summary_grade_capture",
    "stub_capture",
    "rhetorical_analogy",
}


def test_freeman_capture_map_exists() -> None:
    assert CAPTURE_MAP.is_file()
    data = json.loads(CAPTURE_MAP.read_text(encoding="utf-8"))
    assert len(data["rows"]) == 36


def test_freeman_predictions_json_exists() -> None:
    assert JSON_PATH.is_file()
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    assert data["speaker"] == "freeman"
    assert len(data["events"]) == 7
    assert data["_meta"].get("schema") == "freeman-predictions-v3"


def test_freeman_events_have_anchor_excerpts() -> None:
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    for event in data["events"]:
        assert str(event.get("anchor_excerpt") or "").strip()
        cite = event.get("anchor_citation") or {}
        assert cite.get("title")
        assert "youtube_url" in cite


def test_freeman_appearances_have_excerpts() -> None:
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    for event in data["events"]:
        for app in event["appearances"]:
            assert str(app.get("public_excerpt") or "").strip()
            assert str(app.get("public_excerpt_short") or "").strip()
            assert "youtube_url" in (app.get("citation") or {})


def test_freeman_predictions_markdown_public_structure() -> None:
    text = MD_PATH.read_text(encoding="utf-8")
    for needle in (
        "# Chas Freeman Prediction Record",
        "## At a Glance",
        "## Method",
        "<details>",
        "<summary>Source trail</summary>",
        "— Chas Freeman,",
    ):
        assert needle in text


def test_freeman_predictions_builder_check() -> None:
    proc = subprocess.run(
        ["python3", "scripts/build_freeman_predictions.py", "--check"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout


def test_excerpt_in_capture_requires_full_substring() -> None:
    from voice_prediction_pilot import excerpt_in_capture

    body = (
        "alpha beta gamma delta epsilon zeta eta theta but loses his own soul "
        "israel continues"
    )
    good = "alpha beta gamma delta epsilon zeta eta theta but loses his own soul"
    bad = "alpha beta gamma delta epsilon zeta eta theta and loses his own soul"
    assert excerpt_in_capture(good, body)
    assert not excerpt_in_capture(bad, body)


def test_freeman_predictions_shape_checker() -> None:
    config = get_voice_config("freeman")
    issues, _ = checker.run_check(
        config=config,
        json_path=JSON_PATH,
        md_path=MD_PATH,
    )
    assert not issues


def test_public_map_prediction_object_terms() -> None:
    public_map = load_public_map(PUBLIC_MAP)
    for event_id in FREEMAN_PILOT_EVENT_ORDER:
        terms = public_map[event_id].get("prediction_object_terms")
        assert isinstance(terms, list) and terms


def test_capture_map_disallowed_exceptions_removed() -> None:
    rows = json.loads(CAPTURE_MAP.read_text(encoding="utf-8"))["rows"]
    for row in rows:
        assert row.get("excerpt_exception") not in DISALLOWED_EXCEPTIONS


def test_gaza_hostage_anchor_names_object() -> None:
    public_map = load_public_map(PUBLIC_MAP)
    rows = json.loads(CAPTURE_MAP.read_text(encoding="utf-8"))["rows"]
    anchor_capture = public_map["gaza_hostage_deal_jan_2025"]["anchor_capture"]
    anchor_row = next(
        r
        for r in rows
        if r["event_id"] == "gaza_hostage_deal_jan_2025" and r["capture"] == anchor_capture
    )
    excerpt = anchor_row["public_excerpt"].casefold()
    terms = anchor_row.get("prediction_object_terms") or public_map[
        "gaza_hostage_deal_jan_2025"
    ].get("prediction_object_terms", [])
    assert any(str(term).casefold() in excerpt for term in terms) or any(
        term.casefold() in excerpt for term in ("hostage", "hostages", "ceasefire", "deal", "trump", "settlement")
    )


def test_short_anchor_context_note_in_outputs() -> None:
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    md = MD_PATH.read_text(encoding="utf-8")
    china = next(e for e in data["events"] if e["event_id"] == "china_tariff_capitulation_2025")
    note = str(china.get("anchor_context_note") or "").strip()
    assert note
    assert note in md
    assert china["anchor_excerpt"] in md


def test_no_host_only_rows_render_as_freeman_quotes() -> None:
    rows = load_capture_map(CAPTURE_MAP, guest_speaker="freeman")
    md = MD_PATH.read_text(encoding="utf-8")
    for row in rows:
        if row.get("quote_speaker") != "host" or row.get("public_display", True):
            continue
        excerpt = str(row.get("public_excerpt") or row.get("public_excerpt_raw") or "").strip()
        if not excerpt:
            continue
        needle = excerpt[: min(32, len(excerpt))].replace('"', "")
        assert ('> "' + needle) not in md


def test_mixed_rows_have_host_setup_and_context() -> None:
    rows = load_capture_map(CAPTURE_MAP, guest_speaker="freeman")
    mixed = [r for r in rows if r.get("quote_speaker") == "mixed"]
    assert mixed, "expected at least one mixed row"
    for row in mixed:
        assert str(row.get("host_setup") or "").strip()
        assert str(row.get("context_note") or "").strip()


def test_public_rows_have_asr_repair_metadata() -> None:
    rows = load_capture_map(CAPTURE_MAP, guest_speaker="freeman")
    for row in rows:
        if not row.get("public_display", True):
            continue
        if row.get("quote_speaker") in {"host", "operator_summary"}:
            continue
        assert row.get("asr_repair") in {
            "none",
            "punctuation_capitalization",
            "punctuation_capitalization_filler_boundary",
            "punctuation_capitalization_obvious_asr",
            "not_public_verbatim",
        }
        assert "public_excerpt_raw" in row and str(row["public_excerpt_raw"]).strip()


def test_obvious_asr_fragments_rejected() -> None:
    public_map = load_public_map(PUBLIC_MAP)
    body = "Israel is is in the process of destroying itself rather"
    row = {
        "event_id": "israel_self_destruction_trajectory",
        "capture": "source-archive/statecraft/2025-01-07/source-judging-freedom-amb-chas-freeman-is-israel-destroying-itself-2025-01-07.md",
        "stance": "yes",
        "speech_act": "initial",
        "public_excerpt": "Israel is is in the process of destroying itself rather",
        "public_excerpt_raw": "Israel is is in the process of destroying itself rather",
        "quote_speaker": "freeman",
        "public_display": True,
        "asr_repair": "none",
    }
    errors = validate_capture_row(
        row,
        body,
        public_map["israel_self_destruction_trajectory"],
        guest_speaker="freeman",
    )
    assert any("ASR fragment" in err for err in errors)


def test_non_public_rows_not_rendered_in_markdown() -> None:
    rows = load_capture_map(CAPTURE_MAP, guest_speaker="freeman")
    md = MD_PATH.read_text(encoding="utf-8")
    hidden = [r for r in rows if not r.get("public_display", True)]
    assert hidden, "expected non-public rows"
    for row in hidden:
        excerpt = str(row.get("public_excerpt") or "").strip()
        if excerpt and len(excerpt) > 20:
            assert excerpt not in md or row.get("quote_speaker") in {"host", "operator_summary"}


def test_bootstrap_capture_map_check() -> None:
    proc = subprocess.run(
        ["python3", "scripts/bootstrap_freeman_capture_map.py", "--check"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout
