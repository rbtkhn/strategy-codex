from __future__ import annotations

from strategy_codex.compat.grace_mar_paths import (
    bootstrap_dir,
    bot_dir,
    grace_mar_instance_dir,
    recursion_gate_staging_dir,
)


def test_grace_mar_compat_paths_point_to_archive_instance():
    assert bot_dir().as_posix().endswith("archive/grace-mar-instance/bot")
    assert bootstrap_dir().as_posix().endswith("archive/grace-mar-instance/bootstrap")
    assert recursion_gate_staging_dir().as_posix().endswith(
        "archive/grace-mar-instance/recursion-gate-staging"
    )
    assert grace_mar_instance_dir().as_posix().endswith("archive/grace-mar-instance")


def test_grace_mar_compat_paths_exist():
    assert bot_dir().is_dir()
    assert bootstrap_dir().is_dir()
    assert recursion_gate_staging_dir().is_dir()
    assert grace_mar_instance_dir().is_dir()
