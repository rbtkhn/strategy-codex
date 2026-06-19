"""Tests for dream coffee rollup and related handoff helpers."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

from dream_coffee_rollup import (
    build_last_coffee_echo,
    parse_coffee_cadence_lines,
    rollup_coffee_24h,
    rollup_conductor_24h,
    rollup_conductor_window,
    rollup_object_closes_24h,
    rollup_work_pass_24h,
)
from dream_civmem_echoes import (
    ANALOGY_CANDIDATE_LABEL,
    CIVMEM_DISCLAIMER,
    build_civmem_query_from_digest,
    compute_civmem_echoes,
    excerpt_self_memory_short_term,
)
from dream_execution_paths import build_execution_paths


def test_parse_coffee_cadence_lines_filters_user_and_window() -> None:
    md = """
_(Append below this line.)_
- **2026-04-02 10:00 UTC** — coffee (grace-mar) ok=true mode=work-start
- **2026-04-02 11:00 UTC** — coffee (other-user) ok=true mode=work-start
- **2026-04-02 12:00 UTC** — coffee (grace-mar) ok=false mode=closeout
- **2026-04-01 09:00 UTC** — coffee (grace-mar) ok=true mode=minimal
"""
    ws = datetime(2026, 4, 2, 9, 0, tzinfo=timezone.utc)
    we = datetime(2026, 4, 2, 15, 0, tzinfo=timezone.utc)
    runs = parse_coffee_cadence_lines(md, user_id="grace-mar", window_start=ws, window_end=we)
    assert len(runs) == 2
    assert runs[0]["mode"] == "work-start"
    assert runs[0]["ok"] is True
    assert runs[1]["mode"] == "closeout"
    assert runs[1]["ok"] is False


def test_rollup_coffee_24h_counts_modes(tmp_path: Path) -> None:
    md = """- **2026-04-02 14:00 UTC** — coffee (grace-mar) ok=true mode=work-start
- **2026-04-02 15:00 UTC** — coffee (grace-mar) ok=true mode=light
"""
    p = tmp_path / "cadence.md"
    p.write_text(md, encoding="utf-8")
    now = datetime(2026, 4, 2, 16, 0, tzinfo=timezone.utc)
    r = rollup_coffee_24h(user_id="grace-mar", now_utc=now, events_path=p, max_runs=20)
    assert r["count"] == 2
    assert r["by_mode"]["work-start"] == 1
    assert r["by_mode"]["light"] == 1
    assert r["first_ts"] is not None
    assert r["span_hours"] is not None


def test_rollup_missing_file_note() -> None:
    p = Path(__file__).resolve().parent / "nonexistent_cadence_xyz.md"
    r = rollup_coffee_24h(user_id="grace-mar", events_path=p)
    assert r["count"] == 0
    assert r["note"] == "no cadence file"


def test_rollup_conductor_24h_pairs_outcomes_with_active_master(tmp_path: Path) -> None:
    md = """- **2026-04-02 14:00 UTC** â€” coffee_pick (grace-mar) ok=true picked=conductor conductor=furtwangler
- **2026-04-02 14:05 UTC** â€” coffee_conductor_outcome (grace-mar) ok=true falsify=redesign-not-patch
- **2026-04-02 14:10 UTC** â€” coffee_pick (grace-mar) ok=true picked=conductor conductor=bernstein
- **2026-04-02 14:15 UTC** â€” coffee_conductor_outcome (grace-mar) ok=true verdict=no_action
"""
    p = tmp_path / "cadence.md"
    p.write_text(md, encoding="utf-8")
    now = datetime(2026, 4, 2, 16, 0, tzinfo=timezone.utc)
    r = rollup_conductor_24h(user_id="grace-mar", now_utc=now, events_path=p)
    assert r["pick_count"] == 2
    assert r["outcome_count"] == 2
    assert r["completed_passes"] == 1
    assert r["off_menu_refusals"] == 1
    assert r["last_master"] == "bernstein"
    assert r["last_outcome"]["conductor"] == "bernstein"
    assert "bernstein" in r["echo"]
    assert "notebook_ref_count" not in r
    assert "falsify_count" not in r
    assert "falsifiers" not in r
    assert "open_arcs" not in r
    assert "recent_closed" not in r


def test_rollup_conductor_window_keeps_open_arcs_and_notebook_counts(tmp_path: Path) -> None:
    md = """- **2026-04-02 14:00 UTC** â€” coffee_pick (grace-mar) ok=true picked=conductor conductor=kleiber
