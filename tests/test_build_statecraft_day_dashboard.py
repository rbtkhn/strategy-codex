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

def test_dashboard_filters_days_by_channel_thread_host_and_guest(tmp_path: Path) -> None:
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
        day_two / "youtube-daniel-davis-deep-dive-us-must-stop-the-siege-of-iran-2026-05-27.md",
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
    idx.write_day_index(day_two)
    days = [dash.load_day_summary(day_one), dash.load_day_summary(day_two)]

    by_channel = dash.filter_day_summaries(days, channels=("judging freedom",))
    by_thread = dash.filter_day_summaries(days, threads=("iran",))
    by_host_guest = dash.filter_day_summaries(days, hosts=("daniel davis",), guests=("seyed m. marandi",))
    by_intersection = dash.filter_day_summaries(days, channels=("Daniel Davis Deep Dive",), threads=("hoh",))

    assert [day.date for day in by_channel] == ["2026-05-26"]
    assert [day.date for day in by_thread] == ["2026-05-27"]
    assert [day.date for day in by_host_guest] == ["2026-05-27"]
    assert by_intersection == []

def test_resolve_output_paths_uses_default_and_slugged_paths() -> None:
    default_md, default_json = dash.resolve_output_paths(None)
    slug_md, slug_json = dash.resolve_output_paths("Dialogue Works")

    assert default_md == dash.OUT_MD
    assert default_json == dash.OUT_JSON
    assert slug_md == dash.SLICES_DIR / "dialogue-works.md"
    assert slug_json == dash.SLICES_DIR / "dialogue-works.json"

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

def test_dashboard_payload_records_slug_in_query(tmp_path: Path) -> None:
    root = tmp_path / "source-archive" / "statecraft"
    day = root / "2026-05-26"
    _write(day / "youtube-alex-mercouris-russia-returns-2026-05-26.md", "No frontmatter.\n")

    payload = dash.build_dashboard_payload(root, [dash.load_day_summary(day)], threads=("mercouris",), slug="mercouris-thread")

    assert payload["query"]["slug"] == "mercouris-thread"

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
    payload = dash.build_dashboard_payload(
        root,
        [dash.load_day_summary(day)],
        channels=("Substack",),
        threads=("pape",),
    )

    markdown = dash.render_dashboard_markdown(root, payload)

    assert "# Statecraft Day Dashboard" in markdown
    assert "## Active Query" in markdown
    assert "- Slug: (default dashboard)" in markdown
    assert "- Channels: `Substack`" in markdown
    assert "- Threads: `pape`" in markdown
    assert "## Day Ledger" in markdown
    assert "[2026-05-26](" in markdown
    assert "Quiet Days (1-2 files)" in markdown

def test_dashboard_json_shape_is_serializable(tmp_path: Path) -> None:
    root = tmp_path / "source-archive" / "statecraft"
    day = root / "2026-05-26"
    _write(day / "youtube-alex-mercouris-russia-returns-2026-05-26.md", "No frontmatter.\n")

    payload = dash.build_dashboard_payload(root, [dash.load_day_summary(day)], channels=("Alex Mercouris",))
    encoded = json.dumps(payload)

    assert '"schemaVersion": "1.0.0-statecraft-day-dashboard"' in encoded
    assert '"days"' in encoded
    assert '"channels": ["Alex Mercouris"]' in encoded

def test_slugged_write_does_not_touch_default_dashboard(tmp_path: Path) -> None:
    root = tmp_path / "source-archive" / "statecraft"
    day = root / "2026-05-26"
    _write(
        day / "youtube-daniel-davis-deep-dive-us-must-stop-the-siege-of-iran-2026-05-26.md",
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
    idx.write_day_index(day)

    original_out_dir = dash.OUT_DIR
    original_slices_dir = dash.SLICES_DIR
    original_out_md = dash.OUT_MD
    original_out_json = dash.OUT_JSON
    try:
        dash.OUT_DIR = tmp_path / "runtime/artifacts" / "statecraft"
        dash.SLICES_DIR = dash.OUT_DIR / "slices"
        dash.OUT_MD = dash.OUT_DIR / "day-dashboard.md"
        dash.OUT_JSON = dash.OUT_DIR / "day-dashboard.json"

        default_payload = dash.build_dashboard_payload(root, [dash.load_day_summary(day)])
        dash.OUT_DIR.mkdir(parents=True, exist_ok=True)
        dash.OUT_JSON.write_text(json.dumps(default_payload, indent=2) + "\n", encoding="utf-8", newline="\n")
        dash.OUT_MD.write_text(dash.render_dashboard_markdown(root, default_payload), encoding="utf-8", newline="\n")
        default_before = dash.OUT_MD.read_text(encoding="utf-8")

        slice_payload = dash.build_dashboard_payload(root, [dash.load_day_summary(day)], channels=("Daniel Davis Deep Dive",), slug="davis")
        slice_md, slice_json = dash.resolve_output_paths("davis")
        slice_md.parent.mkdir(parents=True, exist_ok=True)
        slice_json.write_text(json.dumps({**slice_payload, "runtime/artifacts": {"markdown": str(slice_md), "json": str(slice_json)}}, indent=2) + "\n", encoding="utf-8", newline="\n")
        slice_md.write_text(dash.render_dashboard_markdown(root, {**slice_payload, "runtime/artifacts": {"markdown": str(slice_md), "json": str(slice_json)}}), encoding="utf-8", newline="\n")

        assert dash.OUT_MD.read_text(encoding="utf-8") == default_before
        assert slice_md.is_file()
        assert slice_json.is_file()
        assert "- Slug: `davis`" in slice_md.read_text(encoding="utf-8")
    finally:
        dash.OUT_DIR = original_out_dir
        dash.SLICES_DIR = original_slices_dir
        dash.OUT_MD = original_out_md
        dash.OUT_JSON = original_out_json
