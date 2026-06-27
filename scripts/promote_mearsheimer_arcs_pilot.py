#!/usr/bin/env python3
"""Pilot: promote Mearsheimer host×guest arcs to statecraft/notes/."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
NOTES = REPO / "statecraft" / "notes"
RECEIPT = REPO / "runtime" / "artifacts" / "arc-promote-mearsheimer-pilot-receipt.json"

PROMOTIONS = (
    {
        "src": REPO / "statecraft/notes/arc-mearsheimer-davis-host.md",
        "dest": NOTES / "arc-mearsheimer-davis-host.md",
        "yaml": {
            "note_type": "arc",
            "primary_voice": "mearsheimer",
            "host_channel": "daniel-davis",
            "topic": "feasibility-bargaining-geometry",
            "span_start": "2025-01-17",
            "span_end": "2026-04-30",
            "legacy_path": "statecraft/notes/arc-mearsheimer-davis-host.md",
        },
        "stubs": (
            REPO / "statecraft/notes/arc-mearsheimer-davis-host.md",
            REPO / "statecraft/notes/arc-mearsheimer-davis-host.md",
        ),
        "title": "Davis × Mearsheimer — feasibility and bargaining geometry",
    },
    {
        "src": REPO / "statecraft/notes/arc-mearsheimer-diesen-host.md",
        "dest": NOTES / "arc-mearsheimer-diesen-host.md",
        "yaml": {
            "note_type": "arc",
            "primary_voice": "mearsheimer",
            "host_channel": "glenn-diesen",
            "topic": "structural-realism-order-transition",
            "span_start": "2025-09-07",
            "span_end": "2026-05-04",
            "legacy_path": "statecraft/notes/arc-mearsheimer-diesen-host.md",
        },
        "stubs": (
            REPO / "statecraft/notes/arc-mearsheimer-diesen-host.md",
            REPO / "statecraft/notes/arc-mearsheimer-diesen-host.md",
        ),
        "title": "Diesen × Mearsheimer — structural realism and order transition",
    },
    {
        "src": REPO / "statecraft/notes/arc-mearsheimer-napolitano-host.md",
        "dest": NOTES / "arc-mearsheimer-napolitano-host.md",
        "yaml": {
            "note_type": "arc",
            "primary_voice": "mearsheimer",
            "host_channel": "judging-freedom",
            "topic": "defeat-accounting-self-entrapment",
            "span_start": "2025-11-17",
            "span_end": "2026-04-28",
            "legacy_path": "statecraft/notes/arc-mearsheimer-napolitano-host.md",
        },
        "stubs": (
            REPO / "statecraft/notes/arc-mearsheimer-napolitano-host.md",
            REPO / "statecraft/notes/arc-mearsheimer-napolitano-host.md",
        ),
        "title": "Napolitano × Mearsheimer — defeat accounting and self-entrapment",
    },
)

CROSS_LINKS = {
    "arc-mearsheimer-davis-host.md": (
        r"\[arc-mearsheimer-davis-host\.md\][^\n]*",
        "[arc-mearsheimer-davis-host.md](arc-mearsheimer-davis-host.md)",
    ),
    "arc-mearsheimer-diesen-host.md": (
        r"\[arc-mearsheimer-diesen-host\.md\][^\n]*",
        "[arc-mearsheimer-diesen-host.md](arc-mearsheimer-diesen-host.md)",
    ),
    "arc-mearsheimer-napolitano-host.md": (
        r"\[arc-mearsheimer-napolitano-host\.md\][^\n]*",
        "[arc-mearsheimer-napolitano-host.md](arc-mearsheimer-napolitano-host.md)",
    ),
}

REWRITE_GLOBS = (
    "statecraft/voices/mearsheimer",
    "statecraft/voices/diesen",
    "statecraft/channels/daniel-davis",
    "statecraft/channels/judging-freedom",
    "statecraft/sheets",
    "codex/academy/statecraft/sheets",
    "codex/speaker-lattice.md",
    "tests/test_speaker_routing_queue.py",
)

OLD_TO_NEW = (
    ("statecraft/notes/arc-mearsheimer-davis-host.md", "statecraft/notes/arc-mearsheimer-davis-host.md"),
    ("statecraft/notes/arc-mearsheimer-diesen-host.md", "statecraft/notes/arc-mearsheimer-diesen-host.md"),
    ("statecraft/notes/arc-mearsheimer-napolitano-host.md", "statecraft/notes/arc-mearsheimer-napolitano-host.md"),
    ("../../notes/arc-mearsheimer-davis-host.md", "../../notes/arc-mearsheimer-davis-host.md"),
    ("../../notes/arc-mearsheimer-diesen-host.md", "../../notes/arc-mearsheimer-diesen-host.md"),
    ("../../notes/arc-mearsheimer-napolitano-host.md", "../../notes/arc-mearsheimer-napolitano-host.md"),
    ("../../channels/daniel-davis/arc-mearsheimer-davis-host.md", "../notes/arc-mearsheimer-davis-host.md"),
    ("../diesen/arc-mearsheimer-diesen-host.md", "../notes/arc-mearsheimer-diesen-host.md"),
    ("arc-mearsheimer-napolitano-host.md", "arc-mearsheimer-napolitano-host.md"),
    ("arc-mearsheimer-davis-host.md", "arc-mearsheimer-davis-host.md"),
    ("arc-mearsheimer-diesen-host.md", "arc-mearsheimer-diesen-host.md"),
)


def _yaml_block(meta: dict) -> str:
    lines = ["---"]
    for key, val in meta.items():
        lines.append(f"{key}: {val}")
    lines.append("---")
    return "\n".join(lines)


def _normalize_body(text: str) -> str:
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
        r"",
        text,
        flags=re.I,
    )
    text = re.sub(
        r"/C:/dev/strategy-codex/statecraft/channels/daniel-davis/arc-mearsheimer-davis-host\.md",
        "arc-mearsheimer-davis-host.md",
        text,
        flags=re.I,
    )
    text = re.sub(
        r"/C:/dev/strategy-codex/statecraft/voices/diesen/arc-mearsheimer-diesen-host\.md",
        "arc-mearsheimer-diesen-host.md",
        text,
        flags=re.I,
    )
    text = re.sub(
        r"/C:/dev/strategy-codex/statecraft/channels/judging-freedom/arc-mearsheimer-napolitano-host\.md",
        "arc-mearsheimer-napolitano-host.md",
        text,
        flags=re.I,
    )
    for _, (pattern, repl) in CROSS_LINKS.items():
        text = re.sub(pattern, repl, text)
    # fix broken link missing closing paren from prior migration
    text = re.sub(
        r"\(\../../source-archive/statecraft/([^\)]+)\.md(?!\))",
        r"(../../source-archive/statecraft/\1.md)",
        text,
    )
    return text


def _stub_body(title: str, dest_rel: str, legacy_rel: str) -> str:
    return f"""# {title} (compat redirect)

