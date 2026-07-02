# Judgment Contracts

This file indexes the deterministic contract tests that guard strategy-codex judgment workflows. These tests do not prove that geopolitical conclusions are true. They prove that the working artifacts keep their source discipline, role boundaries, forecast discipline, path hygiene, and instrument shape under pressure.

## Contract Map

| Contract | Test | Fixture | Protects | Failure Means | Run When |
| --- | --- | --- | --- | --- | --- |
| Mercouris CIV-MEM | `tests/test_mercouris_civmem_gauntlet.py` | `tests/fixtures/mercouris_civmem_gauntlet.json` | Current-source analysis stays distinct from CIV-MEM recurrence logic. | Historical memory is being used as proof, Iran/PERSIA routing is drifting, or durable synthesis is landing on the wrong surface. | Mercouris skill, CIV-MEM, or statecraft routing changes. |
| Draft Skill Contracts | `tests/test_draft_skill_contract_gauntlets.py` | `tests/fixtures/draft_skill_contract_gauntlets.json` | Draft skills retain explicit judgment contracts instead of decorative prose. | A draft skill lacks enforceable source, role, excerpt, routing, or boundary language. | Ritter, Marandi, Parsi, Mercouris, statecraft draft skills, or expert-ledger draft skills change. |
| Statecraft Transaction Validity | `tests/test_statecraft_transaction_validity_gauntlet.py` | `tests/fixtures/statecraft_transaction_validity_gauntlet.json` | Statecraft outputs become usable instruments, not just elegant commentary. | A transaction or template lacks provenance, authority/restraint/settlement, instrument text, validity status, mirror test, falsifier, or revisit discipline. | Statecraft transaction templates or exemplar transactions change. |
| Rehome Path Hygiene | `tests/test_rehome_path_hygiene_contract.py` | `tests/fixtures/rehome_path_hygiene_contract.json` | Canonical rehome paths stay canonical. | Live tracked files are pointing back to old pre-rehome academy, speakers, raw-input, or 2025 paths, or `.gitmodules` drifted. | Rehome, path, submodule, or raw-input tooling changes. |
| Speaker Orthogonality | `tests/test_speaker_orthogonality_contract.py` | `tests/fixtures/speaker_orthogonality_contract.json` | Speaker roles stay distinct instead of collapsing into generic geopolitical analysis. | Pape, Ritter, Parsi, Crooke, Marandi, or Mercouris loses its functional difference, or a cluster/skill artifact erases role boundaries. | Speaker cluster maps, speaker skills, helix notes, or interview/source wiring changes. |
| Crisis Premise Realism | `tests/test_crisis_premise_realism_contract.py` | `tests/fixtures/crisis_premise_realism_contract.json` | Crisis premises are reclassified before drafting when attribution, intent, or object classification is weak. | The workflow is jumping from capability to intent, ignoring actor dependence, omitting accident/negligence/third-party explanations, flattening state asymmetry, or drafting before reclassification. | Crisis-test casebook, statecraft drafting skill, or statecraft transaction workflow changes. |
| Forecast Discipline | `tests/test_forecast_discipline_contract.py` | `tests/fixtures/forecast_discipline_contract.json` | Forecast ledgers remain falsifiable and source-backed. | Forecast rows lack date, source path, mechanism, falsifier, revisit trigger, status, or support language for `held` claims. | Forecast ledgers or forecast-extraction skills change. |

## Discipline Map

| Discipline | Guarded By |
| --- | --- |
| Source discipline | Mercouris CIV-MEM, Draft Skill Contracts, Forecast Discipline |
| Role discipline | Speaker Orthogonality, Draft Skill Contracts |
| Forecast discipline | Forecast Discipline, Mercouris CIV-MEM |
| Instrument discipline | Statecraft Transaction Validity |
| Premise discipline | Crisis Premise Realism, Statecraft Transaction Validity |
| Architecture/path discipline | Rehome Path Hygiene |

## Run Set

```powershell
python scripts/validate_judgment_contracts.py
```

The same suite also runs through the experimental validation group:

```powershell
python scripts/validate.py experimental
```

## New Contract Checklist

Before adding another judgment contract, define:

1. Protected judgment: what human or system judgment must not drift?
2. Source boundary: which source class counts, and which class is excluded?
3. Role boundary: which speaker, lane, skill, or statecraft role must stay distinct?
4. Failure meaning: what does a failed test imply about the artifact?
5. Fixture shape: which fields are required, and what score budget applies?
6. Score band: what counts as pass, warning, and failure?
7. Critical gates: which failures override the score?

Use `tests/fixtures/_judgment_contract_template.json` as the starting fixture shape.

## Failure Handling

When a contract fails, first classify the failure:

1. The contract is right and the artifact drifted.
2. The artifact is right and the contract is too brittle.
3. The test is permissive and missed the real drift until now.

Prefer fixing the doctrine or artifact when a failure exposes real drift. Fix the test when it punishes anti-drift language, intended provenance, or a valid source-boundary exception. Never treat a 100/100 score as proof that a geopolitical conclusion is true; it only means the artifact preserved the declared judgment shape.

## Audit Notes

The current gauntlets deliberately duplicate small helper logic. That keeps each contract readable while the family is still young. Extract shared scoring or Markdown-table helpers only after more contracts reveal a stable pattern.

The rehome path hygiene contract scans tracked files with `git ls-files` and excludes `runtime/artifacts/benchmarks/**` as historical provenance. It intentionally ignores untracked local churn.

There is no `tests/README.md` in this repo at the time of writing, so this file is the local discovery surface for judgment contracts.
