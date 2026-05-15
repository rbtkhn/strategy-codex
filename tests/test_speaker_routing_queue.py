from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import build_speaker_routing_queue as srq  # noqa: E402


def _endswith_all(values: list[str], suffixes: list[str]) -> bool:
    if len(values) != len(suffixes):
        return False
    return all(value.replace("\\", "/").endswith(suffix) for value, suffix in zip(values, suffixes))


def _write_raw(
    raw_root: Path,
    name: str,
    *,
    guest: str = "",
    host: str = "",
    show: str = "",
    thread: str = "",
) -> Path:
    path = raw_root / "2026-05-12" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    guest_line = f"guest: {json.dumps(guest)}\n" if guest else ""
    path.write_text(
        "---\n"
        "pub_date: 2026-05-12\n"
        "title: Example episode\n"
        "source_url: https://www.youtube.com/watch?v=example\n"
        f"host: {json.dumps(host)}\n"
        f"show: {json.dumps(show)}\n"
        f"thread: {json.dumps(thread)}\n"
        f"{guest_line}"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    return path


def _inventory(tmp_path: Path) -> tuple[Path, Path, srq.SpeakerInventory]:
    notebook = tmp_path / "codex" / "2026"
    speakers = notebook / "speakers"
    inventory = srq._discover_inventory(speakers, notebook)
    return notebook, speakers, inventory


def test_guest_matching_existing_speaker_object_routes_to_object_and_candidate_arc_action(tmp_path: Path) -> None:
    notebook, speakers, _ = _inventory(tmp_path)
    obj = speakers / "ritter" / "ritter-speaker-object.md"
    obj.parent.mkdir(parents=True)
    obj.write_text("# Ritter speaker object\n", encoding="utf-8")
    inventory = srq._discover_inventory(speakers, notebook)
    raw = _write_raw(
        notebook / "raw-input",
        "dialogue-works-ritter.md",
        guest="Scott Ritter",
        host="Nima Alkhorshid",
        show="Dialogue Works",
        thread="alkorshid",
    )

    row = srq.build_rows([raw], inventory, notebook)[0]

    assert row["route_type"] == "existing-speaker-object"
    assert row["recommended_route"].endswith("speakers/ritter/ritter-speaker-object.md")
    assert row["primary_route"] == row["recommended_route"]
    assert row["next_action"] == "create-candidate-arc"
    assert row["also_strengthens"][0].endswith("codex/2026/alkorshid/alkorshid-ritter-speaker-arc.md")
    assert row["appearance"]["appearance_id"].startswith("ap-")
    assert row["appearance"]["speaker"] == "Scott Ritter"
    assert row["appearance"]["speaker_slug"] == "ritter"
    assert row["appearance"]["host_slug"] == "alkorshid"
    assert row["appearance"]["speaker_resolution"] == "guest-metadata-match"
    assert row["appearance"]["raw_input_path"].endswith(
        "codex/2026/raw-input/2026-05-12/dialogue-works-ritter.md"
    )
    assert row["confidence"] == "high"
    assert row["evidence_grade"] == "legacy-appearance-only"


def test_existing_speaker_object_and_arc_routes_to_arc_primary(tmp_path: Path) -> None:
    notebook, speakers, _ = _inventory(tmp_path)
    obj = speakers / "macgregor" / "macgregor-speaker-object.md"
    obj.parent.mkdir(parents=True)
    obj.write_text("# Macgregor speaker object\n", encoding="utf-8")
    note = obj.parent / "macgregor-cross-host-note.md"
    note.write_text("# Macgregor cross-host note\n", encoding="utf-8")
    arc = notebook / "davis" / "davis-macgregor-speaker-arc.md"
    arc.parent.mkdir(parents=True)
    arc.write_text("# Davis x Macgregor\n", encoding="utf-8")
    inventory = srq._discover_inventory(speakers, notebook)
    raw = _write_raw(
        notebook / "raw-input",
        "davis-macgregor.md",
        guest="Douglas Macgregor",
        host="Daniel Davis",
        show="Daniel Davis / Deep Dive",
        thread="davis",
    )

    row = srq.build_rows([raw], inventory, notebook)[0]

    assert row["route_type"] == "existing-speaker-arc"
    assert row["recommended_route"].endswith("davis/davis-macgregor-speaker-arc.md")
    assert row["primary_route"] == row["recommended_route"]
    assert row["next_action"] == "update-existing-arc"
    assert _endswith_all(
        row["also_strengthens"],
        [
            "codex/2026/speakers/macgregor/macgregor-speaker-object.md",
            "codex/2026/speakers/macgregor/macgregor-cross-host-note.md",
        ],
    )


def test_host_guest_matching_existing_speaker_arc_routes_to_arc(tmp_path: Path) -> None:
    notebook, speakers, _ = _inventory(tmp_path)
    arc = notebook / "davis" / "davis-macgregor-speaker-arc.md"
    arc.parent.mkdir(parents=True)
    arc.write_text("# Davis x Macgregor\n", encoding="utf-8")
    inventory = srq._discover_inventory(speakers, notebook)
    raw = _write_raw(
        notebook / "raw-input",
        "davis-macgregor.md",
        guest="Douglas Macgregor",
        host="Daniel Davis",
        show="Daniel Davis / Deep Dive",
        thread="davis",
    )

    row = srq.build_rows([raw], inventory, notebook)[0]

    assert row["route_type"] == "existing-speaker-arc"
    assert row["recommended_route"].endswith("davis/davis-macgregor-speaker-arc.md")
    assert row["next_action"] == "update-existing-arc"


def test_existing_speaker_folder_without_object_routes_to_candidate_object(tmp_path: Path) -> None:
    notebook, speakers, _ = _inventory(tmp_path)
    (speakers / "freeman").mkdir(parents=True)
    inventory = srq._discover_inventory(speakers, notebook)
    raw = _write_raw(
        notebook / "raw-input",
        "diesen-freeman.md",
        guest="Chas Freeman",
        host="Glenn Diesen",
        show="Glenn Diesen",
        thread="diesen",
    )

    row = srq.build_rows([raw], inventory, notebook)[0]

    assert row["route_type"] == "candidate-speaker-object"
    assert row["recommended_route"].endswith("speakers/freeman/freeman-speaker-object.md")
    assert row["primary_route"] == row["recommended_route"]
    assert row["also_strengthens"] == []
    assert row["next_action"] == "create-candidate-object"


def test_guest_without_object_or_arc_routes_to_candidate_arc(tmp_path: Path) -> None:
    notebook, speakers, inventory = _inventory(tmp_path)
    raw = _write_raw(
        notebook / "raw-input",
        "diesen-new-guest.md",
        guest="Example Guest",
        host="Glenn Diesen",
        show="Glenn Diesen",
        thread="diesen",
    )

    row = srq.build_rows([raw], inventory, notebook)[0]

    assert row["route_type"] == "candidate-speaker-arc"
    assert row["recommended_route"].endswith("diesen/diesen-guest-speaker-arc.md")
    assert row["appearance"]["speaker"] == "Example Guest"
    assert row["appearance"]["speaker_slug"] == "guest"
    assert row["appearance"]["host_slug"] == "diesen"
    assert row["next_action"] == "create-candidate-arc"
    assert row["appearance"]["speaker_resolution"] == "guest-metadata-slug"
    assert row["evidence_grade"] == "legacy-appearance-only"


def test_monologue_without_matching_speaker_produces_no_route_row(tmp_path: Path) -> None:
    notebook, _speakers, inventory = _inventory(tmp_path)
    raw = _write_raw(
        notebook / "raw-input",
        "mercouris-monologue.md",
        host="Alexander Mercouris",
        show="Alexander Mercouris",
        thread="mercouris",
    )

    rows = srq.build_rows([raw], inventory, notebook)
    unresolved = srq.build_unresolved_rows([raw], inventory)

    assert rows == []
    assert len(unresolved) == 1
    assert unresolved[0]["appearance"]["speaker_slug"] == ""
    assert unresolved[0]["reason"].startswith("Guest metadata is absent or ambiguous")


def test_writes_markdown_and_jsonl_with_stable_fields(tmp_path: Path) -> None:
    notebook, _speakers, inventory = _inventory(tmp_path)
    raw = _write_raw(
        notebook / "raw-input",
        "diesen-new-guest.md",
        guest="Example Guest",
        host="Glenn Diesen",
        show="Glenn Diesen",
        thread="diesen",
    )
    rows = srq.build_rows([raw], inventory, notebook)

    written = srq.write_outputs(rows, tmp_path / "artifacts", date(2026, 5, 12), date(2026, 5, 12))

    jsonl_path = Path(written["jsonl"])
    md_path = Path(written["markdown"])
    appearance_path = Path(written["appearance_ledger"])
    payload = json.loads(jsonl_path.read_text(encoding="utf-8").splitlines()[0])
    assert set(payload) == {
        "raw_input_path",
        "pub_date",
        "title",
        "source_url",
        "host",
        "show",
        "guest",
        "thread",
        "recommended_route",
        "primary_route",
        "also_strengthens",
        "appearance",
        "evidence_grade",
        "route_type",
        "confidence",
        "next_action",
        "reason",
    }
    appearance = json.loads(appearance_path.read_text(encoding="utf-8").splitlines()[0])
    assert appearance == payload["appearance"]
    assert appearance["appearance_id"].startswith("ap-")
    assert appearance["speaker_slug"] == "guest"
    assert appearance["host_slug"] == "diesen"
    assert payload["evidence_grade"] == "legacy-appearance-only"
    md_text = md_path.read_text(encoding="utf-8")
    assert "## candidate-speaker-arc" in md_text
    assert "`create-candidate-arc`" in md_text
    assert "evidence `legacy-appearance-only`" in md_text


def test_appearance_id_is_deterministic(tmp_path: Path) -> None:
    notebook, _speakers, inventory = _inventory(tmp_path)
    raw = _write_raw(
        notebook / "raw-input",
        "diesen-new-guest.md",
        guest="Example Guest",
        host="Glenn Diesen",
        show="Glenn Diesen",
        thread="diesen",
    )

    first = srq.build_rows([raw], inventory, notebook)[0]
    second = srq.build_rows([raw], inventory, notebook)[0]

    assert first["appearance"]["appearance_id"] == second["appearance"]["appearance_id"]


def test_explicit_raw_input_path_mode_preserves_row_shape(tmp_path: Path) -> None:
    notebook, _speakers, inventory = _inventory(tmp_path)
    raw = _write_raw(
        notebook / "raw-input",
        "diesen-new-guest.md",
        guest="Example Guest",
        host="Glenn Diesen",
        show="Glenn Diesen",
        thread="diesen",
    )

    raw_paths = srq.normalize_raw_input_paths([raw])
    rows = srq.build_rows(raw_paths, inventory, notebook)

    assert len(rows) == 1
    assert set(rows[0]) == {
        "raw_input_path",
        "pub_date",
        "title",
        "source_url",
        "host",
        "show",
        "guest",
        "thread",
        "recommended_route",
        "primary_route",
        "also_strengthens",
        "appearance",
        "evidence_grade",
        "route_type",
        "confidence",
        "next_action",
        "reason",
    }
    assert rows[0]["raw_input_path"].endswith("diesen-new-guest.md")


def test_cli_raw_input_mode_excludes_other_same_date_files(tmp_path: Path, capsys) -> None:
    notebook, _speakers, _inventory_obj = _inventory(tmp_path)
    selected = _write_raw(
        notebook / "raw-input",
        "selected.md",
        guest="Example Guest",
        host="Glenn Diesen",
        show="Glenn Diesen",
        thread="diesen",
    )
    _write_raw(
        notebook / "raw-input",
        "same-date-other.md",
        guest="Other Guest",
        host="Glenn Diesen",
        show="Glenn Diesen",
        thread="diesen",
    )
    output_dir = tmp_path / "artifacts"

    rc = srq.main(
        [
            "--raw-input",
            str(selected),
            "--notebook-root",
            str(notebook),
            "--output-dir",
            str(output_dir),
        ]
    )

    captured = capsys.readouterr()
    assert rc == 0
    assert '"rows": 1' in captured.out
    jsonl = next(output_dir.rglob("speaker-routing-queue.jsonl"))
    payloads = [json.loads(line) for line in jsonl.read_text(encoding="utf-8").splitlines()]
    assert len(payloads) == 1
    assert payloads[0]["raw_input_path"].endswith("selected.md")


def test_legacy_host_metadata_keeps_host_slug_separate_from_thread(tmp_path: Path) -> None:
    notebook, speakers, _inventory_obj = _inventory(tmp_path)
    (speakers / "johnson").mkdir(parents=True)
    arc = notebook / "napolitano" / "napolitano-johnson-speaker-arc.md"
    arc.parent.mkdir(parents=True)
    arc.write_text("# Napolitano x Johnson\n", encoding="utf-8")
    raw = notebook / "raw-input" / "2025-12-22" / "napolitano-johnson.md"
    raw.parent.mkdir(parents=True)
    raw.write_text(
        "---\n"
        "pub_date: 2025-12-22\n"
        'title: "Larry Johnson: Why Is the West Ignorant of Russia?"\n'
        "source_url: https://www.youtube.com/watch?v=example\n"
        "host: Judge Andrew Napolitano\n"
        "guest: Larry Johnson\n"
        "thread: johnson\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    inventory = srq._discover_inventory(speakers, notebook)

    row = srq.build_rows([raw], inventory, notebook)[0]

    assert row["route_type"] == "existing-speaker-arc"
    assert row["recommended_route"].endswith("napolitano/napolitano-johnson-speaker-arc.md")
    assert row["appearance"]["speaker_slug"] == "johnson"
    assert row["appearance"]["host_slug"] == "napolitano"
    assert row["evidence_grade"] == "legacy-appearance-only"


def test_davis_ranked_host_alias_canonicalizes_to_davis(tmp_path: Path) -> None:
    notebook, speakers, _inventory_obj = _inventory(tmp_path)
    (speakers / "barnes").mkdir(parents=True)
    arc = notebook / "davis" / "davis-barnes-speaker-arc.md"
    arc.parent.mkdir(parents=True)
    arc.write_text("# Davis x Barnes\n", encoding="utf-8")
    raw = notebook / "raw-input" / "2026-04-03" / "davis-barnes.md"
    raw.parent.mkdir(parents=True)
    raw.write_text(
        "---\n"
        "pub_date: 2026-04-03\n"
        'title: "Robert Barnes on war crimes, Iran, and Hormuz"\n'
        "source_url: https://www.youtube.com/watch?v=example\n"
        "show: Daniel Davis Deep Dive\n"
        "host: Lt Col Daniel Davis\n"
        "guest: Robert Barnes\n"
        "thread: davis\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    inventory = srq._discover_inventory(speakers, notebook)

    row = srq.build_rows([raw], inventory, notebook)[0]

    assert row["route_type"] == "existing-speaker-arc"
    assert row["recommended_route"].endswith("davis/davis-barnes-speaker-arc.md")
    assert row["appearance"]["speaker_slug"] == "barnes"
    assert row["appearance"]["host_slug"] == "davis"


def test_dialogue_works_short_host_alias_canonicalizes_to_alkorshid(tmp_path: Path) -> None:
    notebook, speakers, _inventory_obj = _inventory(tmp_path)
    (speakers / "freeman").mkdir(parents=True)
    arc = notebook / "alkorshid" / "alkorshid-freeman-speaker-arc.md"
    arc.parent.mkdir(parents=True)
    arc.write_text("# Alkhorshid x Freeman\n", encoding="utf-8")
    raw = notebook / "raw-input" / "2025-10-17" / "alkorshid-freeman.md"
    raw.parent.mkdir(parents=True)
    raw.write_text(
        "---\n"
        "pub_date: 2025-10-17\n"
        'title: "Amb. Chas Freeman: How the U.S. Is Spiraling Toward Disaster"\n'
        "source_url: https://www.youtube.com/watch?v=example\n"
        "show: Dialogue Works\n"
        "host: Nima\n"
        "guest: Chas Freeman\n"
        "thread: freeman\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    inventory = srq._discover_inventory(speakers, notebook)

    row = srq.build_rows([raw], inventory, notebook)[0]

    assert row["route_type"] == "existing-speaker-arc"
    assert row["recommended_route"].endswith("alkorshid/alkorshid-freeman-speaker-arc.md")
    assert row["appearance"]["speaker_slug"] == "freeman"
    assert row["appearance"]["host_slug"] == "alkorshid"


def test_cleaned_transcript_grade_is_preserved(tmp_path: Path) -> None:
    notebook, speakers, _inventory_obj = _inventory(tmp_path)
    obj = speakers / "johnson" / "johnson-speaker-object.md"
    obj.parent.mkdir(parents=True)
    obj.write_text("# Johnson\n", encoding="utf-8")
    arc = notebook / "davis" / "davis-johnson-speaker-arc.md"
    arc.parent.mkdir(parents=True)
    arc.write_text("# Davis x Johnson\n", encoding="utf-8")
    raw = notebook / "raw-input" / "2026-05-05" / "davis-johnson.md"
    raw.parent.mkdir(parents=True)
    raw.write_text(
        "---\n"
        "pub_date: 2026-05-05\n"
        "title: Johnson on Hormuz\n"
        "source_url: https://www.youtube.com/watch?v=example\n"
        "kind: cleaned-transcript\n"
        "source_type: youtube\n"
        "transcript_type: auto_subtitles_vtt\n"
        "source_note: Auto-captions extracted with yt_dlp.\n"
        "host: Daniel Davis\n"
        "show: Daniel Davis Deep Dive\n"
        "guest: Larry Johnson\n"
        "thread: davis\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    inventory = srq._discover_inventory(speakers, notebook)

    row = srq.build_rows([raw], inventory, notebook)[0]

    assert row["evidence_grade"] == "cleaned-transcript"


def test_summary_grade_is_preserved(tmp_path: Path) -> None:
    notebook, speakers, _inventory_obj = _inventory(tmp_path)
    obj = speakers / "mearsheimer" / "mearsheimer-speaker-object.md"
    obj.parent.mkdir(parents=True)
    obj.write_text("# Mearsheimer\n", encoding="utf-8")
    arc = notebook / "napolitano" / "napolitano-mearsheimer-speaker-arc.md"
    arc.parent.mkdir(parents=True)
    arc.write_text("# Napolitano x Mearsheimer\n", encoding="utf-8")
    raw = notebook / "raw-input" / "2026-04-28" / "napolitano-mearsheimer.md"
    raw.parent.mkdir(parents=True)
    raw.write_text(
        "---\n"
        "pub_date: 2026-04-28\n"
        "title: Mearsheimer on how Trump lost his war\n"
        "source_url: https://www.youtube.com/watch?v=example\n"
        "source_type: operator-note-derived-youtube\n"
        "transcript_type: operator_summary_from_cleaned_transcript\n"
        "editorial_note: summary\n"
        "host: Judge Andrew Napolitano\n"
        "guest: John Mearsheimer\n"
        "thread: mearsheimer\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    inventory = srq._discover_inventory(speakers, notebook)

    row = srq.build_rows([raw], inventory, notebook)[0]

    assert row["evidence_grade"] == "summary-grade"


def test_appearance_id_is_stable_across_file_renames(tmp_path: Path) -> None:
    notebook, _speakers, inventory = _inventory(tmp_path)
    raw1 = _write_raw(
        notebook / "raw-input",
        "first-name.md",
        guest="Example Guest",
        host="Glenn Diesen",
        show="Glenn Diesen",
        thread="diesen",
    )
    raw2 = _write_raw(
        notebook / "raw-input",
        "second-name.md",
        guest="Example Guest",
        host="Glenn Diesen",
        show="Glenn Diesen",
        thread="diesen",
    )
    for raw in (raw1, raw2):
        text = raw.read_text(encoding="utf-8")
        text = text.replace("source_url: https://www.youtube.com/watch?v=example", "source_url: https://www.youtube.com/watch?v=sameid12345")
        raw.write_text(text, encoding="utf-8")

    first = srq.build_rows([raw1], inventory, notebook)[0]
    second = srq.build_rows([raw2], inventory, notebook)[0]

    assert first["appearance"]["appearance_id"] == second["appearance"]["appearance_id"]
