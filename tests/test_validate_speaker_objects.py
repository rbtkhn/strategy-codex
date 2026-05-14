from __future__ import annotations

import subprocess
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "scripts" / "validate_speaker_objects.py"


def run_validator(speakers_dir: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--speakers-dir", str(speakers_dir)],
        cwd=REPO,
        capture_output=True,
        text=True,
    )


def test_current_speaker_objects_validate() -> None:
    result = run_validator(REPO / "codex" / "2026" / "speakers")

    assert result.returncode == 0, result.stderr
    assert "validate_speaker_objects: OK" in result.stderr


def test_rejects_missing_open_first_link(tmp_path: Path) -> None:
    speakers_dir = tmp_path / "speakers"
    speaker_dir = speakers_dir / "example"
    speaker_dir.mkdir(parents=True)
    (speaker_dir / "example-speaker-object.md").write_text(
        """# Example speaker object

WORK only; not Record.

object_shape: stream-native

## Object shape

Example is a stream-native speaker object.

## Open first

Stay here.

## Boundaries

- Not a provenance ledger.
""",
        encoding="utf-8",
    )

    result = run_validator(speakers_dir)

    assert result.returncode == 1
    assert "`## Open first` must include at least one markdown link" in result.stderr


def test_rejects_missing_work_boundary(tmp_path: Path) -> None:
    speakers_dir = tmp_path / "speakers"
    speaker_dir = speakers_dir / "example"
    speaker_dir.mkdir(parents=True)
    (speaker_dir / "example-speaker-object.md").write_text(
        """# Example speaker object

object_shape: stream-native

## Object shape

Example is a stream-native speaker object.

## Open first

- open [example.md](example.md)

## Boundaries

- Not a provenance ledger.
""",
        encoding="utf-8",
    )

    result = run_validator(speakers_dir)

    assert result.returncode == 1
    assert "missing `WORK only; not Record.` boundary" in result.stderr


def test_rejects_unsupported_shape(tmp_path: Path) -> None:
    speakers_dir = tmp_path / "speakers"
    speaker_dir = speakers_dir / "example"
    speaker_dir.mkdir(parents=True)
    (speaker_dir / "example-speaker-object.md").write_text(
        """# Example speaker object

WORK only; not Record.

object_shape: universal-theory

## Object shape

Example is a universal theory.

## Open first

- open [example.md](example.md)

## Boundaries

- Not a provenance ledger.
""",
        encoding="utf-8",
    )

    result = run_validator(speakers_dir)

    assert result.returncode == 1
    assert "unsupported object shape `universal-theory`" in result.stderr


def test_accepts_cross_host_reinforced_shape(tmp_path: Path) -> None:
    speakers_dir = tmp_path / "speakers"
    speaker_dir = speakers_dir / "example"
    speaker_dir.mkdir(parents=True)
    (speaker_dir / "example-speaker-object.md").write_text(
        """# Example speaker object

WORK only; not Record.

object_shape: cross-host-reinforced

## Object shape

Example is a cross-host reinforced speaker object.

## Open first

- open [example.md](example.md)

## Boundaries

- Not a provenance ledger.
""",
        encoding="utf-8",
    )

    result = run_validator(speakers_dir)

    assert result.returncode == 0, result.stderr
    assert "validate_speaker_objects: OK" in result.stderr


def test_rejects_ambiguous_inferred_shape(tmp_path: Path) -> None:
    speakers_dir = tmp_path / "speakers"
    speaker_dir = speakers_dir / "example"
    speaker_dir.mkdir(parents=True)
    (speaker_dir / "example-speaker-object.md").write_text(
        """# Example speaker object

WORK only; not Record.

## Object shape

Example is a single-helix or stream-native speaker object.

## Open first

- open [example.md](example.md)

## Boundaries

- Not a provenance ledger.
""",
        encoding="utf-8",
    )

    result = run_validator(speakers_dir)

    assert result.returncode == 1
    assert "ambiguous object shape prose" in result.stderr
