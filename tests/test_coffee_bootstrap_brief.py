"""Tests for first-command coffee bootstrap helpers."""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from assess_session_load import _compute_option_weights, _pick_recommendation
from coffee_bootstrap_brief import (
    _git_credential_status,
    _git_state_status,
    _pytest_status,
    format_coffee_bootstrap_brief,
    format_coffee_recent_rhythm,
)
from operator_coffee import _CAPTURE_KWARGS, _run


def _write_events(path: Path, body: str) -> Path:
    path.write_text(body, encoding="utf-8")
    return path


def test_recent_rhythm_prefers_coffee_close_and_omits_dates(tmp_path: Path) -> None:
    events = _write_events(
        tmp_path / "cadence.md",
        """# Cadence events

_(Append below this line.)_
- **2026-05-01 10:00 UTC** — coffee_close (strategy-codex) ok=true picked=B outcome=partial readiness=execution_ready artifacts=scripts/a.py,tests/test_a.py loops=materialization-stub,next-action next=run-tests
- **2026-05-01 11:00 UTC** — coffee_close (strategy-codex) ok=true picked=C outcome=blocked readiness=blocked artifacts=docs/x.md loops=materialization-stub next=repair-fetch
- **2026-05-01 12:00 UTC** — coffee_close (strategy-codex) ok=true picked=conductor outcome=done readiness=ship_ready conductor=kleiber conductor_state=closed artifacts=commit:abc1234 loops=materialization-stub next=push
""",
    )

    text = format_coffee_recent_rhythm(
        "strategy-codex",
        events_path=events,
        now=datetime(2026, 5, 3, 0, 0, tzinfo=timezone.utc),
    )

    assert "Recent rhythm:" in text
    assert "readiness ship_ready" in text
    assert "commit:abc1234" in text
    assert "materialization-stub x2" in text
    assert "kleiber is closed" in text
    assert "2026-" not in text
    assert "UTC" not in text


def test_recent_rhythm_falls_back_to_recent_cadence_without_close(tmp_path: Path) -> None:
    events = _write_events(
        tmp_path / "cadence.md",
        """# Cadence events

_(Append below this line.)_
- **2026-05-01 09:00 UTC** — coffee (strategy-codex) ok=true mode=work-start
- **2026-05-01 10:00 UTC** — dream (strategy-codex) ok=true
""",
    )

    text = format_coffee_recent_rhythm(
        "strategy-codex",
        events_path=events,
        now=datetime(2026, 5, 3, 0, 0, tzinfo=timezone.utc),
    )

    assert "coffee work-start -> dream pass" in text
    assert "No coffee_close receipt yet" in text


def test_bootstrap_brief_formats_recommendation_without_conductor_hub_line() -> None:
    text = format_coffee_bootstrap_brief(
        {
            "start_state": "load=light; branches=0; memory=ok",
            "repo_identity": "ok - root-name=strategy-codex; origin=https rbtkhn/strategy-codex; AGENTS=active strategy-codex",
            "git_credentials": "origin=https; gh=ok",
            "git_state": "main...origin/main [ahead 1]; dirty=2; untracked=1",
            "pytest": "available (pytest 9.0.3)",
            "recent_rhythm": "Recent rhythm:\n- Last close picked A: done, readiness ship_ready.",
            "artifact_anchors": ["commit:abc1234"],
            "conductor_continuity": {
                "conductor": "kleiber",
                "state": "closed",
                "source": "coffee_close",
            },
            "recommended_hub": "A",
            "recommended_label": "Steward",
            "reason": "last coffee close is ship_ready - Steward can review and ship",
        }
    )

    assert "Coffee Bootstrap Brief" in text
    assert "Repo identity: ok - root-name=strategy-codex" in text
    assert "Git credentials: origin=https; gh=ok" in text
    assert "Git state: main...origin/main [ahead 1]; dirty=2; untracked=1" in text
    assert "Pytest: available (pytest 9.0.3)" in text
    assert "Recommended hub: A. Steward" in text
    assert "Conductor continuity: kleiber closed" in text
    assert "E. Conductor" not in text


