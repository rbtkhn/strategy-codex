"""
Illustrations for coffee conductor helpers (name-only standalone **`conductor`**).

Helper signals still matter: the log can show which conductor was picked most recently,
and dream/load can still point elsewhere (e.g. **Bernstein** when ``recommended: C``).
"""

from __future__ import annotations

from datetime import datetime, timezone
from scripts.audit_cadence_rhythm import parse_events
from scripts.cadence_conductor_resolution import (
    active_conductor_arc,
    build_conductor_mcq_for_user,
    compiled_shortcut_for_conductor,
    conductor_for_d1_continuation,
    conductor_slug_for_menu_pick,
    conductor_submenu_letter_to_slug,
    d2_conductor_from_assess_load,
    d2_conductor_from_menu_recommendation,
    d2_conductor_resolved,
    focus_for_d1_continuation,
    format_coffee_hub_e_line,
    format_conductor_mcq_block,
    last_coffee_pick_conductor_event,
    last_logged_conductor,
    menu_pick_for_conductor_slug,
    normalize_conductor_slug,
    resolve_active_conductor_movement,
    resolve_d_conductor,
    should_offer_compiled_shortcut,
    system_recommended_menu_pick,
)

def _ts(*, day: int = 1, hour: int = 12, minute: int = 0) -> datetime:
    return datetime(2026, 4, day, hour, minute, tzinfo=timezone.utc)

def _pick(
    dt: datetime,
    *,
    picked: str = "D1",
    conductor: str = "kleiber",
    focus: str | None = None,
    arc: str | None = None,
) -> dict:
    kv: dict[str, str] = {"picked": picked, "conductor": conductor}
    if focus is not None:
        kv["focus"] = focus
    if arc is not None:
        kv["arc"] = arc
    return {"dt": dt, "kind": "coffee_pick", "user": "grace-mar", "kv": kv, "line": ""}

def test_illustration_normalize_legacy_stack():
    assert normalize_conductor_slug("kleiber+toscanini") == "kleiber"

def test_illustration_menu_exposes_five_named_conductors_directly():
    assert conductor_slug_for_menu_pick("D1") == "toscanini"
    assert conductor_slug_for_menu_pick("D2") == "furtwangler"
    assert conductor_slug_for_menu_pick("D3") == "bernstein"
    assert conductor_slug_for_menu_pick("D4") == "karajan"
    assert conductor_slug_for_menu_pick("D5") == "kleiber"
    assert conductor_slug_for_menu_pick("D") is None

def test_illustration_menu_round_trip_is_stable():
    for slug in ("toscanini", "furtwangler", "bernstein", "karajan", "kleiber"):
        assert menu_pick_for_conductor_slug(slug) == "D"
    assert menu_pick_for_conductor_slug("kleiber+toscanini") == "D"

def test_resolve_d_bare_uses_last():
    slug, err = resolve_d_conductor("", last_conductor_slug="bernstein")
    assert slug is None and err == "no_prior"
    _s, err2 = resolve_d_conductor("", last_conductor_slug=None)
    assert err2 == "no_prior"

def test_resolve_d_prefix():
    assert resolve_d_conductor("bern", last_conductor_slug=None) == ("bernstein", None)
    assert resolve_d_conductor("kar", last_conductor_slug=None) == ("karajan", None)
    assert resolve_d_conductor("karajan", last_conductor_slug=None) == ("karajan", None)
    assert resolve_d_conductor("kleiber", last_conductor_slug=None) == ("kleiber", None)
    assert resolve_d_conductor("k", last_conductor_slug=None)[1] == "ambiguous"
    assert resolve_d_conductor("conductor", last_conductor_slug=None) == (None, "no_match")

def test_resolve_d_single_letters_do_not_select_masters():
    """Master-selection letters are deprecated; letters only select resolved actions."""
    assert resolve_d_conductor("B", last_conductor_slug=None) == (None, "no_match")
    assert resolve_d_conductor("b", last_conductor_slug=None) == (None, "no_match")
    assert conductor_submenu_letter_to_slug("D") is None
    assert conductor_submenu_letter_to_slug("x") is None

def test_format_conductor_name_prompt_has_no_master_rows():
    text = format_conductor_mcq_block(
        last_slug="kleiber",
        focus_text="iran/hormuz",
        recommended_slug="karajan",
    )
    assert "Name a conductor:" in text
    assert "toscanini" in text
    assert "karajan" in text
    assert "iran/hormuz" in text
    assert "Last conductor: **Kleiber**." in text
    assert "System hint: **Karajan**." in text
    assert "**A.**" not in text
    assert "**E.**" not in text

