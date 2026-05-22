#!/usr/bin/env python3
"""
Resolve coffee-conductor helpers for the **single D â€” Conductor** menu line.

The live UI no longer has a lettered conductor chooser. Operators invoke a conductor by name (`toscanini`, `furtwangler`, `karajan`, `kleiber`, or `bernstein`), then receive the resolved A-D Conductor Action Menu.
invokes **D** / a name fragment **without** a full **coffee** session (see
``.cursor/skills/coffee/SKILL.md`` Â§ *Conductor only*). The five masters are
Legacy ``D1``..``D5`` and old cadence lines are still recognized for log continuity, but helper output must not emit lettered conductor choices.

Legacy ``D1``..``D5`` in old logs are still recognized.

Pure functions over event dicts shaped like ``audit_cadence_rhythm.parse_events()``
output: ``{"dt", "kind", "user", "line", "kv"}``.

This module still helps with two advisory questions:

1. Which conductor was picked most recently on disk? (continuity)
2. Which conductor does the system recommend from dream + load signals? (recommendation)
"""

from __future__ import annotations

import unicodedata
import sys
from typing import Any
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from strategy_notebook.judgment_loops import (
    build_judgment_loop_report,
    format_due_open_loops_markdown,
)

MENU_PICK_TO_CONDUCTOR = {
    "D1": "toscanini",
    "D2": "furtwangler",
    "D3": "bernstein",
    "D4": "karajan",
    "D5": "kleiber",
}
# Display order in coffee menu text (Toscanini / FurtwÃ¤ngler / Karajan / Kleiber / Bernstein)
_CONDUCTOR_MENU: list[tuple[str, str]] = [
    ("Toscanini", "toscanini"),
    ("FurtwÃ¤ngler", "furtwangler"),
    ("Karajan", "karajan"),
    ("Kleiber", "kleiber"),
    ("Bernstein", "bernstein"),
]
KNOWN_CONDUCTOR_SLUGS = frozenset(s for _n, s in _CONDUCTOR_MENU)
CONDUCTOR_MOVEMENT_LETTERS = frozenset({"A", "B", "C", "D"})
COMPILED_CONDUCTOR_SHORTCUTS: dict[str, str] = {
    "toscanini": "toscanini-verify",
    "furtwangler": "furtwangler-tension",
    "karajan": "karajan-review",
    "kleiber": "kleiber-close",
    "bernstein": "bernstein-stakes",
}

# Deprecated master-selection row. Kept only so old log helpers can import
# a stable shape; do not emit these letters in user-facing prompts.
_CONDUCTOR_MCQ_ROWS: tuple[tuple[str, str, str, str], ...] = (
    ("A", "toscanini", "Toscanini", "Precision â€” verify claims and seams; cut flourish that outruns the material."),
    ("B", "furtwangler", "FurtwÃ¤ngler", "Flow â€” hold tension open; listen for the line under the line before closing."),
    ("C", "karajan", "Karajan", "Elegance â€” long-arc balance and proportion; remove what blurs the whole."),
    ("D", "kleiber", "Kleiber", "Selectivity â€” one or two deep hotspots; refuse the rest explicitly this round."),
    ("E", "bernstein", "Bernstein", "Vitality â€” stakes, pulse, and language that can carry heat live."),
)
CONDUCTOR_SUBMENU_LETTER_TO_SLUG: dict[str, str] = {
    letter: slug for letter, slug, _name, _attr in _CONDUCTOR_MCQ_ROWS
}

# Legacy: D1..D5 â†’ different letters; new logs use picked=D with conductor=.
CONDUCTOR_TO_MENU_PICK = {slug: pick for pick, slug in MENU_PICK_TO_CONDUCTOR.items()}

# Legacy logs may still contain ``picked=D`` from the older single-line conductor menu.
_PICKED_CONDUCTOR = frozenset({"conductor", "E", "D", *MENU_PICK_TO_CONDUCTOR.keys()})


def normalize_conductor_slug(value: str) -> str:
    """Return first segment if legacy ``a+b`` stacks; else stripped value."""
    s = str(value).strip()
    if "+" in s:
        return s.split("+", 1)[0].strip()
    return s


def conductor_slug_for_menu_pick(pick: str) -> str | None:
    """Map legacy ``D1``..``D5`` to slug. Bare ``D`` has no slug without ``conductor=``."""
    p = str(pick).strip().upper()
    if p == "D":
        return None
    return MENU_PICK_TO_CONDUCTOR.get(p)


