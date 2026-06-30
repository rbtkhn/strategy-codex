#!/usr/bin/env python3
"""Backfill structured source-schema fields for bounded statecraft source slices."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import statecraft_day_archive as sda

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ROOT = REPO_ROOT / "source-archive" / "statecraft"
FRONTMATTER_RE = sda.FRONTMATTER_RE
STRUCTURED_KEYS = ("host_people", "guest_people", "show_title", "channel_name")

HOST_OVERRIDES: dict[str, tuple[str, ...]] = {
    "source-daniel-davis-col-douglas-macgregor-the-israel-first-white-house-2026-06-02.md": ("Daniel Davis",),
    "source-diesen-krapivnik-kiev-attacked-frontlines-fall-belarus-enters-war-2026-06-02.md": ("Glenn Diesen",),
}

def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="Statecraft source-archive root.")
    ap.add_argument("--from", dest="from_day", default="2026-06-01", help="Lower YYYY-MM-DD day bound.")
    ap.add_argument("--to", dest="to_day", default="2026-06-03", help="Upper YYYY-MM-DD day bound.")
    ap.add_argument("--check", action="store_true", help="Report pending rewrites without writing files.")
    return ap.parse_args()

def _ordered_meta_keys(block: str) -> list[str]:
    keys: list[str] = []
    for line in block.splitlines():
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):(?:\s|$)", line)
        if match and match.group(1) not in keys:
            keys.append(match.group(1))
    return keys

def _needs_quotes(value: str) -> bool:
    if value == "" or value != value.strip():
        return True
    return bool(re.search(r"[:{}\[\],#&*!?|>'\"%@`]", value))

def _render_scalar(value: object) -> str:
    text = sda.norm_scalar(value)
    if _needs_quotes(text):
        return json.dumps(text, ensure_ascii=False)
    return text

def _render_field(key: str, value: object) -> list[str]:
    if isinstance(value, (list, tuple)):
        items = [sda.norm_scalar(item) for item in value if sda.norm_scalar(item)]
        if not items:
            return [f"{key}: []"] if key in {"host_people", "guest_people"} else []
        return [f"{key}:"] + [f"  - {_render_scalar(item)}" for item in items]
    text = sda.norm_scalar(value)
    if not text:
        return []
    return [f"{key}: {_render_scalar(text)}"]

def _derive_host_people(meta: dict[str, object], file_name: str) -> tuple[str, ...]:
    if file_name in HOST_OVERRIDES:
        return HOST_OVERRIDES[file_name]
    return sda.host_meta_values(meta)

def _derive_guest_people(meta: dict[str, object], source_form: str) -> tuple[str, ...]:
    if source_form in {"newsletter", "article", "post"}:
        return ()
    return sda.guest_meta_values(meta)

def _derive_show_title(meta: dict[str, object], source_form: str) -> str:
    explicit = sda.norm_scalar(meta.get("show_title"))
    if explicit:
        return explicit
    if source_form in {"newsletter", "article", "post"}:
        return ""
    return sda.norm_scalar(meta.get("show"))

def _derive_channel_name(
    meta: dict[str, object],
    source_form: str,
    host_people: tuple[str, ...],
    show_title: str,
) -> str:
    explicit = sda.norm_scalar(meta.get("channel_name"))
    if explicit:
        return explicit
    publication = sda.norm_scalar(meta.get("publication"))
    if source_form in {"newsletter", "article"} and publication:
        return publication
    if show_title in {"Mercouris", "Diesen"} and len(host_people) == 1:
        return host_people[0]
    if show_title:
        return show_title
    if publication:
        return publication
    if len(host_people) == 1:
        return host_people[0]
    return sda.normalize_channel_label(sda.norm_scalar(meta.get("channel_slug")))

def _render_updated_frontmatter(path: Path) -> str:
    text = sda.read_text(path)
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError(f"missing frontmatter: {path}")

    block = match.group(1)
    meta = sda.parse_simple_frontmatter_block(block)
    ordered_keys = [key for key in _ordered_meta_keys(block) if key not in STRUCTURED_KEYS]

    source_form = sda.norm_scalar(meta.get("source_form")) or sda.infer_source_form(meta, sda.host_meta_values(meta), sda.guest_meta_values(meta))
    host_people = _derive_host_people(meta, path.name)
    guest_people = _derive_guest_people(meta, source_form)
    show_title = _derive_show_title(meta, source_form)
    channel_name = _derive_channel_name(meta, source_form, host_people, show_title)

    meta["host_people"] = list(host_people)
    meta["guest_people"] = list(guest_people)
    if show_title:
        meta["show_title"] = show_title
    else:
        meta.pop("show_title", None)
    if channel_name:
        meta["channel_name"] = channel_name
    else:
        meta.pop("channel_name", None)

    insert_at = ordered_keys.index("source_form") + 1 if "source_form" in ordered_keys else ordered_keys.index("kind") + 1 if "kind" in ordered_keys else 0
    new_order = list(ordered_keys)
    for offset, key in enumerate(STRUCTURED_KEYS):
        if key in meta:
            new_order.insert(insert_at + offset, key)

    lines = ["---"]
    for key in new_order:
        lines.extend(_render_field(key, meta.get(key)))
    lines.append("---")
    return "\n".join(lines) + text[match.end() - 1 :]

def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    day_dirs = sda.select_day_dirs(root, year=None, from_day=args.from_day, to_day=args.to_day)
    changed: list[Path] = []
    for day_dir in day_dirs:
        for path in sda.iter_source_files(day_dir):
            updated = _render_updated_frontmatter(path)
            current = sda.read_text(path)
            if updated != current:
                changed.append(path)
                if not args.check:
                    path.write_text(updated, encoding="utf-8", newline="\n")
    action = "would update" if args.check else "updated"
    print(f"{action} {len(changed)} files")
    for path in changed[:20]:
        print(path)
    return 1 if args.check and changed else 0

if __name__ == "__main__":
    raise SystemExit(main())