- **2026-04-02 14:05 UTC** â€” coffee_conductor_outcome (grace-mar) ok=true conductor=kleiber verdict=watch notebook_ref=docs/x.md falsify=stay-narrow
- **2026-04-02 15:00 UTC** â€” coffee_pick (grace-mar) ok=true picked=conductor conductor=karajan focus=month-arc
"""
    p = tmp_path / "cadence.md"
    p.write_text(md, encoding="utf-8")
    now = datetime(2026, 4, 2, 16, 0, tzinfo=timezone.utc)
    r = rollup_conductor_window(user_id="grace-mar", now_utc=now, events_path=p, window_hours=72)
    assert r["pick_count"] == 2
    assert r["outcome_count"] == 1
    assert r["notebook_ref_count"] == 1
    assert r["falsify_count"] == 1
    assert r["open_arcs"] == [
        {"conductor": "karajan", "ts_iso": "2026-04-02T15:00:00+00:00", "menu_label": "conductor"}
    ]


def test_malformed_line_skipped() -> None:
    md = """- **2026-04-02 10:00 UTC** — coffee (grace-mar) ok=true mode=work-start
not a valid line
- **2026-04-02 11:00 UTC** — bridge (grace-mar) ok=true
"""
    ws = datetime(2026, 4, 2, 9, 0, tzinfo=timezone.utc)
    we = datetime(2026, 4, 2, 15, 0, tzinfo=timezone.utc)
    runs = parse_coffee_cadence_lines(md, user_id="grace-mar", window_start=ws, window_end=we)
    assert len(runs) == 1


def test_rollup_work_pass_24h_prefers_coffee_close(tmp_path: Path) -> None:
    md = """- **2026-04-02 14:00 UTC** — coffee_pick (strategy-codex) ok=true picked=D
- **2026-04-02 14:05 UTC** — coffee_close (strategy-codex) ok=true picked=D outcome=partial readiness=execution_ready object_ref=statecraft/daily/2026-06-17.md falsify=pseudo-gate-J16 verdict=shaped attention=one object only
"""
    p = tmp_path / "cadence.md"
    p.write_text(md, encoding="utf-8")
    now = datetime(2026, 4, 2, 16, 0, tzinfo=timezone.utc)
    r = rollup_work_pass_24h(user_id="strategy-codex", now_utc=now, events_path=p)
    assert r["source"] == "coffee_close"
    assert r["close_count"] == 1
    assert r["substantive_count"] == 1
    assert r["last_object_ref"] == "statecraft/daily/2026-06-17.md"
    assert r["last_attention"] == "one object only"


def test_rollup_conductor_24h_exposes_handoff_fields_only(tmp_path: Path) -> None:
    md = """- **2026-04-02 14:00 UTC** — coffee_pick (strategy-codex) ok=true picked=D
