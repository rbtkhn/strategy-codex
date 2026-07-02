"""Tests for scripts/build_two_pillar_notebook_graph.py (non-authoritative)."""

from __future__ import annotations

import json
import shutil
import sys
import uuid
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from build_two_pillar_notebook_graph import (  # noqa: E402
    _guess_guest_block,
    build_graph,
    DEFAULT_RAW_INPUT_ROOT,
    render_markdown,
)
from backfill_youtube_channel_raw_input import convert_index_to_raw_input  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent

def _write_index(path: Path, videos: list[dict[str, str]]) -> None:
    path.write_text(json.dumps({"videos": videos}, indent=2), encoding="utf-8")

def _write_raw_input(path: Path, *, frontmatter: str, body: str) -> None:
    path.write_text(f"---\n{frontmatter}\n---\n{body}\n", encoding="utf-8")

def test_default_raw_input_root_points_to_2026_volume() -> None:
    assert DEFAULT_RAW_INPUT_ROOT == REPO_ROOT / "codex" / "2026" / "raw-input"

def test_guess_guest_block_handles_embedded_guest_names() -> None:
    assert (
        _guess_guest_block(
            "Nima x Glenn Diesen - Iran, War, and Order",
            pillar_id="nima",
        )
        == "Glenn Diesen"
    )
    assert (
        _guess_guest_block(
            "Lt Col Daniel Davis & Ian Proud: More Iran Strikes, NOT a Strategy",
            pillar_id="davis",
        )
        == "Ian Proud"
    )
    assert (
        _guess_guest_block(
            "President Putin asked by Glenn Diesen: Russia's Reaction to Sweden and Finland Joining NATO",
            pillar_id="diesen",
        )
        == "Vladimir Putin"
    )
    assert (
        _guess_guest_block(
            "Fractured Iran or fractured Trump? w/ Robert Barnes (Live)",
            pillar_id="mercouris_duran",
        )
        == "Robert Barnes"
    )
    assert _guess_guest_block("BREAKING: Trump", pillar_id="diesen") is None
    assert _guess_guest_block("EU", pillar_id="diesen") is None
    assert _guess_guest_block("A Closer Look Inside U.S. Operations /Larry Johnson", pillar_id="diesen") == "Larry Johnson"

