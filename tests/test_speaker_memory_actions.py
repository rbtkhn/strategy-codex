from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import build_speaker_memory_actions as sma  # noqa: E402

def row(
    appearance_id: str,
    *,
    speaker: str = "beebe",
    host: str = "diesen",
    route_type: str = "existing-voice-arc",
    next_action: str = "update-existing-arc",
    primary: str = "continuity/years/2026/diesen/arc-beebe-diesen-host.md",
    also: list[str] | None = None,
) -> dict:
    return {
        "appearance": {
            "appearance_id": appearance_id,
            "speaker": speaker.title(),
            "speaker_slug": speaker,
            "guest": speaker.title(),
            "host": host.title(),
            "host_slug": host,
            "show": host.title(),
            "thread": host,
            "pub_date": "2026-05-12",
            "title": "Example",
            "source_url": f"https://www.youtube.com/watch?v={appearance_id[-11:]}",
            "raw_input_path": f"source-archive/statecraft/2026-05-12/{appearance_id}.md",
        },
        "route_type": route_type,
        "next_action": next_action,
        "recommended_route": primary,
        "primary_route": primary,
        "also_strengthens": also or [],
        "evidence_grade": "transcript-bearing",
        "reason": "test route",
    }

def test_existing_arc_route_emits_update_action() -> None:
    actions = sma.build_actions([row("ap-arc0000001")])

    assert len(actions) == 1
    assert actions[0]["action_type"] == "update-existing-arc"
    assert actions[0]["priority"] == "high"
    assert actions[0]["target_path"] == "continuity/years/2026/diesen/arc-beebe-diesen-host.md"
    assert actions[0]["evidence_appearances"] == ["ap-arc0000001"]

def test_existing_object_with_candidate_arc_emits_create_candidate_arc() -> None:
    actions = sma.build_actions(
        [
            row(
                "ap-object0001",
                route_type="existing-voice-object",
                next_action="create-candidate-arc",
                primary="statecraft/voices/beebe/beebe-speaker-object.md",
                also=["continuity/years/2026/davis/davis-beebe-speaker-arc.md"],
            )
        ]
    )

    assert len(actions) == 1
    assert actions[0]["action_type"] == "create-candidate-arc"
    assert actions[0]["target_path"] == "continuity/years/2026/davis/davis-beebe-speaker-arc.md"

def test_candidate_object_route_emits_create_candidate_object() -> None:
    actions = sma.build_actions(
        [
            row(
                "ap-object0002",
                speaker="guest",
                route_type="candidate-voice-object",
                next_action="create-candidate-object",
                primary="statecraft/voices/guest/guest-speaker-object.md",
            )
        ]
    )

    assert actions[0]["action_type"] == "create-candidate-object"
    assert actions[0]["target_path"].endswith("guest-speaker-object.md")

def test_repeated_speaker_across_hosts_emits_consider_helix() -> None:
    actions = sma.build_actions(
        [
            row("ap-host000001", speaker="marandi", host="diesen"),
            row(
                "ap-host000002",
                speaker="marandi",
                host="davis",
                primary="continuity/years/2026/davis/arc-marandi-davis-host.md",
            ),
        ]
    )

    helix = [action for action in actions if action["action_type"] == "consider-helix"]
    assert len(helix) == 1
    assert helix[0]["target_path"] == "statecraft/voices/marandi/marandi-helix.md"
    assert helix[0]["evidence_appearances"] == ["ap-host000001", "ap-host000002"]

def test_existing_cross_host_note_suppresses_consider_helix() -> None:
    actions = sma.build_actions(
        [
            row(
                "ap-host000003",
                speaker="beebe",
                host="diesen",
                also=["statecraft/voices/beebe/beebe-cross-host-note.md"],
            ),
            row("ap-host000004", speaker="beebe", host="davis"),
        ]
    )

    assert "consider-helix" not in {action["action_type"] for action in actions}

def test_monologue_is_excluded_by_default_and_included_when_requested() -> None:
    monologue = row(
        "ap-mono000001",
        speaker="",
        host="mercouris",
        route_type="no-clear-route",
        next_action="no-action",
        primary="",
    )

    assert sma.build_actions([monologue]) == []
    actions = sma.build_actions([monologue], include_no_action=True)
    assert actions[0]["action_type"] == "no-action"
    assert actions[0]["priority"] == "low"

def test_writes_markdown_and_jsonl_with_stable_fields(tmp_path: Path) -> None:
    rows = [row("ap-write00001")]
    actions = sma.build_actions(rows)

    written = sma.write_outputs(
        rows=rows,
        actions=actions,
        output_dir=tmp_path / "runtime/artifacts",
        start=date(2026, 5, 12),
        end=date(2026, 5, 12),
    )

    action_jsonl = Path(written["memory_action_queue_jsonl"])
    action_md = Path(written["memory_action_queue_markdown"])
    rollup_json = Path(written["appearance_rollup_json"])
    payload = json.loads(action_jsonl.read_text(encoding="utf-8").splitlines()[0])
    assert set(payload) == {
        "action_id",
        "action_type",
        "priority",
        "target_path",
        "speaker_slug",
        "host_slug",
        "evidence_appearances",
        "evidence_grades",
        "reason",
        "operator_instruction",
    }
    assert payload["action_id"].startswith("act-")
    assert payload["evidence_grades"] == ["transcript-bearing"]
    assert "Speaker memory action queue" in action_md.read_text(encoding="utf-8")
    assert json.loads(rollup_json.read_text(encoding="utf-8"))["appearance_count"] == 1
