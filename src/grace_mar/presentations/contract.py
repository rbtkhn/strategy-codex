from __future__ import annotations

import hashlib
import json
from typing import Any

FAMILIES = ("ph-civ", "civ-emp")
SUBSURFACES_BY_FAMILY: dict[str, tuple[str, ...]] = {
    "ph-civ": ("ph-civ", "ph-apo", "ph-mus"),
    "civ-emp": ("ce-civ", "ce-emp", "ce-mus"),
}
SUBSURFACES = tuple(
    subsurface
    for members in SUBSURFACES_BY_FAMILY.values()
    for subsurface in members
)
INTENTS = ("briefing", "lesson", "summary", "roadmap", "comparison")
EXPORT_FORMATS = ("pptx", "web")

INTENT_SUBSURFACE_MAP: dict[str, tuple[str, ...]] = {
    "briefing": ("ce-civ", "ce-emp"),
    "lesson": ("ph-civ", "ph-apo", "ph-mus", "ce-civ", "ce-mus"),
    "summary": SUBSURFACES,
    "roadmap": ("ce-emp",),
    "comparison": SUBSURFACES,
}


class BundleValidationError(ValueError):
    """Raised when a presentation bundle violates the v1 contract."""


def canonical_bundle_json(bundle: dict[str, Any]) -> str:
    return json.dumps(bundle, ensure_ascii=True, indent=2, sort_keys=True)


def bundle_sha256(bundle: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_bundle_json(bundle).encode("utf-8")).hexdigest()


def _require_mapping(value: Any, field: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise BundleValidationError(f"{field} must be an object")
    return value


def _require_non_empty_string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise BundleValidationError(f"{field} must be a non-empty string")
    return value.strip()


def _require_list(value: Any, field: str) -> list[Any]:
    if not isinstance(value, list):
        raise BundleValidationError(f"{field} must be a list")
    return value


def validate_bundle(bundle: dict[str, Any]) -> dict[str, Any]:
    """Validate and normalize the shared presentation bundle contract."""
    if not isinstance(bundle, dict):
        raise BundleValidationError("bundle must be an object")

    family = _require_non_empty_string(bundle.get("family"), "family")
    if family not in FAMILIES:
        raise BundleValidationError(f"family must be one of {', '.join(FAMILIES)}")

    subsurface = _require_non_empty_string(bundle.get("subsurface"), "subsurface")
    if subsurface not in SUBSURFACES_BY_FAMILY[family]:
        allowed = ", ".join(SUBSURFACES_BY_FAMILY[family])
        raise BundleValidationError(
            f"subsurface {subsurface!r} is not allowed for family {family!r}; expected one of {allowed}"
        )

    intent = _require_non_empty_string(bundle.get("intent"), "intent")
    if intent not in INTENTS:
        raise BundleValidationError(f"intent must be one of {', '.join(INTENTS)}")
    if subsurface not in INTENT_SUBSURFACE_MAP[intent]:
        raise BundleValidationError(
            f"intent {intent!r} is not allowed for subsurface {subsurface!r}"
        )

    title = _require_non_empty_string(bundle.get("title"), "title")
    audience = _require_non_empty_string(bundle.get("audience"), "audience")

    source_items = _require_list(bundle.get("source_items"), "source_items")
    if not source_items:
        raise BundleValidationError("source_items must not be empty")

    normalized_items: list[dict[str, Any]] = []
    total_chars = 0
    for idx, item in enumerate(source_items):
        row = _require_mapping(item, f"source_items[{idx}]")
        item_id = _require_non_empty_string(row.get("id"), f"source_items[{idx}].id")
        item_title = _require_non_empty_string(row.get("title"), f"source_items[{idx}].title")
        text = _require_non_empty_string(row.get("text"), f"source_items[{idx}].text")
        citation = _require_non_empty_string(row.get("citation"), f"source_items[{idx}].citation")
        total_chars += len(text)
        normalized_items.append(
            {
                "id": item_id,
                "title": item_title,
                "text": text,
                "citation": citation,
                "kind": str(row.get("kind") or "section"),
                "source_path": str(row.get("source_path") or ""),
                "public": bool(row.get("public", False)),
            }
        )

    if total_chars > 80_000:
        raise BundleValidationError("content is over budget for v1 render service")

    policy = _require_mapping(bundle.get("policy"), "policy")
    classification = _require_non_empty_string(
        policy.get("classification"), "policy.classification"
    )
    if classification not in {"public", "work_public_safe"}:
        raise BundleValidationError(
            "policy.classification must be 'public' or 'work_public_safe'"
        )
    if not policy.get("approved_for_render", False):
        raise BundleValidationError("policy.approved_for_render must be true")
    allowed_outputs = [
        str(x).strip()
        for x in _require_list(policy.get("allowed_outputs"), "policy.allowed_outputs")
    ]
    if not allowed_outputs:
        raise BundleValidationError("policy.allowed_outputs must not be empty")
    invalid_outputs = [x for x in allowed_outputs if x not in EXPORT_FORMATS]
    if invalid_outputs:
        raise BundleValidationError(
            f"policy.allowed_outputs contains invalid values: {invalid_outputs}"
        )

    provenance = _require_mapping(bundle.get("provenance"), "provenance")
    normalized_provenance = {
        "source_repo": _require_non_empty_string(
            provenance.get("source_repo"), "provenance.source_repo"
        ),
        "source_ref": _require_non_empty_string(
            provenance.get("source_ref"), "provenance.source_ref"
        ),
        "bundle_created_at": _require_non_empty_string(
            provenance.get("bundle_created_at"), "provenance.bundle_created_at"
        ),
        "content_hashes": _require_mapping(
            provenance.get("content_hashes"), "provenance.content_hashes"
        ),
    }
    if not normalized_provenance["content_hashes"]:
        raise BundleValidationError("provenance.content_hashes must not be empty")

    hints = _require_mapping(bundle.get("presentation_hints"), "presentation_hints")
    section_order = [
        str(x).strip()
        for x in _require_list(
            hints.get("section_order"), "presentation_hints.section_order"
        )
    ]
    if not section_order:
        raise BundleValidationError(
            "presentation_hints.section_order must not be empty"
        )

    if family == "ph-civ":
        for row in normalized_items:
            if not row["public"]:
                raise BundleValidationError(
                    "ph-civ family source items must all be marked public=true"
                )

    return {
        "family": family,
        "subsurface": subsurface,
        "intent": intent,
        "title": title,
        "audience": audience,
        "source_items": normalized_items,
        "policy": {
            "classification": classification,
            "approved_for_render": True,
            "allowed_outputs": allowed_outputs,
            "source_mode": str(policy.get("source_mode") or ""),
        },
        "provenance": normalized_provenance,
        "presentation_hints": {
            "section_order": section_order,
            "chart_candidates": [str(x).strip() for x in hints.get("chart_candidates", [])],
            "visual_notes": [str(x).strip() for x in hints.get("visual_notes", [])],
            "template_key": str(hints.get("template_key") or ""),
        },
    }
