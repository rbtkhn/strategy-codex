from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

REPORT_PATH = REPO_ROOT / "runtime" / "artifacts" / "repo-convergence-report.json"
LOG_PATH = REPO_ROOT / "runtime" / "operator-events" / "repo-convergence.jsonl"

def _read_bytes_or_none(path: Path) -> bytes | None:
    if not path.is_file():
        return None
    return path.read_bytes()

def _restore_bytes(path: Path, content: bytes | None) -> None:
    if content is None:
        if path.exists():
            path.unlink()
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)

def _path_stat(path: Path) -> tuple[float, int] | None:
    if not path.is_file():
        return None
    st = path.stat()
    return st.st_mtime, st.st_size

class _preserve_file:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.content: bytes | None = None

    def __enter__(self) -> None:
        self.content = _read_bytes_or_none(self.path)
        return None

    def __exit__(self, exc_type, exc, tb) -> None:
        _restore_bytes(self.path, self.content)

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

def test_check_does_not_write_report_or_log():
    before_report = _path_stat(REPORT_PATH)
    before_log = _path_stat(LOG_PATH)

    proc = subprocess.run(
        [
            sys.executable,
            "scripts/run_repo_convergence.py",
            "--check",
            "--loop",
            "schema",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "check complete; report not written" in proc.stdout
    assert _path_stat(REPORT_PATH) == before_report
    assert _path_stat(LOG_PATH) == before_log

def test_hash_excludes_convergence_artifacts():
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    from run_repo_convergence import (  # noqa: E402
        HASH_EXCLUDE_PATHS,
        hash_paths,
        repo_path,
        should_hash_path,
    )

    assert all(not should_hash_path(repo_path(p)) for p in HASH_EXCLUDE_PATHS)

    with _preserve_file(REPORT_PATH):
        before = hash_paths(("runtime/artifacts",))
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        REPORT_PATH.write_text("temporary convergence report mutation\n", encoding="utf-8")
        after = hash_paths(("runtime/artifacts",))
        assert before == after

def test_record_report_writes_in_check_mode():
    with _preserve_file(REPORT_PATH), _preserve_file(LOG_PATH):
        before = _path_stat(REPORT_PATH)

        proc = subprocess.run(
            [
                sys.executable,
                "scripts/run_repo_convergence.py",
                "--check",
                "--record-report",
                "--quiet",
                "--loop",
                "schema",
            ],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        assert proc.returncode == 0, proc.stdout + proc.stderr
        after = _path_stat(REPORT_PATH)
        assert after is not None
        if before is None:
            assert after[1] > 0
        else:
            assert after[0] >= before[0]

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
