#!/usr/bin/env python3
"""Build a derived speaker-routing queue from raw-input frontmatter.

WORK-layer advisory automation only. This script reads raw-input files and the
current speaker/arc inventory, then writes queue artifacts under artifacts/.
It does not edit speaker folders, lattice rows, or raw-input files.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from yaml_compat import safe_load_text  # noqa: E402


DEFAULT_NOTEBOOK_ROOT = REPO_ROOT / "codex" / str(date.today().year)
DEFAULT_SPEAKERS_DIR = DEFAULT_NOTEBOOK_ROOT / "speakers"
DEFAULT_OUT_DIR = REPO_ROOT / "artifacts" / "speaker-routing"
ROUTE_TYPES = {
    "existing-speaker-object",
    "existing-speaker-arc",
    "candidate-speaker-object",
    "candidate-speaker-arc",
    "no-clear-route",
}
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


@dataclass(frozen=True)
class SpeakerInventory:
    speakers_dir: Path
    speaker_folders: dict[str, Path]
    speaker_objects: dict[str, Path]
    arcs: dict[tuple[str, str], Path]


def _parse_date(value: str) -> date:
    return date.fromisoformat(value)


def _window_slug(start: date, end: date) -> str:
    return f"{start.isoformat()}_to_{end.isoformat()}"


def _slug(value: object) -> str:
    text = str(value or "").casefold()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def _slug_candidates(value: object) -> list[str]:
    slug = _slug(value)
    if not slug:
        return []
    parts = [part for part in slug.split("-") if part]
    candidates = [slug]
    if parts:
        candidates.append(parts[-1])
    if len(parts) >= 2 and parts[0] in {"col", "lt", "prof", "professor", "dr"}:
        candidates.append("-".join(parts[1:]))
        candidates.append(parts[-1])
    out: list[str] = []
    for candidate in candidates:
        if candidate and candidate not in out:
            out.append(candidate)
    return out


def _rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    data = safe_load_text(match.group(1), feature="build_speaker_routing_queue.py")
    return data if isinstance(data, dict) else {}


def _discover_raw_inputs(raw_root: Path, start: date, end: date) -> list[Path]:
    if not raw_root.exists():
        return []
    paths: list[Path] = []
    for date_dir in sorted(path for path in raw_root.iterdir() if path.is_dir()):
        try:
            current = _parse_date(date_dir.name)
        except ValueError:
            continue
        if start <= current <= end:
            paths.extend(sorted(date_dir.glob("*.md")))
    return paths


def _discover_inventory(speakers_dir: Path, notebook_root: Path) -> SpeakerInventory:
    speaker_folders: dict[str, Path] = {}
    speaker_objects: dict[str, Path] = {}
    if speakers_dir.exists():
        for folder in sorted(path for path in speakers_dir.iterdir() if path.is_dir()):
            speaker_folders[folder.name] = folder
            obj = folder / f"{folder.name}-speaker-object.md"
            if obj.exists():
                speaker_objects[folder.name] = obj

    arcs: dict[tuple[str, str], Path] = {}
    if notebook_root.exists():
        for path in sorted(notebook_root.rglob("*-speaker-arc.md")):
            stem = path.stem
            base = stem.removesuffix("-speaker-arc")
            parts = [part for part in base.split("-") if part]
            if len(parts) < 2:
                continue
            host, guest = parts[0], "-".join(parts[1:])
            arcs[(host, guest)] = path

    return SpeakerInventory(
        speakers_dir=speakers_dir,
        speaker_folders=speaker_folders,
        speaker_objects=speaker_objects,
        arcs=arcs,
    )


def _match_speaker(value: object, inventory: SpeakerInventory) -> str | None:
    candidates = _slug_candidates(value)
    for candidate in candidates:
        if candidate in inventory.speaker_folders:
            return candidate
    for speaker in inventory.speaker_folders:
        if speaker in candidates:
            return speaker
    return None


def _host_candidates(meta: dict[str, Any]) -> list[str]:
    candidates: list[str] = []
    for key in ("host", "show", "channel_slug", "thread"):
        for candidate in _slug_candidates(meta.get(key)):
            if candidate not in candidates:
                candidates.append(candidate)
    return candidates


def _match_arc(host_candidates: list[str], guest_slug: str, inventory: SpeakerInventory) -> Path | None:
    guest_candidates = _slug_candidates(guest_slug)
    for host in host_candidates:
        for guest in guest_candidates:
            path = inventory.arcs.get((host, guest))
            if path:
                return path
    return None


def _candidate_object_path(guest_slug: str, inventory: SpeakerInventory) -> Path:
    return inventory.speakers_dir / guest_slug / f"{guest_slug}-speaker-object.md"


def _candidate_arc_path(meta: dict[str, Any], guest_slug: str, notebook_root: Path) -> Path:
    host_slug = _slug(meta.get("channel_slug")) or (_host_candidates(meta)[-1] if _host_candidates(meta) else "host")
    host_dir = host_slug
    if host_slug in {"glenn-diesen", "diesen"}:
        host_dir = "diesen"
        host_slug = "diesen"
    elif host_slug in {"daniel-davis", "davis", "daniel-davis-deep-dive"}:
        host_dir = "davis"
        host_slug = "davis"
    elif host_slug in {"dialogue-works", "alkhorshid", "nima-alkhorshid"}:
        host_dir = "alkorshid"
        host_slug = "alkorshid"
    elif host_slug in {"alexander-mercouris", "alex-mercouris", "mercouris"}:
        host_dir = "mercouris"
        host_slug = "mercouris"
    return notebook_root / host_dir / f"{host_slug}-{guest_slug}-speaker-arc.md"


def route_raw_input(path: Path, meta: dict[str, Any], inventory: SpeakerInventory, notebook_root: Path) -> dict[str, Any]:
    title = str(meta.get("title") or path.stem)
    guest = str(meta.get("guest") or "").strip()
    thread = str(meta.get("thread") or "").strip()
    host_candidates = _host_candidates(meta)

    guest_slug = _match_speaker(guest, inventory) if guest else None
    thread_slug = _match_speaker(thread, inventory) if thread else None
    matched_speaker = guest_slug or thread_slug

    if matched_speaker and matched_speaker in inventory.speaker_objects:
        return {
            "recommended_route": _rel(inventory.speaker_objects[matched_speaker]),
            "route_type": "existing-speaker-object",
            "confidence": "high",
            "reason": f"Matched {'guest' if guest_slug else 'thread'} to existing speaker object `{matched_speaker}`.",
        }

    if guest:
        guessed_guest_slug = guest_slug or _slug_candidates(guest)[-1]
        arc = _match_arc(host_candidates, guessed_guest_slug, inventory)
        if arc:
            return {
                "recommended_route": _rel(arc),
                "route_type": "existing-speaker-arc",
                "confidence": "high",
                "reason": "Matched host plus guest to an existing host-local speaker arc.",
            }

    if matched_speaker:
        candidate = _candidate_object_path(matched_speaker, inventory)
        return {
            "recommended_route": _rel(candidate),
            "route_type": "candidate-speaker-object",
            "confidence": "medium",
            "reason": f"Matched {'guest' if guest_slug else 'thread'} to speaker folder `{matched_speaker}`, but no speaker object exists yet.",
        }

    if guest:
        guest_candidate = _slug_candidates(guest)[-1]
        candidate = _candidate_arc_path(meta, guest_candidate, notebook_root)
        return {
            "recommended_route": _rel(candidate),
            "route_type": "candidate-speaker-arc",
            "confidence": "medium",
            "reason": "Guest metadata is present, but no existing speaker object or host-local arc matched.",
        }

    return {
        "recommended_route": "",
        "route_type": "no-clear-route",
        "confidence": "low",
        "reason": "No guest metadata, matching speaker folder, or matching speaker arc found.",
    }


def build_rows(raw_paths: list[Path], inventory: SpeakerInventory, notebook_root: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in raw_paths:
        meta = _read_frontmatter(path)
        route = route_raw_input(path, meta, inventory, notebook_root)
        route_type = route["route_type"]
        if route_type not in ROUTE_TYPES:
            raise ValueError(f"unknown route_type {route_type!r}")
        rows.append(
            {
                "raw_input_path": _rel(path),
                "pub_date": str(meta.get("pub_date") or meta.get("ingest_date") or path.parent.name),
                "title": str(meta.get("title") or path.stem),
                "source_url": str(meta.get("source_url") or ""),
                "host": str(meta.get("host") or ""),
                "show": str(meta.get("show") or ""),
                "guest": str(meta.get("guest") or ""),
                "thread": str(meta.get("thread") or ""),
                "recommended_route": route["recommended_route"],
                "route_type": route_type,
                "confidence": route["confidence"],
                "reason": route["reason"],
            }
        )
    return rows


def _render_markdown(rows: list[dict[str, Any]], start: date, end: date) -> str:
    lines = [
        "# Speaker routing queue",
        "",
        "WORK only; not Record.",
        "",
        f"Window: `{start.isoformat()}` to `{end.isoformat()}`",
        "",
    ]
    if not rows:
        lines.extend(["_No raw-input files found._", ""])
        return "\n".join(lines)

    for route_type in sorted(ROUTE_TYPES):
        bucket = [row for row in rows if row["route_type"] == route_type]
        if not bucket:
            continue
        lines.extend([f"## {route_type}", ""])
        for row in bucket:
            route = row["recommended_route"] or "_none_"
            title = row["title"].replace("\n", " ")
            lines.append(
                f"- `{row['pub_date']}` `{row['confidence']}` [{title}]({row['source_url']}) "
                f"-> `{route}`"
            )
            lines.append(f"  - raw: `{row['raw_input_path']}`")
            lines.append(f"  - reason: {row['reason']}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_outputs(rows: list[dict[str, Any]], output_dir: Path, start: date, end: date) -> dict[str, str]:
    window_dir = output_dir / _window_slug(start, end)
    window_dir.mkdir(parents=True, exist_ok=True)

    jsonl_path = window_dir / "speaker-routing-queue.jsonl"
    with jsonl_path.open("w", encoding="utf-8", newline="") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n")

    md_path = window_dir / "speaker-routing-queue.md"
    md_path.write_text(_render_markdown(rows, start, end), encoding="utf-8")

    return {"jsonl": str(jsonl_path), "markdown": str(md_path)}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start", required=True, type=_parse_date, help="Start date, YYYY-MM-DD.")
    parser.add_argument("--end", required=True, type=_parse_date, help="End date, YYYY-MM-DD.")
    parser.add_argument("--notebook-root", type=Path, default=DEFAULT_NOTEBOOK_ROOT)
    parser.add_argument("--speakers-dir", type=Path, default=None)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUT_DIR)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.end < args.start:
        print("--end must be on or after --start", file=sys.stderr)
        return 2

    notebook_root = args.notebook_root.resolve()
    speakers_dir = (args.speakers_dir or (notebook_root / "speakers")).resolve()
    raw_root = notebook_root / "raw-input"
    inventory = _discover_inventory(speakers_dir, notebook_root)
    rows = build_rows(_discover_raw_inputs(raw_root, args.start, args.end), inventory, notebook_root)
    written = write_outputs(rows, args.output_dir.resolve(), args.start, args.end)

    print(json.dumps({"rows": len(rows), "written": written}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