def test_build_graph_creates_polyphonic_cognition_streams_and_cohost_nodes() -> None:
    temp_root = REPO_ROOT / f".cognition-stream-test-{uuid.uuid4().hex}"
    temp_root.mkdir(parents=True, exist_ok=False)
    try:
        dialogue_index = temp_root / "dialogue-index.json"
        diesen_index = temp_root / "diesen-index.json"
        davis_index = temp_root / "davis-index.json"
        raw_root = temp_root / "raw-input"
        raw_root.mkdir()

        _write_index(
            dialogue_index,
            [
                {
                    "video_id": "dw000000001",
                    "title": "Jeffrey Sachs: The Global Order Is Shifting",
                    "upload_date": "20250501",
                    "url": "https://www.youtube.com/watch?v=dw000000001",
                },
                {
                    "video_id": "dw000000002",
                    "title": "Scott Ritter: This Is the Moment the West Started Losing",
                    "upload_date": "20250502",
                    "url": "https://www.youtube.com/watch?v=dw000000002",
                },
            ],
        )
        _write_index(
            diesen_index,
            [
                {
                    "video_id": "ds000000001",
                    "title": "Jeffrey Sachs: The Global Order Is Shifting",
                    "upload_date": "20250503",
                    "url": "https://www.youtube.com/watch?v=ds000000001",
                },
                {
                    "video_id": "ds000000002",
                    "title": "Warwick Powell: Energy Sovereignty and Multipolar Transition",
                    "upload_date": "20250504",
                    "url": "https://www.youtube.com/watch?v=ds000000002",
                },
            ],
        )
        _write_index(
            davis_index,
            [
                {
                    "video_id": "dv000000001",
                    "title": "Jeffrey Sachs: The Global Order Is Shifting",
                    "upload_date": "20250505",
                    "url": "https://www.youtube.com/watch?v=dv000000001",
                },
                {
                    "video_id": "dv000000002",
                    "title": "Lt Col Daniel Davis & Ian Proud: More Iran Strikes, NOT a Strategy",
                    "upload_date": "20250506",
                    "url": "https://www.youtube.com/watch?v=dv000000002",
                },
            ],
        )

        _write_raw_input(
            raw_root / "2025-05-07.md",
            frontmatter="\n".join(
                [
                    'pub_date: 2025-05-07',
                    'show: The Duran',
                    'host: Alexander Mercouris',
                    'thread: mercouris',
                    'participants: [mercouris, jeffrey sachs, christoforou]',
                    'source_url: https://www.youtube.com/watch?v=TBD-mercouris-2025-05-07',
                    'title: "Jeffrey Sachs joins Alexander Mercouris and Alex Christoforou"',
                ]
            ),
            body=(
                "# Jeffrey Sachs joins Alexander Mercouris and Alex Christoforou\n"
                "**Participants:** Alexander Mercouris, Jeffrey Sachs, Alex Christoforou"
            ),
        )
        _write_raw_input(
            raw_root / "2025-05-08.md",
            frontmatter="\n".join(
                [
                    'pub_date: 2025-05-08',
                    'show: The Duran',
                    'host: Alexander Mercouris',
                    'thread: mercouris',
                    'speaker: Alexander Mercouris',
                    'source_url: https://www.youtube.com/watch?v=TBD-mercouris-2025-05-08',
                    'title: "Alexander Mercouris – Iran and Europe"',
                ]
            ),
            body=(
                "# Alexander Mercouris – Iran and Europe\n"
                "**Speaker:** Alexander Mercouris"
            ),
        )

        graph = build_graph(
            dialogue_index=dialogue_index,
            diesen_index=diesen_index,
            davis_index=davis_index,
            raw_input_root=raw_root,
        )

        assert graph["schema_version"] == "2.0.0-cognition-streams-graph"
        assert graph["title"] == "Polyphonic Cognition Streams"
        assert graph["stream_model"]["analysis_mode"] == "contrapuntal comparison"
        assert graph["summary"]["episodes_total"] == 8
        assert graph["summary"]["status_counts"]["provisional"] == 1
        assert graph["summary"]["cohosts_total"] == 1
        assert graph["summary"]["bridge_guests_total"] >= 1
        assert graph["summary"]["episodes_by_pillar"]["mercouris_duran"] == 2
        assert graph["summary"]["episodes_by_stream"]["crooke"] == 0
        assert graph["summary"]["raw_inputs_by_stream"]["pape"] == 0
        assert graph["summary"]["guests_by_pillar"]["mercouris_duran"] == 1
        assert graph["summary"]["cohosts_by_pillar"]["mercouris_duran"] == 1

        guests = {node["guest_id"]: node for node in graph["nodes"] if node["type"] == "guest"}
        bridges = {node["guest_id"]: node for node in graph["nodes"] if node["type"] == "bridge"}
        cohosts = {node["cohost_id"]: node for node in graph["nodes"] if node["type"] == "cohost"}
        episodes = {node["episode_id"]: node for node in graph["nodes"] if node["type"] == "episode"}
        streams = {node["stream_id"]: node for node in graph["nodes"] if node["type"] == "stream"}

        assert set(streams) == {
            "nima",
            "diesen",
            "davis",
            "mercouris_duran",
            "crooke",
            "parsi",
            "pape",
            "ritter",
        }
        assert streams["nima"]["display_name"] == "Nima"
        assert streams["mercouris_duran"]["display_name"] == "Mercouris"
        assert streams["mercouris_duran"]["source_channels"] == ["@AlexMercouris", "@TheDuran"]
        assert streams["nima"]["axis_label"] == "Synthesis"
        assert streams["diesen"]["axis_label"] == "Order"
        assert streams["davis"]["axis_label"] == "Conflict"
        assert streams["mercouris_duran"]["axis_label"] == "Statecraft"
        assert streams["crooke"]["stream_kind"] == "expert_lens"
        assert streams["pape"]["voice_note"].startswith("Escalation")

        assert episodes["https://www.youtube.com/watch?v=dw000000001"]["status"] == "needs_capture"
        assert episodes["https://www.youtube.com/watch?v=ds000000001"]["status"] == "needs_capture"
        assert episodes["https://www.youtube.com/watch?v=dv000000002"]["routing"]["host_thread"] == "thread:davis"
        assert episodes["https://www.youtube.com/watch?v=TBD-mercouris-2025-05-07"]["source"]["source_channel"] == "@TheDuran"
        assert episodes["https://www.youtube.com/watch?v=TBD-mercouris-2025-05-07"]["cohost_ids"] == [
            "alex-christoforou"
        ]
        assert episodes["https://www.youtube.com/watch?v=TBD-mercouris-2025-05-07"]["source"]["source_url_is_synthetic"] is True
        assert episodes["https://www.youtube.com/watch?v=TBD-mercouris-2025-05-07"]["source"]["source_url_status"] == "provisional"
        assert episodes["https://www.youtube.com/watch?v=TBD-mercouris-2025-05-08"]["status"] == "provisional"

        assert cohosts["alex-christoforou"]["episode_count"] == 1
        assert "alex-christoforou" not in guests

        assert guests["jeffrey-sachs"]["is_bridge"] is True
        assert guests["jeffrey-sachs"]["pillar_ids"] == [
            "nima",
            "davis",
            "diesen",
            "mercouris_duran",
        ]
        assert bridges["jeffrey-sachs"]["episode_counts_by_pillar"] == {
            "nima": 1,
            "davis": 1,
            "diesen": 1,
            "mercouris_duran": 1,
        }

        markdown = render_markdown(graph)
        assert "# Polyphonic Cognition Streams" in markdown
        assert "count-neutral lattice of cognition streams" in markdown
        assert "contrapuntal comparison" in markdown
        assert "Automation readiness" in markdown
        assert "Mercouris" in markdown
        assert "Alexander Mercouris / The Duran" in markdown
        assert "Dialogue Works" in markdown
        assert "Four-Pillar" not in markdown
        assert "## Cohosts" in markdown
        assert "Alex Christoforou" in markdown
        assert "## Motif Clusters" in markdown
        assert "## Bridge Roles" in markdown
        assert "## Contrapuntal Notes" in markdown
        assert "## Source Provenance" in markdown
        assert "Cohost lane keeps Alex Christoforou visible" in markdown
        assert "CIV-MEM" not in markdown
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)

