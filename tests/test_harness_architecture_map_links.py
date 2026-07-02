"""Link integrity checks for docs/harness-architecture-map.md."""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MAP_PATH = REPO_ROOT / "docs" / "harness-architecture-map.md"

# Markdown links: [text](target) or [text](target#anchor)
LINK_RE = re.compile(r"\]\(([^)#]+)(?:#[^)]+)?\)")

def _resolve_link(target: str, source_dir: Path) -> Path:
    if target.startswith("http://") or target.startswith("https://"):
        return Path()  # external; skip existence check
    if target.startswith("/"):
        return REPO_ROOT / target.lstrip("/")
    return (source_dir / target).resolve()

def test_harness_architecture_map_internal_links_exist() -> None:
    text = MAP_PATH.read_text(encoding="utf-8")
    source_dir = MAP_PATH.parent
    missing: list[str] = []
    for match in LINK_RE.finditer(text):
        target = match.group(1).strip()
        if not target or target.startswith("http"):
            continue
        resolved = _resolve_link(target, source_dir)
        if resolved.is_file() or resolved.is_dir():
            continue
        missing.append(target)
    assert not missing, "broken internal link(s) in harness-architecture-map.md:\n" + "\n".join(
        sorted(set(missing))
    )

def test_harness_architecture_map_links_to_membrane_ssot_sections() -> None:
    text = MAP_PATH.read_text(encoding="utf-8")
    assert "work-membrane-v2.md" in text
    assert "engineering-translation" in text
    assert "what-can-cross" in text
