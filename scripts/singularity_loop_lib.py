"""Shared singularity loop loading, validation, and registry builders."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
LOOPS_DIR = REPO_ROOT / "singularity" / "loops"
LOOP_SCHEMA_PATH = REPO_ROOT / "schemas" / "singularity" / "loop.schema.json"
DEFAULT_REGISTRY_OUTPUT = REPO_ROOT / "runtime" / "artifacts" / "loop-registry.json"
DEFAULT_SIGNALS_OUTPUT = REPO_ROOT / "runtime" / "artifacts" / "singularity-signals.json"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from mcp_receipt_lib import validate_json_schema  # noqa: E402
from singularity_loop_invariants import run_singularity_loop_invariants  # noqa: E402
from yaml_compat import safe_load_path  # noqa: E402

def repo_relative(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")

def render_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"

def iter_loop_yaml_files(*, loops_dir: Path | None = None) -> list[Path]:
    root = loops_dir or LOOPS_DIR
    if not root.is_dir():
        return []
    return sorted(root.rglob("*.yaml"))

def load_loop_document(path: Path) -> dict[str, Any]:
    data = safe_load_path(path, feature=repo_relative(path))
    if not isinstance(data, dict):
        raise ValueError(f"{repo_relative(path)}: expected mapping at root")
    return data

def validate_loop_document(data: dict[str, Any], *, label: str) -> None:
    validate_json_schema(data, LOOP_SCHEMA_PATH)

def flatten_loop_row(data: dict[str, Any], *, source_file: str) -> dict[str, Any]:
    loop = data["loop"]
    row = dict(loop)
    row["source_file"] = source_file
    if "dependencies" not in row:
        row["dependencies"] = []
    if "last_run" not in row:
        row["last_run"] = None
    return row

def collect_loop_rows(*, loops_dir: Path | None = None) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    errors: list[str] = []

    for path in iter_loop_yaml_files(loops_dir=loops_dir):
        rel = repo_relative(path)
        try:
            data = load_loop_document(path)
            validate_loop_document(data, label=rel)
            rows.append(flatten_loop_row(data, source_file=rel))
        except Exception as exc:
            errors.append(f"{rel}: {exc}")

    if errors:
        raise ValueError("\n".join(errors))

    invariant_issues = run_singularity_loop_invariants(rows)
    if invariant_issues:
        raise ValueError("\n".join(invariant_issues))

    rows.sort(key=lambda row: str(row["id"]))
    return rows

def build_registry_payload(*, loops_dir: Path | None = None) -> dict[str, Any]:
    loops = collect_loop_rows(loops_dir=loops_dir)
    return {
        "_meta": {
            "generated": True,
            "do_not_edit": True,
            "source": "scripts/build_loop_registry.py",
        },
        "loops": loops,
    }

def default_signals_payload() -> dict[str, Any]:
    return {
        "_meta": {
            "generated": False,
            "do_not_edit": False,
            "source": "operator-or-run_singularity_loops",
        },
        "pending_loops": [],
        "blocked_loops": [],
        "attention_required": [],
    }

def build_orchestrator_signals(*, loops: list[dict[str, Any]], source: str) -> dict[str, Any]:
    attention: list[str] = []
    pending: list[str] = []
    blocked: list[str] = []

    for row in loops:
        loop_id = str(row.get("id") or "")
        status = str((row.get("state") or {}).get("status") or "")
        if status == "paused":
            pending.append(loop_id)
        elif status == "completed":
            continue
        elif status == "active" and row.get("last_run") is None:
            attention.append(loop_id)

    payload = default_signals_payload()
    payload["pending_loops"] = sorted(pending)
    payload["blocked_loops"] = sorted(blocked)
    payload["attention_required"] = sorted(attention)
    payload["_meta"]["generated"] = True
    payload["_meta"]["source"] = source
    return payload

def refresh_orchestrator_signals(
    *,
    registry_path: Path | None = None,
    output_path: Path | None = None,
    source: str = "scripts/run_singularity_loops.py --status",
) -> dict[str, Any]:
    registry = load_registry(registry_path=registry_path)
    loops = registry.get("loops") or []
    if not isinstance(loops, list):
        raise ValueError("registry loops must be a list")
    payload = build_orchestrator_signals(loops=loops, source=source)
    out = output_path or DEFAULT_SIGNALS_OUTPUT
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_json(payload), encoding="utf-8")
    return payload

def format_singularity_signals_brief(payload: dict[str, Any]) -> str | None:
    pending = payload.get("pending_loops") or []
    blocked = payload.get("blocked_loops") or []
    attention = payload.get("attention_required") or []
    if not pending and not blocked and not attention:
        return None
    parts: list[str] = []
    if attention:
        parts.append(f"attention: {', '.join(attention)}")
    if pending:
        parts.append(f"pending: {', '.join(pending)}")
    if blocked:
        parts.append(f"blocked: {', '.join(blocked)}")
    return "Singularity loops — " + "; ".join(parts)

def refresh_and_brief(*, source: str) -> str | None:
    """Refresh orchestrator signals and return a one-line brief when non-empty."""
    payload = refresh_orchestrator_signals(source=source)
    return format_singularity_signals_brief(payload)

def load_registry(*, registry_path: Path | None = None) -> dict[str, Any]:
    path = registry_path or DEFAULT_REGISTRY_OUTPUT
    if not path.is_file():
        raise FileNotFoundError(f"missing {repo_relative(path)}")
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError(f"{repo_relative(path)}: expected object")
    return data
