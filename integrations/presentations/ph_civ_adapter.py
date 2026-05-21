from __future__ import annotations

import json
from pathlib import Path

from grace_mar.presentations.contract import bundle_sha256

from .common import REPO_ROOT, current_git_ref, file_sha256, markdown_excerpt, utc_now_iso

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


def _forbidden_local_ph_path(path: Path) -> bool:
    resolved = path.resolve()
    for root in FORBIDDEN_PH_ROOTS:
        try:
            resolved.relative_to(root.resolve())
        except ValueError:
            continue
        return True
    return False


def _base_bundle(
    *,
    subsurface: str,
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
            "section_order": DEFAULT_SECTION_ORDERS[subsurface],
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
        raise ValueError("ph-civ adapter requires at least one explicit public source path")
    public_ids = [x.strip() for x in (public_ids or []) if x.strip()]
    items = []
    hashes: dict[str, str] = {}
    for path in source_paths:
        resolved = path.resolve()
        if _forbidden_local_ph_path(resolved):
            raise ValueError(f"{path} is forbidden local Predictive History residue")
        rel = resolved.as_posix()
        hashes[rel] = file_sha256(resolved)
        label = path.stem.replace("-", " ")
        if public_ids:
            label = f"{label} ({', '.join(public_ids)})"
        items.append(
            {
                "id": rel,
                "title": label,
                "text": markdown_excerpt(resolved),
                "citation": rel,
                "kind": "public_packet",
                "source_path": rel,
                "public": True,
            }
        )
    return _base_bundle(
        subsurface=subsurface,
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
    packet = json.loads(resolved.read_text(encoding="utf-8"))
    packet_blob = json.dumps(packet, ensure_ascii=True, sort_keys=True)
    for marker in PH_MUS_PRIVATE_MARKERS:
        if marker in packet_blob:
            raise ValueError(f"ph-mus packet contains forbidden private marker: {marker}")
    if str(packet.get("packet_type") or "") != "ph_mus_packet":
        raise ValueError("ph-mus packet must use packet_type=ph_mus_packet")
    source_id = str(packet.get("source_id") or "").strip()
    if not source_id:
        raise ValueError("ph-mus packet must include source_id")
    exhibit_path = str(packet.get("museum_exhibit_path") or "").strip()
    if not exhibit_path:
        raise ValueError("ph-mus packet must include museum_exhibit_path")
    visitor_path = packet.get("visitor_path") or []
    if not isinstance(visitor_path, list) or not visitor_path:
        raise ValueError("ph-mus packet must include visitor_path")
    items = [
        {
            "id": source_id,
            "title": str(packet.get("title") or source_id),
            "text": "\n".join(
                [
                    f"museum_status: {str(packet.get('museum_status') or '')}",
                    f"route_type: {str(packet.get('route_type') or '')}",
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
    for idx, artifact in enumerate(packet.get("artifacts") or []):
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
        intent=intent,
        title=title,
        audience=audience,
        items=items,
        hashes=hashes,
        source_mode="ph-mus-cli-packet",
    )
