from __future__ import annotations

import json
import os
import shlex
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "runtime/artifacts" / "codegraph"
if os.name == "nt":
    DEFAULT_CODEGRAPH_CMD = ["cmd.exe", "/d", "/c", "npx", "@colbymchenry/codegraph"]
else:
    DEFAULT_CODEGRAPH_CMD = ["npx", "@colbymchenry/codegraph"]


def utc_now_iso() -> str:
    return datetime.now(UTC).isoformat()


def relative_to_repo(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(path)


def _windows_codegraph_cache_glob() -> str:
    return (
        ".codex-tmp/npm-cache/_npx/*/node_modules/"
        "@colbymchenry/codegraph-win32-x64/platform/bin/codegraph.cmd"
    )


def find_local_codegraph_cmd() -> list[str] | None:
    if os.name != "nt":
        return None

    candidates = list(REPO_ROOT.glob(_windows_codegraph_cache_glob()))
    if not candidates:
        return None

    newest = max(candidates, key=lambda path: path.stat().st_mtime)
    return [str(newest)]


def resolve_codegraph_cmd(explicit: str | None = None) -> list[str]:
    raw = explicit or os.environ.get("CODEGRAPH_CMD", "").strip()
    if raw:
        return shlex.split(raw, posix=False)
    local_cmd = find_local_codegraph_cmd()
    if local_cmd:
        return local_cmd
    return list(DEFAULT_CODEGRAPH_CMD)


def run_codegraph(
    args: list[str],
    *,
    cwd: Path | None = None,
    codegraph_cmd: list[str] | None = None,
) -> subprocess.CompletedProcess[str]:
    command = list(codegraph_cmd or DEFAULT_CODEGRAPH_CMD) + args
    env = os.environ.copy()
    if "NPM_CONFIG_CACHE" not in env:
        env["NPM_CONFIG_CACHE"] = str(REPO_ROOT / ".codex-tmp" / "npm-cache")
    return subprocess.run(
        command,
        cwd=cwd or REPO_ROOT,
        check=True,
        text=True,
        capture_output=True,
        env=env,
    )


def run_codegraph_json(
    args: list[str],
    *,
    cwd: Path | None = None,
    codegraph_cmd: list[str] | None = None,
) -> Any:
    result = run_codegraph(args, cwd=cwd, codegraph_cmd=codegraph_cmd)
    return json.loads(result.stdout)


def write_json(path: Path, payload: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    return path


def write_text(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")
    return path
