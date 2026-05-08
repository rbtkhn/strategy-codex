"""Runtime-only memory helpers for Strategy Codex workflows.

This module intentionally stays non-canonical: it builds operational payloads
for session continuity, retrieval feedback, and briefings, but it never claims
Record authority.

Boundary note:
- ``structured_memory.py`` is the OB1 bridge contract and session/capture
  router.
- This module is the Strategy Codex runtime-only payload layer.
- Both may render briefs and route captures, but only the bridge owns the OB1
  integration contract.
"""

from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any, Mapping, Sequence


RUNTIME_USE_CASES: tuple[dict[str, Any], ...] = (
    {
        "name": "session_start_briefing",
        "reads": [
            "session-log.md",
            "recursion-gate.md",
            "self-evidence.md",
            "docs/skill-work/work-dev/workspace.md",
            "docs/skill-work/work-dev/session-continuity-contract.md",
        ],
        "writes": ["sessions", "runtime_observations", "prepared_context_cache"],
    },
    {
        "name": "post_tool_context_capture",
        "reads": ["current tool result", "active lane docs", "immediately relevant repo files"],
        "writes": ["runtime_observations"],
    },
    {
        "name": "decision_capture",
        "reads": [
            "docs/skill-work/work-dev/agent-memory-pgvector-spec.md",
            "docs/integrations/ob1/structured-memory-mcp.md",
            "active work doc or lane README",
        ],
        "writes": ["runtime_observations"],
    },
    {
        "name": "retrieval_miss_logging",
        "reads": ["failed query", "active context", "searched docs/files"],
        "writes": ["retrieval_misses"],
    },
    {
        "name": "wrap_up_handoff",
        "reads": ["session-log.md", "recursion-gate.md", "self-evidence.md", "current session manifest"],
        "writes": ["sessions", "runtime_observations", "session_events"],
    },
)


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _read_text(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    return path.read_text(encoding="utf-8")


def _excerpt(text: str, *, limit: int = 18) -> str:
    lines = [line.rstrip() for line in text.splitlines() if line.strip()]
    if not lines:
        return ""
    excerpt = lines[:limit]
    if len(lines) > limit:
        excerpt.append("...")
    return "\n".join(excerpt)


def _fingerprint(content: str) -> str:
    return sha256(content.encode("utf-8")).hexdigest()


def _normalize_related_paths(paths: Sequence[str | Path] | None) -> list[str]:
    normalized: list[str] = []
    for item in paths or ():
        normalized.append(str(item).replace("\\", "/"))
    return normalized


def build_session_start_brief(
    repo_root: Path,
    *,
    instance_id: str = "grace-mar",
    lane: str = "work-dev",
    session_id: str = "",
    include_paths: Sequence[str | Path] | None = None,
) -> dict[str, Any]:
    """Build the session-start brief for the runtime layer.

    The default read set mirrors the repo's continuity contract and work-dev
    workspace entrypoint.
    """

    paths = [
        Path("session-log.md"),
        Path("recursion-gate.md"),
        Path("self-evidence.md"),
        Path("docs/skill-work/work-dev/workspace.md"),
        Path("docs/skill-work/work-dev/session-continuity-contract.md"),
    ]
    if include_paths:
        paths.extend(Path(p) for p in include_paths)

    sections: list[str] = []
    sources: list[dict[str, Any]] = []
    for rel in paths:
        abs_path = (repo_root / rel).resolve()
        text = _read_text(abs_path)
        sources.append(
            {
                "path": str(rel).replace("\\", "/"),
                "exists": bool(text),
                "excerpt": _excerpt(text),
            }
        )
        if text:
            sections.append(f"## {rel.as_posix()}")
            sections.append(_excerpt(text, limit=12))
            sections.append("")

    markdown = "\n".join(
        [
            "# Runtime Session Brief",
            "",
            f"- instance_id: {instance_id}",
            f"- lane: {lane}",
            f"- session_id: {session_id}",
            f"- generated_at: {_utc_now()}",
            "",
            *sections,
            "## Use",
            "- Start from the brief, then capture new runtime observations as the session evolves.",
            "- Keep Record changes on the Git + recursion-gate path.",
            "",
        ]
    ).rstrip() + "\n"

    return {
        "kind": "session_start_brief",
        "instance_id": instance_id,
        "lane": lane,
        "session_id": session_id,
        "generated_at": _utc_now(),
        "sources": sources,
        "markdown": markdown,
    }


def build_runtime_observation(
    content: str,
    *,
    instance_id: str,
    source: str,
    session_id: str = "",
    lane: str = "",
    metadata: Mapping[str, Any] | None = None,
    related_record_path: str = "",
    observation_type: str = "observation",
    fingerprint: str | None = None,
) -> dict[str, Any]:
    """Normalize one runtime observation for the runtime_observations table."""

    payload = {
        "instance_id": instance_id,
        "source": source,
        "content": content.strip(),
        "fingerprint": fingerprint or _fingerprint(content.strip()),
        "metadata": dict(metadata or {}),
        "created_at": _utc_now(),
        "session_id": session_id,
        "lane": lane,
        "related_record_path": related_record_path,
        "observation_type": observation_type,
    }
    return payload


def capture_tool_use(
    content: str,
    *,
    instance_id: str,
    session_id: str,
    lane: str = "",
    metadata: Mapping[str, Any] | None = None,
    related_record_path: str = "",
) -> dict[str, Any]:
    return build_runtime_observation(
        content,
        instance_id=instance_id,
        source="tool_use",
        session_id=session_id,
        lane=lane,
        metadata=metadata,
        related_record_path=related_record_path,
        observation_type="tool_use",
    )


def capture_observation(
    content: str,
    *,
    instance_id: str,
    session_id: str,
    lane: str = "",
    metadata: Mapping[str, Any] | None = None,
    related_record_path: str = "",
) -> dict[str, Any]:
    return build_runtime_observation(
        content,
        instance_id=instance_id,
        source="observation",
        session_id=session_id,
        lane=lane,
        metadata=metadata,
        related_record_path=related_record_path,
        observation_type="observation",
    )


def capture_decision(
    content: str,
    *,
    instance_id: str,
    session_id: str,
    lane: str = "",
    metadata: Mapping[str, Any] | None = None,
    related_record_path: str = "",
) -> dict[str, Any]:
    return build_runtime_observation(
        content,
        instance_id=instance_id,
        source="decision",
        session_id=session_id,
        lane=lane,
        metadata=metadata,
        related_record_path=related_record_path,
        observation_type="decision",
    )


def capture_brag(
    content: str,
    *,
    instance_id: str,
    session_id: str,
    lane: str = "",
    metadata: Mapping[str, Any] | None = None,
    related_record_path: str = "",
) -> dict[str, Any]:
    return build_runtime_observation(
        content,
        instance_id=instance_id,
        source="brag",
        session_id=session_id,
        lane=lane,
        metadata=metadata,
        related_record_path=related_record_path,
        observation_type="brag",
    )


def log_retrieval_miss(
    query: str,
    *,
    instance_id: str,
    surface: str,
    failure_class: str,
    session_id: str = "",
    lane_or_context: str = "",
    expected_target: str = "",
    notes: str = "",
    related_paths: Sequence[str | Path] | None = None,
    recorded_by: str = "operator",
    suggested_improvement: str = "",
) -> dict[str, Any]:
    return {
        "instance_id": instance_id,
        "query": query,
        "retrieval_surface": surface,
        "failure_class": failure_class,
        "session_id": session_id,
        "lane_or_context": lane_or_context,
        "expected_target": expected_target,
        "notes": notes,
        "related_paths": _normalize_related_paths(related_paths),
        "recorded_by": recorded_by,
        "suggested_improvement": suggested_improvement,
        "timestamp": _utc_now(),
    }


def build_sync_receipt(
    git_commit_sha: str,
    *,
    instance_id: str,
    surfaces: Sequence[str | Path],
    status: str = "success",
    notes: str = "",
) -> dict[str, Any]:
    return {
        "instance_id": instance_id,
        "git_commit_sha": git_commit_sha,
        "synced_at": _utc_now(),
        "surfaces": [str(surface).replace("\\", "/") for surface in surfaces],
        "status": status,
        "notes": notes,
    }


def build_wrap_up_session(
    *,
    instance_id: str,
    session_id: str,
    lane: str = "",
    status: str = "ended",
    summary: str = "",
    open_loops: Sequence[str] | None = None,
    next_entrypoint: str = "",
) -> dict[str, Any]:
    return {
        "instance_id": instance_id,
        "session_id": session_id,
        "lane": lane,
        "status": status,
        "summary": summary,
        "open_loops": list(open_loops or ()),
        "next_entrypoint": next_entrypoint,
        "ended_at": _utc_now(),
    }
