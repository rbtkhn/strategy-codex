# Domain-pack triage (generated)

Generated: `2026-06-24T00:54:03Z`

Inventory source: `runtime/artifacts/skill-inventory.json` (generated `2026-06-24T00:53:05Z`)

Regenerate:

```bash
python3 scripts/generate_skill_inventory.py
python3 scripts/generate_domain_pack_triage.py
```

Disposition SSOT: [`scripts/domain_pack_dispositions.yaml`](../scripts/domain_pack_dispositions.yaml)

## Summary

- **Total domain-pack rows:** 54
- **By disposition:** ARCHIVE: 9 | CONVERT_TO_RUNBOOK: 5 | KEEP_ACTIVE: 10 | PROMOTE_TO_PORTABLE: 1 | REDIRECT: 3 | REVIEW_WITH_OPERATOR: 26
- **Active + proof_standard missing:** 37 (target after full pass: 0–3)

> **Note:** `civ-state-volume-architect` is **not** domain-pack — it is `legacy-redirect` → `civ-state` in the skill inventory.

## CIV-STATE family

| name | location | manifest_listed | cursor_only | status | proof_standard | current_trigger | proposed_disposition | replacement_or_runbook | reason | risk |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| civ-state | both | True | False | active | missing | civ-state | KEEP_ACTIVE |  | Umbrella CIV-STATE entry; A-D menu router | low |
| civ-state-essay | both | True | False | active | present | civ-state essay | KEEP_ACTIVE |  | Distinct public essay path; proof present | low |
| civ-state-note | both | True | False | active | present | civ-state note | KEEP_ACTIVE |  | Atomic CIV-STATE note promotion; proof present | low |
| civ-state-primary-text-acquisition | both | True | False | active | missing |  | CONVERT_TO_RUNBOOK | civ-state-primary-text | Multi-step acquisition chain; runbook exists | low |
| civ-state-volume-harden | both | True | False | active | missing |  | CONVERT_TO_RUNBOOK | civ-state-volume-hardening | Multi-step volume hardening; runbook exists | low |

## Portable domain skills (manifest-listed)

| name | location | manifest_listed | cursor_only | status | proof_standard | current_trigger | proposed_disposition | replacement_or_runbook | reason | risk |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| jurisdiction-campaign-history | both | True | False | active | missing | jurisdiction history | KEEP_ACTIVE |  | work-politics campaign history primitive | medium |
| politics-massie | both | True | False | active | missing | massie x | KEEP_ACTIVE |  | Standing work-politics domain skill; practical output | low |
| work-jiang-ingest-fallback | both | True | False | active | missing | jiang ingest fallback | KEEP_ACTIVE |  | Narrow ingest fallback; keep if still invoked | medium |

## State-lane openers

| name | location | manifest_listed | cursor_only | status | proof_standard | current_trigger | proposed_disposition | replacement_or_runbook | reason | risk |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| state-america | cursor-only | False | True | active | missing | state-america | KEEP_ACTIVE |  | Active lane opener; frequently invoked | low |
| state-china | cursor-only | False | True | active | missing | state-china | KEEP_ACTIVE |  | Active lane opener; frequently invoked | low |
| state-deploy | cursor-only | False | True | active | missing | state-deploy | REVIEW_WITH_OPERATOR |  | Lane router; archive unless operator confirms active use | medium |
| state-persia | cursor-only | False | True | active | missing | state-persia | KEEP_ACTIVE |  | Active lane opener; frequently invoked | low |
| state-russia | cursor-only | False | True | active | missing | state-russia | KEEP_ACTIVE |  | Active lane opener; frequently invoked | low |

## Country culture (art / lit / god)