def test_build_conductor_mcq_for_user_runs():
    s = build_conductor_mcq_for_user("grace-mar")
    assert "Name a conductor:" in s
    assert "**E.** **Bernstein**" not in s

def test_removed_coffee_hub_e_helper_is_name_only():
    s = format_coffee_hub_e_line("grace-mar")
    assert "Conductor is standalone" in s
    assert "**E" not in s
    assert "bernstein" in s

def test_illustration_three_kleiber_repetition():
    events = [
        _pick(_ts(day=1, hour=9), conductor="kleiber"),
        _pick(_ts(day=1, hour=10), conductor="kleiber"),
        _pick(_ts(day=1, hour=11), conductor="kleiber"),
    ]
    assert conductor_for_d1_continuation(events) == "kleiber"
    assert last_logged_conductor(events) == "kleiber"
    assert last_coffee_pick_conductor_event(events)["kv"]["conductor"] == "kleiber"

def test_illustration_rotation_tracks_newest():
    events = [
        _pick(_ts(day=1, hour=8), conductor="kleiber"),
        _pick(_ts(day=2, hour=9), conductor="karajan"),
        _pick(_ts(day=2, hour=10), conductor="karajan"),
    ]
    assert conductor_for_d1_continuation(events) == "karajan"

def test_illustration_d2_abc_map():
    assert d2_conductor_from_menu_recommendation("A") == "kleiber"
    assert d2_conductor_from_menu_recommendation("B") == "toscanini"
    assert d2_conductor_from_menu_recommendation("C") == "bernstein"
    assert d2_conductor_from_menu_recommendation("Z") == "furtwangler"

def test_illustration_orthogonal_d1_kleiber_d2_bernstein():
    """Last pick can be Kleiber while the helper recommendation points elsewhere."""
    events = [_pick(_ts(), conductor="kleiber")]
    assert conductor_for_d1_continuation(events) == "kleiber"
    d2 = d2_conductor_resolved(
        dream=None,
        assess={"recommended": "C", "line": "Session load: … (recommended: C)"},
    )
    assert d2 == "bernstein"
    assert system_recommended_menu_pick(assess={"recommended": "C"}) == "D"

def test_illustration_focus_tracks_like_conductor():
    events = [
        _pick(_ts(day=1, hour=8), focus="ritter-april", conductor="kleiber"),
        _pick(_ts(day=2, hour=9), focus="mercouris", conductor="kleiber"),
    ]
    assert focus_for_d1_continuation(events) == "mercouris"

def test_illustration_dream_worktree_seam_overrides_assess_b():
    dream = {"worktreeAdvice": "merge conflict risk on feature seam"}
    assess = {"recommended": "B"}
    assert d2_conductor_resolved(dream=dream, assess=assess) == "toscanini"
    assert d2_conductor_from_assess_load(assess) == "toscanini"
    assert system_recommended_menu_pick(dream=dream, assess=assess) == "D"

def test_illustration_dream_tomorrow_inherits_kleiber():
    assert (
        d2_conductor_resolved(
            dream={"tomorrow_inherits": "Carry: daily brief"},
            assess={"recommended": "C"},
        )
        == "kleiber"
    )

def test_illustration_dream_long_arc_hint_prefers_karajan():
    dream = {"summary": "Shape the month arc and rebalance the meta architecture."}
    assert d2_conductor_resolved(dream=dream, assess={"recommended": "C"}) == "karajan"
    assert system_recommended_menu_pick(dream=dream, assess={"recommended": "C"}) == "D"

def test_illustration_outcome_parsed_from_snippet(tmp_path):
    user = "grace-mar"
    log = tmp_path / "work-cadence-events.md"
    log.write_text(
        "# Cadence events\n\n_(Append below this line.)_\n"
        f"- **2026-04-20 12:00 UTC** — coffee_pick ({user}) ok=true picked=D5 conductor=kleiber\n"
        f"- **2026-04-20 12:30 UTC** — coffee_conductor_outcome ({user}) ok=true verdict=promote\n",
        encoding="utf-8",
    )
    events = parse_events(user, events_path=log)
    kinds = [e["kind"] for e in events]
    assert "coffee_conductor_outcome" in kinds
    outcomes = [e for e in events if e["kind"] == "coffee_conductor_outcome"]
    assert outcomes[-1]["kv"].get("verdict") == "promote"

