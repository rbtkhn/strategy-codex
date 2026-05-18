#!/usr/bin/env python3
"""Build a derived speaker-routing queue from raw-input frontmatter.

WORK-layer advisory automation only. This script reads raw-input files and the
current speaker/arc inventory, then writes queue artifacts under artifacts/.
It does not edit speaker folders, lattice rows, or raw-input files.
"""

from __future__ import annotations

import argparse
import hashlib
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
from codex_paths import speakers_root, year_root  # noqa: E402


DEFAULT_NOTEBOOK_ROOT = year_root()
DEFAULT_SPEAKERS_DIR = speakers_root()
DEFAULT_OUT_DIR = REPO_ROOT / "artifacts" / "speaker-routing"
EVIDENCE_GRADES = {
    "transcript-grade",
    "cleaned-transcript",
    "transcript-bearing",
    "summary-grade",
    "legacy-appearance-only",
}
ROUTE_TYPES = {
    "existing-speaker-object",
    "existing-speaker-arc",
    "candidate-speaker-object",
    "candidate-speaker-arc",
    "no-clear-route",
}
NEXT_ACTIONS = {
    "update-existing-arc",
    "review-existing-object",
    "create-candidate-arc",
    "create-candidate-object",
    "no-action",
}
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


@dataclass(frozen=True)
class SpeakerInventory:
    speakers_dir: Path
    speaker_folders: dict[str, Path]
    speaker_objects: dict[str, Path]
    speaker_comparative_notes: dict[str, list[Path]]
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


def load_raw_input_list(path: Path, *, base_dir: Path = REPO_ROOT) -> list[Path]:
    paths: list[Path] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        item = Path(line)
        if not item.is_absolute():
            item = base_dir / item
        paths.append(item)
    return paths


def normalize_raw_input_paths(paths: list[Path], *, base_dir: Path = REPO_ROOT) -> list[Path]:
    out: list[Path] = []
    seen: set[Path] = set()
    for raw_path in paths:
        path = raw_path if raw_path.is_absolute() else base_dir / raw_path
        resolved = path.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        out.append(resolved)
    return out


def window_for_raw_paths(paths: list[Path]) -> tuple[date, date]:
    dates: list[date] = []
    for path in paths:
        meta = _read_frontmatter(path) if path.exists() else {}
        raw_date = str(meta.get("pub_date") or meta.get("ingest_date") or path.parent.name)
        dates.append(_parse_date(raw_date))
    if not dates:
        today = date.today()
        return today, today
    return min(dates), max(dates)


def _discover_inventory(speakers_dir: Path, notebook_root: Path) -> SpeakerInventory:
    speaker_folders: dict[str, Path] = {}
    speaker_objects: dict[str, Path] = {}
    if speakers_dir.exists():
        for folder in sorted(path for path in speakers_dir.iterdir() if path.is_dir()):
            speaker_folders[folder.name] = folder
            obj = folder / f"{folder.name}-speaker-object.md"
            if obj.exists():
                speaker_objects[folder.name] = obj
    speaker_comparative_notes: dict[str, list[Path]] = {}
    for speaker, folder in speaker_folders.items():
        notes = [
            path
            for path in sorted(folder.glob("*.md"))
            if path.name.endswith("-cross-host-note.md") or "helix" in path.stem
        ]
        if notes:
            speaker_comparative_notes[speaker] = notes

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
        speaker_comparative_notes=speaker_comparative_notes,
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
    for key in ("host", "hosts", "show", "series", "channel_slug", "thread"):
        for candidate in _slug_candidates(meta.get(key)):
            if candidate not in candidates:
                candidates.append(candidate)
    canonical = _canonical_host_slug(meta)
    if canonical and canonical not in candidates:
        candidates.insert(0, canonical)
    return candidates


