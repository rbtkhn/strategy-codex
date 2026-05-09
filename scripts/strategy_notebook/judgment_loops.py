"""Derived judgment-loop surfacing for strategy-codex WORK tooling.

Read-only helpers that assemble revisit candidates from:
- codex-pages
- strategy-page blocks inside thread files
- the optional judgment-loop register
- cadence conductor outcomes as supporting context

This module is intentionally heuristic. It should surface revisitable judgment
without pretending to be a new source of notebook truth.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path
import re

from audit_cadence_rhythm import parse_events

RE_PAGE_START = re.compile(
    r'<!--\s*strategy-page:start\b(?P<attrs>[^>]*)-->(?P<body>.*?)<!--\s*strategy-page:end\s*-->',
    re.DOTALL,
)
RE_ATTR = re.compile(r'(\w+)="([^"]*)"')
RE_SECTION = re.compile(
    r"^###\s+(?P<title>[^\n]+)\n(?P<body>.*?)(?=^###\s+|\Z)",
    re.MULTILINE | re.DOTALL,
)
RE_DATE = re.compile(r"\b(20\d{2}-\d{2}-\d{2})\b")
RE_MD_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
RE_HEADING = re.compile(r"^#\s+(.+)$", re.MULTILINE)
RE_FIELD_LINE = re.compile(r"^\s*-\s+\*\*(?P<key>[^*]+)\*\*:\s*(?P<value>.+?)\s*$")
RE_BOLD_FIELD = re.compile(r"\*\*(Call|Prediction|Falsifier|Revisit|Status|Outcome note|Reference):\*\*\s*(.+)")

OPEN_STATUSES = {"open", "still open"}
RESOLVED_STATUSES = {"held", "weakened", "broke", "superseded"}
STATUS_VOCAB = OPEN_STATUSES | RESOLVED_STATUSES
POSITIVE_CUES = (
    "settlement",
    "hold",
    "holds",
    "pause",
    "stabil",
    "diplomac",
    "reopen",
    "relief",
    "durable",
    "resume",
    "de-escalat",
)
NEGATIVE_CUES = (
    "escalat",
    "collapse",
    "break",
    "broke",
    "ratchet",
    "blockade",
    "widen",
    "ground",
    "war",
    "fracture",
    "squeeze",
    "strike",
    "spoiler",
)
TOPIC_STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "that",
    "from",
    "into",
    "this",
    "page",
    "thread",
    "watch",
    "strategy",
    "codex",
    "iran",
    "2026",
    "2025",
    "same",
    "day",
}


@dataclass
class JudgmentLoop:
    key: str
    source_kind: str
    source_path: str
    stream: str
    title: str
    page_id: str | None
    watch: str | None
    page_date: str | None
    call: str
    falsifier: str
    revisit: str
    status: str = "open"
    confidence: str = "explicit"
    register_status: str | None = None
    register_reference: str | None = None
    last_cadence_touch: str | None = None
    cadence_verdict: str | None = None
    cadence_falsify: str | None = None
    cadence_notebook_ref: str | None = None
    derived_state: str = "open"
    due_reason: str = ""
    suggested_next_action: str = ""
    aliases: set[str] = field(default_factory=set)
    topic_keys: set[str] = field(default_factory=set)
    polarity: str = "mixed"


@dataclass
class TensionGroup:
    group_id: str
    topic: str
    shared_horizon: str
    loops: list[JudgmentLoop]
    suggested_next_action: str


def _clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\xa0", " ")).strip()


def _strip_markdown(text: str) -> str:
    text = RE_MD_LINK.sub(lambda m: m.group(1), text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    return _clean_text(text)


def _slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", _clean_text(text).lower()).strip("-")


def _extract_sections(text: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    for match in RE_SECTION.finditer(text):
        title = _clean_text(match.group("title")).lower()
        sections[title] = match.group("body").strip()
    return sections


def _extract_primary_heading(text: str) -> str | None:
    match = RE_HEADING.search(text)
    return _clean_text(match.group(1)) if match else None


def _extract_field_block(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        match = RE_FIELD_LINE.match(line)
        if match:
            fields[_clean_text(match.group("key")).lower()] = _strip_markdown(match.group("value"))
            continue
        match = RE_BOLD_FIELD.search(line)
        if match:
            fields[_clean_text(match.group(1)).lower()] = _strip_markdown(match.group(2))
    return fields


def _first_meaningful_line(text: str) -> str:
    for raw_line in text.splitlines():
        line = _strip_markdown(raw_line)
        if not line:
            continue
        if line.startswith("|"):
            continue
        return line
    return ""


def _first_paragraph(text: str) -> str:
    blocks = [block.strip() for block in re.split(r"\n\s*\n", text) if block.strip()]
    for block in blocks:
        line = _strip_markdown(block)
        if line:
            return line
    return ""


def _first_list_items(text: str, limit: int = 2) -> list[str]:
    items: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line.startswith("-"):
            continue
        item = _strip_markdown(line.lstrip("- ").strip())
        if item:
            items.append(item)
        if len(items) >= limit:
            break
    return items


def _extract_date_from_text(text: str) -> str | None:
    match = RE_DATE.search(text)
    return match.group(1) if match else None


def _to_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def _infer_polarity(call: str) -> str:
    low = call.lower()
    positive_hits = [low.find(token) for token in POSITIVE_CUES if token in low]
    negative_hits = [low.find(token) for token in NEGATIVE_CUES if token in low]
    positive = bool(positive_hits)
    negative = bool(negative_hits)
    if positive and not negative:
        return "positive"
    if negative and not positive:
        return "negative"
    if positive and negative:
        if min(positive_hits) < min(negative_hits):
            return "positive"
        if min(negative_hits) < min(positive_hits):
            return "negative"
    return "mixed"


def _topic_keys(loop: JudgmentLoop) -> set[str]:
    keys: set[str] = set()
    if loop.watch:
        keys.add(_slugify(loop.watch))
    if loop.page_id:
        keys.update(
            part
            for part in _slugify(loop.page_id).split("-")
            if len(part) > 3 and part not in TOPIC_STOPWORDS
        )
    for source in (loop.title, loop.call, loop.revisit):
        for token in re.findall(r"[a-z0-9]+", source.lower()):
            if len(token) > 4 and token not in TOPIC_STOPWORDS:
                keys.add(token)
    return keys


def _build_loop(
    *,
    source_kind: str,
    source_path: str,
    stream: str,
    title: str,
    page_id: str | None,
    watch: str | None,
    page_date: str | None,
    call: str,
    falsifier: str,
    revisit: str,
    confidence: str,
) -> JudgmentLoop | None:
    call = _clean_text(call)
    falsifier = _clean_text(falsifier)
    revisit = _clean_text(revisit)
    if not (call or falsifier or revisit):
        return None
    key_base = page_id or title or Path(source_path).stem
    loop = JudgmentLoop(
        key=f"{source_kind}:{_slugify(stream)}:{_slugify(key_base)}",
        source_kind=source_kind,
        source_path=source_path,
        stream=stream,
        title=title,
        page_id=page_id,
        watch=watch,
        page_date=page_date,
        call=call or title,
        falsifier=falsifier,
        revisit=revisit,
        confidence=confidence,
    )
    loop.aliases = {
        _slugify(title),
        _slugify(Path(source_path).stem),
    }
    if page_id:
        loop.aliases.add(_slugify(page_id))
    loop.topic_keys = _topic_keys(loop)
    loop.polarity = _infer_polarity(loop.call)
    return loop


def _parse_loop_from_sections(
    *,
    source_kind: str,
    source_path: str,
    stream: str,
    title: str,
    page_id: str | None,
    watch: str | None,
    page_date: str | None,
    sections: dict[str, str],
) -> JudgmentLoop | None:
    predictive = sections.get("prediction") or sections.get("predictive outlook") or ""
    reflection = sections.get("judgment") or sections.get("reflection") or ""
    foresight = (
        sections.get("prediction")
        or sections.get("predictive outlook")
        or
        sections.get("foresight / verify")
        or sections.get("foresight")
        or ""
    )

    explicit_fields = _extract_field_block(predictive)
    call = explicit_fields.get("prediction") or explicit_fields.get("call", "")
    falsifier = explicit_fields.get("falsifier", "")
    revisit = explicit_fields.get("revisit", "")
    confidence = "explicit"

    if not (call or falsifier or revisit):
        reflection_fields = _extract_field_block(reflection)
        call = _first_paragraph(reflection) or _first_meaningful_line(predictive) or title
        falsifier = reflection_fields.get("falsifier", "")
        revisit_items = _first_list_items(foresight, limit=2)
        revisit = " / ".join(revisit_items) if revisit_items else _first_meaningful_line(foresight)
        confidence = "legacy"

    return _build_loop(
        source_kind=source_kind,
        source_path=source_path,
        stream=stream,
        title=title,
        page_id=page_id,
        watch=watch,
        page_date=page_date,
        call=call,
        falsifier=falsifier,
        revisit=revisit,
        confidence=confidence,
    )


def _iter_codex_page_loops(notebook_root: Path) -> list[JudgmentLoop]:
    loops: list[JudgmentLoop] = []
    for path in sorted(notebook_root.glob("20[0-9][0-9]/*/*-page-*.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        sections = _extract_sections(text)
        stream = path.parent.name
        title = _extract_primary_heading(text) or path.stem
        page_date = _extract_date_from_text(path.name) or _extract_date_from_text(text)
        loop = _parse_loop_from_sections(
            source_kind="codex-page",
            source_path=path.relative_to(notebook_root).as_posix(),
            stream=stream,
            title=title,
            page_id=path.stem,
            watch=None,
            page_date=page_date,
            sections=sections,
        )
        if loop is not None:
            loops.append(loop)
    return loops


def _iter_thread_page_loops(notebook_root: Path) -> list[JudgmentLoop]:
    loops: list[JudgmentLoop] = []
    for path in sorted(notebook_root.glob("20[0-9][0-9]/*/*thread*.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        stream = path.parent.name
        for match in RE_PAGE_START.finditer(text):
            attrs = dict(RE_ATTR.findall(match.group("attrs")))
            body = match.group("body").strip()
            sections = _extract_sections(body)
            title = ""
            for raw_line in body.splitlines():
                if raw_line.startswith("### Page:"):
                    title = _clean_text(raw_line.split(":", 1)[1])
                    break
            if not title:
                title = _extract_primary_heading(body) or attrs.get("id", "") or f"{stream}-thread-page"
            loop = _parse_loop_from_sections(
                source_kind="strategy-page",
                source_path=path.relative_to(notebook_root).as_posix(),
                stream=stream,
                title=title,
                page_id=attrs.get("id"),
                watch=attrs.get("watch") or None,
                page_date=attrs.get("date") or _extract_date_from_text(body),
                sections=sections,
            )
            if loop is not None:
                loops.append(loop)
    return loops


def _iter_register_loops(notebook_root: Path) -> list[JudgmentLoop]:
    path = notebook_root / "notes" / "JUDGMENT-LOOP-REGISTER.md"
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8", errors="replace")
    chunks = re.split(r"(?m)^##\s+", text)
    loops: list[JudgmentLoop] = []
    for chunk in chunks[1:]:
        lines = chunk.splitlines()
        header = lines[0].strip()
        body = "\n".join(lines[1:])
        header_match = re.match(r"(?P<date>\d{4}-\d{2}-\d{2})\s*-\s*(?P<label>.+)", header)
        if not header_match:
            continue
        fields = _extract_field_block(body)
        label = _clean_text(header_match.group("label"))
        reference = fields.get("reference", "")
        source_path = reference
        link_match = RE_MD_LINK.search(body)
        if link_match:
            source_path = _strip_markdown(link_match.group(1))
        loop = _build_loop(
            source_kind="register",
            source_path=source_path or f"notes/JUDGMENT-LOOP-REGISTER.md#{_slugify(label)}",
            stream="register",
            title=label,
            page_id=_slugify(label),
            watch=None,
            page_date=header_match.group("date"),
            call=fields.get("prediction") or fields.get("call", ""),
            falsifier=fields.get("falsifier", ""),
            revisit=fields.get("revisit", ""),
            confidence="register",
        )
        if loop is None:
            continue
        loop.status = fields.get("status", "open").lower()
        loop.register_status = loop.status
        loop.register_reference = reference
        loops.append(loop)
    return loops


def _latest_continuity_date(notebook_root: Path) -> date | None:
    latest: date | None = None
    for path in notebook_root.glob("20[0-9][0-9]/chapters/*/days.md"):
        text = path.read_text(encoding="utf-8", errors="replace")
        for found in RE_DATE.findall(text):
            parsed = _to_date(found)
            if parsed and (latest is None or parsed > latest):
                latest = parsed
    return latest


def _match_register(page_loop: JudgmentLoop, register_loops: list[JudgmentLoop]) -> JudgmentLoop | None:
    for reg in register_loops:
        haystack = " ".join(filter(None, [reg.source_path, reg.register_reference or "", reg.title])).lower()
        if any(alias and alias in haystack for alias in page_loop.aliases):
            return reg
    return None


def _apply_cadence_context(loop: JudgmentLoop, cadence_events: list[dict]) -> None:
    best_dt: datetime | None = None
    for event in cadence_events:
        kv = event.get("kv") or {}
        verdict = _clean_text(str(kv.get("verdict", ""))).lower()
        notebook_ref = _clean_text(str(kv.get("notebook_ref", ""))).lower()
        falsify = _clean_text(str(kv.get("falsify", "")))
        haystack = " ".join(filter(None, [notebook_ref, falsify.lower()]))
        if not haystack:
            continue
        if not any(alias and alias in haystack for alias in loop.aliases):
            continue
        if best_dt is None or event["dt"] > best_dt:
            best_dt = event["dt"]
            loop.last_cadence_touch = event["dt"].strftime("%Y-%m-%d")
            loop.cadence_verdict = verdict or None
            loop.cadence_falsify = falsify or None
            loop.cadence_notebook_ref = notebook_ref or None
    if loop.cadence_verdict in STATUS_VOCAB:
        loop.status = loop.cadence_verdict


def _derive_due_state(loop: JudgmentLoop, today: date, latest_continuity: date | None) -> None:
    status = (loop.status or "open").lower()
    if status in RESOLVED_STATUSES:
        loop.derived_state = "resolved"
        loop.due_reason = f"Resolved via status `{status}`."
        loop.suggested_next_action = ""
        return

    revisit_date = _to_date(_extract_date_from_text(loop.revisit))
    page_date = _to_date(loop.page_date)
    revisit_low = loop.revisit.lower()

    if revisit_date and revisit_date <= today:
        loop.derived_state = "due"
        loop.due_reason = f"Revisit date {revisit_date.isoformat()} has passed."
    elif any(token in revisit_low for token in ("weekly", "week", "month", "monthly")) and page_date:
        delta = (today - page_date).days
        threshold = 7 if "week" in revisit_low else 30
        if delta >= threshold:
            loop.derived_state = "due"
            loop.due_reason = "Periodic revisit window is stale."
    elif latest_continuity and page_date and latest_continuity > page_date and (latest_continuity - page_date).days >= 7:
        loop.derived_state = "due"
        loop.due_reason = "Continuity advanced without a recorded revisit."
    else:
        loop.derived_state = "open"
        if revisit_date:
            loop.due_reason = f"Waiting for revisit date {revisit_date.isoformat()}."
        elif loop.revisit:
            loop.due_reason = "Open loop with trigger pending or still heuristic."
        else:
            loop.due_reason = "Open loop without a confidently parsed revisit horizon."

    if loop.derived_state == "due":
        if loop.register_status is None and loop.cadence_notebook_ref is None:
            loop.suggested_next_action = "Revisit in days.md or month continuity and tag outcome."
        elif loop.register_status is None:
            loop.suggested_next_action = "Resolve ambiguity between page loop and cadence outcome, then tag continuity."
        else:
            loop.suggested_next_action = "Update register status and mirror the outcome in continuity."
    else:
        if loop.register_status is None and loop.revisit:
            loop.suggested_next_action = "Keep open pending named trigger; add to register only if it becomes consequential."
        elif loop.register_status is None:
            loop.suggested_next_action = "Keep open pending clearer trigger."
        else:
            loop.suggested_next_action = "Keep register and page in sync while the trigger remains open."


def _build_tension_groups(loops: list[JudgmentLoop]) -> list[TensionGroup]:
    candidates = [loop for loop in loops if loop.derived_state in {"due", "open"}]
    groups: dict[str, list[JudgmentLoop]] = {}
    for i, left in enumerate(candidates):
        for right in candidates[i + 1 :]:
            if left.stream == right.stream:
                continue
            if not (left.topic_keys & right.topic_keys):
                continue
            if {left.polarity, right.polarity} != {"positive", "negative"}:
                continue
            topic = sorted(left.topic_keys & right.topic_keys)[0]
            groups.setdefault(topic, [])
            if left not in groups[topic]:
                groups[topic].append(left)
            if right not in groups[topic]:
                groups[topic].append(right)

    tensions: list[TensionGroup] = []
    for topic, grouped_loops in sorted(groups.items()):
        if len(grouped_loops) < 2:
            continue
        shared_horizon = next(
            (loop.page_date for loop in grouped_loops if loop.page_date),
            "",
        )
        tensions.append(
            TensionGroup(
                group_id=f"tension-{_slugify(topic)}",
                topic=topic,
                shared_horizon=shared_horizon,
                loops=sorted(grouped_loops, key=lambda loop: (loop.stream, loop.title)),
                suggested_next_action="Compare side-by-side in days.md or month continuity; keep both open until the trigger resolves.",
            )
        )
    return tensions


def build_judgment_loop_report(
    notebook_root: Path,
    *,
    user_id: str = "grace-mar",
    cadence_events_path: Path | None = None,
    today: date | None = None,
) -> dict[str, object]:
    """Return a derived judgment-loop report for console and conductor surfaces."""
    notebook_root = notebook_root.resolve()
    today = today or date.today()
    latest_continuity = _latest_continuity_date(notebook_root)

    page_loops = _iter_codex_page_loops(notebook_root) + _iter_thread_page_loops(notebook_root)
    register_loops = _iter_register_loops(notebook_root)
    cadence_events = parse_events(
        user_id,
        events_path=(cadence_events_path or Path(__file__).resolve().parents[2] / "docs" / "skill-work" / "work-cadence" / "work-cadence-events.md"),
    )
    cadence_outcomes = [event for event in cadence_events if event.get("kind") == "coffee_conductor_outcome"]

    loops: list[JudgmentLoop] = []
    matched_register_keys: set[str] = set()
    for loop in page_loops:
        reg = _match_register(loop, register_loops)
        if reg is not None:
            loop.register_status = reg.status
            loop.register_reference = reg.register_reference
            loop.status = reg.status
            matched_register_keys.add(reg.key)
        _apply_cadence_context(loop, cadence_outcomes)
        _derive_due_state(loop, today, latest_continuity)
        if loop.derived_state in {"due", "open"}:
            loops.append(loop)

    # Also surface register-only consequential loops that do not match a page yet.
    for reg in register_loops:
        if reg.key in matched_register_keys:
            continue
        _apply_cadence_context(reg, cadence_outcomes)
        _derive_due_state(reg, today, latest_continuity)
        if reg.derived_state in {"due", "open"}:
            loops.append(reg)

    tensions = _build_tension_groups(loops)
    return {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "notebook_root": notebook_root,
        "latest_continuity_date": latest_continuity.isoformat() if latest_continuity else None,
        "loops": sorted(loops, key=lambda loop: (loop.derived_state != "due", loop.stream, loop.page_date or "", loop.title)),
        "tensions": tensions,
    }


def format_due_open_loops_markdown(
    report: dict[str, object],
    *,
    max_loops: int = 6,
    include_tension: bool = True,
) -> list[str]:
    """Render a compact markdown block for conductor or console surfaces."""
    loops: list[JudgmentLoop] = report["loops"]  # type: ignore[assignment]
    tensions: list[TensionGroup] = report["tensions"]  # type: ignore[assignment]

    if not loops:
        return ["- _No due/open judgment loops surfaced from pages, register, or cadence._"]

    lines: list[str] = []
    for loop in loops[:max_loops]:
        state = "due" if loop.derived_state == "due" else "open"
        path = loop.source_path
        lines.append(
            f"- **{loop.stream}** â€” `{state}` â€” `{path}` â€” "
            f"Prediction: {loop.call} "
            f"Revisit: {loop.revisit or 'not explicit'} "
            f"Next: {loop.suggested_next_action}"
        )
    if include_tension and tensions:
        lines.extend(["", "### Tension", ""])
        for tension in tensions:
            stream_bits = " vs ".join(f"`{loop.stream}`" for loop in tension.loops[:4])
            call_bits = " / ".join(_clean_text(loop.call)[:90] for loop in tension.loops[:2])
            horizon = tension.shared_horizon or "shared trigger not explicit"
            lines.append(
                f"- **{tension.topic}** â€” {stream_bits} â€” horizon: {horizon} â€” "
                f"{call_bits} â€” Next: {tension.suggested_next_action}"
            )
    return lines
