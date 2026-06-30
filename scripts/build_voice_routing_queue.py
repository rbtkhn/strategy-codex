#!/usr/bin/env python3
"""Build a derived voice-routing queue from source-archive frontmatter.

WORK-layer advisory automation only. Reads source-archive files and the current
voice shelf / arc inventory, then writes queue artifacts under runtime/artifacts/.
Targets speaker-state shelves under statecraft/voices/ and host shelves under
statecraft/channels/. Not Grace-Mar Record Voice (bot/prompt.py). Does not edit
shelf folders, lattice rows, or source-archive files.
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
from repo_io import ARTIFACTS_DIR

from yaml_compat import safe_load_text  # noqa: E402

DEFAULT_NOTEBOOK_ROOT = REPO_ROOT / "source-archive" / "statecraft"
DEFAULT_CHANNELS_DIR = REPO_ROOT / "statecraft" / "channels"

# channel-index folder slug -> legacy file prefix inside shelf
CHANNEL_OBJECT_PREFIX = {
    "daniel-davis": "davis",
    "judging-freedom": "napolitano",
    "dialogue-works": "nima",
}
# legacy host slug -> channel-index folder name
CHANNEL_FOLDER_ALIASES = {
    "davis": "daniel-davis",
    "napolitano": "judging-freedom",
    "nima": "dialogue-works",
}
DEFAULT_VOICES_DIR = REPO_ROOT / "statecraft" / "voices"
DEFAULT_CHANNELS_DIR = REPO_ROOT / "statecraft" / "channels"
DEFAULT_NOTES_DIR = REPO_ROOT / "statecraft" / "notes"
DEFAULT_SPEAKERS_DIR = DEFAULT_VOICES_DIR
DEFAULT_OUT_DIR = ARTIFACTS_DIR / "voice-routing"
EVIDENCE_GRADES = {
    "transcript-grade",
    "cleaned-transcript",
    "transcript-bearing",
    "summary-grade",
    "legacy-appearance-only",
}
ROUTE_TYPES = {
    "existing-voice-object",
    "existing-voice-arc",
    "candidate-voice-object",
    "candidate-voice-arc",
    "no-clear-route",
}
LEGACY_ROUTE_TYPE = {
    "existing-speaker-object": "existing-voice-object",
    "existing-speaker-arc": "existing-voice-arc",
    "candidate-speaker-object": "candidate-voice-object",
    "candidate-speaker-arc": "candidate-voice-arc",
}
NEXT_ACTIONS = {
    "update-existing-arc",
    "review-existing-object",
    "create-candidate-arc",
    "create-candidate-object",
    "no-action",
}
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
SPEAKER_SLUG_ALIASES = {
    "alex-christoforou": "christoforou",
    "alex-christoforu": "christoforou",
    "christoforu": "christoforou",
    "john-kiriakou": "kiriakou",
    "stanislav-krapivnik": "krapivnik",
}

@dataclass(frozen=True)
class VoiceInventory:
    voices_dir: Path
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
        alias = SPEAKER_SLUG_ALIASES.get(candidate)
        if alias and alias not in out:
            out.append(alias)
    return out

def _rel(path: Path) -> str:
    def _rewrite(relative: str) -> str:
        rel = relative.replace("\\", "/")
        parts = rel.split("/")
        for idx in range(len(parts) - 2):
            if parts[idx] == "codex" and parts[idx + 1] == "2026":
                branch = parts[idx + 2]
                tail = "/".join(parts[idx + 3 :])
                if branch == "raw-input":
                    return "source-archive/statecraft" if not tail else f"source-archive/statecraft/{tail}"
                if branch == "speakers":
                    return "statecraft/voices" if not tail else f"statecraft/voices/{tail}"
                remainder = "/".join(parts[idx + 2 :])
                return f"codex/years/2026/{remainder}"
        return rel

    try:
        return _rewrite(path.resolve().relative_to(REPO_ROOT).as_posix())
    except ValueError:
        parts = list(path.resolve().parts)
        for anchor in ("codex", "source-archive", "runtime/artifacts"):
            if anchor in parts:
                return _rewrite(Path(*parts[parts.index(anchor) :]).as_posix())
        return _rewrite(path.as_posix())

def _read_frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8-sig")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    data = safe_load_text(match.group(1), feature="build_voice_routing_queue.py")
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

def normalize_route_row(row: dict[str, Any]) -> dict[str, Any]:
    rt = row.get("route_type")
    if isinstance(rt, str) and rt in LEGACY_ROUTE_TYPE:
        return {**row, "route_type": LEGACY_ROUTE_TYPE[rt]}
    return row

def _arc_host_guest_from_stem(stem: str) -> tuple[str, str] | None:
    if stem.startswith("arc-") and stem.endswith("-host"):
        inner = stem[4:-5]
        if "-" not in inner:
            return None
        guest, host = inner.rsplit("-", 1)
        if host and guest:
            return host, guest
        return None
    if stem.endswith("-speaker-arc"):
        base = stem.removesuffix("-speaker-arc")
    elif stem.endswith("-arc"):
        base = stem.removesuffix("-arc")
    else:
        return None
    parts = [part for part in base.split("-") if part]
    if len(parts) < 2:
        return None
    return parts[0], "-".join(parts[1:])

def _discover_inventory(voices_dir: Path, notebook_root: Path) -> VoiceInventory:
    speaker_folders: dict[str, Path] = {}
    speaker_objects: dict[str, Path] = {}
    roots: list[Path] = []
    for candidate in (voices_dir, DEFAULT_CHANNELS_DIR):
        if candidate.exists() and candidate not in roots:
            roots.append(candidate)
    for root in roots:
        for folder in sorted(path for path in root.iterdir() if path.is_dir()):
            if folder.name.startswith("_") or folder.name in {"relations", "map"}:
                continue
            speaker_folders[folder.name] = folder
            prefix = CHANNEL_OBJECT_PREFIX.get(folder.name, folder.name)
            obj = folder / f"{prefix}-speaker-object.md"
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
    arc_scan_roots: list[Path] = []
    if notebook_root.exists():
        arc_scan_roots.append(notebook_root)
    if voices_dir.resolve() == DEFAULT_VOICES_DIR.resolve():
        for candidate in (DEFAULT_NOTES_DIR, DEFAULT_CHANNELS_DIR):
            if candidate.exists() and candidate not in arc_scan_roots:
                arc_scan_roots.append(candidate)
    elif voices_dir.exists() and voices_dir not in arc_scan_roots:
        arc_scan_roots.append(voices_dir)
    for root in arc_scan_roots:
        arc_paths = sorted(root.rglob("*-speaker-arc.md"))
        arc_paths.extend(
            path for path in sorted(root.rglob("*-arc.md")) if not path.name.endswith("-speaker-arc.md")
        )
        arc_paths.extend(path for path in sorted(root.rglob("arc-*-host.md")))
        for path in arc_paths:
            pair = _arc_host_guest_from_stem(path.stem)
            if pair:
                arcs[pair] = path

    return VoiceInventory(
        voices_dir=voices_dir,
        speaker_folders=speaker_folders,
        speaker_objects=speaker_objects,
        speaker_comparative_notes=speaker_comparative_notes,
        arcs=arcs,
    )

def _match_speaker(value: object, inventory: VoiceInventory) -> str | None:
    candidates = _slug_candidates(value)
    for candidate in candidates:
        folder_key = CHANNEL_FOLDER_ALIASES.get(candidate, candidate)
        if folder_key in inventory.speaker_folders:
            return folder_key
        if candidate in inventory.speaker_folders:
            return candidate
    for speaker in inventory.speaker_folders:
        if speaker in candidates:
            return speaker
        for candidate in candidates:
            if CHANNEL_FOLDER_ALIASES.get(candidate) == speaker:
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
    if host_slug in {
        "dialogue-works",
        "alkhorshid",
        "alkhorshid",
        "nima",
        "nima-alkhorshid",
        "nima-alkorshid",
    }:
        return "nima"
    if host_slug in {"alexander-mercouris", "alex-mercouris", "mercouris"}:
        return "mercouris"
    if host_slug in {"alex-christoforou", "alex-christoforu", "christoforu", "christoforou"}:
        return "christoforou"
    if host_slug in {"judge-andrew-napolitano", "andrew-napolitano", "judging-freedom", "napolitano"}:
        return "napolitano"
    if host_slug in {"john-kiriakou", "kiriakou"}:
        return "kiriakou"
    return host_slug

def _match_arc(host_candidates: list[str], guest_slug: str, inventory: VoiceInventory) -> Path | None:
    guest_candidates = _slug_candidates(guest_slug)
    for host in host_candidates:
        for guest in guest_candidates:
            path = inventory.arcs.get((host, guest))
            if path:
                return path
    return None

def _speaker_strengthening_paths(speaker_slug: str | None, inventory: VoiceInventory) -> list[str]:
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

def _candidate_object_path(guest_slug: str, inventory: VoiceInventory) -> Path:
    return inventory.voices_dir / guest_slug / f"{guest_slug}-speaker-object.md"

def _candidate_arc_path(meta: dict[str, Any], guest_slug: str, notebook_root: Path) -> Path:
    host_slug = _canonical_host_slug(meta) or "host"
    host_dir = host_slug
    return notebook_root / host_dir / f"{host_slug}-{guest_slug}-speaker-arc.md"

def _resolved_speaker(meta: dict[str, Any], inventory: VoiceInventory) -> tuple[str, str]:
    guest = str(meta.get("guest") or "").strip()
    if not guest:
        return "", ""
    guest_slug = _match_speaker(guest, inventory)
    if guest_slug:
        return guest_slug, "guest-metadata-match"
    guest_candidates = _slug_candidates(guest)
    return (guest_candidates[-1], "guest-metadata-slug") if guest_candidates else ("", "")

def route_raw_input(path: Path, meta: dict[str, Any], inventory: VoiceInventory, notebook_root: Path) -> dict[str, Any]:
    guest = str(meta.get("guest") or "").strip()
    host_candidates = _host_candidates(meta)
    guessed_guest_slug, _speaker_resolution = _resolved_speaker(meta, inventory)
    matched_speaker = guessed_guest_slug if guessed_guest_slug in inventory.speaker_folders else None

    if guessed_guest_slug:
        arc = _match_arc(host_candidates, guessed_guest_slug, inventory)
        if arc:
            return _route(
                recommended_route=_rel(arc),
                route_type="existing-voice-arc",
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
            route_type="existing-voice-object",
            confidence="high",
            next_action=next_action,
            also_strengthens=also_strengthens,
            reason=f"Matched guest metadata to existing speaker object `{matched_speaker}`.",
        )

    if matched_speaker:
        candidate = _candidate_object_path(matched_speaker, inventory)
        return _route(
            recommended_route=_rel(candidate),
            route_type="candidate-voice-object",
            confidence="medium",
            next_action="create-candidate-object",
            reason=f"Matched guest metadata to speaker folder `{matched_speaker}`, but no speaker object exists yet.",
        )

    if guest and guessed_guest_slug:
        candidate = _candidate_arc_path(meta, guessed_guest_slug, notebook_root)
        return _route(
            recommended_route=_rel(candidate),
            route_type="candidate-voice-arc",
            confidence="medium",
            next_action="create-candidate-arc",
            reason="Guest metadata is present, but no existing speaker object or host-local arc matched.",
        )

    return {}

def _appearance(path: Path, meta: dict[str, Any], inventory: VoiceInventory) -> dict[str, str]:
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

def build_rows(raw_paths: list[Path], inventory: VoiceInventory, notebook_root: Path) -> list[dict[str, Any]]:
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

def build_unresolved_rows(raw_paths: list[Path], inventory: VoiceInventory) -> list[dict[str, Any]]:
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
        "# Voice routing queue",
        "",
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

    jsonl_path = window_dir / "voice-routing-queue.jsonl"
    with jsonl_path.open("w", encoding="utf-8", newline="") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n")

    md_path = window_dir / "voice-routing-queue.md"
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
    parser.add_argument("--voices-dir", type=Path, default=None, help="Voice shelf root (statecraft/voices/).")
    parser.add_argument(
        "--speakers-dir",
        type=Path,
        default=None,
        help="Deprecated alias for --voices-dir.",
    )
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUT_DIR)
    return parser.parse_args(argv)

def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    notebook_root = args.notebook_root.resolve()
    voices_dir = (args.voices_dir or args.speakers_dir or DEFAULT_VOICES_DIR).resolve()
    raw_root = notebook_root
    inventory = _discover_inventory(voices_dir, notebook_root)
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

# Compat aliases for deprecated import path
SpeakerInventory = VoiceInventory
