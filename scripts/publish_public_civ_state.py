#!/usr/bin/env python3
"""Publish staged edits from public/civ-state to rbtkhn/civ-state (explicit outbound only)."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))
from academy_mirror_git import git_commit, git_output, push_branch, sync_clone_branch

REPO_ROOT = Path(__file__).resolve().parent.parent
MIRROR_REL = "public/civ-state"
MIRROR_DIR = REPO_ROOT / MIRROR_REL
REMOTE = "https://github.com/rbtkhn/civ-state.git"
RECEIPT_NAME = "docs/MIRROR-RECEIPT.md"
DEFAULT_CLONE = Path(os.environ.get("CIV_STATE_PUBLISH_CLONE", r"C:\dev\civ-state"))
EXCLUDE_DIRS = {".git", ".pytest_cache", "__pycache__"}
WORKSPACE_ONLY_FILES = {RECEIPT_NAME}


def robocopy_publish(src: Path, dest: Path, *, dry_run: bool) -> None:
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
    if dry_run:
        cmd.append("/L")
    for name in sorted(EXCLUDE_DIRS):
        cmd.extend(["/XD", name])
    for name in sorted(WORKSPACE_ONLY_FILES):
        cmd.extend(["/XF", name])
    proc = subprocess.run(cmd, text=True, capture_output=True, check=False)
    if not dry_run and proc.returncode > 7:
        raise RuntimeError(proc.stderr or proc.stdout or f"robocopy exit {proc.returncode}")


def write_receipt(upstream_sha: str, branch: str) -> None:
    text = (
        "# Mirror Receipt\n\n"
        f"- **Upstream:** [{REMOTE}]({REMOTE})\n"
        f"- **Branch:** `{branch}`\n"
        f"- **Upstream commit:** `{upstream_sha}`\n"
        f"- **Published:** {datetime.now(UTC).strftime('%Y-%m-%dT%H:%M:%SZ')}\n"
        f"- **Inbound sync:** `scripts/sync_public_civ_state_mirror.py`\n"
        f"- **Outbound publish:** `scripts/publish_public_civ_state.py`\n\n"
        "Workspace staging copy of public Civilizational Statecraft. "
        "Edit ship-bound prose only under `public/civ-state/`; "
        "push to GitHub only via the publish script.\n"
    )
    (MIRROR_DIR / RECEIPT_NAME).write_text(text, encoding="utf-8")


def ensure_clone(clone_dir: Path, branch: str) -> None:
    if (clone_dir / ".git").exists():
        sync_clone_branch(clone_dir, branch, REMOTE)
        return
    clone_dir.parent.mkdir(parents=True, exist_ok=True)
    git_output(["clone", "--branch", branch, REMOTE, str(clone_dir)], REPO_ROOT)


def publish(
    *,
    clone_dir: Path,
    branch: str,
    message: str | None,
    dry_run: bool,
    do_push: bool,
) -> dict:
    if not MIRROR_DIR.is_dir():
        raise RuntimeError(f"mirror missing: {MIRROR_REL}")

    if dry_run:
        if clone_dir.exists() and (clone_dir / ".git").exists():
            robocopy_publish(MIRROR_DIR, clone_dir, dry_run=True)
        return {"status": "dry_run", "mirror_path": MIRROR_REL, "clone_dir": str(clone_dir)}

    ensure_clone(clone_dir, branch)
    robocopy_publish(MIRROR_DIR, clone_dir, dry_run=False)

    status = git_output(["status", "--short"], clone_dir)
    if not status:
        return {"status": "no_changes", "mirror_path": MIRROR_REL, "clone_dir": str(clone_dir)}

    if not message:
        raise RuntimeError("commit message required (--message) when publish would commit")

    git_commit(clone_dir, message)
    head = git_output(["rev-parse", "HEAD"], clone_dir)

    pushed = False
    push_via = None
    if do_push:
        push_via = push_branch(clone_dir, branch, REMOTE)
        pushed = True
        write_receipt(head, branch)

    return {
        "status": "published" if pushed else "committed_local",
        "mirror_path": MIRROR_REL,
        "clone_dir": str(clone_dir),
        "commit": head,
        "pushed": pushed,
        "push_via": push_via,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--clone-dir", type=Path, default=DEFAULT_CLONE)
    parser.add_argument("--branch", default="main")
    parser.add_argument("--message", "-m", help="Commit message in civ-state clone")
    parser.add_argument("--dry-run", action="store_true", help="List robocopy changes only")
    parser.add_argument(
        "--push",
        action="store_true",
        help="Push commit to origin after robocopy (required for public ship)",
    )
    args = parser.parse_args(argv)

    try:
        result = publish(
            clone_dir=args.clone_dir,
            branch=args.branch,
            message=args.message,
            dry_run=args.dry_run,
            do_push=args.push,
        )
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
