#!/usr/bin/env python3
"""Move legacy statecraft/transactions frameworks to statecraft/notes/compacts with stubs."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

STUB_HEADER = """# Deprecated compatibility stub

WORK only; not Record.

Deprecated compatibility stub.
Canonical: {canonical}
"""

LANE_SINGLES = (
    (
        "statecraft/persia/transactions/hormuz-recognition-transit-transaction.md",
        "statecraft/notes/hormuz-recognition-transit-transaction.md",
    ),
    (
        "statecraft/persia/transactions/lebanon-third-party-recognition-gate-transaction.md",
        "statecraft/notes/lebanon-third-party-recognition-gate-transaction.md",
    ),
    (
        "statecraft/america/transactions/foreign-client-mesh-separation-and-command-review.md",
        "statecraft/notes/foreign-client-mesh-separation-and-command-review.md",
    ),
    (
        "statecraft/america/transactions/digital-identity-continuity-before-platform-control.md",
        "statecraft/notes/digital-identity-continuity-before-platform-control.md",
    ),
    (
        "statecraft/russia/transactions/zangezur-mediation-without-overbinding.md",
        "statecraft/notes/zangezur-mediation-without-overbinding.md",
    ),
    (
        "statecraft/china/transactions/taiwan-inspection-pressure-without-blockade-ownership.md",
        "statecraft/notes/taiwan-inspection-pressure-without-blockade-ownership.md",
    ),
)

TOMBSTONE = """# Deprecated — lane transactions bench

WORK only; not Record.

This surface is deprecated. Durable analytical work now lives in [statecraft/notes/](../notes/README.md).
Multi-lane instrument compacts live in [statecraft/notes/compacts/](../notes/compacts/).

Legacy compatibility stubs may remain under `*/transactions/` until links are recanonicalized.
"""


def _rel(from_path: Path, to_path: Path) -> str:
    return Path(
        Path("../" * len(from_path.parent.relative_to(REPO_ROOT).parts))
        / to_path.relative_to(REPO_ROOT)
    ).as_posix().lstrip("./")


def move_framework(src_dir: Path, dry_run: bool) -> None:
    slug = src_dir.name
    dest = REPO_ROOT / "statecraft" / "notes" / "compacts" / slug
    if dest.exists():
        print(f"skip (exists): {dest.relative_to(REPO_ROOT)}")
        return
    print(f"move: {src_dir.relative_to(REPO_ROOT)} -> {dest.relative_to(REPO_ROOT)}")
    if dry_run:
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src_dir), str(dest))
    canonical = Path("../../notes/compacts") / slug / "README.md"
    stub_readme = src_dir.parent / slug / "README.md"
    src_dir.mkdir(parents=True, exist_ok=True)
    stub_readme.write_text(
        STUB_HEADER.format(canonical=canonical.as_posix()),
        encoding="utf-8",
    )


def move_single(src_rel: str, dest_rel: str, dry_run: bool) -> None:
    src = REPO_ROOT / src_rel
    dest = REPO_ROOT / dest_rel
    if not src.is_file():
        print(f"skip missing: {src_rel}")
        return
    if dest.exists():
        print(f"skip (exists): {dest_rel}")
        return
    print(f"move: {src_rel} -> {dest_rel}")
    if dry_run:
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), str(dest))
    canonical = Path("../" * (len(Path(src_rel).parent.parts) - 1)) / Path(dest_rel).name
    src.write_text(
        STUB_HEADER.format(canonical=canonical.as_posix()),
        encoding="utf-8",
    )


def tombstone_lane_readmes(dry_run: bool) -> None:
    for lane in ("america", "persia", "russia", "china"):
        path = REPO_ROOT / "statecraft" / lane / "transactions" / "README.md"
        print(f"tombstone: {path.relative_to(REPO_ROOT)}")
        if not dry_run:
            path.write_text(TOMBSTONE, encoding="utf-8")


def rename_bench_audit(dry_run: bool) -> None:
    old = REPO_ROOT / "statecraft/notes/transaction-bench-maturity-audit.md"
    new = REPO_ROOT / "statecraft/notes/instrument-bench-maturity-audit.md"
    if not old.is_file():
        return
    if new.exists():
        return
    print(f"rename: {old.name} -> {new.name}")
    if dry_run:
        return
    shutil.move(str(old), str(new))
    old.write_text(
        STUB_HEADER.format(canonical="instrument-bench-maturity-audit.md"),
        encoding="utf-8",
    )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    tx_root = REPO_ROOT / "statecraft" / "transactions"
    for child in sorted(tx_root.iterdir()) if tx_root.is_dir() else []:
        if child.is_dir():
            move_framework(child, args.dry_run)

    for src_rel, dest_rel in LANE_SINGLES:
        move_single(src_rel, dest_rel, args.dry_run)

    tombstone_lane_readmes(args.dry_run)
    rename_bench_audit(args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
