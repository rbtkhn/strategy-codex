from __future__ import annotations

import io
import sys

import pytest

def test_strategy_codex_repo_root_import():
    from strategy_codex import repo_root

    root = repo_root()
    assert root.is_dir()
    assert (root / "users").is_dir()

def test_grace_mar_compat_warns(capsys):
    from strategy_codex.compat.grace_mar import main

    argv = ["grace-mar", "--help"]
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(sys, "argv", argv)
        rc = main()
    assert rc == 0
    err = capsys.readouterr().err
    assert "deprecated" in err.lower()
    assert "strategy-codex" in err

