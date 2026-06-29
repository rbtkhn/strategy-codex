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


def test_voice_index_audit_passes_when_shelf_listed(tmp_path: Path, monkeypatch) -> None:
    voices = tmp_path / "statecraft" / "voices"
    shelf = voices / "sample"
    shelf.mkdir(parents=True)
    _write(
        shelf / "sample-index.md",
        "# Sample index\n",
    )
    _write(
        voices / "voice-index.md",
        "# Voices Index\n\n## Analyst and source-corpus lenses\n\n"
        "| Lens | Index file |\n|---|---|\n"
        "| Sample | [sample/sample-index.md](sample/sample-index.md) |\n\n"
        "## Source index vs source-lattice\n\nsource-lattice doctrine here.\n",
    )
    monkeypatch.setattr(audit, "VOICES_DIR", voices)

    findings = audit.audit_voice_index(voices)
    assert any(f.code == "registry_parity" and f.level == "pass" for f in findings)
    assert audit.main(["--voice-index", "--table-only"]) == 0


def test_voice_index_fails_on_registry_gap(tmp_path: Path, monkeypatch) -> None:
    voices = tmp_path / "statecraft" / "voices"
    shelf = voices / "hidden"
    shelf.mkdir(parents=True)
    _write(shelf / "hidden-index.md", "# Hidden\n")
    _write(
        voices / "voice-index.md",
        "# Voices Index\n\n## Source index vs source-lattice\n\nsource-lattice note.\n",
    )
    monkeypatch.setattr(audit, "VOICES_DIR", voices)

    findings = audit.audit_voice_index(voices)
    assert any(f.code == "registry_gap" and f.level == "fail" for f in findings)
    assert audit.main(["--voice-index"]) == 1


def test_shelf_index_passes_when_capture_links_resolve(
    tmp_path: Path, monkeypatch
) -> None:
    archive = tmp_path / "archive"
    day = archive / "2026-06-01"
    capture = day / "source-parsi-sample-2026-06-01.md"
    _write(
        capture,
        "---\nthread: parsi\npub_date: 2026-06-01\ntitle: Sample\n---\n\nBody.\n",
    )
    voices = tmp_path / "statecraft" / "voices"
    shelf = voices / "parsi"
    shelf.mkdir(parents=True)
    rel = "../../../source-archive/statecraft/2026-06-01/source-parsi-sample-2026-06-01.md"
    _write(
        shelf / "parsi-index.md",
        f"# Parsi index\n\n- [Sample]({rel})\n",
    )
    _write(
        voices / "voice-index.md",
        "# Voices\n\n| Lens | Index |\n|---|---|\n| Parsi | [parsi/parsi-index.md](parsi/parsi-index.md) |\n",
    )
    monkeypatch.setattr(audit, "VOICES_DIR", voices)
    monkeypatch.setattr(audit, "REPO_ROOT", tmp_path)
    # Mirror archive under repo layout expected by relative link from shelf
    archive_mirror = tmp_path / "source-archive" / "statecraft" / "2026-06-01"
    archive_mirror.mkdir(parents=True)
    archive_mirror.joinpath("source-parsi-sample-2026-06-01.md").write_text(
        capture.read_text(encoding="utf-8"), encoding="utf-8", newline="\n"
    )

    findings = audit.audit_shelf_index("parsi", archive_root=archive)
    assert any(f.code == "links_ok" and f.level == "pass" for f in findings)
    assert any(f.code == "capture_links" and f.level == "pass" for f in findings)


def test_shelf_index_fails_when_index_links_missing_capture(
    tmp_path: Path, monkeypatch
) -> None:
    archive = tmp_path / "archive"
    voices = tmp_path / "statecraft" / "voices"
    shelf = voices / "parsi"
    shelf.mkdir(parents=True)
    rel = "../../../source-archive/statecraft/2026-06-01/source-parsi-missing-2026-06-01.md"
    _write(shelf / "parsi-index.md", f"# Parsi\n\n- [Missing]({rel})\n")
    _write(
        voices / "voice-index.md",
        "# Voices\n\n| Lens | Index |\n|---|---|\n| Parsi | [parsi/parsi-index.md](parsi/parsi-index.md) |\n",
    )
    monkeypatch.setattr(audit, "VOICES_DIR", voices)

    findings = audit.audit_shelf_index("parsi", archive_root=archive)
    assert any(f.code == "capture_missing" and f.level == "fail" for f in findings)
    assert audit.main(["--shelf-index", "parsi", "--root", str(archive)]) == 1


