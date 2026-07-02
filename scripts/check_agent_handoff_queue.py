#!/usr/bin/env python3
"""Validate Agent Handoff Queue items under runtime/operator-queue/."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
DEFAULT_QUEUE_ROOT = REPO_ROOT / "runtime" / "operator-queue"

STATUS_DIRS = {
    "agent_todo": "agent-todo",
    "agent_working": "agent-working",
    "needs_input": "needs-input",
    "gate_required": "gate-required",
    "agent_done": "agent-done",
    "void": "void",
}

MEMBRANE_CLASSES = frozenset(
    {
        "record",
        "governed_adjacent",
        "instrumental_work",
        "runtime_derived",
        "external_complement",
    }
)

CORE_REQUIRED_FIELDS = frozenset(
    {
        "id",
        "title",
        "status",
        "owner",
        "requester",
        "created_at",
        "membrane_class",
        "context",
        "definition_of_done",
        "receipt_required",
    }
)

RECOMMENDED_FIELDS = frozenset(
    {
        "allowed_actions",
        "forbidden_actions",
        "stop_conditions",
        "priority",
        "labels",
    }
)

KNOWN_OWNERS = frozenset({"operator", "codex", "cursor", "human"})

ID_RE = re.compile(r"^ahq-\d{8}-\d{3}$")

NEGATION_RE = re.compile(
    r"(?:\bnot\b|\bnon[-_]|do not|does not|don't|never|not a substitute)",
    re.I,
)

AUTHORITY_PHRASES = (
    "automatic promotion",
    "auto-merge",
    "promotes authority",
)

FORBIDDEN_ACTION_TOKENS = (
    "promote_",
    "merge_record",
    "auto_promote",
)

BLOCKING_QUESTION_KEYS = frozenset({"asked_at", "question", "needed_from"})
RECEIPT_KEYS = frozenset({"completed_at", "actor", "stopped_because"})
GATE_KEYS = frozenset({"type", "reason", "required_decision"})

def parse_frontmatter(text: str) -> dict[str, Any]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    raw = text[4:end]
    try:
        from scripts.yaml_compat import safe_load_text

        data = safe_load_text(raw, feature="agent handoff queue frontmatter")
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}

def repo_rel(path: Path, repo_root: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()

def iter_items(queue_root: Path) -> list[Path]:
    if not queue_root.exists():
        return []
    out: list[Path] = []
    for status_dir in STATUS_DIRS.values():
        root = queue_root / status_dir
        if root.exists():
            out.extend(sorted(root.glob("*.md")))
    return sorted(out)

def _require_list(data: dict[str, Any], field: str, rel: str, errors: list[str]) -> None:
    value = data.get(field)
    if not isinstance(value, list) or not value:
        errors.append(f"{rel}: `{field}` must be a non-empty list")

def _require_dict_keys(
    block: Any,
    *,
    rel: str,
    block_name: str,
    required_keys: frozenset[str],
    errors: list[str],
) -> None:
    if not isinstance(block, dict) or not block:
        errors.append(f"{rel}: `{block_name}` must be a non-empty object")
        return
    missing = sorted(required_keys - set(block))
    for key in missing:
        errors.append(f"{rel}: `{block_name}` missing required key `{key}`")

def _parse_created_at(value: Any) -> bool:
    if not value:
        return False
    text = str(value).strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        datetime.fromisoformat(text)
    except ValueError:
        return False
    return True

def _line_claims_authority_violation(line: str) -> str | None:
    if NEGATION_RE.search(line):
        return None
    lowered = line.lower()
    for phrase in AUTHORITY_PHRASES:
        if phrase in lowered:
            return phrase
    return None

def _check_authority_heuristic(data: dict[str, Any], text: str, rel: str, errors: list[str]) -> None:
    allowed = data.get("allowed_actions")
    if isinstance(allowed, list):
        for action in allowed:
            token = str(action).lower()
            for forbidden in FORBIDDEN_ACTION_TOKENS:
                if forbidden in token:
                    errors.append(
                        f"{rel}: `allowed_actions` contains forbidden authority token `{action}`"
                    )
    for line in text.splitlines():
        hit = _line_claims_authority_violation(line)
        if hit:
            errors.append(f"{rel}: possible automatic authority promotion phrase `{hit}`")
            break

def _check_receipt_evidence(receipt: dict[str, Any], rel: str, warnings: list[str]) -> None:
    has_commands = isinstance(receipt.get("commands_run"), list) and receipt["commands_run"]
    has_files = isinstance(receipt.get("changed_files"), list) and receipt["changed_files"]
    if has_commands or has_files:
        return
    evidence = receipt.get("evidence")
    if isinstance(evidence, list) and evidence:
        return
    warnings.append(f"{rel}: `receipt` missing `commands_run`, `changed_files`, and evidence")

def validate_item(
    path: Path,
    *,
    repo_root: Path,
    queue_root: Path,
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    rel = repo_rel(path, repo_root)
    text = path.read_text(encoding="utf-8", errors="replace")
    data = parse_frontmatter(text)

    if not data:
        return ([f"{rel}: missing or invalid YAML frontmatter"], warnings)

    missing_core = sorted(CORE_REQUIRED_FIELDS - set(data))
    for field in missing_core:
        errors.append(f"{rel}: missing required field `{field}`")

    item_id = str(data.get("id") or "")
    if item_id and not ID_RE.fullmatch(item_id):
        errors.append(f"{rel}: invalid id `{item_id}`")
    if item_id and not path.name.startswith(item_id):
        errors.append(f"{rel}: filename must start with id `{item_id}`")

    status = str(data.get("status") or "")
    if status not in STATUS_DIRS:
        errors.append(f"{rel}: invalid status `{status}`")
    else:
        expected_dir = STATUS_DIRS[status]
        expected_path = queue_root / expected_dir
        if path.parent != expected_path:
            errors.append(
                f"{rel}: status `{status}` must live under runtime/operator-queue/{expected_dir}/"
            )

    membrane_class = str(data.get("membrane_class") or "")
    if membrane_class and membrane_class not in MEMBRANE_CLASSES:
        errors.append(f"{rel}: invalid membrane_class `{membrane_class}`")

    if "context" in data:
        _require_list(data, "context", rel, errors)
    if "definition_of_done" in data:
        _require_list(data, "definition_of_done", rel, errors)

    if "receipt_required" in data and not isinstance(data.get("receipt_required"), bool):
        errors.append(f"{rel}: `receipt_required` must be boolean")

    if not _parse_created_at(data.get("created_at")):
        errors.append(f"{rel}: `created_at` must be parseable ISO-8601")

    for field in RECOMMENDED_FIELDS:
        if field not in data:
            warnings.append(f"{rel}: missing recommended field `{field}`")

    owner = str(data.get("owner") or "")
    if owner and owner not in KNOWN_OWNERS:
        warnings.append(f"{rel}: unknown owner `{owner}`")

    if isinstance(data.get("context"), list):
        for ctx in data["context"]:
            ctx_path = repo_root / str(ctx)
            if not ctx_path.exists():
                warnings.append(f"{rel}: context path does not exist `{ctx}`")

    if status == "agent_done":
        if data.get("receipt_required") is False:
            errors.append(f"{rel}: `agent_done` cannot have `receipt_required: false`")
        receipt = data.get("receipt")
        _require_dict_keys(
            receipt,
            rel=rel,
            block_name="receipt",
            required_keys=RECEIPT_KEYS,
            errors=errors,
        )
        if isinstance(receipt, dict):
            _check_receipt_evidence(receipt, rel, warnings)

    if status == "needs_input":
        _require_dict_keys(
            data.get("blocking_question"),
            rel=rel,
            block_name="blocking_question",
            required_keys=BLOCKING_QUESTION_KEYS,
            errors=errors,
        )

    if status == "gate_required":
        _require_dict_keys(
            data.get("gate"),
            rel=rel,
            block_name="gate",
            required_keys=GATE_KEYS,
            errors=errors,
        )

    if status == "void":
        void_reason = data.get("void_reason")
        if void_reason is None or (isinstance(void_reason, str) and not void_reason.strip()):
            errors.append(f"{rel}: `void` status requires non-empty `void_reason`")

    if status == "agent_working":
        if "claimed_at" not in data:
            warnings.append(f"{rel}: missing recommended field `claimed_at` for agent_working")
        if "claimed_by" not in data:
            warnings.append(f"{rel}: missing recommended field `claimed_by` for agent_working")

    _check_authority_heuristic(data, text, rel, errors)
    return (errors, warnings)

def validate_queue(
    *,
    repo_root: Path,
    queue_root: Path,
    strict: bool,
) -> tuple[list[str], list[str], int]:
    errors: list[str] = []
    warnings: list[str] = []
    items = iter_items(queue_root)
    for item in items:
        item_errors, item_warnings = validate_item(item, repo_root=repo_root, queue_root=queue_root)
        errors.extend(item_errors)
        warnings.extend(item_warnings)
    if strict:
        errors.extend(warnings)
        warnings = []
    return errors, warnings, len(items)

GLANCE_DIRS = ("agent-todo", "needs-input")

def _item_summary(path: Path) -> tuple[str, str]:
    data = parse_frontmatter(path.read_text(encoding="utf-8", errors="replace"))
    item_id = str(data.get("id") or path.stem)
    title = str(data.get("title") or path.stem)
    return item_id, title

def render_agent_handoff_glance(*, queue_root: Path = DEFAULT_QUEUE_ROOT) -> str:
    """Compact Step 1 block: open agent-todo and needs-input items."""
    lines = ["## Agent handoff queue (open)", ""]
    found = False
    labels = {
        "agent-todo": "agent_todo",
        "needs-input": "needs_input",
    }
    for status_dir in GLANCE_DIRS:
        root = queue_root / status_dir
        if not root.is_dir():
            continue
        items = sorted(root.glob("*.md"))
        if not items:
            continue
        lines.append(f"**{labels[status_dir]}** (runtime/operator-queue/{status_dir}/):")
        for path in items:
            item_id, title = _item_summary(path)
            rel = path.relative_to(queue_root).as_posix()
            lines.append(f"- {item_id} — {title} ({rel})")
            found = True
        lines.append("")
    if not found:
        lines.append("- None in agent-todo/ or needs-input/.")
        lines.append("")
    lines.append(
        "Validate: python3 scripts/check_agent_handoff_queue.py · "
        "Doctrine: docs/agent-handoff-queue.md"
    )
    return "\n".join(lines)

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--glance", action="store_true", help="Print open handoff items for coffee Step 1")
    parser.add_argument("--queue-root", type=Path, default=DEFAULT_QUEUE_ROOT)
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    args = parser.parse_args()

    if args.glance:
        print(render_agent_handoff_glance(queue_root=args.queue_root.resolve()))
        return 0

    errors, warnings, count = validate_queue(
        repo_root=args.repo_root.resolve(),
        queue_root=args.queue_root.resolve(),
        strict=args.strict,
    )

    payload = {
        "items": count,
        "errors": errors,
        "warnings": warnings,
        "status": "ok" if not errors else "fail",
    }

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        for warning in warnings:
            print(f"warning: {warning}", file=sys.stderr)
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        if not errors and not warnings:
            print(f"[ok] agent handoff queue ({count} item(s))")

    return 1 if errors else 0

if __name__ == "__main__":
    raise SystemExit(main())
