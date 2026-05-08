# Runtime ledger root policy close - 2026-05-08

## Scope

WORK-layer close note for the root-layout runtime/export audit follow-on.
This is not Record truth and does not change merge authority.

## What changed

- `5d009e74 Normalize root layout holdout scripts` normalized the six high-risk root-layout holdout scripts from the 2026-05-05 audit to the repo-root profile contract.
- `9c4b4e27 Normalize runtime audit writers to root` moved the runtime/export audit writers off `users/<id>/` assumptions:
  - `scripts/export_runtime_bundle.py`
  - `scripts/harness_events.py`
  - `scripts/emit_compute_ledger.py`
- `141f0bfa Ignore root compute ledger artifact` aligned `compute-ledger.jsonl` with the existing local-audit treatment for `harness-events.jsonl`.

## Policy

Root runtime ledgers are operator-local audit artifacts, not committed Record
surfaces. They may preserve local run receipts for debugging and replay, but
they do not become canonical identity, Evidence, MEMORY, or governance state.

Current local-audit treatment:

- `harness-events.jsonl` is ignored.
- `compute-ledger.jsonl` is ignored.
- runtime bundle audit JSONL remains generated/export noise.

If future work decides these ledgers should be committed, reconsider
`compute-ledger.jsonl` and `harness-events.jsonl` together. Do not promote one
without an explicit policy for the other.

## Verification receipts

- Focused regression: `python -m pytest tests/test_root_layout_holdouts.py tests/test_record_paths.py tests/test_analyze_rejection_feedback.py tests/test_import_working_identity_candidates.py` -> 26 passed.
- Runtime audit regression: `python -m pytest tests/test_compute_ledger.py tests/test_runtime_audit_root_paths.py tests/test_root_layout_holdouts.py` -> 13 passed.
- Live smoke: `python --% scripts/export_runtime_bundle.py -u strategy-codex -o .smoke-runtime-bundle`.
  - Export succeeded with bundle id `d4ddb8753571`.
  - `users/strategy-codex/` was not recreated.
  - New export receipts appended at repo root.
  - `.smoke-runtime-bundle/` was removed after verification.

## Remaining tension

Locked pytest temp directories still emit permission warnings in local status
scans (`.tmp-pytest-root-layout/` and related paths). That is environment
cleanup, not evidence of a continuing `users/strategy-codex/` compatibility
path.
