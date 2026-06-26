#!/usr/bin/env python3
"""Migrate statecraft/daily/ to synthesis-pure layout + notes subfolders.

Usage:
    python scripts/migrate_statecraft_synthesis_layout.py --dry-run
    python scripts/migrate_statecraft_synthesis_layout.py --apply
    python scripts/migrate_statecraft_synthesis_layout.py --rewrite-links
    python scripts/migrate_statecraft_synthesis_layout.py --write-stub
"""

from __future__ import annotations

import argparse
import csv
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DAILY_DIR = REPO_ROOT / "statecraft" / "daily"
SYNTHESIS_DIR = REPO_ROOT / "statecraft" / "synthesis"
NOTES_DIR = REPO_ROOT / "statecraft" / "notes"
MANIFEST_PATH = REPO_ROOT / "runtime" / "artifacts" / "statecraft-synthesis-migrate-manifest.csv"
LINK_REWRITE_PATH = REPO_ROOT / "runtime" / "artifacts" / "statecraft-synthesis-link-rewrite.tsv"

DAY_SYNTH_RE = re.compile(r"^\d{4}-\d{2}-\d{2}\.md$")
MONTH_SYNTH_RE = re.compile(r"^\d{4}-\d{2}\.md$")
WIRE_RE = re.compile(r"-news-verify-matrix\.md$")
WATCH_RE = re.compile(r"-72h-watch-run\.md$")
WEEK_HINGE_RE = re.compile(r"-week\d+-start-here\.md$")
INTAKE_READY_RE = re.compile(r"-intake-readiness\.md$")
DAY_SLUG_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-.+\.md$")
INTELLIGENCE_ESSAY_RE = re.compile(r"-strategic-memory\.md$")

SYNTHESIS_ROOT_META = frozenset(
    {
        "METHOD.md",
        "MONTHLY-METHOD-COMPANION.md",
        "audit-rubric.md",
        "benchmark-manifest.md",
    }
)
CLOSE_RECEIPT_RE = re.compile(r"^(karajan-close|method-hardening-close)-.*\.md$")

SKIP_NAMES = frozenset({"README.md"})

NOTE_TYPE_MAP = {
    "verification receipt": "wire_matrix",
    "operational watch window": "watch_run",
    "navigation hinge": "reentry",
    "pre-synthesis queue": "intake",
    "statecraft note (compare/mechanism)": "compare",
}

REWRITE_SCAN_DIRS = (
    "statecraft",
    "docs",
    ".cursor",
    "skills",
    "tests",
    "LLM-ROUTING.md",
    "README.md",
)
REWRITE_EXCLUDE_PARTS = (
    "runtime/artifacts",
    "source-archive/statecraft",
    "statecraft/daily/README.md",
    ".cursor/plans",
)


@dataclass
class MoveRow:
    src: Path
    dest: Path
    dest_shelf: str
    epistemic_class: str
    collision_flag: str
    manual_triage: str

    @property
    def basename(self) -> str:
        return self.src.name

    @property
    def old_daily_ref(self) -> str:
        return f"statecraft/daily/{self.basename}"

    @property
    def new_ref(self) -> str:
        return str(self.dest.relative_to(REPO_ROOT)).replace("\\", "/")


def classify(path: Path) -> MoveRow | None:
    name = path.name
    if name in SKIP_NAMES:
        return None
    rel = path.relative_to(DAILY_DIR)
    if rel.parts[0] == "_templates":
        dest = NOTES_DIR / "reentry" / rel
        return MoveRow(path, dest, "notes/reentry", "reentry template", "", "")

    if name == "intake-digest-TEMPLATE.md":
        dest = NOTES_DIR / "intake" / name
        return MoveRow(path, dest, "notes/intake", "intake doctrine", "", "")

    if WIRE_RE.search(name):
        dest = NOTES_DIR / "wire" / name
        return MoveRow(path, dest, "notes/wire", "verification receipt", "", "")

    if WATCH_RE.search(name):
        dest = NOTES_DIR / "watch" / name
        return MoveRow(path, dest, "notes/watch", "operational watch window", "", "")

    if WEEK_HINGE_RE.search(name):
        dest = NOTES_DIR / "reentry" / name
        return MoveRow(path, dest, "notes/reentry", "navigation hinge", "", "")

    if INTAKE_READY_RE.search(name):
        dest = NOTES_DIR / "intake" / name
        return MoveRow(path, dest, "notes/intake", "pre-synthesis queue", "", "")

    if DAY_SYNTH_RE.match(name):
        dest = SYNTHESIS_DIR / "day" / name
        return MoveRow(path, dest, "synthesis/day", "day synthesis", "", "")

    if MONTH_SYNTH_RE.match(name):
        dest = SYNTHESIS_DIR / "month" / name
        return MoveRow(path, dest, "synthesis/month", "month synthesis", "", "")

    if CLOSE_RECEIPT_RE.match(name) or name in SYNTHESIS_ROOT_META:
        dest = SYNTHESIS_DIR / name
        return MoveRow(path, dest, "synthesis/root", "synthesis doctrine", "", "")

    if DAY_SLUG_RE.match(name):
        manual = ""
        if INTELLIGENCE_ESSAY_RE.search(name):
            manual = "intelligence-essay-class"
        dest = NOTES_DIR / name
        return MoveRow(path, dest, "notes/root", "statecraft note (compare/mechanism)", "", manual)

    if path.suffix == ".md":
        dest = SYNTHESIS_DIR / name
        return MoveRow(path, dest, "synthesis/root", "synthesis doctrine", "", "")

    return None