def test_git_credential_status_reports_invalid_token(monkeypatch) -> None:
    calls: list[list[str]] = []

    def fake_which(name: str) -> str | None:
        return "gh" if name == "gh" else None

    def fake_run(argv, **kwargs):
        calls.append(list(argv))
        if argv[:3] == ["git", "remote", "get-url"]:
            return type(
                "Result",
                (),
                {"returncode": 0, "stdout": "https://github.com/rbtkhn/strategy-codex.git\n", "stderr": ""},
            )()
        return type(
            "Result",
            (),
            {"returncode": 1, "stdout": "", "stderr": "The token in default is invalid."},
        )()

    monkeypatch.setattr("coffee_bootstrap_brief.shutil.which", fake_which)
    monkeypatch.setattr("coffee_bootstrap_brief.subprocess.run", fake_run)

    assert _git_credential_status() == "origin=https; gh=invalid token - run gh auth login before shell push"
    assert calls == [
        ["git", "remote", "get-url", "origin"],
        ["gh", "auth", "status", "-h", "github.com"],
    ]


def test_git_state_status_summarizes_ahead_dirty_and_untracked(monkeypatch) -> None:
    def fake_run(argv, **kwargs):
        assert argv == ["git", "status", "--short", "--branch"]
        return type(
            "Result",
            (),
            {
                "returncode": 0,
                "stdout": (
                    "## main...origin/main [ahead 1]\n"
                    " M scripts/a.py\n"
                    "A  docs/new.md\n"
                    "?? artifacts/tmp/\n"
                ),
                "stderr": "",
            },
        )()

    monkeypatch.setattr("coffee_bootstrap_brief.subprocess.run", fake_run)

    assert _git_state_status() == "main...origin/main [ahead 1]; dirty=2; untracked=1"


def test_git_state_status_reports_clean(monkeypatch) -> None:
    def fake_run(argv, **kwargs):
        return type(
            "Result",
            (),
            {"returncode": 0, "stdout": "## main...origin/main\n", "stderr": ""},
        )()

    monkeypatch.setattr("coffee_bootstrap_brief.subprocess.run", fake_run)

    assert _git_state_status() == "main...origin/main; clean"


def test_pytest_status_reports_missing(monkeypatch) -> None:
    def fake_run(argv, **kwargs):
        return type(
            "Result",
            (),
            {"returncode": 1, "stdout": "", "stderr": "No module named pytest"},
        )()

    monkeypatch.setattr("coffee_bootstrap_brief.subprocess.run", fake_run)

    assert _pytest_status() == "missing - install test extras before pytest verification"


def test_recommendation_uses_coffee_close_readiness() -> None:
    base_weights = _compute_option_weights("light", None, 0)

    rec, reason = _pick_recommendation(
        "light",
        base_weights,
        [],
        {"last_close": {"readiness": "ship_ready", "artifacts": ["commit:abc1234"]}},
    )
    assert (rec, reason) == (
        "A",
        "last coffee close is ship_ready - Steward can review and ship",
    )

    rec, reason = _pick_recommendation(
        "light",
        base_weights,
        [],
        {"last_close": {"readiness": "execution_ready", "artifacts": ["scripts/x.py"]}},
    )
    assert rec == "B"
    assert "code/test artifacts" in reason

    rec, reason = _pick_recommendation(
        "light",
        base_weights,
        [],
        {"last_close": {"readiness": "orientation", "artifacts": ["docs/x.md"]}},
    )
    assert rec == "C"
    assert "orientation-only" in reason

    rec, reason = _pick_recommendation(
        "light",
        base_weights,
        [],
        {"last_close": {"readiness": "blocked", "artifacts": ["scripts/x.py"]}},
    )
    assert rec == "B"
    assert "blocked on code/test artifacts" in reason


def test_operator_coffee_exposes_first_command_mode() -> None:
    src = (REPO_ROOT / "scripts" / "operator_coffee.py").read_text(encoding="utf-8")

    assert '"first-command"' in src
    assert "--first-command" in src
    assert "Coffee Bootstrap Brief" in src
    assert "append_cadence_event(" in src
    assert "mode=args.mode" in src


def test_operator_coffee_quiet_capture_replaces_decode_errors(monkeypatch) -> None:
    seen: dict[str, object] = {}

    def fake_run(argv, **kwargs):
        seen.update(kwargs)
        return type("Result", (), {"returncode": 0, "stdout": "smart quote \u201d", "stderr": ""})()

    monkeypatch.setattr("operator_coffee.subprocess.run", fake_run)

    assert _run([sys.executable, "-c", "print('ok')"], quiet=True) == 0
    assert seen["encoding"] == "utf-8"
    assert seen["errors"] == "replace"
    assert _CAPTURE_KWARGS["encoding"] == "utf-8"
    assert _CAPTURE_KWARGS["errors"] == "replace"
