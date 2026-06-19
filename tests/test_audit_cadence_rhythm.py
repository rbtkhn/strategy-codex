"""Tests for conductor-aware cadence auditing."""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from audit_cadence_rhythm import (
    compute_coffee_recursion_summary,
    compute_conductor_audit,
    compute_rhythm_summary,
    format_conductor_audit,
    format_summary,
    parse_events,
)


def _write_events(path: Path, body: str) -> Path:
    path.write_text(body, encoding="utf-8")
    return path


def test_conductor_audit_counts_explicit_and_inferred_paths(tmp_path: Path) -> None:
    events = _write_events(
        tmp_path / "cadence.md",
        """# Cadence events

_(Append below this line.)_
- **2026-05-01 10:00 UTC** â€” coffee_pick (grace-mar) ok=true picked=conductor conductor=karajan
- **2026-05-01 10:05 UTC** â€” coffee_conductor_outcome (grace-mar) ok=true verdict=watch conductor=karajan notebook_ref=docs/a.md falsify=stay-narrow
- **2026-05-01 11:00 UTC** â€” coffee_pick (grace-mar) ok=true picked=E conductor=bernstein
- **2026-05-01 11:05 UTC** â€” coffee_conductor_outcome (grace-mar) ok=true verdict=watch falsify=needs-public-stakes
- **2026-05-01 12:00 UTC** â€” coffee_pick (grace-mar) ok=true picked=E
- **2026-05-01 12:30 UTC** â€” coffee_conductor_outcome (grace-mar) ok=true verdict=watch
""",
    )
    summary = compute_conductor_audit(
        "grace-mar",
        days=7,
        events_path=events,
        now=datetime(2026, 5, 3, 0, 0, tzinfo=timezone.utc),
    )
    assert summary["explicit_pick_count"] == 2
    assert summary["explicit_picks_by_conductor"]["karajan"] == 1
    assert summary["explicit_picks_by_conductor"]["bernstein"] == 1
    assert summary["explicit_outcomes_by_conductor"]["karajan"] == 1
    assert summary["inferred_outcomes_by_conductor"]["bernstein"] == 1
    assert summary["closure"]["unattributed_outcomes"] == 1
    assert summary["closure"]["total_closed"] == 2
    assert summary["closure"]["open_pick_count"] == 0


def test_conductor_audit_tracks_open_picks_and_legacy_partial(tmp_path: Path) -> None:
    events = _write_events(
        tmp_path / "cadence.md",
        """# Cadence events

_(Append below this line.)_
- **2026-05-01 10:00 UTC** â€” coffee_pick (grace-mar) ok=true conductor=kleiber
- **2026-05-01 10:10 UTC** â€” coffee_pick (grace-mar) ok=true picked=conductor conductor=toscanini
""",
    )
    summary = compute_conductor_audit(
        "grace-mar",
        days=7,
        events_path=events,
        now=datetime(2026, 5, 3, 0, 0, tzinfo=timezone.utc),
    )
    assert summary["legacy_partial_picks_by_conductor"]["kleiber"] == 1
    assert summary["explicit_pick_count"] == 1
    assert summary["closure"]["open_pick_count"] == 1
    assert summary["open_picks"][0]["conductor"] == "toscanini"


def test_conductor_audit_evidence_richness_and_format(tmp_path: Path) -> None:
    events = _write_events(
        tmp_path / "cadence.md",
        """# Cadence events

_(Append below this line.)_
- **2026-05-01 10:00 UTC** â€” coffee_pick (grace-mar) ok=true picked=conductor conductor=kleiber
- **2026-05-01 10:05 UTC** â€” coffee_conductor_outcome (grace-mar) ok=true verdict=watch conductor=kleiber action=trim falsify=one-test notebook_ref=docs/x.md
""",
    )
    summary = compute_conductor_audit(
        "grace-mar",
        days=7,
        events_path=events,
        now=datetime(2026, 5, 3, 0, 0, tzinfo=timezone.utc),
    )
    assert summary["evidence_richness"] == {
        "verdict": 1,
        "action": 1,
        "notebook_ref": 1,
        "falsify": 1,
    }
    text = format_conductor_audit(summary)
    assert "5-conductor audit" in text
    assert (
        "kleiber: picks=1 explicit_outcomes=1 inferred_outcomes=0 coffee_closes=0 "
        "legacy_partial=0"
    ) in text