- **2026-04-02 14:05 UTC** — coffee_close (strategy-codex) ok=true picked=D outcome=done readiness=ship_ready object_ref=docs/x.md falsify=stay-narrow
"""
    p = tmp_path / "cadence.md"
    p.write_text(md, encoding="utf-8")
    now = datetime(2026, 4, 2, 16, 0, tzinfo=timezone.utc)
    r = rollup_conductor_24h(user_id="strategy-codex", now_utc=now, events_path=p)
    assert sorted(r.keys()) == [
        "completed_passes",
        "echo",
        "last_master",
        "last_outcome",
        "note",
        "off_menu_refusals",
        "orientation_only",
        "outcome_count",
        "pick_count",
        "window_end_utc",
        "window_hours",
        "window_start_utc",
    ]


def test_excerpt_self_memory_short_term() -> None:
    text = "## Short-term\n\nhello world\nmore\n\n## Medium-term\n\nx"
    ex = excerpt_self_memory_short_term(text, max_chars=100)
    assert "hello" in ex
    assert "Medium-term" not in ex


def test_build_civmem_query_from_digest_skips_reinforcement() -> None:
    d = {
        "entries": [
            {"title": "Alpha", "summary": "one", "relationship_type": "reinforcement"},
            {"title": "Beta", "summary": "two", "relationship_type": "contradiction", "why_flagged": ["x"]},
        ]
    }
    q = build_civmem_query_from_digest(d, max_chars=500)
    assert "Beta" in q
    assert "Alpha" not in q


def test_compute_civmem_echoes_index_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    import dream_civmem_echoes as dce

    monkeypatch.setattr(dce, "CIVMEM_INDEX_PATH", Path("/nonexistent/inrepo_index.json"))
    echoes, missing = compute_civmem_echoes(
        digest={"entries": [{"title": "t", "summary": "s", "relationship_type": "duplicate"}]},
        self_memory_text="",
    )
    assert missing is True
    assert echoes == []


def test_build_execution_paths_heavy_reentry_prefers_reframe() -> None:
    now = datetime(2026, 1, 1, 22, 0, tzinfo=timezone.utc)
    paths, idx, reason = build_execution_paths(
        user_id="grace-mar",
        now_utc=now,
        integrity_ok=True,
        governance_ok=True,
        reviewable_count=0,
        contradiction_count=0,
        coffee_count_24h=10,
    )
    assert [p["id"] for p in paths] == ["confirm", "test", "deepen", "reframe"]
    assert idx == 3
    assert reason == "reentry_heavy"


def test_build_execution_paths_integrity_fail() -> None:
    paths, idx, reason = build_execution_paths(
        user_id="grace-mar",
        now_utc=datetime(2026, 6, 15, 12, 0, tzinfo=timezone.utc),
        integrity_ok=False,
        governance_ok=True,
        reviewable_count=0,
        contradiction_count=0,
        coffee_count_24h=0,
    )
    assert idx == 1
    assert reason == "integrity_or_governance_pressure"


def test_build_execution_paths_gate_backlog_forces_reframe() -> None:
    paths, idx, reason = build_execution_paths(
        user_id="grace-mar",
        now_utc=datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc),
        integrity_ok=True,
        governance_ok=True,
        reviewable_count=0,
        contradiction_count=0,
        coffee_count_24h=0,
        gate_pending_count=20,
        max_pending_candidates=12,
    )
    assert paths[3]["id"] == "reframe"
    assert idx == 3
    assert reason == "gate_backlog"


def test_parse_coffee_pick_in_rollup(tmp_path: Path) -> None:
    md = """- **2026-04-02 14:00 UTC** — coffee (grace-mar) ok=true mode=work-start
- **2026-04-02 14:05 UTC** — coffee_pick (grace-mar) ok=true picked=E steward=gate
- **2026-04-02 15:00 UTC** — coffee_pick (grace-mar) ok=true picked=A
- **2026-04-02 15:05 UTC** — coffee_pick (grace-mar) ok=true picked=conductor conductor=kleiber
"""
    p = tmp_path / "cadence.md"
    p.write_text(md, encoding="utf-8")
    now = datetime(2026, 4, 2, 16, 0, tzinfo=timezone.utc)
    r = rollup_coffee_24h(user_id="grace-mar", now_utc=now, events_path=p)
    assert r["by_picked"]["E"] == 1
    assert r["by_picked"]["A"] == 1
    assert r["by_picked"]["conductor"] == 1
    assert len(r["picks"]) == 3
    assert r["picks"][-1].get("picked") == "conductor"
    assert r["picks"][-1].get("conductor") == "kleiber"


def test_last_coffee_echo_sees_new_style_conductor_pick(tmp_path: Path) -> None:
    md = """- **2026-04-02 14:00 UTC** — coffee (grace-mar) ok=true mode=work-start
