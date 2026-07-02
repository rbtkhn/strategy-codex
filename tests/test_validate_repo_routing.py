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
        discover_host_shelves,
        discover_source_indexes,
        host_shelf_route_id,
        load_repo_map,
        validate_host_shelf_registry,
        validate_required_routes,
        validate_schema,
    )

    errors: list[str] = []
    data = load_repo_map()
    validate_schema(data, errors)
    validate_required_routes(data, errors)
    validate_host_shelf_registry(data, errors, generate_hints=False)
    assert not errors, errors

    ids = {r["id"] for r in data["routes"]}
    assert "barnes-source-index" in ids
    assert "source-lattice-doctrine" in ids

    discovered = {p.relative_to(REPO_ROOT).as_posix() for p in discover_source_indexes()}
    assert len(discovered) >= 20

    host_shelves = discover_host_shelves()
    assert len(host_shelves) == 3
    for shelf in host_shelves:
        assert host_shelf_route_id(shelf.parent.name) in ids

def test_collect_routing_metrics() -> None:
    from scripts.validate_repo_routing import collect_routing_metrics

    metrics = collect_routing_metrics(strict=True)
    assert metrics["source_index_count"] >= 20
    assert metrics["host_shelf_count"] == 3
    assert metrics["host_shelf_coverage_pct"] == 100.0
    assert metrics["registry_coverage_pct"] == 100.0
    assert metrics["markdown_link_count"] >= 600
    assert metrics["broken_link_count"] == 0
    assert metrics["absolute_path_violations"] == 0

def test_validate_repo_routing_report_flag() -> None:
    proc = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "validate_repo_routing.py"),
            "--strict",
            "--report",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout
    assert "## Repo routing metrics" in proc.stdout
    assert "host shelves (disk): 3" in proc.stdout
    assert "host shelves: repo-map lists 3/3 (100.0%)" in proc.stdout

def test_benchmark_routing_discovery() -> None:
    proc = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "benchmark_routing_discovery.py"),
            "--rounds",
            "3",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout
    assert "Barnes index discovery benchmark" in proc.stdout
    assert "LLM-ROUTING dispatch" in proc.stdout
