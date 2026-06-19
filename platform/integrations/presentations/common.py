from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from grace_mar.presentations.contract import canonical_bundle_json

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def current_git_ref() -> str:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=REPO_ROOT,
            text=True,
        ).strip()
    except Exception:
        return "unknown"
    return out or "unknown"


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def utc_now_iso() -> str:
    return datetime.now(UTC).isoformat()


def markdown_excerpt(path: Path, max_chars: int = 3_500) -> str:
    text = path.read_text(encoding="utf-8")
    excerpt = text.strip()
    if len(excerpt) > max_chars:
        excerpt = excerpt[: max_chars - 3].rstrip() + "..."
    return excerpt


def write_bundle(bundle: dict[str, Any], output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(canonical_bundle_json(bundle) + "\n", encoding="utf-8")
    return output_path
