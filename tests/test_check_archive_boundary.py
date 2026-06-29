from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

from scripts.check_archive_boundary import (
    CANONICAL_ARCHIVE_POINTER,
    _count_narrative_mentions,
    _has_canonical_pointer,
    _scan_mention_budget,
)


REPO_ROOT = Path(__file__).resolve().parent.parent


def test_canonical_pointer_matches_complexity_budget():
    expected = (
        "Grace-Mar is archived/frozen. Active strategy-codex work does not grow the fork. "
        "See docs/archive/grace-mar.md."
    )
    assert CANONICAL_ARCHIVE_POINTER == expected


def test_duplicated_narrative_fails_mention_budget():
    bad = (
        "Grace-Mar is archived.\n"
        "The Grace-Mar fork is frozen archaeology with extra story.\n"
    )
    issues = _scan_mention_budget("README.md", bad, max_narrative=1)
    assert any("without canonical archive pointer" in i for i in issues)
    assert _count_narrative_mentions(bad) >= 2


def test_pointer_plus_operational_fork_revive_passes():
    good = (
        f"{CANONICAL_ARCHIVE_POINTER}\n"
        "| **A** | Companion (fork revive / seed) | boundary.md |\n"
        "| Gate review | **Fork revive only** — [archive/grace-mar.md](archive/grace-mar.md) |\n"
    )
    assert _has_canonical_pointer(good)
    issues = _scan_mention_budget("docs/start-here.md", good, max_narrative=1)
    assert issues == []


def test_check_archive_boundary_passes_primary_docs():
    proc = subprocess.run(
        [sys.executable, "scripts/check_archive_boundary.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
    assert "ok: archive mention budget check passed" in proc.stdout


def test_check_archive_boundary_strict_on_bad_fixture():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        readme = root / "README.md"
        readme.write_text(
            "Grace-Mar story one.\nGrace-Mar story two.\nGrace-Mar story three.\n",
            encoding="utf-8",
        )
        # Patch REPO_ROOT behavior via direct scan on synthetic content
        issues = _scan_mention_budget("README.md", readme.read_text(encoding="utf-8"), max_narrative=1)
        assert len(issues) >= 1
