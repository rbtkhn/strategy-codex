#!/usr/bin/env python3
"""Promote {speaker}-source-index.md to {speaker}-index.md with compat stub."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
VOICES = REPO_ROOT / "statecraft" / "voices"
REPO_MAP = REPO_ROOT / "repo-map.yaml"

PROMOTE = [
    "barnes",
    "crooke",
    "freeman",
    "helmer",
    "hoh",
    "jermy",
    "jiang",
    "johnson",
    "karaganov",
    "kent",
    "krapivnik",
    "lascaris",
    "macgregor",
    "marandi",
    "martyanov",
    "mate",
    "mcgovern",
    "mearsheimer",
    "parsi",
    "postol",
    "ritter",
    "sachs",
    "weichert",
    "wilkerson",
]

COMPAT_TEMPLATE = """WORK only; not Record.

# {title} Source Index (compat redirect)

Compatibility pointer only.

The canonical exhaustive {title} corpus route map now lives at **[{slug}-index.md]({slug}-index.md)**.

Use **`{slug}-index.md`** going forward; this file remains only as a stable back-compat entry for older links and routing discovery.
"""


def _is_compat_stub(text: str) -> bool:
    return "compat redirect" in text.lower()


def promote_speaker(slug: str) -> bool:
    folder = VOICES / slug
    src = folder / f"{slug}-source-index.md"
    dst = folder / f"{slug}-index.md"
    if not src.is_file():
        print(f"skip {slug}: no source-index")
        return False
    if dst.is_file() and not _is_compat_stub(src.read_text(encoding="utf-8")):
        print(f"skip {slug}: index already exists")
        return False
    if dst.is_file():
        dst.unlink()
    subprocess.run(
        ["git", "mv", str(src), str(dst)],
        cwd=REPO_ROOT,
        check=True,
    )
    title = slug.replace("-", " ").title()
    if slug == "mate":
        title = "Maté"
    src.write_text(
        COMPAT_TEMPLATE.format(title=title, slug=slug),
        encoding="utf-8",
        newline="\n",
    )
    body = dst.read_text(encoding="utf-8")
    if "source index" in body.lower() and f"# {title}" not in body:
        body = body.replace("source index", "index", 1)
        dst.write_text(body, encoding="utf-8", newline="\n")
    print(f"promoted {slug}")
    return True


def update_repo_map(promoted: list[str]) -> None:
    data = yaml.safe_load(REPO_MAP.read_text(encoding="utf-8"))
    routes = data.get("routes") or []
    by_id = {r.get("id"): r for r in routes if r.get("id")}

    for slug in promoted:
        src_id = f"{slug}-source-index"
        idx_id = f"{slug}-index"
        src_route = by_id.get(src_id)
        if not src_route:
            print(f"warn: repo-map missing {src_id}")
            continue
        if idx_id not in by_id:
            idx_route = dict(src_route)
            idx_route["id"] = idx_id
            idx_route["title"] = src_route.get("title", "").replace(" source index", " index").replace(
                " Source Index", " Index"
            )
            if idx_route["title"] == src_route.get("title"):
                idx_route["title"] = f"{slug.replace('-', ' ').title()} index"
            idx_route["path"] = f"statecraft/voices/{slug}/{slug}-index.md"
            hints = list(idx_route.get("search_hints") or [])
            primary_hint = f"{slug.replace('-', ' ').title()} index"
            if primary_hint not in hints:
                hints.insert(0, primary_hint)
            idx_route["search_hints"] = hints
            insert_at = next(
                (i for i, r in enumerate(routes) if r.get("id") == src_id),
                len(routes),
            )
            routes.insert(insert_at, idx_route)
            by_id[idx_id] = idx_route
        src_route["title"] = f"{src_route.get('title', slug)} (compat redirect)"
        compat_hints = list(src_route.get("search_hints") or [])
        if f"{slug} source index compat" not in compat_hints:
            compat_hints.append(f"{slug} source index compat")
        src_route["search_hints"] = compat_hints

    data["routes"] = routes
    REPO_MAP.write_text(
        yaml.dump(data, sort_keys=False, allow_unicode=True, default_flow_style=False),
        encoding="utf-8",
        newline="\n",
    )


def main() -> int:
    promoted: list[str] = []
    for slug in PROMOTE:
        if promote_speaker(slug):
            promoted.append(slug)
    if promoted:
        update_repo_map(promoted)
    print(f"done: {len(promoted)} promoted")
    return 0


if __name__ == "__main__":
    sys.exit(main())
