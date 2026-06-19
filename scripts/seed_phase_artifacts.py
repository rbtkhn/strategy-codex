"""Single source of truth for seed-phase JSON artifacts (strict validation + genesis hash).

Keep in sync with docs/seed-phase-artifacts.md. Import from sibling scripts only
when run as ``python3 scripts/<tool>.py`` (scripts/ on sys.path).
"""

from __future__ import annotations

# JSON files validated against schema-registry (order preserved for genesis hashing).
SCHEMA_BY_FILE: dict[str, str] = {
    "seed-phase-manifest.json": "schemas/registry/seed-phase-manifest.v1.json",
    "seed_intake.json": "schemas/registry/seed-intake.v1.json",
    "seed_intent.json": "schemas/registry/seed-intent.v1.json",
    "seed_identity.json": "schemas/registry/seed-identity.v1.json",
    "seed_curiosity.json": "schemas/registry/seed-curiosity.v1.json",
    "seed_pedagogy.json": "schemas/registry/seed-pedagogy.v1.json",
    "seed_expression.json": "schemas/registry/seed-expression.v1.json",
    "seed_memory_contract.json": "schemas/registry/seed-memory-contract.v1.json",
    "memory_ops_contract.json": "schemas/registry/seed-memory-ops-contract.v1.json",
    "seed_trial_report.json": "schemas/registry/seed-trial-report.v1.json",
    "seed_readiness.json": "schemas/registry/seed-readiness.v1.json",
    "seed_confidence_map.json": "schemas/registry/seed-confidence-map.v1.json",
    "work_business_seed.json": "schemas/registry/work-business-seed.v1.json",
    "work_dev_seed.json": "schemas/registry/work-dev-seed.v1.json",
    "seed_constitution.json": "schemas/registry/seed-constitution.v1.json",
}

# Keys expected in seed-phase-manifest.json "runtime/artifacts" object.
EXPECTED_ARTIFACT_KEYS = frozenset(
    {
        "seed_intake",
        "seed_intent",
        "seed_identity",
        "seed_curiosity",
        "seed_pedagogy",
        "seed_expression",
        "seed_memory_contract",
        "memory_ops_contract",
        "seed_trial_report",
        "seed_readiness",
        "seed_confidence_map",
        "work_business_seed",
        "work_dev_seed",
        "seed_constitution",
    }
)
