from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_agents_slim_line_budget():
    text = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
    lines = [ln for ln in text.splitlines() if ln.strip()]
    assert len(lines) <= 150, f"AGENTS.md has {len(lines)} non-empty lines (target <= 150)"


def test_deep_rules_exists():
    path = REPO_ROOT / "docs" / "agent-rules" / "deep-rules.md"
    assert path.is_file()
    assert "Permission Boundaries" in path.read_text(encoding="utf-8")


def test_active_architecture_not_archived_stub():
    text = (REPO_ROOT / "docs" / "architecture.md").read_text(encoding="utf-8")
    assert "archived: true" not in text
    assert "governed interpretive machine" in text.lower()


def test_check_repo_health_quick():
    proc = subprocess.run(
        [sys.executable, "scripts/check_repo_health.py", "--quick"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
