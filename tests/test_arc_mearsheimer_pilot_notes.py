"""Mearsheimer orthogonality pilot — host×guest arcs live in statecraft/notes/."""

from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
NOTES = REPO / "statecraft" / "notes"

CANONICAL = (
    "arc-mearsheimer-davis-host.md",
    "arc-mearsheimer-diesen-host.md",
    "arc-mearsheimer-napolitano-host.md",
)

LEGACY_STUBS = (
    REPO / "statecraft/voices/davis/davis-mearsheimer-arc.md",
    REPO / "statecraft/voices/diesen/diesen-mearsheimer-arc.md",
    REPO / "statecraft/channels/judging-freedom/napolitano-mearsheimer-arc.md",
)


def test_canonical_arcs_in_notes_with_yaml():
    for name in CANONICAL:
        path = NOTES / name
        assert path.is_file(), f"missing canonical arc {name}"
        text = path.read_text(encoding="utf-8")
        assert text.startswith("---\n")
        assert "note_type: arc" in text.split("---", 2)[1]
        assert "primary_voice: mearsheimer" in text.split("---", 2)[1]
        assert "## Arc set" in text or "## Why this guest run matters" in text


def test_legacy_paths_are_stubs_not_bodies():
    for path in LEGACY_STUBS:
        text = path.read_text(encoding="utf-8")
        assert "compat redirect" in text.lower()
        assert "Canonical:" in text
        assert len(text) < 600, f"{path.name} looks like a full body, not a stub"


def test_orthogonality_cross_links_in_notes():
    davis = (NOTES / "arc-mearsheimer-davis-host.md").read_text(encoding="utf-8")
    diesen = (NOTES / "arc-mearsheimer-diesen-host.md").read_text(encoding="utf-8")
    nap = (NOTES / "arc-mearsheimer-napolitano-host.md").read_text(encoding="utf-8")
    assert "arc-mearsheimer-napolitano-host.md" in davis
    assert "arc-mearsheimer-davis-host.md" in diesen
    assert "arc-mearsheimer-diesen-host.md" in nap
    assert "arc-mearsheimer-davis-host.md" in nap
