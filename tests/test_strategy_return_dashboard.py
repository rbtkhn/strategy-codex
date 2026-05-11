"""Tests for the derived Strategy return HTML dashboard."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import render_strategy_return_dashboard as dash  # noqa: E402


def _fixture_repo(tmp_path: Path) -> Path:
    repo = tmp_path
    inbox = repo / "codex" / "daily-strategy-inbox.md"
    status = repo / "codex" / "STATUS.md"
    raw_root = repo / "codex" / "2026" / "raw-input"
    days = repo / "codex" / "2026" / "chapters" / "2026-04" / "days.md"
    raw_file = raw_root / "2026-05-09" / "matched.md"
    inbox.parent.mkdir(parents=True)
    raw_file.parent.mkdir(parents=True)
    days.parent.mkdir(parents=True)
    inbox.write_text(
        """# Daily strategy inbox

**Accumulator for:** 2026-05-08

_(Append below this line during the day.)_

- batch-analysis | theme | synthesis-ready cluster
- source | cold: unmatched | https://example.substack.com/p/unmatched | verify:pending-primary
- open loop: revisit falsifier
""",
        encoding="utf-8",
    )
    status.write_text("| **Active chapter** | `2026-04` |\n", encoding="utf-8")
    days.write_text("# days\n", encoding="utf-8")
    raw_file.write_text(
        """---
source_url: https://example.substack.com/p/matched
---
body
""",
        encoding="utf-8",
    )
    return repo


def test_dashboard_contains_warning_provenance_and_counts(tmp_path: Path) -> None:
    repo = _fixture_repo(tmp_path)
    ctx = dash.build_dashboard_context(
        repo,
        generated_at="2026-05-09T10:00:00-06:00",
        today=dash.date(2026, 5, 9),
    )
    html = dash.render_dashboard_html(ctx)

    assert "Non-canonical / derived / rebuildable" in html
    assert "No files were mutated by this dashboard" in html
    assert "codex/daily-strategy-inbox.md" in html
    assert "codex/STATUS.md" in html
    assert "codex/2026/raw-input" in html
    assert "scripts/strategy_return_hint.py" in html
    assert ">1</strong>" in html
    assert "Accumulator drift" in html
    assert ">+1d<" in html
    assert "source hygiene first" in html
    assert "stale - accumulator is" in html
    assert "https://example.substack.com/p/unmatched" in html


def test_write_dashboard_writes_only_requested_output(tmp_path: Path) -> None:
    repo = _fixture_repo(tmp_path)
    output = tmp_path / "artifacts" / "work-strategy" / "strategy-return-dashboard.html"

    written = dash.write_dashboard(repo, output)

    assert written == output
    assert output.is_file()
    assert "Strategy Return Dashboard" in output.read_text(encoding="utf-8")
    assert (repo / "codex" / "daily-strategy-inbox.md").read_text(encoding="utf-8").startswith(
        "# Daily strategy inbox"
    )


def test_accumulator_status_handles_unknown_and_future() -> None:
    assert dash.accumulator_status(None).startswith("unknown")
    assert dash.accumulator_status("not-a-date").startswith("unknown - accumulator date is malformed")
    assert dash.accumulator_status("2026-05-10", today=dash.date(2026, 5, 9)).startswith("future-dated")
    assert dash.accumulator_drift_label(None) == "unknown"
    assert dash.accumulator_drift_label(0) == "0d"
    assert dash.accumulator_drift_label(2) == "+2d"
    assert dash.accumulator_drift_label(-3) == "-3d"
