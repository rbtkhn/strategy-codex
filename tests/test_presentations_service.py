from __future__ import annotations

from pathlib import Path

from grace_mar.presentations.service import create_app

class _FakeClient:
    def generate_presentation(self, **_: object) -> dict[str, str]:
        return {
            "presentation_id": "presenton-123",
            "path": "/downloads/presenton-123.pptx",
            "edit_path": "/presentations/presenton-123/edit",
        }

def _bundle() -> dict:
    return {
        "bundle_type": "single_bundle",
        "family": "civ-emp",
        "subsurface": "ce-emp",
        "artifact_class": "statecraft_brief",
        "intent": "briefing",
        "title": "Hormuz Briefing",
        "audience": "Operators",
        "source_items": [
            {
                "id": "hormuz",
                "title": "Hormuz",
                "text": "Pattern text",
                "citation": "continuity/academy/statecraft/civ-emp/iran/hormuz-recognition-transit-restraint.md",
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
            "content_hashes": {"a": "b"},
        },
        "presentation_hints": {
            "section_order": ["Executive Summary", "Next Moves"],
            "chart_candidates": [],
            "visual_notes": [],
            "template_key": "ce-emp-briefing",
        },
    }

def test_service_render_and_lookup(tmp_path: Path) -> None:
    app = create_app(client=_FakeClient(), store_root=tmp_path)
    client = app.test_client()

    resp = client.post(
        "/v1/bundles/render",
        json={"bundle": _bundle(), "render_options": {"requested_outputs": ["pptx", "web"]}},
    )
    assert resp.status_code == 201
    payload = resp.get_json()
    assert payload["bundle_type"] == "single_bundle"
    assert payload["family"] == "civ-emp"
    assert payload["subsurface"] == "ce-emp"
    assert payload["artifact_class"] == "statecraft_brief"
    assert payload["outputs"]["pptx_path"].endswith(".pptx")
    assert payload["outputs"]["web_view_path"].endswith("/edit")

    lookup = client.get(f"/v1/presentations/{payload['id']}")
    assert lookup.status_code == 200
    assert lookup.get_json()["render_metadata"]["presenton_presentation_id"] == "presenton-123"

def test_service_rejects_disallowed_outputs(tmp_path: Path) -> None:
    app = create_app(client=_FakeClient(), store_root=tmp_path)
    client = app.test_client()
    resp = client.post(
        "/v1/bundles/render",
        json={"bundle": _bundle(), "render_options": {"requested_outputs": ["pdf"]}},
    )
    assert resp.status_code == 422
    assert "not allowed" in resp.get_json()["error"]

def test_service_rejects_unsupported_composite_bundle_type(tmp_path: Path) -> None:
    app = create_app(client=_FakeClient(), store_root=tmp_path)
    client = app.test_client()
    bundle = _bundle()
    bundle["bundle_type"] = "composite_comparison"
    resp = client.post(
        "/v1/bundles/render",
        json={"bundle": bundle, "render_options": {"requested_outputs": ["pptx", "web"]}},
    )
    assert resp.status_code == 422
    assert "single_bundle" in resp.get_json()["error"]
