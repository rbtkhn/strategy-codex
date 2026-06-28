#!/usr/bin/env python3
"""Validate statecraft/notes contract: typed, source-anchored, promotion-aware."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
NOTES_ROOT = REPO_ROOT / "statecraft" / "notes"

STUB_MARKER = "Deprecated compatibility stub"

NOTE_TYPES = frozenset(
    {
        "mechanism",
        "risk",
        "conflict",
        "trend",
        "thread",
        "arc",
        "compare",
        "synthesis",
        "bridge",
        "wire",
        "watch",
        "reentry",
        "intake",
    }
)
TIER_A_TYPES = frozenset(
    {
        "mechanism",
        "risk",
        "conflict",
        "trend",
        "thread",
        "arc",
        "compare",
        "synthesis",
        "bridge",
    }
)
AUTHORITY_LEVELS = frozenset({"draft", "review-needed", "shelf-native", "deprecated"})
SOURCE_BASIS = frozenset({"source-archive", "synthesis", "mixed"})
TIER_B_SUBFOLDERS = frozenset({"wire", "watch", "reentry", "intake"})

PREFIX_TYPE_MAP: tuple[tuple[str, str], ...] = (
    ("thread-", "thread"),
    ("arc-", "arc"),
    ("trend-", "trend"),
    ("conflict-", "conflict"),
    ("risk-", "risk"),
)

FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)
FENCED_YAML_RE = re.compile(r"```yaml\r?\n(.*?)```", re.DOTALL | re.IGNORECASE)
LINK_RE = re.compile(r"\]\(([^)]+)\)")

EXEMPT_REL = frozenset(
    {
        "statecraft/notes/README.md",
        "statecraft/notes/INDEX.md",
        "statecraft/notes/compacts/README.md",
    }
)

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from yaml_compat import safe_load_text  # noqa: E402
from notes_registry_lib import (  # noqa: E402
    archive_paths_in_text as _archive_paths_in_text,
    build_inbound_note_links as _build_inbound_note_links,
    resolve_link as _resolve_link,
    resolved_archive_anchors as _all_archive_anchors,
    synthesis_paths_in_text as _synthesis_paths_in_text,
    apply_dates,
)


@dataclass
class NoteMeta:
    rel: str
    tier: str
    path: Path
    note_id: str
    note_type: str | None = None
    authority_level: str | None = None
    source_basis: str | None = None
    essay_candidate: bool | None = None
    archive_links: list[str] = field(default_factory=list)
    nodes: list[str] = field(default_factory=list)
    is_stub: bool = False
    prefix_inferred_type: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


def _infer_type_from_filename(stem: str) -> str | None:
    for prefix, note_type in PREFIX_TYPE_MAP:
        if stem.startswith(prefix):
            return note_type
    return None


def _parse_yaml_block(text: str, *, feature: str) -> dict[str, Any]:
    data = safe_load_text(text, feature=feature)
    return data if isinstance(data, dict) else {}


def _notes_relative(path: Path) -> Path | None:
    try:
        return path.relative_to(NOTES_ROOT)
    except ValueError:
        parts = path.as_posix().replace("\\", "/").split("/")
        if "statecraft" not in parts or "notes" not in parts:
            return None
        idx = parts.index("notes")
        tail = parts[idx + 1 :]
        if not tail:
            return None
        return Path(*tail)


def _repo_relative(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        parts = path.as_posix().replace("\\", "/").split("/")
        if "statecraft" in parts and "notes" in parts:
            idx = parts.index("statecraft")
            return "/".join(parts[idx:])
        return path.as_posix().replace("\\", "/")


def parse_note_metadata(path: Path, text: str | None = None) -> NoteMeta:
    rel = _repo_relative(path)
    body = text if text is not None else path.read_text(encoding="utf-8", errors="replace")
    stem = path.stem
    meta = NoteMeta(
        rel=rel,
        tier=classify_tier(path),
        path=path,
        note_id=stem,
        is_stub=STUB_MARKER in body,
        prefix_inferred_type=_infer_type_from_filename(stem),
    )

    merged: dict[str, Any] = {}
    fm = FRONTMATTER_RE.match(body.lstrip("\ufeff"))
    if fm:
        merged.update(_parse_yaml_block(fm.group(1), feature=f"frontmatter {rel}"))
    fence = FENCED_YAML_RE.search(body)
    if fence:
        block = _parse_yaml_block(fence.group(1), feature=f"fenced yaml {rel}")
        for key, value in block.items():
            if key not in merged or merged[key] in (None, "", []):
                merged[key] = value

    if merged.get("note_type"):
        meta.note_type = str(merged["note_type"]).strip()
    elif meta.prefix_inferred_type:
        meta.note_type = meta.prefix_inferred_type

    for key in ("authority_level", "source_basis"):
        val = merged.get(key)
        if val is not None and str(val).strip():
            setattr(meta, key, str(val).strip())

    essay = merged.get("essay_candidate")
    if isinstance(essay, bool):
        meta.essay_candidate = essay
    elif essay is not None:
        meta.essay_candidate = str(essay).strip().lower() == "true"

    for list_key, target in (("archive_links", meta.archive_links), ("nodes", meta.nodes)):
        raw = merged.get(list_key)
        if isinstance(raw, list):
            target.extend(str(item).strip() for item in raw if str(item).strip())
        elif isinstance(raw, str) and raw.strip():
            target.append(raw.strip())

    apply_dates(meta, merged)
    return meta


def classify_tier(path: Path) -> str:
    rel = _repo_relative(path)
    if rel in EXEMPT_REL:
        return "index"
    parts_path = _notes_relative(path)
    if parts_path is None:
        return "skip"
    parts = parts_path.parts
    if not parts:
        return "skip"
    if len(parts) == 1 and path.name.endswith(".md"):
        return "A"
    if parts[0] == "compacts" and path.name == "README.md" and len(parts) >= 2:
        return "A"
    if parts[0] in TIER_B_SUBFOLDERS:
        return "B"
    if parts[0] == "compacts":
        return "skip"
    return "skip"


def collect_note_files(
    *,
    tier_a_only: bool = False,
    changed_only: bool = False,
) -> list[Path]:
    paths: list[Path] = []
    for path in sorted(NOTES_ROOT.rglob("*.md")):
        tier = classify_tier(path)
        if tier == "skip" or tier == "index":
            continue
        if tier_a_only and tier != "A":
            continue
        paths.append(path)

    if not changed_only:
        return paths

    changed = _git_changed_paths()
    if changed is None:
        return paths
    return [p for p in paths if p.relative_to(REPO_ROOT).as_posix() in changed]


def _git_changed_paths() -> set[str] | None:
    try:
        proc = subprocess.run(
            ["git", "diff", "--name-only", "HEAD"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        staged = subprocess.run(
            ["git", "diff", "--name-only", "--cached"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError:
        return None
    names: set[str] = set()
    for proc in (proc, staged):
        if proc.returncode != 0:
            continue
        names.update(line.strip().replace("\\", "/") for line in proc.stdout.splitlines() if line.strip())
    return names


def build_inbound_note_links(paths: list[Path]) -> dict[str, int]:
    return _build_inbound_note_links(paths, classify_tier=classify_tier)


def validate_note(meta: NoteMeta, *, text: str, inbound_count: int = 0) -> list[str]:
    if meta.is_stub or meta.tier == "index":
        return []
    issues: list[str] = []
    rel = meta.rel

    if meta.tier == "B":
        subfolder = Path(meta.rel).parts[2] if meta.rel.startswith("statecraft/notes/") else ""
        inferred = subfolder if subfolder in TIER_B_SUBFOLDERS else None
        note_type = meta.note_type or inferred
        if not note_type:
            issues.append(f"{rel}: missing note_type (Tier B)")
        elif note_type not in NOTE_TYPES:
            issues.append(f"{rel}: invalid note_type `{note_type}`")
        if not meta.source_basis:
            issues.append(f"{rel}: missing source_basis (Tier B)")
        elif meta.source_basis not in SOURCE_BASIS:
            issues.append(f"{rel}: invalid source_basis `{meta.source_basis}`")
        return issues

    if meta.tier != "A":
        return issues

    if not meta.note_type:
        issues.append(f"{rel}: missing note_type")
    elif meta.note_type not in TIER_A_TYPES:
        issues.append(f"{rel}: invalid note_type `{meta.note_type}`")

    if not meta.source_basis:
        issues.append(f"{rel}: missing source_basis")
    elif meta.source_basis not in SOURCE_BASIS:
        issues.append(f"{rel}: invalid source_basis `{meta.source_basis}`")

    if not meta.authority_level:
        issues.append(f"{rel}: missing authority_level")
    elif meta.authority_level not in AUTHORITY_LEVELS:
        issues.append(f"{rel}: invalid authority_level `{meta.authority_level}`")

    if (
        meta.prefix_inferred_type
        and meta.note_type
        and meta.prefix_inferred_type != meta.note_type
        and meta.authority_level not in {"review-needed", "deprecated"}
    ):
        issues.append(
            f"{rel}: prefix implies `{meta.prefix_inferred_type}` but note_type is `{meta.note_type}`"
        )

    authority = meta.authority_level or ""
    if authority == "shelf-native":
        archives = _all_archive_anchors(meta, text)
        synth = _synthesis_paths_in_text(text)
        basis = meta.source_basis or ""
        if basis == "source-archive" and not archives:
            issues.append(f"{rel}: shelf-native with source_basis source-archive requires archive anchor")
        elif basis == "synthesis" and not synth and not archives:
            issues.append(f"{rel}: shelf-native with source_basis synthesis requires synthesis or archive link")
        elif basis == "mixed" and not archives and not synth:
            issues.append(f"{rel}: shelf-native with source_basis mixed requires archive or synthesis link")
        elif not archives and not synth and basis not in SOURCE_BASIS:
            issues.append(f"{rel}: shelf-native requires archive or synthesis anchor")

    if meta.essay_candidate:
        archives = _all_archive_anchors(meta, text)
        distinct_archives = len(set(archives))
        if distinct_archives < 3 and inbound_count < 2:
            issues.append(
                f"{rel}: essay_candidate requires >=3 archive anchors or >=2 inbound note links"
            )

    return issues


def scan_notes(
    *,
    tier_a_only: bool = False,
    changed_only: bool = False,
    warn_orphans: bool = True,
) -> tuple[list[str], int]:
    paths = collect_note_files(tier_a_only=tier_a_only, changed_only=changed_only)
    inbound = build_inbound_note_links(list(NOTES_ROOT.rglob("*.md")))
    issues: list[str] = []
    scanned = 0

    for path in paths:
        tier = classify_tier(path)
        if tier not in {"A", "B"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if STUB_MARKER in text:
            continue
        meta = parse_note_metadata(path, text)
        rel = meta.rel
        scanned += 1
        issues.extend(
            validate_note(meta, text=text, inbound_count=inbound.get(rel, 0))
        )
        if warn_orphans and tier == "A" and meta.authority_level == "shelf-native":
            out_links = [
                raw
                for raw in LINK_RE.findall(text)
                if _resolve_link(path, raw) is not None
            ]
            if inbound.get(rel, 0) == 0 and not out_links:
                issues.append(f"{rel}: orphan shelf-native note (no in/out links)")

    return issues, scanned


def run_check(
    *,
    strict: bool,
    tier_a_only: bool = False,
    changed_only: bool = False,
    verify: bool = False,
) -> int:
    issues, scanned = scan_notes(
        tier_a_only=tier_a_only,
        changed_only=changed_only,
        warn_orphans=not verify,
    )
    if issues:
        for line in issues:
            print(line, file=sys.stderr)
        mode = "strict" if strict else "warn"
        scope = []
        if tier_a_only:
            scope.append("tier-a")
        if changed_only:
            scope.append("changed-only")
        suffix = f" ({', '.join(scope)})" if scope else ""
        print(
            f"check_statecraft_notes ({mode}){suffix}: {len(issues)} violation(s) across {scanned} note(s)",
            file=sys.stderr,
        )
        return 1 if strict else 0

    scope = []
    if tier_a_only:
        scope.append("tier-a")
    if changed_only:
        scope.append("changed-only")
    suffix = f" ({', '.join(scope)})" if scope else ""
    print(f"check_statecraft_notes: ok ({scanned} note(s){suffix})")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--strict", action="store_true", help="Exit 1 on violations")
    ap.add_argument("--warn", action="store_true", help="Warn only (default)")
    ap.add_argument("--tier-a-only", action="store_true", help="Scan Tier A notes only")
    ap.add_argument(
        "--changed-only",
        action="store_true",
        help="Scan only git-changed note paths under statecraft/notes/",
    )
    ap.add_argument(
        "--verify",
        action="store_true",
        help="Promotion verify pass (skip orphan warnings)",
    )
    args = ap.parse_args()
    return run_check(
        strict=args.strict,
        tier_a_only=args.tier_a_only,
        changed_only=args.changed_only,
        verify=args.verify,
    )


if __name__ == "__main__":
    raise SystemExit(main())
