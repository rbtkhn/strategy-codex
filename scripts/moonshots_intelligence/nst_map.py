"""Optional NST mapping layer."""

from __future__ import annotations

from typing import Any

def apply_nst_mapping(document: dict[str, Any]) -> dict[str, Any]:
    mapping: list[dict[str, str]] = []
    for bullet in document.get("bullets") or []:
        mapping.append(
            {
                "evidence_ref": str(bullet.get("evidence_ref") or ""),
                "object_claim": str(bullet.get("claim") or ""),
                "morphism_mechanism": str(bullet.get("mechanism") or ""),
                "functor_implication": str(bullet.get("implication") or ""),
                "ground_anchor": str(bullet.get("evidence") or ""),
            }
        )
    out = dict(document)
    out["nst_mapping"] = mapping
    return out
