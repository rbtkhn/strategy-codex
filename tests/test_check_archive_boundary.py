from __future__ import annotations

import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def test_check_archive_boundary_passes_primary_docs():
    proc = subprocess.run(
        [sys.executable, "scripts/check_archive_boundary.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
    assert "ok: archive boundary check passed" in proc.stdout
