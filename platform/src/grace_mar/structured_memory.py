"""Structured memory helpers for the OB1 MCP bridge.

This module keeps the repo-local contract thin:
- session lifecycle delegates to the existing Grace-Mar fork lifecycle helpers
- capture routing stays hybrid and backward compatible
- briefing rendering is data-driven so the live Supabase bridge can reuse it

The live Supabase implementation is modeled in ``research/bridges/supabase``; this module
provides the local routing and composition logic that the live edge function and
repo-side tests can share.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

from grace_mar import fork_lifecycle

STRUCTURED_SURFACES: tuple[str, ...] = (
    "north_star",
    "active_projects",
    "decisions",
    "brags",
    "thinking",
)

SESSION_EVENT_TYPES: tuple[str, ...] = (
    "session_start",
    "prompt_submit",
    "post_tool_use",
    "wrap_up",
    "session_end",
)

SURFACE_ALIASES: dict[str, str] = {
    "governed_state": "decisions",
    "prepared_context": "thinking",
    "archive/placeholders/evidence": "thinking",
    "goal": "north_star",
    "goals": "north_star",
    "north star": "north_star",
    "north_star": "north_star",
    "objective": "north_star",
    "objectives": "north_star",
    "mission": "north_star",
    "vision": "north_star",
    "priority": "north_star",
    "priorities": "north_star",
    "project": "active_projects",
    "projects": "active_projects",
    "active_project": "active_projects",
    "active_projects": "active_projects",
    "initiative": "active_projects",
    "initiatives": "active_projects",
    "roadmap": "active_projects",
    "blocker": "active_projects",
    "blockers": "active_projects",
    "next step": "active_projects",
    "next steps": "active_projects",
    "decision": "decisions",
    "decisions": "decisions",
    "decided": "decisions",
    "chose": "decisions",
    "tradeoff": "decisions",
    "tradeoffs": "decisions",
    "resolved": "decisions",
    "brag": "brags",
    "brags": "brags",
    "win": "brags",
    "wins": "brags",
    "success": "brags",
    "shipped": "brags",
    "delivered": "brags",
    "accomplished": "brags",
    "thinking": "thinking",
    "thought": "thinking",
    "thoughts": "thinking",
    "note": "thinking",
    "notes": "thinking",
    "idea": "thinking",
    "ideas": "thinking",
}

_SURFACE_KEYWORDS: dict[str, tuple[str, ...]] = {
    "north_star": (
        "north star",
        "goal",
        "goals",
        "objective",
        "objectives",
        "mission",
        "vision",
        "priority",
        "priorities",
        "aim",
        "purpose",
    ),
    "active_projects": (
        "project",
        "projects",
        "initiative",
        "initiatives",
        "roadmap",
        "blocker",
        "blockers",
        "next step",
        "next steps",
        "working on",
        "in progress",
        "currently",
    ),
    "decisions": (
        "decision",
        "decisions",
        "decided",
        "chose",
        "choice",
        "tradeoff",
        "tradeoffs",
        "resolved",
        "settled",
        "we will",
        "we'll",
    ),
    "brags": (
        "brag",
        "brags",
        "success",
        "successful",
        "shipped",
        "delivered",
        "accomplished",
        "won",
        "win",
        "wins",
        "performed well",
        "performance",
    ),
    "thinking": (
        "thinking",
        "thought",
        "thoughts",
        "note",
        "notes",
        "idea",
        "ideas",
        "maybe",
        "might",
        "consider",
        "reflection",
    ),
}

_SURFACE_TITLES: dict[str, str] = {
    "north_star": "North Star",
    "active_projects": "Active Projects",
    "decisions": "Decisions",
    "brags": "Brags",
    "thinking": "Thinking",
    "session_events": "Session Events",
}

_LEGACY_MAP: dict[str, str] = {
    "north_star": "governed_state",
    "active_projects": "governed_state",
    "decisions": "governed_state",
    "brags": "prepared_context",
    "thinking": "prepared_context",
    "session_events": "archive/placeholders/evidence",
}

_SESSION_EVENT_LEGACY_MAP: dict[str, str] = {
    "session_start": "archive/placeholders/evidence",
    "prompt_submit": "prepared_context",
    "post_tool_use": "prepared_context",
    "wrap_up": "archive/placeholders/evidence",
    "session_end": "archive/placeholders/evidence",
}

@dataclass(frozen=True)
class CaptureRoute:
    """Result of a surface routing decision."""

    surface_key: str
    legacy_surface_key: str
    reason: str

def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def normalize_surface_key(value: str | None) -> str | None:
    """Normalize a caller-provided surface hint to a canonical structured surface."""

    if value is None:
        return None
    token = value.strip().lower().replace("-", "_")
    token = " ".join(token.split())
    return SURFACE_ALIASES.get(token, token if token in STRUCTURED_SURFACES else None)

def surface_title(surface_key: str) -> str:
    return _SURFACE_TITLES.get(surface_key, surface_key.replace("_", " ").title())

def legacy_surface_for(surface_key: str) -> str:
    return _LEGACY_MAP.get(surface_key, "prepared_context")

def legacy_surface_for_event(event_type: str) -> str:
    return _SESSION_EVENT_LEGACY_MAP.get(event_type, "prepared_context")

def _count_keyword_hits(text: str, surface_key: str) -> int:
    lowered = text.lower()
    return sum(1 for kw in _SURFACE_KEYWORDS[surface_key] if kw in lowered)

def route_capture_surface(text: str, surface_hint: str | None = None) -> CaptureRoute:
    """Route a capture into a structured surface.

    Explicit hints win. Otherwise the router falls back to a simple keyword
    heuristic that keeps legacy callers working without a second ontology.
    """

    explicit = normalize_surface_key(surface_hint)
    if explicit:
        return CaptureRoute(
            surface_key=explicit,
            legacy_surface_key=legacy_surface_for(explicit),
            reason="explicit surface hint",
        )

    scored = [
        (surface_key, _count_keyword_hits(text, surface_key))
        for surface_key in STRUCTURED_SURFACES
    ]
    scored.sort(key=lambda item: (-item[1], STRUCTURED_SURFACES.index(item[0])))
    winner, score = scored[0]
    if score > 0:
        return CaptureRoute(
            surface_key=winner,
            legacy_surface_key=legacy_surface_for(winner),
            reason=f"heuristic keyword match ({score})",
        )

    return CaptureRoute(
        surface_key="thinking",
        legacy_surface_key=legacy_surface_for("thinking"),
        reason="default fallback to thinking",
    )

def suggest_title(text: str, *, fallback: str = "Untitled entry") -> str:
    """Derive a compact title from the first meaningful fragment of text."""

    clean = " ".join(text.split()).strip()
    if not clean:
        return fallback
    for separator in (". ", " — ", " - ", ": "):
        if separator in clean:
            candidate = clean.split(separator, 1)[0].strip()
            if candidate:
                return candidate[:90]
    return clean[:90]

def build_capture_record(
    text: str,
    *,
    surface_hint: str | None = None,
    user_id: str = "",
    session_id: str = "",
    title: str = "",
    source_tool: str = "capture",
    metadata: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    route = route_capture_surface(text, surface_hint=surface_hint)
    body = text.strip()
    payload = dict(metadata or {})
    return {
        "surface_key": route.surface_key,
        "legacy_surface_key": route.legacy_surface_key,
        "route_reason": route.reason,
        "user_id": user_id,
        "session_id": session_id,
        "title": title.strip() or suggest_title(body),
        "body": body,
        "source_tool": source_tool,
        "metadata": payload,
        "created_at": _utc_now(),
    }

def build_session_event(
    event_type: str,
    *,
    user_id: str,
    session_id: str,
    text: str = "",
    payload: Mapping[str, Any] | None = None,
    source_tool: str = "",
) -> dict[str, Any]:
    if event_type not in SESSION_EVENT_TYPES:
        raise ValueError(f"unsupported session event: {event_type}")
    event_payload = dict(payload or {})
    return {
        "event_type": event_type,
        "surface_key": "session_events",
        "legacy_surface_key": legacy_surface_for_event(event_type),
        "user_id": user_id,
        "session_id": session_id,
        "title": event_type.replace("_", " ").title(),
        "body": text.strip(),
        "payload": event_payload,
        "source_tool": source_tool or event_type,
        "created_at": _utc_now(),
    }

def _coerce_items(items: Sequence[Mapping[str, Any] | str] | None) -> list[dict[str, Any]]:
    coerced: list[dict[str, Any]] = []
    for item in items or ():
        if isinstance(item, str):
            body = item.strip()
            if body:
                coerced.append({"title": "", "body": body})
            continue
        title = str(item.get("title") or item.get("name") or "").strip()
        body = str(item.get("body") or item.get("content") or item.get("text") or "").strip()
        if not body and title:
            body = title
            title = ""
        if body:
            coerced.append({"title": title, "body": body, "metadata": dict(item.get("metadata") or {})})
    return coerced

def _render_items(items: Sequence[Mapping[str, Any] | str] | None) -> list[str]:
    bullets: list[str] = []
    for item in _coerce_items(items):
        title = str(item.get("title") or "").strip()
        body = str(item.get("body") or "").strip()
        if title and body and title.lower() != body.lower():
            bullets.append(f"- {title} — {body}")
        else:
            bullets.append(f"- {body or title}")
    return bullets

def _render_section(lines: list[str], heading: str, items: Sequence[Mapping[str, Any] | str] | None) -> None:
    rendered = _render_items(items)
    if not rendered:
        return
    lines.extend([f"## {heading}", *rendered, ""])

def build_briefing(
    structured_state: Mapping[str, Sequence[Mapping[str, Any] | str]] | None = None,
    *,
    session_manifest: Mapping[str, Any] | None = None,
    title: str = "Structured Memory Brief",
    compact: bool = False,
) -> str:
    """Render a markdown briefing from structured-memory surfaces."""

    state = structured_state or {}
    lines: list[str] = [f"# {title}", ""]

    if session_manifest:
        lines.extend(["## Session", f"- session_id: {session_manifest.get('session_id', '')}"])
        if session_manifest.get("fork_id"):
            lines.append(f"- fork_id: {session_manifest.get('fork_id', '')}")
        if session_manifest.get("started_at"):
            lines.append(f"- started_at: {session_manifest.get('started_at', '')}")
        if session_manifest.get("ended_at"):
            lines.append(f"- ended_at: {session_manifest.get('ended_at', '')}")
        lines.append("")

    _render_section(lines, surface_title("north_star"), state.get("north_star"))
    _render_section(lines, surface_title("active_projects"), state.get("active_projects"))
    _render_section(lines, surface_title("decisions"), state.get("decisions"))
    _render_section(lines, surface_title("brags"), state.get("brags"))
    _render_section(lines, surface_title("thinking"), state.get("thinking"))

    if not compact:
        _render_section(lines, surface_title("session_events"), state.get("session_events"))

    lines.extend(
        [
            "## Compatibility Map",
            "- north_star / active_projects / decisions -> governed_state",
            "- brags / thinking -> prepared_context",
            "- session_events -> archive/placeholders/evidence",
            "",
        ]
    )

    if compact:
        lines.extend(["## Next Step", "- Use this as the live briefing surface for the next session.", ""])
    else:
        lines.extend(
            [
                "## Next Step",
                "- Review the structured sections above, then capture new items with explicit surface hints when possible.",
                "",
            ]
        )

    return "\n".join(lines).rstrip() + "\n"

def get_briefing(
    structured_state: Mapping[str, Sequence[Mapping[str, Any] | str]] | None = None,
    *,
    session_manifest: Mapping[str, Any] | None = None,
) -> str:
    """Full briefing surface used by the bridge and repo-local tests."""

    return build_briefing(structured_state, session_manifest=session_manifest, title="Briefing")

def standup(
    structured_state: Mapping[str, Sequence[Mapping[str, Any] | str]] | None = None,
    *,
    session_manifest: Mapping[str, Any] | None = None,
) -> str:
    """Compact daily standup surface."""

    return build_briefing(
        structured_state,
        session_manifest=session_manifest,
        title="Standup",
        compact=True,
    )

def start_session(repo_root: Path, fork_id: str, *, channel: str = "operator") -> dict[str, Any]:
    """Thin wrapper around the existing fork lifecycle session starter."""

    return fork_lifecycle.begin_session(repo_root, fork_id, channel=channel)

def wrap_up(
    repo_root: Path,
    fork_id: str,
    session_id: str,
    *,
    drift_score_after: float | None = None,
    git_commit: str = "",
) -> dict[str, Any]:
    """Thin wrapper around the existing fork lifecycle session closer."""

    return fork_lifecycle.end_session(
        repo_root,
        fork_id,
        session_id,
        drift_score_after=drift_score_after,
        git_commit=git_commit,
    )

def build_tool_payload(
    tool: str,
    *,
    user_id: str = "",
    session_id: str = "",
    text: str = "",
    surface_hint: str | None = None,
    title: str = "",
    metadata: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a normalized payload for the live MCP edge function."""

    if tool in {"start_session", "session_start"}:
        return build_session_event(
            "session_start",
            user_id=user_id,
            session_id=session_id,
            text=text,
            payload=metadata,
            source_tool=tool,
        )
    if tool in {"wrap_up", "session_end"}:
        return build_session_event(
            "wrap_up",
            user_id=user_id,
            session_id=session_id,
            text=text,
            payload=metadata,
            source_tool=tool,
        )
    if tool == "prompt_submit":
        return build_session_event(
            "prompt_submit",
            user_id=user_id,
            session_id=session_id,
            text=text,
            payload=metadata,
            source_tool=tool,
        )
    if tool == "post_tool_use":
        return build_session_event(
            "post_tool_use",
            user_id=user_id,
            session_id=session_id,
            text=text,
            payload=metadata,
            source_tool=tool,
        )
    if tool in {"standup", "get_briefing"}:
        return {
            "tool": tool,
            "user_id": user_id,
            "session_id": session_id,
            "compact": tool == "standup",
            "include_session_events": tool == "get_briefing",
            "metadata": dict(metadata or {}),
        }
    if tool in {"capture_decision", "capture_brag"}:
        surface_hint = "decisions" if tool == "capture_decision" else "brags"
    elif tool == "capture_observation":
        surface_hint = None
    record = build_capture_record(
        text,
        surface_hint=surface_hint,
        user_id=user_id,
        session_id=session_id,
        title=title,
        source_tool=tool,
        metadata=metadata,
    )
    record["tool"] = tool
    return record
