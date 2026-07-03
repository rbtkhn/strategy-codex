# Validation Family Close — 2026-05-06

## Status

The validation-family cleanup pass is complete enough for the current local runtime.

Current outcome:

- `python scripts/validate.py fast` -> pass
- `python scripts/validate.py ci` -> pass with one explicit skip
- `python scripts/validate.py full` -> pass with one explicit skip

## What was fixed

- root-layout CLI compatibility for `assert_canonical_paths.py`
- BOM-tolerant JSON reads in:
  - `validate_structured_files.py`
  - `validate_template_sync_contract.py`
- quieter, more trustworthy structured-validation warnings
- explicit local skip behavior in `validate.py` for optional dependency failures that announce:
  - `ERROR: PyYAML is required for ...`

## Remaining seam

The only remaining validator skip in this runtime is:

- `scripts/work_dev/validate_control_plane.py`

That skip is **not** validation-family residue in the ordinary sense. It is a separate dependency decision:

- either standardize `PyYAML` for the work-dev control-plane workflow
- or design a narrow parser / alternate reader for that control-plane YAML subset

## Decision

Do **not** continue treating `validate_control_plane.py` as generic validator polish.

It should be handled later as its own wedge:

- `work-dev control plane dependency`

That preserves the distinction between:

- validation-stack repair
- and work-dev control-plane architecture
