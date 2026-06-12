"""Tests for scripts/validate_repo_routing.py"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_validate_repo_routing_allow_absolute_paths() -> None:
    """Routing surfaces exist; absolute paths allowed until link normalization."""
    proc = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "validate_repo_routing.py"),
            "--allow-absolute-paths",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout


def test_repo_map_schema_and_barnes_route() -> None:
    from scripts.validate_repo_routing import (
        discover_source_indexes,
        load_repo_map,
        validate_required_routes,
        validate_schema,
    )

    errors: list[str] = []
    data = load_repo_map()
    validate_schema(data, errors)
    validate_required_routes(data, errors)
    assert not errors, errors

    ids = {r["id"] for r in data["routes"]}
    assert "barnes-source-index" in ids
    assert "source-lattice-doctrine" in ids

    discovered = {p.relative_to(REPO_ROOT).as_posix() for p in discover_source_indexes()}
    assert len(discovered) == 20
