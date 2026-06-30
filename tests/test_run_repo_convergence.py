from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_run_repo_convergence_explain():
    proc = subprocess.run(
        [sys.executable, "scripts/run_repo_convergence.py", "--explain"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "statecraft_predictions" in proc.stdout


def test_run_repo_convergence_check():
    proc = subprocess.run(
        [sys.executable, "scripts/run_repo_convergence.py", "--check", "--quiet"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_topo_sort_detects_cycle():
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    from run_repo_convergence import topo_sort_loops  # noqa: E402

    import repo_convergence_registry as reg  # noqa: E402

    original = dict(reg.LOOPS)
    try:
        reg.LOOPS.clear()
        reg.LOOPS["a"] = reg.LoopSpec(
            kind="validator",
            inputs=("README.md",),
            commands=(("scripts/validate_repo_routing.py",),),
            depends_on=("b",),
        )
        reg.LOOPS["b"] = reg.LoopSpec(
            kind="validator",
            inputs=("AGENTS.md",),
            commands=(("scripts/validate_repo_routing.py",),),
            depends_on=("a",),
        )
        try:
            topo_sort_loops(["a", "b"])
            assert False, "expected cycle detection"
        except SystemExit as exc:
            assert "cycle" in str(exc).lower()
    finally:
        reg.LOOPS.clear()
        reg.LOOPS.update(original)


def test_registry_scripts_exist():
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    from repo_convergence_registry import LOOPS  # noqa: E402

    for name, spec in LOOPS.items():
        for cmd in spec.commands:
            script = REPO_ROOT / cmd[0]
            assert script.is_file(), f"{name}: missing script {cmd[0]}"
