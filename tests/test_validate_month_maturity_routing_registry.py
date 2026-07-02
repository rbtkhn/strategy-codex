"""Tests for scripts/validate_month_maturity_routing_registry.py."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

@pytest.fixture()
def vmr_mod():
    path = REPO_ROOT / "scripts" / "validate_month_maturity_routing_registry.py"
    spec = importlib.util.spec_from_file_location("validate_month_maturity_routing_registry", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod

def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

def make_registry(month_entry: dict) -> dict:
    return {
        "generated_at": "2026-06-02T00:00:00Z",
        "generated_by": "manual-seed",
        "scope": "test",
        "months": [month_entry],
    }

def make_metadata(month: str, *, surfaces: list[str], finite_queue: bool, benchmark: bool) -> dict:
    return {
        "generated_at": "2026-06-02T00:00:00Z",
        "generated_by": "test",
        "registry_path": "statecraft/data/month-maturity-routing-registry.json",
        "months": {
            month: {
                "captured_days": 1,
                "source_count": 1,
                "thread_count": 1,
                "channel_or_show_count": 1,
                "host_count": 1,
                "guest_count": 1,
                "guest_label_variants": [],
                "existing_month_surface_count": len(surfaces),
                "existing_month_surfaces": surfaces,
                "is_dense_month": False,
                "has_finite_queue": finite_queue,
                "has_existing_benchmark_surfaces": benchmark,
                "needs_label_normalization": False,
            }
        },
    }

def make_entry(route_class: str = "benchmark", status: str = "stable") -> dict:
    return {
        "month": "2026-01",
        "route_class": route_class,
        "maturity_label": "opening continuity/setup benchmark",
        "status": status,
        "primary_surfaces": ["statecraft/notes/sample-note.md"],
        "comparison_uses": ["January vs February"],
        "open_questions": ["Guest-label normalization if needed."],
        "next_honest_move": "Keep using the month as a benchmark.",
        "has_finite_queue": False,
        "updated_at": "2026-06-02",
    }

def test_validate_registry_ok(tmp_path: Path, vmr_mod):
    repo_root = tmp_path
    surface = repo_root / "statecraft" / "notes" / "sample-note.md"
    surface.parent.mkdir(parents=True, exist_ok=True)
    surface.write_text("ok\n", encoding="utf-8")

    entry = make_entry()
    write_json(repo_root / "statecraft" / "data" / "month-maturity-routing-registry.json", make_registry(entry))
    write_json(
        repo_root / "statecraft" / "data" / "month-routing-metadata.json",
        make_metadata("2026-01", surfaces=entry["primary_surfaces"], finite_queue=False, benchmark=True),
    )

    errors = vmr_mod.validate_month_maturity_routing_registry(repo_root)
    assert errors == []

def test_rejects_bad_route_class(tmp_path: Path, vmr_mod):
    repo_root = tmp_path
    surface = repo_root / "statecraft" / "notes" / "sample-note.md"
    surface.parent.mkdir(parents=True, exist_ok=True)
    surface.write_text("ok\n", encoding="utf-8")

    entry = make_entry(route_class="unknown")
    write_json(repo_root / "statecraft" / "data" / "month-maturity-routing-registry.json", make_registry(entry))
    write_json(
        repo_root / "statecraft" / "data" / "month-routing-metadata.json",
        make_metadata("2026-01", surfaces=entry["primary_surfaces"], finite_queue=False, benchmark=False),
    )

    errors = vmr_mod.validate_month_maturity_routing_registry(repo_root)
    assert any("route_class must be one of" in error for error in errors)

def test_rejects_missing_primary_surface_file(tmp_path: Path, vmr_mod):
    repo_root = tmp_path
    entry = make_entry()
    write_json(repo_root / "statecraft" / "data" / "month-maturity-routing-registry.json", make_registry(entry))
    write_json(
        repo_root / "statecraft" / "data" / "month-routing-metadata.json",
        make_metadata("2026-01", surfaces=entry["primary_surfaces"], finite_queue=False, benchmark=True),
    )

    errors = vmr_mod.validate_month_maturity_routing_registry(repo_root)
    assert any("primary_surface not found" in error for error in errors)

def test_rejects_metadata_surface_drift(tmp_path: Path, vmr_mod):
    repo_root = tmp_path
    surface = repo_root / "statecraft" / "notes" / "sample-note.md"
    surface.parent.mkdir(parents=True, exist_ok=True)
    surface.write_text("ok\n", encoding="utf-8")

    entry = make_entry()
    write_json(repo_root / "statecraft" / "data" / "month-maturity-routing-registry.json", make_registry(entry))
    write_json(
        repo_root / "statecraft" / "data" / "month-routing-metadata.json",
        make_metadata("2026-01", surfaces=[], finite_queue=False, benchmark=True),
    )

    errors = vmr_mod.validate_month_maturity_routing_registry(repo_root)
    assert any("metadata missing primary surface" in error for error in errors)

def test_rejects_metadata_queue_mismatch(tmp_path: Path, vmr_mod):
    repo_root = tmp_path
    surface = repo_root / "statecraft" / "notes" / "sample-note.md"
    surface.parent.mkdir(parents=True, exist_ok=True)
    surface.write_text("ok\n", encoding="utf-8")

    entry = make_entry()
    entry["has_finite_queue"] = True
    write_json(repo_root / "statecraft" / "data" / "month-maturity-routing-registry.json", make_registry(entry))
    write_json(
        repo_root / "statecraft" / "data" / "month-routing-metadata.json",
        make_metadata("2026-01", surfaces=entry["primary_surfaces"], finite_queue=False, benchmark=True),
    )

    errors = vmr_mod.validate_month_maturity_routing_registry(repo_root)
    assert any("metadata has_finite_queue does not match registry" in error for error in errors)
