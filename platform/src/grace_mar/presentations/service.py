from __future__ import annotations

import json
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, request

from grace_mar.repo_io import repo_root

from .contract import BundleValidationError, bundle_sha256, validate_bundle
from .intents import INTENT_REGISTRY, build_presenton_markdown, get_template_key, list_intents, list_templates
from .presenton_client import PresentonClient


def _presentation_store_root(config_root: Path | None = None) -> Path:
    return (config_root or (repo_root() / "runtime/artifacts" / "presentations")).resolve()


def _manifest_path(root: Path) -> Path:
    return root / "manifest.jsonl"


def _record_path(root: Path, presentation_id: str) -> Path:
    return root / "records" / f"{presentation_id}.json"


def _append_manifest(root: Path, row: dict[str, Any]) -> None:
    root.mkdir(parents=True, exist_ok=True)
    manifest = _manifest_path(root)
    with manifest.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n")


def _write_record(root: Path, row: dict[str, Any]) -> None:
    path = _record_path(root, row["id"])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(row, ensure_ascii=True, indent=2, sort_keys=True), encoding="utf-8")


def _read_record(root: Path, presentation_id: str) -> dict[str, Any] | None:
    path = _record_path(root, presentation_id)
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def create_app(
    *,
    client: PresentonClient | None = None,
    store_root: Path | None = None,
) -> Flask:
    app = Flask(__name__)
    presenton = client or PresentonClient()
    root = _presentation_store_root(store_root)

    @app.get("/v1/intents")
    def intents_index():
        return jsonify({"intents": list_intents()})

    @app.get("/v1/templates")
    def templates_index():
        return jsonify({"templates": list_templates()})

    @app.get("/v1/presentations/<presentation_id>")
    def presentation_status(presentation_id: str):
        row = _read_record(root, presentation_id)
        if row is None:
            return jsonify({"ok": False, "error": "presentation not found"}), 404
        return jsonify(row)

    @app.post("/v1/bundles/render")
    def render_bundle():
        payload = request.get_json(silent=True) or {}
        try:
            bundle = validate_bundle(payload.get("bundle"))
        except BundleValidationError as exc:
            return jsonify({"ok": False, "error": str(exc)}), 422

        render_options = payload.get("render_options") or {}
        if not isinstance(render_options, dict):
            return jsonify({"ok": False, "error": "render_options must be an object"}), 422

        requested_outputs = render_options.get("requested_outputs") or ["pptx", "web"]
        if not isinstance(requested_outputs, list) or not requested_outputs:
            return jsonify({"ok": False, "error": "requested_outputs must be a non-empty list"}), 422
        allowed_outputs = set(bundle["policy"]["allowed_outputs"])
        missing = [item for item in requested_outputs if item not in allowed_outputs]
        if missing:
            return jsonify({"ok": False, "error": f"requested outputs not allowed: {missing}"}), 422

        template = str(
            render_options.get("template")
            or bundle["presentation_hints"]["template_key"]
            or get_template_key(
                bundle["family"],
                bundle["subsurface"],
                bundle["intent"],
                str(bundle.get("artifact_class") or ""),
            )
        )
        language = str(render_options.get("language") or "English")
        n_slides = int(render_options.get("n_slides") or INTENT_REGISTRY[bundle["intent"]]["n_slides"])
        content = build_presenton_markdown(bundle)
        bundle_hash = bundle_sha256(bundle)
        presenton_resp = presenton.generate_presentation(
            content=content,
            template=template,
            n_slides=n_slides,
            language=language,
            export_as="pptx",
        )

        now = datetime.now(UTC).isoformat()
        service_id = f"deck-{uuid.uuid4().hex[:12]}"
        row = {
            "ok": True,
            "id": service_id,
            "status": "rendered",
            "bundle_type": bundle.get("bundle_type") or "single_bundle",
            "family": bundle["family"],
            "subsurface": bundle["subsurface"],
            "artifact_class": bundle.get("artifact_class") or "",
            "intent": bundle["intent"],
            "title": bundle["title"],
            "audience": bundle["audience"],
            "template": template,
            "requested_outputs": requested_outputs,
            "bundle_sha256": bundle_hash,
            "rendered_at": now,
            "provenance": bundle["provenance"],
            "render_metadata": {
                "n_slides": n_slides,
                "language": language,
                "presenton_presentation_id": presenton_resp["presentation_id"],
            },
            "outputs": {
                "pptx_path": presenton_resp["path"],
                "web_view_path": presenton_resp["edit_path"],
            },
            "diagnostics": {
                "source_item_count": len(bundle["source_items"]),
                "policy_classification": bundle["policy"]["classification"],
                "source_mode": bundle["policy"]["source_mode"],
            },
        }
        _write_record(root, row)
        _append_manifest(
            root,
            {
                "id": service_id,
                "rendered_at": now,
                "bundle_type": bundle.get("bundle_type") or "single_bundle",
                "family": bundle["family"],
                "subsurface": bundle["subsurface"],
                "artifact_class": bundle.get("artifact_class") or "",
                "intent": bundle["intent"],
                "title": bundle["title"],
                "bundle_sha256": bundle_hash,
                "presenton_presentation_id": presenton_resp["presentation_id"],
            },
        )
        return jsonify(row), 201

    return app
