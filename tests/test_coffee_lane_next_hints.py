"""Tests for coffee_lane_next_hints (work-dev + singularity one-liners)."""

from __future__ import annotations

from pathlib import Path

from scripts.coffee_lane_next_hints import (
    format_lane_next_hints,
    next_academy_singularity_line,
    next_work_dev_line,
)


def test_next_work_dev_finds_first_open_item(tmp_path: Path) -> None:
    ws = tmp_path / "docs/skill-work/work-dev"
    ws.mkdir(parents=True)
    (ws / "workspace.md").write_text(
        """# workspace

## Next actions

1. ~~done item~~
2. Ship the widget
3. Another thing
""",
        encoding="utf-8",
    )
    line = next_work_dev_line(tmp_path)
    assert "Ship the widget" in line
    assert "#2" in line or "(#2)" in line


def test_next_work_dev_all_struck(tmp_path: Path) -> None:
    ws = tmp_path / "docs/skill-work/work-dev"
    ws.mkdir(parents=True)
    (ws / "workspace.md").write_text(
        """## Next actions

1. ~~only struck~~
""",
        encoding="utf-8",
    )
    line = next_work_dev_line(tmp_path)
    assert "no open item" in line


def test_next_academy_singularity_prefers_marked_override(tmp_path: Path) -> None:
    sdir = tmp_path / "singularity/workshop/sheets"
    sdir.mkdir(parents=True)
    (sdir / "coffee-d-singularity.md").write_text(
        """## Coffee D Next Action

- **Route class:** `control-plane`
- **Source:** `singularity/workshop/sheets/agent-control-plane.md`
- **Reason:** the live pressure is objective, memory, permissions, and rollback clarity.
""",
        encoding="utf-8",
    )
    line = next_academy_singularity_line(tmp_path)
    assert "[control-plane]" in line
    assert "agent-control-plane.md" in line
    assert "rollback clarity" in line


def test_next_academy_singularity_falls_back_to_bridge_when_present(tmp_path: Path) -> None:
    sdir = tmp_path / "singularity/workshop/sheets"
    sdir.mkdir(parents=True)
    (sdir / "sovereignty-under-acceleration.md").write_text("# bridge\n", encoding="utf-8")
    line = next_academy_singularity_line(tmp_path)
    assert "[statecraft-bridge]" in line
    assert "sovereignty-under-acceleration.md" in line
    assert "institutional carrier" in line


def test_next_academy_singularity_falls_back_to_latest_innermost_loop(tmp_path: Path) -> None:
    sdir = tmp_path / "singularity/workshop/sheets"
    sdir.mkdir(parents=True)
    (sdir / "innermost-loop-2026-05-15.md").write_text("# old\n", encoding="utf-8")
    (sdir / "innermost-loop-2026-05-17.md").write_text("# new\n", encoding="utf-8")
    line = next_academy_singularity_line(tmp_path)
    assert "[pulse]" in line
    assert "innermost-loop-2026-05-17.md" in line


def test_next_academy_singularity_falls_back_to_workshop_readme(tmp_path: Path) -> None:
    wdir = tmp_path / "singularity/workshop"
    wdir.mkdir(parents=True)
    (wdir / "README.md").write_text("# workshop\n", encoding="utf-8")
    line = next_academy_singularity_line(tmp_path)
    assert "[reuse]" in line
    assert "singularity/workshop/README.md" in line


def test_format_lane_next_hints_two_lines(tmp_path: Path) -> None:
    ws = tmp_path / "docs/skill-work/work-dev"
    ws.mkdir(parents=True)
    (ws / "workspace.md").write_text("## Next actions\n\n1. Alpha\n", encoding="utf-8")
    sdir = tmp_path / "singularity/workshop/sheets"
    sdir.mkdir(parents=True)
    (sdir / "coffee-d-singularity.md").write_text(
        """## Coffee D Next Action

- **Route class:** `warning`
- **Source:** `singularity/workshop/sheets/sovereignty-under-acceleration.md`
- **Reason:** ceremonial control is the visible risk.
""",
        encoding="utf-8",
    )
    out = format_lane_next_hints(tmp_path)
    lines = out.strip().splitlines()
    assert len(lines) == 2
    assert "Alpha" in lines[0]
    assert "[warning]" in lines[1]


def test_assess_session_load_includes_menu_weights() -> None:
    from scripts.assess_session_load import assess_load

    r = assess_load("grace-mar")
    ow = r.get("option_weights") or {}
    assert set(ow.keys()) == {"A", "B", "C", "D"}
    assert r.get("recommended") in ("A", "B", "C")
