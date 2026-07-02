from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import build_statecraft_day_indices as idx  # noqa: E402
import build_statecraft_speaker_dashboard as spk  # noqa: E402

def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")

def test_collect_speaker_stats_rolls_up_guest_host_channel_and_thread(tmp_path: Path) -> None:
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
    _write(
        day / "transcript-napolitano-marandi-iran-standoff-2026-05-26.md",
        (
            "---\n"
            'title: "Iran Standoff"\n'
            "show: Judging Freedom\n"
            "host: Judge Andrew Napolitano\n"
            "guest: Seyed M. Marandi\n"
            "thread: marandi\n"
            "---\n\n"
            "Body.\n"
        ),
    )

    stats, total_files = spk.collect_speaker_stats([day])

    marandi = stats["Seyed M. Marandi"]
    assert total_files == 2
    assert marandi.file_count == 2
    assert marandi.day_set == {"2026-05-26"}
    assert marandi.host_counter["Daniel Davis"] == 1
    assert marandi.host_counter["Andrew Napolitano"] == 1
    assert marandi.channel_counter["Daniel Davis Deep Dive"] == 1
    assert marandi.channel_counter["Judging Freedom"] == 1
    assert marandi.thread_counter["iran"] == 1
    assert marandi.thread_counter["marandi"] == 1

def test_build_speaker_dashboard_payload_ranks_top_guests(tmp_path: Path) -> None:
    root = tmp_path / "source-archive" / "statecraft"
    day_one = root / "2026-05-26"
    day_two = root / "2026-05-27"
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
    _write(
        day_two / "transcript-napolitano-marandi-iran-standoff-2026-05-27.md",
        (
            "---\n"
            'title: "Iran Standoff"\n'
            "show: Judging Freedom\n"
            "host: Judge Andrew Napolitano\n"
            "guest: Seyed M. Marandi\n"
            "thread: marandi\n"
            "---\n\n"
            "Body.\n"
        ),
    )
    _write(
        day_two / "youtube-daniel-davis-deep-dive-freeman-asia-2026-05-27.md",
        (
            "---\n"
            'title: "Asia"\n'
            "show: Daniel Davis Deep Dive\n"
            "host: Daniel Davis\n"
            "guest: Chas Freeman\n"
            "thread: freeman\n"
            "---\n\n"
            "Body.\n"
        ),
    )

    stats, _ = spk.collect_speaker_stats([day_one, day_two])
    payload = spk.build_speaker_dashboard_payload(root, [day_one, day_two], stats, top_speakers=10)

    assert payload["coverage"]["dayCount"] == 2
    assert payload["coverage"]["sourceFileCount"] == 3
    assert payload["coverage"]["distinctGuestCount"] == 2
    assert payload["aggregates"]["topSpeakers"][0]["name"] == "Seyed M. Marandi"
    assert payload["aggregates"]["topSpeakers"][0]["fileCount"] == 2
    assert payload["aggregates"]["topSpeakers"][0]["dayCount"] == 2

def test_build_saved_speaker_slices_writes_guest_filtered_day_dashboard(tmp_path: Path) -> None:
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

    original_out_dir = spk.OUT_DIR
    original_slices_dir = spk.SLICES_DIR
    try:
        spk.OUT_DIR = tmp_path / "runtime/artifacts" / "statecraft" / "speakers"
        spk.SLICES_DIR = spk.OUT_DIR / "slices"
        built = spk.build_saved_speaker_slices(root, [day], ["Seyed M. Marandi"])
        out_md = spk.SLICES_DIR / "seyed-m-marandi.md"
        out_json = spk.SLICES_DIR / "seyed-m-marandi.json"

        assert built == ["seyed-m-marandi"]
        assert out_md.is_file()
        assert out_json.is_file()
        data = json.loads(out_json.read_text(encoding="utf-8"))
        assert data["query"]["guests"] == ["Seyed M. Marandi"]
        assert data["query"]["slug"] == "seyed-m-marandi"
    finally:
        spk.OUT_DIR = original_out_dir
        spk.SLICES_DIR = original_slices_dir

def test_render_speaker_dashboard_markdown_mentions_saved_slices(tmp_path: Path) -> None:
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

    stats, _ = spk.collect_speaker_stats([day])
    payload = spk.build_speaker_dashboard_payload(root, [day], stats, top_speakers=5)
    markdown = spk.render_speaker_dashboard_markdown(payload, ["seyed-m-marandi"])

    assert "# Statecraft Speaker Dashboard" in markdown
    assert "## Top Guests" in markdown
    assert "`Seyed M. Marandi`" in markdown
    assert "## Saved Speaker Slices" in markdown
    assert "`seyed-m-marandi`" in markdown

def test_select_day_dirs_respects_year_and_range(tmp_path: Path) -> None:
    root = tmp_path / "source-archive" / "statecraft"
    for name in ("2025-01-01", "2025-05-01", "2026-05-26", "2026-05-27"):
        (root / name).mkdir(parents=True)

    by_year = spk._select_day_dirs(root, "2026", None, None)
    by_range = spk._select_day_dirs(root, None, "2025-05-01", "2026-05-26")

    assert [path.name for path in by_year] == ["2026-05-26", "2026-05-27"]
    assert [path.name for path in by_range] == ["2025-05-01", "2026-05-26"]
