"""Shelf arcs live in statecraft/notes/; voices/channels keep compat redirects only."""

from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
NOTES = REPO / "statecraft" / "notes"
VOICES = REPO / "statecraft" / "voices"
CHANNELS = REPO / "statecraft" / "channels"
SKIP = frozenset({"_scratch", "_templates", "map", "relations"})

BODY_MARKERS = (
    "## Arc set",
    "Purpose: compact reuse note",
    "Purpose: define the current",
    "## Why this guest run matters",
)


def _shelf_arc_files(root: Path) -> list[Path]:
    out: list[Path] = []
    for path in root.rglob("*.md"):
        if any(p in SKIP for p in path.parts):
            continue
        if path.name.endswith("-arc.md") or path.name.endswith("-speaker-arc.md"):
            out.append(path)
    return out


def test_no_load_bearing_arc_bodies_on_shelves():
    offenders: list[str] = []
    for root in (VOICES, CHANNELS):
        for path in _shelf_arc_files(root):
            text = path.read_text(encoding="utf-8")
            if "compat redirect" in text.lower():
                continue
            if any(marker in text for marker in BODY_MARKERS):
                offenders.append(str(path.relative_to(REPO)))
    assert not offenders, "arc bodies remain on shelves:\n" + "\n".join(offenders[:20])


def test_notes_arc_inventory_minimum():
    arcs = list(NOTES.glob("arc-*.md"))
    assert len(arcs) >= 90


def test_mearsheimer_orthogonality_trio_in_notes():
    for name in (
        "arc-mearsheimer-davis-host.md",
        "arc-mearsheimer-diesen-host.md",
        "arc-mearsheimer-napolitano-host.md",
    ):
        path = NOTES / name
        assert path.is_file()
        assert "note_type: arc" in path.read_text(encoding="utf-8").split("---", 2)[1]
