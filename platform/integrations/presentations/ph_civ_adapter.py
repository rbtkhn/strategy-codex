from __future__ import annotations

import json
import re
from pathlib import Path

from grace_mar.presentations.contract import bundle_sha256
from grace_mar.presentations.intents import default_sections_for

from .common import REPO_ROOT, current_git_ref, file_sha256, utc_now_iso

FORBIDDEN_PH_ROOTS = [
    REPO_ROOT / "codex" / "predictive-history",
    REPO_ROOT / "research" / "external" / "youtube-channels" / "predictive-history",
]
PH_MUS_PRIVATE_MARKERS = (
    "local_vault_path",
    "shared_cloud_path",
    "C:\\",
    "C:/",
)
PH_PUBLIC_PACKET_PRIVATE_MARKERS = (
    "local_vault_path",
    "shared_cloud_path",
    "recursion-gate",
    "self-memory",
    "session-log",
    "C:\\",
    "C:/",
)
SOURCE_ID_RE = re.compile(r"^[a-z]+-[0-9]{2,3}$")
DEFAULT_SECTION_ORDERS = {
    "ph-civ": [
        "Opening Thesis",
        "Reader Orientation",
        "Pattern",
        "Evidence",
        "Study Questions",
    ],
    "ph-apo": [
        "Crisis Frame",
        "Pressure System",
        "Evidence",
        "Caveats",
        "Implications",
    ],
    "ph-mus": [
        "Museum Orientation",
        "Visitor Path",
        "Key Artifacts",
        "What To Notice",
        "Cautions",
    ],
}
PH_MUS_ARTIFACT_CLASSES = {"museum_route", "museum_artifact_set"}


def _forbidden_local_ph_path(path: Path) -> bool:
    resolved = path.resolve()
    for root in FORBIDDEN_PH_ROOTS:
        try:
            resolved.relative_to(root.resolve())
        except ValueError:
            continue
        return True
    return False


def _require_source_id(source_id: object, *, field: str) -> str:
    value = str(source_id or "").strip()
    if not value:
        raise ValueError(f"{field} must include source_id")
    if not SOURCE_ID_RE.match(value):
        raise ValueError(f"{field} must use a public ph-civ style source_id")
    return value


def _base_bundle(
    *,
    subsurface: str,
    artifact_class: str,
    intent: str,
    title: str,
    audience: str,
    items: list[dict[str, object]],
    hashes: dict[str, str],
    source_mode: str,
) -> dict[str, object]:
    bundle: dict[str, object] = {
        "family": "ph-civ",
        "subsurface": subsurface,
        "artifact_class": artifact_class,
        "intent": intent,
        "title": title,
        "audience": audience,
        "source_items": items,
        "policy": {
            "classification": "public",
            "approved_for_render": True,
            "allowed_outputs": ["pptx", "web"],
            "source_mode": source_mode,
        },
        "provenance": {
            "source_repo": "strategy-codex-review-packet",
            "source_ref": current_git_ref(),
            "bundle_created_at": utc_now_iso(),
            "content_hashes": hashes,
        },
        "presentation_hints": {
            "section_order": default_sections_for(subsurface, intent, artifact_class),
            "chart_candidates": ["Visitor path" if subsurface == "ph-mus" else "Pattern flow"],
            "visual_notes": ["Reader-facing public style", "Keep citations and ids visible"],
            "template_key": "",
        },
    }
    bundle["provenance"]["bundle_sha256"] = bundle_sha256(bundle)
    return bundle