def _is_explicit_conductor_pick(event: dict[str, Any]) -> bool:
    if event.get("kind") != "coffee_pick":
        return False
    kv = event.get("kv") or {}
    picked = str(kv.get("picked", "")).strip()
    conductor = normalize_conductor_slug(kv.get("conductor"))
    return picked in _PICKED_CONDUCTOR and conductor in KNOWN_CONDUCTOR_SLUGS


def _strip_accents(s: str) -> str:
    return "".join(
        c
        for c in unicodedata.normalize("NFD", s)
        if unicodedata.category(c) != "Mn"
    )


def conductor_submenu_letter_to_slug(letter: str) -> str | None:
    """Deprecated: master letters no longer resolve to conductor slugs."""
    _ = letter
    return None


def _display_name_for_slug(slug: str) -> str:
    for _L, s, display, _attr in _CONDUCTOR_MCQ_ROWS:
        if s == normalize_conductor_slug(slug):
            return display
    return slug


def _continuity_kicker(
    slug: str,
    *,
    last_slug: str | None,
    recommended_slug: str | None,
) -> str:
    """One short clause for the MCQ line (continuity + advisory)."""
    s = normalize_conductor_slug(slug)
    last = normalize_conductor_slug(last_slug) if last_slug else None
    rec = normalize_conductor_slug(recommended_slug) if recommended_slug else None
    if last and last == s:
        return "Continuity: same card as your last `coffee_pick`."
    if last and last != s and rec == s:
        return (
            f"Continuity: pivot from **{_display_name_for_slug(last)}**; "
            "advisory (dream/load) also leans here today."
        )
    if last and last != s:
        return f"Continuity: pivot from last **{_display_name_for_slug(last)}** toward this mode."
    if rec == s:
        return "Advisory: dream / session-load tips this card today (no prior pick match)."
    return "Open entry: no prior conductor in this chain."


def format_conductor_mcq_block(
    *,
    last_slug: str | None = None,
    focus_text: str | None = None,
    recommended_slug: str | None = None,
) -> str:
    """Return the compatibility name prompt; no lettered master rows are emitted."""
    names = ", ".join(slug for _display, slug in _CONDUCTOR_MENU)
    lines: list[str] = [
        f"Name a conductor: {names}.",
        "Letters select only actions after a conductor is resolved; they do not select a conductor.",
    ]
    if focus_text and str(focus_text).strip():
        lines.append(
            f"Last cadence `focus` / `arc`: **{str(focus_text).strip()}**"
        )
    if last_slug:
        lines.append(f"Last conductor: **{_display_name_for_slug(last_slug)}**.")
    if recommended_slug:
        lines.append(f"System hint: **{_display_name_for_slug(recommended_slug)}**.")
    return "\n".join(lines)


def build_conductor_mcq_for_user(user_id: str) -> str:
    """Load cadence (optional dream + session load) and format a name-only prompt.

    Compatibility wrapper for the old master-MCQ helper. It must not emit A-E
    conductor-selection rows.
    """
    import json
    from pathlib import Path

    try:
        from audit_cadence_rhythm import parse_events
    except ImportError:
        from scripts.audit_cadence_rhythm import parse_events

    events = parse_events(user_id)
    last = last_logged_conductor(events)
    focus = focus_for_last_conductor(events)

    dream: dict[str, Any] | None = None
    try:
        try:
            from repo_io import profile_dir
        except ImportError:
            from scripts.repo_io import profile_dir
        p = profile_dir(user_id) / "last-dream.json"
        if p.is_file():
            dream = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, TypeError):
        dream = None

    try:
        from assess_session_load import assess_load
    except ImportError:
        from scripts.assess_session_load import assess_load

    assess = assess_load(user_id)
    rec_slug = system_recommended_conductor(dream=dream, assess=assess)

    return format_conductor_mcq_block(
        last_slug=last,
        focus_text=focus,
        recommended_slug=rec_slug,
    )