def classify_evidence_grade(meta: dict[str, Any], verification_reason: str = "") -> str:
    verification_lower = verification_reason.casefold()
    kind = str(meta.get("kind") or "").strip().casefold()
    source_type = str(meta.get("source_type") or "").strip().casefold()
    transcript_type = str(meta.get("transcript_type") or "").strip().casefold()

    if "appearance-eligible legacy raw-input" in verification_lower:
        return "legacy-appearance-only"
    if "operator_summary" in transcript_type or source_type.startswith("operator-note-derived"):
        return "summary-grade"
    if kind == "cleaned-transcript":
        return "cleaned-transcript"
    if kind == "transcript" and (not source_type or not transcript_type):
        return "legacy-appearance-only"
    if kind == "transcript" and transcript_type == "manual_subtitles_vtt":
        return "transcript-grade"
    if kind == "transcript":
        return "transcript-bearing"
    return "legacy-appearance-only"


def _canonical_host_slug(meta: dict[str, Any]) -> str:
    hostish: list[str] = []
    for key in ("channel_slug", "show", "series", "host", "hosts"):
        for candidate in _slug_candidates(meta.get(key)):
            if candidate not in hostish:
                hostish.append(candidate)
    host_slug = hostish[-1] if hostish else ""
    if not host_slug:
        thread_candidates = _slug_candidates(meta.get("thread"))
        host_slug = thread_candidates[-1] if thread_candidates else ""
    if host_slug in {"glenn-diesen", "diesen"}:
        return "diesen"
    if host_slug in {"daniel-davis", "davis", "daniel-davis-deep-dive", "col-daniel-davis", "lt-col-daniel-davis"}:
        return "davis"
    if host_slug in {"dialogue-works", "alkhorshid", "nima", "nima-alkhorshid"}:
        return "alkorshid"
    if host_slug in {"alexander-mercouris", "alex-mercouris", "mercouris"}:
        return "mercouris"
    if host_slug in {"judge-andrew-napolitano", "andrew-napolitano", "judging-freedom", "napolitano"}:
        return "napolitano"
    return host_slug


def _match_arc(host_candidates: list[str], guest_slug: str, inventory: SpeakerInventory) -> Path | None:
    guest_candidates = _slug_candidates(guest_slug)
    for host in host_candidates:
        for guest in guest_candidates:
            path = inventory.arcs.get((host, guest))
            if path:
                return path
    return None


def _speaker_strengthening_paths(speaker_slug: str | None, inventory: SpeakerInventory) -> list[str]:
    if not speaker_slug:
        return []
    paths: list[str] = []
    obj = inventory.speaker_objects.get(speaker_slug)
    if obj:
        paths.append(_rel(obj))
    for note in inventory.speaker_comparative_notes.get(speaker_slug, []):
        rel = _rel(note)
        if rel not in paths:
            paths.append(rel)
    return paths


def _route(
    *,
    recommended_route: str,
    route_type: str,
    confidence: str,
    reason: str,
    next_action: str,
    also_strengthens: list[str] | None = None,
) -> dict[str, Any]:
    primary_route = recommended_route
    also = [path for path in (also_strengthens or []) if path and path != primary_route]
    if next_action not in NEXT_ACTIONS:
        raise ValueError(f"unknown next_action {next_action!r}")
    return {
        "recommended_route": recommended_route,
        "primary_route": primary_route,
        "also_strengthens": also,
        "route_type": route_type,
        "confidence": confidence,
        "next_action": next_action,
        "reason": reason,
    }


def _candidate_object_path(guest_slug: str, inventory: SpeakerInventory) -> Path:
    return inventory.speakers_dir / guest_slug / f"{guest_slug}-speaker-object.md"


def _candidate_arc_path(meta: dict[str, Any], guest_slug: str, notebook_root: Path) -> Path:
    host_slug = _canonical_host_slug(meta) or "host"
    host_dir = host_slug
    return notebook_root / host_dir / f"{host_slug}-{guest_slug}-speaker-arc.md"


def _resolved_speaker(meta: dict[str, Any], inventory: SpeakerInventory) -> tuple[str, str]:
    guest = str(meta.get("guest") or "").strip()
    if not guest:
        return "", ""
    guest_slug = _match_speaker(guest, inventory)
    if guest_slug:
        return guest_slug, "guest-metadata-match"
    guest_candidates = _slug_candidates(guest)
    return (guest_candidates[-1], "guest-metadata-slug") if guest_candidates else ("", "")


