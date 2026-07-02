"""Tests for scripts/validate_sid_embargo.py."""

from __future__ import annotations

import sys
import uuid
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from validate_sid_embargo import validate_file  # noqa: E402

def _scratch_path(name: str) -> Path:
    scratch = REPO_ROOT / ".codex-tmp" / "pytest-scratch"
    scratch.mkdir(parents=True, exist_ok=True)
    return scratch / f"{name}-{uuid.uuid4().hex}.md"

def test_valid_embargo_passes() -> None:
    path = _scratch_path("embargo-ok")
    path.write_text(
        """---
embargo: client-only
sid_deliverable: transaction-memo
---

# body
""",
        encoding="utf-8",
    )
    assert validate_file(path, strict=True) == []

def test_invalid_embargo_fails() -> None:
    path = _scratch_path("embargo-bad")
    path.write_text(
        """---
embargo: public
---

# body
""",
        encoding="utf-8",
    )
    errors = validate_file(path, strict=True)
    assert any("invalid embargo" in e for e in errors)