def build_conductor_revisit_block(
    user_id: str,
    *,
    notebook_root: str | Path | None = None,
    max_loops: int = 4,
) -> str:
    """Compact due/open judgment-loop surfacing for conductor orientation.

    This is advisory WORK scaffolding only. It surfaces derived revisit pressure
    and polyphonic tension; it does not resolve judgments or write outcomes.
    """
    root = Path(notebook_root) if notebook_root is not None else Path(__file__).resolve().parent.parent / "codex"
    report = build_judgment_loop_report(root, user_id=user_id)
    lines = [
        "**Open loops due for revisit** Ã¢â‚¬â€ derived from pages, the judgment-loop register, and cadence outcomes.",
    ]
    lines.extend(
        format_due_open_loops_markdown(
            report,
            max_loops=max_loops,
            include_tension=True,
        )
    )
    return "\n".join(lines)


def resolve_d_conductor(
    name_fragment: str | None,
    *,
    last_conductor_slug: str | None = None,
) -> tuple[str | None, str | None]:
    """Resolve a conductor name fragment.

    Bare ``conductor`` / empty fragments are incomplete in the live UI. Single
    letters no longer resolve masters; A-D are reserved for a resolved action
    menu, and E is not a conductor pick.
    Returns ``(slug, err)`` with ``err`` in ``(None, "no_prior", "no_match", "ambiguous")``.
    """
    frag = (name_fragment or "").strip()
    if not frag:
        return None, "no_prior"
    if len(frag) == 1 and frag.upper() in {"A", "B", "C", "D", "E"}:
        return None, "no_match"
    frag_l = frag.lower()
    fstrip = _strip_accents(frag).lower()
    matches: list[str] = []
    for display, slug in _CONDUCTOR_MENU:
        s = normalize_conductor_slug(slug)
        dnorm = _strip_accents(display).lower()
        dcompact = dnorm.replace(" ", "")
        if (
            s.startswith(frag_l)
            or s.startswith(frag_l.replace("w", "v"))
            or dcompact.startswith(frag_l)
            or dnorm.startswith(frag_l)
            or (fstrip and s.startswith(fstrip))
        ):
            if s not in matches:
                matches.append(s)
    if len(matches) == 1:
        return matches[0], None
    if not matches:
        return None, "no_match"
    return None, "ambiguous"


def menu_pick_for_conductor_slug(slug: str) -> str | None:
    """Return ``D`` for any known conductor slug (new log convention); else ``None``."""
    s = normalize_conductor_slug(slug)
    if s in KNOWN_CONDUCTOR_SLUGS:
        return "D"
    return None


def last_coffee_pick_conductor_event(events: list[dict[str, Any]]) -> dict[str, Any] | None:
    """Most recent ``coffee_pick`` with a conductor-bearing ``picked=`` value."""
    candidates: list[dict[str, Any]] = []
    for e in events:
        if e.get("kind") != "coffee_pick":
            continue
        kv = e.get("kv") or {}
        picked = str(kv.get("picked", "")).strip()
        if picked not in _PICKED_CONDUCTOR:
            continue
        cond = kv.get("conductor")
        if cond is None or not str(cond).strip():
            continue
        candidates.append(e)
    if not candidates:
        return None
    return max(candidates, key=lambda x: x["dt"])


def last_logged_conductor(events: list[dict[str, Any]]) -> str | None:
    """Normalized conductor slug from last qualifying ``coffee_pick``, or ``None``."""
    ev = last_coffee_pick_conductor_event(events)
    if ev is None:
        return None
    c = (ev.get("kv") or {}).get("conductor")
    if c is None:
        return None
    return normalize_conductor_slug(str(c))


def _is_conductor_close_event(event: dict[str, Any], conductor: str) -> bool:
    if event.get("kind") != "coffee_close":
        return False
    kv = event.get("kv") or {}
    state = str(kv.get("conductor_state", "")).strip().lower()
    closed_conductor = normalize_conductor_slug(kv.get("conductor"))
    return state == "closed" and closed_conductor == conductor


