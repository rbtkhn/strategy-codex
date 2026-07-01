"""Tests for epistemic observation layer (PR2)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
EPISTEMIC_ROOT = REPO_ROOT / "statecraft" / "epistemic"
FIXTURE_VOICE_DIR = EPISTEMIC_ROOT / "observation" / "voice_captures"

if str(EPISTEMIC_ROOT) not in sys.path:
    sys.path.insert(0, str(EPISTEMIC_ROOT))

from observation.loader import load_voice_captures, write_observations  # noqa: E402
from observation.parser import extract_sentences, parse_voice_capture  # noqa: E402
from pipeline.run_pipeline import run_observation_layer  # noqa: E402


def test_extract_sentences_splits_on_punctuation() -> None:
    text = "First claim. Second claim! Third claim?"
    assert extract_sentences(text) == ["First claim", "Second claim", "Third claim"]


def test_parse_voice_capture_deterministic_id() -> None:
    kwargs = {
        "voice": "macgregor",
        "source_file": "statecraft/epistemic/observation/voice_captures/macgregor/sample.md",
        "text": "Escalation is likely.",
        "mtime_iso": "2026-01-23T12:00:00+00:00",
    }
    first = parse_voice_capture(**kwargs)
    second = parse_voice_capture(**kwargs)
    assert first["observation_id"] == second["observation_id"]
    assert first["sentences"] == ["Escalation is likely"]


def test_parse_voice_capture_includes_all_sentences() -> None:
    obs = parse_voice_capture(
        voice="macgregor",
        source_file="test/sample.md",
        text="The US will face constraints. Neutral line.",
        mtime_iso="2026-01-23T12:00:00+00:00",
    )
    assert obs["sentences"] == ["The US will face constraints", "Neutral line"]


def test_load_voice_captures_from_fixtures() -> None:
    observations = load_voice_captures(voice_dir=FIXTURE_VOICE_DIR, repo_root=REPO_ROOT)
    assert len(observations) >= 2
    voices = {obs["voice"] for obs in observations}
    assert "macgregor" in voices
    assert "freeman" in voices
    macgregor = next(o for o in observations if o["voice"] == "macgregor")
    assert len(macgregor["sentences"]) >= 2


def test_write_observations_envelope(tmp_path: Path) -> None:
    observations = [
        parse_voice_capture(
            voice="macgregor",
            source_file="test/sample.md",
            text="Escalation is likely.",
            mtime_iso="2026-01-23T12:00:00+00:00",
        )
    ]
    out_path = tmp_path / "observations.json"
    write_observations(observations, out_path=out_path)
    payload = json.loads(out_path.read_text(encoding="utf-8"))
    assert payload["_meta"]["layer"] == "observation"
    assert payload["_meta"]["row_count"] == 1
    assert len(payload["observations"]) == 1


def test_run_observation_layer_integration(tmp_path: Path) -> None:
    voice_dir = tmp_path / "voice_captures" / "macgregor"
    voice_dir.mkdir(parents=True)
    (voice_dir / "sample.md").write_text(
        "The US will face severe constraints. Neutral line.",
        encoding="utf-8",
    )
    out_path = tmp_path / "observations.json"
    observations = run_observation_layer(
        voice_dir=voice_dir.parent,
        out_path=out_path,
        repo_root=tmp_path,
        write=True,
    )
    assert len(observations) == 1
    assert out_path.is_file()
    payload = json.loads(out_path.read_text(encoding="utf-8"))
    assert len(payload["observations"][0]["sentences"]) == 2