def test_shelf_index_excludes_pape_date_stub(tmp_path: Path, monkeypatch) -> None:
    archive = tmp_path / "archive"
    day = archive / "2026-04-17"
    stub = day / "source-pape-2026-04-17.md"
    _write(stub, "---\nthread: pape\npub_date: 2026-04-17\nkind: transcript\n---\n\nX thread.\n")
    voices = tmp_path / "statecraft" / "voices"
    shelf = voices / "pape"
    shelf.mkdir(parents=True)
    _write(shelf / "pape-index.md", "# Pape\n\n## Boundary\n\nDate stubs excluded.\n")
    _write(
        voices / "voice-index.md",
        "# Voices\n\n| Lens | Index |\n|---|---|\n| Pape | [pape/pape-index.md](pape/pape-index.md) |\n",
    )
    monkeypatch.setattr(audit, "VOICES_DIR", voices)

    findings = audit.audit_shelf_index("pape", archive_root=archive)
    assert not any(f.code == "archive_unlisted" for f in findings)
    assert any(f.code == "archive_parity" and f.level == "pass" for f in findings)


def test_karaganov_shelf_excludes_ritter_reaction_capture(tmp_path: Path, monkeypatch) -> None:
    import shelf_index_utils as shelf_utils  # noqa: E402

    archive = tmp_path / "archive"
    day = archive / "2026-01-03"
    reaction = day / "source-ritter-russia-dark-sage-karaganov-2026-01-03.md"
    _write(
        reaction,
        "---\nthread: ritter\npub_date: 2026-01-03\nspeaker: Scott Ritter\n---\n\nAbout Karaganov.\n",
    )
    guest = archive / "2025-05-14" / "source-glenn-diesen-sergey-karaganov-solo-2025-05-14.md"
    _write(
        guest,
        "---\nthread: diesen\npub_date: 2025-05-14\nguest: Sergey Karaganov\n---\n\nGuest.\n",
    )
    voices = tmp_path / "statecraft" / "voices"
    shelf = voices / "karaganov"
    shelf.mkdir(parents=True)
    rel_guest = "../../../source-archive/statecraft/2025-05-14/source-glenn-diesen-sergey-karaganov-solo-2025-05-14.md"
    rel_reaction = (
        "../../../source-archive/statecraft/2026-01-03/"
        "source-ritter-russia-dark-sage-karaganov-2026-01-03.md"
    )
    _write(
        shelf / "karaganov-index.md",
        f"# Karaganov\n\n| File |\n|---|\n| [guest]({rel_guest}) |\n| [reaction]({rel_reaction}) |\n",
    )
    _write(
        voices / "voice-index.md",
        "# Voices\n\n| Lens | Index |\n|---|---|\n"
        "| Karaganov | [karaganov/karaganov-index.md](karaganov/karaganov-index.md) |\n",
    )
    mirror_root = tmp_path / "source-archive" / "statecraft"
    for src in (guest, reaction):
        dest = mirror_root / src.parent.name / src.name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(src.read_text(encoding="utf-8"), encoding="utf-8", newline="\n")
    monkeypatch.setattr(audit, "VOICES_DIR", voices)
    monkeypatch.setattr(audit, "REPO_ROOT", tmp_path)

    assert shelf_utils.shelf_capture_excluded("karaganov", reaction, {}, "")
    assert not shelf_utils.shelf_capture_excluded("karaganov", guest, {}, "")

    findings = audit.audit_shelf_index("karaganov", archive_root=archive)
    parity = [f for f in findings if f.code == "archive_parity"]
    assert parity and parity[0].level == "pass"
    assert "1 eligible" in parity[0].message


def test_shelf_index_from_capture_resolves_and_appends(tmp_path: Path, monkeypatch) -> None:
    import shelf_index_from_capture as shelf_cli  # noqa: E402
    import shelf_index_utils as shelf_utils  # noqa: E402

    archive = tmp_path / "archive"
    day = archive / "2026-06-10"
    capture = day / "source-crooke-sample-2026-06-10.md"
    _write(
        capture,
        "---\nthread: crooke\npub_date: 2026-06-10\nkind: substack-post\ntitle: Sample Crooke\n---\n\nBody.\n",
    )
    voices = tmp_path / "statecraft" / "voices"
    crooke = voices / "crooke"
    crooke.mkdir(parents=True)
    _write(crooke / "crooke-index.md", "# Crooke index\n\n## 2026-06\n")
    _write(
        voices / "voice-index.md",
        "# Voices\n\n| Lens | Index |\n|---|---|\n| Crooke | [crooke/crooke-index.md](crooke/crooke-index.md) |\n",
    )
    monkeypatch.setattr(shelf_utils, "VOICES_DIR", voices)
    monkeypatch.setattr(shelf_cli, "REPO_ROOT", tmp_path)

    code = shelf_cli.main(["--path", str(capture), "--root", str(archive), "--apply"])
    assert code == 0
    index_text = (crooke / "crooke-index.md").read_text(encoding="utf-8")
    assert capture.name in index_text


