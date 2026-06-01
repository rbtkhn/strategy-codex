from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import audit_hormuz_mistranscriptions as audit  # noqa: E402


def test_find_direct_findings_catches_first_wave_variants() -> None:
    body = (
        "Iran can shut the straight of hormones.\n"
        "They also discussed the trade of hormones.\n"
        "And then the straight of\n"
        "Hormos becomes the choke point.\n"
    )

    findings = audit.find_direct_findings(REPO_ROOT / "source-archive" / "statecraft" / "2026-02-17" / "sample.md", body)

    matches = {finding.match_text for finding in findings}
    assert "straight of hormones" in matches
    assert "trade of hormones" in matches
    assert "straight of / Hormos" in matches
    assert all(finding.suspected_target == "Strait of Hormuz" for finding in findings)


def test_find_direct_findings_catches_second_wave_phrase_variants() -> None:
    body = (
        "The state of armus matters for regional escalation.\n"
        "They also discussed the street of armors and the straight of Armoose.\n"
        "Trump mentioned the straight of foremost while others warned about the trade of formos.\n"
        "Another guest referred to the straight of Barmuz.\n"
    )

    findings = audit.find_direct_findings(REPO_ROOT / "source-archive" / "statecraft" / "2026-05-16" / "sample.md", body)

    matches = {finding.match_text for finding in findings}
    assert "state of armus" in matches
    assert "street of armors" in matches
    assert "straight of Armoose" in matches
    assert "straight of foremost" in matches
    assert "trade of formos" in matches
    assert "straight of Barmuz" in matches
    assert all(finding.tier == "high_confidence" for finding in findings)


def test_find_direct_findings_catches_hermuz_and_hormuse_family() -> None:
    body = (
        "The Straits of Hermuz remain blocked.\n"
        "Another line said the straits of Hormuse stayed closed.\n"
        "A third speaker warned the straight of Hormuse could crash the market.\n"
        "One messy transcript even said the street Hermuz was contested.\n"
    )

    findings = audit.find_direct_findings(REPO_ROOT / "source-archive" / "statecraft" / "2026-03-04" / "sample.md", body)

    matches = {finding.match_text for finding in findings}
    assert "Straits of Hermuz" in matches
    assert "straits of Hormuse" in matches
    assert "straight of Hormuse" in matches
    assert "street Hermuz" in matches
    assert all(finding.tier == "high_confidence" for finding in findings)


def test_find_direct_findings_does_not_promote_clipped_her_fragment() -> None:
    body = "Oman may collect tolls from the straight of her with Iran."

    findings = audit.find_direct_findings(REPO_ROOT / "source-archive" / "statecraft" / "2026-05-27" / "sample.md", body)

    assert findings == []


def test_find_direct_findings_ignores_correct_mentions() -> None:
    body = (
        "The Strait of Hormuz matters.\n"
        "Shipping through the Straits of Hormuz remains open.\n"
    )

    findings = audit.find_direct_findings(REPO_ROOT / "source-archive" / "statecraft" / "2026-03-01" / "sample.md", body)

    assert findings == []


def test_find_direct_findings_labels_generic_noun_flattening() -> None:
    body = "Managed traffic continued in the street of Ormuz."

    findings = audit.find_direct_findings(REPO_ROOT / "source-archive" / "statecraft" / "2026-05-18" / "sample.md", body)

    assert len(findings) == 1
    assert findings[0].tier == "high_confidence"
    assert findings[0].reason_code == "generic_noun_flattening"


def test_find_direct_findings_uses_medium_for_weaker_phonetic_variant() -> None:
    body = "The navy cannot reopen the straight of Hormone under these conditions."

    findings = audit.find_direct_findings(REPO_ROOT / "source-archive" / "statecraft" / "2026-03-11" / "sample.md", body)

    assert len(findings) == 1
    assert findings[0].tier == "medium_confidence"
    assert findings[0].reason_code == "phonetic_variant"


def test_context_only_for_hormuz_titled_transcript_without_direct_variant(tmp_path: Path) -> None:
    path = tmp_path / "transcript-johnson-hormuz-example.md"
    text = (
        "---\n"
        'title: "Johnson on Hormuz and shipping"\n'
        "kind: transcript\n"
        "source_type: youtube\n"
        "---\n\n"
        "# Johnson on Hormuz and shipping\n\n"
        "The waterway stayed open for tankers and oil traffic while Iran kept pressure on shipping.\n"
    )
    path.write_text(text, encoding="utf-8")

    findings = audit.audit_path(path)

    assert len(findings) == 1
    assert findings[0].tier == "context_only"
    assert findings[0].reason_code == "title_body_divergence"