WORK only; not Record.

**Canonical:** [{dest_rel.split('/')[-1]}]({dest_rel})

Legacy path: `{legacy_rel}` — pointer only; do not duplicate arc bodies here.

Do not treat `*-speaker-arc.md` as a second arc class.
"""


def apply() -> dict:
    receipt: dict = {"promotions": [], "rewrites": []}
    for item in PROMOTIONS:
        src = item["src"]
        dest = item["dest"]
        body = src.read_text(encoding="utf-8")
        if body.lstrip().startswith("---"):
            body = body.split("---", 2)[-1].lstrip("\n")
        promoted = _yaml_block(item["yaml"]) + "\n\n" + _normalize_body(body)
        dest.write_text(promoted, encoding="utf-8", newline="\n")
        dest_rel = dest.relative_to(REPO).as_posix()
        for stub_path in item["stubs"]:
            legacy = stub_path.relative_to(REPO).as_posix()
            depth = len(stub_path.relative_to(REPO).parts) - 2
            rel_link = Path(*([".."] * depth), "notes", dest.name).as_posix()
            stub_path.write_text(
                _stub_body(item["title"], rel_link, legacy),
                encoding="utf-8",
                newline="\n",
            )
        receipt["promotions"].append({"from": src.relative_to(REPO).as_posix(), "to": dest_rel})

    for glob in REWRITE_GLOBS:
        path = REPO / glob
        files = [path] if path.is_file() else sorted(path.rglob("*.md"))
        for fp in files:
            if fp.name.startswith("arc-mearsheimer-"):
                continue
            if "compat redirect" in fp.read_text(encoding="utf-8").lower():
                continue
            text = fp.read_text(encoding="utf-8")
            orig = text
            for old, new in OLD_TO_NEW:
                text = text.replace(old, new)
            text = re.sub(
                r"/C:/dev/strategy-codex/statecraft/notes/arc-mearsheimer-([a-z-]+)\.md",
                r"../../notes/arc-mearsheimer-\1.md",
                text,
                flags=re.I,
            )
            if text != orig:
                fp.write_text(text, encoding="utf-8", newline="\n")
                receipt["rewrites"].append(fp.relative_to(REPO).as_posix())

    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    return receipt


def main() -> int:
    receipt = apply()
    print(json.dumps(receipt, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