- **2026-04-02 14:05 UTC** — coffee_pick (grace-mar) ok=true picked=conductor conductor=bernstein
"""
    p = tmp_path / "cadence.md"
    p.write_text(md, encoding="utf-8")
    now = datetime(2026, 4, 2, 16, 0, tzinfo=timezone.utc)

    echo = build_last_coffee_echo(rollup_coffee_24h(user_id="grace-mar", now_utc=now, events_path=p))

    assert echo is not None
    assert echo["menu_letter"] == "conductor"
    assert echo["conductor"] == "bernstein"
    assert "Conductor line: bernstein." in echo["highlight"]


def test_build_last_coffee_echo_none_without_runs() -> None:
    assert build_last_coffee_echo({"count": 0, "runs": [], "picks": []}) is None


def test_build_last_coffee_echo_cap_and_source() -> None:
    rollup = {
        "count": 1,
        "last_ts": "2026-04-23T10:00:00+00:00",
        "runs": [
            {
                "ts_iso": "2026-04-23T10:00:00+00:00",
                "mode": "work-start",
                "kv": {},
            }
        ],
        "picks": [
            {
                "ts_iso": "2026-04-23T10:01:00+00:00",
                "picked": "B",
                "menu_label": "B",
                "conductor": "kleiber",
            }
        ],
    }
    e = build_last_coffee_echo(rollup)
    assert e is not None
    assert e["source"] == "coffee_rollup_24h"
    assert e["conductor"] == "kleiber"
    assert e["mode"] == "work-start"
    assert len(e["highlight"]) <= 160


def test_compute_civmem_echoes_default_limit_one(monkeypatch: pytest.MonkeyPatch) -> None:
    """Default limit=1 returns at most one echo (plan matrix E)."""
    import build_civmem_inrepo_index as bcii
    import dream_civmem_echoes as dce_mod

    def fake_query(_q: str, *, limit: int = 3):
        return [
            {"path": "a.md", "overlap": 6, "snippet": "one"},
            {"path": "b.md", "overlap": 5, "snippet": "two"},
            {"path": "c.md", "overlap": 4, "snippet": "three"},
        ]

    monkeypatch.setattr(dce_mod, "CIVMEM_INDEX_PATH", Path(__file__))
    monkeypatch.setattr(bcii, "query_inrepo_civmem", fake_query)
    echoes, missing = compute_civmem_echoes(
        digest={"entries": [{"title": "t", "summary": "s", "relationship_type": "duplicate"}]},
        self_memory_text="",
    )
    assert missing is False
    assert len(echoes) == 1
    assert echoes[0]["path"] == "a.md"


def test_compute_civmem_echoes_filters_min_overlap(monkeypatch: pytest.MonkeyPatch) -> None:
    import build_civmem_inrepo_index as bcii
    import dream_civmem_echoes as dce_mod

    def fake_query(_q: str, *, limit: int = 3):
        return [
            {"path": "x.md", "overlap": 2, "snippet": "low"},
            {"path": "y.md", "overlap": 5, "snippet": "high enough"},
        ]

    monkeypatch.setattr(dce_mod, "CIVMEM_INDEX_PATH", Path(__file__))
    monkeypatch.setattr(bcii, "query_inrepo_civmem", fake_query)
    echoes, missing = compute_civmem_echoes(
        digest={"entries": [{"title": "t", "summary": "s", "relationship_type": "duplicate"}]},
        self_memory_text="",
        min_overlap=4,
        limit=3,
    )
    assert missing is False
    assert len(echoes) == 1
    assert echoes[0]["path"] == "y.md"
    assert echoes[0]["analogy_label"] == ANALOGY_CANDIDATE_LABEL


def test_civmem_disclaimer_nonempty() -> None:
    assert "Record" in CIVMEM_DISCLAIMER


def test_rollup_object_closes_24h_echoes_last_anchor(tmp_path: Path) -> None:
    md = """- **2026-04-02 14:00 UTC** — coffee_close (strategy-codex) ok=true picked=D outcome=partial readiness=execution_ready object_ref=statecraft/daily/2026-06-17.md falsify=pseudo-gate-J16 verdict=shaped
- **2026-04-02 15:00 UTC** — coffee_close (strategy-codex) ok=true picked=A outcome=done readiness=ship_ready
"""
    p = tmp_path / "cadence.md"
    p.write_text(md, encoding="utf-8")
    now = datetime(2026, 4, 2, 16, 0, tzinfo=timezone.utc)
    r = rollup_object_closes_24h(user_id="strategy-codex", now_utc=now, events_path=p)
    assert r["close_count"] == 2
    assert r["object_ref_count"] == 1
    assert r["falsify_count"] == 1
    assert r["last_object_ref"] == "statecraft/daily/2026-06-17.md"
    assert r["last_falsify"] == "pseudo-gate-J16"
    assert "object=statecraft/daily/2026-06-17.md" in (r["echo"] or "")