def build_ph_civ_bundle(
    *,
    intent: str,
    title: str,
    audience: str,
    source_paths: list[Path],
    public_ids: list[str] | None = None,
    subsurface: str = "ph-civ",
) -> dict[str, object]:
    if not source_paths:
        raise ValueError("ph-civ adapter requires at least one explicit public packet path")
    public_ids = [x.strip() for x in (public_ids or []) if x.strip()]
    items: list[dict[str, object]] = []
    hashes: dict[str, str] = {}
    for path in source_paths:
        resolved = path.resolve()
        if _forbidden_local_ph_path(resolved):
            raise ValueError(f"{path} is forbidden local Predictive History residue")
        try:
            packet = json.loads(resolved.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError("ph public packet must be valid JSON") from exc
        packet_blob = json.dumps(packet, ensure_ascii=True, sort_keys=True)
        for marker in PH_PUBLIC_PACKET_PRIVATE_MARKERS:
            if marker in packet_blob:
                raise ValueError(f"ph public packet contains forbidden private marker: {marker}")
        if str(packet.get("packet_type") or "") != "ph_public_packet":
            raise ValueError("ph public packet must use packet_type=ph_public_packet")
        packet_subsurface = str(packet.get("subsurface") or "").strip()
        if packet_subsurface != subsurface:
            raise ValueError(
                f"ph public packet subsurface {packet_subsurface!r} does not match requested subsurface {subsurface!r}"
            )
        if packet_subsurface not in {"ph-civ", "ph-apo"}:
            raise ValueError("ph public packet subsurface must be 'ph-civ' or 'ph-apo'")
        if packet.get("public") is not True:
            raise ValueError("ph public packet must set public=true")
        packet_source_id = _require_source_id(packet.get("source_id"), field="ph public packet")
        source_rows = packet.get("source_items")
        if not isinstance(source_rows, list) or not source_rows:
            raise ValueError("ph public packet must include non-empty source_items")
        rel = resolved.as_posix()
        hashes[rel] = file_sha256(resolved)
        packet_title = str(packet.get("title") or packet_source_id).strip()
        for idx, row in enumerate(source_rows):
            if not isinstance(row, dict):
                raise ValueError(f"ph public packet source_items[{idx}] must be an object")
            item_text = str(row.get("text") or "").strip()
            if not item_text:
                raise ValueError(f"ph public packet source_items[{idx}] must include text")
            item_citation = str(row.get("citation") or "").strip()
            if not item_citation:
                raise ValueError(f"ph public packet source_items[{idx}] must include citation")
            item_id = str(row.get("id") or f"{packet_source_id}:{idx+1}").strip()
            item_title = str(row.get("title") or packet_title).strip()
            if public_ids:
                item_title = f"{item_title} ({', '.join(public_ids)})"
            items.append(
                {
                    "id": item_id,
                    "title": item_title,
                    "text": item_text,
                    "citation": item_citation,
                    "kind": str(row.get("kind") or "public_packet"),
                    "source_path": str(row.get("source_path") or rel),
                    "public": True,
                }
            )
    artifact_class = "route_comparison" if intent == "comparison" else "chapter_packet"
    return _base_bundle(
        subsurface=subsurface,
        artifact_class=artifact_class,
        intent=intent,
        title=title,
        audience=audience,
        items=items,
        hashes=hashes,
        source_mode="external-public-packet",
    )


def build_ph_mus_packet_bundle(
    *,
    intent: str,
    title: str,
    audience: str,
    packet_path: Path,
) -> dict[str, object]:
    resolved = packet_path.resolve()
    try:
        packet = json.loads(resolved.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError("ph-mus packet must be valid JSON") from exc
    packet_blob = json.dumps(packet, ensure_ascii=True, sort_keys=True)
    for marker in PH_MUS_PRIVATE_MARKERS:
        if marker in packet_blob:
            raise ValueError(f"ph-mus packet contains forbidden private marker: {marker}")
    if str(packet.get("packet_type") or "") != "ph_mus_packet":
        raise ValueError("ph-mus packet must use packet_type=ph_mus_packet")
    source_id = _require_source_id(packet.get("source_id"), field="ph-mus packet")
    packet_subsurface = str(packet.get("subsurface") or "").strip()
    if packet_subsurface and packet_subsurface != "ph-mus":
        raise ValueError("ph-mus packet subsurface must be 'ph-mus'")
    surface = str(packet.get("surface") or "").strip()
    if surface not in {"ph-civ", "ph-apo"}:
        raise ValueError("ph-mus packet must include public surface 'ph-civ' or 'ph-apo'")
    conceptual_volumes = packet.get("conceptual_volumes") or []
    if not isinstance(conceptual_volumes, list) or not conceptual_volumes:
        raise ValueError("ph-mus packet must include non-empty conceptual_volumes")
    if not all(isinstance(x, str) and x.strip() for x in conceptual_volumes):
        raise ValueError("ph-mus packet conceptual_volumes must be strings")
    exhibit_path = str(packet.get("museum_exhibit_path") or "").strip()
    if not exhibit_path:
        raise ValueError("ph-mus packet must include museum_exhibit_path")
    if not exhibit_path.startswith("corpus/media-packs/"):
        raise ValueError("ph-mus packet museum_exhibit_path must point to the public museum corpus")
    museum_status = str(packet.get("museum_status") or "").strip()
    if not museum_status:
        raise ValueError("ph-mus packet must include museum_status")
    route_type = str(packet.get("route_type") or "").strip()
    if not route_type:
        raise ValueError("ph-mus packet must include route_type")
    visitor_path = packet.get("visitor_path") or []
    if not isinstance(visitor_path, list) or not visitor_path:
        raise ValueError("ph-mus packet must include visitor_path")
    artifact_class = str(packet.get("artifact_class") or "").strip()
    if artifact_class:
        if artifact_class not in PH_MUS_ARTIFACT_CLASSES:
            raise ValueError("ph-mus packet artifact_class must be museum_route or museum_artifact_set")
    elif intent == "comparison" and packet.get("runtime/artifacts"):
        artifact_class = "museum_artifact_set"
    else:
        artifact_class = "museum_route"
    items = [
        {
            "id": source_id,
            "title": str(packet.get("title") or source_id),
            "text": "\n".join(
                [
                    f"surface: {surface}",
                    f"conceptual_volumes: {', '.join(str(x).strip() for x in conceptual_volumes)}",
                    f"museum_status: {museum_status}",
                    f"route_type: {route_type}",
                    f"what_changes_here: {str(packet.get('what_changes_here') or '')}",
                    f"caveat: {str(packet.get('caveat') or '')}",
                    "visitor_path:",
                    *[f"- {room}" for room in visitor_path],
                ]
            ).strip(),
            "citation": exhibit_path,
            "kind": "museum_route",
            "source_path": exhibit_path,
            "public": True,
        }
    ]
    for idx, artifact in enumerate(packet.get("runtime/artifacts") or []):
        if not isinstance(artifact, dict):
            raise ValueError(f"ph-mus artifacts[{idx}] must be an object")
        items.append(
            {
                "id": str(artifact.get("artifact_id") or f"{source_id}-artifact-{idx+1}"),
                "title": str(artifact.get("title") or f"{source_id} artifact {idx+1}"),
                "text": "\n".join(
                    [
                        f"room: {str(artifact.get('room') or '')}",
                        f"artifact_type: {str(artifact.get('artifact_type') or '')}",
                        f"what_to_notice: {str(artifact.get('what_to_notice') or '')}",
                        f"lecture_connection: {str(artifact.get('lecture_connection') or '')}",
                        f"limit_or_caution: {str(artifact.get('limit_or_caution') or '')}",
                        f"curator_note: {str(artifact.get('curator_note') or '')}",
                    ]
                ).strip(),
                "citation": exhibit_path,
                "kind": "museum_artifact",
                "source_path": exhibit_path,
                "public": True,
            }
        )
    hashes = {resolved.as_posix(): file_sha256(resolved)}
    return _base_bundle(
        subsurface="ph-mus",
        artifact_class=artifact_class,
        intent=intent,
        title=title,
        audience=audience,
        items=items,
        hashes=hashes,
        source_mode="ph-mus-cli-packet",
    )
