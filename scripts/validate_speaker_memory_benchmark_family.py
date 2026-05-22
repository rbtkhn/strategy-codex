#!/usr/bin/env python3
"""Bundle-first validator for the speaker-memory benchmark family."""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable


REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = Path(__file__).resolve().parent
FIXTURES_DIR = REPO_ROOT / "artifacts" / "benchmarks" / "speaker-memory" / "fixtures"
README_PATH = REPO_ROOT / "artifacts" / "benchmarks" / "speaker-memory" / "README.md"
SCORE_SCRIPT_PATH = REPO_ROOT / "scripts" / "score_speaker_memory_benchmark.py"
SCORE_TEST_PATH = REPO_ROOT / "tests" / "test_score_speaker_memory_benchmark.py"
SYNC_SCRIPT_PATH = REPO_ROOT / "scripts" / "sync_portable_skills.py"
VALIDATE_SPEAKER_OBJECTS_PATH = REPO_ROOT / "scripts" / "validate_speaker_objects.py"

EXPECTED_FIXTURE_FILES = {
    "metadata.json",
    "prompt.md",
    "source-pack.md",
    "expected-output-shape.md",
    "rubric.md",
}

SAMPLE_OUTPUTS = {
    "sm-1-speaker-object-repair": {
        "strong": """# Sachs speaker object

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
""",
        "weak": """# Sachs biography

Sachs is a famous public intellectual.

## Object shape

He is important.

## Boundaries

More research may be needed.
""",
    },
    "sm-2-speaker-arc-ranking": {
        "strong": """# Diesen x Freeman speaker arc

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
""",
        "weak": """# Freeman profile

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
""",
    },
    "sm-3-speaker-structure-metrics": {
        "strong": """Freeman is the strongest shelf in this comparison set because the structure is not only dense, but visibly complete and coherent.

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
""",
        "weak": """Freeman feels mature and complete.

Composite: 5

It is just better overall.
""",
    },
    "sm-4-speaker-maturity-ranking": {
        "strong": """Freeman comes out ahead because its density, completeness, coherence, and maturity all reinforce each other rather than merely piling up files.

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
""",
        "weak": """Baud is best.

All speakers always follow the same maturity law.
""",
    },
}

WIRING_EXPECTATIONS = {
    "artifacts": [README_PATH],
    "scripts": [SCORE_SCRIPT_PATH],
    "tests": [SCORE_TEST_PATH],
}


@dataclass(frozen=True)
class CheckResult:
    name: str
    ok: bool
    detail: str


def load_module(path: Path, module_name: str) -> Any:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def run_command(argv: list[str], *, cwd: Path = REPO_ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )


def check_fixture_completeness(fixtures_dir: Path = FIXTURES_DIR) -> tuple[CheckResult, list[str]]:
    fixture_ids: list[str] = []
    missing: list[str] = []
    for fixture_dir in sorted(fixtures_dir.iterdir()):
        if not fixture_dir.is_dir() or not fixture_dir.name.startswith("sm-"):
            continue
        fixture_ids.append(fixture_dir.name)
        for filename in EXPECTED_FIXTURE_FILES:
            if not (fixture_dir / filename).is_file():
                missing.append(f"{fixture_dir.name}/{filename}")
    ok = not missing and bool(fixture_ids)
    detail = "All benchmark fixtures contain the required files." if ok else f"Missing fixture files: {', '.join(missing)}"
    return CheckResult("fixture_completeness", ok, detail), fixture_ids


def check_registry_consistency(
    scorer_module: Any,
    fixtures_dir: Path = FIXTURES_DIR,
) -> tuple[CheckResult, list[str]]:
    fixture_ids: list[str] = []
    mismatches: list[str] = []
    duplicates: set[str] = set()
    seen_ids: set[str] = set()
    missing_targets: list[str] = []

    for fixture_dir in sorted(fixtures_dir.iterdir()):
        if not fixture_dir.is_dir() or not fixture_dir.name.startswith("sm-"):
            continue
        metadata_path = fixture_dir / "metadata.json"
        if not metadata_path.is_file():
            continue
        data = json.loads(metadata_path.read_text(encoding="utf-8"))
        benchmark_id = data.get("benchmark_id")
        fixture_ids.append(fixture_dir.name)
        if benchmark_id != fixture_dir.name:
            mismatches.append(f"{fixture_dir.name} -> {benchmark_id}")
        if benchmark_id in seen_ids:
            duplicates.add(str(benchmark_id))
        else:
            seen_ids.add(str(benchmark_id))
        if benchmark_id not in scorer_module.DEFAULT_TARGETS:
            missing_targets.append(str(benchmark_id))

    problems: list[str] = []
    if mismatches:
        problems.append(f"folder/benchmark_id mismatches: {', '.join(mismatches)}")
    if duplicates:
        problems.append(f"duplicate benchmark ids: {', '.join(sorted(duplicates))}")
    if missing_targets:
        problems.append(f"missing scorer default targets: {', '.join(sorted(missing_targets))}")
    ok = not problems
    detail = "Fixture metadata and scorer registry are consistent." if ok else "; ".join(problems)
    return CheckResult("registry_consistency", ok, detail), fixture_ids


