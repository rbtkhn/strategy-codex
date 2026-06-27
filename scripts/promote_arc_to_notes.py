#!/usr/bin/env python3
"""Promote shelf *-arc.md bodies from voices/ and channels/ to statecraft/notes/."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
NOTES = REPO / "statecraft" / "notes"
VOICES = REPO / "statecraft" / "voices"
CHANNELS = REPO / "statecraft" / "channels"
RECEIPT = REPO / "runtime" / "artifacts" / "arc-promote-to-notes-receipt.json"

CHANNEL_HOST_PREFIX: dict[str, str] = {
    "daniel-davis": "davis",
    "judging-freedom": "napolitano",
    "dialogue-works": "nima",
}

SKIP_VOICE_DIRS = frozenset({"_scratch", "_templates", "map", "relations"})

REWRITE_SCAN = (
    "statecraft",
    "docs",
    ".cursor",
    "skills",
    "tests",
    "scripts",
    "codex",
    "LLM-ROUTING.md",
    "README.md",
)

REWRITE_EXCLUDE_PREFIXES = (
    "runtime/artifacts/benchmarks/",
    "runtime/artifacts/arc-promote",
    ".cursor/plans/",
    "public/predictive-history/",
)

# Pilot names — do not rename
DEST_OVERRIDES: dict[str, str] = {
    "statecraft/notes/arc-mearsheimer-davis-host.md": "arc-mearsheimer-davis-host.md",
    "statecraft/notes/arc-mearsheimer-diesen-host.md": "arc-mearsheimer-diesen-host.md",
    "statecraft/notes/arc-mearsheimer-napolitano-host.md": "arc-mearsheimer-napolitano-host.md",
}


@dataclass
class ArcMove:
    canonical: Path
    dest: Path
    primary_voice: str
    host_channel: str | None
    stubs: tuple[Path, ...]
    title: str


def _rel(path: Path) -> str:
    return path.relative_to(REPO).as_posix()


def _normalize_stem(name: str) -> str:
    stem = name
    if stem.endswith("-speaker-arc"):
        return stem[: -len("-speaker-arc")]
    if stem.endswith("-arc"):
        return stem[: -len("-arc")]
    return stem


def _is_stub(text: str) -> bool:
    lower = text.lower()
    if "compat redirect" in lower:
        return True
    if len(text) < 700 and "canonical:" in lower and "legacy path:" in lower:
        return True
    if len(text) < 500 and "compatibility alias" in lower:
        return True
    if len(text) < 400 and "redirect to the canonical" in lower:
        return True
    return False


# Pilot / stable names keyed by (shelf_dir_rel, normalized_stem)
GROUP_DEST_OVERRIDES: dict[tuple[str, str], str] = {
    ("statecraft/channels/daniel-davis", "davis-mearsheimer"): "arc-mearsheimer-davis-host.md",
    ("statecraft/voices/diesen", "diesen-mearsheimer"): "arc-mearsheimer-diesen-host.md",
    ("statecraft/channels/judging-freedom", "napolitano-mearsheimer"): "arc-mearsheimer-napolitano-host.md",
}


def _dest_basename(canonical: Path, group_parent: str, group_stem: str) -> str:
    group_key = (group_parent, group_stem)
    if group_key in GROUP_DEST_OVERRIDES:
        return GROUP_DEST_OVERRIDES[group_key]

    key = _rel(canonical)
    if key in DEST_OVERRIDES:
        return DEST_OVERRIDES[key]

    stem = _normalize_stem(canonical.stem)
    shelf = canonical.parent.name
    parts = canonical.parts
    in_channels = "channels" in parts

    if "cross-host" in stem or "cross-context" in stem:
        return f"arc-{stem}.md"

    if in_channels:
        prefix = CHANNEL_HOST_PREFIX.get(shelf, "")
        if prefix and stem.startswith(f"{prefix}-"):
            guest = stem[len(prefix) + 1 :]
            return f"arc-{guest}-{prefix}-host.md"
        return f"arc-{stem}.md"

    # voices shelf
    if stem == shelf:
        return f"arc-{shelf}-continuity.md"
    if stem.startswith(f"{shelf}-"):
        guest = stem[len(shelf) + 1 :]
        return f"arc-{guest}-{shelf}-host.md"
    if shelf == "kent" and stem.endswith("-kent"):
        host = stem[: -len("-kent")]
        return f"arc-kent-{host}-host.md"
    if shelf == "jermy" and stem.endswith("-jermy"):
        host = stem[: -len("-jermy")]
        return f"arc-jermy-{host}-host.md"
    return f"arc-{stem}.md"


def _primary_voice(canonical: Path, dest_name: str) -> str:
    stem = _normalize_stem(canonical.stem)
    shelf = canonical.parent.name
    in_channels = "channels" in canonical.parts

    if in_channels:
        prefix = CHANNEL_HOST_PREFIX.get(shelf, "")
        if prefix and stem.startswith(f"{prefix}-"):
            return stem[len(prefix) + 1 :]
        return stem.split("-")[0] if stem else shelf

    if stem == shelf or "cross-host" in stem or "cross-context" in stem:
        return shelf
    if stem.startswith(f"{shelf}-"):
        return stem[len(shelf) + 1 :]
    if shelf == "kent" and stem.endswith("-kent"):
        return "kent"
    if shelf == "jermy" and stem.endswith("-jermy"):
        return "jermy"
    return shelf


def _host_channel(canonical: Path) -> str | None:
    if "channels" not in canonical.parts:
        if _normalize_stem(canonical.stem).startswith(f"{canonical.parent.name}-"):
            return "glenn-diesen" if canonical.parent.name == "diesen" else None
        return None
    return canonical.parent.name


def _title(canonical: Path) -> str:
    first = canonical.read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip()
    if first and not first.startswith("---"):
        return first
    return canonical.stem.replace("-", " ")


def _collect_arc_files() -> list[Path]:
    out: list[Path] = []
    for root in (VOICES, CHANNELS):
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*.md")):
            if any(p in SKIP_VOICE_DIRS for p in path.parts):
                continue
            if path.name.endswith("-arc.md") or path.name.endswith("-speaker-arc.md"):
                out.append(path)
    return out


def _group_key(path: Path) -> tuple[str, str]:
    return _rel(path.parent), _normalize_stem(path.stem)


def _pick_canonical(group: list[Path]) -> Path:
    bodies = [p for p in group if not _is_stub(p.read_text(encoding="utf-8"))]
    if not bodies:
        bodies = group
    bodies.sort(
        key=lambda p: (
            0 if p.name.endswith("-arc.md") and not p.name.endswith("-speaker-arc.md") else 1,
            -len(p.read_text(encoding="utf-8")),
        )
    )
    return bodies[0]


def plan_moves() -> list[ArcMove]:
    files = _collect_arc_files()
    groups: dict[tuple[str, str], list[Path]] = defaultdict(list)
    for f in files:
        groups[_group_key(f)].append(f)

    moves: list[ArcMove] = []
    used_dests: dict[str, Path] = {}

    for _key, group in sorted(groups.items()):
        group_parent, group_stem = _key
        canonical = _pick_canonical(group)
        if _is_stub(canonical.read_text(encoding="utf-8")):
            dest_name = _dest_basename(canonical, group_parent, group_stem)
            dest = NOTES / dest_name
            if not dest.is_file():
                continue
        else:
            dest_name = _dest_basename(canonical, group_parent, group_stem)
            dest = NOTES / dest_name
            if dest_name in used_dests and used_dests[dest_name] != canonical:
                dest_name = f"arc-{_normalize_stem(canonical.stem)}-legacy.md"
                dest = NOTES / dest_name
            used_dests[dest.name] = canonical

        primary = _primary_voice(canonical, dest.name)
        host = _host_channel(canonical)
        moves.append(
            ArcMove(
                canonical=canonical,
                dest=dest,
                primary_voice=primary,
                host_channel=host,
                stubs=tuple(sorted(set(group))),
                title=_title(canonical) if not _is_stub(canonical.read_text(encoding="utf-8")) else dest.stem,
            )
        )
    return moves


def _yaml_block(move: ArcMove) -> str:
    lines = [
        "---",
        "note_type: arc",
        f"primary_voice: {move.primary_voice}",
        f"topic: {_normalize_stem(move.canonical.stem).replace('_', '-')}",
        f"legacy_path: {_rel(move.canonical)}",
    ]
    if move.host_channel:
        lines.append(f"host_channel: {move.host_channel}")
    lines.append("---")
    return "\n".join(lines)


def _normalize_body(text: str, mapping: dict[str, str]) -> str:
    text = re.sub(
        r"/C:/dev/strategy-codex/codex/years/(\d{4})/provenance/",
        r"../../source-archive/statecraft/",
        text,
        flags=re.I,
    )
    text = re.sub(
        r"\.\./\.\./\.\./codex/years/(\d{4})/provenance/",
        r"../../source-archive/statecraft/",
        text,
    )
    text = re.sub(
        r"/C:/dev/strategy-codex/statecraft/notes/",
        "",
        text,
        flags=re.I,
    )
    for old_base, new_base in sorted(mapping.items(), key=lambda x: -len(x[0])):
        text = text.replace(old_base, new_base)
    text = re.sub(
        r"\(\../../source-archive/statecraft/([^\)]+)\.md(?!\))",
        r"(../../source-archive/statecraft/\1.md)",
        text,
    )
    return text


def _stub_rel(stub: Path, dest_name: str) -> str:
    depth = len(stub.relative_to(REPO).parts) - 2
    return Path(*([".."] * depth), "notes", dest_name).as_posix()


def _stub_body(title: str, rel_link: str, legacy: str, speaker_arc: bool) -> str:
    extra = (
        "Legacy `*-speaker-arc.md` — pointer only.\n\nDo not treat this as a second arc class."
        if speaker_arc
        else "Pointer only; do not duplicate arc bodies here."
    )
    return f"""# {title} (compat redirect)

