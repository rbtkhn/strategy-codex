from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import scripts.validate_speaker_state_sets as validator


REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "scripts" / "validate_speaker_state_sets.py"


def run_validator(*args: str, repo_root: Path | None = None) -> subprocess.CompletedProcess[str]:
    command = [sys.executable, str(SCRIPT)]
    if repo_root is not None:
        command.extend(["--repo-root", str(repo_root)])
    command.extend(args)
    return subprocess.run(
        command,
        cwd=REPO,
        capture_output=True,
        text=True,
    )


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def rel_link(target: Path, base_file: Path) -> str:
    return Path(os.path.relpath(target, base_file.parent)).as_posix()


def test_duplicate_raw_input_link_fails_when_exact_once_declared(tmp_path: Path) -> None:
    raw = tmp_path / "codex" / "years" / "2026" / "raw-input" / "2026-01-01" / "substack-pape-one.md"
    write(raw, "# source\n")
    ledger = tmp_path / "codex" / "years" / "2026" / "pape" / "ledger.md"
    write(
        ledger,
        f"""# Ledger

WORK only; not Record.

## Source Set

| date | source |
| --- | --- |
| 2026-01-01 | [one]({rel_link(raw, ledger)}) |
| 2026-01-01 | [one again]({rel_link(raw, ledger)}) |
""",
    )

    errors = validator.validate_source_set(
        validator.SourceSetSpec(
            file=ledger.relative_to(tmp_path).as_posix(),
            expected_count=2,
            required_prefixes=("substack-pape-",),
        ),
        tmp_path,
    )

    assert any("duplicate Source Set target" in error for error in errors)


def test_missing_raw_input_target_fails(tmp_path: Path) -> None:
    ledger = tmp_path / "codex" / "years" / "2026" / "pape" / "ledger.md"
    write(
        ledger,
        """# Ledger

WORK only; not Record.

## Source Set

| date | source |
| --- | --- |
| 2026-01-01 | [missing](../provenance/2026-01-01/substack-pape-missing.md) |
""",
    )

    errors = validator.validate_source_set(
        validator.SourceSetSpec(
            file=ledger.relative_to(tmp_path).as_posix(),
            expected_count=1,
            required_prefixes=("substack-pape-",),
        ),
        tmp_path,
    )

    assert any("missing Source Set target" in error for error in errors)


def test_excluded_source_class_in_source_set_fails(tmp_path: Path) -> None:
    raw = tmp_path / "codex" / "years" / "2026" / "raw-input" / "2026-01-01" / "substack-crooke-one.md"
    write(raw, "# source\n")
    note = tmp_path / "codex" / "speakers" / "crooke" / "interviews.md"
    write(
        note,
        f"""# Interviews

WORK only; not Record.

## Source Set

| host | source |
| --- | --- |
| example | [bad]({rel_link(raw, note)}) |
""",
    )

    errors = validator.validate_source_set(
        validator.SourceSetSpec(
            file=note.relative_to(tmp_path).as_posix(),
            expected_count=1,
            excluded_patterns=("substack-crooke-",),
        ),
        tmp_path,
    )

    assert any("excluded source class" in error for error in errors)


def test_missing_host_arc_from_guest_matrix_fails(tmp_path: Path) -> None:
    arc_one = tmp_path / "codex" / "years" / "2026" / "davis" / "davis-one-speaker-arc.md"
    arc_two = tmp_path / "codex" / "years" / "2026" / "davis" / "davis-two-speaker-arc.md"
    write(arc_one, "# one\n")
    write(arc_two, "# two\n")
    matrix = tmp_path / "codex" / "speakers" / "davis" / "davis-host-wiring-2026.md"
    write(
        matrix,
        f"""# Davis host wiring

WORK only; not Record.

## Guest Transformation Matrix

| guest | arc |
| --- | --- |
| one | [arc]({rel_link(arc_one, matrix)}) |
""",
    )

    errors = validator.validate_guest_matrix(
        validator.GuestMatrixSpec(
            file=matrix.relative_to(tmp_path).as_posix(),
            arc_glob="codex/years/2026/davis/davis-*-speaker-arc.md",
            expected_count=2,
        ),
        tmp_path,
    )

    assert any("davis-two-speaker-arc.md" in error for error in errors)


def test_unregistered_speaker_folder_warns_without_failure(tmp_path: Path) -> None:
    speaker_dir = tmp_path / "statecraft" / "voices" / "example"
    speaker_dir.mkdir(parents=True)

    errors, warnings = validator.validate_all(
        repo_root=tmp_path,
        voices_dir=tmp_path / "statecraft" / "voices",
        hosts_dir=tmp_path / "statecraft" / "hosts",
        speaker="example",
    )

    assert errors == []
    assert any("no README.md" in warning for warning in warnings)
    assert any("no `example-speaker-object.md`" in warning for warning in warnings)


