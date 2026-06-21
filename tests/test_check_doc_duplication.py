from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_check_doc_duplication_runs_warn_mode():
    proc = subprocess.run(
        [sys.executable, "scripts/check_doc_duplication.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode in (0, 1)
    assert "doc-duplication:" in proc.stderr or "ok: doc duplication" in proc.stdout


def test_check_doc_duplication_strict_exits_one_with_known_dupes():
    proc = subprocess.run(
        [sys.executable, "scripts/check_doc_duplication.py", "--strict"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 1
    assert "doc-duplication:" in proc.stderr
