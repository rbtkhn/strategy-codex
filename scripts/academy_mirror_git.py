#!/usr/bin/env python3
"""Shared git helpers for academy mirror publish scripts (no repo config writes)."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

DEFAULT_COMMITTER_NAME = "Robert Kuhne"
DEFAULT_COMMITTER_EMAIL = "rbtkhn@users.noreply.github.com"

def committer_name() -> str:
    return os.environ.get("ACADEMY_MIRROR_GIT_USER_NAME", DEFAULT_COMMITTER_NAME)

def committer_email() -> str:
    return os.environ.get("ACADEMY_MIRROR_GIT_USER_EMAIL", DEFAULT_COMMITTER_EMAIL)

def commit_identity_args() -> list[str]:
    return [
        "-c",
        f"user.name={committer_name()}",
        "-c",
        f"user.email={committer_email()}",
    ]

def ssh_remote_from_https(remote_url: str) -> str:
    prefix = "https://github.com/"
    if not remote_url.startswith(prefix):
        raise ValueError(f"unsupported remote URL for SSH fallback: {remote_url}")
    slug = remote_url[len(prefix) :].removesuffix(".git")
    return f"git@github.com:{slug}"

def git_output(args: list[str], cwd: Path, *, identity: bool = False) -> str:
    prefix = commit_identity_args() if identity else []
    proc = subprocess.run(
        ["git", *prefix, *args],
        cwd=str(cwd),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        detail = proc.stderr.strip() or proc.stdout.strip() or "unknown git error"
        raise RuntimeError(f"git {' '.join(args)} failed in {cwd}: {detail}")
    return proc.stdout.strip()

def sync_clone_branch(clone_dir: Path, branch: str, remote_url: str) -> None:
    if not (clone_dir / ".git").exists():
        raise RuntimeError(f"clone missing git dir: {clone_dir}")
    try:
        git_output(["fetch", "origin"], clone_dir)
        git_output(["checkout", branch], clone_dir)
        git_output(["pull", "--ff-only", "origin", branch], clone_dir)
    except RuntimeError:
        ssh = ssh_remote_from_https(remote_url)
        git_output(["fetch", ssh, branch], clone_dir)
        git_output(["checkout", branch], clone_dir)
        git_output(["merge", "--ff-only", "FETCH_HEAD"], clone_dir)

def git_commit(clone_dir: Path, message: str) -> None:
    git_output(["add", "-A"], clone_dir)
    git_output(["commit", "-m", message], clone_dir, identity=True)

def push_branch(clone_dir: Path, branch: str, remote_url: str) -> str:
    try:
        git_output(["push", "origin", branch], clone_dir)
        return "https"
    except RuntimeError as https_error:
        ssh = ssh_remote_from_https(remote_url)
        try:
            git_output(["push", ssh, branch], clone_dir)
            return "ssh"
        except RuntimeError as ssh_error:
            raise RuntimeError(
                f"git push failed over HTTPS and SSH in {clone_dir}: "
                f"https={https_error}; ssh={ssh_error}"
            ) from ssh_error
