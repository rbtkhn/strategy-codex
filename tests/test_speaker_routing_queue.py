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


def test_guest_matching_existing_speaker_object_routes_to_object(tmp_path: Path) -> None:
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
    assert row["confidence"] == "high"


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


def test_monologue_without_matching_speaker_route_is_no_clear_route(tmp_path: Path) -> None:
    notebook, _speakers, inventory = _inventory(tmp_path)
    raw = _write_raw(
        notebook / "raw-input",
        "mercouris-monologue.md",
        host="Alexander Mercouris",
        show="Alexander Mercouris",
        thread="mercouris",
    )

    row = srq.build_rows([raw], inventory, notebook)[0]

    assert row["route_type"] == "no-clear-route"
    assert row["recommended_route"] == ""


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
        "route_type",
        "confidence",
        "reason",
    }
    assert "## candidate-speaker-arc" in md_path.read_text(encoding="utf-8")