def test_index_only_backfill_writes_raw_input_without_transcript_body() -> None:
    temp_root = REPO_ROOT / f".index-only-test-{uuid.uuid4().hex}"
    temp_root.mkdir(parents=True, exist_ok=False)
    try:
        output_dir = temp_root / "youtube-index"
        notebook_root = temp_root / "notebook"
        output_dir.mkdir()
        notebook_root.mkdir()
        (output_dir / "index.json").write_text(
            json.dumps(
                {
                    "videos": [
                        {
                            "video_id": "abc123def45",
                            "title": "Alexander Mercouris: Daily Briefing on Europe and Iran",
                            "upload_date": "20260501",
                            "url": "https://www.youtube.com/watch?v=abc123def45",
                        }
                    ]
                },
                indent=2,
            ),
            encoding="utf-8",
        )

        rc = convert_index_to_raw_input(
            output_dir=output_dir,
            notebook_root=notebook_root,
            ingest_date="2026-05-02",
            apply=True,
            channel_slug="alex-mercouris",
            channel_url="https://www.youtube.com/@AlexMercouris/videos",
            show="Alexander Mercouris",
            host="Alexander Mercouris",
            thread="mercouris",
            file_prefix="youtube-alex-mercouris",
            source_note="Index mirror for direct channel capture.",
            infer_guest=True,
            index_only=True,
        )

        assert rc == 0
        raw_files = list((notebook_root / "raw-input").rglob("*.md"))
        assert len(raw_files) == 1
        raw_text = raw_files[0].read_text(encoding="utf-8")
        assert "pub_date: 2026-05-01" in raw_text
        assert "source_url: \"https://www.youtube.com/watch?v=abc123def45\"" in raw_text
        assert "# Alexander Mercouris: Daily Briefing on Europe and Iran" in raw_text
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)

def test_codex_2026_author_shelves_include_civ_mem_fields() -> None:
    authors = ["nima", "diesen", "mercouris", "davis", "pape", "parsi", "ritter", "crooke"]
    for author in authors:
        shelf = REPO_ROOT / "codex" / "2026" / author
        assert (shelf / "README.md").is_file()
        assert (shelf / f"{author}-profile.md").is_file()
        assert (shelf / f"{author}-book-2026-04.md").is_file()
        assert (shelf / f"{author}-chapter-2026-04-01.md").is_file()
        assert list(shelf.glob(f"{author}-page-2026-04-01*.md"))
        book = (shelf / f"{author}-book-2026-04.md").read_text(encoding="utf-8")
        assert "## Civ-Mem Fields" in book
        assert "Fit / mismatch / falsifier" in book
        assert "legitimacy and continuity" in book
        assert "narrative authority" in book

    resonance = (REPO_ROOT / "codex" / "2026" / "civ-mem-resonance-2026-04.md").read_text(encoding="utf-8")
    assert "Monthly lattice note" in resonance
    assert "Fit / mismatch / falsifier" in resonance
    assert "not Record" in resonance