| name | location | manifest_listed | cursor_only | status | proof_standard | current_trigger | proposed_disposition | replacement_or_runbook | reason | risk |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| america-art | cursor-only | False | True | active | missing | america-art | ARCHIVE |  | Low-frequency subordinate lens; confirm before Commit 4 | confirm_before_commit_4 |
| america-lit | cursor-only | False | True | active | missing | america-lit | ARCHIVE |  | Low-frequency subordinate lens; confirm before Commit 4 | confirm_before_commit_4 |
| china-art | cursor-only | False | True | active | missing | china-art | ARCHIVE |  | Low-frequency subordinate lens; confirm before Commit 4 | confirm_before_commit_4 |
| china-lit | cursor-only | False | True | active | missing | china-lit | ARCHIVE |  | Low-frequency subordinate lens; confirm before Commit 4 | confirm_before_commit_4 |
| iran-art | cursor-only | False | True | active | missing | iran-art | ARCHIVE |  | Low-frequency subordinate lens; confirm before Commit 4 | confirm_before_commit_4 |
| iran-lit | cursor-only | False | True | active | missing | iran-lit | ARCHIVE |  | Low-frequency subordinate lens; confirm before Commit 4 | confirm_before_commit_4 |
| russia-art | cursor-only | False | True | active | missing | russia-art | ARCHIVE |  | Low-frequency subordinate lens; confirm before Commit 4 | confirm_before_commit_4 |
| russia-god | cursor-only | False | True | active | missing | russia-god | ARCHIVE |  | Low-frequency subordinate lens; confirm before Commit 4 | confirm_before_commit_4 |
| russia-lit | cursor-only | False | True | active | missing | russia-lit | ARCHIVE |  | Low-frequency subordinate lens; confirm before Commit 4 | confirm_before_commit_4 |

## General domain helpers

| name | location | manifest_listed | cursor_only | status | proof_standard | current_trigger | proposed_disposition | replacement_or_runbook | reason | risk |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| lane-survey | cursor-only | False | True | active | missing | survey | CONVERT_TO_RUNBOOK | domain-lane-survey | Composed landscape scan; not a single primitive | low |
| pros-and-cons | cursor-only | False | True | active | missing | unpack | REDIRECT | domain-lane-survey | Overlaps lane-survey / think-lane fork; redirect or archive | medium |
| strategy-notebook-lane-split | cursor-only | False | True | active | missing | lane split | REDIRECT |  | Legacy notebook routing; redirect to current docs or archive | medium |

## Speaker / intake / bridge

| name | location | manifest_listed | cursor_only | status | proof_standard | current_trigger | proposed_disposition | replacement_or_runbook | reason | risk |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| speaker-relations-membrane | cursor-only | False | True | active | missing | speaker membrane | REVIEW_WITH_OPERATOR | speaker-shelf-maintenance | Specialized membrane audit; keep or fold into runbook | medium |
| speaker-shelf-hygiene | cursor-only | False | True | active | missing | speaker shelf | CONVERT_TO_RUNBOOK | speaker-shelf-maintenance | Repeatable shelf maintenance step | low |
| speaker-structural-continuity | cursor-only | False | True | active | missing |  | CONVERT_TO_RUNBOOK | speaker-shelf-maintenance | Multi-step continuity check; compose in runbook | low |
| statecraft-bridge | cursor-only | False | True | active | missing | statecraft-bridge | REDIRECT | bridge | Overlaps operator bridge skill; redirect or archive | medium |
| statecraft-lane-intake-router | cursor-only | False | True | active | missing | statecraft-lane-intake-router | PROMOTE_TO_PORTABLE |  | Active routing primitive for lane intake | low |

## Work-lane cursor skills

| name | location | manifest_listed | cursor_only | status | proof_standard | current_trigger | proposed_disposition | replacement_or_runbook | reason | risk |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| skill-cici | cursor-only | False | True | active | missing | skill-cici | REVIEW_WITH_OPERATOR |  | Cici lane entry; may need category review (not pure domain-pack) | medium |
| skill-jiang | cursor-only | False | True | active | missing | skill-jiang | REVIEW_WITH_OPERATOR |  | work-jiang lane entry; may need category review | medium |
| skill-write | cursor-only | False | True | active | missing | skill-write | REVIEW_WITH_OPERATOR |  | Likely mis-categorized; product-narrative candidate | medium |
| weekly-brief-run | cursor-only | False | True | active | missing | weekly brief | REVIEW_WITH_OPERATOR |  | work-politics weekly brief; confirm keep vs runbook | medium |
| work-jiang-feature-checklist | cursor-only | False | True | active | missing | jiang check | REVIEW_WITH_OPERATOR |  | Jiang feature checklist; confirm active use | medium |

## Other cursor-only domain-pack