def test_last_logged_conductor_accepts_new_conductor_pick_shape() -> None:
    events = [_pick(_ts(), picked="conductor", conductor="karajan")]
    assert last_logged_conductor(events) == "karajan"

def test_last_logged_conductor_accepts_hub_e_with_conductor() -> None:
    events = [_pick(_ts(), picked="E", conductor="bernstein")]
    assert last_logged_conductor(events) == "bernstein"

def test_active_conductor_arc_requires_unclosed_pick() -> None:
    events = [
        _pick(_ts(day=1, hour=8), picked="conductor", conductor="kleiber", focus="front-door"),
        {
            "dt": _ts(day=1, hour=8, minute=5),
            "kind": "coffee_conductor_outcome",
            "user": "grace-mar",
            "kv": {"conductor": "kleiber", "verdict": "watch", "falsify": "stay-narrow"},
            "line": "",
        },
    ]
    active = active_conductor_arc(events)
    assert active is not None
    assert active["conductor"] == "kleiber"
    assert active["focus"] == "front-door"
    assert active["outcome_count"] == 1

def test_active_conductor_arc_clears_after_closed_coffee_close() -> None:
    events = [
        _pick(_ts(day=1, hour=8), picked="conductor", conductor="karajan"),
        {
            "dt": _ts(day=1, hour=8, minute=10),
            "kind": "coffee_close",
            "user": "grace-mar",
            "kv": {"conductor": "karajan", "conductor_state": "closed"},
            "line": "",
        },
    ]
    assert active_conductor_arc(events) is None

def test_resolve_active_conductor_movement_uses_latest_open_arc() -> None:
    events = [
        _pick(_ts(day=1, hour=8), picked="conductor", conductor="toscanini"),
        _pick(_ts(day=1, hour=9), picked="conductor", conductor="bernstein"),
    ]
    resolved = resolve_active_conductor_movement("b", events)
    assert resolved == {
        "conductor": "bernstein",
        "movement": "B",
        "source": "active_conductor_arc",
        "focus": None,
        "arc": None,
        "picked_at": _ts(day=1, hour=9),
        "outcome_count": 0,
    }

def test_resolve_active_conductor_movement_returns_none_without_active_arc() -> None:
    events = [
        _pick(_ts(day=1, hour=8), picked="conductor", conductor="kleiber"),
        {
            "dt": _ts(day=1, hour=8, minute=20),
            "kind": "coffee_close",
            "user": "grace-mar",
            "kv": {"conductor": "kleiber", "conductor_state": "closed"},
            "line": "",
        },
    ]
    assert resolve_active_conductor_movement("d", events) is None

def test_closed_arc_stays_dead_after_later_unattributed_outcome() -> None:
    events = [
        _pick(_ts(day=1, hour=8), picked="conductor", conductor="kleiber", focus="comment-lab"),
        {
            "dt": _ts(day=1, hour=8, minute=5),
            "kind": "coffee_conductor_outcome",
            "user": "grace-mar",
            "kv": {"conductor": "kleiber", "verdict": "tighten", "falsify": "no clear membrane"},
            "line": "",
        },
        {
            "dt": _ts(day=1, hour=8, minute=10),
            "kind": "coffee_close",
            "user": "grace-mar",
            "kv": {"conductor": "kleiber", "conductor_state": "closed", "outcome": "done"},
            "line": "",
        },
        {
            "dt": _ts(day=1, hour=9),
            "kind": "coffee_conductor_outcome",
            "user": "grace-mar",
            "kv": {"verdict": "stray-note"},
            "line": "",
        },
    ]
    assert active_conductor_arc(events) is None
    assert resolve_active_conductor_movement("b", events) is None

def test_compiled_shortcut_helpers_are_conservative() -> None:
    events = [
        _pick(_ts(day=1, hour=8), picked="conductor", conductor="karajan"),
        {
            "dt": _ts(day=1, hour=8, minute=10),
            "kind": "coffee_conductor_outcome",
            "user": "grace-mar",
            "kv": {"conductor": "karajan", "verdict": "watch"},
            "line": "",
        },
        _pick(_ts(day=2, hour=8), picked="conductor", conductor="karajan"),
        {
            "dt": _ts(day=2, hour=8, minute=10),
            "kind": "coffee_conductor_outcome",
            "user": "grace-mar",
            "kv": {"conductor": "karajan", "verdict": "hold"},
            "line": "",
        },
    ]
    assert compiled_shortcut_for_conductor("karajan") == "karajan-review"
    assert should_offer_compiled_shortcut(events, "karajan") is True
    assert should_offer_compiled_shortcut(events, "bernstein") is False