def test_context_only_skips_when_body_already_mentions_hormuz(tmp_path: Path) -> None:
    path = tmp_path / "transcript-johnson-hormuz-clean-body.md"
    text = (
        "---\n"
        'title: "Johnson on Hormuz and shipping"\n'
        "kind: transcript\n"
        "source_type: youtube\n"
        "---\n\n"
        "# Johnson on Hormuz and shipping\n\n"
        "Traffic through the Strait of Hormuz stayed open while Iran kept pressure on shipping.\n"
    )
    path.write_text(text, encoding="utf-8")

    findings = audit.audit_path(path)

    assert findings == []


def test_context_only_skips_when_title_body_divergence_is_reviewed(tmp_path: Path) -> None:
    path = tmp_path / "transcript-johnson-hormuz-reviewed.md"
    text = (
        "---\n"
        'title: "Johnson on Hormuz and shipping"\n'
        "kind: transcript\n"
        "source_type: youtube\n"
        'editorial_note: "Title-body divergence reviewed: source-owned Hormuz title retained; transcript body contains no direct Hormuz phrase."\n'
        "---\n\n"
        "# Johnson on Hormuz and shipping\n\n"
        "The waterway stayed open for tankers and oil traffic while Iran kept pressure elsewhere.\n"
    )
    path.write_text(text, encoding="utf-8")

    findings = audit.audit_path(path)

    assert findings == []


def test_audit_excludes_non_transcript_docs(tmp_path: Path) -> None:
    path = tmp_path / "note.md"
    path.write_text("# Notes\n\nThe straight of hormones appears in this essay example.\n", encoding="utf-8")

    findings = audit.audit_path(path)

    assert findings == []


def test_main_writes_json_and_markdown_outputs(tmp_path: Path) -> None:
    root = tmp_path / "source-archive" / "statecraft" / "2026-02-17"
    root.mkdir(parents=True)
    transcript = root / "transcript-example.md"
    transcript.write_text(
        "---\n"
        'title: "Example on Hormuz"\n'
        "kind: transcript\n"
        "source_type: youtube\n"
        "---\n\n"
        "# Example on Hormuz\n\n"
        "Iran discussed the straight of hormones and oil traffic.\n",
        encoding="utf-8",
    )
    output_dir = tmp_path / "artifacts"

    rc = audit.main(
        [
            "--root",
            str(tmp_path / "source-archive" / "statecraft"),
            "--output-dir",
            str(output_dir),
            "--prefix",
            "unit-hormuz",
        ]
    )

    assert rc == 0
    json_path = output_dir / "unit-hormuz.json"
    md_path = output_dir / "unit-hormuz.md"
    assert json_path.is_file()
    assert md_path.is_file()
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload["summary"]["candidate_files"] == 1
    assert payload["summary"]["total_findings"] >= 1
    assert "straight of hormones" in md_path.read_text(encoding="utf-8")


def test_main_accepts_relative_output_dir(tmp_path: Path, monkeypatch) -> None:
    root = tmp_path / "source-archive" / "statecraft" / "2026-02-17"
    root.mkdir(parents=True)
    transcript = root / "transcript-example.md"
    transcript.write_text(
        "---\n"
        'title: "Example on Hormuz"\n'
        "kind: transcript\n"
        "source_type: youtube\n"
        "---\n\n"
        "# Example on Hormuz\n\n"
        "Iran discussed the straight of hormones and oil traffic.\n",
        encoding="utf-8",
    )

    original_root = audit.REPO_ROOT
    monkeypatch.chdir(tmp_path)
    audit.REPO_ROOT = tmp_path
    try:
        rc = audit.main(
            [
                "--root",
                str(tmp_path / "source-archive" / "statecraft"),
                "--output-dir",
                "artifacts",
                "--prefix",
                "unit-hormuz-relative",
            ]
        )
    finally:
        audit.REPO_ROOT = original_root

    assert rc == 0
    json_path = tmp_path / "artifacts" / "unit-hormuz-relative.json"
    md_path = tmp_path / "artifacts" / "unit-hormuz-relative.md"
    assert json_path.is_file()
    assert md_path.is_file()