def route_raw_input(path: Path, meta: dict[str, Any], inventory: SpeakerInventory, notebook_root: Path) -> dict[str, Any]:
    guest = str(meta.get("guest") or "").strip()
    host_candidates = _host_candidates(meta)
    guessed_guest_slug, _speaker_resolution = _resolved_speaker(meta, inventory)
    matched_speaker = guessed_guest_slug if guessed_guest_slug in inventory.speaker_folders else None

    if guessed_guest_slug:
        arc = _match_arc(host_candidates, guessed_guest_slug, inventory)
        if arc:
            return _route(
                recommended_route=_rel(arc),
                route_type="existing-speaker-arc",
                confidence="high",
                next_action="update-existing-arc",
                also_strengthens=_speaker_strengthening_paths(matched_speaker, inventory),
                reason="Matched host plus guest to an existing host-local speaker arc.",
            )

    if matched_speaker and matched_speaker in inventory.speaker_objects:
        also_strengthens: list[str] = []
        next_action = "review-existing-object"
        if guest and host_candidates:
            candidate_arc = _candidate_arc_path(meta, guessed_guest_slug or matched_speaker, notebook_root)
            also_strengthens.append(_rel(candidate_arc))
            next_action = "create-candidate-arc"
        also_strengthens.extend(_speaker_strengthening_paths(matched_speaker, inventory))
        return _route(
            recommended_route=_rel(inventory.speaker_objects[matched_speaker]),
            route_type="existing-speaker-object",
            confidence="high",
            next_action=next_action,
            also_strengthens=also_strengthens,
            reason=f"Matched guest metadata to existing speaker object `{matched_speaker}`.",
        )

    if matched_speaker:
        candidate = _candidate_object_path(matched_speaker, inventory)
        return _route(
            recommended_route=_rel(candidate),
            route_type="candidate-speaker-object",
            confidence="medium",
            next_action="create-candidate-object",
            reason=f"Matched guest metadata to speaker folder `{matched_speaker}`, but no speaker object exists yet.",
        )

    if guest and guessed_guest_slug:
        candidate = _candidate_arc_path(meta, guessed_guest_slug, notebook_root)
        return _route(
            recommended_route=_rel(candidate),
            route_type="candidate-speaker-arc",
            confidence="medium",
            next_action="create-candidate-arc",
            reason="Guest metadata is present, but no existing speaker object or host-local arc matched.",
        )

    return {}


def _appearance(path: Path, meta: dict[str, Any], inventory: SpeakerInventory) -> dict[str, str]:
    guest = str(meta.get("guest") or "").strip()
    thread = str(meta.get("thread") or "").strip()
    speaker_slug, speaker_resolution = _resolved_speaker(meta, inventory)
    host_slug = _canonical_host_slug(meta)
    pub_date = str(meta.get("pub_date") or meta.get("ingest_date") or path.parent.name)
    raw_input_path = _rel(path)
    source_url = str(meta.get("source_url") or "")
    youtube_id = str(meta.get("youtube_id") or "").strip()
    identity = "|".join([source_url.casefold(), youtube_id.casefold(), pub_date, speaker_slug, host_slug])
    return {
        "appearance_id": f"ap-{hashlib.sha1(identity.encode('utf-8')).hexdigest()[:12]}",
        "speaker": guest,
        "speaker_slug": speaker_slug,
        "guest": guest,
        "host": str(meta.get("host") or ""),
        "host_slug": host_slug,
        "show": str(meta.get("show") or ""),
        "thread": thread,
        "pub_date": pub_date,
        "title": str(meta.get("title") or path.stem),
        "source_url": source_url,
        "youtube_id": youtube_id,
        "raw_input_path": raw_input_path,
        "speaker_resolution": speaker_resolution,
        "guest_inference": str(meta.get("guest_inference") or ""),
    }


