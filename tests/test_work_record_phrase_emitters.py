"""Ensure markdown emitters never reintroduce deprecated WORK/Record banner phrasing."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
RENDER_PATH = REPO_ROOT / "scripts" / "moonshots_intelligence" / "render.py"

FORBIDDEN_FRAGMENTS = (
    "work only; not record",
    "work only — not record",
    "work only - not record",
)


def _load_render_module():
    spec = importlib.util.spec_from_file_location("moonshots_render", RENDER_PATH)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def test_moonshots_render_never_emits_deprecated_phrase() -> None:
    mod = _load_render_module()
    document = {
        "provenance": {
            "output_basename": "test-episode",
            "archive_path": "source-archive/singularity/moonshots/test.md",
            "episode_number": 1,
            "source_url": "https://example.com/ep",
            "compiler_version": "test",
            "prompt_id": "test",
            "model": "test",
            "generated_at": "2026-07-02",
        },
        "core_thesis": "Test thesis.",
        "bullets": [],
        "open_questions": [],
        "operator_actions": [],
    }
    md = mod.render_markdown(document)
    lowered = md.casefold()
    for fragment in FORBIDDEN_FRAGMENTS:
        assert fragment not in lowered, f"render output contained forbidden fragment: {fragment!r}"