def test_conductor_audit_preserves_multiword_falsify_value(tmp_path: Path) -> None:
    events = _write_events(
        tmp_path / "cadence.md",
        """# Cadence events

_(Append below this line.)_
- **2026-05-01 10:00 UTC** — coffee_pick (grace-mar) ok=true picked=conductor conductor=karajan
- **2026-05-01 10:05 UTC** — coffee_conductor_outcome (grace-mar) ok=true verdict=watch conductor=karajan notebook_ref=docs/a.md falsify=If the accumulator date changes on refresh, the read was stale.
""",
    )
    parsed = parse_events("grace-mar", events_path=events)

    assert parsed[1]["kv"]["falsify"] == (
        "If the accumulator date changes on refresh, the read was stale."
    )


def test_coffee_recursion_summary_tracks_repeated_unresolved_loops_and_artifacts(
    tmp_path: Path,
) -> None:
    events = _write_events(
        tmp_path / "cadence.md",
        """# Cadence events

_(Append below this line.)_
- **2026-05-01 10:00 UTC** — coffee_close (strategy-codex) ok=true picked=B outcome=partial readiness=execution_ready artifacts=scripts/a.py,tests/test_a.py loops=materialization-stub,next-action next=run-tests
- **2026-05-01 11:00 UTC** — coffee_close (strategy-codex) ok=true picked=C outcome=blocked readiness=blocked artifacts=docs/x.md loops=materialization-stub next=repair-fetch
- **2026-05-01 12:00 UTC** — coffee_close (strategy-codex) ok=true picked=A outcome=done readiness=ship_ready artifacts=commit:abc1234 loops=materialization-stub next=push
""",
    )

    summary = compute_coffee_recursion_summary(
        "strategy-codex",
        days=7,
        events_path=events,
        now=datetime(2026, 5, 3, 0, 0, tzinfo=timezone.utc),
    )

    assert summary["close_count"] == 3
    assert summary["last_close"]["readiness"] == "ship_ready"
    assert summary["last_close"]["runtime/artifacts"] == ["commit:abc1234"]
    assert summary["artifact_counts"]["scripts/a.py"] == 1
    assert summary["artifact_counts"]["tests/test_a.py"] == 1
    assert summary["repeated_unresolved_loops"] == [
        {"loop": "materialization-stub", "count": 2}
    ]


def test_rhythm_summary_reports_last_close_separately_from_orientation(tmp_path: Path) -> None:
    events = _write_events(
        tmp_path / "cadence.md",
        """# Cadence events

_(Append below this line.)_
- **2026-05-01 09:00 UTC** — coffee (strategy-codex) ok=true mode=work-start
- **2026-05-01 09:30 UTC** — coffee_close (strategy-codex) ok=true picked=B outcome=partial readiness=execution_ready artifacts=scripts/a.py loops=coffee-close next=tests
""",
    )

    summary = compute_rhythm_summary(
        "strategy-codex",
        days=7,
        events_path=events,
        now=datetime(2026, 5, 3, 0, 0, tzinfo=timezone.utc),
    )
    text = format_summary(summary)

    assert summary["coffee"]["count"] == 1
    assert summary["coffee"]["close_count"] == 1
    assert summary["coffee_recursion"]["last_close"]["readiness"] == "execution_ready"
    assert "coffee close: picked=B outcome=partial readiness=execution_ready" in text


def test_conductor_audit_uses_coffee_close_closed_without_double_counting_outcomes(
    tmp_path: Path,
) -> None:
    events = _write_events(
        tmp_path / "cadence.md",
        """# Cadence events

_(Append below this line.)_
- **2026-05-01 10:00 UTC** — coffee_pick (strategy-codex) ok=true picked=conductor conductor=kleiber
- **2026-05-01 10:30 UTC** — coffee_close (strategy-codex) ok=true picked=conductor outcome=done readiness=ship_ready conductor=kleiber conductor_state=closed artifacts=commit:abc1234 loops=benchmark next=dream
""",
    )

    summary = compute_conductor_audit(
        "strategy-codex",
        days=7,
        events_path=events,
        now=datetime(2026, 5, 3, 0, 0, tzinfo=timezone.utc),
    )

    assert summary["explicit_outcome_count"] == 0
    assert summary["closure"]["coffee_close_closed"] == 1
    assert summary["closure"]["total_closed"] == 1
    assert summary["closure"]["open_pick_count"] == 0
    assert summary["coffee_close_closes_by_conductor"]["kleiber"] == 1

    recursion = compute_coffee_recursion_summary(
        "strategy-codex",
        days=7,
        events_path=events,
        now=datetime(2026, 5, 3, 0, 0, tzinfo=timezone.utc),
    )
    assert recursion["latest_conductor_state"] == {
        "ts": "2026-05-01T10:30:00+00:00",
        "conductor": "kleiber",
        "state": "closed",
        "source": "coffee_close",
    }