def test_strict_warnings_convert_warnings_to_failure(tmp_path: Path) -> None:
    (tmp_path / "statecraft" / "voices" / "example").mkdir(parents=True)

    result = run_validator(
        "--speaker",
        "example",
        "--strict-warnings",
        repo_root=tmp_path,
    )

    assert result.returncode == 1
    assert "warning(s) promoted" in result.stderr


def test_strict_state_boundary_converts_boundary_warning_to_failure(tmp_path: Path) -> None:
    speaker_dir = tmp_path / "statecraft" / "voices" / "example"
    write(
        speaker_dir / "example-speaker-object.md",
        """# Example speaker object

## Open first

- [source](../../years/2026/provenance/2026-01-01/example.md)
""",
    )

    result = run_validator(
        "--speaker",
        "example",
        "--strict-state-boundary",
        repo_root=tmp_path,
    )

    assert result.returncode == 1
    assert "missing WORK-only state boundary" in result.stderr


def test_missing_manifest_fails_for_registered_speaker(tmp_path: Path) -> None:
    result = run_validator("--speaker", "crooke", repo_root=tmp_path)

    assert result.returncode == 1
    assert "registered speaker manifest is missing" in result.stderr


def test_manifest_slug_mismatch_fails(tmp_path: Path) -> None:
    manifest = tmp_path / "statecraft" / "voices" / "crooke" / "state-set.toml"
    write(
        manifest,
        """version = 1
slug = "wrong"
compact_state_files = []
provenance_roots = ["source-archive/statecraft"]
""",
    )
    (tmp_path / "codex" / "years" / "2026" / "raw-input").mkdir(parents=True)

    result = run_validator("--speaker", "crooke", repo_root=tmp_path)

    assert result.returncode == 1
    assert "`slug` must be `crooke`" in result.stderr


def test_source_set_link_outside_declared_provenance_roots_fails(tmp_path: Path) -> None:
    raw_2025 = tmp_path / "codex" / "years" / "2025" / "raw-input" / "2025-01-01" / "substack-pape-one.md"
    write(raw_2025, "# source\n")
    raw_2026_root = tmp_path / "codex" / "years" / "2026" / "raw-input"
    raw_2026_root.mkdir(parents=True)
    ledger = tmp_path / "codex" / "years" / "2026" / "pape" / "ledger.md"
    write(
        ledger,
        f"""# Ledger

WORK only; not Record.

## Source Set

| date | source |
| --- | --- |
| 2025-01-01 | [one]({rel_link(raw_2025, ledger)}) |
""",
    )
    manifest = tmp_path / "statecraft" / "voices" / "pape" / "state-set.toml"
    write(
        manifest,
        f"""version = 1
slug = "pape"
compact_state_files = ["{ledger.relative_to(tmp_path).as_posix()}"]
provenance_roots = ["source-archive/statecraft"]

[[source_sets]]
file = "{ledger.relative_to(tmp_path).as_posix()}"
expected_count = 1
required_prefixes = ["substack-pape-"]
""",
    )

    result = run_validator("--speaker", "pape", repo_root=tmp_path)

    assert result.returncode == 1
    assert "outside provenance roots" in result.stderr


def test_current_repo_registered_state_sets_validate() -> None:
    for slug in ("pape", "crooke", "ritter", "parsi", "davis", "diesen"):
        result = run_validator("--speaker", slug)
        assert result.returncode == 0, result.stderr


def test_current_repo_manifests_load_and_counts_are_registered() -> None:
    speakers_dir = REPO / "statecraft" / "voices"
    hosts_dir = REPO / "statecraft" / "hosts"
    crooke, crooke_errors = validator.load_manifest("crooke", REPO, speakers_dir, hosts_dir)
    ritter, ritter_errors = validator.load_manifest("ritter", REPO, speakers_dir, hosts_dir)
    davis, davis_errors = validator.load_manifest("davis", REPO, speakers_dir, hosts_dir)
    diesen, diesen_errors = validator.load_manifest("diesen", REPO, speakers_dir, hosts_dir)

    assert crooke_errors == []
    assert ritter_errors == []
    assert davis_errors == []
    assert diesen_errors == []
    assert crooke is not None and crooke.source_sets[1].expected_count == 22
    assert ritter is not None and ritter.source_sets[1].expected_count == 48
    assert davis is not None and davis.guest_matrices[0].expected_count == 13
    assert diesen is not None and diesen.guest_matrices[0].expected_count == 20


def test_list_prints_registered_state_files() -> None:
    result = run_validator("--list")

    assert result.returncode == 0
    assert "crooke" in result.stdout
    assert "manifest: statecraft/voices/crooke/state-set.toml" in result.stdout
    assert "speaker state-set links" not in result.stdout
    assert "statecraft/voices/crooke/crooke-interview-appearances-2025-2026.md" in result.stdout
