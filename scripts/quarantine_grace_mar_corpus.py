#!/usr/bin/env python3
"""One-shot helper: git mv docs → archive/grace-mar-corpus + stub at old path."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BOUNDARY = "../../docs/grace-mar-instance-boundary.md"

BANNER = (
    "> **ARCHIVED (Grace-Mar corpus).** Fork growth is **not** default strategy-codex routing. "
    "**`fork revive` only** — see [grace-mar-instance-boundary.md]({boundary}).\n\n"
)

CORPUS: dict[str, list[str]] = {
    "doctrine": [
        "grace-mar-core.md",
        "white-paper.md",
        "admissions-link-use-case.md",
        "concept.md",
        "identity-fork-protocol.md",
        "fork-lifecycle.md",
        "fork-isolation-and-multi-tenant.md",
        "governance-unbundling.md",
        "anti-cheating.md",
        "harness-replay-spec.md",
        "grace-mar-vs-companion-self.md",
    ],
    "operator-habits": [
        "pipeline-map.md",
        "we-did-x-habit.md",
        "wisdom-questions.md",
        "operator-weekly-review.md",
    ],
    "template": [
        "seed-phase.md",
        "seed-phase-doctrine.md",
        "seed-registry.md",
        "seed-phase-readiness.md",
        "companion-self-developer-plan.md",
        "companion-self-seed-phase-v2-mapping.md",
    ],
    "competitive": [
        "aws-agentcore-alignment.md",
        "google-gemini-alignment.md",
        "apple-intelligence-alignment.md",
        "agent-365-alignment.md",
        "atlassian-rovo-alignment.md",
        "design-notes.md",
        "differentiation.md",
        "business-plan.md",
        "business-prospectus.md",
        "parent-brief.md",
        "openclaw-integration.md",
        "feedback-autogen-exploration-2026-03.md",
        "feedback-autogen-exploration-2026-03-assessment.md",
    ],
}

def stub_body(title: str, moved_rel: str) -> str:
    lines = [
        "---",
        "archived: true",
        f"moved_to: {moved_rel}",
        "---",
        "",
        f"# {title} (archived)",
        "",
        f"Moved to [`{moved_rel}`]({moved_rel}). Record frozen — see [grace-mar-instance-boundary.md](grace-mar-instance-boundary.md).",
        "",
    ]
    return "\n".join(lines)

def title_from_name(name: str) -> str:
    return name.replace(".md", "").replace("-", " ").title()

def quarantine_folder(folder: str, *, dry_run: bool) -> int:
    moved = 0
    for name in CORPUS[folder]:
        src = REPO / "docs" / name
        if not src.is_file():
            print(f"skip missing: {src}", file=sys.stderr)
            continue
        dest_dir = REPO / "archive" / "grace-mar-corpus" / folder
        dest = dest_dir / name
        moved_rel = f"archive/grace-mar-corpus/{folder}/{name}"
        if dry_run:
            print(f"would mv {src} -> {dest}")
            continue
        dest_dir.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "mv", str(src), str(dest)], cwd=REPO, check=True)
        text = dest.read_text(encoding="utf-8")
        rel_boundary = "../" * (3 + folder.count("/")) + "docs/grace-mar-instance-boundary.md"
        if folder == "doctrine":
            rel_boundary = "../../docs/grace-mar-instance-boundary.md"
        elif folder == "operator-habits":
            rel_boundary = "../../docs/grace-mar-instance-boundary.md"
        elif folder == "template":
            rel_boundary = "../../docs/grace-mar-instance-boundary.md"
        else:
            rel_boundary = "../../docs/grace-mar-instance-boundary.md"
        if not text.startswith("> **ARCHIVED"):
            dest.write_text(BANNER.format(boundary=rel_boundary) + text, encoding="utf-8")
        stub = stub_body(title_from_name(name), moved_rel)
        src.write_text(stub, encoding="utf-8")
        moved += 1
        print(f"quarantined {name} -> {moved_rel}")
    return moved

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("folder", choices=list(CORPUS.keys()))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    n = quarantine_folder(args.folder, dry_run=args.dry_run)
    print(f"done: {n} files in {args.folder}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
