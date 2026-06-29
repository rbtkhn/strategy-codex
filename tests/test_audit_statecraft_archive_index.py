from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import audit_statecraft_archive_index as audit  # noqa: E402
import build_statecraft_archive_navigation as nav  # noqa: E402
import build_statecraft_day_indices as day_idx  # noqa: E402
import statecraft_writer_index as writer_idx  # noqa: E402


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def _sample_capture(host_people: bool = True, threads: bool = True) -> str:
    host_block = "host_people:\n  - Nima Alkhorshid\n" if host_people else ""
    threads_block = "threads:\n  - alkorshid\n  - johnson\n" if threads else ""
    return (
        "---\n"
        "pub_date: 2026-06-28\n"
        "kind: cleaned-transcript\n"
        "source_form: interview\n"
        "source_type: youtube\n"
        f"{host_block}"
        "guest_people:\n  - Larry Johnson\n"
        f"{threads_block}"
        "thread: johnson\n"
        "host: Nima Alkhorshid\n"
        'title: "Breaking sample"\n'
        "youtube_id: abc123\n"
        'source_url: "https://www.youtube.com/watch?v=abc123"\n'
        "transcript_curation: curated_sectioned\n"
        "---\n\n"
        "# Breaking sample\n\n"
        "## Transcript\n\n"
        "### Show Open — Sample\n\n"
        "One two three four five.\n\n"
        "### Close — Sample\n\n"
        "Six seven eight nine ten.\n"
    )


def test_audit_day_passes_when_index_fresh(tmp_path: Path) -> None:
    day = tmp_path / "2026-06-28"
    _write(day / "source-dialogue-works-sample-2026-06-28.md", _sample_capture())
    day_idx.write_day_index(day)

    findings = audit.audit_day_dir(day)
    assert any(f.code == "parity" and f.level == "pass" for f in findings)
    assert any(f.code == "index_fresh" and f.level == "pass" for f in findings)

    code = audit.main(["--day", "2026-06-28", "--root", str(tmp_path)])
    assert code == 0


def test_audit_day_fails_parity_when_index_omits_file(tmp_path: Path) -> None:
    day = tmp_path / "2026-06-28"
    _write(day / "source-dialogue-works-sample-2026-06-28.md", _sample_capture())
    day_idx.write_day_index(day)
    _write(
        day / "source-dialogue-works-second-2026-06-28.md",
        _sample_capture().replace("Breaking sample", "Second sample"),
    )

    findings = audit.audit_day_dir(day)
    assert any(f.code == "parity" and f.level == "fail" for f in findings)


def test_audit_day_fails_when_index_stale(tmp_path: Path) -> None:
    day = tmp_path / "2026-06-28"
    _write(day / "source-dialogue-works-sample-2026-06-28.md", _sample_capture())
    day_idx.write_day_index(day)
    index_path = day / "day-index.md"
    index_path.write_text(index_path.read_text(encoding="utf-8") + "\n<!-- stale -->\n", encoding="utf-8")

    findings = audit.audit_day_dir(day)
    assert any(f.code == "stale_index" and f.level == "fail" for f in findings)

    code = audit.main(["--day", "2026-06-28", "--root", str(tmp_path)])
    assert code == 1


def test_hygiene_warns_empty_host_people(tmp_path: Path) -> None:
    day = tmp_path / "2026-06-28"
    path = day / "source-dialogue-works-sample-2026-06-28.md"
    _write(path, _sample_capture(host_people=False))
    meta = audit.parse_frontmatter(path)
    warnings = audit.capture_hygiene_warnings(path, meta)
    assert any("host_people empty" in w for w in warnings)


def test_table_only_emits_inventory_columns(tmp_path: Path, capsys) -> None:
    day = tmp_path / "2026-06-28"
    _write(day / "source-dialogue-works-sample-2026-06-28.md", _sample_capture())

    code = audit.main(
        ["--day", "2026-06-28", "--root", str(tmp_path), "--table-only"]
    )
    out = capsys.readouterr().out

    assert code == 0
    assert "| Date | Title | URL | Words | Bucket | Kind | § |" in out
    assert "https://www.youtube.com/watch?v=abc123" in out
    assert "Breaking sample" in out


def test_table_sort_words_and_json_rows(tmp_path: Path, capsys) -> None:
    day = tmp_path / "2026-06-28"
    short = _sample_capture().replace("Breaking sample", "Short")
    long = _sample_capture().replace("Breaking sample", "Long") + "\n" + ("word " * 200)
    _write(day / "source-a-2026-06-28.md", short)
    _write(day / "source-b-2026-06-28.md", long)

    code = audit.main(
        [
            "--day",
            "2026-06-28",
            "--root",
            str(tmp_path),
            "--table-only",
            "--table-sort",
            "words",
            "--json",
        ]
    )
    payload = json.loads(capsys.readouterr().out)
    assert code == 0
    assert len(payload["table"]) == 2
    assert payload["table"][0]["words"] >= payload["table"][1]["words"]


