from __future__ import annotations

import json
from pathlib import Path

import pytest

from integrations.presentations.civ_emp_adapter import CIV_EMP_ROOT, build_civ_emp_bundle, build_civ_emp_packet_bundle
from integrations.presentations.ph_civ_adapter import build_ph_civ_bundle, build_ph_mus_packet_bundle

REPO_ROOT = Path(__file__).resolve().parent.parent
EXAMPLES_ROOT = REPO_ROOT / "runtime/artifacts" / "presentations" / "examples"


def test_civ_emp_adapter_marks_work_safe_bundle() -> None:
    bundle = build_civ_emp_bundle(
        intent="briefing",
        title="CIV-EMP Briefing",
        audience="Operators",
    )
    assert bundle["family"] == "civ-emp"
    assert bundle["subsurface"] == "ce-emp"
    assert bundle["artifact_class"] == "statecraft_brief"
    assert bundle["policy"]["classification"] == "work_public_safe"
    assert bundle["policy"]["approved_for_render"] is True
    assert bundle["source_items"]


def test_civ_emp_adapter_rejects_outside_paths(tmp_path: Path) -> None:
    outside = tmp_path / "outside.md"
    outside.write_text("x", encoding="utf-8")
    with pytest.raises(ValueError, match="not under"):
        build_civ_emp_bundle(
            intent="briefing",
            title="Bad",
            audience="Operators",
            source_paths=[outside],
        )


def test_civ_emp_adapter_rejects_ce_mus_without_packet_input() -> None:
    with pytest.raises(ValueError, match="require packet_json input"):
        build_civ_emp_bundle(
            intent="summary",
            title="CE-MUS summary",
            audience="Operators",
            subsurface="ce-mus",
        )


