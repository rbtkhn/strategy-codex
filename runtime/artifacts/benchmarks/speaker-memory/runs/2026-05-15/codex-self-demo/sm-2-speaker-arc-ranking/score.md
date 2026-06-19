# Speaker Memory Score - sm-2-speaker-arc-ranking

**Closeout:** `Held`
**Score:** `110/110` (100.0%)

## Checks

| Check | Score | Pass | Note |
|---|---:|---|---|
| `work_boundary` | 10/10 | yes | Required WORK-only boundary is present. |
| `required_sections` | 18/18 | yes | All required speaker-arc sections are present. |
| `expected_rank_order` | 18/18 | yes | Expected 2026-05-06 before 2026-04-18 ranking is present. |
| `paired_read_coverage` | 14/14 | yes | Matlock and Jiang paired-read logic is present. |
| `host_form_awareness` | 14/14 | yes | Host-conditioned form is explicit. |
| `lattice_restraint` | 12/12 | yes | Lattice is treated as a pointer surface. |
| `boundary_coverage` | 12/12 | yes | Boundary section covers 7 expected warning term(s). |
| `source_pack_restraint` | 12/12 | yes | No obvious unsupported biography markers found. |

## Failure Codes

- none

## Repair Actions

- none

## Recursive Use

Use this score as repair telemetry. Fix one high-severity repair target, rerun the scorer, and compare `percentage`, `closeout`, and `failure_codes` before treating the loop as improved.
