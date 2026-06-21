from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


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
    assert "statecraft/voices/INDEX.md" in text
    assert "source-lattice-beyond-the-repo.md" in text
    assert "Route registry (generated from repo-map.yaml)" in text

def test_category_enum_in_schema():
    import json

    schema = json.loads((REPO_ROOT / "schemas" / "repo_map.schema.json").read_text(encoding="utf-8"))
    category = schema["properties"]["routes"]["items"]["properties"]["category"]
    assert set(category["enum"]) == {"source", "work", "generated", "archive"}