| name | location | manifest_listed | cursor_only | status | proof_standard | current_trigger | proposed_disposition | replacement_or_runbook | reason | risk |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| anyang-ai | cursor-only | False | True | active | missing | anyang-ai | REVIEW_WITH_OPERATOR |  | Cici cohort localization; confirm keep or archive | medium |
| brewmind-governed-steward | cursor-only | False | True | active | missing | brewmind governed steward | REVIEW_WITH_OPERATOR |  | BrewMind × Cici steward; confirm active use | medium |
| hn-bookshelf-lookup | cursor-only | False | True | active | missing |  | REVIEW_WITH_OPERATOR |  | History notebook lookup helper; low-frequency | medium |
| skill-elicitation | cursor-only | False | True | active | missing | elicit | REVIEW_WITH_OPERATOR |  | Bounded elicitation pass; confirm vs operator-coherence | medium |

## Drafts (domain-pack)

| name | location | manifest_listed | cursor_only | status | proof_standard | current_trigger | proposed_disposition | replacement_or_runbook | reason | risk |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| academy-statecraft-drafting | draft | False | True | draft | n/a | statecraft | REVIEW_WITH_OPERATOR |  | Draft; defer promote/archive to Commit 7 | low |
| cici-ai-daily-brief | draft | False | True | draft | n/a | cici daily brief | REVIEW_WITH_OPERATOR |  | Draft; defer to Commit 7 | low |
| context-folder-assembly | draft | False | True | draft | n/a | context folder | REVIEW_WITH_OPERATOR |  | Draft; defer to Commit 7 | low |
| daily-brief-regen-merge | draft | False | True | draft | n/a | daily brief regen | REVIEW_WITH_OPERATOR |  | Draft; defer to Commit 7 | low |
| expert-forecast-ledger | draft | False | True | draft | n/a | forecast ledger for <expert> | REVIEW_WITH_OPERATOR |  | Draft; defer to Commit 7 | low |
| fast-tools-finish | draft | False | True | draft | n/a |  | REVIEW_WITH_OPERATOR |  | Draft; defer to Commit 7 | low |
| graceful-constraint-reporting | draft | False | True | draft | n/a | graceful report | REVIEW_WITH_OPERATOR |  | Draft; defer to Commit 7 | low |
| marandi-state-extraction | draft | False | True | draft | n/a | marandi-state | REVIEW_WITH_OPERATOR |  | Draft extraction skill; defer to Commit 7 | low |
| mercouris-daily-continuity-extraction | draft | False | True | draft | n/a | mercouris-continuity | REVIEW_WITH_OPERATOR |  | Draft extraction skill; defer to Commit 7 | low |
| observability-to-cadence-capture | draft | False | True | draft | n/a | observability capture | REVIEW_WITH_OPERATOR |  | Draft; defer to Commit 7 | low |
| parsi-diplomacy-extraction | draft | False | True | draft | n/a | parsi-diplomacy | REVIEW_WITH_OPERATOR |  | Draft extraction skill; defer to Commit 7 | low |
| persian-regime-adaptive-strategy | draft | False | True | draft | n/a | regime strategy | REVIEW_WITH_OPERATOR |  | Draft; defer to Commit 7 | low |
| printing-press-scrape-creators | draft | False | True | draft | n/a |  | REVIEW_WITH_OPERATOR |  | Draft; defer to Commit 7 | low |
| ritter-warning-extraction | draft | False | True | draft | n/a | ritter-warning | REVIEW_WITH_OPERATOR |  | Draft extraction skill; defer to Commit 7 | low |
| russian-endurance-compression-strategy | draft | False | True | draft | n/a | endurance strategy | REVIEW_WITH_OPERATOR |  | Draft; defer to Commit 7 | low |

## Runbook cross-reference

| Runbook | Status | Path |
| --- | --- | --- |
| `civ-state-primary-text` | **exists** | `skills/runbooks/civ-state-primary-text.runbook.md` |
| `civ-state-volume-hardening` | **exists** | `skills/runbooks/civ-state-volume-hardening.runbook.md` |
| `domain-lane-survey` | **planned Commit 5** | `skills/runbooks/domain-lane-survey.runbook.md` |
| `speaker-shelf-maintenance` | **planned Commit 6** | `skills/runbooks/speaker-shelf-maintenance.runbook.md` |
