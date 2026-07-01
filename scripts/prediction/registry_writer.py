"""Append-only event registry changelog + compile to event-registry.json."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SCRIPTS = _REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from prediction.contracts import ISRAEL_CHILD_IDS, normalize_event_v4  # noqa: E402

REGISTRY_PATH = _REPO_ROOT / "statecraft" / "data" / "event-registry.json"
CHANGELOG_PATH = _REPO_ROOT / "statecraft" / "data" / "event-registry-changelog.jsonl"


def load_registry(path: Path | None = None) -> dict[str, Any]:
    target = path or REGISTRY_PATH
    return json.loads(target.read_text(encoding="utf-8"))


def load_changelog(path: Path | None = None) -> list[dict[str, Any]]:
    target = path or CHANGELOG_PATH
    if not target.exists():
        return []
    entries: list[dict[str, Any]] = []
    for line in target.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            entries.append(json.loads(line))
    return entries


def append_changelog(
    op: str,
    payload: dict[str, Any],
    *,
    note: str = "",
    path: Path | None = None,
) -> dict[str, Any]:
    target = path or CHANGELOG_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "op": op,
        "note": note,
        **payload,
    }
    with target.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry


def apply_ops(registry: dict[str, Any], ops: list[dict[str, Any]]) -> dict[str, Any]:
    out = dict(registry)
    for entry in ops:
        op = str(entry.get("op") or "")
        if op == "upsert_event":
            event_id = str(entry["event_id"])
            event = dict(entry.get("event") or {})
            out[event_id] = normalize_event_v4(event_id, event)
        elif op == "delete_event":
            out.pop(str(entry["event_id"]), None)
        elif op == "migrate_israel_dimensions":
            parent_id = "israel_self_destruction_trajectory"
            parent = dict(out.get(parent_id) or {})
            dimensions: list[dict[str, Any]] = []
            for child_id in ISRAEL_CHILD_IDS:
                child = out.pop(child_id, None)
                if not child:
                    continue
                dimensions.append(
                    {
                        "id": child_id,
                        "label": str(child.get("question") or child_id),
                        "falsifier": child.get("falsifier") or "",
                        "confirmation_criteria": child.get("confirmation_criteria") or "",
                    }
                )
            parent["dimensions"] = dimensions
            parent.pop("child_event_ids", None)
            parent.pop("parent_event_id", None)
            out[parent_id] = normalize_event_v4(parent_id, parent)
            for child_id in ISRAEL_CHILD_IDS:
                out.pop(child_id, None)
        elif op == "normalize_all_v4":
            out = {
                eid: normalize_event_v4(eid, ev)
                for eid, ev in sorted(out.items())
            }
    return out


def compile_registry(
    *,
    registry_path: Path | None = None,
    changelog_path: Path | None = None,
    write: bool = True,
) -> dict[str, Any]:
    base = load_registry(registry_path) if (registry_path or REGISTRY_PATH).exists() else {}
    ops = load_changelog(changelog_path)
    compiled = apply_ops(base, ops)
    if write:
        target = registry_path or REGISTRY_PATH
        target.write_text(
            json.dumps(compiled, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    return compiled


def seed_v4_migration(*, write_changelog: bool = True) -> dict[str, Any]:
    registry = load_registry()
    ops = [
        {"op": "migrate_israel_dimensions"},
        {"op": "normalize_all_v4"},
    ]
    if write_changelog and not CHANGELOG_PATH.exists():
        append_changelog(
            "baseline_v4",
            {"ops": ops},
            note="Phase 3: Israel dimensions collapse + v4 field normalization",
        )
    return apply_ops(registry, ops)


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Event registry changelog writer")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("compile", help="Apply changelog and write event-registry.json")
    seed = sub.add_parser("seed-v4", help="One-time Israel dimensions migration")
    seed.add_argument("--write", action="store_true", help="Write registry + changelog")
    args = parser.parse_args()

    if args.command == "compile":
        compile_registry()
        print(f"Compiled {REGISTRY_PATH}")
        return 0

    compiled = seed_v4_migration(write_changelog=args.write)
    if args.write:
        REGISTRY_PATH.write_text(
            json.dumps(compiled, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"Wrote {REGISTRY_PATH} ({len(compiled)} events)")
    else:
        print(json.dumps({"event_count": len(compiled)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
