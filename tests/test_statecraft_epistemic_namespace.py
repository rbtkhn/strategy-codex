"""Epistemic audit namespace existence (PR1 foundation)."""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "statecraft/epistemic",
    "statecraft/epistemic/observation",
    "statecraft/epistemic/structuring",
    "statecraft/epistemic/analysis",
    "statecraft/epistemic/plugins",
    "statecraft/epistemic/pipeline",
    "statecraft/epistemic/data",
]


def test_epistemic_audit_namespace_exists() -> None:
    for rel in REQUIRED:
        assert (REPO_ROOT / rel).exists(), f"missing: {rel}"
