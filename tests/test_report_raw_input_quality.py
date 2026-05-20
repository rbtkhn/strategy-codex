from __future__ import annotations

from pathlib import Path

import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import report_raw_input_quality as report_quality  # noqa: E402


def _notebook(tmp_path: Path) -> Path:
    notebook_root = tmp_path / "codex" / "2026"
    obj = notebook_root / "speakers" / "scott-ritter" / "scott-ritter-speaker-object.md"
    obj.parent.mkdir(parents=True, exist_ok=True)
    obj.write_text("# Scott Ritter\n", encoding="utf-8")
    arc = notebook_root / "davis" / "davis-scott-ritter-speaker-arc.md"
    arc.parent.mkdir(parents=True, exist_ok=True)
    arc.write_text("# Davis x Scott Ritter\n", encoding="utf-8")
    return notebook_root


def _write_raw(
    notebook_root: Path,
    name: str,
    *,
    legacy: bool = False,
    bom: bool = False,
    body: str = "Welcome back. " + " ".join(f"word{i}" for i in range(80)),
) -> Path:
    raw = notebook_root / "raw-input" / "2026-04-12" / f"{name}.md"
    raw.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "---",
        "ingest_date: 2026-05-18",
        "pub_date: 2026-04-12",
        "kind: transcript",
        f"title: {name}",
        "source_url: https://www.youtube.com/watch?v=abcdefghijk",
        "host: Daniel Davis",
        "show: Daniel Davis",
        "thread: davis",
        "guest: Scott Ritter",
    ]
    if not legacy:
        fields.extend(
            [
                "source_type: youtube",
                "transcript_type: auto_subtitles_vtt",
                "editorial_note: Subtitle-derived transcript.",
            ]
        )
    else:
        fields.append("source_note: Legacy automated transcript fetch.")
    fields.extend(["---", "", f"# {name}", "", body])
    raw.write_text("\n".join(fields) + "\n", encoding="utf-8-sig" if bom else "utf-8")
    return raw


def test_report_raw_input_quality_reports_item_and_host_month_closeout(tmp_path: Path) -> None:
    notebook_root = _notebook(tmp_path)
    raw = _write_raw(notebook_root, "bearing")

    report = report_quality.build_report(raw, notebook_root=notebook_root, output_root=tmp_path / "quality")
    markdown = report_quality.render_markdown(report)

    assert report["evidence_grade"] == "transcript-bearing"
    assert report["routeable"] is True
    assert report["unresolved"] is False
    assert report["legacy_transcript_warning"] == ""
    assert "Purity: +1 transcript-valid / 100.0%" in report["host_month_closeout"]
    assert "- evidence grade: `transcript-bearing`" in markdown
    assert "- routeable: yes; unresolved speaker: no" in markdown


def test_report_raw_input_quality_warns_when_body_is_legacy_classified(tmp_path: Path) -> None:
    notebook_root = _notebook(tmp_path)
    raw = _write_raw(notebook_root, "legacy", legacy=True)

    report = report_quality.build_report(raw, notebook_root=notebook_root, output_root=tmp_path / "quality")
    markdown = report_quality.render_markdown(report)

    assert report["evidence_grade"] == "legacy-appearance-only"
    assert report["word_count"] > 0
    assert "metadata classifies this as `legacy-appearance-only`" in report["legacy_transcript_warning"]
    assert "do not call it transcript-valid" in markdown


def test_report_raw_input_quality_accepts_bom_frontmatter(tmp_path: Path) -> None:
    notebook_root = _notebook(tmp_path)
    raw = _write_raw(notebook_root, "bom-bearing", bom=True)

    report = report_quality.build_report(raw, notebook_root=notebook_root, output_root=tmp_path / "quality")

    assert report["host"] == "davis"
    assert report["evidence_grade"] == "transcript-bearing"


def test_report_raw_input_quality_does_not_warn_for_metadata_only_stub(tmp_path: Path) -> None:
    notebook_root = _notebook(tmp_path)
    raw = _write_raw(notebook_root, "metadata-only", legacy=True, body="")

    report = report_quality.build_report(raw, notebook_root=notebook_root, output_root=tmp_path / "quality")

    assert report["evidence_grade"] == "legacy-appearance-only"
    assert report["legacy_transcript_warning"] == ""


def test_report_raw_input_quality_surfaces_residual_noise_terms(tmp_path: Path) -> None:
    notebook_root = _notebook(tmp_path)
    raw = _write_raw(
        notebook_root,
        "noisy-bearing",
        body=(
            "Welcome back. Scott Ritterder says flights from Pulkava matter while "
            "the Kaggon of doctrine is debated near Thrron. "
            + " ".join(f"word{i}" for i in range(80))
        ),
    )

    report = report_quality.build_report(raw, notebook_root=notebook_root, output_root=tmp_path / "quality")
    markdown = report_quality.render_markdown(report)

    assert report["residual_noise_terms"] == [
        "Kaggon of doctrine",
        "Pulkava",
        "Ritterder",
        "Thrron",
    ]
    assert "- residual noise: `Kaggon of doctrine`, `Pulkava`, `Ritterder`, `Thrron`" in markdown
