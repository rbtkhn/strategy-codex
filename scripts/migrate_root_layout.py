#!/usr/bin/env python3
"""Sequential git mv for root folder consolidation (Windows-safe)."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

DIR_MOVES: list[tuple[str, str]] = [
    ("evidence", "archive/placeholders/evidence"),
    ("reflection-proposals", "archive/queues/reflection-proposals"),
    ("review-queue", "archive/queues/review-queue"),
    ("prepared-context", "runtime/prepared-context"),
    ("artifacts", "runtime/artifacts"),
    ("daily-handoff", "runtime/daily-handoff"),
    ("runtime-bundle", "runtime/bundle"),
    ("apps", "platform/apps"),
    ("app", "platform/app"),
    ("src", "platform/src"),
    ("bin", "platform/bin"),
    ("deployment", "platform/deployment"),
    ("config", "platform/config"),
    ("extension", "platform/extension"),
    ("integrations", "platform/integrations"),
    ("miniapp", "platform/miniapp"),
    ("users", "platform/users"),
    ("_template", "platform/template"),
    ("profile", "platform/profile"),
    ("auto-research", "research/auto-research"),
    ("bridges", "research/bridges"),
    ("schema-registry", "schemas/registry"),
    ("styles", "templates/styles"),
    ("skills-portable", "skills"),
    ("bot", "archive/grace-mar-instance/bot"),
    ("recursion-gate-staging", "archive/grace-mar-instance/recursion-gate-staging"),
    ("bootstrap", "archive/grace-mar-instance/bootstrap"),
]

RECORD_FILES: tuple[str, ...] = (
    "self.md",
    "self-archive.md",
    "self-knowledge.md",
    "recursion-gate.md",
    "self-skills.md",
    "self-library.md",
    "self-evidence.md",
    "self-history.md",
    "self-memory.md",
    "self-moonshots.md",
    "session-log.md",
    "intent.md",
    "self-llm.txt",
    "openclaw-user.md",
)


def run_git_mv(src: Path, dst: Path, *, dry_run: bool) -> None:
    if not src.exists():
        print(f"skip missing: {src.relative_to(REPO_ROOT)}")
        return
    if dst.exists():
        raise RuntimeError(f"destination already exists: {dst.relative_to(REPO_ROOT)}")
    rel_src = src.relative_to(REPO_ROOT)
    rel_dst = dst.relative_to(REPO_ROOT)
    if dry_run:
        print(f"would git mv {rel_src} -> {rel_dst}")
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "mv", str(rel_src), str(rel_dst)], cwd=REPO_ROOT, check=True)
    print(f"moved {rel_src} -> {rel_dst}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Migrate root directories")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--skip-record", action="store_true")
    args = parser.parse_args()
    if not args.dry_run and not args.apply:
        parser.error("Specify --dry-run or --apply")

    for src_rel, dst_rel in DIR_MOVES:
        run_git_mv(REPO_ROOT / src_rel, REPO_ROOT / dst_rel, dry_run=args.dry_run)

    instance = REPO_ROOT / "archive" / "grace-mar-instance"
    if not args.skip_record:
        for name in RECORD_FILES:
            src = REPO_ROOT / name
            dst = instance / name
            if src.is_file():
                run_git_mv(src, dst, dry_run=args.dry_run)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
