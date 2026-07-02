#!/usr/bin/env python3
"""Run repo-wide convergence loops for generated artifacts and validators."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from collections import deque
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from repo_convergence_registry import LOOPS, LoopSpec  # noqa: E402
from repo_io import ARTIFACTS_DIR, REPO_ROOT  # noqa: E402

REPORT_PATH = ARTIFACTS_DIR / "repo-convergence-report.json"
STATE_PATH = ARTIFACTS_DIR / "repo-convergence-state.json"
LOG_PATH = REPO_ROOT / "runtime" / "operator-events" / "repo-convergence.jsonl"

HASH_EXCLUDE_PATHS = {
    "runtime/artifacts/repo-convergence-report.json",
    "runtime/artifacts/repo-convergence-state.json",
    "runtime/operator-events/repo-convergence.jsonl",
}

@dataclass
class CommandResult:
    cmd: list[str]
    returncode: int
    stdout_tail: str
    stderr_tail: str

def utc_now() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )

def repo_path(rel: str) -> Path:
    return REPO_ROOT / rel

def repo_rel(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()

def should_hash_path(path: Path) -> bool:
    return repo_rel(path) not in HASH_EXCLUDE_PATHS

def hash_paths(paths: tuple[str, ...] | list[str]) -> str:
    h = hashlib.sha256()
    for raw in sorted(paths):
        root = repo_path(raw)
        if not root.exists():
            if raw not in HASH_EXCLUDE_PATHS:
                h.update(f"missing:{raw}".encode("utf-8"))
            continue
        if root.is_file():
            if should_hash_path(root):
                h.update(raw.encode("utf-8"))
                h.update(root.read_bytes())
            continue
        for p in sorted(root.rglob("*")):
            if p.is_file() and should_hash_path(p):
                rel = p.relative_to(REPO_ROOT).as_posix()
                h.update(rel.encode("utf-8"))
                h.update(p.read_bytes())
    return h.hexdigest()

def load_state() -> dict[str, Any]:
    if not STATE_PATH.exists():
        return {}
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))

def save_state(state: dict[str, Any]) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")

def tail(text: str, lines: int = 8) -> str:
    parts = text.strip().splitlines()
    return "\n".join(parts[-lines:]) if parts else ""

def normalize_cmd(cmd: tuple[str, ...] | list[str]) -> list[str]:
    parts = list(cmd)
    if not parts:
        raise ValueError("empty command")
    if parts[0] in ("python3", "python"):
        return [sys.executable, *parts[1:]]
    if parts[0].startswith("scripts/"):
        return [sys.executable, *parts]
    return parts

def run_command(cmd: tuple[str, ...] | list[str]) -> CommandResult:
    argv = normalize_cmd(cmd)
    proc = subprocess.run(
        argv,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    return CommandResult(
        cmd=argv,
        returncode=proc.returncode,
        stdout_tail=tail(proc.stdout),
        stderr_tail=tail(proc.stderr),
    )

def append_log(event: dict[str, Any]) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, sort_keys=True) + "\n")

def topo_sort_loops(names: list[str]) -> list[str]:
    name_set = set(names)
    for name in names:
        spec = LOOPS[name]
        for dep in spec.depends_on:
            if dep not in LOOPS:
                raise SystemExit(f"unknown dependency {dep!r} for loop {name!r}")
            if dep not in name_set:
                name_set.add(dep)

    expanded = sorted(name_set)
    indegree = {name: 0 for name in expanded}
    dependents: dict[str, list[str]] = {name: [] for name in expanded}
    for name in expanded:
        for dep in LOOPS[name].depends_on:
            if dep not in indegree:
                continue
            indegree[name] += 1
            dependents[dep].append(name)

    queue = deque(sorted(name for name, deg in indegree.items() if deg == 0))
    ordered: list[str] = []
    while queue:
        name = queue.popleft()
        ordered.append(name)
        for child in sorted(dependents[name]):
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)

    if len(ordered) != len(expanded):
        raise SystemExit("cycle detected in loop dependency graph")
    return ordered

def closure_with_deps(loop_name: str) -> list[str]:
    if loop_name not in LOOPS:
        raise SystemExit(f"unknown loop: {loop_name}")
    needed: set[str] = set()
    stack = [loop_name]
    while stack:
        name = stack.pop()
        if name in needed:
            continue
        needed.add(name)
        stack.extend(LOOPS[name].depends_on)
    return topo_sort_loops(sorted(needed))

def mark_transitive_dependents_dirty(source: str, dirty: set[str]) -> None:
    for name, spec in LOOPS.items():
        if source in spec.depends_on and name not in dirty:
            dirty.add(name)
            mark_transitive_dependents_dirty(name, dirty)

def selected_loop_names(loop_name: str | None) -> list[str]:
    if loop_name:
        return closure_with_deps(loop_name)
    return topo_sort_loops(sorted(LOOPS))

def explain_loops(*, as_json: bool) -> int:
    payload = {
        name: {
            "kind": spec.kind,
            "description": spec.description,
            "inputs": list(spec.inputs),
            "writes": list(spec.writes),
            "depends_on": list(spec.depends_on),
            "commands": [" ".join(normalize_cmd(cmd)) for cmd in spec.commands],
        }
        for name, spec in LOOPS.items()
    }
    if as_json:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0
    for name in topo_sort_loops(sorted(LOOPS)):
        spec = LOOPS[name]
        print(f"Loop: {name}")
        print(f"  Kind: {spec.kind}")
        if spec.description:
            print(f"  Description: {spec.description}")
        print("  Inputs:")
        for path in spec.inputs:
            print(f"    - {path}")
        if spec.writes:
            print("  Writes:")
            for path in spec.writes:
                print(f"    - {path}")
        print("  Depends on:")
        if spec.depends_on:
            for dep in spec.depends_on:
                print(f"    - {dep}")
        else:
            print("    - none")
        print("  Commands:")
        for cmd in spec.commands:
            print(f"    - {' '.join(normalize_cmd(cmd))}")
        print()
    return 0

def maybe_append_log(event: dict[str, Any], *, record_run: bool) -> None:
    if record_run:
        append_log(event)

def run_loops(
    *,
    mode_name: str,
    loop_names: list[str],
    force_all: bool,
    quiet: bool,
    record_run: bool,
) -> tuple[dict[str, Any], dict[str, Any], int]:
    old_state = load_state()
    old_hashes = old_state.get("hashes", {})
    generated_at = utc_now()
    new_state: dict[str, Any] = {"generated_at": generated_at, "hashes": dict(old_hashes)}

    report: dict[str, Any] = {
        "status": "ok",
        "mode": mode_name,
        "generated_at": generated_at,
        "recorded": record_run,
        "hash_exclusions": sorted(HASH_EXCLUDE_PATHS),
        "loops": {},
        "gate_required": [],
        "errors": [],
    }

    input_hashes = {name: hash_paths(LOOPS[name].inputs) for name in loop_names}
    dirty: set[str] = set()
    for name in loop_names:
        if force_all or input_hashes[name] != old_hashes.get(name):
            dirty.add(name)

    propagated = True
    while propagated:
        propagated = False
        for name in loop_names:
            if name in dirty:
                continue
            if any(dep in dirty for dep in LOOPS[name].depends_on):
                dirty.add(name)
                propagated = True

    rc = 0
    for name in loop_names:
        spec = LOOPS[name]
        input_hash = input_hashes[name]
        inputs_changed = input_hash != old_hashes.get(name)
        is_dirty = name in dirty

        loop_report: dict[str, Any] = {
            "kind": spec.kind,
            "input_hash": input_hash,
            "inputs_changed": inputs_changed,
            "changed": is_dirty,
            "writes": list(spec.writes),
            "commands": [],
        }

        should_run_validator = spec.kind == "validator" and (is_dirty or force_all)
        should_run_builder = spec.kind == "builder" and mode_name == "write" and (is_dirty or force_all)

        if spec.kind == "builder" and mode_name != "write":
            if is_dirty or force_all:
                loop_report["status"] = "needs_write"
                if report["status"] == "ok":
                    report["status"] = "needs_attention"
            else:
                loop_report["status"] = "ok"
            report["loops"][name] = loop_report
            new_state["hashes"][name] = input_hash
            continue

        if spec.kind == "validator" and not should_run_validator:
            loop_report["status"] = "skipped"
            report["loops"][name] = loop_report
            new_state["hashes"][name] = input_hash
            maybe_append_log(
                {
                    "timestamp": utc_now(),
                    "loop": name,
                    "status": "skipped",
                    "mode": mode_name,
                },
                record_run=record_run,
            )
            continue

        if spec.kind == "builder" and not should_run_builder:
            loop_report["status"] = "ok"
            report["loops"][name] = loop_report
            new_state["hashes"][name] = input_hash
            continue

        loop_status = "ok"
        for cmd in spec.commands:
            if not quiet:
                print(f"[run] {name}: {' '.join(normalize_cmd(cmd))}")
            result = run_command(cmd)
            loop_report["commands"].append(
                {
                    "cmd": " ".join(result.cmd),
                    "returncode": result.returncode,
                    "stdout_tail": result.stdout_tail,
                    "stderr_tail": result.stderr_tail,
                }
            )
            if result.returncode != 0:
                loop_status = "fail"
                report["status"] = "fail"
                report["errors"].append(
                    {
                        "loop": name,
                        "cmd": " ".join(result.cmd),
                        "returncode": result.returncode,
                        "stderr_tail": result.stderr_tail,
                    }
                )
                rc = result.returncode or 1
                break

        if loop_status == "ok" and spec.kind == "builder" and (is_dirty or force_all):
            loop_status = "rebuilt"
            mark_transitive_dependents_dirty(name, dirty)
            for dependent in loop_names:
                if dependent in dirty and dependent != name:
                    input_hashes[dependent] = hash_paths(LOOPS[dependent].inputs)

        loop_report["status"] = loop_status
        report["loops"][name] = loop_report
        new_state["hashes"][name] = hash_paths(spec.inputs)

        maybe_append_log(
            {
                "timestamp": utc_now(),
                "loop": name,
                "status": loop_report["status"],
                "mode": mode_name,
            },
            record_run=record_run,
        )

        if not quiet:
            print(f"[{loop_report['status']}] {name}")

    return report, new_state, rc

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="Non-mutating check mode (default)")
    mode.add_argument("--write", action="store_true", help="Allow declared derived writes")
    parser.add_argument("--explain", action="store_true", help="Print loop graph and exit")
    parser.add_argument("--loop", help="Run one loop and its dependencies")
    parser.add_argument("--all", action="store_true", help="Run even unchanged loops")
    parser.add_argument("--json", action="store_true", help="Print report JSON to stdout")
    parser.add_argument("--quiet", action="store_true", help="Suppress command chatter")
    parser.add_argument("--strict", action="store_true", help="Fail on needs_write or errors")
    parser.add_argument(
        "--record-report",
        action="store_true",
        help="Write report/log artifacts even in check mode",
    )
    args = parser.parse_args()

    if args.explain:
        return explain_loops(as_json=args.json)

    mode_name = "write" if args.write else "check"
    record_run = args.write or args.record_report
    loop_names = selected_loop_names(args.loop)
    report, new_state, rc = run_loops(
        mode_name=mode_name,
        loop_names=loop_names,
        force_all=args.all,
        quiet=args.quiet,
        record_run=record_run,
    )

    if record_run:
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if mode_name == "write" and rc == 0:
        save_state(new_state)

    if args.strict:
        if report["status"] in ("needs_attention", "fail"):
            rc = rc or 1

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    elif not args.quiet:
        if record_run:
            rel = REPORT_PATH.relative_to(REPO_ROOT)
            print(f"[{report['status']}] wrote {rel.as_posix()}")
        else:
            print(f"[{report['status']}] check complete; report not written")

    return rc

if __name__ == "__main__":
    raise SystemExit(main())
