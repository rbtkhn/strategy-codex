from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from grace_mar.presentations.contract import bundle_sha256
from grace_mar.presentations.intents import default_sections_for

from .common import REPO_ROOT, current_git_ref, file_sha256, markdown_excerpt, utc_now_iso

CIV_EMP_ROOT = REPO_ROOT / "codex" / "academy" / "statecraft" / "civ-emp"
DEFAULT_SOURCES_BY_SUBSURFACE = {
    "ce-civ": [
        CIV_EMP_ROOT / "README.md",
        CIV_EMP_ROOT / "indexes" / "source-retrieval-matrix.md",
    ],
    "ce-emp": [
        CIV_EMP_ROOT / "README.md",
        CIV_EMP_ROOT / "indexes" / "source-retrieval-matrix.md",
        CIV_EMP_ROOT / "iran" / "hormuz-recognition-transit-restraint.md",
    ],
}
DEFAULT_SECTION_ORDERS = {
    "ce-civ": [
        "Civilization Frame",
        "Institutional Pattern",
        "Evidence",
        "Application",
    ],
    "ce-emp": [
        "Executive Summary",
        "Statecraft Use",
        "Counterweights",
        "Decision Points",
        "Next Moves",
    ],
    "ce-mus": [
        "Exhibit Frame",
        "Object Sequence",
        "Interpretation",
        "Operational Relevance",
        "Cautions",
    ],
}
PACKET_TYPE_BY_SUBSURFACE = {
    "ce-civ": {"ce_civ_packet": "civilization_pattern_packet"},
    "ce-emp": {
        "ce_emp_packet": "statecraft_brief",
        "ce_emp_decision_comparison_packet": "decision_comparison",
    },
    "ce-mus": {"ce_mus_packet": "strategic_exhibit"},
}

def _ensure_under_civ_emp(path: Path) -> Path:
    resolved = path.resolve()
    try:
        resolved.relative_to(CIV_EMP_ROOT.resolve())
    except ValueError as exc:
        raise ValueError(f"{path} is not under {CIV_EMP_ROOT}") from exc
    return resolved

def _base_bundle(
    *,
    subsurface: str,
    artifact_class: str,
    intent: str,
    title: str,
    audience: str,
    items: list[dict[str, Any]],
    hashes: dict[str, str],
    source_mode: str,
) -> dict[str, Any]:
    bundle: dict[str, Any] = {
        "family": "civ-emp",
        "subsurface": subsurface,
        "artifact_class": artifact_class,
        "intent": intent,
        "title": title,
        "audience": audience,
        "source_items": items,
        "policy": {
            "classification": "work_public_safe",
            "approved_for_render": True,
            "allowed_outputs": ["pptx", "web"],
            "source_mode": source_mode,
        },
        "provenance": {
            "source_repo": "strategy-codex",
            "source_ref": current_git_ref(),
            "bundle_created_at": utc_now_iso(),
            "content_hashes": hashes,
        },
        "presentation_hints": {
            "section_order": default_sections_for(subsurface, intent, artifact_class),
            "chart_candidates": ["Object map" if subsurface == "ce-mus" else "Counterweight coverage"],
            "visual_notes": [
                "Neutral strategy visual style",
                "Prefer maps, matrices, and simple timelines",
            ],
            "template_key": "",
        },
    }
    bundle["provenance"]["bundle_sha256"] = bundle_sha256(bundle)
    return bundle

def build_civ_emp_bundle(
    *,
    intent: str,
    title: str,
    audience: str,
    subsurface: str = "ce-emp",
    source_paths: list[Path] | None = None,
) -> dict[str, Any]:
    if subsurface == "ce-mus":
        raise ValueError("ce-mus bundles require packet_json input")
    selected = [
        _ensure_under_civ_emp(path)
        for path in (source_paths or DEFAULT_SOURCES_BY_SUBSURFACE[subsurface])
    ]
    items: list[dict[str, Any]] = []
    hashes: dict[str, str] = {}
    for path in selected:
        rel = path.relative_to(REPO_ROOT).as_posix()
        hashes[rel] = file_sha256(path)
        items.append(
            {
                "id": rel.replace("/", ":"),
                "title": path.stem.replace("-", " "),
                "text": markdown_excerpt(path),
                "citation": rel,
                "kind": "markdown",
                "source_path": rel,
                "public": False,
            }
        )
    artifact_class = "civilization_pattern_packet"
    if subsurface == "ce-emp":
        artifact_class = "decision_comparison" if intent == "comparison" else "statecraft_brief"
    return _base_bundle(
        subsurface=subsurface,
        artifact_class=artifact_class,
        intent=intent,
        title=title,
        audience=audience,
        items=items,
        hashes=hashes,
        source_mode="strategy-codex-civ-emp-adapter",
    )

def build_civ_emp_packet_bundle(
    *,
    intent: str,
    title: str,
    audience: str,
    subsurface: str,
    packet_path: Path,
) -> dict[str, Any]:
    resolved = packet_path.resolve()
    packet = json.loads(resolved.read_text(encoding="utf-8"))
    packet_type = str(packet.get("packet_type") or "")
    allowed_packet_types = PACKET_TYPE_BY_SUBSURFACE[subsurface]
    if packet_type not in allowed_packet_types:
        allowed = ", ".join(sorted(allowed_packet_types))
        raise ValueError(f"{subsurface} packet must use one of: {allowed}")
    packet_subsurface = str(packet.get("subsurface") or "").strip()
    if packet_subsurface and packet_subsurface != subsurface:
        raise ValueError(
            f"packet subsurface {packet_subsurface!r} does not match requested subsurface {subsurface!r}"
        )
    source_id = str(packet.get("source_id") or "").strip()
    if not source_id:
        raise ValueError("packet must include source_id")
    artifact_class = str(packet.get("artifact_class") or "").strip()
    inferred_artifact_class = allowed_packet_types[packet_type]
    if artifact_class and artifact_class != inferred_artifact_class:
        raise ValueError(
            f"packet artifact_class {artifact_class!r} does not match packet_type {packet_type!r}"
        )
    artifact_class = artifact_class or inferred_artifact_class
    sections = packet.get("source_items")
    if not isinstance(sections, list) or not sections:
        raise ValueError("packet must include non-empty source_items")
    items: list[dict[str, Any]] = []
    for idx, row in enumerate(sections):
        if not isinstance(row, dict):
            raise ValueError(f"packet source_items[{idx}] must be an object")
        item_id = str(row.get("id") or f"{source_id}:{idx+1}").strip()
        item_title = str(row.get("title") or f"{source_id} item {idx+1}").strip()
        item_text = str(row.get("text") or "").strip()
        item_citation = str(row.get("citation") or f"packet:{source_id}:{idx+1}").strip()
        if not item_text:
            raise ValueError(f"packet source_items[{idx}] must include text")
        items.append(
            {
                "id": item_id,
                "title": item_title,
                "text": item_text,
                "citation": item_citation,
                "kind": str(row.get("kind") or "packet"),
                "source_path": str(row.get("source_path") or resolved.as_posix()),
                "public": False,
            }
        )
    hashes = {resolved.as_posix(): file_sha256(resolved)}
    return _base_bundle(
        subsurface=subsurface,
        artifact_class=artifact_class,
        intent=intent,
        title=title,
        audience=audience,
        items=items,
        hashes=hashes,
        source_mode=f"strategy-codex-{subsurface}-packet",
    )
