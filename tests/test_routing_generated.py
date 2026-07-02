from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from validate_repo_routing import CATEGORY_ENUM, expected_route_category  # noqa: E402
from yaml_compat import safe_load_path  # noqa: E402

def _load_routes() -> list[dict]:
    data = safe_load_path(REPO_ROOT / "repo-map.yaml", feature="test_routing_generated")
    return data.get("routes") or []

def test_generate_llm_routing_check_passes():
    proc = subprocess.run(
        [sys.executable, "scripts/generate_llm_routing.py", "--check"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout

def test_generated_llm_routing_required_links():
    text = (REPO_ROOT / "LLM-ROUTING.md").read_text(encoding="utf-8")
    assert "statecraft/voices/voice-index.md" in text
    assert "source-lattice-beyond-the-repo.md" in text
    assert "Route registry (generated from repo-map.yaml)" in text

def test_category_enum_in_schema():
    schema = json.loads((REPO_ROOT / "schemas" / "repo_map.schema.json").read_text(encoding="utf-8"))
    category = schema["properties"]["routes"]["items"]["properties"]["category"]
    assert set(category["enum"]) == {"source", "work", "generated", "archive"}
    required = schema["properties"]["routes"]["items"]["required"]
    assert "category" in required

def test_repo_map_routes_have_valid_categories():
    for route in _load_routes():
        declared = route.get("category")
        assert declared in CATEGORY_ENUM, f"{route.get('id')}: {declared}"

def test_repo_map_categories_match_expected_rules():
    for route in _load_routes():
        declared = route.get("category")
        expected = expected_route_category(route)
        assert declared == expected, (
            f"{route.get('id')}: declared={declared} expected={expected}"
        )

def test_llm_routing_has_no_blank_categories():
    text = (REPO_ROOT / "LLM-ROUTING.md").read_text(encoding="utf-8")
    in_registry = False
    for line in text.splitlines():
        if line.startswith("## Route registry"):
            in_registry = True
            continue
        if in_registry and line.startswith("## ") and "Route registry" not in line:
            break
        if not in_registry or not line.startswith("|"):
            continue
        if line.startswith("|---") or "id | kind" in line:
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 5:
            category = parts[3]
            assert category and category != "—", line

def test_grace_mar_paths_are_archive():
    for route in _load_routes():
        path = str(route.get("path") or "").replace("\\", "/")
        if path.startswith("archive/grace-mar-"):
            assert route.get("category") == "archive", route.get("id")

def test_runtime_artifacts_routes_are_generated():
    for route in _load_routes():
        path = str(route.get("path") or "").replace("\\", "/")
        if path.startswith("runtime/artifacts/"):
            assert route.get("category") == "generated", route.get("id")

def test_source_capture_route_is_source():
    route = next(r for r in _load_routes() if r.get("id") == "statecraft-source-capture")
    assert route.get("kind") == "source_capture"
    assert route.get("category") == "source"

def test_all_four_categories_represented():
    seen = {r.get("category") for r in _load_routes()}
    assert seen >= CATEGORY_ENUM
