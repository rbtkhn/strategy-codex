from __future__ import annotations

import json
from pathlib import Path

import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import host_shelf_quality as quality  # noqa: E402


def _caption(words: int = 90) -> str:
    return " ".join(f"word{i}" for i in range(words))


def _write_raw(
    notebook_root: Path,
    name: str,
    *,
    pub_date: str = "2026-04-12",
    kind: str = "transcript",
    source_type: str = "youtube",
    transcript_type: str = "auto_subtitles_vtt",
    guest: str = "Scott Ritter",
    host: str = "Daniel Davis",
    body_words: int = 90,
    body_text: str | None = None,
    normalization_state: str = "",
    quality_note: str = "",
) -> Path:
    raw = notebook_root / "raw-input" / pub_date / f"{name}.md"
    raw.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "---",
        "ingest_date: 2026-05-15",
        f"pub_date: {pub_date}",
        f"kind: {kind}",
        f"title: {name}",
        f"source_url: https://www.youtube.com/watch?v={name[:11].ljust(11, 'x')}",
        f"host: {host}",
        f"show: {host}",
        "thread: davis",
    ]
    if source_type:
        fields.append(f"source_type: {source_type}")
    if transcript_type:
        fields.append(f"transcript_type: {transcript_type}")
    if guest:
        fields.append(f"guest: {guest}")
    if normalization_state:
        fields.append(f"normalization_state: {normalization_state}")
    if quality_note:
        fields.append(f"quality_note: {quality_note}")
    fields.extend(["---", "", f"# {name}", "", body_text or _caption(body_words)])
    raw.write_text("\n".join(fields) + "\n", encoding="utf-8")
    return raw


def _notebook(tmp_path: Path) -> Path:
    notebook_root = tmp_path / "codex" / "2026"
    obj = notebook_root / "speakers" / "scott-ritter" / "scott-ritter-speaker-object.md"
    obj.parent.mkdir(parents=True, exist_ok=True)
    obj.write_text("# Scott Ritter\n", encoding="utf-8")
    arc = notebook_root / "davis" / "davis-scott-ritter-speaker-arc.md"
    arc.parent.mkdir(parents=True, exist_ok=True)
    arc.write_text("# Davis x Scott Ritter\n", encoding="utf-8")
    return notebook_root


def test_quality_counts_all_grades_and_excludes_summary_and_legacy_from_valid_percent(tmp_path: Path) -> None:
    notebook_root = _notebook(tmp_path)
    paths = [
        _write_raw(notebook_root, "manual", transcript_type="manual_subtitles_vtt"),
        _write_raw(notebook_root, "cleaned", kind="cleaned-transcript", transcript_type="cleaned_transcript"),
        _write_raw(notebook_root, "bearing"),
        _write_raw(notebook_root, "summary", source_type="operator-note-derived-youtube", transcript_type="operator_summary"),
        _write_raw(notebook_root, "legacy", source_type="", transcript_type=""),
    ]

    summary = quality.build_quality_summary(
        host="davis",
        year=2026,
        month_label="2026-04",
        raw_paths=paths,
        notebook_root=notebook_root,
    )

    assert summary["routeable_artifact_count"] == 5
    assert summary["counts"] == {
        "transcript-grade": 1,
        "cleaned-transcript": 1,
        "transcript-bearing": 1,
        "summary-grade": 1,
        "legacy-appearance-only": 1,
    }
    assert summary["transcript_valid_count"] == 3
    assert summary["transcript_valid_percent"] == 60.0
    assert summary["input_scope"] == "provided-paths"


def test_unresolved_speaker_rows_are_counted_but_not_routeable(tmp_path: Path) -> None:
    notebook_root = _notebook(tmp_path)
    paths = [
        _write_raw(notebook_root, "routeable"),
        _write_raw(notebook_root, "unresolved", guest=""),
    ]

    summary = quality.build_quality_summary(
        host="davis",
        year=2026,
        month_label="2026-04",
        raw_paths=paths,
        notebook_root=notebook_root,
    )

    assert summary["raw_input_count"] == 2
    assert summary["routeable_artifact_count"] == 1
    assert summary["unresolved_speaker_count"] == 1
    assert summary["counts"]["transcript-bearing"] == 2


