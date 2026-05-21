from __future__ import annotations

import pytest

from grace_mar.presentations.contract import BundleValidationError, validate_bundle


def _base_bundle() -> dict:
    return {
        "family": "civ-emp",
        "subsurface": "ce-emp",
        "intent": "briefing",
        "title": "Hormuz Briefing",
        "audience": "Statecraft operators",
        "source_items": [
            {
                "id": "ce-emp:iran:hormuz",
                "title": "Hormuz Recognition Transit Restraint",
                "text": "Pattern text with transaction hooks.",
                "citation": "codex/academy/statecraft/civ-emp/iran/hormuz-recognition-transit-restraint.md",
                "kind": "markdown",
                "source_path": "codex/academy/statecraft/civ-emp/iran/hormuz-recognition-transit-restraint.md",
                "public": False,
            }
        ],
        "policy": {
            "classification": "work_public_safe",
            "approved_for_render": True,
            "allowed_outputs": ["pptx", "web"],
            "source_mode": "strategy-codex-civ-emp-adapter",
        },
        "provenance": {
            "source_repo": "strategy-codex",
            "source_ref": "abc123",
            "bundle_created_at": "2026-05-21T00:00:00+00:00",
            "content_hashes": {"x.md": "sha"},
        },
        "presentation_hints": {
            "section_order": ["Executive Summary", "Statecraft Use", "Next Moves"],
            "chart_candidates": [],
            "visual_notes": [],
            "template_key": "ce-emp-briefing",
        },
    }


def test_validate_bundle_accepts_valid_ce_emp() -> None:
    normalized = validate_bundle(_base_bundle())
    assert normalized["family"] == "civ-emp"
    assert normalized["subsurface"] == "ce-emp"
    assert normalized["intent"] == "briefing"


def test_validate_bundle_rejects_old_flat_surface_payload() -> None:
    bundle = _base_bundle()
    bundle["surface"] = "civ-emp"
    with pytest.raises(BundleValidationError, match="family"):
        validate_bundle({"surface": bundle["surface"]})


def test_validate_bundle_rejects_cross_family_subsurface() -> None:
    bundle = _base_bundle()
    bundle["subsurface"] = "ph-civ"
    with pytest.raises(BundleValidationError, match="not allowed for family"):
        validate_bundle(bundle)


def test_validate_bundle_rejects_subsurface_intent_mismatch() -> None:
    bundle = _base_bundle()
    bundle["intent"] = "lesson"
    with pytest.raises(BundleValidationError, match="not allowed"):
        validate_bundle(bundle)


def test_validate_bundle_rejects_missing_hashes() -> None:
    bundle = _base_bundle()
    bundle["provenance"]["content_hashes"] = {}
    with pytest.raises(BundleValidationError, match="content_hashes"):
        validate_bundle(bundle)


def test_validate_bundle_rejects_ph_family_non_public_items() -> None:
    bundle = _base_bundle()
    bundle["family"] = "ph-civ"
    bundle["subsurface"] = "ph-mus"
    bundle["intent"] = "lesson"
    bundle["policy"]["classification"] = "public"
    bundle["source_items"][0]["public"] = False
    with pytest.raises(BundleValidationError, match="public=true"):
        validate_bundle(bundle)


def test_validate_bundle_rejects_ph_family_non_public_classification() -> None:
    bundle = _base_bundle()
    bundle["family"] = "ph-civ"
    bundle["subsurface"] = "ph-civ"
    bundle["intent"] = "summary"
    bundle["policy"]["classification"] = "work_public_safe"
    bundle["source_items"][0]["public"] = True
    with pytest.raises(BundleValidationError, match="classification='public'"):
        validate_bundle(bundle)