def collect_moves() -> list[MoveRow]:
    if not DAILY_DIR.is_dir():
        print(f"migrate: missing {DAILY_DIR}", file=sys.stderr)
        sys.exit(1)
    rows: list[MoveRow] = []
    for path in sorted(DAILY_DIR.rglob("*")):
        if not path.is_file():
            continue
        row = classify(path)
        if row is None:
            continue
        if row.dest.exists() and row.dest.resolve() != path.resolve():
            row.collision_flag = "merge-review"
        rows.append(row)
    return rows


def write_manifest(rows: list[MoveRow]) -> None:
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    with MANIFEST_PATH.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "src",
                "dest_path",
                "dest_shelf",
                "epistemic_class",
                "collision_flag",
                "manual_triage",
            ]
        )
        for r in rows:
            w.writerow(
                [
                    str(r.src.relative_to(REPO_ROOT)).replace("\\", "/"),
                    r.new_ref,
                    r.dest_shelf,
                    r.epistemic_class,
                    r.collision_flag,
                    r.manual_triage,
                ]
            )


def write_link_rewrite(rows: list[MoveRow]) -> None:
    LINK_REWRITE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LINK_REWRITE_PATH.open("w", newline="", encoding="utf-8") as f:
        f.write("old_ref\tnew_ref\tscope\n")
        for r in rows:
            f.write(f"{r.old_daily_ref}\t{r.new_ref}\tabsolute\n")
            f.write(f"./{r.basename}\t{r.new_ref}\trelative\n")
            f.write(f"../daily/{r.basename}\t../{r.new_ref.split('/', 1)[1]}\tcross-shelf\n")
        f.write("statecraft/daily/\tstatecraft/synthesis/day/\tabsolute-prefix\n")
        f.write("../daily/\t../synthesis/day/\tcross-shelf-prefix\n")


def ensure_scaffold() -> None:
    for d in (
        SYNTHESIS_DIR / "day",
        SYNTHESIS_DIR / "month",
        SYNTHESIS_DIR / "week",
        NOTES_DIR / "wire",
        NOTES_DIR / "watch",
        NOTES_DIR / "reentry" / "_templates",
        NOTES_DIR / "intake",
    ):
        d.mkdir(parents=True, exist_ok=True)
    week_readme = SYNTHESIS_DIR / "week" / "README.md"
    if not week_readme.exists():
        week_readme.write_text(
            "# Week synthesis (reserved)\n\n"
            "WORK only; not Record.\n\n"
            "Placeholder for a future **week-synthesis** contract. "
            "Week hinges live under [`notes/reentry/`](../../notes/reentry/); "
            "they are navigation surfaces, not synthesis.\n",
            encoding="utf-8",
        )


def apply_moves(rows: list[MoveRow]) -> None:
    collisions = [r for r in rows if r.collision_flag]
    if collisions:
        print("Collisions (aborting apply):", file=sys.stderr)
        for r in collisions:
            print(f"  {r.basename} -> {r.new_ref}", file=sys.stderr)
        sys.exit(1)
    ensure_scaffold()
    for r in rows:
        r.dest.parent.mkdir(parents=True, exist_ok=True)
        if r.src.resolve() == r.dest.resolve():
            continue
        print(f"mv {r.src.relative_to(REPO_ROOT)} -> {r.new_ref}")
        r.dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(r.src), str(r.dest))


def write_synthesis_readme(old_readme: Path) -> None:
    dest = SYNTHESIS_DIR / "README.md"
    body = (
        "WORK only; not Record.\n\n"
        "# State Synthesis Shelf\n\n"
        "Canonical path for **archive-grounded synthesis** (day / month cadence). "
        "Adjacent operational artifacts live under [`notes/`](../notes/README.md) subfolders.\n\n"
        "## Promotion ladder\n\n"
        "`source-archive/statecraft/` → `statecraft/synthesis/day/` → "
        "`statecraft/notes/` → `statecraft/*/transactions/`\n\n"
        "## Cadence layout\n\n"
        "| Path | Contents |\n"
        "| --- | --- |\n"
        "| [`day/`](day/) | Daily synthesis / register (`YYYY-MM-DD.md`) |\n"
        "| [`month/`](month/) | Monthly synthesis (`YYYY-MM.md`) |\n"
        "| [`week/`](week/) | Reserved — week synthesis TBD |\n\n"
        "## Method\n\n"
        "- [METHOD.md](METHOD.md)\n"
        "- [audit-rubric.md](audit-rubric.md)\n"
        "- [benchmark-manifest.md](benchmark-manifest.md)\n\n"
        "## Adjacent notes (not synthesis)\n\n"
        "| Subfolder | Class |\n"
        "| --- | --- |\n"
        "| [`notes/wire/`](../notes/wire/) | News-verify matrices |\n"
        "| [`notes/watch/`](../notes/watch/) | 72h watch runs |\n"
        "| [`notes/reentry/`](../notes/reentry/) | Week hinges |\n"
        "| [`notes/intake/`](../notes/intake/) | Intake readiness / digest |\n\n"
        "Legacy path: [`statecraft/daily/`](../daily/README.md) (redirect stub).\n"
    )
    dest.write_text(body, encoding="utf-8")


