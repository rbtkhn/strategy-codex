#!/usr/bin/env python3
"""Validate WORK-only speaker-object routing notes."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SPEAKERS_DIR = REPO_ROOT / "codex" / "2026" / "speakers"

ALLOWED_SHAPES = {
    "profile-only",
    "stream-native",
    "stream-anchored",
    "stream-anchored-with-cross-host-reinforcement",
    "cross-host-reinforced",
    "single-helix",
    "double-helix",
    "triple-helix",
    "helix-first",
}

SHAPE_PHRASES = {
    "profile-only": (
        "profile-only speaker object",
        "profile only speaker object",
    ),
    "stream-native": (
        "stream-native speaker object",
        "stream native speaker object",
    ),
    "stream-anchored": (
        "stream-anchored speaker object",
        "stream anchored speaker object",
    ),
    "stream-anchored-with-cross-host-reinforcement": (
        "stream-anchored speaker object with cross-host reinforcement",
        "stream anchored speaker object with cross host reinforcement",
    ),
    "cross-host-reinforced": (
        "cross-host reinforced speaker object",
        "cross host reinforced speaker object",
        "cross-host reinforced commentary object",
        "cross host reinforced commentary object",
    ),
    "single-helix": (
        "single-helix",
        "single helix",
    ),
    "double-helix": (
        "double-helix",
        "double helix",
    ),
    "triple-helix": (
        "triple-helix",
        "triple helix",
        "triple speaker-helix",
        "triple speaker helix",
    ),
    "helix-first": (
        "helix-first speaker object",
        "helix first speaker object",
    ),
}

HEADING_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
EXPLICIT_SHAPE_RE = re.compile(
    r"(?im)^\s*object_shape\s*:\s*([a-z0-9-]+)\s*$"
)
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\([^)]+\)")


def rel(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def section_text(text: str, heading: str) -> str:
    target = heading.casefold()
    for match in HEADING_RE.finditer(text):
        if match.group(1).strip().casefold() != target:
            continue
        start = match.end()
        next_match = HEADING_RE.search(text, start)
        end = next_match.start() if next_match else len(text)
        return text[start:end]
    return ""


def explicit_shape(text: str) -> str | None:
    match = EXPLICIT_SHAPE_RE.search(text)
    if not match:
        return None
    return match.group(1).strip()


def inferred_shapes(text: str) -> list[str]:
    object_shape_section = section_text(text, "Object shape")
    haystack = object_shape_section.casefold()
    found: list[str] = []
    for shape, phrases in SHAPE_PHRASES.items():
        if any(phrase.casefold() in haystack for phrase in phrases):
            found.append(shape)
    return found


def declared_shape(text: str) -> tuple[str | None, list[str]]:
    shape = explicit_shape(text)
    if shape:
        return shape, []
    inferred = inferred_shapes(text)
    if len(inferred) == 1:
        return inferred[0], []
    if len(inferred) > 1:
        return None, [
            "ambiguous object shape prose; add one explicit "
            "`object_shape: <shape>` line"
        ]
    return None, []


def validate_speaker_object(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []

    if "WORK only; not Record." not in text:
        errors.append(f"{rel(path)}: missing `WORK only; not Record.` boundary")

    for heading in ("Object shape", "Open first", "Boundaries"):
        if not section_text(text, heading):
            errors.append(f"{rel(path)}: missing `## {heading}` section")

    shape, shape_errors = declared_shape(text)
    for error in shape_errors:
        errors.append(f"{rel(path)}: {error}")
    if shape is None:
        if not shape_errors:
            errors.append(
                f"{rel(path)}: missing object shape declaration "
                f"(use `object_shape: <shape>` or Object shape prose)"
            )
    elif shape not in ALLOWED_SHAPES:
        allowed = ", ".join(sorted(ALLOWED_SHAPES))
        errors.append(f"{rel(path)}: unsupported object shape `{shape}`; allowed: {allowed}")

    open_first = section_text(text, "Open first")
    if open_first and not MARKDOWN_LINK_RE.search(open_first):
        errors.append(f"{rel(path)}: `## Open first` must include at least one markdown link")

    return errors


def discover_speaker_objects(speakers_dir: Path) -> list[Path]:
    if not speakers_dir.exists():
        return []
    return sorted(speakers_dir.glob("*/*-speaker-object.md"))


def validate_speakers_dir(speakers_dir: Path) -> list[str]:
    errors: list[str] = []
    for path in discover_speaker_objects(speakers_dir):
        errors.extend(validate_speaker_object(path))
    return errors


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--speakers-dir",
        type=Path,
        default=DEFAULT_SPEAKERS_DIR,
        help="Speaker shelf to validate (default: codex/speakers).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    errors = validate_speakers_dir(args.speakers_dir.resolve())
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        print(f"validate_speaker_objects: failed ({len(errors)} issue(s))", file=sys.stderr)
        return 1
    print("validate_speaker_objects: OK", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
