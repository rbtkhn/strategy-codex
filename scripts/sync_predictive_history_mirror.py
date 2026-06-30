#!/usr/bin/env python3
"""Refresh the inbound snapshot at public/predictive-history/ from rbtkhn/predictive-history."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile
from datetime import UTC, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MIRROR_REL = "public/predictive-history"
MIRROR_DIR = REPO_ROOT / MIRROR_REL
REMOTE = "https://github.com/rbtkhn/predictive-history.git"
RECEIPT_NAME = "MIRROR-RECEIPT.md"
EXCLUDE_DIRS = {".git", ".pytest_cache", "__pycache__"}

def run_git(args: list[str], cwd: Path) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=str(cwd),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        detail = proc.stderr.strip() or proc.stdout.strip() or "unknown git error"
        raise RuntimeError(f"git {' '.join(args)} failed: {detail}")
    return proc.stdout.strip()

def robocopy_mirror(src: Path, dest: Path) -> None:
    if not dest.exists():
        dest.mkdir(parents=True)
    cmd = [
        "robocopy",
        str(src),
        str(dest),
        "/MIR",
        "/NFL",
        "/NDL",
        "/NJH",
        "/NJS",
        "/nc",
        "/ns",
        "/np",
    ]
    for name in sorted(EXCLUDE_DIRS):
        cmd.extend(["/XD", name])
    proc = subprocess.run(cmd, text=True, capture_output=True, check=False)
    if proc.returncode > 7:
        raise RuntimeError(proc.stderr or proc.stdout or f"robocopy exit {proc.returncode}")

def default_operator_root() -> str:
    for key in ("PREDICTIVE_HISTORY_ROOT", "PREDICTIVE_HISTORY_ROOT", "PH_CIV_ROOT"):
        value = os.environ.get(key)
        if value:
            return value
    return r"C:\dev\predictive-history"

def write_receipt(dest: Path, upstream_sha: str, branch: str) -> None:
    operator_root = default_operator_root()
    text = (
        "# Mirror Receipt\n\n"
        f"- **Upstream:** [{REMOTE}]({REMOTE})\n"
        f"- **Branch:** `{branch}`\n"
        f"- **Upstream commit:** `{upstream_sha}`\n"
        f"- **Synced:** {datetime.now(UTC).strftime('%Y-%m-%dT%H:%M:%SZ')}\n"
        f"- **Inbound sync:** `scripts/sync_predictive_history_mirror.py`\n"
        f"- **Operator workspace:** `{operator_root}` (`PREDICTIVE_HISTORY_ROOT`)\n\n"
        "**Inbound read-only snapshot.** Do not edit corpus files here. "
        "Author in the canonical repo; refresh this tree with inbound sync only. "
        "See [DO-NOT-EDIT.md](DO-NOT-EDIT.md) and "
        "[docs/predictive-history-operator-workspace.md](../../docs/predictive-history-operator-workspace.md).\n"
    )
    (dest / RECEIPT_NAME).write_text(text, encoding="utf-8")

def sync(branch: str) -> dict:
    with tempfile.TemporaryDirectory(prefix="predictive-history-sync-") as tmp:
        clone_root = Path(tmp) / "predictive-history"
        run_git(["clone", "--depth", "1", "--branch", branch, REMOTE, str(clone_root)], REPO_ROOT)
        upstream_sha = run_git(["rev-parse", "HEAD"], clone_root)
        robocopy_mirror(clone_root, MIRROR_DIR)
        write_receipt(MIRROR_DIR, upstream_sha, branch)
        return {
            "mirror_path": MIRROR_REL,
            "upstream_sha": upstream_sha,
            "branch": branch,
            "remote": REMOTE,
        }

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--branch", default="main")
    args = parser.parse_args(argv)
    try:
        result = sync(branch=args.branch)
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"Synced {result['mirror_path']} @ {result['upstream_sha']} from {result['remote']}")
    print("Commit with tag [predictive-history-sync] in the message.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
