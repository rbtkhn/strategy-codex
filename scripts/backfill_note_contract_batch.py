#!/usr/bin/env python3
"""Backfill note contract frontmatter on a bounded shelf-native batch."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
NOTES_ROOT = REPO_ROOT / "statecraft" / "notes"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from check_statecraft_notes import (  # noqa: E402
    FRONTMATTER_RE,
    ARCHIVE_PATH_RE,
    SYNTHESIS_PATH_RE,
    parse_note_metadata,
    validate_note,
    build_inbound_note_links,
)

# README MOU enforcement cluster (exemplars already contract-complete omitted)
MOU_ENFORCEMENT_BATCH: dict[str, str] = {
    "risk-mou-enforcement.md": "risk",
    "risk-hormuz-chokepoint.md": "risk",
    "june-18-2026-mou-convergence.md": "synthesis",
    "june-18-2026-mou-guest-pair-citation-split.md": "compare",
    "june-18-2026-mou-material-vs-sabotage-lens.md": "compare",
    "june-18-2026-mou-falsifier-3-standoff-watch.md": "mechanism",
    "june-18-2026-mou-hormuz-governance-armistice-note.md": "mechanism",
    "june-18-2026-mou-dahhiya-backfire-mou-terms-note.md": "mechanism",
    "june-17-2026-mou-dem-co-ownership-torpedo-note.md": "mechanism",
    "us-israel-military-integration-captured-command-risk.md": "mechanism",
}

# README Hormuz / chokepoint + May Iran compare + March benchmark (exemplars omitted)
IRAN_THEATER_BATCH: dict[str, str] = {
    "2026-02-17-iran-bench-weave-marandi-mearsheimer-helmer.md": "synthesis",
    "2026-03-24-helmer-marandi-energy-hormuz-five-terms-weave.md": "synthesis",
    "arc-helmer-iran-five-terms.md": "arc",
    "iran-war-inquiry-ladder-stress-test.md": "synthesis",
    "jiang-vs-johnson-2026-05.md": "compare",
    "jiang-vs-johnson-others-2026-05.md": "compare",
    "march-2026-benchmark-note.md": "synthesis",
}

# README Artificial intelligence cluster (exemplars + legacy redirects omitted)
AI_CLUSTER_BATCH: dict[str, str] = {
    "risk-artificial-intelligence.md": "risk",
    "pape-on-china-ai.md": "mechanism",
    "jiang-on-ai.md": "mechanism",
    "barnes-on-ai.md": "mechanism",
    "ritter-on-ai.md": "mechanism",
    "weichert-on-ai.md": "mechanism",
    "sachs-on-ai.md": "mechanism",
    "gulf-ai-architecture.md": "mechanism",
    "minab-palantir-four-voice-compare.md": "compare",
    "june-19-2026-moonshots-export-control-sovereign-ai-crossover.md": "bridge",
}

BATCHES: dict[str, dict[str, str]] = {
    "mou-enforcement": MOU_ENFORCEMENT_BATCH,
    "iran-theater": IRAN_THEATER_BATCH,
    "ai-cluster": AI_CLUSTER_BATCH,
}

DATE_IN_NAME = re.compile(r"(\d{4}-\d{2}-\d{2})")


def _infer_created_at(stem: str) -> str:
    match = DATE_IN_NAME.search(stem)
    return match.group(1) if match else "2026-06-18"


def _extract_archive_links(text: str, *, limit: int = 8) -> list[str]:
    links: list[str] = []
    for match in ARCHIVE_PATH_RE.findall(text.replace("\\", "/")):
        path = match.rstrip(").,")
        if path not in links:
            links.append(path)
        if len(links) >= limit:
            break
    return links


def _source_basis(text: str, archives: list[str]) -> str:
    if SYNTHESIS_PATH_RE.search(text.replace("\\", "/")) and archives:
        return "mixed"
    if archives:
        return "source-archive"
    if SYNTHESIS_PATH_RE.search(text.replace("\\", "/")):
        return "synthesis"
    return "mixed"


def _render_frontmatter(
    *,
    note_id: str,
    note_type: str,
    source_basis: str,
    created_at: str,
    updated_at: str,
    archive_links: list[str],
) -> str:
    lines = [
        "---",
        f"note_id: {note_id}",
        f"note_type: {note_type}",
        "authority_level: shelf-native",
        f"source_basis: {source_basis}",
        "essay_candidate: false",
        f"created_at: {created_at}",
        f"updated_at: {updated_at}",
    ]
    if archive_links:
        lines.append("archive_links:")
        for link in archive_links[:8]:
            lines.append(f"  - {link}")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def backfill_file(path: Path, note_type: str, *, updated_at: str, dry_run: bool) -> bool:
    text = path.read_text(encoding="utf-8", errors="replace")
    meta = parse_note_metadata(path, text)
    if meta.authority_level and meta.source_basis and meta.note_type:
        return False

    archives = _extract_archive_links(text)
    basis = _source_basis(text, archives)
    created = _infer_created_at(path.stem)
    block = _render_frontmatter(
        note_id=path.stem,
        note_type=note_type,
        source_basis=basis,
        created_at=created,
        updated_at=updated_at,
        archive_links=archives,
    )

    if FRONTMATTER_RE.match(text.lstrip("\ufeff")):
        return False

    if text.startswith("WORK only; not Record."):
        new_text = block + text
    elif text.lstrip("\ufeff").startswith("---"):
        return False
    else:
        new_text = block + text

    if dry_run:
        print(f"would backfill: {path.relative_to(REPO_ROOT)}")
        return True

    path.write_text(new_text, encoding="utf-8", newline="\n")
    print(f"backfilled: {path.relative_to(REPO_ROOT)}")
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--batch",
        choices=tuple(BATCHES),
        default="mou-enforcement",
        help="Named shelf-native batch from notes/README clusters",
    )
    ap.add_argument("--updated-at", default="2026-06-28")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--verify", action="store_true", help="Validate batch after backfill")
    args = ap.parse_args()

    batch = BATCHES[args.batch]
    changed = 0
    for name, note_type in batch.items():
        path = NOTES_ROOT / name
        if not path.is_file():
            print(f"missing: {name}", file=sys.stderr)
            continue
        if backfill_file(path, note_type, updated_at=args.updated_at, dry_run=args.dry_run):
            changed += 1

    print(f"batch {args.batch}: {changed} file(s) {'would change' if args.dry_run else 'updated'}")
    if args.verify and not args.dry_run:
        inbound = build_inbound_note_links(list(NOTES_ROOT.rglob("*.md")))
        failures = 0
        for name in batch:
            path = NOTES_ROOT / name
            text = path.read_text(encoding="utf-8")
            meta = parse_note_metadata(path, text)
            issues = validate_note(meta, text=text, inbound_count=inbound.get(meta.rel, 0))
            if issues:
                failures += 1
                print(f"FAIL {name}:", file=sys.stderr)
                for issue in issues:
                    print(f"  {issue}", file=sys.stderr)
        return 1 if failures else 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
