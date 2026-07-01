"""Load voice capture files and write observation artifacts."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .parser import parse_voice_capture

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_VOICE_DIR = REPO_ROOT / "statecraft" / "epistemic" / "observation" / "voice_captures"
DEFAULT_OUT = REPO_ROOT / "statecraft" / "epistemic" / "data" / "observations.json"


def _mtime_iso(path: Path) -> str:
    mtime = path.stat().st_mtime
    return datetime.fromtimestamp(mtime, tz=UTC).isoformat()


def _rel_source_file(path: Path, repo_root: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()


def load_voice_captures(
    *,
    voice_dir: Path | None = None,
    repo_root: Path | None = None,
) -> list[dict[str, Any]]:
    root = repo_root or REPO_ROOT
    captures_dir = voice_dir or DEFAULT_VOICE_DIR
    if not captures_dir.is_dir():
        return []

    observations: list[dict[str, Any]] = []
    for file in sorted(captures_dir.glob("**/*.md")):
        if file.name.startswith("_"):
            continue
        if any(part.startswith("_") for part in file.relative_to(captures_dir).parts[:-1]):
            continue

        voice = file.parent.name
        text = file.read_text(encoding="utf-8")
        source_file = _rel_source_file(file, root)
        observations.append(
            parse_voice_capture(
                voice=voice,
                source_file=source_file,
                text=text,
                mtime_iso=_mtime_iso(file),
            )
        )

    return observations


def write_observations(
    observations: list[dict[str, Any]],
    *,
    out_path: Path | None = None,
) -> Path:
    destination = out_path or DEFAULT_OUT
    destination.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "_meta": {
            "generated": True,
            "do_not_edit": True,
            "layer": "observation",
            "source": "statecraft/epistemic/observation/loader.py",
            "row_count": len(observations),
        },
        "observations": observations,
    }
    destination.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return destination
