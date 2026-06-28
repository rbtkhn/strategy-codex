"""Tests for scripts/statecraft_war_room.py."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import statecraft_intake_queue as intake_queue  # noqa: E402
from statecraft_war_room import (  # noqa: E402
    RouterEntry,
    build_json_payload,
    build_markdown,
    build_war_room_context,
    classify_transaction_fit,
    extract_daily_objects,
    main,
    parse_transaction_router,
)

FIXTURE_ROUTER = """\
# Transaction Router (fixture)

## Router Index

| Transaction object | Crisis object | Use when | Primary lanes | Settlement spine | Entropy signal | Recursive utility |
| --- | --- | --- | --- | --- | --- | --- |
| [Hormuz Transit / Sanctions Relief Compact](../notes/compacts/hormuz-transit-sanctions-relief-compact/) | Chokepoint transit, insurance, sanctions relief, escorted passage | Hormuz shipping, oil-flow, sanctions, insurance, or escort risk becomes the bargaining object | America, Russia, China, Iran | Transit security | Chokepoint leverage | Restraint-for-relief |
| [Iran Nuclear Latency Recognition Framework](../notes/compacts/iran-nuclear-latency-recognition-framework/) | Nuclear threshold capability, inspection, recognition, sanctions triggers | Iran enrichment breakout inspection threshold status crisis | America, Russia, China, Iran | Recognize latency | Ambiguity panic | Restraint observable |
"""


def _write_archive(path: Path) -> None:
    day = path.stem[-10:]
    path.write_text(
        "\n".join(
            [
                "---",
                f"pub_date: '{day}'",
                "kind: transcript",
                "source_form: interview",
                "thread: marandi",
                "threads:",
                "  - marandi",
                "host_people:",
                "  - Glenn Diesen",
                "guest_people:",
                "  - Seyed M. Marandi",
                "source_url: https://example.com/watch",
                "---",
                "# Body",
                "",
            ]
        ),
        encoding="utf-8",
    )


def _setup_fixture_repo(tmp_path: Path, day: str) -> dict[str, Path]:
    archive_root = tmp_path / "source-archive" / "statecraft"
    day_dir = archive_root / day
    day_dir.mkdir(parents=True)
    slug = f"source-war-room-test-{day}.md"
    source = day_dir / slug
    _write_archive(source)

    daily_dir = tmp_path / "statecraft" / "synthesis" / "day"
    daily_dir.mkdir(parents=True)
    daily_path = daily_dir / f"{day}.md"
    daily_path.write_text(
        "\n".join(
            [
                f"# State Synthesis — {day}",
                "",
                "## Executive Read",
                "",
                "Dominant object — **Hormuz chokepoint transit insurance sanctions relief**.",
                "",
                f"Archive checkpoint: **1** source-bearing captures.",
                f"- [War room test](../../source-archive/statecraft/{day}/{slug})",
                "",
            ]
        ),
        encoding="utf-8",
    )

    sheets_dir = tmp_path / "statecraft" / "sheets"
    sheets_dir.mkdir(parents=True)
    router_path = sheets_dir / "instrument-router.md"
    router_path.write_text(FIXTURE_ROUTER, encoding="utf-8")

    queue_root = tmp_path / "runtime" / "artifacts" / "statecraft-intake-queue"
    queue_day = queue_root / day
    queue_day.mkdir(parents=True)
    sidecar_path = queue_day / f"{slug[:-3]}.v1.json"
    sidecar_path.write_text(
        json.dumps(
            {
                "schema_version": "statecraft-intake-sidecar.v1",
                "source_path": f"source-archive/statecraft/{day}/{slug}",
                "synthesis_status": "queued",
                "strategic_relevance": "high",
                "transaction_candidate": True,
                "regions": ["Persia"],
                "mechanisms": ["sanctions", "transit"],
                "non_canonical": True,
            }
        ),
        encoding="utf-8",
    )

    transactions_dir = tmp_path / "statecraft" / "transactions"
    transactions_dir.mkdir(parents=True, exist_ok=True)

    return {
        "archive_root": archive_root,
        "daily_dir": daily_dir,
        "daily_path": daily_path,
        "router_path": router_path,
        "queue_root": queue_root,
        "source": source,
        "transactions_dir": transactions_dir,
    }


@pytest.fixture()
def war_room_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    day = "2026-06-25"
    paths = _setup_fixture_repo(tmp_path, day)
    monkeypatch.setattr(intake_queue, "QUEUE_ROOT", paths["queue_root"])
    monkeypatch.setattr("statecraft_war_room.QUEUE_ROOT", paths["queue_root"])
    return tmp_path, day, paths


def test_generates_report_from_fixture_daily_and_sidecar(war_room_env) -> None:
    repo_root, day, _paths = war_room_env
    ctx = build_war_room_context(repo_root, pin_day=day, max_objects=12)
    md = build_markdown(ctx, generated_at="2099-01-01 00:00 UTC")
    assert "Mode: runtime / derived" in md
    assert "Authority: advisory only" in md
    assert len(ctx.objects) >= 1
    assert any("Hormuz" in o.name for o in ctx.objects)


def test_does_not_mutate_archive_or_daily(war_room_env) -> None:
    repo_root, day, paths = war_room_env
    source_before = paths["source"].read_text(encoding="utf-8")
    daily_before = paths["daily_path"].read_text(encoding="utf-8")
    build_war_room_context(repo_root, pin_day=day, max_objects=12)
    assert paths["source"].read_text(encoding="utf-8") == source_before
    assert paths["daily_path"].read_text(encoding="utf-8") == daily_before


def test_transaction_router_links(war_room_env) -> None:
    _repo_root, day, paths = war_room_env
    router = parse_transaction_router(paths["router_path"])
    daily_text = paths["daily_path"].read_text(encoding="utf-8")
    daily_text += (
        "\nSee [Hormuz framework]"
        "(../notes/compacts/hormuz-transit-sanctions-relief-compact/).\n"
    )
    paths["daily_path"].write_text(daily_text, encoding="utf-8")
    objs = extract_daily_objects(paths["daily_path"], pub_date=day, router=router)
    assert objs
    assert objs[0].transaction_fit.kind == "exact"
    assert objs[0].transaction_fit.operator_confirm is True
    assert "hormuz-transit-sanctions-relief-compact" in (objs[0].transaction_fit.transaction_path or "")


def test_distinguishes_exact_near_none() -> None:
    router = parse_transaction_router(Path(__file__).parent / "_nonexistent_router.md")
    router = [
        RouterEntry(
            name="Hormuz Transit / Sanctions Relief Compact",
            crisis_object="Chokepoint transit, insurance, sanctions relief, escorted passage",
            use_when="Hormuz shipping, oil-flow, sanctions, insurance, or escort risk",
            primary_lanes="America, Iran",
            transaction_path="statecraft/notes/compacts/hormuz-transit-sanctions-relief-compact/",
        ),
        RouterEntry(
            name="Iran Nuclear Latency Recognition Framework",
            crisis_object="Nuclear threshold capability, inspection, recognition",
            use_when="Iran enrichment breakout inspection threshold",
            primary_lanes="America, Iran",
            transaction_path="statecraft/transactions/iran-nuclear-latency-recognition-framework/",
        ),
    ]

    exact_text = (
        "Hormuz chokepoint transit insurance sanctions relief escorted passage "
        "oil-flow shipping sanctions insurance escort risk bargaining object"
    )
    near_text = (
        "Hormuz shipping insurance sanctions relief on chokepoint transit "
        "with partial overlap but no explicit transaction link yet"
    )
    none_text = "Unrelated Baltic cable shadow fleet infrastructure damage only"

    exact = classify_transaction_fit(exact_text, router)
    near = classify_transaction_fit(near_text, router)
    none = classify_transaction_fit(none_text, router)

    assert exact.kind == "exact"
    assert exact.operator_confirm is True
    assert near.kind == "near"
    assert near.operator_confirm is True
    assert none.kind == "none"
    assert none.operator_confirm is False


def test_runtime_derived_authority_label(war_room_env) -> None:
    repo_root, day, _paths = war_room_env
    ctx = build_war_room_context(repo_root, pin_day=day, max_objects=12)
    md = build_markdown(ctx, generated_at="2099-01-01 00:00 UTC")
    payload = build_json_payload(ctx, generated_at="2099-01-01 00:00 UTC")
    assert "Mode: runtime / derived" in md
    assert payload["authority"] == "runtime_derived"


def test_handles_no_intake_sidecars_gracefully(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    day = "2026-06-26"
    archive_root = tmp_path / "source-archive" / "statecraft"
    day_dir = archive_root / day
    day_dir.mkdir(parents=True)
    _write_archive(day_dir / f"source-empty-queue-{day}.md")

    daily_dir = tmp_path / "statecraft" / "synthesis" / "day"
    daily_dir.mkdir(parents=True)
    (daily_dir / f"{day}.md").write_text(
        f"# State Synthesis — {day}\n\n## Executive Read\n\n**Standalone daily object headline.**\n",
        encoding="utf-8",
    )

    sheets_dir = tmp_path / "statecraft" / "sheets"
    sheets_dir.mkdir(parents=True)
    (sheets_dir / "transaction-router.md").write_text(FIXTURE_ROUTER, encoding="utf-8")

    queue_root = tmp_path / "runtime" / "artifacts" / "statecraft-intake-queue"
    monkeypatch.setattr(intake_queue, "QUEUE_ROOT", queue_root)
    monkeypatch.setattr("statecraft_war_room.QUEUE_ROOT", queue_root)

    ctx = build_war_room_context(tmp_path, pin_day=day, max_objects=12)
    md = build_markdown(ctx, generated_at="2099-01-01 00:00 UTC")
    assert "## 3. Intake Queue Watch" in md
    assert len(ctx.objects) >= 1


def test_json_schema_fields(war_room_env) -> None:
    repo_root, day, _paths = war_room_env
    ctx = build_war_room_context(repo_root, pin_day=day, max_objects=12)
    payload = build_json_payload(ctx, generated_at="2099-01-01 00:00 UTC")
    for key in (
        "generated_at",
        "authority",
        "latest_archive_day",
        "latest_daily_path",
        "sync_status",
        "active_objects",
    ):
        assert key in payload
    assert payload["active_objects"]
    obj = payload["active_objects"][0]
    for key in (
        "name",
        "lane",
        "lane_confidence",
        "source_floor",
        "transaction_fit",
        "status",
        "next_action",
        "falsifier",
    ):
        assert key in obj
    fit = obj["transaction_fit"]
    for key in ("kind", "transaction_path", "reason", "operator_confirm"):
        assert key in fit


def test_no_transaction_directory_creation(war_room_env, monkeypatch: pytest.MonkeyPatch) -> None:
    repo_root, day, paths = war_room_env
    before = {p.relative_to(paths["transactions_dir"]) for p in paths["transactions_dir"].rglob("*")}
    out = repo_root / "runtime" / "artifacts" / "statecraft-war-room" / "latest.md"
    json_out = repo_root / "runtime" / "artifacts" / "statecraft-war-room" / "latest.json"
    monkeypatch.setattr("statecraft_war_room.REPO_ROOT", repo_root)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "statecraft_war_room.py",
            "--out",
            str(out),
            "--json-out",
            str(json_out),
            "--day",
            day,
            "--max-objects",
            "12",
        ],
    )
    assert main() == 0
    after = {p.relative_to(paths["transactions_dir"]) for p in paths["transactions_dir"].rglob("*")}
    assert before == after
