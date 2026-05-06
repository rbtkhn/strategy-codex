#!/usr/bin/env python3
"""Build a typed Conductor delegation brief and receipt skeleton.

V1 is generate-only: it writes a WORK-only brief and receipt skeleton. It does
not spawn agents, call an LLM, stage git changes, edit the gate, or merge the
Record.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = REPO_ROOT / "config" / "conductor-delegation-types.json"
TEMPLATE_PATH = (
    REPO_ROOT
    / "docs"
    / "skill-work"
    / "work-dev"
    / "templates"
    / "conductor-delegation"
    / "base-brief.md"
)
DEFAULT_OUTPUT_DIR = REPO_ROOT / "artifacts" / "work-dev" / "conductor-delegations"
CONDUCTORS = ("toscanini", "furtwangler", "karajan", "kleiber", "bernstein")


def load_registry(path: Path = REGISTRY_PATH) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _slugify(value: str, *, max_len: int = 48) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return slug[:max_len].strip("-") or "task"


def _bullet_list(values: list[str]) -> str:
    if not values:
        return "- _None specified._"
    return "\n".join(f"- {value}" for value in values)


def _read_optional_brief(path: Path | None) -> str:
    if path is None:
        return "_None provided._"
    return path.read_text(encoding="utf-8").strip() or "_Provided brief was empty._"


def _brief_input_line(path: Path | None) -> str:
    if path is None:
        return "- _None specified._"
    try:
        display = path.relative_to(REPO_ROOT)
    except ValueError:
        display = path
    return f"- Additional brief file: `{display}`"


def _render_template(template: str, values: dict[str, str]) -> str:
    rendered = template
    for key, value in values.items():
        rendered = rendered.replace("{{" + key + "}}", value)
    return rendered


def build_delegation(
    *,
    delegation_type: str,
    task: str,
    conductor: str,
    brief_file: Path | None = None,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    now: datetime | None = None,
) -> tuple[Path, Path]:
    registry = load_registry()
    types = registry.get("types", {})
    if delegation_type not in types:
        available = ", ".join(sorted(types))
        raise ValueError(f"Unknown delegation type {delegation_type!r}. Available: {available}")
    if conductor not in CONDUCTORS:
        available = ", ".join(CONDUCTORS)
        raise ValueError(f"Unknown conductor {conductor!r}. Available: {available}")

    type_config = types[delegation_type]
    now_dt = now or datetime.now(timezone.utc)
    stamp = now_dt.strftime("%Y%m%d-%H%M%S")
    created_at = now_dt.isoformat().replace("+00:00", "Z")
    delegation_id = f"cdel-{stamp}-{delegation_type}"
    task_slug = _slugify(task)

    output_dir.mkdir(parents=True, exist_ok=True)
    brief_path = output_dir / f"{delegation_id}-{task_slug}-brief.md"
    receipt_path = output_dir / f"{delegation_id}-{task_slug}-receipt.json"

    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    brief_text = _render_template(
        template,
        {
            "delegation_id": delegation_id,
            "type": delegation_type,
            "type_label": str(type_config["label"]),
            "conductor": conductor,
            "created_at": created_at,
            "task": task,
            "type_purpose": str(type_config["purpose"]),
            "authority_boundary": str(type_config["authority_boundary"]),
            "suggested_scope": _bullet_list(list(type_config.get("suggested_scope", []))),
            "evidence_inputs": _brief_input_line(brief_file),
            "output_expectations": _bullet_list(list(type_config.get("output_expectations", []))),
            "additional_brief_context": _read_optional_brief(brief_file),
        },
    )
    brief_path.write_text(brief_text.rstrip() + "\n", encoding="utf-8")

    receipt = {
        "schema_version": "1.0.0-conductor-delegation-receipt",
        "delegation_id": delegation_id,
        "type": delegation_type,
        "task": task,
        "conductor": conductor,
        "created_at": created_at,
        "status": "brief_created",
        "work_only": True,
        "record_authority": "none",
        "gate_effect": "none",
        "operator_choice_context": {
            "source": "conductor_action_menu",
            "menu_policy": "at_most_one_typed_delegation_option",
        },
        "close_loop": {
            "closed": False,
            "outcome": None,
            "falsify": None,
            "followup": None,
            "next_menu_adjustment": None,
        },
        "paths": {
            "brief": str(brief_path.relative_to(REPO_ROOT)).replace("\\", "/"),
            "receipt": str(receipt_path.relative_to(REPO_ROOT)).replace("\\", "/"),
        },
    }
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    return brief_path, receipt_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--type", required=True, choices=("explore", "plan", "review", "reflection"))
    parser.add_argument("--task", required=True)
    parser.add_argument("--conductor", required=True, choices=CONDUCTORS)
    parser.add_argument("--brief-file", type=Path, default=None)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    brief_file = args.brief_file
    if brief_file is not None and not brief_file.is_absolute():
        brief_file = REPO_ROOT / brief_file
    output_dir = args.output_dir if args.output_dir.is_absolute() else REPO_ROOT / args.output_dir

    brief_path, receipt_path = build_delegation(
        delegation_type=args.type,
        task=args.task,
        conductor=args.conductor,
        brief_file=brief_file,
        output_dir=output_dir,
    )
    print(f"wrote {brief_path.relative_to(REPO_ROOT)}")
    print(f"wrote {receipt_path.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