WORK only; not Record.

**Canonical:** [{rel_link.split('/')[-1]}]({rel_link})

Legacy path: `{legacy}` — {extra}
"""


def _build_link_mapping(moves: list[ArcMove]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for move in moves:
        dest_rel = _rel(move.dest)
        dest_name = move.dest.name
        for stub in move.stubs:
            legacy_rel = _rel(stub)
            mapping[legacy_rel] = dest_rel
            mapping[stub.name] = dest_name
            old_stem = stub.stem
            mapping[old_stem] = dest_name[:-3] if dest_name.endswith(".md") else dest_name
        mapping[_rel(move.canonical)] = dest_rel
        mapping[move.canonical.name] = dest_name
    return mapping


def _rewrite_repo(mapping: dict[str, str]) -> list[str]:
    changed: list[str] = []
    items = sorted(mapping.items(), key=lambda x: -len(x[0]))
    for scan in REWRITE_SCAN:
        root = REPO / scan
        if not root.is_file():
            if not root.is_dir():
                continue
            paths = sorted(root.rglob("*.md")) + sorted(root.rglob("*.py"))
        else:
            paths = [root]
        for fp in paths:
            rel = _rel(fp)
            if any(rel.startswith(p) for p in REWRITE_EXCLUDE_PREFIXES):
                continue
            if fp.suffix not in {".md", ".py"}:
                continue
            try:
                text = fp.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if fp.suffix != ".md":
                continue
            if "compat redirect" in text.lower():
                continue
            orig = text
            for old, new in items:
                if old.endswith(".md") and not new.endswith(".md"):
                    continue
                text = text.replace(old, new)
            # common relative rewrites to notes/
            text = re.sub(
                r"\.\./\.\./\.\./statecraft/notes/(arc-[a-z0-9-]+\.md)",
                r"../../notes/\1",
                text,
            )
            text = re.sub(
                r"statecraft/notes/(arc-[a-z0-9-]+\.md)",
                lambda m: m.group(1) if fp.parent == NOTES else f"statecraft/notes/{m.group(1)}",
                text,
            )
            if text != orig:
                fp.write_text(text, encoding="utf-8", newline="\n")
                changed.append(rel)
    return changed


def apply(dry_run: bool = False) -> dict:
    moves = plan_moves()
    link_map = _build_link_mapping(moves)
    receipt: dict = {"dry_run": dry_run, "promotions": [], "stubs": [], "skipped": []}

    for move in moves:
        entry = {
            "from": _rel(move.canonical),
            "to": _rel(move.dest),
            "stubs": [_rel(s) for s in move.stubs],
        }
        body = move.canonical.read_text(encoding="utf-8")
        if _is_stub(body):
            if move.dest.is_file():
                receipt["skipped"].append(entry)
                if not dry_run:
                    for stub in move.stubs:
                        rel = _stub_rel(stub, move.dest.name)
                        stub.write_text(
                            _stub_body(
                                move.title,
                                rel,
                                _rel(stub),
                                stub.name.endswith("-speaker-arc.md"),
                            ),
                            encoding="utf-8",
                            newline="\n",
                        )
                continue
            receipt["skipped"].append({**entry, "reason": "stub without notes target"})
            continue

        if dry_run:
            receipt["promotions"].append(entry)
            continue

        if body.lstrip().startswith("---"):
            body = body.split("---", 2)[-1].lstrip("\n")
        promoted = _yaml_block(move) + "\n\n" + _normalize_body(body, link_map)
        move.dest.parent.mkdir(parents=True, exist_ok=True)
        move.dest.write_text(promoted, encoding="utf-8", newline="\n")
        receipt["promotions"].append(entry)

        for stub in move.stubs:
            rel = _stub_rel(stub, move.dest.name)
            stub.write_text(
                _stub_body(
                    move.title,
                    rel,
                    _rel(stub),
                    stub.name.endswith("-speaker-arc.md"),
                ),
                encoding="utf-8",
                newline="\n",
            )
            receipt["stubs"].append(_rel(stub))

    if not dry_run:
        receipt["rewrites"] = _rewrite_repo(link_map)
        RECEIPT.parent.mkdir(parents=True, exist_ok=True)
        RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    else:
        receipt["would_rewrite_files"] = len(link_map)

    receipt["move_count"] = len(moves)
    receipt["promote_count"] = len(receipt["promotions"])
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    if not args.dry_run and not args.apply:
        parser.error("Specify --dry-run or --apply")
    receipt = apply(dry_run=args.dry_run)
    print(json.dumps(receipt, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
