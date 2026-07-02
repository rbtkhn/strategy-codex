#!/usr/bin/env python3
"""Cross-object invariants for singularity loop definitions."""

from __future__ import annotations

from typing import Any

def run_singularity_loop_invariants(loops: list[dict[str, Any]]) -> list[str]:
    """Return human-readable violation lines for loaded loop registry rows."""
    issues: list[str] = []
    by_id: dict[str, dict[str, Any]] = {}

    for row in loops:
        loop_id = str(row.get("id") or "").strip()
        if not loop_id:
            issues.append(f"{row.get('source_file', '?')}: missing loop id")
            continue
        if loop_id in by_id:
            other = by_id[loop_id]["source_file"]
            issues.append(f"duplicate loop id `{loop_id}` in {row.get('source_file')} and {other}")
        by_id[loop_id] = row

    for row in loops:
        loop_id = str(row.get("id") or "").strip()
        for dep in row.get("dependencies") or []:
            dep_id = str(dep.get("loop_id") or "").strip()
            if not dep_id:
                issues.append(f"{loop_id}: dependency missing loop_id")
                continue
            if dep_id not in by_id:
                issues.append(f"{loop_id}: unknown dependency `{dep_id}`")

    for loop_id in by_id:
        if _has_cycle(loop_id, by_id, set()):
            issues.append(f"dependency cycle involving `{loop_id}`")

    return issues

def _has_cycle(
    loop_id: str,
    by_id: dict[str, dict[str, Any]],
    visiting: set[str],
) -> bool:
    if loop_id in visiting:
        return True
    row = by_id.get(loop_id)
    if not row:
        return False
    visiting.add(loop_id)
    for dep in row.get("dependencies") or []:
        dep_id = str(dep.get("loop_id") or "").strip()
        if dep_id and _has_cycle(dep_id, by_id, visiting):
            return True
    visiting.remove(loop_id)
    return False
