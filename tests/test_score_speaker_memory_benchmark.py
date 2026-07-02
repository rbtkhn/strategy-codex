from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "score_speaker_memory_benchmark.py"
SAMPLES_PATH = REPO_ROOT / "runtime/artifacts" / "benchmarks" / "speaker-memory" / "benchmark_samples.py"

def load_sample_outputs() -> dict:
    spec = importlib.util.spec_from_file_location("speaker_memory_benchmark_samples", SAMPLES_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.SAMPLE_OUTPUTS

SAMPLE_OUTPUTS = load_sample_outputs()
STRONG_SM1 = SAMPLE_OUTPUTS["sm-1-speaker-object-repair"]["strong"]
WEAK_SM1 = SAMPLE_OUTPUTS["sm-1-speaker-object-repair"]["weak"]
STRONG_SM2 = SAMPLE_OUTPUTS["sm-2-speaker-arc-ranking"]["strong"]
WEAK_SM2 = SAMPLE_OUTPUTS["sm-2-speaker-arc-ranking"]["weak"]
STRONG_SM3 = SAMPLE_OUTPUTS["sm-3-speaker-structure-metrics"]["strong"]
WEAK_SM3 = SAMPLE_OUTPUTS["sm-3-speaker-structure-metrics"]["weak"]
STRONG_SM4 = SAMPLE_OUTPUTS["sm-4-speaker-maturity-ranking"]["strong"]
WEAK_SM4 = SAMPLE_OUTPUTS["sm-4-speaker-maturity-ranking"]["weak"]

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
