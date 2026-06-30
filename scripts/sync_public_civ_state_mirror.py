#!/usr/bin/env python3
"""Refresh the vendored public/civ-state workspace copy from rbtkhn/civ-state (inbound pull only)."""

from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from datetime import UTC, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MIRROR_REL = "public/civ-state"
MIRROR_DIR = REPO_ROOT / MIRROR_REL
REMOTE = "https://github.com/rbtkhn/civ-state.git"
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

def write_receipt(dest: Path, upstream_sha: str, branch: str) -> None:
    text = (
        "# Mirror Receipt\n\n"
        f"- **Upstream:** [{REMOTE}]({REMOTE})\n"
        f"- **Branch:** `{branch}`\n"
        f"- **Upstream commit:** `{upstream_sha}`\n"
        f"- **Synced:** {datetime.now(UTC).strftime('%Y-%m-%dT%H:%M:%SZ')}\n"
        f"- **Inbound sync:** `scripts/sync_public_civ_state_mirror.py`\n"
        f"- **Outbound publish:** `scripts/publish_public_civ_state.py`\n\n"
        "Workspace staging copy. Edit under `public/civ-state/`; push upstream only via publish script.\n"
    )
    (dest / RECEIPT_NAME).write_text(text, encoding="utf-8")

def sync(branch: str) -> dict:
    with tempfile.TemporaryDirectory(prefix="civ-state-sync-") as tmp:
        clone_root = Path(tmp) / "civ-state"
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
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