def active_conductor_arc(events: list[dict[str, Any]]) -> dict[str, Any] | None:
    """Return the most recent unresolved conductor arc from cadence-style events.

    This helper is conservative: a bare movement letter may continue only if the
    latest relevant conductor event is an explicit conductor pick and no later
    `coffee_close conductor_state=closed` sealed that same arc. Outcome lines
    enrich the arc but do not open a fresh one.
    """
    relevant = sorted(events, key=lambda e: e.get("dt"))
    active: dict[str, Any] | None = None
    for event in relevant:
        if _is_explicit_conductor_pick(event):
            kv = event.get("kv") or {}
            conductor = normalize_conductor_slug(kv.get("conductor"))
            active = {
                "conductor": conductor,
                "focus": str(kv.get("focus", "")).strip() or None,
                "arc": str(kv.get("arc", "")).strip() or None,
                "picked_at": event.get("dt"),
                "picked_line": event.get("line"),
                "latest_event_kind": "coffee_pick",
                "outcome_count": 0,
                "closed": False,
            }
            continue
        if active is None:
            continue
        conductor = active["conductor"]
        kv = event.get("kv") or {}
        if event.get("kind") == "coffee_conductor_outcome":
            explicit = normalize_conductor_slug(kv.get("conductor"))
            if explicit and explicit != conductor:
                continue
            active["outcome_count"] += 1
            active["latest_event_kind"] = "coffee_conductor_outcome"
            active["latest_outcome"] = {
                "dt": event.get("dt"),
                "verdict": str(kv.get("verdict", "")).strip() or None,
                "notebook_ref": str(kv.get("notebook_ref", "")).strip() or None,
                "falsify": str(kv.get("falsify", "")).strip() or None,
            }
            continue
        if _is_conductor_close_event(event, conductor):
            active["closed"] = True
            active["latest_event_kind"] = "coffee_close"
            active["closed_at"] = event.get("dt")

    if active is None or active.get("closed"):
        return None
    return active


def resolve_active_conductor_movement(
    movement: str | None,
    events: list[dict[str, Any]],
) -> dict[str, Any] | None:
    """Resolve a bare movement letter against the current active conductor arc."""
    letter = str(movement or "").strip().upper()
    if letter not in CONDUCTOR_MOVEMENT_LETTERS:
        return None
    active = active_conductor_arc(events)
    if active is None:
        return None
    return {
        "conductor": active["conductor"],
        "movement": letter,
        "source": "active_conductor_arc",
        "focus": active.get("focus"),
        "arc": active.get("arc"),
        "picked_at": active.get("picked_at"),
        "outcome_count": int(active.get("outcome_count") or 0),
    }


def format_coffee_hub_e_line(user_id: str) -> str:
    """Compatibility helper for the removed coffee conductor hub line.

    New UI must not emit an E conductor option. Return a name-only instruction
    so accidental callers remain safe.
    """
    _ = user_id
    return "Conductor is standalone: name toscanini, furtwangler, karajan, kleiber, or bernstein."


def focus_for_last_conductor(events: list[dict[str, Any]]) -> str | None:
    """Last ``focus=`` or ``arc=`` on a qualifying ``coffee_pick`` (``focus`` wins)."""
    ev = last_coffee_pick_conductor_event(events)
    if ev is None:
        return None
    kv = ev.get("kv") or {}
    if "focus" in kv and str(kv.get("focus", "")).strip():
        return str(kv["focus"]).strip()
    if "arc" in kv and str(kv.get("arc", "")).strip():
        return str(kv["arc"]).strip()
    return None


def recommended_conductor_from_menu_recommendation(letter: str) -> str:
    """Map session-load ``recommended`` hub letter (A/B/C) to conductor slug; unknown â†’ ``furtwangler``.

    Aligns with coffee hub: **A** Steward â†’ **kleiber**; **B** Engineer â†’ **toscanini**; **C** Historian â†’ **bernstein**.
    """
    m = {"A": "kleiber", "B": "toscanini", "C": "bernstein"}
    key = str(letter).strip().upper()[:1]
    return m.get(key, "furtwangler")


def _dream_implies_risky_worktree_seam(dream: dict[str, Any]) -> bool:
    if dream.get("risky_worktree") is True:
        return True
    wt = str(dream.get("worktreeAdvice") or "").lower()
    if not wt.strip():
        return False
    # seam / merge / conflict / explicit worktree caution
    markers = ("seam", "merge", "conflict", "risky", "dirty", "rebase", "worktree")
    return any(m in wt for m in markers)


def _dream_implies_steward_or_tomorrow(dream: dict[str, Any]) -> bool:
    if str(dream.get("tomorrow_inherits") or "").strip():
        return True
    sh = str(dream.get("steward_hint") or "").strip().lower()
    if sh and sh not in ("false", "0", "no", ""):
        return True
    st = str(dream.get("steward") or "").strip().lower()
    if st and st not in ("false", "0", "no", ""):
        return True
    summary = str(dream.get("summary") or "").lower()
    return "steward" in summary and "gate" in summary


