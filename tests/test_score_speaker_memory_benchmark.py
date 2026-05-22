from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "score_speaker_memory_benchmark.py"


STRONG_SM1 = """# Sachs speaker object

WORK only; not Record.

object_shape: cross-host-reinforced

## Object shape

Sachs is a cross-host-reinforced speaker object, not a mature helix.

## Open first

- open [Diesen x Sachs](/tmp/diesen-sachs.md)
- open [Sachs cross-host note](/tmp/sachs-cross-host-note.md)

## Routing use

Use this when deciding whether a new Sachs item strengthens the speaker object.

## Boundaries

- This is not raw-input provenance.
- This is not a biography.
- Do not treat Sachs as a wire-grade verifier.
- Do not claim a helix until denser host-local structure exists.
"""


WEAK_SM1 = """# Sachs biography

Sachs is a famous public intellectual.

## Object shape

He is important.

## Boundaries

More research may be needed.
"""


STRONG_SM2 = """# Diesen x Freeman speaker arc

WORK only; not Record.

Purpose: host-local conversational form, not a generic Freeman profile.

## Why this guest run matters

Inside the Diesen stream, Diesen brings out Freeman's diplomatic-memory register.

## Arc set

1. [2026-05-06 maritime dominance](/tmp/2026-05-06.md)
   Best mature anchor.
2. [2026-04-18 Freeman Diesen](/tmp/2026-04-18.md)
   Best vocabulary anchor.

## Open first

Open 2026-05-06 first.

## Best paired read

Best paired read: [diesen-matlock-speaker-arc.md](/tmp/matlock.md).
Second-best paired read: [diesen-jiang-speaker-arc.md](/tmp/jiang.md).

## Routing use

Use this arc when lattice rows can cite the arc without carrying the interpretation themselves.

## Boundary

- Not a wire substitute.
- Not a fleet fact source.
- Not cargo arithmetic.
- Not blockade verification.
- Not ORBAT.
- Not a generic Freeman profile.
"""


WEAK_SM2 = """# Freeman profile

WORK only; not Record.

## Arc set

1. 2026-04-18
2. 2026-05-06

## Open first

Open the latest thing.

## Best paired read

None.

## Routing use

Put the interpretation in the lattice because the lattice is where this belongs.

## Boundary

Freeman is broadly useful.
"""


STRONG_SM3 = """Freeman is the strongest shelf in this comparison set because the structure is not only dense, but visibly complete and coherent.

| metric | score | note |
|---|---:|---|
| density | 5 | multi-host recurrence across host-local arcs and helix surfaces |
| completeness | 4 | most known appearances are materialized, though watch URL coverage is partial |
| coherence | 5 | README, object, routing, and helix surfaces agree |
| maturity | 5 | cross-year continuity and open-first routes survive extension |

Composite: 4.7

| evidence | value |
|---|---|
| host_lanes | 4 |
| materialized_transcripts | 23 |
| host-local arcs | 4 |
| helix_present | yes |
| cross-year note | yes |
| watch_url_coverage | partial |

Notes:
- Density is structured, not mere transcript pileup.
- The main gap is partial watch URL coverage.
"""


WEAK_SM3 = """Freeman feels mature and complete.

Composite: 5

It is just better overall.
"""


STRONG_SM4 = """Freeman comes out ahead because its density, completeness, coherence, and maturity all reinforce each other rather than merely piling up files.

| speaker | density | completeness | coherence | maturity | rank |
|---|---:|---:|---:|---:|---:|
| freeman | 5 | 4 | 5 | 5 | 1 |
| crooke | 4 | 4 | 5 | 4 | 2 |
| baud | 5 | 3 | 4 | 4 | 3 |
| armstrong | 3 | 4 | 4 | 4 | 4 |

Strongest shelf:
Freeman is the top-ranked shelf and wins because its helix-first structure is backed by cross-year continuity and stable host transformations.

Most instructive mismatch case:
Baud is dense but that density does not fully translate into maturity when completeness lags. Armstrong is a thinner but cleaner single-branch mature shelf that scores above its raw volume. Crooke remains a strong cross-host reinforced comparative object rather than an embryonic shelf.
"""


