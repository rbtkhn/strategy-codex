from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import build_statecraft_day_dashboard as dash  # noqa: E402
import build_statecraft_day_indices as idx  # noqa: E402


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def test_dashboard_uses_local_day_readme_when_present(tmp_path: Path) -> None:
    root = tmp_path / "source-archive" / "statecraft"
    day = root / "2026-05-26"
    _write(
        day / "transcript-napolitano-hoh-why-the-pentagon-lies-2026-05-26.md",
        (
            "---\n"
            'title: "Matt Hoh: Why the Pentagon Lies"\n'
            "show: Judging Freedom\n"
            "host: Judge Andrew Napolitano\n"
            "guest: Matt Hoh\n"
            "thread: hoh\n"
            "---\n\n"
            "Body.\n"
        ),
    )
    idx.write_day_index(day)

    summary = dash.load_day_summary(day)

    assert summary.has_readme is True
    assert summary.readme_parse_ok is True
    assert summary.source_count == 1
    assert summary.host_counter["Andrew Napolitano"] == 1
    assert summary.guest_counter["Matt Hoh"] == 1


def test_day_readme_parser_round_trips_section_boundaries(tmp_path: Path) -> None:
    root = tmp_path / "source-archive" / "statecraft"
    day = root / "2026-05-26"
    _write(
        day / "transcript-napolitano-hoh-why-the-pentagon-lies-2026-05-26.md",
        (
            "---\n"
            'title: "Matt Hoh: Why the Pentagon Lies"\n'
            "show: Judging Freedom\n"
            "host: Judge Andrew Napolitano\n"
            "guest: Matt Hoh\n"
            "thread: hoh\n"
            "---\n\n"
            "Body.\n"
        ),
    )
    _write(day / "youtube-alex-mercouris-russia-returns-2026-05-26.md", "No frontmatter.\n")
    idx.write_day_index(day)

    summary = dash.load_day_summary(day)

    assert summary.channel_counter == {"Judging Freedom": 1}
    assert summary.host_counter == {"Andrew Napolitano": 1}
    assert summary.guest_counter == {"Matt Hoh": 1}
    assert summary.thread_counter == {"hoh": 1}
    assert summary.fallback_counter == {"youtube-alex-mercouris-*": 1}


def test_dashboard_falls_back_to_direct_folder_parse_when_readme_missing(tmp_path: Path) -> None:
    root = tmp_path / "source-archive" / "statecraft"
    day = root / "2025-01-01"
    _write(
        day / "youtube-alex-mercouris-russia-returns-2025-01-01.md",
        (
            "---\n"
            'title: "Russia Returns"\n'
            "show: alex-mercouris\n"
            "guest: John Helmer\n"
            "thread: ukraine\n"
            "---\n\n"
            "Body.\n"
        ),
    )

    summary = dash.load_day_summary(day)

    assert summary.has_readme is False
    assert summary.readme_parse_ok is False
    assert summary.source_count == 1
    assert summary.channel_counter["Alex Mercouris"] == 1


def test_dashboard_filters_days_by_year_and_date_range(tmp_path: Path) -> None:
    root = tmp_path / "source-archive" / "statecraft"
    for name in ("2025-01-01", "2025-06-01", "2026-05-26", "2026-05-27"):
        (root / name).mkdir(parents=True)

    by_year = dash._select_day_dirs(root, "2026", None, None)
    by_range = dash._select_day_dirs(root, None, "2026-05-26", "2026-05-26")

    assert [path.name for path in by_year] == ["2026-05-26", "2026-05-27"]
    assert [path.name for path in by_range] == ["2026-05-26"]


def test_dashboard_payload_rolls_up_days_and_marks_anomalies(tmp_path: Path) -> None:
    root = tmp_path / "source-archive" / "statecraft"
    day_one = root / "2026-05-26"
    day_two = root / "2026-05-27"
    _write(
        day_one / "transcript-napolitano-hoh-why-the-pentagon-lies-2026-05-26.md",
        (
            "---\n"
            'title: "Matt Hoh: Why the Pentagon Lies"\n'
            "show: Judging Freedom\n"
            "host: Judge Andrew Napolitano\n"
            "guest: Matt Hoh\n"
            "thread: hoh\n"
            "---\n\n"
            "Body.\n"
        ),
    )
    _write(
        day_one / "youtube-daniel-davis-deep-dive-us-must-stop-the-siege-of-iran-2026-05-26.md",
        (
            "---\n"
            'title: "US Must Stop the Siege of Iran"\n'
            "show: Daniel Davis Deep Dive\n"
            "host: Daniel Davis\n"
            "guest: Seyed M. Marandi\n"
            "thread: iran\n"
            "---\n\n"
            "Body.\n"
        ),
    )
    idx.write_day_index(day_one)
    _write(day_two / "youtube-alex-mercouris-russia-returns-2026-05-27.md", "No frontmatter.\n")

    payload = dash.build_dashboard_payload(
        root,
        [dash.load_day_summary(day_one), dash.load_day_summary(day_two)],
    )

    assert payload["coverage"]["dayCount"] == 2
    assert payload["coverage"]["sourceFileCount"] == 3
    assert payload["aggregates"]["topDays"][0] == {"date": "2026-05-26", "sourceCount": 2}
    channel_names = {item["name"] for item in payload["aggregates"]["channels"]}
    assert "Daniel Davis Deep Dive" in channel_names
    assert "Judging Freedom" in channel_names
    assert payload["anomalies"]["missingReadmes"] == ["2026-05-27"]
    assert payload["anomalies"]["fallbackHeavyDays"][0]["date"] == "2026-05-27"


def test_rendered_dashboard_contains_day_ledger_and_links(tmp_path: Path) -> None:
    root = tmp_path / "source-archive" / "statecraft"
    day = root / "2026-05-26"
    _write(
        day / "substack-pape-irans-new-battlefield-the-global-2026-05-26.md",
        (
            "---\n"
            'title: "Iran\'s New Battlefield"\n'
            "publication: Substack\n"
            "thread: pape\n"
            "---\n\n"
            "Body.\n"
        ),
    )
    idx.write_day_index(day)
    payload = dash.build_dashboard_payload(root, [dash.load_day_summary(day)])

    markdown = dash.render_dashboard_markdown(root, payload)

    assert "# Statecraft Day Dashboard" in markdown
    assert "## Day Ledger" in markdown
    assert "[2026-05-26](" in markdown
    assert "Quiet Days (1-2 files)" in markdown


def test_dashboard_json_shape_is_serializable(tmp_path: Path) -> None:
    root = tmp_path / "source-archive" / "statecraft"
    day = root / "2026-05-26"
    _write(day / "youtube-alex-mercouris-russia-returns-2026-05-26.md", "No frontmatter.\n")

    payload = dash.build_dashboard_payload(root, [dash.load_day_summary(day)])
    encoded = json.dumps(payload)

    assert '"schemaVersion": "1.0.0-statecraft-day-dashboard"' in encoded
    assert '"days"' in encoded
