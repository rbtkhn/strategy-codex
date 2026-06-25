#!/usr/bin/env python3
"""Check that a vendored academy mirror matches its upstream receipt and remote."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
RECEIPT_NAME = "MIRROR-RECEIPT.md"
UPSTREAM_SHA_RE = re.compile(r"^\-\s\*\*Upstream commit:\*\*\s`([0-9a-f]{7,40})`", re.MULTILINE)

PUBLIC_MIRRORS = {
    "predictive-history": {
        "path": "public/predictive-history",
        "remote": "https://github.com/rbtkhn/predictive-history.git",
    },
    "ph-civ": {
        "path": "public/predictive-history",
        "remote": "https://github.com/rbtkhn/predictive-history.git",
    },
    "civ-state": {
        "path": "public/civ-state",
        "remote": "https://github.com/rbtkhn/civ-state.git",
    },
}
DEFAULT_MIRROR = PUBLIC_MIRRORS["predictive-history"]["path"]


def run_git(args: list[str], cwd: Path) -> tuple[int, str, str]:
    proc = subprocess.run(
        ["git", *args],
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


def read_receipt_sha(mirror_dir: Path) -> str | None:
    receipt = mirror_dir / RECEIPT_NAME
    if not receipt.is_file():
        return None
    match = UPSTREAM_SHA_RE.search(receipt.read_text(encoding="utf-8"))
    return match.group(1) if match else None


def remote_main_head(remote_url: str, branch: str, fetch: bool) -> tuple[str | None, list[str]]:
    errors: list[str] = []
    if not fetch:
        return None, ["fetch skipped"]
    with tempfile.TemporaryDirectory(prefix="ph-civ-check-") as tmp:
        clone_root = Path(tmp) / "ph-civ"
        code, _, err = run_git(
            ["clone", "--depth", "1", "--branch", branch, remote_url, str(clone_root)],
            REPO_ROOT,
        )
        if code != 0:
            errors.append(err or "clone failed")
            return None, errors
        return git_output(["rev-parse", "HEAD"], clone_root), errors


def check_sync(mirror_rel: str, remote_url: str, branch: str, fetch: bool) -> dict:
    mirror_path = (REPO_ROOT / mirror_rel).resolve()
    result: dict = {
        "mirror_path": mirror_rel,
        "remote": remote_url,
        "branch": branch,
        "mode": "vendored",
        "fetch_attempted": fetch,
        "checks": {},
        "errors": [],
    }

    if not mirror_path.is_dir():
        result["errors"].append(f"mirror path missing: {mirror_rel}")
        result["status"] = "invalid"
        return result

    receipt_sha = read_receipt_sha(mirror_path)
    result["receipt_sha"] = receipt_sha
    result["checks"]["receipt_present"] = receipt_sha is not None

    code, _, _ = run_git(["diff", "--quiet", "--", mirror_rel], REPO_ROOT)
    result["checks"]["parent_has_no_mirror_diff"] = code == 0

    remote_head, remote_errors = remote_main_head(remote_url, branch, fetch)
    result["remote_head"] = remote_head
    result["errors"].extend(remote_errors)
    if remote_head:
        result["checks"]["receipt_matches_remote"] = receipt_sha == remote_head
    else:
        result["checks"]["receipt_matches_remote"] = False

    checks_ok = all(result["checks"].values())
    if checks_ok and not remote_errors:
        result["status"] = "synced"
    elif checks_ok and remote_errors:
        result["status"] = "remote_unverified"
    else:
        result["status"] = "out_of_sync"
    return result


def emit_text(result: dict) -> None:
    print(f"academy mirror: {result['mirror_path']} ({result.get('mode', 'unknown')})")
    print(f"status: {result['status']}")
    if result.get("receipt_sha"):
        print(f"receipt_sha: {result['receipt_sha']}")
    if result.get("remote_head"):
        print(f"remote_head: {result['remote_head']}")
    for name, passed in result.get("checks", {}).items():
        print(f"{name}: {'ok' if passed else 'fail'}")
    for error in result.get("errors", []):
        print(f"error: {error}")


def resolve_mirror(mirror: str, remote_url: str | None) -> tuple[str, str]:
    if mirror in PUBLIC_MIRRORS:
        spec = PUBLIC_MIRRORS[mirror]
        return spec["path"], remote_url or spec["remote"]
    return mirror, remote_url or PUBLIC_MIRRORS["predictive-history"]["remote"]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mirror",
        default="predictive-history",
        help="Mirror slug (predictive-history, ph-civ alias, civ-state) or mirror path",
    )
    parser.add_argument("--remote-url", default=None)
    parser.add_argument("--branch", default="main")
    parser.add_argument("--no-fetch", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    mirror_rel, remote_url = resolve_mirror(args.mirror, args.remote_url)

    result = check_sync(
        mirror_rel=mirror_rel,
        remote_url=remote_url,
        branch=args.branch,
        fetch=not args.no_fetch,
    )
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        emit_text(result)
    return 0 if result["status"] in {"synced", "remote_unverified"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
