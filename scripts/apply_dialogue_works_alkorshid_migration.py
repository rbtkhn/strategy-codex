#!/usr/bin/env python3
"""Apply Dialogue Works / Alkorshid renames and YAML patches from audit CSV."""

from __future__ import annotations

import argparse
import csv
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from statecraft_day_archive import parse_frontmatter, read_text  # noqa: E402

FRONTMATTER_RE = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)


def compute_target_path(src: Path, target_prefix: str, class_: str) -> Path:
    name = src.name
    if target_prefix == "source-daniel-davis-alkorshid":
        day = src.parent.name
        stem = re.sub(r"^source-(?:dialogue-works|alkorshid|nima-alkorshid)-", "", name)
        stem = re.sub(r"-\d{4}-\d{2}-\d{2}\.md$", "", stem)
        if "alkorshid" not in stem.lower() and "nima" not in stem.lower():
            stem = f"alkorshid-{stem}"
        return src.parent / f"source-daniel-davis-alkorshid-{stem}-{day}.md"
    if name.startswith("source-dialogue-works-"):
        return src
    if name.startswith("source-nima-alkorshid-"):
        rest = name[len("source-nima-alkorshid-") :]
        return src.parent / f"source-dialogue-works-{rest}"
    if name.startswith("source-alkorshid-"):
        rest = name[len("source-alkorshid-") :]
        return src.parent / f"source-dialogue-works-{rest}"
    return src


def patch_threads_block(text: str, guest_thread: str | None, class_: str) -> str:
    fm_match = FRONTMATTER_RE.match(text)
    if not fm_match:
        return text
    fm = fm_match.group(0)
    body = text[len(fm) :]
    lines = fm.splitlines()
    out: list[str] = []
    skip_until_next_key = False
    threads_written = False
    guest_thread_val = guest_thread or ""

    for i, line in enumerate(lines):
        if skip_until_next_key:
            if re.match(r"^[A-Za-z_]", line) and not line.startswith(" "):
                skip_until_next_key = False
            else:
                continue
        if line.startswith("threads:"):
            skip_until_next_key = True
            if class_ == "davis-guest":
                out.append("threads:")
                out.append("  - davis")
                out.append("  - alkorshid")
            elif guest_thread_val:
                out.append("threads:")
                out.append("  - alkorshid")
                out.append(f"  - {guest_thread_val}")
            else:
                out.append("threads:")
                out.append("  - alkorshid")
            threads_written = True
            continue
        if line.startswith("thread:") and not threads_written:
            val = line.split(":", 1)[1].strip()
            if class_ == "davis-guest":
                out.append("thread: davis")
                out.append("threads:")
                out.append("  - davis")
                out.append("  - alkorshid")
            elif val and val != "nima":
                out.append(f"thread: {val}")
                out.append("threads:")
                out.append("  - alkorshid")
                out.append(f"  - {val}")
            else:
                out.append("thread: alkorshid")
                out.append("threads:")
                out.append("  - alkorshid")
            threads_written = True
            continue
        if line.startswith("host:") and class_ == "davis-guest":
            out.append("host: Daniel Davis")
            continue
        if line.startswith("guest:") and class_ == "davis-guest":
            out.append("guest: Nima Alkorshid")
            continue
        if line.startswith("channel_slug:") and class_ == "davis-guest":
            out.append("channel_slug: daniel-davis")
            continue
        if line.startswith("host:") and class_ in ("dw-host", "dw-solo"):
            out.append("host: Nima Alkorshid")
            continue
        out.append(line)

    new_fm = "\n".join(out)
    if not new_fm.endswith("\n---\n"):
        if new_fm.endswith("---"):
            new_fm += "\n"
    return new_fm + body


def guest_thread_from_meta(meta: dict[str, Any]) -> str | None:
    t = meta.get("thread")
    if t and str(t) != "nima":
        return str(t)
    threads = meta.get("threads")
    if isinstance(threads, list):
        for v in threads:
            if str(v) not in ("nima", "alkorshid", ""):
                return str(v)
    return None


def git_mv(src: Path, dst: Path, dry_run: bool) -> None:
    if src == dst:
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["git", "mv", str(src), str(dst)]
    if dry_run:
        print("DRY", " ".join(cmd))
        return
    subprocess.run(cmd, cwd=REPO_ROOT, check=True)


def apply_row(row: dict[str, str], dry_run: bool) -> bool:
    if row.get("needs_rename", "").lower() not in ("true", "1", "yes"):
        return False
    if row.get("dedup_action", "keep") != "keep":
        return False
    src = REPO_ROOT / row["path"]
    if not src.exists():
        print(f"skip missing {src}")
        return False
    dst = compute_target_path(src, row["target_prefix"], row["class"])
    meta = parse_frontmatter(src)
    text = read_text(src)
    guest_t = guest_thread_from_meta(meta)
    new_text = patch_threads_block(text, guest_t, row["class"])
    if dry_run:
        print(f"would mv {src.name} -> {dst.name}")
        return True
    if src != dst:
        git_mv(src, dst, dry_run=False)
        target = dst
    else:
        target = src
    target.write_text(new_text, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--csv",
        type=Path,
        default=REPO_ROOT
        / "statecraft/audits/dialogue-works-alkorshid-audit-2026-06-24.csv",
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--offset", type=int, default=0)
    args = parser.parse_args()
    rows = list(csv.DictReader(args.csv.open(encoding="utf-8")))
    candidates = [r for r in rows if r.get("needs_rename", "").lower() in ("true", "1", "yes") and r.get("dedup_action") == "keep"]
    batch = candidates[args.offset :]
    if args.limit:
        batch = batch[: args.limit]
    n = 0
    for row in batch:
        if apply_row(row, args.dry_run):
            n += 1
    print(f"Applied {n} renames/patches (batch size {len(batch)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
