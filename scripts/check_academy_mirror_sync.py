#!/usr/bin/env python3
"""Check that an academy mirror folder, its remote, and the parent gitlink agree."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MIRROR = "codex/academy/ph-civ"


def run_git(args: list[str], cwd: Path) -> tuple[int, str, str]:
    safe_cwd = cwd.resolve().as_posix()
    safe_root = REPO_ROOT.resolve().as_posix()
    proc = subprocess.run(
        ["git", "-c", f"safe.directory={safe_cwd}", "-c", f"safe.directory={safe_root}", *args],
        cwd=str(cwd),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def git_output(args: list[str], cwd: Path) -> str:
    code, out, err = run_git(args, cwd)
    if code != 0:
        detail = err or out or "unknown git error"
        raise RuntimeError(f"git {' '.join(args)} failed in {cwd}: {detail}")
    return out


def parent_gitlink_sha(mirror_rel: str) -> str | None:
    output = git_output(["ls-files", "-s", mirror_rel], REPO_ROOT)
    if not output:
        return None
    parts = output.split()
    if len(parts) < 2:
        return None
    return parts[1]


def status_dirty(status_short: str) -> bool:
    return any(line and not line.startswith("## ") for line in status_short.splitlines())


def check_sync(mirror_rel: str, remote: str, branch: str, fetch: bool) -> dict:
    mirror_path = (REPO_ROOT / mirror_rel).resolve()
    result: dict = {
        "mirror_path": mirror_rel,
        "remote": remote,
        "branch": branch,
        "fetch_attempted": fetch,
        "fetch_ok": None,
        "checks": {},
        "errors": [],
    }

    if not mirror_path.exists():
        result["errors"].append(f"mirror path missing: {mirror_rel}")
        result["status"] = "invalid"
        return result

    status_short = git_output(["status", "--short", "--branch"], mirror_path)
    nested_head = git_output(["rev-parse", "HEAD"], mirror_path)
    result["nested_head"] = nested_head
    result["nested_status"] = status_short
    result["checks"]["nested_clean"] = not status_dirty(status_short)

    if fetch:
        code, out, err = run_git(["fetch", remote], mirror_path)
        result["fetch_ok"] = code == 0
        if code != 0:
            result["errors"].append(f"fetch failed: {err or out}")
    else:
        result["fetch_ok"] = False

    remote_ref = f"{remote}/{branch}"
    try:
        remote_head = git_output(["rev-parse", remote_ref], mirror_path)
    except RuntimeError as exc:
        remote_head = None
        result["errors"].append(str(exc))
    result["remote_head"] = remote_head
    result["checks"]["nested_matches_remote"] = nested_head == remote_head

    gitlink_sha = parent_gitlink_sha(mirror_rel)
    result["parent_gitlink"] = gitlink_sha
    result["checks"]["parent_gitlink_matches_nested"] = gitlink_sha == nested_head

    code, _, _ = run_git(["diff", "--quiet", "--", mirror_rel], REPO_ROOT)
    result["checks"]["parent_has_no_mirror_diff"] = code == 0

    checks_ok = all(result["checks"].values())
    if checks_ok and not result["errors"]:
        result["status"] = "synced"
    elif checks_ok and result["errors"]:
        result["status"] = "remote_unverified"
    else:
        result["status"] = "out_of_sync"
    return result


def emit_text(result: dict) -> None:
    print(f"academy mirror: {result['mirror_path']}")
    print(f"status: {result['status']}")
    if result.get("nested_head"):
        print(f"nested_head: {result['nested_head']}")
    if result.get("remote_head"):
        print(f"remote_head: {result['remote_head']}")
    if result.get("parent_gitlink"):
        print(f"parent_gitlink: {result['parent_gitlink']}")
    if result.get("fetch_attempted"):
        print(f"fetch_ok: {'ok' if result.get('fetch_ok') else 'fail'}")
    for name, passed in result.get("checks", {}).items():
        print(f"{name}: {'ok' if passed else 'fail'}")
    for error in result.get("errors", []):
        print(f"error: {error}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mirror", default=DEFAULT_MIRROR)
    parser.add_argument("--remote", default="origin")
    parser.add_argument("--branch", default="main")
    parser.add_argument("--no-fetch", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    result = check_sync(
        mirror_rel=args.mirror,
        remote=args.remote,
        branch=args.branch,
        fetch=not args.no_fetch,
    )
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        emit_text(result)
    return 0 if result["status"] == "synced" else 1


if __name__ == "__main__":
    raise SystemExit(main())