def test_civ_emp_packet_bundle_accepts_ce_mus_summary(tmp_path: Path) -> None:
    packet = tmp_path / "ce-mus.json"
    packet.write_text(
        json.dumps(
            {
                "packet_type": "ce_mus_packet",
                "subsurface": "ce-mus",
                "artifact_class": "strategic_exhibit",
                "source_id": "ce-mus-demo",
                "source_items": [
                    {
                        "id": "ce-mus-demo:1",
                        "title": "Object 1",
                        "text": "Interpretive object text",
                        "citation": "packet:ce-mus-demo:1",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    bundle = build_civ_emp_packet_bundle(
        intent="summary",
        title="CE-MUS summary",
        audience="Operators",
        subsurface="ce-mus",
        packet_path=packet,
    )
    assert bundle["subsurface"] == "ce-mus"
    assert bundle["artifact_class"] == "strategic_exhibit"
    assert bundle["policy"]["source_mode"] == "strategy-codex-ce-mus-packet"
    assert bundle["presentation_hints"]["section_order"][0] == "Exhibit Summary"


def test_civ_emp_packet_bundle_rejects_subsurface_drift(tmp_path: Path) -> None:
    packet = tmp_path / "ce-emp.json"
    packet.write_text(
        json.dumps(
            {
                "packet_type": "ce_emp_packet",
                "subsurface": "ce-civ",
                "source_id": "ce-emp-demo",
                "source_items": [
                    {
                        "id": "ce-emp-demo:1",
                        "title": "Brief",
                        "text": "Decision packet text",
                        "citation": "packet:ce-emp-demo:1",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="does not match requested subsurface"):
        build_civ_emp_packet_bundle(
            intent="briefing",
            title="CE-EMP briefing",
            audience="Operators",
            subsurface="ce-emp",
            packet_path=packet,
        )


def test_civ_emp_packet_bundle_accepts_decision_comparison_packet(tmp_path: Path) -> None:
    packet = tmp_path / "ce-emp-comparison.json"
    packet.write_text(
        json.dumps(
            {
                "packet_type": "ce_emp_decision_comparison_packet",
                "subsurface": "ce-emp",
                "artifact_class": "decision_comparison",
                "source_id": "ce-emp-compare",
                "source_items": [
                    {
                        "id": "ce-emp-compare:1",
                        "title": "Option A",
                        "text": "Decision path A",
                        "citation": "packet:ce-emp-compare:1",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    bundle = build_civ_emp_packet_bundle(
        intent="comparison",
        title="CE-EMP comparison",
        audience="Operators",
        subsurface="ce-emp",
        packet_path=packet,
    )
    assert bundle["artifact_class"] == "decision_comparison"
    assert bundle["presentation_hints"]["section_order"][0] == "Comparison Frame"


def test_ph_civ_adapter_rejects_forbidden_local_residue() -> None:
    forbidden = Path("C:/dev/strategy-codex/codex/predictive-history/fake.md")
    with pytest.raises(ValueError, match="forbidden local Predictive History residue"):
        build_ph_civ_bundle(
            intent="lesson",
            title="PH lesson",
            audience="Readers",
            source_paths=[forbidden],
        )


def test_ph_civ_adapter_accepts_explicit_public_packet_for_ph_apo(tmp_path: Path) -> None:
    packet = tmp_path / "public-packet.json"
    packet.write_text(
        json.dumps(
            {
                "packet_type": "ph_public_packet",
                "public": True,
                "source_id": "gt-16",
                "subsurface": "ph-apo",
                "title": "PH-APO lesson",
                "source_items": [
                    {
                        "id": "gt-16:1",
                        "title": "GT-16 packet excerpt",
                        "text": "Visible text",
                        "citation": "public packet gt-16",
                        "kind": "public_packet",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    bundle = build_ph_civ_bundle(
        intent="lesson",
        title="PH-APO lesson",
        audience="Readers",
        source_paths=[packet],
        public_ids=["gt-16"],
        subsurface="ph-apo",
    )
    assert bundle["family"] == "ph-civ"
    assert bundle["subsurface"] == "ph-apo"
    assert bundle["artifact_class"] == "chapter_packet"
    assert bundle["policy"]["classification"] == "public"
    assert bundle["source_items"][0]["public"] is True


def test_ph_civ_adapter_rejects_non_packet_source_file(tmp_path: Path) -> None:
    packet = tmp_path / "public-packet.md"
    packet.write_text("# Not a packet\n\nVisible text", encoding="utf-8")
    with pytest.raises(ValueError, match="valid JSON"):
        build_ph_civ_bundle(
            intent="summary",
            title="PH-CIV summary",
            audience="Readers",
            source_paths=[packet],
            subsurface="ph-civ",
        )


def test_ph_civ_adapter_rejects_packet_with_private_markers(tmp_path: Path) -> None:
    packet = tmp_path / "public-packet.json"
    packet.write_text(
        json.dumps(
            {
                "packet_type": "ph_public_packet",
                "public": True,
                "source_id": "gt-16",
                "subsurface": "ph-apo",
                "title": "PH-APO lesson",
                "source_items": [
                    {
                        "id": "gt-16:1",
                        "title": "GT-16 packet excerpt",
                        "text": "Visible text",
                        "citation": "C:/private/source.md",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="forbidden private marker"):
        build_ph_civ_bundle(
            intent="lesson",
            title="PH-APO lesson",
            audience="Readers",
            source_paths=[packet],
            subsurface="ph-apo",
        )


def test_ph_mus_packet_bundle_rejects_private_markers(tmp_path: Path) -> None:
    packet = tmp_path / "ph-mus.json"
    packet.write_text(
        json.dumps(
            {
                "packet_type": "ph_mus_packet",
                "source_id": "gt-16",
                "museum_exhibit_path": "corpus/media-packs/gt-16.md",
                "visitor_path": ["entrance_artifact"],
                "runtime/artifacts": [{"local_vault_path": "C:/private/file.png"}],
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="forbidden private marker"):
        build_ph_mus_packet_bundle(
            intent="lesson",
            title="GT-16 museum lesson",
            audience="Readers",
            packet_path=packet,
        )


def test_ph_mus_packet_bundle_accepts_public_packet(tmp_path: Path) -> None:
    packet = tmp_path / "ph-mus.json"
    packet.write_text(
        json.dumps(
            {
                "packet_type": "ph_mus_packet",
                "source_id": "gt-16",
                "title": "GT-16 museum",
                "surface": "ph-apo",
                "museum_status": "curated_draft",
                "museum_exhibit_path": "corpus/media-packs/gt-16.md",
                "route_type": "application",
                "what_changes_here": "Pressure shifts become legible through exhibit sequencing.",
                "caveat": "Public orientation only.",
                "conceptual_volumes": ["volume_ii"],
                "visitor_path": ["entrance_artifact", "pressure_systems"],
                "runtime/artifacts": [
                    {
                        "artifact_id": "gt16-map-1",
                        "title": "Map",
                        "room": "pressure_systems",
                        "artifact_type": "map",
                        "what_to_notice": "Regional pressure nodes.",
                        "lecture_connection": "Connects to crisis framing.",
                        "limit_or_caution": "Illustrative, not exhaustive.",
                        "curator_note": "Use as orientation.",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    bundle = build_ph_mus_packet_bundle(
        intent="lesson",
        title="GT-16 museum lesson",
        audience="Readers",
        packet_path=packet,
    )
    assert bundle["family"] == "ph-civ"
    assert bundle["subsurface"] == "ph-mus"
    assert bundle["artifact_class"] == "museum_route"
    assert bundle["policy"]["source_mode"] == "ph-mus-cli-packet"


def test_ph_mus_packet_bundle_rejects_missing_public_route_metadata(tmp_path: Path) -> None:
    packet = tmp_path / "ph-mus.json"
    packet.write_text(
        json.dumps(
            {
                "packet_type": "ph_mus_packet",
                "source_id": "gt-16",
                "museum_exhibit_path": "corpus/media-packs/gt-16.md",
                "visitor_path": ["entrance_artifact"],
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="public surface"):
        build_ph_mus_packet_bundle(
            intent="lesson",
            title="GT-16 museum lesson",
            audience="Readers",
            packet_path=packet,
        )


def test_ph_mus_packet_bundle_accepts_artifact_set_comparison(tmp_path: Path) -> None:
    packet = tmp_path / "ph-mus-artifact-set.json"
    packet.write_text(
        json.dumps(
            {
                "packet_type": "ph_mus_packet",
                "subsurface": "ph-mus",
                "artifact_class": "museum_artifact_set",
                "source_id": "gt-16",
                "title": "GT-16 runtime/artifacts",
                "surface": "ph-apo",
                "museum_status": "curated_draft",
                "museum_exhibit_path": "corpus/media-packs/gt-16.md",
                "route_type": "application",
                "what_changes_here": "Artifacts carry the comparison.",
                "caveat": "Public orientation only.",
                "conceptual_volumes": ["volume_ii"],
                "visitor_path": ["entrance_artifact", "pressure_systems"],
                "runtime/artifacts": [
                    {
                        "artifact_id": "gt16-map-1",
                        "title": "Map",
                        "room": "pressure_systems",
                        "artifact_type": "map",
                        "what_to_notice": "Regional pressure nodes.",
                        "lecture_connection": "Connects to crisis framing.",
                        "limit_or_caution": "Illustrative, not exhaustive.",
                        "curator_note": "Use as orientation.",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    bundle = build_ph_mus_packet_bundle(
        intent="comparison",
        title="GT-16 museum comparison",
        audience="Readers",
        packet_path=packet,
    )
    assert bundle["artifact_class"] == "museum_artifact_set"
    assert bundle["presentation_hints"]["section_order"][0] == "Comparison Frame"


def test_example_ph_mus_packet_builds_public_museum_bundle() -> None:
    bundle = build_ph_mus_packet_bundle(
        intent="lesson",
        title="GT-16 Museum Lesson",
        audience="Readers",
        packet_path=EXAMPLES_ROOT / "ph-mus-gt16.packet.json",
    )
    assert bundle["family"] == "ph-civ"
    assert bundle["subsurface"] == "ph-mus"
    assert bundle["artifact_class"] == "museum_route"
    assert bundle["policy"]["classification"] == "public"
    assert bundle["source_items"][0]["kind"] == "museum_route"
    assert any(item["kind"] == "museum_artifact" for item in bundle["source_items"])


def test_example_ce_mus_packet_builds_work_safe_museum_bundle() -> None:
    bundle = build_civ_emp_packet_bundle(
        intent="summary",
        title="Hormuz Exhibit Summary",
        audience="Operators",
        subsurface="ce-mus",
        packet_path=EXAMPLES_ROOT / "ce-mus-hormuz.packet.json",
    )
    assert bundle["family"] == "civ-emp"
    assert bundle["subsurface"] == "ce-mus"
    assert bundle["artifact_class"] == "strategic_exhibit"
    assert bundle["policy"]["classification"] == "work_public_safe"
    assert bundle["policy"]["source_mode"] == "strategy-codex-ce-mus-packet"
    assert len(bundle["source_items"]) >= 4


def test_example_museum_packets_expose_parallel_taxonomy() -> None:
    ph_bundle = build_ph_mus_packet_bundle(
        intent="lesson",
        title="GT-16 Museum Lesson",
        audience="Readers",
        packet_path=EXAMPLES_ROOT / "ph-mus-gt16.packet.json",
    )
    ce_bundle = build_civ_emp_packet_bundle(
        intent="summary",
        title="Hormuz Exhibit Summary",
        audience="Operators",
        subsurface="ce-mus",
        packet_path=EXAMPLES_ROOT / "ce-mus-hormuz.packet.json",
    )
    assert ph_bundle["family"] == "ph-civ"
    assert ph_bundle["subsurface"] == "ph-mus"
    assert ph_bundle["artifact_class"] == "museum_route"
    assert ce_bundle["family"] == "civ-emp"
    assert ce_bundle["subsurface"] == "ce-mus"
    assert ce_bundle["artifact_class"] == "strategic_exhibit"
