#!/usr/bin/env python3
"""Migrate singularity/research/ into research/narrative-systems/ numbered taxonomy."""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_BASE = REPO_ROOT / "singularity" / "research"
DST_BASE = REPO_ROOT / "research" / "narrative-systems"

NUMBERED_DIRS: tuple[str, ...] = (
    "00_system",
    "01_ontology",
    "02_narrative_systems",
    "02_narrative_systems/formal_variants",
    "03_core_models",
    "04_mappings",
    "05_geometric_lenses",
    "06_dynamics",
    "07_applications",
    "08_comparisons",
    "09_open_problems",
)

DIR_MOVES: list[tuple[str, str]] = [
    ("narrative-systems/model-relations", "04_mappings/model_relations"),
    ("predictive-history", "03_core_models/predictive_history"),
    ("civilization-state", "03_core_models/civilization_state"),
    ("epistemic-geometry", "05_geometric_lenses/epistemic_geometry"),
]

GLOB_MOVES: list[tuple[str, str]] = [
    ("system", "00_system"),
    ("ontology", "01_ontology"),
    ("comparisons", "08_comparisons"),
    ("applications", "07_applications"),
    ("dynamics", "06_dynamics"),
    ("misc", "09_open_problems"),
    ("scratch", "09_open_problems"),
    ("notes", "09_open_problems"),
]

NST_ROOT_FILES: tuple[str, ...] = (
    "formal_model.md",
    "monoidal_extension.md",
    "phase_transition_model.md",
    "mapping_functions.md",
    "dual_structure.md",
    "invariants.md",
    "assumptions.md",
    "open_questions.md",
)

def is_tracked(rel_posix: str) -> bool:
    result = subprocess.run(
        ["git", "ls-files", "--error-unmatch", rel_posix],
        cwd=REPO_ROOT,
        capture_output=True,
    )
    return result.returncode == 0

def is_dir_tracked(src: Path) -> bool:
    rel = src.relative_to(REPO_ROOT).as_posix()
    if src.is_file():
        return is_tracked(rel)
    if not src.is_dir():
        return False
    tracked = subprocess.run(
        ["git", "ls-files", rel],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    return bool(tracked.stdout.strip())

def move_path(src: Path, dst: Path, *, dry_run: bool) -> None:
    if not src.exists():
        print(f"skip missing: {src.relative_to(REPO_ROOT)}")
        return
    if dst.exists():
        raise RuntimeError(f"destination already exists: {dst.relative_to(REPO_ROOT)}")
    rel_src = src.relative_to(REPO_ROOT)
    rel_dst = dst.relative_to(REPO_ROOT)
    tracked = is_dir_tracked(src)
    if dry_run:
        verb = "git mv" if tracked else "mv + git add"
        print(f"would {verb} {rel_src} -> {rel_dst}")
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    if tracked:
        subprocess.run(["git", "mv", str(rel_src), str(rel_dst)], cwd=REPO_ROOT, check=True)
    else:
        shutil.move(str(src), str(dst))
        subprocess.run(["git", "add", str(rel_dst)], cwd=REPO_ROOT, check=True)
    print(f"moved {rel_src} -> {rel_dst}")

def ensure_scaffold(*, dry_run: bool) -> None:
    for rel in NUMBERED_DIRS:
        path = DST_BASE / rel
        if dry_run:
            print(f"would mkdir {path.relative_to(REPO_ROOT)}")
            continue
        path.mkdir(parents=True, exist_ok=True)

def move_glob_contents(src_name: str, dst_rel: str, *, dry_run: bool) -> None:
    src_dir = SRC_BASE / src_name
    if not src_dir.is_dir():
        print(f"skip missing dir: {src_dir.relative_to(REPO_ROOT)}")
        return
    dst_dir = DST_BASE / dst_rel
    for item in sorted(src_dir.iterdir()):
        move_path(item, dst_dir / item.name, dry_run=dry_run)
    if not dry_run and src_dir.exists() and not any(src_dir.iterdir()):
        src_dir.rmdir()
        print(f"removed empty {src_dir.relative_to(REPO_ROOT)}")

def move_nst_root_files(*, dry_run: bool) -> None:
    nst = SRC_BASE / "narrative-systems"
    if not nst.is_dir():
        print(f"skip missing: {nst.relative_to(REPO_ROOT)}")
        return

    umbrella_readme = nst / "README.md"
    if umbrella_readme.is_file():
        move_path(umbrella_readme, DST_BASE / "README.md", dry_run=dry_run)

    for name in NST_ROOT_FILES:
        src = nst / name
        if src.is_file():
            move_path(src, DST_BASE / "02_narrative_systems" / name, dry_run=dry_run)

    if not dry_run and nst.exists():
        remaining = list(nst.iterdir())
        if remaining:
            print(f"warning: narrative-systems not empty after moves: {remaining}")
        else:
            nst.rmdir()
            print(f"removed empty {nst.relative_to(REPO_ROOT)}")

def write_category_definition_pointer(*, dry_run: bool) -> None:
    path = DST_BASE / "02_narrative_systems" / "category_definition.md"
    body = (
        "# Narrative Systems (NS) — Category Definition\n\n"
        "See [formal_model.md](formal_model.md) for the category-theoretic specification "
        "(objects, morphisms, functor F, transformation space Δ).\n"
    )
    if dry_run:
        print(f"would write {path.relative_to(REPO_ROOT)}")
        return
    if not path.exists():
        path.write_text(body, encoding="utf-8")
        subprocess.run(["git", "add", str(path.relative_to(REPO_ROOT))], cwd=REPO_ROOT, check=True)
        print(f"wrote {path.relative_to(REPO_ROOT)}")

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Migrate singularity/research into research/narrative-systems/"
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    if not args.dry_run and not args.apply:
        parser.error("Specify --dry-run or --apply")

    dry_run = args.dry_run
    if not SRC_BASE.is_dir():
        raise SystemExit(f"source missing: {SRC_BASE.relative_to(REPO_ROOT)}")

    ensure_scaffold(dry_run=dry_run)

    for src_rel, dst_rel in DIR_MOVES:
        move_path(SRC_BASE / src_rel, DST_BASE / dst_rel, dry_run=dry_run)

    move_nst_root_files(dry_run=dry_run)

    for src_name, dst_rel in GLOB_MOVES:
        move_glob_contents(src_name, dst_rel, dry_run=dry_run)

    write_category_definition_pointer(dry_run=dry_run)

    if not dry_run:
        for legacy in ("epistemic-geometry", "predictive-history", "civilization-state"):
            leftover = SRC_BASE / legacy
            if leftover.is_dir() and not any(leftover.iterdir()):
                leftover.rmdir()

    print("migration pass complete")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
