#!/usr/bin/env python3
"""Migrate legacy check-sources discovery receipt keys to canonical roster slugs.

Reads ``slug_aliases`` from ``platform/config/statecraft_youtube_discovery.json``
(the same map ``cognition_streams_audit`` expects for roster ``channel_key`` values).

Receipt layout::

    .codex-tmp/cognition-streams/<window>/<channel_key>.discovery.json

Default: dry-run (print planned renames / JSON patches). Use ``--apply`` to write.

Legacy name: cognition-streams receipt cache.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from cognition_streams_audit import DEFAULT_RECEIPT_ROOT  # noqa: E402
from statecraft_youtube_discovery import load_slug_aliases  # noqa: E402


@dataclass
class MigrationResult:
    renamed: list[str] = field(default_factory=list)
    patched: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)
    conflicts: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "renamed": self.renamed,
            "patched": self.patched,
            "skipped": self.skipped,
            "conflicts": self.conflicts,
            "counts": {
                "renamed": len(self.renamed),
                "patched": len(self.patched),
                "skipped": len(self.skipped),
                "conflicts": len(self.conflicts),
            },
        }


def _slug_from_receipt_path(path: Path) -> str:
    name = path.name
    suffix = ".discovery.json"
    if not name.endswith(suffix):
        raise ValueError(f"not a discovery receipt: {path}")
    return name[: -len(suffix)]


def _target_path(receipt_path: Path, canonical_slug: str) -> Path:
    return receipt_path.with_name(f"{canonical_slug}.discovery.json")


def _patch_channel_key(data: dict[str, Any], aliases: dict[str, str]) -> bool:
    key = str(data.get("channel_key") or "").strip()
    if not key or key not in aliases:
        return False
    data["channel_key"] = aliases[key]
    return True


def migrate_receipt_file(
    receipt_path: Path,
    aliases: dict[str, str],
    *,
    dry_run: bool,
) -> tuple[str, MigrationResult]:
    """Return action label and accumulate into a fresh partial result."""
    partial = MigrationResult()
    slug = _slug_from_receipt_path(receipt_path)
    canonical = aliases.get(slug, slug)
    target = _target_path(receipt_path, canonical)

    needs_rename = slug in aliases and receipt_path != target
    needs_patch = False
    data: dict[str, Any] | None = None

    if receipt_path.is_file():
        data = json.loads(receipt_path.read_text(encoding="utf-8"))
        needs_patch = _patch_channel_key(data, aliases)

    if not needs_rename and not needs_patch:
        partial.skipped.append(str(receipt_path))
        return "skip", partial

    if needs_rename and target.exists() and not target.samefile(receipt_path):
        partial.conflicts.append(f"{receipt_path} -> {target} (target exists)")
        return "conflict", partial

    label_parts: list[str] = []
    if needs_rename:
        label_parts.append(f"rename {slug} -> {canonical}")
        partial.renamed.append(f"{receipt_path} -> {target}")
        if not dry_run:
            if needs_patch and data is not None:
                target.write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
                receipt_path.unlink()
                partial.patched.append(str(target))
            else:
                receipt_path.rename(target)
    elif needs_patch and data is not None:
        label_parts.append(f"patch channel_key in {receipt_path.name}")
        partial.patched.append(str(receipt_path))
        if not dry_run:
            receipt_path.write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    return " ".join(label_parts) or "update", partial


def migrate_receipt_root(
    receipt_root: Path,
    aliases: dict[str, str],
    *,
    window: str | None = None,
    dry_run: bool = True,
) -> MigrationResult:
    result = MigrationResult()
    if not receipt_root.is_dir():
        return result

    window_dirs = sorted(p for p in receipt_root.iterdir() if p.is_dir())
    if window:
        window_dirs = [p for p in window_dirs if p.name == window]

    for window_dir in window_dirs:
        for receipt_path in sorted(window_dir.glob("*.discovery.json")):
            slug = _slug_from_receipt_path(receipt_path)
            if slug not in aliases:
                data: dict[str, Any] | None = None
                if receipt_path.is_file():
                    data = json.loads(receipt_path.read_text(encoding="utf-8"))
                    key = str(data.get("channel_key") or "").strip()
                    if key not in aliases:
                        continue
                else:
                    continue
            _, partial = migrate_receipt_file(receipt_path, aliases, dry_run=dry_run)
            result.renamed.extend(partial.renamed)
            result.patched.extend(partial.patched)
            result.skipped.extend(partial.skipped)
            result.conflicts.extend(partial.conflicts)

    return result


def _build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--receipt-root",
        type=Path,
        default=DEFAULT_RECEIPT_ROOT,
        help="Root containing window subdirs of *.discovery.json receipts",
    )
    ap.add_argument(
        "--window",
        help="Optional window slug filter (e.g. 2026-05-21_to_2026-05-21)",
    )
    ap.add_argument(
        "--apply",
        action="store_true",
        help="Perform renames and JSON patches (default: dry-run only)",
    )
    ap.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable summary JSON on stdout",
    )
    return ap


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    aliases = load_slug_aliases()
    if not aliases:
        print("error: slug_aliases is empty in discovery config", file=sys.stderr)
        return 1

    result = migrate_receipt_root(
        args.receipt_root.resolve(),
        aliases,
        window=args.window,
        dry_run=not args.apply,
    )

    mode = "apply" if args.apply else "dry-run"
    if args.json:
        payload = result.to_dict()
        payload["mode"] = mode
        payload["receipt_root"] = str(args.receipt_root.resolve())
        if args.window:
            payload["window"] = args.window
        print(json.dumps(payload, indent=2, ensure_ascii=True))
    else:
        print(f"# migrate_cognition_stream_receipt_keys ({mode})")
        for line in result.renamed:
            print(f"RENAME {line}")
        for line in result.patched:
            print(f"PATCH {line}")
        for line in result.conflicts:
            print(f"CONFLICT {line}")
        counts = result.to_dict()["counts"]
        print(
            f"# renamed={counts['renamed']} patched={counts['patched']} "
            f"conflicts={counts['conflicts']} skipped={counts['skipped']}"
        )

    return 1 if result.conflicts else 0


if __name__ == "__main__":
    raise SystemExit(main())