def check_scorer_smoke(
    scorer_module: Any,
    fixture_ids: list[str],
) -> CheckResult:
    failures: list[str] = []
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        for benchmark_id in fixture_ids:
            samples = SAMPLE_OUTPUTS.get(benchmark_id)
            if not samples:
                failures.append(f"{benchmark_id}: missing smoke samples")
                continue
            for strength, expected in (("strong", "Held"), ("weak", "Broke")):
                run_dir = root / benchmark_id / strength
                run_dir.mkdir(parents=True, exist_ok=True)
                (run_dir / "metadata.json").write_text(
                    json.dumps({"benchmark_id": benchmark_id}),
                    encoding="utf-8",
                )
                (run_dir / "output.md").write_text(samples[strength], encoding="utf-8")
                score = scorer_module.build_score(run_dir)
                closeout = score.get("closeout")
                if closeout != expected:
                    failures.append(f"{benchmark_id} {strength}: expected {expected}, got {closeout}")
    ok = not failures
    detail = "Strong/weak scorer smoke checks passed for sm-1..sm-4." if ok else "; ".join(failures)
    return CheckResult("scorer_smoke", ok, detail)


def check_portable_skill_verify(
    command_runner: Callable[[list[str]], subprocess.CompletedProcess[str]] = run_command,
) -> CheckResult:
    proc = command_runner(
        [
            sys.executable,
            str(SYNC_SCRIPT_PATH),
            "--verify",
            "--skill",
            "check-streams",
        ]
    )
    ok = proc.returncode == 0
    detail = "Portable skill verify passed for check-streams." if ok else (proc.stderr.strip() or proc.stdout.strip() or "Portable skill verify failed.")
    return CheckResult("portable_skill_verify", ok, detail)


def check_speaker_object_baseline(
    command_runner: Callable[[list[str]], subprocess.CompletedProcess[str]] = run_command,
) -> CheckResult:
    proc = command_runner([sys.executable, str(VALIDATE_SPEAKER_OBJECTS_PATH)])
    ok = proc.returncode == 0
    detail = "Speaker-object validator passed." if ok else (proc.stderr.strip() or proc.stdout.strip() or "Speaker-object validator failed.")
    return CheckResult("speaker_object_baseline", ok, detail)


def check_benchmark_wiring(
    fixture_ids: list[str],
) -> CheckResult:
    missing: list[str] = []
    for group, paths in WIRING_EXPECTATIONS.items():
        for benchmark_id in fixture_ids:
            if not any(benchmark_id in path.read_text(encoding="utf-8") for path in paths):
                missing.append(f"{benchmark_id} missing in {group}")
    ok = not missing
    detail = "Benchmark ids are wired in artifacts, scripts, and tests." if ok else "; ".join(missing)
    return CheckResult("benchmark_wiring", ok, detail)


def run_all_checks(
    *,
    fixtures_dir: Path = FIXTURES_DIR,
    scorer_path: Path = SCORE_SCRIPT_PATH,
    command_runner: Callable[[list[str]], subprocess.CompletedProcess[str]] = run_command,
) -> dict[str, Any]:
    scorer_module = load_module(scorer_path, "score_speaker_memory_benchmark")
    fixture_check, fixture_ids = check_fixture_completeness(fixtures_dir)
    registry_check, registry_ids = check_registry_consistency(scorer_module, fixtures_dir)
    active_ids = registry_ids or fixture_ids

    checks = [
        fixture_check,
        registry_check,
        check_scorer_smoke(scorer_module, active_ids) if active_ids else CheckResult("scorer_smoke", False, "No fixtures discovered for scorer smoke validation."),
        check_portable_skill_verify(command_runner),
        check_speaker_object_baseline(command_runner),
        check_benchmark_wiring(active_ids) if active_ids else CheckResult("benchmark_wiring", False, "No fixtures discovered for wiring validation."),
    ]
    ok = all(check.ok for check in checks)
    return {
        "ok": ok,
        "interpreter": sys.executable,
        "fixtures": active_ids,
        "checks": [asdict(check) for check in checks],
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    return parser.parse_args(argv)


def render_human(result: dict[str, Any]) -> str:
    lines = [
        "speaker-memory benchmark family: OK" if result["ok"] else "speaker-memory benchmark family: FAILED",
        f"interpreter: {result['interpreter']}",
        "",
    ]
    for check in result["checks"]:
        prefix = "PASS" if check["ok"] else "FAIL"
        lines.append(f"[{prefix}] {check['name']}: {check['detail']}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    result = run_all_checks()
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(render_human(result))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