def test_table_limit_truncates_month_scope(tmp_path: Path) -> None:
    root = tmp_path
    for i in range(3):
        day = root / f"2026-06-{i + 1:02d}"
        _write(day / f"source-sample-{i}-2026-06-{i + 1:02d}.md", _sample_capture())

    rows = audit.collect_inventory_rows(
        [root / "2026-06-01", root / "2026-06-02", root / "2026-06-03"]
    )
    sorted_rows = audit.sort_inventory_rows(rows, "date")
    shown, truncated = audit.apply_table_limit(sorted_rows, 2)
    assert len(shown) == 2
    assert truncated == 1


def test_channel_index_table_and_audit_fresh(tmp_path: Path, monkeypatch) -> None:
    archive_root = tmp_path / "archive"
    channel_dir = tmp_path / "channels"
    channel_dir.mkdir()
    day = archive_root / "2026-06-28"
    capture = _sample_capture().replace("Nima Alkhorshid", "Dialogue Works")
    capture = capture.replace("kind: cleaned-transcript", "kind: cleaned-transcript\nchannel_slug: dialogue-works")
    _write(day / "source-dialogue-works-sample-2026-06-28.md", capture)

    monkeypatch.setattr(audit, "CHANNEL_INDEX_DIR", channel_dir)
    nav.write_rendered(channel_dir / "channel-index.md", nav.build_channel_index(archive_root), check=False)
    nav.write_channel_index_json(channel_dir / "channel-index.json", archive_root, check=False)
    nav.write_rendered(
        channel_dir / "channel-index-misc.md",
        nav.build_channel_index_misc(archive_root),
        check=False,
    )

    findings = audit.audit_channel_index(archive_root)
    assert any(f.code == "channel_md" and f.level == "pass" for f in findings)
    assert any(f.code == "channel_json" and f.level == "pass" for f in findings)

    code = audit.main(
        ["--channel-index", "--root", str(archive_root), "--table-only", "--table-sort", "words"]
    )
    assert code == 0


def _sample_writer_capture() -> str:
    return (
        "---\n"
        "pub_date: 2026-06-27\n"
        "kind: substack-post\n"
        "source_type: substack\n"
        "source_form: newsletter\n"
        "thread: pape\n"
        'title: "Situation Report"\n'
        'source_url: "https://escalationtrap.substack.com/p/situation-report"\n'
        "---\n\n"
        "# Situation Report\n\n"
        "Prose body for writer index test.\n"
    )


def test_writer_index_table_and_audit_fresh(tmp_path: Path) -> None:
    archive_root = tmp_path / "archive"
    day = archive_root / "2026-06-27"
    _write(day / "source-pape-situation-report-2026-06-27.md", _sample_writer_capture())

    nav.write_rendered(
        archive_root / "writer-index.md",
        writer_idx.build_writer_index(archive_root),
        check=False,
    )
    nav.write_writer_index_json(archive_root / "writer-index.json", archive_root, check=False)

    findings = audit.audit_writer_index(archive_root)
    assert any(f.code == "writer_md" and f.level == "pass" for f in findings)
    assert any(f.code == "writer_json" and f.level == "pass" for f in findings)

    code = audit.main(
        ["--writer-index", "--root", str(archive_root), "--table-only", "--table-sort", "words"]
    )
    assert code == 0


def test_writer_index_fails_when_md_stale(tmp_path: Path) -> None:
    archive_root = tmp_path / "archive"
    day = archive_root / "2026-06-27"
    _write(day / "source-pape-situation-report-2026-06-27.md", _sample_writer_capture())

    nav.write_rendered(
        archive_root / "writer-index.md",
        writer_idx.build_writer_index(archive_root),
        check=False,
    )
    (archive_root / "writer-index.md").write_text("stale\n", encoding="utf-8")
    nav.write_writer_index_json(archive_root / "writer-index.json", archive_root, check=False)

    findings = audit.audit_writer_index(archive_root)
    assert any(f.code == "stale_writer_md" and f.level == "fail" for f in findings)
    assert audit.main(["--writer-index", "--root", str(archive_root)]) == 1


def test_channel_index_fails_when_md_stale(tmp_path: Path, monkeypatch) -> None:
    archive_root = tmp_path / "archive"
    channel_dir = tmp_path / "channels"
    channel_dir.mkdir()
    day = archive_root / "2026-06-28"
    _write(day / "source-dialogue-works-sample-2026-06-28.md", _sample_capture())

    monkeypatch.setattr(audit, "CHANNEL_INDEX_DIR", channel_dir)
    nav.write_rendered(channel_dir / "channel-index.md", nav.build_channel_index(archive_root), check=False)
    (channel_dir / "channel-index.md").write_text("stale\n", encoding="utf-8")
    nav.write_channel_index_json(channel_dir / "channel-index.json", archive_root, check=False)
    nav.write_rendered(
        channel_dir / "channel-index-misc.md",
        nav.build_channel_index_misc(archive_root),
        check=False,
    )

    findings = audit.audit_channel_index(archive_root)
    assert any(f.code == "stale_channel_md" and f.level == "fail" for f in findings)
    assert audit.main(["--channel-index", "--root", str(archive_root)]) == 1
