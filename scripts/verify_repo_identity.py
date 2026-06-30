#!/usr/bin/env python3
"""Verify that this checkout is the active strategy-codex repo.

Read-only guard for fresh chats and pre-ship checks. It is deliberately narrow:
it verifies the current Git checkout identity rather than trying to infer every
possible workspace relationship.
"""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path
from typing import Callable

EXPECTED_REPO_NAME = "strategy-codex"
EXPECTED_ORIGIN = "https://github.com/rbtkhn/strategy-codex.git"

REPO_ROOT = Path(__file__).resolve().parent.parent

Runner = Callable[[list[str], Path], tuple[int, str, str]]

def _run(argv: list[str], cwd: Path) -> tuple[int, str, str]:
    result = subprocess.run(
        argv,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=8,
        check=False,
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()

def _origin_protocol(remote: str) -> str:
    if remote.startswith("https://"):
        return "https"
    if remote.startswith("git@"):
        return "ssh"
    return "unknown"

def verify_repo_identity(
    repo_root: Path = REPO_ROOT,
    *,
    runner: Runner = _run,
) -> tuple[bool, list[str]]:
    """Return ``(ok, receipt_lines)`` for the active checkout identity."""
    lines: list[str] = []
    ok = True

    code, top, err = runner(["git", "rev-parse", "--show-toplevel"], repo_root)
    if code != 0 or not top:
        return False, [f"git root unavailable: {err or 'git rev-parse failed'}"]

    root = Path(top)
    root_name = root.name
    if root_name != EXPECTED_REPO_NAME:
        ok = False
        lines.append(f"root-name={root_name} expected={EXPECTED_REPO_NAME}")
    else:
        lines.append(f"root-name={root_name}")

    code, origin, err = runner(["git", "remote", "get-url", "origin"], root)
    if code != 0 or not origin:
        ok = False
        lines.append(f"origin=missing ({err or 'git remote get-url failed'})")
    elif origin != EXPECTED_ORIGIN:
        ok = False
        lines.append(f"origin={origin} expected={EXPECTED_ORIGIN}")
    else:
        lines.append(f"origin={_origin_protocol(origin)} rbtkhn/strategy-codex")

    agents = root / "AGENTS.md"
    if not agents.is_file():
        ok = False
        lines.append("AGENTS.md=missing")
    else:
        text = agents.read_text(encoding="utf-8", errors="replace")
        if "Active repo identity:" in text and "`strategy-codex`" in text:
            lines.append("AGENTS=active strategy-codex")
        else:
            ok = False
            lines.append("AGENTS=missing active strategy-codex identity")

    return ok, lines

def format_repo_identity_status(repo_root: Path = REPO_ROOT) -> str:
    """Compact one-line status for coffee bootstrap."""
    ok, lines = verify_repo_identity(repo_root)
    prefix = "ok" if ok else "FAIL"
    return f"{prefix} - " + "; ".join(lines)

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=REPO_ROOT)
    args = parser.parse_args()

    ok, lines = verify_repo_identity(args.root)
    print(("OK" if ok else "FAIL") + " repo identity")
    for line in lines:
        print(f"- {line}")
    return 0 if ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
