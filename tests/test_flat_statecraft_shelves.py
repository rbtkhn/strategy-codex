"""Flat shelf law — no subfolders under statecraft/voices/<speaker>/ or channels/<slug>/."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
VOICES = REPO_ROOT / "statecraft" / "voices"
CHANNELS = REPO_ROOT / "statecraft" / "channels"
VOICES_META = frozenset({"_scratch", "_templates", "map", "relations"})
BENCHMARK_EXCLUDE = "runtime/artifacts/benchmarks/"
FORBIDDEN_IN_TRACKED = re.compile(
    r"statecraft/(?:voices/[a-z0-9-]+/(?:stream|themes)/|channels/[a-z0-9-]+/stream/)"
)


def _tracked_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=REPO_ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def test_no_subdirs_under_speaker_shelves() -> None:
    violations: list[str] = []
    for base, meta in ((VOICES, VOICES_META), (CHANNELS, frozenset())):
        if not base.is_dir():
            continue
        for shelf in sorted(base.iterdir()):
            if not shelf.is_dir() or shelf.name in meta:
                continue
            for child in shelf.iterdir():
                if child.is_dir():
                    violations.append(str(child.relative_to(REPO_ROOT)).replace("\\", "/"))
    assert not violations, "flat shelf violation — subdirs under shelf root:\n" + "\n".join(
        violations
    )


def test_no_tracked_stream_or_themes_paths() -> None:
    bad: list[str] = []
    for path in _tracked_files():
        if path.startswith(BENCHMARK_EXCLUDE):
            continue
        if "/stream/" in path or "/themes/" in path:
            if path.startswith("statecraft/voices/") or path.startswith("statecraft/channels/"):
                bad.append(path)
    assert not bad, "tracked files still under stream/ or themes/:\n" + "\n".join(bad[:50])


def test_no_forbidden_path_strings_in_live_docs() -> None:
    hits: list[str] = []
    for path in _tracked_files():
        if path.startswith(BENCHMARK_EXCLUDE):
            continue
        if not path.endswith((".md", ".toml", ".py", ".mdc", ".json")):
            continue
        if path.startswith("runtime/artifacts/flat-shelf-migrate-receipt.json"):
            continue
        if path.startswith("runtime/artifacts/statecraft/codex-speakers-migration-receipt.json"):
            continue
        if path == "scripts/flatten_statecraft_shelves.py":
            continue
        if path == "tests/test_flat_statecraft_shelves.py":
            continue
        full = REPO_ROOT / path
        if not full.is_file():
            continue
        try:
            text = full.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if FORBIDDEN_IN_TRACKED.search(text):
            hits.append(path)
    assert not hits, "live files still cite nested stream/themes paths:\n" + "\n".join(hits[:30])