def test_prior_artifact_comparison_produces_structure_and_purity_deltas(tmp_path: Path) -> None:
    notebook_root = _notebook(tmp_path)
    output_root = tmp_path / "artifacts" / "host-shelf-quality"
    first = [_write_raw(notebook_root, "first")]

    quality.write_quality_summary(
        host="davis",
        year=2026,
        month_label="2026-04",
        raw_paths=first,
        notebook_root=notebook_root,
        output_root=output_root,
    )
    second = first + [_write_raw(notebook_root, "second", transcript_type="manual_subtitles_vtt")]
    summary = quality.write_quality_summary(
        host="davis",
        year=2026,
        month_label="2026-04",
        raw_paths=second,
        notebook_root=notebook_root,
        output_root=output_root,
    )

    assert summary["deltas"]["routeable_artifact_count"] == 1
    assert summary["deltas"]["transcript_valid_count"] == 1
    assert "Structure: +1 routeable" in summary["closeout_line"]


def test_residual_noise_and_normalization_state_are_reported(tmp_path: Path) -> None:
    notebook_root = _notebook(tmp_path)
    paths = [
        _write_raw(
            notebook_root,
            "noisy",
            body_text="Cining met Tajjikistan officials while Rigul discussed energy liquidity.",
            normalization_state="proper-noun-pass",
            quality_note="Known residual noisy forms remain after scoped cleanup.",
        )
    ]

    summary = quality.build_quality_summary(
        host="davis",
        year=2026,
        month_label="2026-04",
        raw_paths=paths,
        notebook_root=notebook_root,
    )
    artifact = summary["artifacts"][0]
    markdown = quality.render_markdown(summary)

    assert summary["residual_noise_artifact_count"] == 1
    assert artifact["normalization_state"] == "proper-noun-pass"
    assert artifact["quality_note"] == "Known residual noisy forms remain after scoped cleanup."
    assert artifact["residual_noise_terms"] == ["Cining", "Rigul", "Tajjikistan"]
    assert "## Residual Noise" in markdown
    assert "normalization `proper-noun-pass`" in markdown


def test_write_reports_for_paths_can_expand_to_full_host_month(tmp_path: Path) -> None:
    notebook_root = _notebook(tmp_path)
    selected = _write_raw(notebook_root, "selected", pub_date="2026-04-12")
    _write_raw(notebook_root, "sibling", pub_date="2026-04-13")
    output_root = tmp_path / "artifacts" / "host-shelf-quality"

    summaries = quality.write_quality_reports_for_paths(
        [selected],
        notebook_root=notebook_root,
        output_root=output_root,
        expand_to_month=True,
    )

    assert len(summaries) == 1
    assert summaries[0]["input_scope"] == "full-host-month"
    assert summaries[0]["raw_input_count"] == 2


def test_cli_apply_writes_json_and_markdown_with_naming_warning(tmp_path: Path, capsys) -> None:
    notebook_root = _notebook(tmp_path)
    _write_raw(notebook_root, "cli")
    (notebook_root / "davis" / "davis-shelf-core.md").write_text("# Shelf\n", encoding="utf-8")
    (notebook_root / "davis" / "davis-book-legacy.md").write_text("# Book\n", encoding="utf-8")
    output_root = tmp_path / "artifacts" / "host-shelf-quality"

    rc = quality.main(
        [
            "--host",
            "davis",
            "--year",
            "2026",
            "--month",
            "2026-04",
            "--notebook-root",
            str(notebook_root),
            "--output-root",
            str(output_root),
            "--apply",
        ]
    )

    assert rc == 0
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["warnings"]
    assert (output_root / "2026" / "davis" / "2026-04" / "quality-summary.json").is_file()
    assert (output_root / "2026" / "davis" / "2026-04" / "quality-summary.md").is_file()
