"""Tests for event-registry validation."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"

if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from check_event_registry import check_registry, wire_stub_path  # noqa: E402
from prediction_lib import load_event_registry  # noqa: E402


def test_wire_stub_path_uses_kebab_slug() -> None:
    path = wire_stub_path("gaza_ceasefire_holds_2025")
    assert path.name == "prediction-resolution-gaza-ceasefire-holds-2025.md"
    assert path.is_file()


def test_resolved_gaza_has_registry_closure_fields() -> None:
    events = load_event_registry()
    gaza = events["gaza_ceasefire_holds_2025"]
    assert gaza["status"] == "resolved"
    assert gaza["outcome"] == "no"
    assert gaza.get("resolved_date")
    assert gaza.get("resolution_source")


def test_israel_trajectory_has_child_event_ids() -> None:
    events = load_event_registry()
    parent = events["israel_self_destruction_trajectory"]
    children = parent.get("child_event_ids") or []
    assert len(children) == 6
    for child_id in children:
        assert events[child_id]["parent_event_id"] == "israel_self_destruction_trajectory"


def test_check_event_registry_cli_passes() -> None:
    proc = subprocess.run(
        ["python3", "scripts/check_event_registry.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout


def test_strict_enrolled_falsifiers_pass_for_pilot_events() -> None:
    events = load_event_registry()
    errors, warnings, _ = check_registry(events, strict_enrolled=True)
    assert not errors, errors
    assert not warnings or all("resolved without wire stub" in w for w in warnings)