def _dream_implies_long_arc_balance(dream: dict[str, Any]) -> bool:
    text = " ".join(
        str(dream.get(key) or "")
        for key in ("summary", "tomorrow_inherits", "dream_to_coffee_menu", "long_arc_hint")
    ).lower()
    if not text.strip():
        return False
    markers = ("month", "meta", "balance", "blend", "arc", "shape", "architecture", "polish")
    return any(marker in text for marker in markers)


def system_recommended_conductor(
    *,
    dream: dict[str, Any] | None = None,
    assess: dict[str, Any] | None = None,
) -> str:
    """Layered conductor recommendation from dream + load signals.

    Order: (1) risky worktree / ``worktreeAdvice`` â†’ **toscanini**;
    (2) ``tomorrow_inherits`` or steward-style hint â†’ **kleiber**;
    (3) long-arc / balance hints â†’ **karajan**;
    (4) ``assess["recommended"]`` â†’ hub A/B/C map (Steward/Engineer/Historian);
    (5) **furtwangler**.
    """
    if dream:
        if _dream_implies_risky_worktree_seam(dream):
            return "toscanini"
        if _dream_implies_steward_or_tomorrow(dream):
            return "kleiber"
        if _dream_implies_long_arc_balance(dream):
            return "karajan"
    if assess:
        rec = assess.get("recommended")
        if isinstance(rec, str) and rec.strip():
            letter = rec.strip().upper()[:1]
            if letter in ("A", "B", "C"):
                return recommended_conductor_from_menu_recommendation(letter)
    return "furtwangler"


def system_recommended_menu_pick(
    *,
    dream: dict[str, Any] | None = None,
    assess: dict[str, Any] | None = None,
) -> str:
    """Menu pick for the current recommendation helper."""
    slug = system_recommended_conductor(dream=dream, assess=assess)
    pick = menu_pick_for_conductor_slug(slug)
    if pick is None:
        raise ValueError(f"Unknown conductor slug: {slug}")
    return pick


def conductor_for_d1_continuation(events: list[dict[str, Any]]) -> str | None:
    """Backward-compatible alias for older D1 continuity wording."""
    return last_logged_conductor(events)


def focus_for_d1_continuation(events: list[dict[str, Any]]) -> str | None:
    """Backward-compatible alias for older D1 continuity wording."""
    return focus_for_last_conductor(events)


def d2_conductor_from_menu_recommendation(letter: str) -> str:
    """Backward-compatible alias for session-load recommendation helper."""
    return recommended_conductor_from_menu_recommendation(letter)


def d2_conductor_resolved(
    *,
    dream: dict[str, Any] | None = None,
    assess: dict[str, Any] | None = None,
) -> str:
    """Backward-compatible alias for recommendation helper."""
    return system_recommended_conductor(dream=dream, assess=assess)


def d2_conductor_from_assess_load(assess: dict[str, Any]) -> str:
    """Backward-compatible alias for assess-only recommendation helper."""
    return system_recommended_conductor(dream=None, assess=assess)


def compiled_shortcut_for_conductor(slug: str | None) -> str | None:
    """User-facing compiled shortcut name for a mature conductor line."""
    if slug is None:
        return None
    return COMPILED_CONDUCTOR_SHORTCUTS.get(normalize_conductor_slug(slug))


def should_offer_compiled_shortcut(
    events: list[dict[str, Any]],
    slug: str | None,
    *,
    min_picks: int = 2,
    min_outcomes: int = 2,
) -> bool:
    """Conservative heuristic for when a compiled shortcut is mature enough to offer."""
    normalized = normalize_conductor_slug(slug)
    if normalized not in KNOWN_CONDUCTOR_SLUGS:
        return False
    pick_count = 0
    outcome_count = 0
    for event in events:
        kv = event.get("kv") or {}
        event_slug = normalize_conductor_slug(kv.get("conductor"))
        if event.get("kind") == "coffee_pick" and _is_explicit_conductor_pick(event):
            if event_slug == normalized:
                pick_count += 1
        elif event.get("kind") == "coffee_conductor_outcome" and event_slug == normalized:
            outcome_count += 1
    return pick_count >= min_picks and outcome_count >= min_outcomes