def build_rows(raw_paths: list[Path], inventory: SpeakerInventory, notebook_root: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in raw_paths:
        meta = _read_frontmatter(path)
        appearance = _appearance(path, meta, inventory)
        if not appearance["speaker_slug"]:
            continue
        route = route_raw_input(path, meta, inventory, notebook_root)
        route_type = route.get("route_type", "")
        if route_type not in ROUTE_TYPES:
            raise ValueError(f"unknown route_type {route_type!r}")
        evidence_grade = classify_evidence_grade(meta)
        if evidence_grade not in EVIDENCE_GRADES:
            raise ValueError(f"unknown evidence_grade {evidence_grade!r}")
        rows.append(
            {
                "raw_input_path": appearance["raw_input_path"],
                "pub_date": appearance["pub_date"],
                "title": appearance["title"],
                "source_url": appearance["source_url"],
                "host": appearance["host"],
                "show": appearance["show"],
                "guest": appearance["guest"],
                "thread": appearance["thread"],
                "recommended_route": route["recommended_route"],
                "primary_route": route["primary_route"],
                "also_strengthens": route["also_strengthens"],
                "appearance": appearance,
                "evidence_grade": evidence_grade,
                "route_type": route_type,
                "confidence": route["confidence"],
                "next_action": route["next_action"],
                "reason": route["reason"],
            }
        )
    return rows


def build_unresolved_rows(raw_paths: list[Path], inventory: SpeakerInventory) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in raw_paths:
        meta = _read_frontmatter(path)
        appearance = _appearance(path, meta, inventory)
        if appearance["speaker_slug"]:
            continue
        rows.append(
            {
                "raw_input_path": appearance["raw_input_path"],
                "pub_date": appearance["pub_date"],
                "title": appearance["title"],
                "source_url": appearance["source_url"],
                "host": appearance["host"],
                "show": appearance["show"],
                "guest": appearance["guest"],
                "thread": appearance["thread"],
                "appearance": appearance,
                "evidence_grade": classify_evidence_grade(meta),
                "reason": "Guest metadata is absent or ambiguous, so no speaker appearance was emitted.",
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
                f"-> `{route}` (`{row['next_action']}`) evidence `{row['evidence_grade']}`"
            )
            lines.append(f"  - raw: `{row['raw_input_path']}`")
            if row["also_strengthens"]:
                lines.append(f"  - also strengthens: {', '.join(f'`{path}`' for path in row['also_strengthens'])}")
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

    appearance_path = window_dir / "appearance-ledger.jsonl"
    with appearance_path.open("w", encoding="utf-8", newline="") as fh:
        for row in rows:
            fh.write(json.dumps(row["appearance"], ensure_ascii=True, sort_keys=True) + "\n")

    return {"jsonl": str(jsonl_path), "markdown": str(md_path), "appearance_ledger": str(appearance_path)}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start", type=_parse_date, help="Start date, YYYY-MM-DD.")
    parser.add_argument("--end", type=_parse_date, help="End date, YYYY-MM-DD.")
    parser.add_argument("--raw-input", action="append", type=Path, default=[], help="Explicit raw-input path. Repeatable.")
    parser.add_argument("--raw-input-list", type=Path, default=None, help="Text file with one raw-input path per line.")
    parser.add_argument("--notebook-root", type=Path, default=DEFAULT_NOTEBOOK_ROOT)
    parser.add_argument("--speakers-dir", type=Path, default=None)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUT_DIR)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    notebook_root = args.notebook_root.resolve()
    speakers_dir = (args.speakers_dir or DEFAULT_SPEAKERS_DIR).resolve()
    raw_root = notebook_root / "raw-input"
    inventory = _discover_inventory(speakers_dir, notebook_root)
    explicit_paths = list(args.raw_input)
    if args.raw_input_list:
        explicit_paths.extend(load_raw_input_list(args.raw_input_list))
    if explicit_paths:
        raw_paths = normalize_raw_input_paths(explicit_paths)
        start, end = window_for_raw_paths(raw_paths)
    else:
        if args.start is None or args.end is None:
            print("provide --start/--end or explicit --raw-input paths", file=sys.stderr)
            return 2
        if args.end < args.start:
            print("--end must be on or after --start", file=sys.stderr)
            return 2
        start, end = args.start, args.end
        raw_paths = _discover_raw_inputs(raw_root, start, end)
    rows = build_rows(raw_paths, inventory, notebook_root)
    written = write_outputs(rows, args.output_dir.resolve(), start, end)

    print(json.dumps({"rows": len(rows), "written": written}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
