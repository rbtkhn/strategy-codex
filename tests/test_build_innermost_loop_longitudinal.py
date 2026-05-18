from __future__ import annotations

import json
from pathlib import Path

import build_innermost_loop_longitudinal as longitudinal


def _capture(
    root: Path,
    day: str,
    body: str,
    *,
    url: str | None = None,
) -> Path:
    path = root / f"innermost-loop-{day}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(
            [
                "---",
                f"title_date: {day}",
                f"source_url: {url or f'https://theinnermostloop.substack.com/p/welcome-to-{day}'}",
                "---",
                "",
                f"# The Innermost Loop - {day}",
                "",
                "WORK only; not Record.",
                "",
                "## Source",
                "",
                f"- Title: Welcome to {day}",
                "",
                "## Newsletter Text",
                "",
                body,
                "",
                "_Backfilled by `scripts/backfill_innermost_loop_academy_raw.py`; local WORK copy, not Record._",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return path


def test_build_index_detects_fronts_and_keeps_source_links(tmp_path: Path) -> None:
    raw_root = tmp_path / "raw"
    _capture(
        raw_root,
        "2026-05-04",
        "Claude and GPT models hit a benchmark while an autonomous agent workflow expands.",
        url="https://example.test/may-4",
    )

    index = longitudinal.build_index(raw_root)

    assert index["coverage"]["issue_count"] == 1
    item = index["items"][0]
    assert item["date"] == "2026-05-04"
    assert item["source_url"] == "https://example.test/may-4"
    labels = [front["label"] for front in item["detected_fronts"]]
    assert "Frontier models and benchmarks" in labels
    assert "Agents and autonomy" in labels
    model_front = next(
        front for front in item["detected_fronts"] if front["slug"] == "frontier-models-and-benchmarks"
    )
    assert model_front["confidence"] == "high"
    assert model_front["matched_terms"]["claude"] == 1
    assert model_front["matched_terms"]["gpt"] == 1
    assert model_front["matched_terms"]["models"] == 1
    assert model_front["matched_terms"]["benchmark"] == 1


def test_boilerplate_is_ignored_and_gaps_are_preserved(tmp_path: Path) -> None:
    raw_root = tmp_path / "raw"
    _capture(
        raw_root,
        "2026-05-04",
        "Thanks for reading The Innermost Loop! Subscribe for free to receive new posts and support my work.",
    )
    _capture(raw_root, "2026-05-06", "A robot, humanoid vehicle, and drone made the physical layer visible.")

    index = longitudinal.build_index(raw_root)

    assert index["coverage"]["gaps"] == ["2026-05-05"]
    first = index["items"][0]
    assert first["detected_fronts"] == []
    assert first["needs_review"] is True
    second_labels = [front["label"] for front in index["items"][1]["detected_fronts"]]
    assert "Robotics and embodiment" in second_labels


def test_low_confidence_matches_are_reviewed_not_timeline_signals(tmp_path: Path) -> None:
    raw_root = tmp_path / "raw"
    _capture(raw_root, "2026-05-04", "One human concern appeared once.")

    index = longitudinal.build_index(raw_root)

    item = index["items"][0]
    assert item["needs_review"] is True
    assert item["detected_fronts"][0]["confidence"] == "low"
    assert item["detected_fronts"][0]["slug"] == "trust-provenance-and-human-meaning"
    assert index["front_timelines"]["trust-provenance-and-human-meaning"] == []


def test_run_writes_stable_outputs_and_readme_section(tmp_path: Path) -> None:
    raw_root = tmp_path / "raw"
    out_dir = tmp_path / "longitudinal"
    readme = tmp_path / "README.md"
    readme.write_text(
        "# Singularity Workshop\n\n## First Instruments To Build\n\n- Existing\n",
        encoding="utf-8",
    )
    _capture(raw_root, "2026-05-04", "Compute, chips, silicon, and energy moved together.")
    _capture(raw_root, "2026-05-06", "A lawsuit and government policy made regulation visible.")

    assert longitudinal.run(raw_root=raw_root, out_dir=out_dir, readme=readme, apply=True) == 0
    first_md = (out_dir / "innermost-loop.md").read_text(encoding="utf-8")
    first_json = (out_dir / "innermost-loop-signals.json").read_text(encoding="utf-8")
    first_readme = readme.read_text(encoding="utf-8")

    assert "## Date-by-Date" in first_md
    assert "2026-05-05" in first_md
    parsed = json.loads(first_json)
    assert parsed["coverage"]["gaps"] == ["2026-05-05"]
    assert first_readme.count("## Longitudinal Views") == 1
    assert "longitudinal/innermost-loop.md" in first_readme

    assert longitudinal.run(raw_root=raw_root, out_dir=out_dir, readme=readme, apply=True) == 0
    assert (out_dir / "innermost-loop.md").read_text(encoding="utf-8") == first_md
    assert (out_dir / "innermost-loop-signals.json").read_text(encoding="utf-8") == first_json
    assert readme.read_text(encoding="utf-8") == first_readme
