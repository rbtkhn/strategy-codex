from __future__ import annotations

import hashlib
import json
import os
import re
import shlex
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "artifacts" / "simulations"
DEFAULT_FORECAST_ROOT = REPO_ROOT / ".forecast"
DEFAULT_SCENARIO_LAB_ROOT = REPO_ROOT.parent / "scenario-lab"
if os.name == "nt":
    DEFAULT_SCENARIO_LAB_CMD = ["cmd.exe", "/d", "/c", "scenario-lab"]
else:
    DEFAULT_SCENARIO_LAB_CMD = ["scenario-lab"]


def utc_now_iso() -> str:
    return datetime.now(UTC).isoformat()


def relative_to_repo(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(path)


def slugify(value: str, *, fallback: str = "scenario") -> str:
    text = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return text or fallback


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def markdown_excerpt(path: Path, max_chars: int = 2_000) -> str:
    text = path.read_text(encoding="utf-8").strip()
    if len(text) > max_chars:
        text = text[: max_chars - 3].rstrip() + "..."
    return text


def resolve_scenario_lab_root(explicit: str | None = None) -> Path:
    raw = explicit or os.environ.get("SCENARIO_LAB_ROOT", "").strip()
    if raw:
        return Path(raw).expanduser().resolve()
    return DEFAULT_SCENARIO_LAB_ROOT


def resolve_forecast_root(explicit: str | None = None) -> Path:
    raw = explicit or os.environ.get("SCENARIO_LAB_FORECAST_ROOT", "").strip()
    if raw:
        return Path(raw).expanduser().resolve()
    return DEFAULT_FORECAST_ROOT


def resolve_scenario_lab_cmd(explicit: str | None = None) -> list[str]:
    raw = explicit or os.environ.get("SCENARIO_LAB_CMD", "").strip()
    if raw:
        return shlex.split(raw, posix=False)
    return list(DEFAULT_SCENARIO_LAB_CMD)


def run_scenario_lab(
    args: list[str],
    *,
    cwd: Path,
    scenario_lab_cmd: list[str] | None = None,
) -> subprocess.CompletedProcess[str]:
    command = list(scenario_lab_cmd or DEFAULT_SCENARIO_LAB_CMD) + args
    return subprocess.run(
        command,
        cwd=cwd,
        check=False,
        text=True,
        capture_output=True,
    )


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    return path


def write_text(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")
    return path


def append_jsonl(path: Path, row: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n")
    return path


def resolve_output_path(path: Path, *, default_root: Path) -> Path:
    if path.is_absolute():
        return path
    if path.parts and path.parts[0] in {"artifacts", "codex", "docs", "src", "tests", ".forecast"}:
        return REPO_ROOT / path
    return default_root / path