def write_stub(rows: list[MoveRow]) -> None:
    stub_dir = REPO_ROOT / "statecraft" / "daily"
    stub_dir.mkdir(parents=True, exist_ok=True)
    lines = [
        "WORK only; not Record.",
        "",
        "# Moved — State Synthesis Shelf",
        "",
        "Canonical path: [statecraft/synthesis/README.md](../synthesis/README.md).",
        "",
        "Promotion ladder: source-archive → statecraft/synthesis/day/ → transactions.",
        "",
        "## Redirect manifest",
        "",
        "| Old path (under daily/) | New path |",
        "| --- | --- |",
    ]
    for r in sorted(rows, key=lambda x: x.basename):
        lines.append(f"| `{r.basename}` | `{r.new_ref}` |")
    (stub_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def load_manifest() -> list[tuple[str, str]]:
    if not MANIFEST_PATH.is_file():
        print(f"missing manifest: {MANIFEST_PATH}", file=sys.stderr)
        sys.exit(1)
    pairs: list[tuple[str, str]] = []
    with MANIFEST_PATH.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            old = f"statecraft/daily/{Path(row['src']).name}"
            pairs.append((old, row["dest_path"]))
            pairs.append((f"./{Path(row['src']).name}", row["dest_path"]))
            name = Path(row["src"]).name
            new = row["dest_path"]
            if new.startswith("statecraft/notes/"):
                pairs.append((f"../daily/{name}", f"../{new[len('statecraft/'):]}"))
            elif new.startswith("statecraft/synthesis/"):
                pairs.append((f"../daily/{name}", f"../{new[len('statecraft/'):]}"))
    pairs.append(("statecraft/daily/", "statecraft/synthesis/day/"))
    pairs.append(("../daily/", "../synthesis/day/"))
    # longest first to avoid partial replacements
    pairs.sort(key=lambda p: len(p[0]), reverse=True)
    return pairs


def should_rewrite(path: Path) -> bool:
    rel = str(path.relative_to(REPO_ROOT)).replace("\\", "/")
    for ex in REWRITE_EXCLUDE_PARTS:
        if ex in rel:
            return False
    if path.suffix not in {".md", ".mdc", ".py", ".yaml", ".yml", ".json"}:
        return False
    return True


def rewrite_links() -> int:
    pairs = load_manifest()
    changed = 0
    targets: list[Path] = []
    for item in REWRITE_SCAN_DIRS:
        p = REPO_ROOT / item
        if p.is_file():
            targets.append(p)
        elif p.is_dir():
            targets.extend(p.rglob("*"))
    seen: set[Path] = set()
    for path in targets:
        if not path.is_file() or path in seen or not should_rewrite(path):
            continue
        seen.add(path)
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        new_text = text
        for old, new in pairs:
            new_text = new_text.replace(old, new)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            changed += 1
            print(f"rewrote {path.relative_to(REPO_ROOT)}")
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description="Migrate statecraft/daily layout")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--rewrite-links", action="store_true")
    parser.add_argument("--write-stub", action="store_true")
    args = parser.parse_args()

    if args.rewrite_links:
        n = rewrite_links()
        print(f"rewrite-links: {n} file(s) updated")
        return 0

    rows = collect_moves()
    write_manifest(rows)
    write_link_rewrite(rows)
    print(f"manifest: {MANIFEST_PATH} ({len(rows)} moves)")
    print(f"link_rewrite: {LINK_REWRITE_PATH}")

    collisions = [r for r in rows if r.collision_flag]
    if collisions:
        print(f"WARNING: {len(collisions)} collision(s)")
        for r in collisions:
            print(f"  {r.basename}")

    if args.dry_run:
        for r in rows:
            print(f"  {r.old_daily_ref} -> {r.new_ref} [{r.epistemic_class}]")
        return 0

    if args.apply:
        old_readme = DAILY_DIR / "README.md"
        apply_moves(rows)
        write_synthesis_readme(old_readme)
        # Remove empty _templates and daily dir except stub will be rewritten
        write_stub(rows)
        # Clean leftover empty dirs under old daily
        if DAILY_DIR.is_dir():
            for sub in sorted(DAILY_DIR.rglob("*"), reverse=True):
                if sub.is_dir() and not any(sub.iterdir()):
                    sub.rmdir()
        print(f"apply: {len(rows)} file(s) moved")
        return 0

    if args.write_stub:
        write_stub(rows)
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