def test_shelf_slug_filename_token_not_substring(tmp_path: Path, monkeypatch) -> None:
    import shelf_index_utils as shelf_utils  # noqa: E402

    archive = tmp_path / "archive"
    day = archive / "2026-05-14"
    mate_capture = day / "source-judging-freedom-mate-sample-2026-05-14.md"
    checkmate = day / "source-judging-freedom-wilkerson-checkmate-in-iran-2026-05-14.md"
    decimated = (
        archive
        / "2026-04-28"
        / "source-dialogue-works-col-larry-wilkerson-trumps-own-advisors-now-split-on-iran-israels-plan-decimated-2026-04-28.md"
    )
    for path, body in (
        (mate_capture, "---\nthread: mate\npub_date: 2026-05-14\n---\n\n"),
        (checkmate, "---\nthread: wilkerson\npub_date: 2026-05-14\n---\n\n"),
        (decimated, "---\nthread: wilkerson\npub_date: 2026-04-28\n---\n\n"),
    ):
        _write(path, body)

    voices = tmp_path / "statecraft" / "voices"
    mate_shelf = voices / "mate"
    mate_shelf.mkdir(parents=True)
    rel = f"../../../source-archive/statecraft/2026-05-14/{mate_capture.name}"
    _write(
        mate_shelf / "mate-index.md",
        f"# Mate\n\n- [Sample]({rel})\n",
    )
    _write(
        voices / "voice-index.md",
        "# Voices\n\n| Lens | Index |\n|---|---|\n| Maté | [mate/mate-index.md](mate/mate-index.md) |\n",
    )
    monkeypatch.setattr(audit, "VOICES_DIR", voices)
    monkeypatch.setattr(audit, "REPO_ROOT", tmp_path)
    for path in (mate_capture, checkmate, decimated):
        mirror = tmp_path / "source-archive" / "statecraft" / path.parent.name / path.name
        mirror.parent.mkdir(parents=True, exist_ok=True)
        mirror.write_text(path.read_text(encoding="utf-8"), encoding="utf-8", newline="\n")

    paths = audit.iter_archive_captures_for_shelf("mate", archive)
    names = {p.name for p in paths}
    assert mate_capture.name in names
    assert checkmate.name not in names
    assert decimated.name not in names
    assert not shelf_utils.slug_token_in_capture_filename("mate", checkmate.name)
    assert not shelf_utils.slug_token_in_capture_filename("mate", decimated.name)
    assert shelf_utils.slug_token_in_capture_filename("mate", mate_capture.name)

    findings = audit.audit_shelf_index("mate", archive_root=archive)
    assert any(f.code == "archive_parity" and f.level == "pass" for f in findings)
    assert not any(f.code == "archive_unlisted" for f in findings)


def test_martyanov_slug_matches_typo_token_and_guest_meta(tmp_path: Path, monkeypatch) -> None:
    import shelf_index_utils as shelf_utils  # noqa: E402

    archive = tmp_path / "archive"
    typo_capture = (
        archive
        / "2025-10-20"
        / "source-daniel-davis-russia-all-about-demilitarizing-nato-andrei-martynaov-lt-col-daniel-davis-2025-10-20.md"
    )
    guest_meta_capture = (
        archive
        / "2025-12-08"
        / "source-daniel-davis-a-just-and-lasting-defeat-europe-meets-zelensky-lt-col-daniel-davis-and-2025-12-08.md"
    )
    _write(
        typo_capture,
        "---\npub_date: 2025-10-20\nguest: Andrei Martyanov\nthread: davis\n---\n\n",
    )
    _write(
        guest_meta_capture,
        "---\npub_date: 2025-12-08\nguest: Andrei Martyanov\nthread: davis\n---\n\n",
    )

    assert shelf_utils.slug_token_in_capture_filename("martyanov", typo_capture.name)
    assert not shelf_utils.slug_token_in_capture_filename("martyanov", "source-checkmate-only.md")
    assert shelf_utils.capture_matches_shelf(
        "martyanov", guest_meta_capture, {"guest": "Andrei Martyanov", "title": "Davis and Martyanov"}, ""
    )

    voices = tmp_path / "statecraft" / "voices"
    shelf = voices / "martyanov"
    shelf.mkdir(parents=True)
    _write(shelf / "martyanov-index.md", "# Martyanov\n")
    _write(
        voices / "voice-index.md",
        "# Voices\n\n| Lens | Index |\n|---|---|\n| Martyanov | [martyanov/martyanov-index.md](martyanov/martyanov-index.md) |\n",
    )
    monkeypatch.setattr(audit, "VOICES_DIR", voices)
    monkeypatch.setattr(audit, "REPO_ROOT", tmp_path)

    names = {p.name for p in audit.iter_archive_captures_for_shelf("martyanov", archive)}
    assert typo_capture.name in names
    assert guest_meta_capture.name in names