WEAK_SM4 = """Baud is best.

All speakers always follow the same maturity law.
"""


def write_run(tmp_path: Path, benchmark_id: str, output: str) -> Path:
    run = tmp_path / benchmark_id
    run.mkdir()
    (run / "metadata.json").write_text(
        json.dumps({"benchmark_id": benchmark_id}), encoding="utf-8"
    )
    (run / "output.md").write_text(output, encoding="utf-8")
    return run


def score(run: Path) -> dict:
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "--run", str(run), "--no-write", "--json"],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(proc.stdout)


def test_strong_sm1_scores_held_without_repairs(tmp_path: Path) -> None:
    result = score(write_run(tmp_path, "sm-1-speaker-object-repair", STRONG_SM1))

    assert result["closeout"] == "Held"
    assert result["percentage"] >= 85
    assert result["failure_codes"] == []
    assert result["repair_actions"] == []


def test_weak_sm1_emits_object_shape_and_open_first_failures(tmp_path: Path) -> None:
    result = score(write_run(tmp_path, "sm-1-speaker-object-repair", WEAK_SM1))

    assert result["closeout"] == "Broke"
    assert "missing_object_shape" in result["failure_codes"]
    assert "weak_open_first" in result["failure_codes"]


def test_strong_sm2_scores_held(tmp_path: Path) -> None:
    result = score(write_run(tmp_path, "sm-2-speaker-arc-ranking", STRONG_SM2))

    assert result["closeout"] == "Held"
    assert result["failure_codes"] == []


def test_weak_sm2_emits_rank_and_lattice_failures(tmp_path: Path) -> None:
    result = score(write_run(tmp_path, "sm-2-speaker-arc-ranking", WEAK_SM2))

    assert result["closeout"] == "Broke"
    assert "wrong_arc_rank" in result["failure_codes"]
    assert "lattice_overload" in result["failure_codes"]


def test_missing_work_boundary_targets_source_note(tmp_path: Path) -> None:
    output = STRONG_SM2.replace("WORK only; not Record.\n\n", "")
    result = score(write_run(tmp_path, "sm-2-speaker-arc-ranking", output))

    assert "missing_work_boundary" in result["failure_codes"]
    actions = {
        action["failure_code"]: action for action in result["repair_actions"]
    }
    assert actions["missing_work_boundary"]["target_type"] == "source_note"


def test_strong_sm3_scores_held(tmp_path: Path) -> None:
    result = score(write_run(tmp_path, "sm-3-speaker-structure-metrics", STRONG_SM3))

    assert result["closeout"] == "Held"
    assert result["failure_codes"] == []


def test_weak_sm3_emits_metric_vector_failure(tmp_path: Path) -> None:
    result = score(write_run(tmp_path, "sm-3-speaker-structure-metrics", WEAK_SM3))

    assert result["closeout"] == "Broke"
    assert "missing_metric_vector" in result["failure_codes"]


def test_strong_sm4_scores_held(tmp_path: Path) -> None:
    result = score(write_run(tmp_path, "sm-4-speaker-maturity-ranking", STRONG_SM4))

    assert result["closeout"] == "Held"
    assert result["failure_codes"] == []


def test_weak_sm4_emits_ranking_and_mismatch_failures(tmp_path: Path) -> None:
    result = score(write_run(tmp_path, "sm-4-speaker-maturity-ranking", WEAK_SM4))

    assert result["closeout"] == "Broke"
    assert "insufficient_ranking_set" in result["failure_codes"]
    assert "missing_mismatch_case" in result["failure_codes"]


def test_no_write_emits_no_files_and_normal_mode_writes_outputs(tmp_path: Path) -> None:
    run = write_run(tmp_path, "sm-1-speaker-object-repair", STRONG_SM1)
    result = score(run)

    assert result["closeout"] == "Held"
    assert not (run / "score.json").exists()
    assert not (run / "score.md").exists()
    assert not (run / "repair-queue.jsonl").exists()

    subprocess.run(
        [sys.executable, str(SCRIPT), "--run", str(run)],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert (run / "score.json").exists()
    assert (run / "score.md").exists()
    assert (run / "repair-queue.jsonl").exists()
