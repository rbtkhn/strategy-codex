"""Shared paths for runtime observation tooling."""

from __future__ import annotations

import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from repo_io import SCHEMA_REGISTRY_DIR

def ledger_base() -> Path:
    if os.environ.get("GRACE_MAR_RUNTIME_LEDGER_ROOT"):
        return Path(os.environ["GRACE_MAR_RUNTIME_LEDGER_ROOT"]).resolve()
    return REPO_ROOT

def observations_dir() -> Path:
    return ledger_base() / "runtime" / "observations"

def observations_jsonl() -> Path:
    return observations_dir() / "index.jsonl"

def runtime_observation_schema() -> Path:
    return SCHEMA_REGISTRY_DIR / "runtime-observation.v1.json"

def retrieval_misses_dir() -> Path:
    return ledger_base() / "runtime" / "retrieval-misses"

def retrieval_misses_jsonl() -> Path:
    return retrieval_misses_dir() / "index.jsonl"

def retrieval_miss_schema() -> Path:
    return SCHEMA_REGISTRY_DIR / "retrieval-miss.v1.json"

def chunks_dir_root() -> Path:
    return ledger_base() / "runtime" / "chunks"

def chunks_dir(surface: str) -> Path:
    return chunks_dir_root() / surface