def test_jiang_shelf_excludes_game_theory(tmp_path: Path) -> None:
    import shelf_index_utils as shelf_utils  # noqa: E402

    path = tmp_path / "2026-04-27" / "source-game-theory-21-world-war-trump-2026-04-27.md"
    meta = {
        "thread": "jiang",
        "source_form": "solo",
        "host": "Jiang Xueqin",
        "kind": "transcript",
    }
    assert not shelf_utils.is_jiang_external_interview(meta, path, "")
    assert not shelf_utils.capture_matches_shelf("jiang", path, meta, "")


def test_jiang_shelf_excludes_dialogue_works_about_jiang(tmp_path: Path) -> None:
    import shelf_index_utils as shelf_utils  # noqa: E402

    path = (
        tmp_path
        / "2026-05-16"
        / "source-dialogue-works-jiang-xueqin-most-embarrassing-prediction-exposed-larry-johnson-nima-alkhorshid-2026-05-16.md"
    )
    meta = {
        "guest": "Larry Johnson",
        "source_form": "interview",
        "kind": "transcript",
        "title": "Jiang Xueqin's Most Embarrassing Prediction Exposed",
    }
    assert not shelf_utils.is_jiang_external_interview(meta, path, "")
    assert not shelf_utils.capture_matches_shelf("jiang", path, meta, "")


def test_jiang_shelf_includes_diesen_guest(tmp_path: Path) -> None:
    import shelf_index_utils as shelf_utils  # noqa: E402

    path = tmp_path / "2026-01-05" / "source-diesen-jiang-predictions-2026-empire-rivalry-collapse-2026-01-05.md"
    meta = {
        "guest": "Jiang Xueqin",
        "source_form": "interview",
        "kind": "transcript",
        "host": "Glenn Diesen",
        "source_url": "https://www.youtube.com/watch?v=ORyCS0r2Tpg",
    }
    assert shelf_utils.is_jiang_external_interview(meta, path, "")
    assert shelf_utils.capture_matches_shelf("jiang", path, meta, "")


def test_jiang_shelf_includes_sneako_dual_index(tmp_path: Path) -> None:
    import shelf_index_utils as shelf_utils  # noqa: E402

    path = tmp_path / "2026-04-14" / "source-interviews-15-sneako-jiang-dugin-eschatology-2026-04-14.md"
    meta = {
        "host": "Sneako",
        "source_form": "interview",
        "kind": "transcript",
        "title": "Interviews #15: Sneako — Jiang Xueqin & Aleksandr Dugin",
        "source_url": "https://www.youtube.com/watch?v=n44OF1Y7zgo",
    }
    assert shelf_utils.is_jiang_external_interview(meta, path, "")
    assert shelf_utils.capture_matches_shelf("jiang", path, meta, "")


def test_jiang_index_rows_have_youtube_url(tmp_path: Path, monkeypatch) -> None:
    import build_jiang_index as jiang_idx  # noqa: E402
    import shelf_index_utils as shelf_utils  # noqa: E402

    archive = tmp_path / "source-archive" / "statecraft"
    capture = archive / "2026-01-05" / "source-diesen-jiang-predictions-2026-empire-rivalry-collapse-2026-01-05.md"
    _write(
        capture,
        "---\n"
        "pub_date: 2026-01-05\n"
        "guest: Jiang Xueqin\n"
        "host: Glenn Diesen\n"
        "source_form: interview\n"
        "kind: transcript\n"
        'title: "Predictions for 2026"\n'
        'source_url: "https://www.youtube.com/watch?v=ORyCS0r2Tpg"\n'
        "---\n\nBody.\n",
    )
    voices = tmp_path / "statecraft" / "voices" / "jiang"
    voices.mkdir(parents=True)
    out = voices / "jiang-index.md"
    monkeypatch.setattr(jiang_idx, "ARCHIVE", archive)
    monkeypatch.setattr(jiang_idx, "OUT", out)
    monkeypatch.setattr(sys, "argv", ["build_jiang_index.py"])
    assert jiang_idx.main() == 0
    text = out.read_text(encoding="utf-8")
    assert "youtube.com/watch?v=ORyCS0r2Tpg" in text
    assert shelf_utils.capture_matches_shelf(
        "jiang", capture, {"guest": "Jiang Xueqin", "source_form": "interview", "kind": "transcript"}, ""
    )
